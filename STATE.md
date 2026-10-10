# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.1 (contact cleanup)

- Added product README: value statement, "who is it for", the problem solved, three real scenarios, terminal demo screenshot (`docs/demo.png` — rendered from a real scan that catches a token, a bad localization header, and a missing supported_version), badges (live CI, live version, 9/9 tests, MIT).
- Removed the unconfigured Telegram placeholder from README and landing; GitHub and email contact links remain functional.
- Added GitHub Pages landing page (`docs/index.html`) with Download / Buy me a coffee / Contact buttons; Pages enabled on `/docs` at https://ghostnever-lkm.github.io/modrelease-studio/.
- Version bumped to 0.3.1 (package + CLI + pinned examples + test).
- Local checks: 9/9 tests pass; `compileall`, `modrelease --version`, `git diff --check` pass.

## Published baseline

- Latest verified published release before this iteration: v0.3.0.

## Next

1. Publish v0.3.1 and verify CI + Pages.
2. Add Telegram only if the owner supplies a real handle; GitHub/email remain available meanwhile.
3. Continue improving the mod-QA ecosystem and verified monetization links.
