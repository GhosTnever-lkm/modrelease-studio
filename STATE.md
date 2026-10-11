# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.21 (CLI regression coverage)

- Added focused CLI tests for absent/default TOML config, configured scan policy loading, JSON stdout and JSON/Markdown file exports, findings-driven exit status, missing/invalid config handling, and `--version`.
- Validation: 43/43 tests pass; pinned Coverage.py 7.16.2 reports 89% package line coverage (80% CI floor). CLI module coverage is 97%.
- Updated the product README badge and coverage statement, synchronized package/CLI/test versions, and recorded the change in CHANGELOG.
- Previous baseline: v0.3.20, 36/36 tests, 84% coverage.

## Published baseline

- Latest release before current iteration: v0.3.20.

## Next

1. Publish v0.3.21 and verify release/preflight workflows.
2. Refresh profile and portfolio links/metrics from verified release data.
3. Continue concrete, tested hardening of the local-first mod-QA tools.
