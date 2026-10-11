# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.35 (release ZIP smoke automation) — published

- Release workflow tests the distributable before publishing: extract built ZIP, install into an isolated venv, assert `modrelease --version` matches the tag, scan the included clean example, and require JSON status READY.
- The v0.3.35 GitHub Actions release job passed every step including `Smoke-test packaged release archive`; preflight matrix and Pages passed on `aaf6e1e`. 57/57 tests; 91% package line coverage.
- Published v0.3.35; archive is 87,432 bytes. Downloaded SHA-256 and ZIP integrity verified. There are 40 releases; preflight is 50/51 successful (98.0%).
- Profile v1.2.96 and portfolio v1.3.74 updated; release workflows and Pages succeeded; live pages verified.
- Six core QA issue queues have zero open issues; seven key URLs return HTTP 200.
- Manual smoke tests of public v0.3.35 Git tag and downloadable ZIP in separate clean venvs both reported version 0.3.35, scanned the sample READY (3 files), and matched the 57/57 README badge.
- Consumer integrations ModRelease Gate v1.0.30 and Paradox Mod Quality Gate v1.0.24 intentionally remain on runtime scanner v0.3.25; both assert exact installed versions in CI.

## Previous iteration — v0.3.34 (badge correction)

- README badge corrected to 57/57 after v0.3.33's expanded ZIP-size regression; no runtime behavior change.
- 57 tests, 91% coverage; release, five CI jobs, Pages, ZIP checksum, and integrity verified.

## Published baseline

- Latest verified release: v0.3.35.

## Next

1. Add a regression ensuring the README test badge matches the discovered unittest count, preventing stale metrics after future test additions.
2. Keep consumer pins at v0.3.25 unless a runtime change justifies updating them.
3. Continue only concrete, tested product improvements.
