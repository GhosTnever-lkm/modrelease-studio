# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.42 (safe terminal output) — published

- `modrelease compare` now escapes control-category Unicode in untrusted paths and messages. Newline, ANSI ESC, and bidi-control content is visibly encoded so hostile filenames cannot inject terminal formatting or fake output lines.
- Added a regression for embedded newline, ANSI color escape, and bidi formatting control. Local public tag and ZIP installs both detect the synthetic token while producing one safe output line.
- Published v0.3.42. All 59 tests pass, package line coverage 91%; all five preflight jobs, release, and Pages passed on `5b55306`.
- Public 34,641-byte release ZIP checksum verified; separate clean tag/ZIP installs report version 0.3.42.
- Profile v1.2.104 and portfolio v1.3.83 reflect 47 releases, 57/58 preflight successes (98.3%), 59 tests, 91% coverage and current asset size; release workflows and Pages passed.

## Previous iteration — v0.3.41 (version-independent checksum instructions)

- Linux/macOS docs use a version-independent sidecar glob; PowerShell detects exactly one matching sidecar. Cross-platform CI verifies instructions. No scanner runtime change.

## Published baseline

- Latest verified release: v0.3.42.
- Consumers remain pinned at v0.3.25; v0.3.41 was docs/CI-only, while v0.3.42 changes compare rendering only and not scanner policy/API.

## Next

1. Audit other local-first QA tools for terminal/output injection from untrusted filenames; reproduce findings first.
2. Recheck core issue queues, featured links, and consumer pins after material runtime releases.
3. Keep owner-dependent payout, license, and support terms pending; do not invent credentials or payment details.
