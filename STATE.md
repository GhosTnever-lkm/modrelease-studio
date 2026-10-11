# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.38 (release checksum gate) — published

- Release workflow now runs `sha256sum --check` immediately after creating the ZIP sidecar and before the distribution install smoke test and publish step.
- Validation: 58/58 tests, 91% package line coverage. Five CI jobs, checksum check, packaged-archive smoke, release and Pages passed on `666172e`.
- Published v0.3.38; 88,593-byte ZIP checksum and archive integrity verified. There are 43 releases; preflight is 53/54 success (98.1%).
- Profile v1.2.99 and portfolio v1.3.77 reflect the release; workflows green, live pages checked.
- Six featured issue queues have zero open issues; seven key URLs returned HTTP 200.
- Linux checksum command validated against release assets; macOS/PowerShell examples documented but not executable in this Linux environment.

## Previous iteration — v0.3.37 (release checksum guidance)

- Documented SHA-256 sidecar verification on Linux/macOS/PowerShell and clarified that this is integrity checking, not a signature.
- 58 tests, 91% coverage; checksum/integrity, tag release smoke, cross-platform CI and Pages verified.

## Published baseline

- Latest verified release: v0.3.38.

## Next

1. Smoke-test public v0.3.38 tag and ZIP in clean environments; verify version, checksum, README badge, and sample scan.
2. Keep consumer pins at v0.3.25 unless runtime changes justify an update.
3. Continue concrete, tested improvements only.
