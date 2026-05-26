# NovaPlay

Game-generation harness for novel NovaPlay environments, plus the
generated game corpus. Drives Claude Code through generating ONE
novel game per run; output is a Python source file conformant with
the NovaPlay design rules (core-knowledge priors only; novel vs. the
prior-games corpus; multiple mechanics per environment; tutorial
level first; difficulty by composition; turn-based; opaque 4-char
ID — with EXACTLY 3 levels per game).

The engine (`novaengine`) and loader (`novacore`) are vendored at the
repo root, so the harness, the desktop player (`play.py`), and the
web player (`web/`) all run self-contained.

## Layout

```
explore-games/
├── README.md             — this file
├── task-overview.md      — workflow framing, paths, retry budget
├── states/               — 5 FSM nodes
├── skills/               — reusable instruction modules
│   ├── global/
│   ├── design-constraints/
│   ├── mechanic-novelty/
│   ├── mechanism-details/   ← per-game deep dives (25 files)
│   ├── code/
│   └── finalize/
├── ideas/                — mechanic seeds and brainstorm notes
├── runs/                 — per-run logs (history)
├── workspace/            — per-run scratch (state logs, deliverables)
├── novaengine/            — vendored game engine (the games import this)
├── novacore/              — vendored loader/wrapper (Arcade, used by play.py)
├── play.py               — interactive pygame player for any game
├── game_sources_3_lvls/  — 25 reference-game sources (3-level truncated)
├── deep-analysis-3lvls/  — per reference game: deep analysis + screenshots
└── prior-games/          — long-lived corpus (116 generated games)
    ├── index.md          — cumulative table
    └── <game_id>/
        ├── <game_id>.py
        ├── metadata.json
        ├── mechanism-detail.md
        └── run-archive/  — oracle recordings + smoke-test data
```

The `novaengine/`, `novacore/`, `game_sources_3_lvls/`, and
`deep-analysis-3lvls/` trees are the engine + reference corpus the
pipeline reads and the generated games run against. They are vendored
into the repo so the harness is self-contained. `novaengine` is pure
Python and needs only `numpy` and `pydantic` at runtime.

## Running

The harness is invoked inside Claude Code. There is no Python
driver; Claude Code IS the host.

> *"Read the task overview at `task-overview.md`, then run the
> harness. Optional one-line seed: `<your seed>` (or `(autonomous)`
> for no seed)."*

### Run inputs

| Input | Required? | Notes |
|---|---|---|
| Seed (one-line natural language hint) | Optional | Empty = autonomous mode (agent picks the mechanic family). |
| Prior-games corpus | Implicit | Read from `prior-games/index.md` automatically. |

### Outputs

After a run:

- `workspace/final-report.md` — terminal deliverable.
- `prior-games/<game_id>/<game_id>.py` — the generated game.
- `prior-games/<game_id>/metadata.json` — game metadata.
- One new row in `prior-games/index.md`.

## Running a generated game (manual smoke test)

Generated games depend on the `novaengine` package, which is vendored
at the repo root. Run from the repo root (so the cwd, and thus
`novaengine`, is on `sys.path`); only `numpy` and `pydantic` need to
be available in the Python environment:

```bash
python -c "
import sys
sys.path.insert(0, 'prior-games/<game_id>')
from <game_id> import <PascalClass>
from novaengine import ActionInput, GameAction
g = <PascalClass>()
g.perform_action(ActionInput(id=GameAction.RESET, data={}))   # init level 1
print('levels:', len(g._levels), 'actions:', list(g._available_actions))
"
```

`<PascalClass>` is the Pascal-case capitalisation of the ID
(e.g. `qz38` → `Qz38`). Driving a game programmatically is done via
`g.perform_action(ActionInput(id=GameAction.ACTION<N>, data=...))`;
ACTION6 carries click coords in `data={"x": ..., "y": ...}`.

## Playing a game interactively (pygame)

`play.py` opens a **game browser**: a window listing every generated
and reference game. Pick one with the keyboard, play it, press `Esc`
to return to the browser and choose another — no need to re-run with a
different id. It needs `pygame` (a binary dependency, so it is NOT
vendored — install it into a local virtualenv). One-time setup (the
`.venv/` is gitignored):

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv pygame numpy pydantic requests python-dotenv
```

Then, from the repo root (so the sibling `novaengine/` and `novacore/`
packages are importable):

```bash
.venv/bin/python play.py                 # open the browser
.venv/bin/python play.py --game gv47      # jump straight into one game
.venv/bin/python play.py --list           # print the catalog, no window
.venv/bin/python play.py --scale 14       # bigger window
```

**Browser controls:** `↑`/`↓` select, `PageUp`/`PageDn` + `Home`/`End`
to move faster, **type to filter** (matches id or title), `Enter` to
play, mouse wheel/click also work, `Esc` clears the filter or quits.

**In-game controls:** arrows → ACTION1-4, Space → ACTION5, Z → ACTION7,
mouse click → ACTION6, `R` reset level, `Shift+R` full reset, `1/2/3`
jump to a level, **`Esc` back to the browser**, `Q` quit. Games under
`--env-dir` (default `prior-games`) and `--ref-dir` (default
`game_sources_3_lvls`) are both listed. `--record` writes an MP4 per
played game (needs `uv pip install --python .venv "imageio[ffmpeg]"`).

## Playing in the browser (pixel-art web player)

`web/` is a self-contained web player with a retro pixel-art UI. The
game logic still runs in Python (`novaengine`) on a tiny stdlib HTTP
backend — the browser only renders the 64×64 frames on a canvas and
sends keyboard/click actions. No web framework, no build step. Uses
the same `.venv` as `play.py` (no `pygame` needed for the web one):

```bash
.venv/bin/python web/server.py        # then open http://localhost:8000/
.venv/bin/python web/server.py --port 8080
```

Left pane is a filterable game browser (all 117 generated + 25
reference games); click a game to load it. Controls: on-screen D-pad
+ buttons, or keyboard (arrows → ACTION1-4, Space → ACTION5, Z →
ACTION7, **click the screen** → ACTION6, `R`/`Shift+R` reset, `1/2/3`
jump level, `Esc` back to the list).

```
web/
├── server.py          — stdlib HTTP backend (catalog + game sessions)
└── static/
    ├── index.html     — layout
    ├── style.css      — pixel-art theme (CRT scanlines, 16-colour palette)
    └── app.js         — canvas renderer + input + API calls
```

## Novelty: floor vs ceiling

The harness's autonomous novelty check is a FLOOR, not a ceiling:

- **The floor**: every generated mechanic is checked against the 25
  NovaPlay reference games (in `skills/mechanic-novelty/
  taxonomy-of-25-games.md` and the deeper `skills/mechanism-details/
  *.md` files) AND against every prior generated game (in
  `prior-games/index.md` plus each `prior-games/<id>/
  mechanism-detail.md`). The harness rejects mechanic-family
  overlaps without a concrete distinguishing rule.
- **The ceiling**: §3.4 of the NovaPlay Technical Report also
  requires novelty vs. preexisting commercial video games. The
  harness CANNOT automate that — it requires a complete catalogue
  of every puzzle/arcade game ever made. The user is the only one
  who can apply this check.

**When you receive a generated game**, sanity-check it against
commercial games you know. If the mechanic is essentially
"Sokoban", "Bejeweled", "Magnet Boy" etc., reject it manually and
re-run the harness with a one-line seed steering away from that
family.
