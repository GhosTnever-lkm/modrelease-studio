"""High-level release checks for common game mod formats."""
from __future__ import annotations

import fnmatch
import re
import unicodedata
from pathlib import PurePosixPath

from .models import Finding, ScanReport, Source
from .paradox import check_paradox_localization, parse_descriptor
from .sources import open_source

SECRET_PATTERNS = (
    ("PRIVATE_KEY", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "Possible private key found."),
    ("AWS_ACCESS_KEY", re.compile(rb"\bAKIA[0-9A-Z]{16}\b"), "Possible AWS access key found."),
    ("AWS_SECRET_KEY", re.compile(rb"(?i)aws_secret_access_key\s*[:=]\s*[\"']?(?!YOUR_|PLACEHOLDER|EXAMPLE|CHANGEME|XXXX|AAAA)[A-Za-z0-9/+=]{40}[\"']?"), "Possible AWS secret access key found."),
    ("GITHUB_TOKEN", re.compile(rb"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"), "Possible GitHub access token found."),
    ("SLACK_TOKEN", re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "Possible Slack token found."),
    ("DISCORD_WEBHOOK", re.compile(rb"https?://(?:canary\.|ptb\.)?discord(?:app)?\.com/api/webhooks/[0-9]{15,}/[A-Za-z0-9._-]{20,}"), "Possible Discord webhook found."),
    ("GENERIC_API_KEY", re.compile(rb"(?i)(?:\"(?:api[_-]?key|secret|token)\"|(?:api[_-]?key|secret|token))\s*[:=]\s*[\"']?(?!YOUR_|PLACEHOLDER|EXAMPLE|CHANGEME|XXXX|AAAA)[A-Za-z0-9_./+=-]{12,}[\"']?"), "Possible hard-coded secret found."),
)
MAX_CONFIGURED_TEXT_FILE_BYTES = 16 * 1024 * 1024
TEXT_EXTENSIONS = {".txt", ".yml", ".yaml", ".json", ".cfg", ".ini", ".lua", ".py", ".js", ".ts", ".toml", ".md", ".xml", ".properties", ".pem", ".key"}
IGNORE_PARTS = {".git", ".github", "node_modules", "__pycache__", ".venv"}


def scan_path(path: str, *, config: dict | None = None) -> ScanReport:
    return scan_source(open_source(path), config=config)


def scan_source(source: Source, *, config: dict | None = None) -> ScanReport:
    config = config or {}
    max_file_bytes = config.get("max_file_bytes", 2_000_000)
    if (isinstance(max_file_bytes, bool) or not isinstance(max_file_bytes, int)
            or not 1 <= max_file_bytes <= MAX_CONFIGURED_TEXT_FILE_BYTES):
        raise ValueError(
            "scan.max_file_bytes must be an integer from 1 to 16777216"
        )
    required_files_value = config.get("required_files", ["README.md"])
    if not isinstance(required_files_value, list) or any(not isinstance(name, str) or not name.strip() for name in required_files_value):
        raise ValueError("scan.required_files must be a list of non-empty filenames")
    required_files = {name.casefold() for name in required_files_value}
    required_paths = config.get("required_paths", [])
    if not isinstance(required_paths, list) or any(not isinstance(pattern, str) or not pattern.strip() for pattern in required_paths):
        raise ValueError("scan.required_paths must be a list of non-empty path patterns")
    required_paths_severity = str(config.get("required_paths_severity", "WARNING")).upper()
    if required_paths_severity not in {"ERROR", "WARNING", "INFO"}:
        raise ValueError("scan.required_paths_severity must be ERROR, WARNING, or INFO")

    # Reports are designed to be shared with maintainers and CI artifacts. Keep
    # the useful source label while omitting user names and parent directories.
    report = ScanReport(target=source.target.name or ".", profile="default", file_count=len(source.records),
                        total_bytes=sum(item.size for item in source.records), sha256=source.digest(), files=source.records)
    report.findings.extend(source.findings)
    file_names = {PurePosixPath(record.path).name.casefold() for record in source.records}
    for name in sorted(required_files - file_names):
        report.findings.append(Finding("MISSING_RELEASE_FILE", "WARNING", name,
                                       f"Recommended release file is missing: {name}"))

    normalized_paths = [record.path.casefold() for record in source.records]
    for pattern in required_paths:
        normalized_pattern = pattern.replace("\\", "/").casefold()
        if not any(fnmatch.fnmatchcase(path, normalized_pattern) for path in normalized_paths):
            report.findings.append(Finding(
                "REQUIRED_PATH_MISSING", required_paths_severity, pattern,
                f"Configured release path is missing: {pattern}",
            ))

    normalized_seen: dict[str, str] = {}
    for record in source.records:
        identity = unicodedata.normalize("NFC", record.path).casefold()
        previous = normalized_seen.get(identity)
        if previous and previous != record.path:
            case_only = previous.casefold() == record.path.casefold()
            code = "CASE_COLLISION" if case_only else "UNICODE_COLLISION"
            message = (
                f"Path differs only by letter case from `{previous}`."
                if case_only else f"Path is Unicode-normalization equivalent to `{previous}`."
            )
            report.findings.append(Finding(code, "ERROR", record.path, message,
                                           "Rename one entry; the target filesystem may treat these paths as identical."))
        else:
            normalized_seen[identity] = record.path

    localization_found = False
    for record in source.records:
        path = PurePosixPath(record.path)
        folded_parts = {part.casefold() for part in path.parts}
        if folded_parts & IGNORE_PARTS:
            continue
        if path.name.casefold() in {"thumbs.db", ".ds_store", "desktop.ini"}:
            report.findings.append(Finding("OS_JUNK", "WARNING", record.path, "Operating-system metadata should not be in a release."))
            continue
        if record.size > max_file_bytes:
            if path.suffix.casefold() in TEXT_EXTENSIONS:
                report.findings.append(Finding("LARGE_TEXT_FILE", "WARNING", record.path,
                                               f"Text file exceeds configured scan limit ({max_file_bytes} bytes)."))
            continue
        if path.suffix.casefold() not in TEXT_EXTENSIONS:
            continue
        data = source.read(record.path, max_file_bytes)
        if data is None:
            report.findings.append(Finding("UNREADABLE_FILE", "WARNING", record.path, "Could not read this file for content checks."))
            continue
        if len(data) > max_file_bytes:
            continue
        for code, pattern, message in SECRET_PATTERNS:
            if pattern.search(data):
                report.findings.append(Finding(code, "ERROR", record.path, message))
                break
        if path.suffix.casefold() in {".yml", ".yaml"} and any(part in {"localisation", "localization"} for part in folded_parts):
            localization_found = True

    if localization_found:
        report.findings.extend(check_paradox_localization(source))
    for record in source.records:
        if PurePosixPath(record.path).name.casefold() == "descriptor.mod":
            fields = parse_descriptor(source, record.path)
            if not fields.get("name"):
                report.findings.append(Finding("DESCRIPTOR_NAME", "WARNING", record.path, "Paradox descriptor is missing a name field."))
            if not fields.get("supported_version"):
                report.findings.append(Finding("DESCRIPTOR_VERSION", "INFO", record.path, "Paradox descriptor does not declare supported_version."))
    report.findings.sort(key=lambda finding: ({"ERROR": 0, "WARNING": 1, "INFO": 2}.get(finding.severity, 3), finding.path or "", finding.code))
    return report
