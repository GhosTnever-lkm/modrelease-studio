# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.23 (symlink-safe directory reads)

- Fixed a trust-boundary gap: `DirectorySource.read()` previously opened a caller-provided relative path directly, so a symlinked descriptor or nested path could be read despite symlink entries being excluded from the scan inventory.
- Directory reads now require an indexed record, reject path traversal and every symlink component, and verify the resolved file remains beneath the scan root. Directory digests apply the same guard and use an unreadable marker if a file disappears or becomes unsafe during scanning.
- Added 3 regression tests covering symlinked files/directories, path allowlisting, bounded reads, and a stable digest for safe files.
- Validation: 46/46 tests pass; Coverage.py 7.16.2 reports 88% package line coverage. The CI floor remains 80%.
- Existing published support matrix is Ubuntu/Python 3.11, 3.12, and 3.13 (v0.3.22).

## Published baseline

- Latest verified release: v0.3.22.

## Next

1. Publish v0.3.23 and verify all matrix jobs.
2. Refresh profile and portfolio metrics from the release.
3. Continue concrete, tested hardening without inventing wallet or payout details.
