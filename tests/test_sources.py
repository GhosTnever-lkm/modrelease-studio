from __future__ import annotations

import hashlib
import struct
import tempfile
import unittest
import zipfile
from unittest.mock import patch
from pathlib import Path

from modrelease_studio.sources import open_source
from modrelease_studio.scanner import scan_path


class DirectorySourceSafetyTests(unittest.TestCase):
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
