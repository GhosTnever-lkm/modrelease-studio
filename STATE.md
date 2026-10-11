# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.13 (escape untrusted Markdown report cells)

- Updated the README GitHub Actions example and the project's preflight/release workflows from older first-party Action majors to v7.
- Retained tested archive hardening: reject non-regular ZIP entries, detect case/Unicode path collisions, and validate configured release policies.
- Version synchronized across package metadata, CLI, README pins, and the version regression test; CHANGELOG updated.
- Local validation: 22/22 tests pass, clean Paradox example scan is READY with zero findings, workflow YAML parses, and `git diff --check` passes.
- Published release includes ZIP + SHA-256; tag release workflow, preflight CI, and Pages build all succeeded.

## Published baseline

- Latest verified published release before this iteration: v0.3.12.

## Next

1. Publish v0.3.13 and verify release CI, preflight, and Pages.
2. Continue concrete, tested hardening of the mod-QA tools.
3. Add Telegram only if the owner supplies a real handle; do not invent wallet or payout details.
