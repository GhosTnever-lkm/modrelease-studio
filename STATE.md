# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.18 (verify supported Python range in CI)

- Updated the README GitHub Actions example and the project's preflight/release workflows from older first-party Action majors to v7.
- Retained tested archive hardening: reject non-regular ZIP entries, detect case/Unicode path collisions, and validate configured release policies.
- JSON and Markdown reports keep only the source basename; a regression test proves parent directories are absent from shareable output. Updated the README GitHub Actions example from stale v0.3.9 to current scanner v0.3.16.
- Version synchronized across package metadata, CLI, and the version regression test; CHANGELOG updated.
- Local validation: 28/28 tests pass, clean Paradox example scan is READY with zero findings, workflow YAML parses, and `git diff --check` passes.
- Published and verified: v0.3.16 release ZIP + SHA-256; tag release, preflight CI, and Pages workflows succeeded.
- Published and verified: v0.3.17 release ZIP + SHA-256; tag release and preflight CI succeeded; Pages deployment succeeded.

## Published baseline

- Latest verified published release: v0.3.17.

## Next

1. Verify v0.3.18 CI on both supported Python versions and release assets.
2. Continue concrete, tested hardening of the mod-QA tools.
3. Add Telegram only if the owner supplies a real handle; do not invent wallet or payout details.
