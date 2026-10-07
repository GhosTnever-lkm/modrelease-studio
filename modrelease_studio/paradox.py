from __future__ import annotations

import re

from .models import Finding, Source
from .sources import MAX_TEXT_FILE

_FIELD = re.compile(r'^\s*([A-Za-z_][\w.-]*)\s*=\s*(.*?)\s*$')
_LOC_LINE = re.compile(r'^\s*([A-Za-z0-9_.-]+)\s*:\s*\d+\s*(?:"(.*)"|(.+))\s*$')


def parse_descriptor(source: Source, path: str) -> dict[str, str]:
    data = source.read(path, MAX_TEXT_FILE)
    if data is None or len(data) > MAX_TEXT_FILE:
        return {}
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return {}
    result: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = _FIELD.match(line)
        if match:
            value = match.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            result[match.group(1).casefold()] = value
    return result


def check_paradox_localization(source: Source) -> list[Finding]:
    findings: list[Finding] = []
    localization_files = [record.path for record in source.records
                          if record.path.casefold().startswith(("localisation/", "localization/"))
                          and record.path.casefold().endswith((".yml", ".yaml"))]
    if not localization_files:
        findings.append(Finding("NO_LOCALIZATION", "WARNING", "localisation/",
                                "No Paradox localization YAML files were found.",
                                "Add localized names and descriptions if the mod contains player-facing text."))
        return findings

    for path in localization_files:
        data = source.read(path, MAX_TEXT_FILE)
        if data is None:
            findings.append(Finding("LOCALIZATION_UNREADABLE", "WARNING", path,
                                    "Could not read localization text as a small UTF-8 file.",
                                    "Check the file encoding and keep localization files under 2 MiB each."))
            continue
        if len(data) > MAX_TEXT_FILE:
            findings.append(Finding("LOCALIZATION_TOO_LARGE", "WARNING", path,
                                    "Localization file exceeds the 2 MiB inspection limit."))
            continue
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            findings.append(Finding("LOCALIZATION_ENCODING", "ERROR", path,
                                    "Localization file is not valid UTF-8.",
                                    "Save it as UTF-8 and check the game-specific BOM requirement."))
            continue
        lines = text.splitlines()
        header = next((line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")), "")
        if not re.fullmatch(r"l_[A-Za-z0-9_-]+:", header):
            findings.append(Finding("LOCALIZATION_HEADER", "ERROR", path,
                                    "First non-comment line is not a language header such as `l_english:`.",
                                    "Put the correct `l_<language>:` header at the beginning of the file."))
        keys: set[str] = set()
        for line_no, line in enumerate(lines, 1):
            stripped = line.lstrip()
            if not stripped or stripped.startswith("#") or line_no == 1 and re.fullmatch(r"l_[A-Za-z0-9_-]+:", stripped.strip()):
                continue
            match = _LOC_LINE.match(line)
            if not match:
                continue
            key = match.group(1)
            if key in keys:
                findings.append(Finding("DUPLICATE_LOCALIZATION_KEY", "ERROR", f"{path}:{line_no}",
                                        f"Localization key `{key}` appears more than once in this file.",
                                        "Keep one definition for each key in a language file."))
            keys.add(key)
            value = match.group(2) if match.group(2) is not None else match.group(3)
            if not value.strip():
                findings.append(Finding("EMPTY_LOCALIZATION", "WARNING", f"{path}:{line_no}",
                                        f"Localization key `{key}` has an empty value.",
                                        "Add a translated value or remove the unused key."))
    return findings
