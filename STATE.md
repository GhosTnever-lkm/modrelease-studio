# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.10 (refresh first-party workflow actions)

- Reject ZIP archive entries whose POSIX type is not a regular file, preventing special filesystem objects from being treated as ordinary payloads.
- Added a Paradox policy example, README configuration guidance, and included the example policy in release archives.
- Removed the unverified Boosty link from support copy; kept Buy Me a Coffee and GitHub Sponsors.
- Version synchronized across package metadata, CLI, pinned README install, and regression test; changelog updated.
- Local validation pending for v0.3.9. The CI workflow runs the checked-in policy alongside the baseline example scan; a reproducible sample report is linked from README and included in the release archive. README install and self-example pins use v0.3.6; regression tests cover malformed policy values, max-file-size validation, Windows-style separators, and case/Unicode collisions across folders and ZIPs. A local wheel build could not run because setuptools is absent in this environment with `--no-build-isolation`; tag CI remains the authoritative packaging check.

## Published baseline

- Latest verified published release before this iteration: v0.3.9.

## Next

1. Publish v0.3.10 and verify release workflow, CI, and Pages.
2. Add Telegram only if the owner supplies a real handle; GitHub/email remain available meanwhile.
3. Continue improving the mod-QA ecosystem and verified monetization links.
