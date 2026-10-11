# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.26 (refresh install examples)

- Updated the README GitHub Actions install pin and sample-policy explanation to the current scanner runtime v0.3.25 (the v0.3.26 changes are documentation-only).
- Validation before release: 50/50 tests pass locally; line coverage 89%. The v0.3.25 Windows/macOS and Ubuntu CI matrix is green.

## Published baseline

- Latest verified release: v0.3.25.

## Next

1. Publish v0.3.26 and verify all workflow jobs.
2. Update the ModRelease Gate and Paradox Quality Gate consumers to scanner v0.3.25 because v0.3.23 contains a runtime safety fix.
3. Continue concrete, tested hardening.
