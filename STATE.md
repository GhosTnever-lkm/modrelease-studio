# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.2 (project-specific required-path policies)

- Added case-insensitive `required_paths` glob checks with configurable ERROR/WARNING/INFO severity; ERROR findings now reliably block CI through the existing exit-code behavior.
- Added a Paradox policy example, README configuration guidance, and included the example policy in release archives.
- Removed the unverified Boosty link from support copy; kept Buy Me a Coffee and GitHub Sponsors.
- Version synchronized across package metadata, CLI, pinned README install, and regression test; changelog updated.
- Local validation: 13/13 tests pass, policy example scan is READY, release workflow YAML parses, diff check passes. A local wheel build could not run because setuptools is absent in this environment with `--no-build-isolation`; tag CI remains the authoritative packaging check.

## Published baseline

- Latest verified published release before this iteration: v0.3.1.

## Next

1. Publish v0.3.2 and verify release workflow, CI, and Pages.
2. Add Telegram only if the owner supplies a real handle; GitHub/email remain available meanwhile.
3. Continue improving the mod-QA ecosystem and verified monetization links.
