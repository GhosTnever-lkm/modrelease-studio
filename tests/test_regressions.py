from __future__ import annotations

import contextlib
import io
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

from modrelease_studio import __version__, cli
from modrelease_studio.models import Finding, ScanReport
from modrelease_studio.scanner import scan_path
from modrelease_studio.scanner import SECRET_PATTERNS


class SecretPatternTests(unittest.TestCase):
    def scan_fixture(self, filename: str, content: bytes) -> ScanReport:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / filename
            path.write_bytes(content)
            return scan_path(directory)

    def test_fake_secret_fixtures_are_detected_without_echoing_values(self) -> None:
        fixtures = {
            "AWS_ACCESS_KEY": b"aws_access_key_id=AKIA1234567890ABCDEF",
            "AWS_SECRET_KEY": b"aws_secret_access_key=FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE",
            "SLACK_TOKEN": b"token=xoxb-123456789012-" + b"FAKEFAKETOKENVALUE",
            "DISCORD_WEBHOOK": b"https://discord.com/api/webhooks/123456789012345678/FAKE.Webhook_Token-Value",
            "GENERIC_API_KEY": b"api_key=FAKE_api_key_value_123456789",
            "GENERIC_API_KEY_JSON": b'{"apiKey": "FAKEjsonApiKeyValue123456"}',
            "PRIVATE_KEY": b"-----BEGIN PRIVATE KEY-----\nfake fixture only\n-----END PRIVATE KEY-----",
            "GITHUB_TOKEN": b"ghp_" + b"A" * 36,
        }
        for code, sample in fixtures.items():
            with self.subTest(code=code):
                report = self.scan_fixture("fixture." + ("pem" if code == "PRIVATE_KEY" else "json" if code.endswith("_JSON") else "txt"), sample)
                self.assertIn(code.removesuffix("_JSON"), {finding.code for finding in report.findings})

    def test_placeholders_are_not_detected(self) -> None:
        samples = [b"api_key=YOUR_API_KEY_PLACEHOLDER_HERE", b'{"apiKey": "YOUR_API_KEY_PLACEHOLDER_HERE"}', b"token=example"]
        for index, sample in enumerate(samples):
            with self.subTest(sample=sample):
                report = self.scan_fixture(f"fixture{index}.json", sample)
                self.assertEqual(report.errors, 0)

    def test_report_messages_do_not_include_fake_secret_value(self) -> None:
        secret = b"AKIA1234567890ABCDEF"
        report = self.scan_fixture("config.txt", b"aws_access_key_id=" + secret)
        self.assertIn("AWS_ACCESS_KEY", {finding.code for finding in report.findings})
        self.assertNotIn(secret.decode(), repr(report.to_dict()))


class CompareTests(unittest.TestCase):
    def test_compare_uses_finding_code_and_differences_do_not_block(self) -> None:
        before = ScanReport("before", "default", findings=[])
        after = ScanReport("after", "default", findings=[Finding("NEW_INFO", "INFO", "readme.txt", "New advisory.")])
        args = type("Args", (), {"before": "before", "after": "after", "config": None})()
        with patch.object(cli, "scan_path", side_effect=[before, after]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = cli._compare(args)
        self.assertEqual(result, 0)
        self.assertIn("NEW_INFO", output.getvalue())

    def test_compare_error_after_build_returns_blocked_exit_code(self) -> None:
        before = ScanReport("before", "default", findings=[])
        after = ScanReport("after", "default", findings=[Finding("SECRET", "ERROR", "config.txt", "Possible hard-coded secret found.")])
        args = type("Args", (), {"before": "before", "after": "after", "config": None})()
        with patch.object(cli, "scan_path", side_effect=[before, after]):
            with contextlib.redirect_stdout(io.StringIO()):
                result = cli._compare(args)
        self.assertEqual(result, 1)


class VersionTests(unittest.TestCase):
    def test_imported_version_matches_package_metadata(self) -> None:
        root = Path(__file__).resolve().parents[1]
        metadata = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(__version__, metadata["project"]["version"])

    def test_cli_prints_installed_version(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as raised:
                cli.main(["--version"])
        self.assertEqual(raised.exception.code, 0)
        self.assertEqual(output.getvalue().strip(), "modrelease 0.2.2")

if __name__ == "__main__":
    unittest.main()
