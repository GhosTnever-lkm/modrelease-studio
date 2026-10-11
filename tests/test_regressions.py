from __future__ import annotations

import contextlib
import io
import json
import stat
import tempfile
import tomllib
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from modrelease_studio import __version__, cli
from modrelease_studio.models import Finding, ScanReport, Source
from modrelease_studio.scanner import scan_path, scan_source
from modrelease_studio.reports import markdown
from modrelease_studio.scanner import SECRET_PATTERNS, MAX_CONFIGURED_TEXT_FILE_BYTES


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


class MarkdownReportEscapingTests(unittest.TestCase):
    def test_untrusted_paths_and_details_cannot_break_markdown_table(self) -> None:
        report = ScanReport(
            target="source`|name\n![spoof](https://example.invalid)",
            profile="default",
            findings=[Finding(
                "UNSAFE_PATH", "ERROR", "bad|`name`\n![row](https://example.invalid)",
                "detail | [link](https://example.invalid)\n<img src=x>",
            )],
        )
        rendered = markdown(report)
        finding_rows = [line for line in rendered.splitlines() if line.startswith("| ERROR |")]
        self.assertEqual(len(finding_rows), 1)
        self.assertNotIn("![spoof]", rendered)
        self.assertNotIn("![row]", rendered)
        self.assertNotIn("[link]", rendered)
        self.assertNotIn("<img src=x>", rendered)
        self.assertIn("&lt;img src=x&gt;", rendered)
        self.assertIn("&#124;", rendered)

    def test_shareable_reports_include_only_source_basename(self) -> None:
        with tempfile.TemporaryDirectory(prefix="private-user-path-") as parent:
            target = Path(parent) / "sample-mod"
            target.mkdir()
            (target / "README.md").write_text("Synthetic fixture", encoding="utf-8")
            report = scan_path(str(target))
            serialized = json.dumps(report.to_dict(), ensure_ascii=False)
            rendered = markdown(report)
        self.assertEqual(report.target, "sample-mod")
        self.assertNotIn(parent, serialized)
        self.assertNotIn(parent, rendered)


class ConfigValidationOrderTests(unittest.TestCase):
    def test_invalid_scan_config_fails_before_source_digest(self) -> None:
        invalid_configs = [
            {"max_file_bytes": 0},
            {"required_files": [""]},
            {"required_paths": [""]},
            {"required_paths_severity": "CRITICAL"},
        ]

        class NeverDigestSource(Source):
            def digest(self) -> str:
                raise AssertionError("source digest should not run for invalid config")

        for config in invalid_configs:
            with self.subTest(config=config):
                source = NeverDigestSource(Path("unused"), [], [], False)
                with self.assertRaises(ValueError):
                    scan_source(source, config=config)


class ArchivePathSafetyTests(unittest.TestCase):
    def test_zip_rejects_colon_in_nested_path_component(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "colon-path.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("mod/payload.txt:stream", "synthetic fixture")
            report = scan_path(str(archive_path))
        finding = next(item for item in report.findings if item.code == "UNSAFE_PATH")
        self.assertEqual(finding.severity, "ERROR")
        self.assertEqual(report.errors, 1)

    def test_zip_rejects_unsafe_and_windows_nonportable_directory_paths(self) -> None:
        entries = ["../outside/", "mod/CON.txt/", "mod/trailing./", "mod/trailing /"]
        for entry in entries:
            with self.subTest(entry=entry), tempfile.TemporaryDirectory() as directory:
                archive_path = Path(directory) / "unsafe-directory.zip"
                with zipfile.ZipFile(archive_path, "w") as archive:
                    archive.writestr(entry, b"")
                report = scan_path(str(archive_path))
            self.assertIn("UNSAFE_PATH", {finding.code for finding in report.findings})
            self.assertEqual(report.errors, 1)



class SpecialArchiveEntryTests(unittest.TestCase):
    def test_zip_fifo_entry_is_blocked_without_reading_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "special.zip"
            info = zipfile.ZipInfo("mod/fifo")
            info.create_system = 3
            info.external_attr = (stat.S_IFIFO | 0o644) << 16
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr(info, b"synthetic fixture only")
            report = scan_path(str(archive_path))
        finding = next(item for item in report.findings if item.code == "UNSAFE_SPECIAL_ENTRY")
        self.assertEqual(finding.severity, "ERROR")
        self.assertEqual(report.errors, 1)


class PathCollisionTests(unittest.TestCase):
    def test_directory_scan_finds_case_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "Common"
            second = Path(directory) / "common"
            first.mkdir()
            second.mkdir()
            (first / "Events.txt").write_text("a", encoding="utf-8")
            (second / "events.TXT").write_text("b", encoding="utf-8")
            report = scan_path(directory)
        self.assertIn("CASE_COLLISION", {item.code for item in report.findings})
        self.assertEqual(report.errors, 1)

    def test_directory_scan_finds_unicode_normalization_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            composed = Path(directory) / "café.txt"
            decomposed = Path(directory) / "cafe\u0301.txt"
            composed.write_text("a", encoding="utf-8")
            decomposed.write_text("b", encoding="utf-8")
            report = scan_path(directory)
        self.assertIn("UNICODE_COLLISION", {item.code for item in report.findings})
        self.assertEqual(report.errors, 1)

    def test_zip_scan_finds_unicode_normalization_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "mod.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("common/café.txt", "a")
                archive.writestr("common/cafe\u0301.txt", "b")
            report = scan_path(str(archive_path))
        self.assertIn("UNICODE_COLLISION", {item.code for item in report.findings})
        self.assertEqual(report.errors, 1)


class RequiredPathPolicyTests(unittest.TestCase):
    def test_configured_required_path_glob_warns_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "README.md").write_text("readme", encoding="utf-8")
            report = scan_path(directory, config={"required_paths": ["descriptor.mod"]})
        findings = [item for item in report.findings if item.code == "REQUIRED_PATH_MISSING"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "WARNING")
        self.assertEqual(findings[0].path, "descriptor.mod")

    def test_required_path_glob_is_case_insensitive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "Common").mkdir()
            (Path(directory) / "Common" / "Events.TXT").write_text("ok", encoding="utf-8")
            report = scan_path(directory, config={
                "required_paths": ["common/*.txt"],
                "required_paths_severity": "error",
            })
        self.assertNotIn("REQUIRED_PATH_MISSING", {item.code for item in report.findings})
        self.assertEqual(report.errors, 0)

    def test_required_path_patterns_normalize_windows_separators_and_case(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "Localization"
            target.mkdir()
            (target / "English.yml").write_text("l_english:\n", encoding="utf-8")
            report = scan_path(directory, config={
                "required_paths": [r"localization\*.yml"],
                "required_paths_severity": "ERROR",
            })
        self.assertNotIn("REQUIRED_PATH_MISSING", {item.code for item in report.findings})
        self.assertEqual(report.errors, 0)

    def test_malformed_required_files_are_rejected(self) -> None:
        malformed = ["README.md", [""], ["LICENSE", None]]
        for value in malformed:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                with self.assertRaisesRegex(ValueError, "required_files"):
                    scan_path(directory, config={"required_files": value})

    def test_empty_required_files_list_disables_filename_recommendations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = scan_path(directory, config={"required_files": []})
        self.assertNotIn("MISSING_RELEASE_FILE", {item.code for item in report.findings})

    def test_invalid_or_unbounded_max_file_bytes_is_rejected(self) -> None:
        invalid_values = [0, -1, True, 1.5, "2000000", MAX_CONFIGURED_TEXT_FILE_BYTES + 1]
        for value in invalid_values:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                with self.assertRaisesRegex(ValueError, "max_file_bytes"):
                    scan_path(directory, config={"max_file_bytes": value})

    def test_max_file_bytes_ceiling_keeps_larger_text_files_unscanned(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.txt"
            with path.open("wb") as stream:
                stream.truncate(MAX_CONFIGURED_TEXT_FILE_BYTES + 1)
            report = scan_path(directory, config={"max_file_bytes": MAX_CONFIGURED_TEXT_FILE_BYTES})
        self.assertIn("LARGE_TEXT_FILE", {item.code for item in report.findings})

    def test_malformed_required_paths_are_rejected(self) -> None:
        malformed = ["descriptor.mod", [""], ["   "], ["README.md", 7]]
        for value in malformed:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                with self.assertRaisesRegex(ValueError, "required_paths"):
                    scan_path(directory, config={"required_paths": value})

    def test_error_severity_blocks_when_required_path_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = scan_path(directory, config={
                "required_paths": ["descriptor.mod"],
                "required_paths_severity": "ERROR",
            })
        self.assertEqual(report.errors, 1)
        finding = next(item for item in report.findings if item.code == "REQUIRED_PATH_MISSING")
        self.assertEqual(finding.severity, "ERROR")

    def test_invalid_required_path_policy_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "required_paths_severity"):
                scan_path(directory, config={"required_paths_severity": "CRITICAL"})


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

    def test_compare_reports_duplicate_finding_count_increases(self) -> None:
        finding = Finding("MISSING_FILE", "WARNING", "README.md", "Recommended release file is missing.")
        before = ScanReport("before", "default", findings=[finding])
        after = ScanReport("after", "default", findings=[finding, finding, finding])
        args = type("Args", (), {"before": "before", "after": "after", "config": None})()
        output = io.StringIO()
        with patch.object(cli, "scan_path", side_effect=[before, after]), contextlib.redirect_stdout(output):
            result = cli._compare(args)
        self.assertEqual(result, 0)
        self.assertIn("+ [WARNING] MISSING_FILE README.md: Recommended release file is missing. (x2)", output.getvalue())

    def test_compare_reports_duplicate_finding_count_decreases(self) -> None:
        finding = Finding("DUPLICATE", "ERROR", "common/example.txt", "Duplicate path.")
        before = ScanReport("before", "default", findings=[finding, finding, finding])
        after = ScanReport("after", "default", findings=[finding])
        args = type("Args", (), {"before": "before", "after": "after", "config": None})()
        output = io.StringIO()
        with patch.object(cli, "scan_path", side_effect=[before, after]), contextlib.redirect_stdout(output):
            result = cli._compare(args)
        self.assertEqual(result, 1)
        self.assertIn("- [ERROR] DUPLICATE common/example.txt: Duplicate path. (x2)", output.getvalue())


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
        self.assertEqual(output.getvalue().strip(), "modrelease 0.3.22")

if __name__ == "__main__":
    unittest.main()
