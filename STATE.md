# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.24 (ZIP source regression coverage) — published

- Added tests for bounded ZIP entry reads, rejection of unindexed/traversal paths, archive SHA-256, graceful decompression failure, and malformed ZIP reporting.
- Validation: 49/49 tests pass; Coverage.py 7.16.2 reports 89% package line coverage (CI floor 80%).
- Published v0.3.24; preflight, release, and Pages workflows passed on commit `e2b2bd92b762e21d977526315ae870df6e81bc6b`. Ubuntu/Python 3.11, 3.12, and 3.13 jobs all passed.
- Release ZIP is 78,763 bytes with SHA-256 asset; 29 releases exist. Completed preflight history is 39/40 successful (97.5%).
- Profile v1.2.82 and portfolio v1.3.63 show v0.3.24, 49 tests, 89% coverage, and Python 3.11–3.13. Profile/portfolio releases and Pages deployment succeeded; live README and site were checked. Profile's historical CI percentage remains explicitly scoped to v0.3.21's release commit.
- The v0.3.23 symlink guard remains active; its dedicated file, directory, path-allowlist, and digest regression tests pass.

## Published baseline

- Latest verified release: v0.3.24.

## Next

1. Continue concrete, tested hardening of the local-first mod-QA tools.
2. Recheck the ecosystem after any scanner runtime change; keep consumer pins intentional.
3. Do not invent Telegram, wallet, payment, or payout details.
