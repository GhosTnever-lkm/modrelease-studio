# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.40 (bytecode-free release archive) — published

- Audit of public v0.3.39 found 13 `__pycache__`/`.pyc` entries in the release ZIP: tests run before `zip -r` and ignored bytecode was included from the working tree.
- Fixed `.github/workflows/release.yml`: remove test-generated caches before archiving and fail release if cache/bytecode entries remain. Updated version, changelog, and CLI version regression; no scanner runtime change.
- Published v0.3.40. All 58 tests pass, 91% package line coverage; five preflight jobs, release checksum/archive smoke, Pages and release passed on `725657d`.
- Verified local artifact and public release asset: 33,881 bytes, zero bytecode entries, sidecar checksum valid. Installed public tag and ZIP independently in clean venvs; both report 0.3.40 and scan the example READY/3 files.
- Profile v1.2.101 and portfolio v1.3.79 updated to 45 releases, 55/56 preflight runs successful (98.2%), 58 tests / 91%; both release workflows passed and Pages deployment was initiated.

## Previous iteration — v0.3.39 (cross-platform checksum documentation)

- CI exercised Linux `sha256sum`, macOS `shasum`, and Windows PowerShell `Get-FileHash` instructions. 58 tests/91% coverage; five CI jobs, release and Pages passed.
- Public tag and ZIP clean-install smoke tests passed; checksum and README badge verified. Packaging audit uncovered ignored Python caches; corrected in v0.3.40.

## Published baseline

- Latest verified release: v0.3.40.
- Consumers remain pinned at v0.3.25: v0.3.40 is packaging/workflow-only and does not change scanner runtime.

## Next

1. Audit release ZIP/asset workflows in the core ecosystem for ignored build outputs; patch only concrete issues.
2. Recheck core issue queues, featured links, profile/site deployment, and exact pinned scanner versions.
3. Continue concrete, tested improvements; do not publish unreviewed Pro terms or invented wallet/payment details.
