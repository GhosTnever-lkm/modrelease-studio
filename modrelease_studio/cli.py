"""Command line interface."""
from __future__ import annotations

import argparse
import json
import sys
import tomllib
import unicodedata
from collections import Counter
from pathlib import Path

from . import __version__
from .models import Finding
from .reports import json_report, markdown, to_dict, write_json, write_markdown, write_sarif
from .scanner import scan_path


def _safe_terminal_field(value: str) -> str:
    """Render untrusted path/message text without terminal control effects."""
    rendered: list[str] = []
    readable_controls = {"\n": r"\n", "\r": r"\r", "\t": r"\t"}
    for char in value:
        if char in readable_controls:
            rendered.append(readable_controls[char])
            continue
        category = unicodedata.category(char)
        if category.startswith("C") or category in {"Zl", "Zp"}:
            codepoint = ord(char)
            if codepoint <= 0xFF:
                rendered.append(f"\\x{codepoint:02x}")
            elif codepoint <= 0xFFFF:
                rendered.append(f"\\u{codepoint:04x}")
            else:
                rendered.append(f"\\U{codepoint:08x}")
        else:
            rendered.append(char)
    return "".join(rendered)


def _config(path: str | None) -> dict:
    if not path:
        default = Path("modrelease.toml")
        if not default.exists():
            return {}
        path = str(default)
    with open(path, "rb") as stream:
        data = tomllib.load(stream)
    return data.get("scan", data)


def _scan(args: argparse.Namespace) -> int:
    report = scan_path(args.path, config=_config(args.config))
    if args.json:
        print(json_report(report))
    else:
        print(markdown(report))
    if args.json_out:
        write_json(report, args.json_out)
    if args.md_out:
        write_markdown(report, args.md_out)
    if args.sarif_out:
        write_sarif(report, args.sarif_out, version=__version__, path_prefix=args.sarif_path_prefix)
    return 1 if report.errors else 0


def _compare(args: argparse.Namespace) -> int:
    before = scan_path(args.before, config=_config(args.config))
    after = scan_path(args.after, config=_config(args.config))
    def finding_key(item: Finding) -> tuple[str, str, str, str]:
        return (item.severity, item.code, item.path or "", item.message)

    left = Counter(finding_key(item) for item in before.findings)
    right = Counter(finding_key(item) for item in after.findings)

    def render(counter: Counter, sign: str) -> list[str]:
        rendered = []
        for severity, code, path, message in sorted(counter):
            count = counter[(severity, code, path, message)]
            suffix = f" (x{count})" if count > 1 else ""
            safe_path = _safe_terminal_field(path or "—")
            safe_message = _safe_terminal_field(message)
            rendered.append(f"{sign} [{severity}] {code} {safe_path}: {safe_message}{suffix}")
        return rendered

    removed = left - right
    added = right - left
    lines = [*render(removed, "-"), *render(added, "+")]
    print("\n".join(lines) if lines else "No finding changes.")
    return 1 if after.errors else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="modrelease", description="Preflight game-mod releases from folders or ZIP archives.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    scan = sub.add_parser("scan", help="scan a mod folder or .zip archive")
    scan.add_argument("path", help="folder or .zip file")
    scan.add_argument("--config", help="path to modrelease.toml")
    scan.add_argument("--json", action="store_true", help="print machine-readable JSON")
    scan.add_argument("--json-out", help="write JSON report")
    scan.add_argument("--md-out", help="write Markdown report")
    scan.add_argument("--sarif-out", help="write a SARIF 2.1.0 report for GitHub Code Scanning")
    scan.add_argument("--sarif-path-prefix", default="", help="repository-relative directory containing the scanned source")
    scan.set_defaults(func=_scan)
    compare = sub.add_parser("compare", help="compare findings between two builds")
    compare.add_argument("before")
    compare.add_argument("after")
    compare.add_argument("--config")
    compare.set_defaults(func=_compare)
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"modrelease: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
