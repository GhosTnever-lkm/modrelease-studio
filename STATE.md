# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.38 (release checksum gate) — published

- Release workflow runs `sha256sum --check` immediately after writing the ZIP sidecar and before distribution install smoke/publish.
- Validation: 58/58 tests, 91% package line coverage. Five CI jobs, checksum gate, packaged ZIP smoke, release and Pages passed on `666172e`.
- Published v0.3.38; 88,593-byte ZIP checksum and archive integrity verified. There are 43 releases; preflight 53/54 success (98.1%).
- Profile v1.2.99 and portfolio v1.3.77 reflect the release; workflows and Pages green. Six issues zero; seven key URLs HTTP 200.
- Public v0.3.38 tag and ZIP were installed in clean venvs; both report 0.3.38 and scan sample READY (3 files). README badge is 58/58.
- Linux SHA-256 documentation command was validated; macOS and PowerShell commands documented but not executable locally.

## Previous iteration — v0.3.37 (checksum documentation)

- Added SHA-256 sidecar verification for Linux/macOS/PowerShell and clarified this is integrity checking, not a separate signature.
- 58 tests, 91% coverage; checksum/integrity, release smoke, matrix and Pages passed.

## Published baseline

- Latest verified release: v0.3.38.

## Next

1. Add OS-specific CI checks for README checksum examples: Linux `sha256sum`, macOS `shasum`, and Windows PowerShell `Get-FileHash`.
2. Keep consumer pins at v0.3.25 unless runtime changes justify updating them.
3. Continue concrete, tested product improvements only.
