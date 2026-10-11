# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.23 (symlink-safe directory reads) — published

- Fixed a trust-boundary gap: `DirectorySource.read()` previously opened a caller-provided relative path directly, so a symlinked descriptor or nested path could be read despite symlink entries being excluded from the scan inventory.
- Directory reads now require an indexed record, reject path traversal and every symlink component, and verify the resolved file remains beneath the scan root. Directory digests apply the same guard and use an unreadable marker if a file disappears or becomes unsafe during scanning.
- Added 3 regression tests covering symlinked files/directories, path allowlisting, bounded reads, and a stable digest for safe files.
- Validation: 46/46 tests pass; Coverage.py 7.16.2 reports 88% package line coverage. The CI floor remains 80%.
- Published v0.3.23; preflight, release, and Pages workflows succeeded on commit `9d6ca429e8b7beed859a8827f79a18f31e11b205`. Matrix jobs for Python 3.11, 3.12, and 3.13 all passed.
- Release ZIP is 77,238 bytes with SHA-256 asset; 28 releases exist. Current completed preflight history: 38/39 successful (97.4%).
- Profile v1.2.81 and portfolio v1.3.62 now link to v0.3.23 and display 46 tests / 88% coverage. Profile release, portfolio release, and Pages deployment succeeded. Profile's CI percentage is explicitly anchored to release commit `928fa07` (v0.3.21).

## Published baseline

- Latest verified release: v0.3.23.

## Next

1. Continue concrete, tested hardening of the local-first mod-QA tools.
2. Recheck the ecosystem after any scanner runtime change; keep consumer pins intentional.
3. Do not invent Telegram, wallet, payment, or payout details.
