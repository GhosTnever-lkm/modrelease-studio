# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.22 (verify Python 3.13 CI support)

- Added focused CLI tests for absent/default TOML config, configured scan policy loading, JSON stdout and JSON/Markdown file exports, findings-driven exit status, missing/invalid config handling, and `--version`.
- Validation: 43/43 tests pass; pinned Coverage.py 7.16.2 reports 89% package line coverage (80% CI floor). CLI module coverage is 97%.
- Product README badge/coverage statement, package version, CLI version regression, and CHANGELOG are synchronized.
- Published v0.3.21; release workflow and preflight passed on commit `928fa0712e578db92c5f1b430fad470543171007`. Pages workflow passed. Release ZIP: 73,072 bytes, plus SHA-256 asset.
- At release commit `928fa07`, account metrics were 26 releases and 35/36 completed preflight runs successful (97.2%). A later docs-only STATE sync added one successful workflow run; current completed preflight history is 36/37 (97.3%). Profile v1.2.79 and portfolio v1.3.60 now point to this release and show 43 tests / 89% coverage. Both release workflows and the portfolio Pages deployment passed; raw profile README and live site returned HTTP 200.

## Published baseline

- Latest verified release: v0.3.21.

## Next

1. Continue concrete, tested hardening of the local-first mod-QA tools.
2. Recheck the ecosystem after any scanner runtime change; keep consumer pins intentional.
3. Do not invent Telegram, wallet, payment, or payout details.


- Extend CI matrix to Python 3.13 after confirming the full suite runs locally on Python 3.13.14. Pending final GitHub preflight verification.
