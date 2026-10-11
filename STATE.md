# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.34 (test badge correction) — published

- Corrected the README test badge to 57/57 after v0.3.33 added the ZIP expanded-size CLI regression; no runtime behavior changed.
- Validation: 57/57 tests, 91% package line coverage. Five CI jobs (Ubuntu Python 3.11–3.13, Windows 3.13, macOS 3.13), release, and Pages passed on `a50f7f4`.
- Published v0.3.34; the 87,333-byte ZIP checksum and archive integrity verified. There are 39 releases; preflight is 49/50 successful (98.0%).
- Profile v1.2.95 and portfolio v1.3.73 reflect the release; both release workflows and Pages succeeded and live content was checked.
- Six featured QA issue queues have zero open issues; seven key release/demo/profile links returned HTTP 200.

## Recent technical work

- v0.3.33: end-to-end CLI regression verifies an oversized ZIP emits `ARCHIVE_SIZE_LIMIT` in JSON, status FAIL, exit code 1, using a small patched threshold.
- v0.3.32: documented 30,000-entry cap, 4 GiB aggregate ZIP threshold, default 2,000,000-byte text-file cap, configurable 16 MiB maximum, and 2 MiB Paradox parsing ceiling; clarified that READY is not a safety certification.
- v0.3.31: folder and ZIP `ENTRY_LIMIT` appear in JSON and block release scans.
- v0.3.30: deterministic folder entry-count exact/overflow boundary test.
- v0.3.29: ZIP entry-count and aggregate-uncompressed-size boundary tests.
- v0.3.28: corrupt DEFLATE content becomes `UNREADABLE_FILE` rather than aborting.
- Consumer integrations ModRelease Gate v1.0.30 and Paradox Mod Quality Gate v1.0.24 intentionally pin scanner v0.3.25; CI asserts the exact installed version. No runtime scanner change since that pin.

## Published baseline

- Latest verified release: v0.3.34.
- Public v0.3.33 was installed in an isolated venv and tested against a normal sample plus a synthetic oversized ZIP; the checks passed.

## Next

1. Smoke-test public v0.3.34 in a fresh virtual environment; verify CLI version, README badge, and release asset consistency.
2. Keep consumer pins at v0.3.25 unless a runtime change justifies an update.
3. Recheck featured links/issues after the next flagship release; pursue only concrete, tested improvements.
