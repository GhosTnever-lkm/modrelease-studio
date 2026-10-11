# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.28 (corrupt ZIP payload handling)

- A synthetic corrupted DEFLATE entry exposed an uncaught `zlib.error` from `ZipSource.read()`. The reader now catches that decompression exception and `scan_path()` reports `UNREADABLE_FILE` rather than aborting the scan.
- Added an end-to-end regression that corrupts a ZIP payload after central-directory indexing.
- Validation: 52/52 tests pass; Coverage.py 7.16.2 reports 90% package line coverage. The 80% floor and five-platform CI matrix remain enabled.

## Published baseline

- Latest verified release: v0.3.27.

## Next

1. Publish v0.3.28 and verify all five matrix jobs.
2. Verify the ZIP's published SHA-256.
3. Continue limits and consumer-version tests from the queue.
