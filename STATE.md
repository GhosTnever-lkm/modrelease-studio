# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.27 (temporal symlink swap regression)

- Added a test that indexes a regular file, replaces it with an outside symlink, then asserts content reads are refused and the digest uses the `UNREADABLE` marker rather than target bytes.
- Validation: 51/51 tests pass locally; Coverage.py 7.16.2 reports 90% package line coverage. CI enforces an 80% floor on Ubuntu/Python 3.11–3.13, Windows/Python 3.13, and macOS/Python 3.13.

## Published baseline

- Latest verified release: v0.3.26.

## Next

1. Publish v0.3.27 and verify all five matrix jobs.
2. Verify its ZIP against the release SHA-256 asset.
3. Continue the active scanner-pin audit.
