# Post-implement smoke-test checks (Tier 1)

A deterministic, cheap battery of programmatic checks that runs after
`implement` and before `finalize`. Each check renders the game in
memory and compares the result to a numeric threshold or a static
expectation; no LLM judgement, no random-play, no human review.

Goal: catch the high-frequency, low-effort bugs (camera misalignment,
HUD overlap, action-slot stubs, palette leaks) that survive the
implement state's basic syntax + instantiate test but produce a game
nobody can actually play.

## Inputs

- The generated source: `prior-games/<id>/<id>.py`.
- The Pascal class name (for instantiation): derived as `<id>[0].upper() + <id>[1:]`.
- The spec's `available_actions=[...]` list.

## Setup snippet (the agent runs this once before the checks)

```python
import importlib.util, sys
from pathlib import Path
import numpy as np

# novaengine is vendored at the repo root; ensure it resolves whether
# this runs via `python -c` (cwd already on sys.path) or as a saved
# script file (script dir on sys.path instead of cwd). Run from root.
sys.path.insert(0, str(Path.cwd()))

src = Path("prior-games/<id>/<id>.py")
spec = importlib.util.spec_from_file_location("smoke_<id>", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = getattr(mod, "<Pascal>")
g = GameClass()
LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)
N_LEVELS = len(g._levels)
```

## The checks

For each check, record one row in `workspace/smoke-test-failures.md`
on failure. Each row contains: check ID, level index (or "all"),
observed value, threshold, and a one-line diagnosis. If every check
passes, write `workspace/smoke-test-pass.md` instead.

### CHECK_CAMERA_VIEWPORT — camera/grid alignment per level

For each level, after calling `g.set_level(level_idx)` (which fires
`on_set_level`), confirm the camera viewport matches the level's
`grid_size`:

```python
g.set_level(level_idx)
gw, gh = g.current_level.grid_size or (64, 64)
cam_w, cam_h = g.camera._width, g.camera._height
match = (cam_w == gw and cam_h == gh)
```

**Threshold**: `match` is True for every level.

**Failure diagnosis**:
"Camera viewport mismatch on level <N> — `level.grid_size` is
(<gw>, <gh>) but `camera._width, camera._height` are
(<cam_w>, <cam_h>). The grid will render at scale=1 in a small patch
of the frame; the rest is letter-box. Fix in `on_set_level`:

    gw, gh = level.grid_size or (64, 64)
    self.camera.width = gw
    self.camera.height = gh

See `code/universal-scaffold.md` § Camera viewport must match level
grid_size. Exempt: a scrolling-viewport game (camera smaller than
grid by design) — but this is rare and must be explicit in the spec."

(This check would have caught the kf42 v1 bug — camera was (64, 64)
while level grid_size was (12, 12), (14, 14), (16, 16).)

A complementary fill-ratio sanity probe is OPTIONAL and only
informative when `BACKGROUND_COLOR != PADDING_COLOR`:

```python
non_letterbox = int(np.count_nonzero(frame != LETTER_BOX))
fill_ratio = non_letterbox / (64 * 64)
```

If `BACKGROUND_COLOR == PADDING_COLOR` the fill-ratio metric is
unreliable (background pixels are indistinguishable from letter-box
pixels) — record the value but do not fail on it.

### CHECK_SPRITE_CONTENT — non-empty playfield

For each level:

```python
distinct_non_letterbox = set(np.unique(frame[frame != LETTER_BOX]).tolist())
```

**Threshold**: `len(distinct_non_letterbox) >= 2` (background + at
least one sprite-content palette value).

**Failure**: "Level <N> rendered frame contains only one palette
value (letter-box plus <X>); no game content visible. Likely cause:
sprites placed off-screen or all sprites have `visible=False`."

### CHECK_ACTION_BRANCHES — every declared action has a step() branch

Parse the source text (string-level; `ast` not strictly needed):

```python
src_text = src.read_text()
declared = list(g._available_actions)  # list[int] from __init__
for action_id in declared:
    needle = f"GameAction.ACTION{action_id}"
    if needle not in src_text:
        FAIL("ACTION<N>")
```

**Failure**: "ACTION<N> is in `available_actions=[...]` but the source
never references `GameAction.ACTION<N>` — the action is a no-op.
Either remove it from `available_actions` or add a branch in
`step()`."

### CHECK_ACTION_RUNTIME — each action runs without exception

For each action in `available_actions`:

```python
g_fresh = GameClass()
prev_count = g_fresh._action_count
try:
    if action_id == 6:
        g_fresh.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True)
    else:
        g_fresh.perform_action(ActionInput(id=GameAction.from_id(action_id)), raw=True)
except Exception as e:
    FAIL("ACTION<N>", error=repr(e))
```

**Threshold**: no exception raised.

**Failure**: "ACTION<N> raised <ExceptionType>: <message>". The fix
state should look at the action handler in `step()`.

(Optional secondary check: confirm `_action_count` increased after
each action — catches `step()` paths that forget `complete_action()`.)

### CHECK_PALETTE_RANGE — all rendered pixels are in [0, 15]

For each level:

```python
mn, mx = int(frame.min()), int(frame.max())
```

**Threshold**: `mn >= 0 and mx <= 15`.

**Failure**: "Frame contains palette value <X> outside the legal
[0, 15] range. Likely cause: a sprite's `pixels=[[...]]` contains
`-1` (transparent) but the camera is leaking it; or a `color_remap`
target was a sentinel like -2."

### CHECK_WIN_PATH_EXISTS — the game can in principle be won

Static check on the source:

```python
has_next_level = "self.next_level()" in src_text
has_win = "self.win()" in src_text
```

**Threshold**: `has_next_level or has_win` is True.

**Failure**: "No `self.next_level()` and no `self.win()` call found
in the source. The game is structurally unwinnable — the spec's win
predicate is not wired through to the engine. Locate the win-check
helper and add the engine call."

### CHECK_WITNESS_WINS — every level's named witness actually wins

Replays each level's witness sequence (from `mechanic-spec.md`'s
*"Witness solution"* lines) against the loaded game and asserts
the level advances. This catches the gap that `CHECK_WIN_PATH_EXISTS`
misses: the source contains `self.next_level()` and `self.win()`
calls, but the spec's named witness doesn't actually trigger them
(e.g. an off-by-one in the win predicate, a wrong action mapping,
a misplaced sprite that breaks the witness path).

The agent must extract the three witnesses from the spec and
translate each into a list of `ActionInput` objects. ACTION1-5 and
ACTION7 take no `data`; ACTION6 carries `data={"x": <px>, "y": <py>}`
with the click's display-pixel coordinates from the spec's
`ACTION6@(<x>, <y>)` notation.

```python
from novaengine import ActionInput, GameAction

# Translate the three spec witnesses into ActionInput lists.
# Replace the placeholder lists below with the actual sequences
# parsed from the spec's "Witness solution" lines.
A = GameAction
def click(x, y):
    return ActionInput(id=A.ACTION6, data={"x": x, "y": y})
def act(n):
    return ActionInput(id=A(n), data={})

WITNESSES = {
    1: [act(4), act(4), act(5)],                        # ← from spec L1
    2: [act(3), act(3), act(5), act(4), act(4), act(5)],# ← from spec L2
    3: [click(48, 26), act(4), act(5)],                 # ← from spec L3
}

# Reset to L1, then replay each witness in sequence. After Lk's
# witness, the game must have advanced past Lk: for k < N_LEVELS,
# `g._score == k` (next_level fired); for k == N_LEVELS, the
# state must be WIN.
g.handle_reset()
failures = []
for level_idx in range(1, N_LEVELS + 1):
    score_before = g._score
    if score_before != level_idx - 1:
        failures.append(
            f"L{level_idx}: expected to be at level {level_idx} "
            f"(score == {level_idx - 1}) before witness replay, "
            f"got score == {score_before}"
        )
        break
    for ai in WITNESSES[level_idx]:
        g.perform_action(ai)
    if level_idx < N_LEVELS:
        if g._score != level_idx:
            failures.append(
                f"L{level_idx}: witness did not advance the level "
                f"(score went {score_before} → {g._score}, expected "
                f"{level_idx}); state == {g._state.name}"
            )
            break
    else:
        if g._state.name != "WIN":
            failures.append(
                f"L{level_idx}: witness did not reach WIN state "
                f"(state == {g._state.name}, score == {g._score})"
            )
            break
```

**Threshold**: `failures == []`.

**Failure**: "The named witness for level <k> does not actually win.
Either the spec's witness is wrong (re-derive it by hand and revise
the spec) or the implementation has a bug that makes the witness
fail (the more common case). Trace the witness step-by-step in the
implementation: at each action, log `g._action.id`, `g.theta` /
`g.active_orb` / etc. for this game, and the relevant sprite
positions to find where the divergence first appears. Common
implementation bugs that fail this check: wrong action-id mapping,
off-by-one in the win predicate, a sprite placed one cell off,
ACTION6 click coords not matching the cell the spec assumed, a
multi-frame animation that consumes more action_count than the
spec budgeted."

### CHECK_LOSE_PATH_EXISTS — the energy bar can fire a lose

Static check:

```python
has_lose = "self.lose()" in src_text
```

**Threshold**: `has_lose` is True.

**Failure**: "No `self.lose()` call found in the source. The energy
bar is decorative — players can never lose. Wire the step counter
expiry into a `self.lose()` call in `step()`."

### CHECK_CAMERA_DEFAULT — camera.width and camera.height set per-level

Read the source for an `on_set_level` body that mutates
`self.camera.width` and `self.camera.height`:

```python
needs_per_level_camera = any(
    g._levels[i].grid_size != g._levels[0].grid_size
    for i in range(1, N_LEVELS)
)
if needs_per_level_camera:
    has_resize = ("self.camera.width" in src_text and
                  "self.camera.height" in src_text)
```

**Threshold**: if levels have different `grid_size` values, the
source must mutate `self.camera.width`/`height` (likely in
`on_set_level`).

**Failure**: "Levels have different `grid_size` values
(<list>) but the source does not resize `self.camera.width` /
`self.camera.height` per-level. The smaller levels will render
mis-scaled. See `code/universal-scaffold.md` § Camera viewport must
match level grid_size."

### CHECK_VISUAL_SANITY — rendered initial frames match the spec

This is the only check that uses vision. For each level, render the
**initial frame** (state immediately after `set_level(idx)`, before
any action) to a PNG, then ask the agent to compare each rendered
frame against the spec's per-level description.

#### Step A — render the three frames

```python
import numpy as np
from pathlib import Path
from PIL import Image

PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)

out_dir = Path("<WORKSPACE>/smoke-frames")  # substitute <WORKSPACE> with the run's workspace path, e.g. runs/<run_id>/workspace/
out_dir.mkdir(parents=True, exist_ok=True)
for L in range(min(3, N_LEVELS)):
    g.set_level(L)
    frame = g.camera.render(g.current_level.get_sprites())
    rgb = PALETTE[frame.clip(0, 15)]                # H,W,3
    img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
    img.save(out_dir / f"level_{L+1}.png")
```

#### Step B — agent inspection (vision pass)

For each level, the agent opens the PNG (use the standard image-
read pathway available in your tool environment) **alongside** the
matching spec sections:

- The spec's `## 2. Mechanic family` paragraph (one source of truth
  for what *should* be moving and how).
- The spec's `## 4. Level progression …` entry for that level
  (sprite roster + per-cell layout + initial-state description).

The agent then asks itself the following four questions per level
and answers PASS / FAIL with a one-line diagnosis:

1. **Sprite count.** Does the rendered frame show roughly the
   number of distinct game-element clusters the spec describes?
   (e.g. spec says "1 player + 2 targets + 5 walls" → image
   should show ~8 distinct shapes, not 2 and not 50).
2. **Sprite placement.** Are the conspicuous sprites (player
   avatar, goal, hazards) in roughly the spec-described regions
   of the frame? (e.g. spec says "player at top-left, goal at
   bottom-right" → image should not show both at the same
   corner). Be coarse — quadrant-level agreement is enough.
3. **HUD presence.** If the spec says there is a step-counter
   bar or other HUD widget, is it visible somewhere on the
   frame? (Top row, bottom row, or single-column edge.)
4. **No catastrophic rendering bug.** Is the playfield filling
   the frame as expected (no tiny patch in the corner; no big
   solid-colour blocks where game content should be; no obvious
   sprite overlaps that look like one big blob)?

#### Important constraints on the visual judgement

- **Do NOT fail on cosmetic differences.** Palette choice within
  the legal 16-colour set, exact sprite shape style, exact pixel
  count of decorative elements — none of these are failure
  conditions. We are checking that the spec's described scene IS
  what got rendered, not that it's beautiful.
- **Do NOT fail on details the spec doesn't explicitly describe.**
  If the spec says "a wall surrounds the playfield" without
  specifying every cell, the rendered wall just needs to look
  like a wall around the playfield.
- **DO fail on**:
  - Sprite missing entirely (spec says "3 pawns", image shows 1).
  - Sprite in completely the wrong region (spec says "goal at
    top", image shows it at bottom).
  - HUD missing when the spec says the energy bar is required.
  - Catastrophic rendering bugs (the kf42 v1 corner-patch class —
    even if `CHECK_CAMERA_VIEWPORT` somehow passes, the visual
    pass should catch any analogous symptom).
  - Sprite shape that resembles a digit or letter (the
    forbidden-elements rule). This is one place where vision
    helps catch a constraint that static analysis misses.

#### Output format

The visual pass produces, per level, exactly one of:

- `PASS — <optional 1-line note, can be empty>`
- `FAIL — <one-line diagnosis quoting the spec claim that's
  contradicted by the rendered frame>`

Aggregate **threshold**: all 3 levels must produce `PASS`.

#### Failure entry for `smoke-test-failures.md`

```markdown
## CHECK_VISUAL_SANITY (level <N>)
- observed: <agent's one-line diagnosis> — see
  `workspace/smoke-frames/level_<N>.png`
- threshold: rendered frame matches spec § Levels — level <N>
- diagnosis: <agent's quoted spec claim vs. quoted observation>
- fix-direction: <usually a sprite-placement edit in
  `_levelN_sprites()` or the relevant Level constructor; or, if
  the rendering itself looks wrong, a camera-viewport / HUD /
  pixel-pattern fix>
```

#### Why this check is light-weight

- One LLM call per smoke-test invocation (3 PNGs bundled).
- Three coarse questions per level → low judgement variance.
- Anchored on the spec, not on free-form aesthetic opinion.
- Does NOT replace any of the other 8 checks; it adds a vision
  pass that those checks structurally cannot do.

(The much heavier Tier-3 alternative — full LLM-as-judge inspection
of mid-game frames during random play — is intentionally NOT in
this skill. Add it later if visual-sanity-only catches start
slipping bugs through.)

## Custom checks (agent-authored, 2-4 per run)

The eight universal checks above catch the structural/runtime bugs
common to any game. After running them, the agent MUST author **2-4
custom checks** that exercise the specific mechanic of the game
being generated. The goal is to catch mechanic-design bugs (the
correct action does not produce the expected effect) that the
universal checks cannot see.

Each custom check follows a strict template — this is what keeps
them easy to write and easy to debug:

```python
def check_<short_name>(GameClass) -> tuple[bool, str]:
    """One-line description of the invariant being asserted."""
    g = GameClass()
    g.set_level(0)        # or 1 or 2; pick the simplest level that exhibits the invariant
    # --- setup: navigate to a known starting state via at most 5 actions ---
    # --- action: perform ONE action under test ---
    # --- assertion: one boolean expression ---
    observed = "<short string of what we saw>"
    passed = <single boolean expression>
    return passed, observed
```

### Hard constraints (enforced by self-review before running)

A custom check **MUST**:

1. **Run in ≤ 1 second wall-clock time.** No `time.sleep`, no
   timing-sensitive checks, no random retries.
2. **Be fully deterministic.** No randomness, no I/O beyond the
   game instance, no environment variables.
3. **Use ≤ 5 setup actions** between `set_level` and the action
   under test. Any check that needs more than 5 setup actions is
   testing too much at once — split it or drop it.
4. **Test ONE action's effect.** The "action under test" is a single
   `env.step(...)` or `g.perform_action(...)` call.
5. **Assert ONE boolean.** No AND-chains of 3+ predicates in the
   final assertion. (`x.position == (3, 4)` is one predicate;
   `x.position == (3, 4) and x.colour == 8` is two — split them
   into two checks.)
6. **Test an essential mechanic invariant**, not a cosmetic
   property. "After UP, the active pawn's `y` decreases by 1" is
   essential. "After UP, the HUD bar drops by 3 pixels" is
   cosmetic — skip it.

### Common patterns the agent can adapt

Pick from the templates below; do not invent baroque ones.

**Pattern A — Direction press moves the avatar one cell.**
```python
def check_up_moves_pawn():
    g = GameClass()
    g.set_level(0)
    pawn = g.pawns[0]                # adapt: the avatar/active sprite
    y0 = pawn.y
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    return pawn.y == y0 - 1, f"y0={y0} y1={pawn.y}"
```

**Pattern B — Click selects a sprite at the clicked cell.**
ACTION6's `data["x"]`/`["y"]` are interpreted as **display pixels in
the 64×64 frame**, not grid coords. The game converts them via
`self.camera.display_to_grid(x, y)`. So the check must convert from
grid → display px before sending the click. With the camera
viewport set to `grid_size` (per the universal scaffold rule), the
conversion is:
```python
def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2

def check_click_selects():
    g = GameClass()
    g.set_level(0)
    target = g.pawns[1]              # any non-default-active sprite
    fx, fy = _grid_to_display_px(g.current_level.grid_size, target.x, target.y)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    return g.active_pawn is target, f"active is {g.active_pawn}"
```

**Pattern C — Modal action toggles a state flag.**
```python
def check_action5_toggles_polarity():
    g = GameClass()
    g.set_level(0)
    p0 = g.polarity                  # adapt: whatever the modal flag is
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    return g.polarity != p0, f"before={p0} after={g.polarity}"
```

**Pattern D — Action increments the engine action counter.**
```python
def check_action_counter_increments():
    g = GameClass()
    g.set_level(0)
    n0 = g._action_count
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    return g._action_count == n0 + 1, f"before={n0} after={g._action_count}"
```

**Pattern E — Lose triggers when budget exhausts.**
```python
def check_lose_at_budget():
    g = GameClass()
    g.set_level(0)
    budget = g.max_steps             # adapt: whatever attribute holds the L1 budget
    for _ in range(budget + 1):
        g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    return g._state.name == "GAME_OVER", f"state after budget+1={g._state.name}"
```

**Pattern F — Hand-crafted minimal solve enters WIN/next_level.**
Only write this if the spec's level-1 expected solution is short
(≤ 5 actions). Otherwise too much could go wrong inside the
sequence and a failure is hard to localise.
```python
def check_l1_minimal_solve():
    g = GameClass()
    g.set_level(0)
    seq = [GameAction.ACTION1, GameAction.ACTION1, GameAction.ACTION6]  # spec's L1 solution
    for aid in seq:
        if aid == GameAction.ACTION6:
            g.perform_action(ActionInput(id=aid, data={"x": 30, "y": 30}), raw=True)
        else:
            g.perform_action(ActionInput(id=aid), raw=True)
    return g._current_level_index == 1, f"level after solve={g._current_level_index}"
```

### Authoring procedure

1. Re-read `mechanic-spec.md` § "Win condition" and § "Action mapping".
2. List the 3-5 mechanic invariants that, if broken, would make the
   game unsolvable or unrecognisable (e.g. "the avatar moves",
   "click selects", "ACTION5 toggles state", "energy bar can lose
   you the level"). These are your candidates.
3. For each candidate, ask: *can I test this with ≤ 5 setup actions
   and a single boolean assertion?* If no → drop. If yes → write
   the check using one of the templates above.
4. Pick **2-4 of the strongest** to commit. Fewer is fine.
5. Author each check inline in `workspace/smoke-test-custom.py`
   (one function per check, all named `check_<short_name>`,
   returning `(bool, str)`).
6. Run them in the smoke_test state alongside the universal checks.

### Failure handling for custom checks

A custom-check failure goes into `workspace/smoke-test-failures.md`
under a `## Custom checks` section, with the same four fields:
`observed`, `threshold` (= "True"), `diagnosis` (the docstring of
the failing check), and `fix-direction` (where in the source to
look — usually the action handler in `step()` for that action).

If a custom check fails because the spec is wrong (rather than the
implementation), `fix_implementation` should write `error.md` and
halt — see that state's "spec-level problem" guidance.

## Output schema

If every check passes, the state writes
`workspace/smoke-test-pass.md`:

```markdown
# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera == level.grid_size |
| CHECK_SPRITE_CONTENT | 4 | 5 | 5 | distinct non-letter-box palettes |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions branched |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions |
| CHECK_PALETTE_RANGE | 0..14 | 0..14 | 0..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | next_level() found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | lose() found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | per-level camera resize present |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_up_moves_pawn | y0=6 y1=5 | UP moves active pawn 1 cell up |
| check_click_selects | active is pawn[1] | clicking pawn[1] makes it active |
| check_action_counter_increments | before=0 after=1 | counter advances |

Visit count: <N>/6.
```

Otherwise the state writes
`workspace/smoke-test-failures.md`:

```markdown
# Smoke test FAILURES (visit <N>/6)

## CHECK_CAMERA_VIEWPORT (level 1)
- observed: camera (64, 64), level.grid_size (12, 12) — mismatch
- threshold: camera viewport == level.grid_size for every level
- diagnosis: Camera viewport not resized for L1. `level.grid_size`
  is (12, 12) but `camera._width, camera._height` are (64, 64);
  the grid renders at scale=1 in a 12x12 patch in the top-left
  corner of the 64x64 output and the rest of the frame is
  letter-box.
- fix-direction: in `on_set_level`, add:
      gw, gh = level.grid_size or (64, 64)
      self.camera.width = gw
      self.camera.height = gh

## CHECK_SPRITE_CONTENT (level 2)
- observed: 1 distinct non-letter-box palette
- threshold: ≥ 2
- diagnosis: Level 2 rendered frame contains only the background
  palette value (no sprite content). Likely cause: <details>.
- fix-direction: <bullet>.

(... more failures ...)
```

Each failure entry has the same four fields: `observed`, `threshold`,
`diagnosis`, `fix-direction`. The `fix-direction` is what
`fix_implementation` reads to decide what to edit.
