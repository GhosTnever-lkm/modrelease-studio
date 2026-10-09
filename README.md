# ModRelease Studio

**Release preflight for game mods and mod packs.** Scan a folder or ZIP, catch common packaging and metadata problems, and publish a readable report before players download the build.

Current unreleased changes are tracked in [CHANGELOG.md](CHANGELOG.md).

ModRelease Studio is local-first: your mod files stay on your machine unless you choose to upload the generated report. It uses only the Python standard library.

## What it checks

- Folder and ZIP contents, unsafe archive paths, duplicate paths, and case-only collisions.
- Accidental secrets in common text/config files (private keys, AWS access-key IDs, GitHub and Slack tokens, Discord webhooks, and likely hard-coded API keys).
- Paradox Clausewitz `descriptor.mod` metadata and localization YAML issues.
- Missing release notes, OS-specific junk, and unexpectedly large files.
- Stable SHA-256 fingerprint of the build, JSON/Markdown reports, and finding changes between two builds.

## Quick start

Requires Python 3.11 or newer. From a checkout:

```console
modrelease --version
python -m modrelease_studio scan ./my-mod --md-out release-report.md --json-out release-report.json
```

Or install it in an isolated environment:

```console
python -m pip install .
modrelease scan ./my-mod.zip --md-out release-report.md
```

The command exits with `0` when there are no critical/error findings, `1` when release-blocking findings exist, and `2` for an invalid input or configuration. Warnings are advisory by default.

## Compare builds

```console
modrelease compare ./previous-build ./candidate-build
```

## Configure checks

Copy `modrelease.example.toml` to `modrelease.toml` in your mod root:

```toml
[scan]
required_files = ["README.md", "CHANGELOG.md", "LICENSE"]
max_file_bytes = 2000000
```

`required_files` checks basenames anywhere in the package. Secret scanning is a best-effort detector; review findings and do not treat a clean scan as proof that a release contains no secret.

## GitHub Actions

Add a workflow to your mod repository:

```yaml
name: Mod release preflight
on:
  pull_request:
  push:
    branches: [main]
jobs:
  preflight:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Scan mod
        run: |
          python -m pip install "modrelease-studio @ git+https://github.com/GhosTnever-lkm/modrelease-studio.git@v0.2.3"
          modrelease scan . --md-out modrelease-report.md --json-out modrelease-report.json
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: modrelease-report
          path: |
            modrelease-report.md
            modrelease-report.json
```

The included `.github/workflows/preflight.yml` installs this repository's local project with `python -m pip install .` and runs the tool against the included clean example mod. In a mod repository, use the pinned tagged source shown above; `pip install .` would try to install the mod repository itself. The example is pinned to `v0.2.3`.

## Current scope

This is an early, intentionally conservative release checker. It does not fully parse every game scripting language, verify that a mod launches in-game, or replace platform-specific validators. Paradox support currently focuses on descriptor metadata and localization files. Add a rule or open an issue if you want another game's packaging checks.

## Development

```console
python -m modrelease_studio --help
python -m unittest discover -s tests -v
```

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [CHANGELOG.md](CHANGELOG.md).

## ☕ Support / Pro Version

ModRelease Studio is free and open source. There is no paid Pro edition yet. If the tool is useful, you can support its development on [Buy Me a Coffee](https://buymeacoffee.com/azizazimov8), [Boosty](https://boosty.to/azizazimov), or [GitHub Sponsors](https://github.com/sponsors/GhosTnever-lkm).

You can also send a supported asset to one of these public receive addresses:

| Network | Asset standard | Address |
|---|---|---|
| Bitcoin | BTC | `bc1qn75pj4n7gyl2k5kf2f97elvyenz52q6nn2g30u` |
| Tron | TRC-20 | `TCBSy38X57hA6w2onJcxom24x1febc1mP1` |
| BNB Smart Chain | BEP-20 | `0xD431a917961E0b086B96D9F72b5C8fF19b19068a` |

**Send funds only on the matching network.** Do not send a different network's asset to these addresses.

## License

MIT. See [LICENSE](LICENSE).
