# Changelog

## 0.3.2 - 2026-10-11

- Add configurable required-path glob checks with selectable ERROR/WARNING/INFO severity for project-specific release policies.
- Remove the unverified Boosty link from the support section.
- Bump package and CLI version to 0.3.2.

## 0.3.1 - 2026-10-11

- Remove the unconfigured Telegram placeholder from the README and landing page; GitHub and email remain the working contact options.
- Bump package and CLI version to 0.3.1.

## 0.3.0 - 2026-10-10

- Add product README: value statement, audience, the problem solved, three real scenarios, terminal demo screenshot, badges (CI, version, tests), pricing and contact sections.
- Add GitHub Pages landing page under `docs/` with Download / Buy / Contact actions and how-it-works demo.
- Bump package and CLI version to 0.3.0.

## 0.2.3 - 2026-10-10

- Preserve duplicate finding counts when comparing builds, so repeated findings are reported as added or resolved counts instead of disappearing in set-based comparison.
- Add regression tests for increases and decreases in duplicate findings.

## 0.2.2 - 2026-10-08

- Synchronize the importable package version with the published package version.
- Add `modrelease --version` so users can confirm the installed release.
- Add a regression test to prevent package-version metadata from drifting again.

## 0.2.1 - 2026-10-08

- Run regression tests in CI and scan only the clean example mod fixture, keeping synthetic secret fixtures out of the self-scan.

## 0.2.0 - 2026-10-08

- Fix build comparison when findings are present and preserve release-blocking exit behavior.
- Detect AWS access-key IDs, Slack tokens, Discord webhooks, unquoted and JSON API keys, and private-key files.
- Add regression tests using synthetic credentials and placeholder values.
- Correct the GitHub Actions example to install ModRelease Studio from a pinned repository tag.

## 0.1.0 - 2026-10-08

- Initial local-first CLI for folders and ZIP archives.
- Add packaging checks, secret pattern detection, and Paradox metadata/localization checks.
- Add JSON and Markdown reports, configuration, and build comparison.
