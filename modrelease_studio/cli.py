"""Command line interface."""
from __future__ import annotations

import argparse
import json
import sys
import tomllib
from collections import Counter
from pathlib import Path

from . import __version__
from .models import Finding
from .reports import markdown, to_dict, write_json, write_markdown
from .scanner import scan_path


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
        print(json.dumps(to_dict(report), ensure_ascii=False, indent=2))
    else:
        print(markdown(report))
    if args.json_out:
        write_json(report, args.json_out)
    if args.md_out:
        write_markdown(report, args.md_out)
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
            rendered.append(f"{sign} [{severity}] {code} {path or '—'}: {message}{suffix}")
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
