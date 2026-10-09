# ModRelease Studio — project state

Updated: 2026-10-10

## Current iteration — v0.2.3

- Fix build comparison to preserve repeated identical findings. Added findings are shown with `+`, resolved findings with `-`, and count deltas use `(xN)`; the exit code still reflects errors in the candidate build.
- Added regression tests for duplicate counts increasing and decreasing. Local checks: 9/9 tests pass; `compileall`, `modrelease --version`, and `git diff --check` pass.
- Feature commit pushed to `main`: `9a867c9` (`Preserve duplicate findings in build comparisons`). Main CI run https://github.com/GhosTnever-lkm/modrelease-studio/actions/runs/37992887381 completed successfully. State commit `d3714f5` also passed main CI: https://github.com/GhosTnever-lkm/modrelease-studio/actions/runs/37992956765.
- Added tag-triggered release workflow to run tests, create a source ZIP and SHA-256 file, and publish a GitHub Release. Workflow has not yet been exercised; release publication is pending its first tagged run.
- `README.md`, `CHANGELOG.md`, package metadata, and CLI version are aligned to v0.2.3. Topics, MIT license, README, and prior v0.2.2 release were present in the current repository.

## Published baseline

- Latest verified published release before this iteration: [v0.2.2](https://github.com/GhosTnever-lkm/modrelease-studio/releases/tag/v0.2.2).
- Previously reported comparison and secret-scanner fixes are in published v0.2.0 and covered by the current 7-test baseline. Fresh local test run before this iteration: 7/7 passed.

## Next

1. Verify main CI for `9a867c9`.
2. If green, push tag `v0.2.3`, verify its release workflow and archive/checksum; repair any failure.
3. Update profile README and portfolio release/download links and topics only if their current pages need it.
