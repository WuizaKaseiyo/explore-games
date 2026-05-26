# Repo paths

All paths are relative to the host agent's repo root unless
explicitly absolute.

| Purpose | Path |
|---|---|
| This harness | `` |
| Cumulative prior-games corpus | `prior-games/` |
| Prior-games index | `prior-games/index.md` |
| Per-run scratch (state logs, deliverables) | `runs/<run_id>/workspace/` (the `<WORKSPACE>` set up by the run-harness skill) |
| Static reference corpus (25 official games, truncated to first 3 levels) | `game_sources_3_lvls/` |
| Per-game deep analyses + initial-frame screenshots (25 reference games) | `deep-analysis-3lvls/<id>/` |
| novaengine package (vendored; API reference AND runtime import target) | `novaengine/` |
| novacore loader/wrapper (vendored; used by the interactive player) | `novacore/` |
| Interactive pygame player (manual play / recording) | `play.py` |
| Reusable instruction modules | `skills/` |

The `novaengine/` package is vendored at the repo root. While
authoring a spec the agent uses it only as an API reference; the
generated game source files `import novaengine`, and the
`implement` / `smoke_test` states import the package at runtime to
instantiate and drive the generated game. Because it lives at the
repo root, `import novaengine` resolves whenever the host runs Python
from the repo root (the cwd is on `sys.path`).
