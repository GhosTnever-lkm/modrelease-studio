# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.37 (release checksum guidance) — published

- README documents `.sha256` sidecar checks for Linux `sha256sum`, macOS `shasum`, and Windows PowerShell `Get-FileHash`; it clarifies that a co-published checksum detects corruption but is not a separate signature/provenance attestation.
- Validation: 58/58 tests, 91% package line coverage. Five CI jobs, release archive smoke step, release, and Pages passed on `8137521`.
- Published v0.3.37; 88,534-byte ZIP checksum and archive integrity verified. There are 42 releases; preflight is 52/53 success (98.1%).
- Profile v1.2.98 and portfolio v1.3.76 updated; workflows and Pages green; live content checked.
- Six featured issue queues have zero open issues; seven key URLs returned HTTP 200.
- Linux `sha256sum --check` documentation example validated against release assets. macOS and PowerShell commands are documented; not executed in this Linux environment.
- Public v0.3.37 tag and downloaded ZIP were installed in separate clean venvs: both reported 0.3.37, scanned the sample READY (3 files), and the tagged README badge was 58/58.

## Previous iteration — v0.3.36 (README test-badge consistency guard)

- Regression discovers full unittest suite and asserts README badge matches test count; badge 58/58.
- 58 tests, 91% coverage; release ZIP smoke install, five CI jobs, release, Pages, checksum and integrity verified.

## Published baseline

- Latest verified release: v0.3.37.

## Next

1. Smoke-test public v0.3.37 tag and ZIP in fresh virtual environments; verify version, checksum docs, and sample output.
2. Keep consumer pins at v0.3.25 unless a runtime change justifies updating them.
3. Continue concrete, tested improvements only.
