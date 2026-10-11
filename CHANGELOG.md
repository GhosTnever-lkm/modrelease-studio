# Changelog

## 0.3.57 - 2026-10-11

- Fail closed when junction metadata cannot be read: prune the directory and report a path-specific `READ_METADATA` warning.
- Add a regression proving inaccessible directory metadata cannot lead to traversal or indexing.
- Refresh the test badge and pin the README install example to v0.3.57.

## 0.3.56 - 2026-10-11

- Do not traverse Windows directory junctions during folder scans; report them as advisory findings and reject junction components during safe reads.
- Add a deterministic junction-pruning regression and a Windows-only regression using an external directory junction.
- Refresh the suite count and pin the README example to v0.3.56.

## 0.3.55 - 2026-10-11

- Make the directory-walker permission-error regression derive its fixture path from the resolved scan root on every OS.


## 0.3.54 - 2026-10-11

- Add regression coverage for path-specific `SCAN_DIRECTORY` errors reported by the bounded directory walker.
- Refresh test metrics; keep the behavioral install example pinned to scanner runtime v0.3.53.


## 0.3.53 - 2026-10-11

- Scan secret-bearing files in ignored/generated path names when they are inside a ZIP release artifact; directory scans still prune those folders from working trees.
- Add regression coverage for `.git` and `node_modules` archive contents.


## 0.3.52 - 2026-10-11

- Prune generated/dependency directories before indexing so their files cannot consume the scan entry limit or affect the build fingerprint.
- Add a deterministic regression reproducing an ignored `.git` directory triggering `ENTRY_LIMIT` ahead of the actual mod file.


## 0.3.51 - 2026-10-11

- Add an end-to-end ZIP regression for OS-junk warnings in JSON and safely escaped Markdown output.
- Keep scanner behavior unchanged; refresh suite count and install example.


## 0.3.50 - 2026-10-11

- Exclude generated and dependency directories from content security checks.
- Report Windows/macOS filesystem junk as advisory findings.
- Add traversal-policy regression tests and refresh the test-count badge.


## 0.3.49 - 2026-10-11

- Add an end-to-end CLI regression verifying file-growth warnings in JSON, Markdown, REVIEW status, and the non-blocking exit code.

## 0.3.48 - 2026-10-11

- Remove an obsolete project-state document from the public product repository.

## 0.3.47 - 2026-10-11

- Update the documented external GitHub Actions install pin to behavioral release v0.3.46.

## 0.3.46 - 2026-10-11

- Report a `LARGE_TEXT_FILE` warning when an indexed text file grows past the configured read limit during scanning, instead of silently skipping content checks.
- Add a deterministic regression for the changed-file-size boundary.

## 0.3.45 - 2026-10-11

- Refresh the external GitHub Actions install example to scanner v0.3.44.


## 0.3.44 - 2026-10-11

- Render Unicode LINE SEPARATOR and PARAGRAPH SEPARATOR characters as visible escapes in terminal compare output, preventing hidden line breaks in hostile filenames or findings.
- Extend the existing compare regression to cover U+2028 and U+2029.

## 0.3.43 - 2026-10-11

- Render invisible Unicode controls visibly in Markdown findings, and use valid JSON escapes in JSON reports while preserving the original parsed values.
- Apply the same safe JSON serialization to CLI stdout and saved JSON files.
- Add a regression for bidi, C1, ANSI, and newline controls in untrusted target/path/message fields; 60 tests.

## 0.3.42 - 2026-10-11

- Escape control, bidi-format, surrogate, and other Unicode control-category characters in compare output so untrusted filenames cannot inject terminal control sequences or extra lines.
- Add a regression for newline, ANSI escape, and bidi control characters; update the README test badge and coverage/test-count summary.

## 0.3.41 - 2026-10-11

- Make Linux/macOS checksum commands work with any downloaded release version; PowerShell detects the matching sidecar and fails safely if more than one is present.
- Update the OS-specific CI fixtures to exercise the version-independent file selection; no scanner runtime behavior changed.

## 0.3.40 - 2026-10-11

- Exclude test-generated Python bytecode from release ZIPs and fail the release job if any `__pycache__` or `.pyc`/`.pyo` files remain.
- No runtime behavior changed; the suite remains 58 tests.

## 0.3.39 - 2026-10-11

- Exercise the documented SHA-256 sidecar verification in CI on Linux (`sha256sum`), macOS (`shasum`), and Windows PowerShell (`Get-FileHash`).
- Keep the release workflow checksum gate and 58-test badge.

## 0.3.38 - 2026-10-11

- Verify the generated release ZIP `.sha256` sidecar with `sha256sum --check` before running the install smoke test and publishing assets.
- No runtime behavior changed; suite remains 58 tests.

## 0.3.37 - 2026-10-11

- Document SHA-256 sidecar verification for downloaded release ZIPs on Linux, macOS, and Windows PowerShell.
- Clarify that the co-published checksum detects corruption but is not a separate signature or provenance attestation.

## 0.3.36 - 2026-10-11

- Add a regression that discovers the unittest suite and asserts the README test badge matches its size, preventing stale test metrics.
- Update the badge to 58/58; runtime behavior is unchanged.

## 0.3.35 - 2026-10-11

- Make the release workflow extract the built ZIP, install it into an isolated virtual environment, check its CLI version against the tag, and scan the clean included sample before publishing.
- Keep the README test badge at 57/57; no runtime scanner behavior changed.

## 0.3.34 - 2026-10-11

- Correct the README test badge to 57/57 after the v0.3.33 ZIP expanded-size regression.
- No runtime behavior changed.

## 0.3.33 - 2026-10-11

- Add an end-to-end CLI regression proving ZIP archives over the unpacked-size limit produce `ARCHIVE_SIZE_LIMIT` in JSON and exit with blocking status 1.
- Increase the suite to 57 tests; package line coverage remains 91%, above the enforced 80% CI floor.

## 0.3.32 - 2026-10-11

- Document the 30,000-entry, 4 GiB aggregate ZIP, 2,000,000-byte default text-file, 16 MiB configurable, and 2 MiB Paradox parser bounds and explain incomplete scans.
- Clarify that `READY` is not a safety certification; update the README test badge to 56/56.

## 0.3.31 - 2026-10-11

- Add an end-to-end CLI regression proving `ENTRY_LIMIT` appears in JSON reports and blocks release scans for both folder and ZIP inputs.
- Increase the suite to 56 tests; package line coverage remains 91%, above the enforced 80% CI floor.

## 0.3.30 - 2026-10-11

- Add a bounded DirectorySource entry-count test for exact-limit acceptance and overflow truncation, complementing the ZIP boundary coverage.
- Increase the suite to 55 tests; package line coverage remains 91%, above the enforced 80% CI floor.

## 0.3.29 - 2026-10-11

- Add bounded ZIP entry-count and total-uncompressed-size boundary regressions using small synthetic fixtures.
- Increase the suite to 54 tests; package line coverage is 91%, above the enforced 80% CI floor.


## 0.3.28 - 2026-10-11

- Catch zlib decompression errors while reading ZIP entries and surface corrupt text files as unreadable findings instead of crashing the scan.
- Add a synthetic corrupt-DEFLATE regression; the suite now has 52 tests and 90% package line coverage.


## 0.3.27 - 2026-10-11

- Add a temporal symlink-swap regression: after a file enters the scan index, replacing it with an outside symlink must not expose target contents through reads or directory digests.
- Raise the suite to 51 tests and package line coverage to 90% (80% CI floor).


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
