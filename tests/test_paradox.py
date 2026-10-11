from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from modrelease_studio.paradox import check_paradox_localization, parse_descriptor
from modrelease_studio.sources import MAX_TEXT_FILE, open_source


class DescriptorParsingTests(unittest.TestCase):
    def test_parses_utf8_bom_comments_quotes_and_casefolded_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            descriptor = Path(directory) / "descriptor.mod"
            descriptor.write_bytes(
                b'\xef\xbb\xbf# comment\nname = "First Name"\nsupported_version = 1.15.*\nNAME=\'Final Name\'\nnot a field\n'
            )
            parsed = parse_descriptor(open_source(directory), "descriptor.mod")
        self.assertEqual(parsed, {"name": "Final Name", "supported_version": "1.15.*"})

    def test_missing_or_oversized_descriptor_returns_empty_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "descriptor.mod").write_bytes(b"x" * (MAX_TEXT_FILE + 1))
            source = open_source(root)
            self.assertEqual(parse_descriptor(source, "missing.mod"), {})
            self.assertEqual(parse_descriptor(source, "descriptor.mod"), {})

    def test_invalid_utf8_descriptor_returns_empty_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            descriptor = Path(directory) / "descriptor.mod"
            descriptor.write_bytes(b"name = \xff\xfe")
            parsed = parse_descriptor(open_source(directory), "descriptor.mod")
        self.assertEqual(parsed, {})


class LocalizationChecksTests(unittest.TestCase):
    def make_source(self, files: dict[str, bytes]):
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        for name, contents in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(contents)
        return directory, open_source(root)

    def test_missing_localization_file_is_a_warning(self) -> None:
        directory, source = self.make_source({"descriptor.mod": b"name = demo\n"})
        with directory:
            findings = check_paradox_localization(source)
        self.assertEqual([item.code for item in findings], ["NO_LOCALIZATION"])
        self.assertEqual(findings[0].severity, "WARNING")

    def test_comments_language_header_duplicates_and_empty_value(self) -> None:
        directory, source = self.make_source({
            "LOCALIZATION/English.yml": (
                b"# explanatory comment\n\nl_english:\nname:0 \"Mod name\"\nname:1 \"Duplicate\"\nempty:0 \"\"\nnot-a-entry\n"
            )
        })
        with directory:
            findings = check_paradox_localization(source)
        self.assertNotIn("LOCALIZATION_HEADER", {item.code for item in findings})
        self.assertEqual(
            [item.code for item in findings],
            ["DUPLICATE_LOCALIZATION_KEY", "EMPTY_LOCALIZATION"],
        )

    def test_bad_header_and_invalid_utf8_are_reported(self) -> None:
        directory, source = self.make_source({
            "localisation/bad.yml": b"english:\nkey:0 \"text\"\n",
            "localization/invalid.yaml": b"l_french:\nname:0 \xff\n",
        })
        with directory:
            findings = check_paradox_localization(source)
        codes = {item.code for item in findings}
        self.assertIn("LOCALIZATION_HEADER", codes)
        self.assertIn("LOCALIZATION_ENCODING", codes)

    def test_oversized_localization_is_reported_without_full_parse(self) -> None:
        directory, source = self.make_source({
            "localisation/large.yml": b"l_english:\n" + b"x" * (MAX_TEXT_FILE + 1),
        })
        with directory:
            findings = check_paradox_localization(source)
        self.assertEqual([item.code for item in findings], ["LOCALIZATION_TOO_LARGE"])

    def test_unreadable_localization_is_reported(self) -> None:
        directory, source = self.make_source({"localisation/english.yml": b"l_english:\n"})
        with directory, patch("modrelease_studio.sources.DirectorySource.read", return_value=None):
            findings = check_paradox_localization(source)
        self.assertEqual([item.code for item in findings], ["LOCALIZATION_UNREADABLE"])


if __name__ == "__main__":
    unittest.main()
