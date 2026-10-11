# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.41 (version-independent checksum docs) — published

- Replaced hard-coded v0.3.36 names in checksum instructions with a wildcard for Linux/macOS and exact-one-sidecar discovery in PowerShell; PowerShell derives the ZIP path from the sidecar.
- Updated the Linux/macOS/Windows CI fixtures to exercise the filename selection and verification commands.
- Published v0.3.41; 58/58 tests pass, package line coverage 91%, all five preflight jobs and release workflow passed; Pages deployment passed on `56afd7b`.
- Verified public v0.3.41 ZIP sidecar using the new wildcard command; archive size 34,089 bytes. Scanner runtime is unchanged, so consumers remain intentionally pinned at v0.3.25.
- Refreshed profile v1.2.103 and portfolio v1.3.82 with 46 releases, 56/57 preflight success (98.2%), 58 tests, 91% coverage, current ZIP size, and v0.3.41 links. Both release workflows and Pages passed; live page confirmed.

## Previous iteration — v0.3.40 (bytecode-free release archive)

- Release packaging removes test-generated `__pycache__` and fails if `.pyc`/`.pyo` entries remain. Public v0.3.40 ZIP has zero bytecode entries; checksum and clean tag/ZIP install smoke passed.

## Published baseline

- Latest verified release: v0.3.41.
- Consumers remain pinned at v0.3.25; recent releases changed packaging/docs/CI only.

## Next

1. Continue only concrete, tested improvements to the local-first QA tools; avoid speculative Pro offers.
2. Recheck core issue queues, featured links, and consumer pins after material runtime releases.
3. Keep owner-dependent payout, license, and support terms pending; do not invent credentials or payment details.
