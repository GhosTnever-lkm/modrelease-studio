from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import quote_from_bytes

from modrelease_studio import cli
from modrelease_studio.models import Finding, ScanReport


class CliTests(unittest.TestCase):
    def test_config_defaults_to_empty_when_file_is_absent(self) -> None:
        with tempfile.TemporaryDirectory() as directory, contextlib.chdir(directory):
            self.assertEqual(cli._config(None), {})

    def test_config_loads_scan_section_from_toml(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "policy.toml"
            config.write_text('[scan]\nrequired_paths = ["descriptor.mod"]\n', encoding="utf-8")
            self.assertEqual(cli._config(str(config)), {"required_paths": ["descriptor.mod"]})

    def test_scan_writes_json_and_markdown_reports(self) -> None:
        with tempfile.TemporaryDirectory() as directory, contextlib.chdir(directory):
            target = "fixture\u202Egpj.zip"
            unsafe_path = "folder\u202Ename.txt"
            report = ScanReport(
                target=target,
                profile="default",
                findings=[Finding("UNSAFE_PATH", "ERROR", unsafe_path, "control\u001b[31m and C1\u0085")],
            )
            stdout = io.StringIO()
            with patch.object(cli, "scan_path", return_value=report) as scan_path, contextlib.redirect_stdout(stdout):
                result = cli.main(["scan", "fixture.zip", "--json", "--json-out", "report.json", "--md-out", "report.md"])

            self.assertEqual(result, 1)
            scan_path.assert_called_once_with("fixture.zip", config={})
            self.assertNotIn("\u202e", stdout.getvalue().casefold())
            self.assertNotIn("\u001b", stdout.getvalue())
            parsed = json.loads(stdout.getvalue())
            self.assertEqual(parsed["target"], target)
            self.assertEqual(parsed["findings"][0]["path"], unsafe_path)
            self.assertEqual(parsed, json.loads(Path("report.json").read_text(encoding="utf-8")))
            markdown = Path("report.md").read_text(encoding="utf-8")
            self.assertIn("# ModRelease Studio report", markdown)
            self.assertNotIn("\u202e", markdown.casefold())
            self.assertNotIn("\u001b", markdown)
            self.assertIn("202e", markdown.casefold())

    def test_scan_returns_one_when_report_has_errors(self) -> None:
        report = ScanReport(
            target="fixture.zip",
            profile="default",
            findings=[Finding("REQUIRED_PATH_MISSING", "ERROR", "descriptor.mod", "Required path is missing")],
        )
        stdout = io.StringIO()
        with patch.object(cli, "scan_path", return_value=report), contextlib.redirect_stdout(stdout):
            result = cli.main(["scan", "fixture.zip"])
        self.assertEqual(result, 1)
        self.assertIn("REQUIRED_PATH_MISSING", stdout.getvalue())

    def test_missing_config_returns_two_with_readable_error(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = cli.main(["scan", "fixture.zip", "--config", "does-not-exist.toml"])
        self.assertEqual(result, 2)
        self.assertIn("modrelease:", stderr.getvalue())

    def test_invalid_toml_returns_two_with_readable_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "invalid.toml"
            config.write_text("[scan\n", encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = cli.main(["scan", "fixture.zip", "--config", str(config)])
        self.assertEqual(result, 2)
        self.assertIn("modrelease:", stderr.getvalue())

    def test_non_table_scan_section_returns_two_with_readable_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "invalid-scan-section.toml"
            config.write_text('scan = "not-a-table"\n', encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = cli.main(["scan", "fixture.zip", "--config", str(config)])
        self.assertEqual(result, 2)
        self.assertIn("modrelease:", stderr.getvalue())
        self.assertIn("must be a TOML table", stderr.getvalue())

    def test_version_option_prints_package_version(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as raised:
            cli.main(["--version"])
        self.assertEqual(raised.exception.code, 0)
        self.assertIn(cli.__version__, stdout.getvalue())


class SarifCliTests(unittest.TestCase):
    def test_sarif_normalizes_dot_segments_in_relative_path_prefix(self) -> None:
        report = ScanReport(
            target="mod",
            profile="default",
            findings=[Finding("TEST", "ERROR", "config.txt", "Check failed.")],
        )
        for prefix, expected_uri in ((".", "config.txt"), ("./mods/./my mod/", "mods/my%20mod/config.txt")):
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as directory, contextlib.chdir(directory):
                with patch.object(cli, "scan_path", return_value=report), contextlib.redirect_stdout(io.StringIO()):
                    result = cli.main(["scan", "mod", "--sarif-out", "report.sarif", "--sarif-path-prefix", prefix])
                document = json.loads(Path("report.sarif").read_text(encoding="utf-8"))
                uri = document["runs"][0]["results"][0]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
                self.assertEqual(result, 1)
                self.assertEqual(uri, expected_uri)

    def test_scan_writes_sarif_with_repo_relative_prefixed_locations(self) -> None:
        with tempfile.TemporaryDirectory() as directory, contextlib.chdir(directory):
            report = ScanReport(
                target="private-local-folder",
                profile="default",
                findings=[
                    Finding("SECRET", "ERROR", "config/settings.json", "Possible secret found."),
                    Finding("DUPLICATE_LOCALIZATION_KEY", "WARNING", "localisation/english.yml:12", "Duplicate key."),
                    Finding("MISSING_RELEASE_FILE", "WARNING", "README.md", "Recommended file is missing."),
                    Finding("ADVISORY", "INFO", "C:\\private\\mod\\file.txt", "No repository path."),
                ],
            )
            with patch.object(cli, "scan_path", return_value=report), contextlib.redirect_stdout(io.StringIO()):
                result = cli.main(["scan", "mod", "--sarif-out", "report.sarif", "--sarif-path-prefix", "mods/my mod#1"])

            document = json.loads(Path("report.sarif").read_text(encoding="utf-8"))
            run = document["runs"][0]
            results = {item["ruleId"]: item for item in run["results"]}
            self.assertEqual(result, 1)
            self.assertEqual(document["version"], "2.1.0")
            self.assertEqual(run["tool"]["driver"]["semanticVersion"], cli.__version__)
            self.assertEqual(results["SECRET"]["level"], "error")
            self.assertEqual(results["MISSING_RELEASE_FILE"]["level"], "warning")
            self.assertEqual(results["ADVISORY"]["level"], "note")
            self.assertEqual(
                results["SECRET"]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"],
                "mods/my%20mod%231/config/settings.json",
            )
            self.assertEqual(
                results["DUPLICATE_LOCALIZATION_KEY"]["locations"][0]["physicalLocation"]["region"]["startLine"], 12,
            )
            self.assertNotIn("locations", results["MISSING_RELEASE_FILE"])
            self.assertNotIn("locations", results["ADVISORY"])
            serialized = Path("report.sarif").read_text(encoding="utf-8")
            self.assertNotIn("private-local-folder", serialized)
            self.assertNotIn("C:\\\\private", serialized)

    def test_sarif_percent_encodes_filesystem_surrogate_paths(self) -> None:
        unsafe_path = "bad_\udcff_name.txt"
        report = ScanReport(
            target="mod",
            profile="default",
            findings=[Finding("UNSAFE_PATH", "ERROR", unsafe_path, "Unsupported filename encoding.")],
        )
        expected_uri = quote_from_bytes(os.fsencode(unsafe_path), safe="/-._~!$&'()*+,;=:@")
        with tempfile.TemporaryDirectory() as directory, contextlib.chdir(directory):
            with patch.object(cli, "scan_path", return_value=report), contextlib.redirect_stdout(io.StringIO()):
                result = cli.main(["scan", "mod", "--sarif-out", "report.sarif"])
            document = json.loads(Path("report.sarif").read_text(encoding="utf-8"))

        self.assertEqual(result, 1)
        self.assertEqual(
            document["runs"][0]["results"][0]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"],
            expected_uri,
        )

    def test_sarif_rejects_unsafe_path_prefix(self) -> None:
        for prefix in ("../mods", "./../mods", "/absolute", "/", "\\\\", "//server/share", "C:\\mods"):
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "report.sarif"
                stderr = io.StringIO()
                with patch.object(cli, "scan_path", return_value=ScanReport("mod", "default")), \
                     contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(stderr):
                    result = cli.main(["scan", "mod", "--sarif-out", str(output), "--sarif-path-prefix", prefix])
                self.assertEqual(result, 2)
                self.assertFalse(output.exists())
