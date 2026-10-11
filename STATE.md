# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.26 (refresh install examples) — published

- Updated the README GitHub Actions scanner pin and sample-policy explanation from v0.3.16 to v0.3.25. This release is documentation-only; consumers remain on v0.3.25 for the runtime symlink fix.
- Validation: 50/50 tests pass, line coverage 89%. Five platform jobs remain green: Ubuntu/Python 3.11–3.13, Windows/Python 3.13, macOS/Python 3.13.
- Published v0.3.26; preflight, release, and Pages passed on the install-doc update. Release ZIP is 79,717 bytes plus SHA-256; 31 releases exist. Current completed preflight history: 41/42 successful (97.6%).
- Repointed consumer defaults to the runtime fix v0.3.25: ModRelease Gate v1.0.29 and Paradox Mod Quality Gate v1.0.23. Both integration CI suites and release entries succeeded; the Pro launcher also uses v0.3.25.
- Profile v1.2.85 and portfolio v1.3.65 link scanner v0.3.26 and consumer releases; profile/Pages releases succeeded and live content was checked.

## Published baseline

- Latest verified release: v0.3.26.

## Next

1. Continue concrete, tested hardening of the local-first mod-QA tools.
2. Recheck ecosystem pins when runtime code changes; keep documentation-only versions distinct from runtime fixes.
3. Never invent owner wallet or payout details.
