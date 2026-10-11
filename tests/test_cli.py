from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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

    def test_version_option_prints_package_version(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as raised:
            cli.main(["--version"])
        self.assertEqual(raised.exception.code, 0)
        self.assertIn(cli.__version__, stdout.getvalue())
