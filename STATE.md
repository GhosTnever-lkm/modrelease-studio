# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.25 (cross-platform CI validation)

- Expanded CI matrix to Ubuntu/Python 3.11, 3.12, 3.13 plus Windows/Python 3.13 and macOS/Python 3.13.
- Added a ZIP case-collision regression; directory case/Unicode collision tests now detect filesystems that cannot represent distinct names and skip rather than fail spuriously. Symlink tests skip cleanly only if the runner cannot create symlinks.
- Local validation: 50/50 tests pass; Coverage.py 7.16.2 reports 89% package line coverage (80% enforced floor).
- Pending GitHub Windows/macOS matrix validation before tagging.

## Published baseline

- Latest verified release: v0.3.24.

## Next

1. Verify Windows and macOS workflow jobs; publish only after green.
2. Refresh profile and portfolio with only confirmed OS support.
3. Continue concrete, tested hardening without inventing wallet or payout details.
