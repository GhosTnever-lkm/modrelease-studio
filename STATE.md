# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.25 (cross-platform CI) — published

- The 50-test suite passes on five CI jobs: Ubuntu/Python 3.11, 3.12, 3.13; Windows/Python 3.13; macOS/Python 3.13.
- Added a ZIP case-collision regression. Directory case/Unicode collision tests skip when host filesystems cannot represent distinct names; symlink tests skip only if the runner cannot create symlinks.
- Local validation: 50/50 tests; Coverage.py 7.16.2 reports 89% package line coverage (80% enforced floor).
- Published v0.3.25; preflight, release, and Pages workflows passed on commit `701432cc2a00fa801c3b783bdb2b66a36a6ad095`. All five matrix jobs succeeded.
- Release ZIP is 79,670 bytes with SHA-256 asset; 30 releases exist. Completed preflight history: 40/41 successful (97.6%).
- Profile v1.2.83 and portfolio v1.3.64 now show confirmed Ubuntu, Windows, and macOS support; profile release, portfolio release, and Pages deployment succeeded; live pages were checked. Profile's historical success-rate snapshot remains explicitly scoped through v0.3.21's release commit.

## Published baseline

- Latest verified release: v0.3.25.

## Next

1. Continue concrete, tested hardening of the local-first mod-QA tools.
2. Recheck the ecosystem after any scanner runtime change; keep consumer pins intentional.
3. Do not invent Telegram, wallet, payment, or payout details.
