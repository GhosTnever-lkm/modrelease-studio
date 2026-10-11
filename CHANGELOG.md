# Changelog

## 0.3.26 - 2026-10-11

- Refresh GitHub Actions scanner examples from v0.3.16 to v0.3.25, including the explanation of the pinned sample.


## 0.3.25 - 2026-10-11

- Extend CI coverage to Windows and macOS on Python 3.13 while keeping the Ubuntu/Python 3.11–3.13 matrix.
- Add a ZIP case-collision regression and make directory case/Unicode collision tests skip when the host filesystem cannot represent distinct names.
- Increase the suite to 50 tests; measured package line coverage remains 89%.


## 0.3.24 - 2026-10-11

- Add ZIP-source regressions for bounded reads, indexed-entry restrictions, deterministic archive hashing, decompression failures, and invalid ZIP reporting.
- Increase the suite to 49 passing tests; measured package line coverage returns to 89%, above the 80% CI floor.


## 0.3.23 - 2026-10-11

- Prevent directory-backed reads and digests from following symbolic links or opening paths absent from the scan index.
- Add three regressions for file/directory symlinks, indexed-path enforcement, bounded reads, and deterministic safe-file digests.
- Raise the suite to 46 tests; package line coverage is 88%, above the enforced 80% floor.


## 0.3.22 - 2026-10-11

- Extend the Ubuntu preflight matrix to Python 3.13; the full 43-test suite and 80% coverage floor run on Python 3.11, 3.12, and 3.13.


## 0.3.21 - 2026-10-11

- Add CLI regression tests for default and explicit configuration, JSON/Markdown exports, error exit codes, and version output.
- Raise the full test suite to 43 tests and measured package line coverage to 89%.


## 0.3.20 - 2026-10-11

- Add unit tests for descriptor parsing and Paradox localization edge cases; measured package line coverage rises to 84%.
- Raise the CI coverage floor from 75% to 80% and refresh the test badge to 36/36.

## 0.3.19 - 2026-10-11

- Measure Python package line coverage in the CI matrix and enforce a 75% minimum; expose coverage as an optional test-only extra.
- Refresh the README test badge to 28/28 and document the coverage command.

## 0.3.18 - 2026-10-11

- Run the regression and example preflight in CI on both supported Python versions, 3.11 and 3.12.


## 0.3.17 - 2026-10-11

- Refresh the GitHub Actions installation example to pin the current scanner release, v0.3.16.


## 0.3.16 - 2026-10-11

- Omit local parent directories from JSON and Markdown reports to avoid exposing usernames or machine-specific paths in shared CI artifacts.
- Keep the source basename so reports still identify the scanned archive or folder.

## 0.3.15 - 2026-10-11

- Validate scan configuration before computing source hashes, avoiding unnecessary full reads on invalid settings.
- Add regression coverage for early rejection of invalid scan policies.
- Bump package and CLI version to 0.3.15.

## 0.3.14 - 2026-10-11

- Cap configured text-file scanning at 16 MiB and reject booleans, floats, strings, and out-of-range limits to preserve bounded memory.
- Add regression tests for invalid limits and skipping larger text files.
- Bump package and CLI version to 0.3.14.

## 0.3.13 - 2026-10-11

- Escape untrusted paths and message text in Markdown reports so ZIP filenames cannot inject rows or markup.
- Add regression coverage for newlines, table pipes, Markdown links/images, and HTML-like filenames.
- Bump package and CLI version to 0.3.13.

## 0.3.12 - 2026-10-11

- Reject unsafe directory entries and Windows-nonportable ZIP path components (reserved device names, trailing dots/spaces).
- Add regression coverage for traversal and nonportable directory entries.
- Bump package and CLI version to 0.3.12.

## 0.3.11 - 2026-10-11

- Reject ZIP entry paths with colon syntax in any component to avoid drive/alternate-stream portability hazards.
- Add a regression fixture for colon syntax nested below the archive root.
- Bump package and CLI version to 0.3.11.

## 0.3.10 - 2026-10-11

- Refresh the README workflow example and project CI/release workflows to the current first-party GitHub Actions v7 majors.
- Bump package and CLI version to 0.3.10.

## 0.3.9 - 2026-10-11

- Reject non-regular special-file entries in ZIP archives instead of scanning them as ordinary files.
- Add a regression fixture proving FIFO entries are blocked without reading their payload.
- Bump package and CLI version to 0.3.9.

## 0.3.8 - 2026-10-11

- Detect case-only and Unicode-normalization path collisions in both folders and ZIPs.
- Add directory and archive regression fixtures for cross-filesystem portability findings.
- Bump package and CLI version to 0.3.8.

## 0.3.7 - 2026-10-11

- Validate `required_files` and `max_file_bytes` configuration instead of silently accepting malformed policies.
- Add regression tests for invalid and intentionally empty required-file lists.
- Bump package and CLI version to 0.3.7.

## 0.3.6 - 2026-10-11

- Add regression coverage for malformed required-path policy values and Windows-style glob separators.
- Bump package and CLI version to 0.3.6.

## 0.3.5 - 2026-10-11

- Refresh the README installation and CI pin to the current released scanner.
- Bump package and CLI version to 0.3.5.

## 0.3.4 - 2026-10-11

- Add a checked-in, generated example report demonstrating the Paradox required-path policy.
- Bump package and CLI version to 0.3.4.

## 0.3.3 - 2026-10-11

- Run the checked-in Paradox required-path policy against the clean example project in CI.
- Bump package and CLI version to 0.3.3.

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
