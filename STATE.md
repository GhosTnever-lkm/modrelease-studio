# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.31 (entry-limit report regression) — published

- Added an end-to-end CLI test with synthetic folder and ZIP inputs over `MAX_ENTRIES`; both JSON reports retain `ENTRY_LIMIT`, report `FAIL`, and return exit code 1.
- Validation: 56/56 tests pass; Coverage.py 7.16.2 reports 91% package line coverage. Five CI jobs (Ubuntu Python 3.11–3.13, Windows 3.13, macOS 3.13), release workflow, and Pages passed.
- Published v0.3.31 on commit `5244137`; ZIP is 85,804 bytes, release SHA-256 verified, and archive integrity checked. There are 36 releases; completed preflight history is 46/47 (97.9%).
- Profile v1.2.92 and portfolio v1.3.70 show the release and metrics; profile release, portfolio release/Pages deployments, and live pages were verified.
- ModRelease Gate v1.0.30 and Paradox Mod Quality Gate v1.0.24 remain intentionally pinned at runtime v0.3.25 (no scanner runtime change) and assert exact installed versions in green CI.
- All six featured QA issue queues have zero open issues; seven critical release/demo links returned HTTP 200.

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

1. Document scanner bounds in README: entry count, ZIP unpacked-size threshold, default/configured text-file bytes, and how limit findings affect completeness.
2. Continue only a concrete, tested product improvement; keep consumer pins v0.3.25 unless a runtime change justifies an update.
3. Recheck featured links/issues after the next flagship release.
1. Add bounded tests for archive entry-count and total-uncompressed-size limits.
2. Add a consumer CI assertion that records exact scanner versions for default and explicit pins.
3. Recheck core issue queues and pinned-project links after the latest release cycle.
