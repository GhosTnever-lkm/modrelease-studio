# ModRelease Studio — project state

Updated: 2026-10-10

## Current iteration — v0.3.0 (flagship launch, Phase 1)

- Added product README: value statement, "who is it for", the problem solved, three real scenarios, terminal demo screenshot (`docs/demo.png` — rendered from a real scan that catches a token, a bad localization header, and a missing supported_version), badges (live CI, live version, 9/9 tests, MIT).
- Added pricing + contact sections (GitHub, email; Telegram placeholder pending user handle).
- Added GitHub Pages landing page (`docs/index.html`) with Download / Buy me a coffee / Contact buttons; Pages enabled on `/docs` at https://ghostnever-lkm.github.io/modrelease-studio/.
- Version bumped to 0.3.0 (package + CLI + pinned examples + test).
- Local checks: 9/9 tests pass; `compileall`, `modrelease --version`, `git diff --check` pass.

## Published baseline

- Latest verified published release: v0.2.3 (this iteration will publish v0.3.0).

## Next

1. Push v0.3.0, tag, release, confirm CI + Pages build green.
2. Get Telegram handle + wallet address confirmation from the user; fill README/landing placeholders.
3. Then move to ecosystem repos: modrelease-studio-action, bugbundle, game-text-gate.
