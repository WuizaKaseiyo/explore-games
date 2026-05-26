# Universal scaffold for a generated game file

Every game file MUST follow this structure. Order matters: imports
first, then sprite bank, then levels, then constants, then optional
HUD widgets, then the game class.

```python
"""Optional one-line description (NOT containing the game's mechanic
- the ID is opaque)."""

import numpy as np
from novaengine import (
    NovaBaseGame,
    Camera,
    GameAction,
    Level,
    RenderableUserDisplay,
    Sprite,
)

# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "<sprite_name>": Sprite(
        pixels=[
            [<int>, ...],
            ...
        ],
        name="<sprite_name>",
        visible=True,
        collidable=True,
        tags=["<tag>"],
    ),
    # ... more sprites
}

# ---------------------------------------------------------------------
# 2. LEVELS  (EXACTLY 3 entries, level 0 is the tutorial)
# ---------------------------------------------------------------------
levels = [
    Level(
        sprites=[<list of placed Sprite instances>],
        grid_size=(<W>, <H>),
    ),
    # ... 2 more levels (3 total)
]

# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = <palette int>
PADDING_COLOR = <palette int>

# ---------------------------------------------------------------------
# 4. OPTIONAL HUD WIDGETS
# ---------------------------------------------------------------------
class <HudWidget>(RenderableUserDisplay):
    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        # ... draw on top of `frame`
        return frame

# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class <Pascal>(NovaBaseGame):
    def __init__(self) -> None:
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
        )
        super().__init__(
            game_id="<4_char_id>",
            levels=levels,
            camera=camera,
            available_actions=[<subset of 1..7>],
        )

    def on_set_level(self, level: Level) -> None:
        # CRITICAL: re-size the camera viewport to match this level's
        # grid_size; see `## Camera viewport must match level grid_size`.
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        # initialise per-level state
        ...

    def step(self) -> None:
        # dispatch on self.action.id
        if self.action.id == GameAction.ACTION1:
            ...
        # ...
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
```

## Camera viewport must match level grid_size

The novaengine `Camera` defaults to `width=64, height=64`. If your
levels have a smaller `grid_size` (e.g. `(12, 12)`, `(16, 16)`,
`(20, 20)`) and you do NOT resize the camera, the `Camera.render`
pipeline does the following:

- `_calculate_scale_and_offset()` computes
  `scale = MAX_DIMENSION // self._width = 64 // 64 = 1`.
- The grid renders 1 pixel per cell, occupying only the top-left
  `grid_size` rectangle of the 64×64 output.
- The remainder of the frame is letter_box.
- Any HUD widget (e.g. `ActiveMarkerHud`) that computes a scale of
  its own from `level.grid_size` will draw at scaled coordinates
  the camera never produced — its decorations land in the empty
  letter-box area.
- ACTION6 click coordinates the agent computes at the imagined
  scale will pass through `camera.display_to_grid` at scale=1, hit
  out-of-bounds cells, and the click does nothing.

**Required**: in `on_set_level`, set the camera viewport to match
the level's `grid_size`:

```python
def on_set_level(self, level: Level) -> None:
    gw, gh = level.grid_size or (64, 64)
    self.camera.width = gw
    self.camera.height = gh
    # ... rest of per-level initialisation
```

The camera then computes the correct scale (e.g. 5× for a 12×12
grid → 60×60 fills most of 64×64 with 2-pixel letter-box on each
side) and centres it in the output. HUD widgets that re-compute
the same scale via `64 // grid_size[0]` will agree with the camera,
and `display_to_grid` will round display pixels back to the right
grid cell.

If your game has a single fixed grid_size of exactly 64×64 (like
ls20), you can skip this — the default 64×64 camera matches and
no scaling is needed.

If your game uses a scrolling viewport (camera smaller than the
grid, like ft09 with a 16×16 viewport over a 32×32 grid), set the
viewport to your scrolling window dimensions, NOT to the level's
grid size, and manage `camera.x` / `camera.y` per turn.

## Style rules

**The 25 reference games obfuscate names for crack-proofing.** The
official games are released to a competitive setting where players
might dig into the source to cheat, so the reference games use
opaque 10-character random-lowercase tokens for sprite dict keys,
sprite `name=` fields, helper-class names (`qkndvajqsk`,
`wztyojnvey`), helper-method names, and module-level constants.

**Our generated games are NOT shipped to that setting** — they are
prototypes, played by the human author and used for harness
iteration. Readable code is far more valuable than crack-proofing.
**Use meaningful, semantic names throughout.** Examples:

- *Sprite dict keys*: `"player"`, `"target_yellow"`, `"wax_pickup"`
  — not `"lzajfunopv"` or `"cdpjpckayh"`.
- *Sprite `name=` field*: same as the dict key.
- *Helper class names*: `StepCounterHud`, `ConeOverlay` — not
  `qkndvajqsk` or `wztyojnvey`.
- *Helper method / function names*: `_check_win`, `_rotate_unlocked`,
  `_consume_pickup_at_lantern` — what the method does, in plain
  English.
- *Module-level constants*: `BACKGROUND_COLOR`, `WAX_BONUS`,
  `LIT_FROM_YELLOW` — what the constant means.

The only naming convention we keep from the reference games:

- **Class name** is a Pascal-case spelling of the 4-character game
  ID (e.g. `Cn04` for `cn04`). This is required because the runner
  / loader looks the class up by ID-derived name. NOT a semantic
  name — the ID *is* the game's identifier.
- **Tags** can be semantic (`"player"`, `"wall"`, `"goal"`) — same
  as before; tags are runtime-only and never visible to the player.

**No comments referring to the mechanic.** A reader peeking at the
source should not be able to deduce the goal from comments. Code
comments may explain the algorithm but never the game's intent.
Note that meaningful names alone do not give away the *goal* of
the game — calling a sprite `lantern` says what the sprite is, not
what the player must do with it.

## Common patterns used in the 25 reference games

- **Step counter HUD**: a small `RenderableUserDisplay` subclass
  draws a horizontal bar reflecting actions remaining; updated in
  `step()`.
- **Click-to-select**: ACTION6's `data["x"], data["y"]` flows
  through `camera.display_to_grid` into a grid coordinate; then
  `level.get_sprite_at(...)` finds the clicked sprite.
- **Tag-based grouping**: sprites are grouped via shared tags;
  `level.get_sprites_by_tag(tag)` returns the group.
- **Per-level data**: `level.get_data(key)` returns level-specific
  parameters (e.g. target shape, max steps, win threshold).
- **Movement guard**: before calling `sprite.move(dx, dy)`, check
  `sprite.x + dx >= 0` etc. against `level.grid_size`.
- **Two-sprite swap (polarity / state toggle)**: when a player can
  toggle between two visible states (e.g. polarity +1 ↔ -1), declare
  BOTH sprite variants in the level, place them at the same cell at
  level-start, set the inactive one to `InteractionMode.REMOVED` and
  the active one to `InteractionMode.TANGIBLE`. On toggle, swap their
  modes (and their positions if the player has moved since
  level-start). Cleaner than `set_visible(False)` because it also
  removes collision; cleaner than `set_position(-100, -100)` because
  the sprite stays inside the level for inspection.
- **Simultaneous-conflict resolution gotcha**: when multiple sprites
  slide concurrently (e.g. a magnet response pulls two blocks toward
  the same destination cell), the naive resolution rule "block A's
  destination is allowed if not occupied by a non-sliding block" is
  incomplete. Two sliding sprites can both target the same cell, OR
  sprite A can target sprite B's old cell while B is also sliding —
  if B's slide fails, A and B end up overlapping. Resolve by:
  computing all desired destinations, dropping any whose destination
  is blocked, dropping any duplicate destination, AND only committing
  a slide if the destination's current occupant is itself committing
  to leave. A two-pass (compute desires → resolve conflicts → commit)
  is safer than per-block sequential commits.
