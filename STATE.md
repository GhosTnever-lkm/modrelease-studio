# ModRelease Studio — project state

Updated: 2026-10-11

## Current iteration — v0.3.22 (Python 3.13 CI support) — published

- Extended the Ubuntu preflight matrix to Python 3.11, 3.12, and 3.13. Local Python 3.13.14 and all remote matrix jobs pass the full 43-test suite and the 80% coverage floor.
- Package line coverage remains 89%. No runtime dependencies were added.
- Published v0.3.22; preflight, release, and Pages workflows succeeded on commit `48d69febdbb68842f3b43b09a42e0c5c51a4ef38`; matrix jobs for all three Python versions passed.
- Release ZIP: 73,126 bytes, plus SHA-256 asset. There are 27 published releases.
- Current completed preflight history: 37/38 successful (97.4%). The profile's success-rate display remains a clearly scoped snapshot through release commit `928fa07`, not the changing all-time count.
- Profile v1.2.80 and portfolio v1.3.61 now point to v0.3.22 and show verified Python 3.13 support. Profile release, portfolio release, Pages deployment, and live page checks succeeded.

## Published baseline

- Latest verified release: v0.3.22.

## Next

1. Continue concrete, tested hardening of the local-first mod-QA tools.
2. Recheck the ecosystem after any scanner runtime change; keep consumer pins intentional.
3. Do not invent Telegram, wallet, payment, or payout details.
