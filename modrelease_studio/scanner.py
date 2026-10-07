"""High-level release checks for common game mod formats."""
from __future__ import annotations

import re
from pathlib import PurePosixPath

from .models import Finding, ScanReport, Source
from .paradox import check_paradox_localization, parse_descriptor
from .sources import open_source

SECRET_PATTERNS = (
    ("PRIVATE_KEY", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "Possible private key found."),
    ("GITHUB_TOKEN", re.compile(rb"gh[pousr]_[A-Za-z0-9_]{30,}"), "Possible GitHub access token found."),
    ("GENERIC_API_KEY", re.compile(rb"(?i)(?:api[_-]?key|secret|token)\s*[:=]\s*[\"'][A-Za-z0-9_./+=-]{20,}[\"']"), "Possible hard-coded secret found."),
)
TEXT_EXTENSIONS = {".txt", ".yml", ".yaml", ".json", ".cfg", ".ini", ".lua", ".py", ".js", ".ts", ".toml", ".md", ".xml", ".properties"}
IGNORE_PARTS = {".git", ".github", "node_modules", "__pycache__", ".venv"}


def scan_path(path: str, *, config: dict | None = None) -> ScanReport:
    return scan_source(open_source(path), config=config)


def scan_source(source: Source, *, config: dict | None = None) -> ScanReport:
    config = config or {}
    report = ScanReport(target=str(source.target), profile="default", file_count=len(source.records),
                        total_bytes=sum(item.size for item in source.records), sha256=source.digest(), files=source.records)
    report.findings.extend(source.findings)
    max_file_bytes = int(config.get("max_file_bytes", 2_000_000))
    required_files = {str(x).casefold() for x in config.get("required_files", ["README.md"])}
    file_names = {PurePosixPath(record.path).name.casefold() for record in source.records}
    for name in sorted(required_files - file_names):
        report.findings.append(Finding("MISSING_RELEASE_FILE", "WARNING", name,
                                       f"Recommended release file is missing: {name}"))

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
