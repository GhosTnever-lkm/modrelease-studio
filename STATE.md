# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.24 (ZIP source regression coverage)

- Added tests for bounded ZIP entry reads, rejection of unindexed/traversal paths, archive SHA-256, graceful read failure, and malformed ZIP reporting.
- Validation: 49/49 tests pass on the local Python 3.13.14 environment; Coverage.py 7.16.2 reports 89% package line coverage. The Ubuntu/Python 3.11/3.12/3.13 CI matrix and 80% floor remain enabled.
- The v0.3.23 symlink guard remains in place and covered by dedicated regressions.

## Published baseline

- Latest verified release: v0.3.23.

## Next

1. Publish v0.3.24 and verify all matrix jobs.
2. Refresh profile and portfolio metrics from the release.
3. Continue concrete, tested hardening without inventing wallet or payout details.
