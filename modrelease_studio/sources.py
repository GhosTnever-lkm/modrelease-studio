from __future__ import annotations

import hashlib
import os
import stat
import zipfile
from pathlib import Path, PurePosixPath

from .models import FileRecord, Finding, Source

MAX_ENTRIES = 30_000
MAX_TOTAL_UNCOMPRESSED = 4 * 1024 * 1024 * 1024
MAX_TEXT_FILE = 2 * 1024 * 1024


class DirectorySource(Source):
    def __init__(self, target: Path):
        findings: list[Finding] = []
        records: list[FileRecord] = []
        try:
            for item in target.rglob("*"):
                rel = item.relative_to(target).as_posix()
                try:
                    if item.is_symlink():
                        findings.append(Finding("SYMLINK", "WARNING", rel,
                                                "Symbolic link is not followed during scanning.",
                                                "Replace it with a regular file or document why it is required."))
                        continue
                    if item.is_file():
                        records.append(FileRecord(rel, item.stat().st_size))
                        if len(records) > MAX_ENTRIES:
                            findings.append(Finding("ENTRY_LIMIT", "ERROR", ".",
                                                    f"More than {MAX_ENTRIES} files were found.",
                                                    "Split the release or remove generated build output."))
                            records = records[:MAX_ENTRIES]
                            break
                except OSError as exc:
                    findings.append(Finding("READ_METADATA", "WARNING", rel,
                                            f"Could not read file metadata: {exc}",
                                            "Check file permissions and retry."))
        except OSError as exc:
            findings.append(Finding("SCAN_DIRECTORY", "ERROR", ".",
                                    f"Could not scan directory: {exc}"))
        super().__init__(target=target, records=records, findings=findings, is_zip=False)

    def read(self, relative_path: str, limit: int) -> bytes | None:
        file_path = self.target.joinpath(*PurePosixPath(relative_path).parts)
        try:
            with file_path.open("rb") as stream:
                return stream.read(limit + 1)
        except (OSError, ValueError):
            return None

    def digest(self) -> str:
        if self.target.is_file():
            return _sha256_file(self.target)
        hasher = hashlib.sha256()
        for record in sorted(self.records, key=lambda item: item.path.casefold()):
            hasher.update(record.path.encode("utf-8", "surrogatepass"))
            hasher.update(b"\0")
            file_path = self.target.joinpath(*PurePosixPath(record.path).parts)
            with file_path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    hasher.update(chunk)
            hasher.update(b"\0")
        return hasher.hexdigest()


class ZipSource(Source):
    def __init__(self, target: Path):
        findings: list[Finding] = []
        records: list[FileRecord] = []
        self._index: dict[str, zipfile.ZipInfo] = {}
        try:
            with zipfile.ZipFile(target) as archive:
                infos = archive.infolist()
                if len(infos) > MAX_ENTRIES:
                    findings.append(Finding("ENTRY_LIMIT", "ERROR", target.name,
                                            f"Archive contains more than {MAX_ENTRIES} entries.",
                                            "Create a smaller release archive."))
                    infos = infos[:MAX_ENTRIES]
                total_size = 0
                exact_seen: set[str] = set()
                folded_seen: dict[str, str] = {}
                for info in infos:
                    raw = info.filename
                    if info.is_dir():
                        continue
                    normalized = raw.replace("\\", "/")
                    path = PurePosixPath(normalized)
                    rel = path.as_posix()
                    unsafe = (normalized.startswith("/") or ".." in path.parts
                              or (path.parts and ":" in path.parts[0]) or "\x00" in raw)
                    if unsafe:
                        findings.append(Finding("UNSAFE_PATH", "ERROR", raw,
                                                "Archive entry has an absolute, parent-traversal, or drive-qualified path.",
                                                "Rebuild the ZIP using paths relative to the mod root."))
                        continue
                    if "\\" in raw:
                        findings.append(Finding("BACKSLASH_PATH", "WARNING", raw,
                                                "Archive path uses backslashes and may unpack inconsistently.",
                                                "Use forward slashes in ZIP entry names."))
                    if rel in exact_seen:
                        findings.append(Finding("DUPLICATE_PATH", "ERROR", rel,
                                                "The archive contains the same path more than once.",
                                                "Remove duplicate entries before publishing."))
                        continue
                    exact_seen.add(rel)
                    folded = rel.casefold()
                    previous = folded_seen.get(folded)
                    if previous and previous != rel:
                        findings.append(Finding("CASE_COLLISION", "ERROR", rel,
                                                f"Path differs only by letter case from `{previous}`.",
                                                "Rename one file; some systems treat these paths as identical."))
                    else:
                        folded_seen[folded] = rel
                    mode = (info.external_attr >> 16) & 0xFFFF
                    if stat.S_ISLNK(mode):
                        findings.append(Finding("ZIP_SYMLINK", "WARNING", rel,
                                                "Archive contains a symbolic-link entry.",
                                                "Avoid shipping symlinks unless the target platform supports them."))
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
                    findings.append(Finding("ARCHIVE_SIZE_LIMIT", "ERROR", target.name,
                                            "Unpacked archive size exceeds 4 GiB scan limit.",
                                            "Split the release into smaller archives."))
        except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
            findings.append(Finding("INVALID_ZIP", "ERROR", target.name,
                                    f"The file could not be read as a valid ZIP archive: {exc}",
                                    "Recreate the archive and open it once in a ZIP utility before release."))
        super().__init__(target=target, records=records, findings=findings, is_zip=True)

    def read(self, relative_path: str, limit: int) -> bytes | None:
        info = self._index.get(relative_path)
        if info is None:
            return None
        try:
            with zipfile.ZipFile(self.target) as archive, archive.open(info) as stream:
                return stream.read(limit + 1)
        except (OSError, RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile):
            return None

    def digest(self) -> str:
        return _sha256_file(self.target)


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
