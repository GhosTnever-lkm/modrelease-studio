# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.20 (expand Paradox tests and raise coverage floor)

- Updated the README GitHub Actions example and the project's preflight/release workflows from older first-party Action majors to v7.
- Retained tested archive hardening: reject non-regular ZIP entries, detect case/Unicode path collisions, and validate configured release policies.
- JSON and Markdown reports keep only the source basename; a regression test proves parent directories are absent from shareable output. Updated the README GitHub Actions example from stale v0.3.9 to current scanner v0.3.16.
- Version synchronized across package metadata, CLI, and the version regression test; CHANGELOG updated.
- Added optional `test` extra for pinned Coverage.py 7.16.2; the Python 3.11/3.12 preflight matrix now reports line coverage and enforces an 80% floor.
- Local validation: 36/36 tests pass; Coverage.py reports 84% line coverage across package modules. The coverage output uses `--source=modrelease_studio` and excludes tests and dependencies.
- Published and verified: v0.3.16 release ZIP + SHA-256; tag release, preflight CI, and Pages workflows succeeded.
- Published and verified: v0.3.17 release ZIP + SHA-256; tag release and preflight CI succeeded; Pages deployment succeeded.

## Published baseline

- Latest verified published release before this iteration: v0.3.18.

## Next

1. Continue concrete, tested hardening of the mod-QA tools.
2. Add Telegram only if the owner supplies a real handle; do not invent wallet or payout details.
