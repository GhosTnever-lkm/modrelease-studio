from __future__ import annotations

import hashlib
import os
import struct
import subprocess
import tempfile
import unittest
import zipfile
from unittest.mock import patch
from pathlib import Path

from modrelease_studio.sources import open_source
from modrelease_studio.scanner import scan_path


class DirectorySourceSafetyTests(unittest.TestCase):
    def test_junction_like_directory_is_pruned_before_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "mod"
            linked = root / "linked"
            linked.mkdir(parents=True)
            (root / "inside.txt").write_text("inside fixture", encoding="utf-8")
            (linked / "outside.txt").write_text("outside fixture", encoding="utf-8")

            with patch.object(Path, "is_junction", lambda path: path.name == "linked", create=True):
                source = open_source(root)

            self.assertIn(("JUNCTION", "linked"), {(item.code, item.path) for item in source.findings})
            self.assertEqual([record.path for record in source.records], ["inside.txt"])
            self.assertIsNone(source.read("linked/outside.txt", 1024))

            if os.name == "nt":
                self._assert_windows_junction_to_external_directory_is_not_traversed()

    def test_junction_status_permission_error_prunes_directory_and_warns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "mod"
            restricted = root / "restricted"
            restricted.mkdir(parents=True)
            (root / "inside.txt").write_text("inside fixture", encoding="utf-8")
            (restricted / "private-fixture.txt").write_text("must not be indexed", encoding="utf-8")

            def junction_status(path: Path) -> bool:
                if path.name == "restricted":
                    raise PermissionError(13, "Permission denied", str(path))
                return False

            with patch.object(Path, "is_junction", junction_status, create=True):
                source = open_source(root)

        self.assertIn(("READ_METADATA", "restricted"),
                      {(item.code, item.path) for item in source.findings})
        metadata_finding = next(item for item in source.findings if item.code == "READ_METADATA")
        self.assertIn("EACCES", metadata_finding.message)
        self.assertNotIn(str(root), metadata_finding.message)
        self.assertEqual([record.path for record in source.records], ["inside.txt"])
        self.assertNotIn("SCAN_DIRECTORY", {item.code for item in source.findings})
        self.assertIsNone(source.read("restricted/private-fixture.txt", 1024))

    def _assert_windows_junction_to_external_directory_is_not_traversed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "mod"
            external = base / "external"
            junction = root / "linked"
            root.mkdir()
            external.mkdir()
            (root / "inside.txt").write_text("inside fixture", encoding="utf-8")
            (external / "private-fixture.txt").write_text("must not be indexed", encoding="utf-8")

            try:
                subprocess.run(
                    ["cmd", "/c", "mklink", "/J", str(junction), str(external)],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                with patch.object(Path, "is_junction", None, create=True):
                    source = open_source(root)

                self.assertIn(("JUNCTION", "linked"), {(item.code, item.path) for item in source.findings})
                self.assertEqual([record.path for record in source.records], ["inside.txt"])
                self.assertIsNone(source.read("linked/private-fixture.txt", 1024))
            finally:
                if junction.exists():
                    junction.rmdir()

    def test_walk_permission_error_becomes_path_specific_blocking_finding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def walk_with_permission_error(path, *, topdown, onerror, followlinks):
                walk_root = Path(path)
                denied = walk_root / "restricted"
                onerror(PermissionError(13, "Permission denied", str(denied)))
                yield str(walk_root), [], []

            with patch("modrelease_studio.sources.os.walk", side_effect=walk_with_permission_error):
                report = scan_path(root, config={"required_files": []})

        finding = next(item for item in report.findings if item.code == "SCAN_DIRECTORY")
        self.assertEqual(finding.path, "restricted")
        self.assertEqual(finding.severity, "ERROR")
        self.assertIn("EACCES", finding.message)
        self.assertNotIn(str(root), finding.message)
        self.assertEqual(report.errors, 1)

    def test_read_refuses_symlinked_files_and_directories(self) -> None:
        with tempfile.TemporaryDirectory() as parent, tempfile.TemporaryDirectory() as external:
            root = Path(parent) / "mod"
            root.mkdir()
            outside = Path(external) / "descriptor.mod"
            outside.write_text('name = "outside-only-fixture"\n', encoding="utf-8")
            (Path(external) / "payload.txt").write_text("outside payload fixture", encoding="utf-8")
            try:
                (root / "descriptor.mod").symlink_to(outside)
                (root / "linked-folder").symlink_to(Path(external), target_is_directory=True)
            except (OSError, NotImplementedError) as error:
                self.skipTest(f"symlinks are unavailable on this runner: {error}")
            (root / "README.md").write_text("inside fixture", encoding="utf-8")

            source = open_source(root)

            self.assertIsNone(source.read("descriptor.mod", 1024))
            self.assertIsNone(source.read("linked-folder/payload.txt", 1024))
            self.assertEqual([record.path for record in source.records], ["README.md"])
            self.assertEqual({finding.code for finding in source.findings}, {"SYMLINK"})

    def test_read_only_accepts_indexed_paths_and_enforces_byte_limit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "notes.txt").write_bytes(b"abcdef")
            source = open_source(root)
            self.assertEqual(source.read("notes.txt", 3), b"abcd")
            self.assertIsNone(source.read("../notes.txt", 3))
            self.assertIsNone(source.read("not-indexed.txt", 3))

    def test_opened_file_replacement_between_validation_and_open_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as parent, tempfile.TemporaryDirectory() as external:
            root = Path(parent) / "mod"
            root.mkdir()
            source_file = root / "notes.txt"
            source_file.write_text("inside fixture", encoding="utf-8")
            external_file = Path(external) / "outside.txt"
            external_file.write_text("outside fixture", encoding="utf-8")
            source = open_source(root)
            original_open = os.open
            def replace_at_open(path, flags, *args, **kwargs):
                if Path(path) == source_file or Path(path).name == "notes.txt":
                    return original_open(external_file, flags, *args, **kwargs)
                return original_open(path, flags, *args, **kwargs)


            with patch("modrelease_studio.sources.os.open", side_effect=replace_at_open):
                self.assertIsNone(source.read("notes.txt", 1024))

            finding = next(item for item in source.findings if item.code == "FILE_CHANGED_DURING_SCAN")
            self.assertEqual(finding.severity, "ERROR")

    def test_replacement_during_scan_blocks_report(self) -> None:
        with tempfile.TemporaryDirectory() as parent, tempfile.TemporaryDirectory() as external:
            root = Path(parent) / "mod"
            root.mkdir()
            source_file = root / "notes.txt"
            source_file.write_text("inside fixture", encoding="utf-8")
            external_file = Path(external) / "outside.txt"
            external_file.write_text("outside fixture", encoding="utf-8")
            original_open = os.open
            opens = 0

            def replace_during_scan(path, flags, *args, **kwargs):
                nonlocal opens
                if Path(path).name == "notes.txt":
                    opens += 1
                    if opens > 1:
                        return original_open(external_file, flags, *args, **kwargs)
                return original_open(path, flags, *args, **kwargs)

            with patch("modrelease_studio.sources.os.open", side_effect=replace_during_scan):
                report = scan_path(str(root), config={"required_files": []})

            self.assertEqual(report.status, "FAIL")
            self.assertIn("FILE_CHANGED_DURING_SCAN", {finding.code for finding in report.findings})

    def test_replaced_indexed_file_symlink_is_refused_and_not_hashed(self) -> None:
        with tempfile.TemporaryDirectory() as parent, tempfile.TemporaryDirectory() as external:
            root = Path(parent) / "mod"
            root.mkdir()
            source_file = root / "notes.txt"
            source_file.write_text("safe original fixture", encoding="utf-8")
            external_file = Path(external) / "outside.txt"
            external_file.write_text("external fixture must not be read", encoding="utf-8")
            source = open_source(root)
            source_file.unlink()
            try:
                source_file.symlink_to(external_file)
            except (OSError, NotImplementedError) as error:
                self.skipTest(f"symlinks are unavailable on this runner: {error}")

            self.assertIsNone(source.read("notes.txt", 1024))
            expected = hashlib.sha256(b"notes.txt\0UNREADABLE\0").hexdigest()
            self.assertEqual(source.digest(), expected)

    def test_directory_entry_limit_accepts_exact_boundary_and_truncates_overflow(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            at_limit = root / "at-limit"
            at_limit.mkdir()
            for name in ("one.txt", "two.txt"):
                (at_limit / name).write_text("fixture", encoding="utf-8")
            over_limit = root / "over-limit"
            over_limit.mkdir()
            for name in ("one.txt", "two.txt", "three.txt"):
                (over_limit / name).write_text("fixture", encoding="utf-8")

            with patch("modrelease_studio.sources.MAX_ENTRIES", 2):
                exact_source = open_source(at_limit)
                self.assertEqual(len(exact_source.records), 2)
                self.assertNotIn("ENTRY_LIMIT", {finding.code for finding in exact_source.findings})

                overflow_source = open_source(over_limit)
                self.assertEqual(len(overflow_source.records), 2)
                self.assertIn("ENTRY_LIMIT", {finding.code for finding in overflow_source.findings})

    def test_directory_digest_matches_safe_file_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_bytes(b"safe fixture")
            source = open_source(root)
            self.assertEqual(source.digest(), hashlib.sha256(b"README.md\0safe fixture\0").hexdigest())


class ZipSourceTests(unittest.TestCase):
    def test_zip_reads_are_bounded_and_limited_to_indexed_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "fixture.zip"
            with zipfile.ZipFile(archive, "w") as output:
                output.writestr("notes.txt", b"abcdef")
            source = open_source(archive)
            self.assertEqual(source.read("notes.txt", 3), b"abcd")
            self.assertIsNone(source.read("../notes.txt", 3))
            self.assertIsNone(source.read("missing.txt", 3))
            self.assertEqual(source.digest(), hashlib.sha256(archive.read_bytes()).hexdigest())

    def test_zip_entry_limit_accepts_exact_boundary_and_truncates_overflow(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            at_limit_archive = Path(directory) / "entry-at-limit.zip"
            with zipfile.ZipFile(at_limit_archive, "w") as output:
                output.writestr("one.txt", b"fixture")
                output.writestr("two.txt", b"fixture")
            over_limit_archive = Path(directory) / "entry-over-limit.zip"
            with zipfile.ZipFile(over_limit_archive, "w") as output:
                for name in ("one.txt", "two.txt", "three.txt"):
                    output.writestr(name, b"fixture")

            with patch("modrelease_studio.sources.MAX_ENTRIES", 2):
                at_limit = open_source(at_limit_archive)
                self.assertEqual([record.path for record in at_limit.records], ["one.txt", "two.txt"])
                self.assertNotIn("ENTRY_LIMIT", {finding.code for finding in at_limit.findings})

                over_limit = open_source(over_limit_archive)
                self.assertEqual([record.path for record in over_limit.records], ["one.txt", "two.txt"])
                self.assertIn("ENTRY_LIMIT", {finding.code for finding in over_limit.findings})

    def test_zip_uncompressed_size_limit_accepts_exact_boundary_and_flags_overflow(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "size-boundary.zip"
            with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as output:
                output.writestr("first.txt", b"123")
                output.writestr("second.txt", b"456")

            with patch("modrelease_studio.sources.MAX_TOTAL_UNCOMPRESSED", 6):
                at_limit = open_source(archive)
                self.assertNotIn("ARCHIVE_SIZE_LIMIT", {finding.code for finding in at_limit.findings})

            with patch("modrelease_studio.sources.MAX_TOTAL_UNCOMPRESSED", 5):
                over_limit = open_source(archive)
                self.assertIn("ARCHIVE_SIZE_LIMIT", {finding.code for finding in over_limit.findings})
                self.assertFalse(over_limit.contents_available)

    def test_oversized_zip_skips_entry_decompression(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "oversized.zip"
            with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as output:
                output.writestr("one.txt", b"123")
                output.writestr("two.txt", b"456")

            with patch("modrelease_studio.sources.MAX_TOTAL_UNCOMPRESSED", 5), \
                    patch("zipfile.ZipFile.open", side_effect=AssertionError("archive content must not be decompressed")):
                report = scan_path(str(archive))

            self.assertIn("ARCHIVE_SIZE_LIMIT", {finding.code for finding in report.findings})
            self.assertNotIn("UNREADABLE_FILE", {finding.code for finding in report.findings})

    def test_zip_read_returns_none_when_decompression_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "fixture.zip"
            with zipfile.ZipFile(archive, "w") as output:
                output.writestr("notes.txt", b"synthetic archive fixture")
            source = open_source(archive)
            with patch("zipfile.ZipFile.open", side_effect=RuntimeError("synthetic decompression failure")):
                self.assertIsNone(source.read("notes.txt", 100))

    def test_corrupt_deflate_payload_becomes_unreadable_finding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "corrupt-payload.zip"
            with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
                output.writestr("payload.txt", b"alpha-beta-gamma-" * 1000)
            with zipfile.ZipFile(archive) as source_zip:
                info = source_zip.getinfo("payload.txt")
            content = bytearray(archive.read_bytes())
            filename_size, extra_size = struct.unpack_from("<HH", content, info.header_offset + 26)
            compressed_data = info.header_offset + 30 + filename_size + extra_size
            content[compressed_data] ^= 0xFF
            archive.write_bytes(content)

            report = scan_path(str(archive))

            self.assertIn("UNREADABLE_FILE", {finding.code for finding in report.findings})
            self.assertEqual(report.errors, 0)

    def test_invalid_zip_is_reported_without_raising(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "invalid.zip"
            archive.write_bytes(b"not a zip file")
            source = open_source(archive)
            self.assertIn("INVALID_ZIP", {finding.code for finding in source.findings})
            self.assertIsNone(source.read("notes.txt", 10))

    def test_zip_open_error_does_not_leak_absolute_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "private-archive.zip"
            archive.write_bytes(b"fixture")
            with patch("modrelease_studio.sources.zipfile.ZipFile", side_effect=PermissionError(13, "Permission denied", str(archive))):
                source = open_source(archive)

            finding = next(item for item in source.findings if item.code == "INVALID_ZIP")
            self.assertIn("EACCES", finding.message)
            self.assertNotIn(directory, finding.message)
