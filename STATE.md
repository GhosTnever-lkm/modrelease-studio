# ModRelease Studio — project state

Updated: 2026-10-10

## Current iteration — v0.2.3

- Fix build comparison to preserve repeated identical findings. Added findings are shown with `+`, resolved findings with `-`, and count deltas use `(xN)`; the exit code still reflects errors in the candidate build.
- Added regression tests for duplicate counts increasing and decreasing. Local checks: 9/9 tests pass; `compileall`, `modrelease --version`, and `git diff --check` pass.
- Feature commit `9a867c9` and state commits `d3714f5`, `e3f648f` are pushed to `main`; main CI runs `37992887381`, `37992956765`, and `37993013034` succeeded.
- Tag `v0.2.3` and release are published: https://github.com/GhosTnever-lkm/modrelease-studio/releases/tag/v0.2.3. Release workflow `37993022731` succeeded. ZIP is 46,257 bytes; downloaded ZIP matches sidecar SHA-256 `c7c3b9dec7b0743f1db07fb4f4bb53d70a64b2c1971ece9144ab74be4298b34d`.
- Portfolio updated to v1.3.17 (commit `f68b55b`); Pages run `37993182652` and release run `37993186727` passed. Live site returned HTTP 200 with the new release/download links.
- Profile README updated to v1.0.1 (commit `45837de`); release workflow `37993205253` passed, and the live README includes v0.2.3 release and download links.
- `README.md`, `CHANGELOG.md`, package metadata, and CLI version are aligned to v0.2.3. Topics, MIT license, README, and prior v0.2.2 release were present in the current repository.

## Published baseline

- Latest verified published release: [v0.2.3](https://github.com/GhosTnever-lkm/modrelease-studio/releases/tag/v0.2.3).
- Previously reported comparison and secret-scanner fixes are in published v0.2.0 and covered by the current 7-test baseline. Fresh local test run before this iteration: 7/7 passed.

## Next

1. Continue with the next outstanding existing project from the account STATE; do not reopen the completed CS:GO overlay task unless the user asks.
2. Refresh account-wide metadata audit after the next project iteration.
