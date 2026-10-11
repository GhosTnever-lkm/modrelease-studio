# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.33 (ZIP expanded-size report regression) — published

- Added an end-to-end CLI regression with a tiny patched `MAX_TOTAL_UNCOMPRESSED`: oversized ZIP reports `ARCHIVE_SIZE_LIMIT` in JSON, has status FAIL, and returns exit code 1 while preserving the scanned file count and total bytes.
- Validation: 57/57 tests pass; package line coverage 91%. Five CI jobs, release, and Pages passed on `316f52d`.
- Published v0.3.33; archive is 87,290 bytes, published checksum and ZIP integrity verified. There are 38 releases; preflight history is 48/49 success (98.0%).
- Profile v1.2.94 and portfolio v1.3.72 updated; six core issues zero; seven key URLs HTTP 200.
- Fresh-venv smoke test of public v0.3.33: CLI version correct, included sample scanned READY with JSON/Markdown output, and a synthetic ZIP over the patched expansion limit produced `ARCHIVE_SIZE_LIMIT`, FAIL, exit 1.
- Follow-up: update README badge from 56/56 to 57/57 (new .33 regression raised the suite by one), then synchronize portfolio metrics.

## Previous iteration — v0.3.32 (scan-limit documentation) — published

- README documented entry-count, archive expanded-size, general text-file, configurable file-size, and Paradox parser bounds; clarified incomplete scans and that READY is not a safety certification. Updated test badge.
- 56/56 tests, 91% coverage; five CI jobs, release, Pages, checksum, and ZIP integrity passed.

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

1. Smoke-test public v0.3.33 tag in a clean virtual environment against an ordinary sample and synthetic oversized ZIP; compare with README limits.
2. Keep consumer pins at v0.3.25 unless a runtime change justifies an update; recheck featured links/issues after the next release.
3. Continue only a concrete, tested product improvement; no placeholder Pro storefronts.
1. Add bounded tests for archive entry-count and total-uncompressed-size limits.
2. Add a consumer CI assertion that records exact scanner versions for default and explicit pins.
3. Recheck core issue queues and pinned-project links after the latest release cycle.
