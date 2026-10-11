# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.32 (scan-limit documentation) — published

- README explains the 30,000-entry indexing cap, 4 GiB ZIP aggregate uncompressed-size threshold, default 2,000,000-byte per-text-file content cap, configured 16 MiB maximum, and fixed 2 MiB Paradox parser ceiling. It explains entry overflow truncation and warns that any blocking limit finding invalidates a complete release approval.
- Corrected wording that implied `READY` is a safety certification; updated the test badge to 56/56.
- Validation: 56/56 tests; 91% package line coverage. Five CI jobs, release, and Pages passed on `4ebdce1`.
- Published v0.3.32; 86,310-byte ZIP checksum and integrity verified. 37 releases; preflight 47/48 successful (97.9%).
- Profile v1.2.93 and portfolio v1.3.71 show current release/metrics; profile and portfolio release workflows, Pages, and live content verified.
- All six featured QA issue queues are empty; seven critical release/demo links returned HTTP 200.

## Previous iteration — v0.3.31 (entry-limit report regression) — published

- CLI regression proves folder and ZIP entry overflow appears as `ENTRY_LIMIT` in JSON, status FAIL, exit code 1.
- 56 tests / 91% line coverage; five CI jobs, release, Pages, checksum, and ZIP integrity verified.

## Previous iteration — v0.3.30 (directory entry boundary test) — published

- Added deterministic directory fixtures at and above `MAX_ENTRIES`; exact limit accepted, overflow emits `ENTRY_LIMIT` and retains only the configured count.
- Suite: 55 tests, 91% package line coverage; five CI jobs, release, and Pages passed. The 84,332-byte ZIP checksum and archive integrity were verified.

## Previous iteration — v0.3.29 (archive limit boundary tests) — published

- Added small ZIP fixtures for exact and over-limit entry counts and total uncompressed size; 54/54 tests passed with 91% coverage.
- The five-platform preflight matrix, release, and Pages passed; the 83,626-byte ZIP checksum and archive integrity were verified.
- Profile v1.2.91 and portfolio v1.3.69 show the current scanner release and metrics; profile also links the verified ecosystem releases.

## Previous iteration — v0.3.28 (corrupt ZIP payload handling) — published

- A synthetic corrupted DEFLATE entry exposed an uncaught `zlib.error` from `ZipSource.read()`. The reader now catches decompression errors, and `scan_path()` reports `UNREADABLE_FILE` instead of aborting.
- Added an end-to-end regression that corrupts a ZIP payload after central-directory indexing.
- Validation: 52/52 tests pass; Coverage.py 7.16.2 reports 90% package line coverage. Five CI jobs for Ubuntu 3.11–3.13, Windows 3.13, and macOS 3.13 passed; the 80% floor remains enforced.
- Published v0.3.28; preflight, release, and Pages succeeded on commit `8e2f1dc`. ZIP is 81,793 bytes; its published SHA-256 was downloaded and verified. There are 33 releases; completed preflight history is 43/44 (97.7%).
- Profile v1.2.87 and portfolio v1.3.67 show the release and current metrics; profile release and Pages deployment succeeded, and live pages were checked.
- Runtime consumers remain intentionally pinned to v0.3.25 (the symlink-read fix); scanner v0.3.26 is docs-only and v0.3.28 adds tests/error handling.

## Published baseline

- Latest verified release: v0.3.28.

## Next

1. Smoke-test public v0.3.32 GitHub-tag install in isolated venv: CLI version, sample scan, and report output.
2. Add end-to-end ZIP `ARCHIVE_SIZE_LIMIT` regression using a tiny patched test limit; assert JSON finding and release-blocking exit code.
3. Keep consumer pins at v0.3.25 unless a runtime change justifies an update; recheck featured links/issues after the next release.
1. Add bounded tests for archive entry-count and total-uncompressed-size limits.
2. Add a consumer CI assertion that records exact scanner versions for default and explicit pins.
3. Recheck core issue queues and pinned-project links after the latest release cycle.
