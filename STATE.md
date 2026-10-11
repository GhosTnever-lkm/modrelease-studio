# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.7 (strict policy validation)

- Added case-insensitive `required_paths` glob checks with configurable ERROR/WARNING/INFO severity; ERROR findings now reliably block CI through the existing exit-code behavior.
- Added a Paradox policy example, README configuration guidance, and included the example policy in release archives.
- Removed the unverified Boosty link from support copy; kept Buy Me a Coffee and GitHub Sponsors.
- Version synchronized across package metadata, CLI, pinned README install, and regression test; changelog updated.
- Local validation: 13/13 tests pass, policy example scan is READY, release workflow YAML parses, diff check passes. The CI workflow runs the checked-in policy alongside the baseline example scan; a reproducible sample report is linked from README and included in the release archive. README install and self-example pins use v0.3.6; regression tests cover malformed required-path/required-file values, max-file-size validation, and Windows-style separator normalization. A local wheel build could not run because setuptools is absent in this environment with `--no-build-isolation`; tag CI remains the authoritative packaging check.

## Published baseline

- Latest verified published release before this iteration: v0.3.1.

## Next

1. Publish v0.3.2 and verify release workflow, CI, and Pages.
2. Add Telegram only if the owner supplies a real handle; GitHub/email remain available meanwhile.
3. Continue improving the mod-QA ecosystem and verified monetization links.
