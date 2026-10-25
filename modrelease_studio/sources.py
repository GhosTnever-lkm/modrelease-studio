from __future__ import annotations

import errno
import hashlib
import os
import stat
import zipfile
import zlib
from pathlib import Path, PurePosixPath

from .models import FileRecord, Finding, Source

MAX_ENTRIES = 30_000
MAX_TOTAL_UNCOMPRESSED = 4 * 1024 * 1024 * 1024
MAX_TEXT_FILE = 2 * 1024 * 1024
IGNORED_DIRS = {".git", ".github", "node_modules", "__pycache__", ".venv"}
WINDOWS_RESERVED_BASENAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


def _safe_os_error_code(error: OSError) -> str:
    """Return a portable code without embedding the exception's local path."""
    code = getattr(error, "errno", None)
    label = errno.errorcode.get(code) if code is not None else None
    if label:
        return label
    winerror = getattr(error, "winerror", None)
    return f"WINERROR_{winerror}" if winerror is not None else "OS_ERROR"


def _is_junction(path: Path) -> bool:
    """Check for a Windows directory junction on supported Python versions."""
    check = getattr(path, "is_junction", None)
    if check is not None:
        return bool(check())
    if os.name != "nt":
        return False

    metadata = os.lstat(path)
    attributes = getattr(metadata, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    mount_point_tag = getattr(stat, "IO_REPARSE_TAG_MOUNT_POINT", None)
    return bool(
        reparse_flag
        and attributes & reparse_flag
        and stat.S_ISDIR(metadata.st_mode)
        and mount_point_tag is not None
        and getattr(metadata, "st_reparse_tag", None) == mount_point_tag
    )


class DirectorySource(Source):
    def __init__(self, target: Path):
        findings: list[Finding] = []
        records: list[FileRecord] = []
        identities: dict[str, tuple[int, int, int, int]] = {}

        def on_walk_error(error: OSError) -> None:
            filename = getattr(error, "filename", None)
            try:
                relative = Path(filename).relative_to(target).as_posix() if filename else "."
            except ValueError:
                relative = "."
            findings.append(Finding("SCAN_DIRECTORY", "ERROR", relative,
                                    f"Could not scan directory ({_safe_os_error_code(error)})."))

        try:
            limit_reached = False
            entry_count = 0
            for current, directories, filenames in os.walk(
                target, topdown=True, onerror=on_walk_error, followlinks=False
            ):
                current_path = Path(current)
                directories.sort(key=str.casefold)
                filenames.sort(key=str.casefold)

                # Prune generated/dependency folders before traversing them so
                # they cannot consume the bounded entry index.
                for name in list(directories):
                    item = current_path / name
                    rel = item.relative_to(target).as_posix()
                    try:
                        if item.is_symlink():
                            findings.append(Finding("SYMLINK", "WARNING", rel,
                                                    "Symbolic link is not followed during scanning.",
                                                    "Replace it with a regular file or document why it is required."))
                            directories.remove(name)
                        elif _is_junction(item):
                            findings.append(Finding("JUNCTION", "WARNING", rel,
                                                    "Directory junction is not followed during scanning.",
                                                    "Replace it with a regular directory or document why it is required."))
                            directories.remove(name)
                        elif name.casefold() in IGNORED_DIRS:
                            directories.remove(name)
                    except OSError as exc:
                        # If link/junction status cannot be checked, fail closed
                        # rather than letting os.walk enter an unverified path.
                        directories.remove(name)
                        findings.append(Finding("READ_METADATA", "WARNING", rel,
                                                f"Could not read file metadata ({_safe_os_error_code(exc)}).",
                                                "Check file permissions and retry."))

                available_entries = sorted(
                    [(name, True) for name in directories]
                    + [(name, False) for name in filenames],
                    key=lambda entry: (entry[0].casefold(), entry[0]),
                )
                remaining = MAX_ENTRIES - entry_count
                if len(available_entries) > remaining:
                    findings.append(Finding("ENTRY_LIMIT", "ERROR", ".",
                                            f"More than {MAX_ENTRIES} filesystem entries were found.",
                                            "Split the release or remove generated build output."))
                    available_entries = available_entries[:remaining]
                    limit_reached = True
                entry_count += len(available_entries)
                selected_directories = {name for name, is_directory in available_entries if is_directory}
                selected_files = {name for name, is_directory in available_entries if not is_directory}
                directories[:] = [name for name in directories if name in selected_directories]
                filenames = [name for name in filenames if name in selected_files]

                for name in filenames:
                    item = current_path / name
                    rel = item.relative_to(target).as_posix()
                    try:
                        metadata = item.stat(follow_symlinks=False)
                        if stat.S_ISLNK(metadata.st_mode):
                            findings.append(Finding("SYMLINK", "WARNING", rel,
                                                    "Symbolic link is not followed during scanning.",
                                                    "Replace it with a regular file or document why it is required."))
                            continue
                        if stat.S_ISREG(metadata.st_mode):
                            records.append(FileRecord(rel, metadata.st_size))
                            identities[rel] = _file_identity(metadata)
                    except OSError as exc:
                        findings.append(Finding("READ_METADATA", "WARNING", rel,
                                                f"Could not read file metadata ({_safe_os_error_code(exc)}).",
                                                "Check file permissions and retry."))
                if limit_reached:
                    break
        except OSError as exc:
            findings.append(Finding("SCAN_DIRECTORY", "ERROR", ".",
                                    f"Could not scan directory ({_safe_os_error_code(exc)})."))
        super().__init__(target=target, records=records, findings=findings, is_zip=False)
        self._record_paths = {record.path for record in records}
        self._record_identities = identities
        self._changed_paths: set[str] = set()

    def _mark_changed(self, relative_path: str) -> None:
        if relative_path in self._changed_paths:
            return
        self._changed_paths.add(relative_path)
        self.findings.append(Finding(
            "FILE_CHANGED_DURING_SCAN", "ERROR", relative_path,
            "File identity or metadata changed after the directory was indexed; content checks were skipped.",
            "Stop modifying the selected folder and run the scan again.",
        ))

    def _safe_record_path(self, relative_path: str) -> Path | None:
        """Return an indexed regular file path without following symlinks."""
        relative = PurePosixPath(relative_path)
        if (relative_path not in self._record_paths or relative.is_absolute()
                or not relative.parts or ".." in relative.parts):
            return None
        expected = self._record_identities.get(relative_path)
        file_path = self.target
        try:
            for part in relative.parts:
                file_path = file_path / part
                if file_path.is_symlink() or _is_junction(file_path):
                    self._mark_changed(relative_path)
                    return None
            metadata = file_path.stat(follow_symlinks=False)
            if (expected is None or not stat.S_ISREG(metadata.st_mode)
                    or _file_identity(metadata) != expected):
                self._mark_changed(relative_path)
                return None
            resolved = file_path.resolve(strict=True)
            root = self.target.resolve(strict=True)
            if root not in resolved.parents or not resolved.is_file():
                self._mark_changed(relative_path)
                return None
        except (OSError, RuntimeError):
            self._mark_changed(relative_path)
            return None
        return file_path

    def _open_indexed_file(self, relative_path: str):
        file_path = self._safe_record_path(relative_path)
        if file_path is None:
            return None
        expected = self._record_identities[relative_path]
        flags = os.O_RDONLY
        flags |= getattr(os, "O_NOFOLLOW", 0)
        flags |= getattr(os, "O_NONBLOCK", 0)
        flags |= getattr(os, "O_BINARY", 0)
        descriptor = None
        try:
            descriptor = os.open(file_path, flags)
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode) or _file_identity(metadata) != expected:
                self._mark_changed(relative_path)
                return None
            stream = os.fdopen(descriptor, "rb")
            descriptor = None
            return stream
        except (OSError, ValueError):
            self._mark_changed(relative_path)
            return None
        finally:
            if descriptor is not None:
                os.close(descriptor)

    def read(self, relative_path: str, limit: int) -> bytes | None:
        stream = self._open_indexed_file(relative_path)
        if stream is None:
            return None
        try:
            with stream:
                content = stream.read(limit + 1)
                if _file_identity(os.fstat(stream.fileno())) != self._record_identities[relative_path]:
                    self._mark_changed(relative_path)
                    return None
                return content
        except (OSError, ValueError):
            self._mark_changed(relative_path)
            return None

    def digest(self) -> str:
        if self.target.is_file():
            return _sha256_file(self.target)
        hasher = hashlib.sha256()
        for record in sorted(self.records, key=lambda item: item.path.casefold()):
            hasher.update(record.path.encode("utf-8", "surrogatepass"))
            hasher.update(b"\0")
            stream = self._open_indexed_file(record.path)
            if stream is None:
                hasher.update(b"UNREADABLE")
                hasher.update(b"\0")
                continue
            try:
                with stream:
                    while chunk := stream.read(1024 * 1024):
                        hasher.update(chunk)
                    if _file_identity(os.fstat(stream.fileno())) != self._record_identities[record.path]:
                        self._mark_changed(record.path)
            except OSError:
                self._mark_changed(record.path)
                hasher.update(b"UNREADABLE")
            hasher.update(b"\0")
        return hasher.hexdigest()


class ZipSource(Source):
    def __init__(self, target: Path):
        findings: list[Finding] = []
        records: list[FileRecord] = []
        self._index: dict[str, zipfile.ZipInfo] = {}
        self.contents_available = True
        self._archive_identity: tuple[int, int, int, int] | None = None
        self._archive_changed = False
        try:
            self._archive_identity = _file_identity(target.stat(follow_symlinks=False))
            with zipfile.ZipFile(target) as archive:
                infos = archive.infolist()
                if len(infos) > MAX_ENTRIES:
                    findings.append(Finding("ENTRY_LIMIT", "ERROR", target.name,
                                            f"Archive contains more than {MAX_ENTRIES} entries.",
                                            "Create a smaller release archive."))
                    infos = infos[:MAX_ENTRIES]
                total_size = 0
                exact_seen: set[str] = set()
                for info in infos:
                    raw = info.filename
                    normalized = raw.replace("\\", "/")
                    path = PurePosixPath(normalized)
                    rel = path.as_posix()
                    windows_nonportable = any(
                        part.endswith((" ", "."))
                        or part.split(".", 1)[0].upper() in WINDOWS_RESERVED_BASENAMES
                        for part in path.parts
                    )
                    unsafe = (not path.parts or normalized.startswith("/") or ".." in path.parts
                              or any(":" in part for part in path.parts)
                              or "\x00" in raw or windows_nonportable)
                    if unsafe:
                        findings.append(Finding("UNSAFE_PATH", "ERROR", raw,
                                                "Archive entry has an absolute, parent-traversal, drive/stream-qualified, or Windows-nonportable path.",
                                                "Rebuild the ZIP using portable relative paths without drive, stream, reserved-name, or trailing-dot/space syntax."))
                        continue
                    if "\\" in raw:
                        findings.append(Finding("BACKSLASH_PATH", "WARNING", raw,
                                                "Archive path uses backslashes and may unpack inconsistently.",
                                                "Use forward slashes in ZIP entry names."))
                    if info.is_dir():
                        continue
                    if rel in exact_seen:
                        findings.append(Finding("DUPLICATE_PATH", "ERROR", rel,
                                                "The archive contains the same path more than once.",
                                                "Remove duplicate entries before publishing."))
                        continue
                    exact_seen.add(rel)
                    mode = (info.external_attr >> 16) & 0xFFFF
                    if stat.S_ISLNK(mode):
                        findings.append(Finding("ZIP_SYMLINK", "WARNING", rel,
                                                "Archive contains a symbolic-link entry.",
                                                "Avoid shipping symlinks unless the target platform supports them."))
                        continue
                    file_type = stat.S_IFMT(mode)
                    if file_type not in {0, stat.S_IFREG}:
                        findings.append(Finding("UNSAFE_SPECIAL_ENTRY", "ERROR", rel,
                                                "Archive entry is a non-regular filesystem object.",
                                                "Rebuild the release archive with regular files and directories only."))
                        continue
                    if info.flag_bits & 0x1:
                        findings.append(Finding("ENCRYPTED_ENTRY", "ERROR", rel,
                                                "Encrypted entries cannot be inspected without a password.",
                                                "Publish an unencrypted archive."))
                        continue
                    records.append(FileRecord(rel, info.file_size, info.compress_size))
                    self._index[rel] = info
                    total_size += info.file_size
                    if info.file_size > 0 and info.compress_size == 0:
                        findings.append(Finding("SUSPICIOUS_COMPRESSION", "ERROR", rel,
                                                "File has a non-zero unpacked size and zero compressed size.",
                                                "Recreate the archive with a standard ZIP tool."))
                    elif info.compress_size and info.file_size / info.compress_size > 1000:
                        findings.append(Finding("EXTREME_RATIO", "WARNING", rel,
                                                "File compression ratio exceeds 1000:1.",
                                                "Review this file; highly compressed entries can cause extraction problems."))
                if total_size > MAX_TOTAL_UNCOMPRESSED:
                    self.contents_available = False
                    findings.append(Finding("ARCHIVE_SIZE_LIMIT", "ERROR", target.name,
                                            "Unpacked archive size exceeds 4 GiB scan limit.",
                                            "Split the release into smaller archives."))
        except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
            code = _safe_os_error_code(exc) if isinstance(exc, OSError) else type(exc).__name__
            findings.append(Finding("INVALID_ZIP", "ERROR", target.name,
                                    f"The file could not be read as a valid ZIP archive ({code}).",
                                    "Recreate the archive and open it once in a ZIP utility before release."))
        super().__init__(target=target, records=records, findings=findings, is_zip=True)
        if not self._archive_matches_index():
            self._mark_archive_changed()

    def _archive_matches_index(self) -> bool:
        if self._archive_identity is None:
            return False
        try:
            current = _file_identity(self.target.stat(follow_symlinks=False))
        except OSError:
            return False
        return current == self._archive_identity

    def _mark_archive_changed(self) -> None:
        if self._archive_changed:
            return
        self._archive_changed = True
        self.contents_available = False
        self.findings.append(Finding(
            "FILE_CHANGED_DURING_SCAN", "ERROR", self.target.name,
            "Archive identity or metadata changed after it was indexed; content checks were skipped.",
            "Stop modifying the selected archive and run the scan again.",
        ))

    def read(self, relative_path: str, limit: int) -> bytes | None:
        if not self.contents_available:
            return None
        if not self._archive_matches_index():
            self._mark_archive_changed()
            return None
        info = self._index.get(relative_path)
        if info is None:
            return None
        try:
            with zipfile.ZipFile(self.target) as archive, archive.open(info) as stream:
                content = stream.read(limit + 1)
            if not self._archive_matches_index():
                self._mark_archive_changed()
                return None
            return content
        except (OSError, RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile, zlib.error):
            if not self._archive_matches_index():
                self._mark_archive_changed()
            return None

    def digest(self) -> str:
        if not self._archive_matches_index():
            self._mark_archive_changed()
        try:
            digest = _sha256_file(self.target)
        except OSError:
            self._mark_archive_changed()
            return hashlib.sha256(b"").hexdigest()
        if not self._archive_matches_index():
            self._mark_archive_changed()
        return digest


def open_source(target: str | Path) -> Source:
    path = Path(target).expanduser().resolve()
    if path.is_dir():
        return DirectorySource(path)
    if path.is_file() and path.suffix.casefold() == ".zip":
        return ZipSource(path)
    raise ValueError("Input must be a directory or a .zip archive.")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _file_identity(metadata: os.stat_result) -> tuple[int, int, int, int]:
    """Capture stable identity and common in-place-change metadata."""
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        getattr(metadata, "st_mtime_ns", int(metadata.st_mtime * 1_000_000_000)),
    )
