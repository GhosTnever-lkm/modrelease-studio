# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.29 (archive limit boundary tests) — published

- Added small synthetic ZIP fixtures for exact and over-limit entry counts and total uncompressed size; tests exercise bounds without allocating large payloads.
- Validation: 54/54 tests pass; Coverage.py 7.16.2 reports 91% package line coverage. Five CI jobs (Ubuntu Python 3.11–3.13, Windows 3.13, macOS 3.13), release workflow, and Pages passed.
- Published v0.3.29 on commit `1cd5d8f`; ZIP is 83,626 bytes, release SHA-256 verified, and archive integrity checked. There are 34 releases; completed preflight history is 44/45 (97.8%).
- Profile v1.2.88 and portfolio v1.3.68 now link to the release and verified metrics; both release workflows and the Pages deployment passed, and live portfolio content was verified.
- No scanner runtime behavior changed; ModRelease Gate and Paradox Mod Quality Gate remain pinned to v0.3.25.

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

1. Add bounded tests for archive entry-count and total-uncompressed-size limits.
2. Add a consumer CI assertion that records exact scanner versions for default and explicit pins.
3. Recheck core issue queues and pinned-project links after the latest release cycle.
