from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from modrelease_studio.sources import open_source


class DirectorySourceSafetyTests(unittest.TestCase):
    def test_read_refuses_symlinked_files_and_directories(self) -> None:
        with tempfile.TemporaryDirectory() as parent, tempfile.TemporaryDirectory() as external:
            root = Path(parent) / "mod"
            root.mkdir()
            outside = Path(external) / "descriptor.mod"
            outside.write_text('name = "outside-only-fixture"\n', encoding="utf-8")
            (Path(external) / "payload.txt").write_text("outside payload fixture", encoding="utf-8")
            (root / "descriptor.mod").symlink_to(outside)
            (root / "linked-folder").symlink_to(Path(external), target_is_directory=True)
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

    def test_directory_digest_matches_safe_file_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_bytes(b"safe fixture")
            source = open_source(root)
            self.assertEqual(source.digest(), hashlib.sha256(b"README.md\0safe fixture\0").hexdigest())
