# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.39 (cross-platform checksum-doc tests) — published

- Preflight matrix now exercises the published SHA-256 snippets on Ubuntu (`sha256sum`), macOS (`shasum -a 256`), and Windows PowerShell (`Get-FileHash` parser/comparison). All matching platform steps passed.
- Validation: 58/58 tests, 91% package line coverage; all five CI jobs, release checksum gate, packaged archive smoke, release and Pages passed on `12e9c0c`.
- Published v0.3.39; 88,654-byte ZIP checksum and archive integrity verified. There are 44 releases; preflight 54/55 successful (98.2%).
- Profile v1.2.100 and portfolio v1.3.78 are current; profile release and Pages green. Six core issue queues empty; seven key URLs HTTP 200.
- Manual v0.3.38 tag/ZIP install smoke passed; Linux checksum command also verified against a real release asset.

## Previous iteration — v0.3.38 (release checksum gate)

- Release job runs `sha256sum --check` after generating the checksum and before installing/smoking/publishing the ZIP.
- 58 tests, 91% coverage; checksum, ZIP install smoke, release, cross-platform tests and Pages passed.

## Published baseline

- Latest verified release: v0.3.39.

## Next

1. Smoke-test public v0.3.39 tag and ZIP in clean venvs; verify version, README badge, checksum and sample scan.
2. Keep consumer pins at v0.3.25 unless a runtime change warrants updating them.
3. Continue concrete, tested improvements only.
