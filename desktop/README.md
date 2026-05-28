# NovaPlay desktop app

Packages the pygame player (`play.py`) into a standalone, double-click
application for macOS, Windows and Linux — no Python install required for
end users. All 142 games (117 generated + 25 reference) are bundled inside.

```
desktop/
├── launcher.py        — frozen-app entry point (sets cwd, then runs play.py)
├── NovaPlay.spec      — PyInstaller build recipe
├── requirements.txt   — runtime + packaging deps
└── README.md          — this file
```

## How it works

`play.py` finds games through **relative paths** (`prior-games/`,
`game_sources_3_lvls/`) and novacore loads each game by `exec()`-ing its
`<id>.py` source at runtime. So packaging needs two things:

1. Bundle each game's `<id>.py` + `metadata.json` as **data files** (not frozen
   modules). The screenshots, logs and run-archives are *not* shipped — the app
   stays ~58 MB.
2. `chdir` into the bundle's resource dir at startup so those relative lookups
   resolve. `launcher.py` does this via `sys._MEIPASS` when frozen.

`novaengine` and `novacore` *are* frozen into the binary, so the exec'd game
code can still `import novaengine`.

## Build locally

PyInstaller does **not** cross-compile — build on the OS you want to ship for.

```bash
# one-time env (matches play.py's .venv)
uv venv --python 3.12 .venv
uv pip install --python .venv -r desktop/requirements.txt

# build  (run from the repo root)
.venv/bin/pyinstaller desktop/NovaPlay.spec --noconfirm
```

Output:

| OS      | Result                | Ship                         |
|---------|-----------------------|------------------------------|
| macOS   | `dist/NovaPlay.app`   | zip the `.app`               |
| Windows | `dist/NovaPlay/`      | zip the folder (has `.exe`)  |
| Linux   | `dist/NovaPlay/`      | tar the folder               |

### Verify a build

`--selftest` is a headless check (no window): it scans the bundled corpus,
loads + resets one game, and exits non-zero on any failure.

```bash
# macOS
dist/NovaPlay.app/Contents/MacOS/NovaPlay --selftest
# Windows
dist\NovaPlay\NovaPlay.exe --selftest
# Linux
dist/NovaPlay/NovaPlay --selftest
```

## Build for all platforms (CI)

`.github/workflows/desktop-build.yml` builds + selftests all three on matching
GitHub runners. Trigger it from the Actions tab (workflow_dispatch), or push a
version tag to also publish the bundles to a GitHub Release:

```bash
git tag v0.1.0 && git push origin v0.1.0
```

## Distribution caveats (signing)

The bundles run locally as-is, but OS gatekeepers warn on *downloaded*
unsigned apps:

- **macOS** — Gatekeeper blocks unsigned/un-notarized `.app`s. For public
  distribution you need an Apple Developer ID cert + `codesign` +
  `notarytool`. Without it, users must right-click → Open the first time.
- **Windows** — SmartScreen warns until the `.exe` is signed with an
  Authenticode cert (or builds enough reputation).
- **Linux** — no signing gate; ship the tarball (or wrap as AppImage later).

These need your developer accounts/certs, so they're left as follow-ups; the
CI workflow has the build + release plumbing ready to slot signing steps into.
