# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.36 (README test-badge consistency guard) — published

- Added a regression that discovers the full unittest suite and asserts the README shield badge matches its count, so new test additions cannot silently leave stale test metrics. README badge now reads 58/58.
- Validation: 58/58 tests, 91% package line coverage. Five CI jobs, release, and Pages passed on `e3e2b7e`.
- Release workflow smoke-tested the extracted distribution: isolated install, tag-matched CLI version, included sample scan READY, then published v0.3.36. Downloaded 87,994-byte ZIP checksum and integrity verified. There are 41 releases; preflight is 51/52 successful (98.1%).
- Profile v1.2.97 and portfolio v1.3.75 show current metrics; release workflows and Pages succeeded; live content verified.
- Six featured issue queues have zero open issues; seven key release/demo/profile URLs returned HTTP 200.
- Fresh-v-0.3.36 public Git-tag and release-ZIP installs both reported version 0.3.36 and produced READY sample reports; tagged README badge is 58/58.
- Consumer integrations remain intentionally pinned at runtime scanner v0.3.25; both assert exact installed scanner versions in CI.

## Previous iteration — v0.3.35 (release ZIP smoke automation)

- Release workflow extracts the package ZIP, installs in a fresh venv, checks CLI/tag parity and scans the included clean example before publication.
- Release smoke job passed; preflight, release, and Pages green. 57/57 tests, 91% coverage; 87,432-byte ZIP verified.

## Published baseline

- Latest verified release: v0.3.36.

## Next

1. Document and verify SHA-256 release ZIP validation commands for Linux/macOS and PowerShell.
2. Keep consumer pins at v0.3.25 unless a runtime change justifies updating them.
3. Continue only concrete, tested improvements.
