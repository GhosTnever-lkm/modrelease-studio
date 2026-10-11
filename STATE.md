# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.27 (temporal symlink swap regression) — published

- Added a test that indexes a regular file, replaces it with an outside symlink, then asserts content reads are refused and the digest uses the `UNREADABLE` marker rather than target bytes.
- Validation: 51/51 tests pass; Coverage.py 7.16.2 reports 90% package line coverage. CI enforces 80% across Ubuntu/Python 3.11–3.13, Windows/Python 3.13, and macOS/Python 3.13.
- Published v0.3.27; all five preflight jobs, release, and Pages succeeded on commit `261cdf2`. ZIP size 80,543 bytes; external SHA-256 matches the published checksum.
- 32 releases exist; completed preflight history is 42/43 successful (97.7%), anchored to commit `261cdf2`.
- Consumers ModRelease Gate v1.0.29 and Paradox Mod Quality Gate v1.0.23 use runtime v0.3.25, the release containing the symlink-read fix; scanner v0.3.26 is docs-only.
- Profile v1.2.86 and portfolio v1.3.66 show the current release.

## Published baseline

- Latest verified release: v0.3.27.

## Next

1. Add a corrupted compressed-payload ZIP fixture and validate graceful read failure.
2. Add bounded tests for archive entry-count and total-uncompressed-size limits.
3. Add a consumer CI assertion that records the exact scanner version for default and explicit pins.
