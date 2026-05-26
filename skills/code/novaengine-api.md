# novaengine API cheatsheet

Vendored at the repo root: `novaengine/`. Read that directory to
verify any signature; this file is a curated summary of what the 25
reference games actually use.

## Imports

```python
import numpy as np
from novaengine import (
    ActionInput,
    NovaBaseGame,
    BlockingMode,
    Camera,
    GameAction,
    InteractionMode,
    Level,
    RenderableUserDisplay,
    Sprite,
)
```

## `Sprite`

`Sprite(pixels, name, visible=True, collidable=True, blocking=BlockingMode.PIXEL_PERFECT, interaction=InteractionMode.TANGIBLE, tags=None, layer=0)` — declarative sprite definition.

- `pixels`: 2D list[list[int]] in palette 0..15. `-1` = transparent.
- `name`: string identifier; sprites are looked up by name.
- `tags`: list of tags for grouping (`level.get_sprites_by_tag(tag)`).
- `layer`: render order (higher = on top).

Runtime methods (callable from `Game.step` / `Game.on_set_level`):

- `move(dx, dy)` — translate by integer offsets.
- `set_position(x, y)` — absolute placement.
- `rotate(deg)` — rotate by 90/180/270 (degrees).
- `set_layer(n)` — change render layer.
- `render() -> np.ndarray` — render current pixels (post-rotation).
- `collides_with(other) -> bool` — pixel-level collision.
- `set_interaction(mode)` — toggle TANGIBLE / REMOVED / INTANGIBLE at runtime.

Properties: `.x`, `.y`, `.width`, `.height`, `.rotation`, `.pixels`,
`.name`.

## `Level`

`Level(sprites, grid_size, level_data=None)` — one level
configuration.

- `sprites`: list of Sprite OBJECTS (placed in this level). Each
  Sprite is from the global `sprites = {...}` dict.
- `grid_size`: `(W, H)` of the playable area in cells (most games
  use 64×64 sub-areas).
- `level_data`: optional dict for per-level parameters. Set with
  `level.set_data(key, val)` if needed; read with `level.get_data(key)`.

Runtime methods:

- `get_sprites()` — all sprites in the level.
- `get_sprites_by_tag(tag)` — filter by tag.
- `get_sprites_by_name(name)` — filter by name (returns list).
- `get_sprite_at(x, y, ignore_collidable=False)` — find sprite
  occupying (x, y).
- `get_data(key)` — pull level-specific data.

## `Camera`

`Camera(x=0, y=0, width=64, height=64, background=int, letter_box=int,
interfaces=None)` — viewport + HUD container.

- `background`: palette value used for empty cells.
- `letter_box`: palette value for the area outside the playable
  grid_size.
- `interfaces`: list of `RenderableUserDisplay` instances; rendered
  on top of the frame.
- `display_to_grid(x, y) -> (int, int) | None`: convert pixel-space
  click coords to grid coords.

## `NovaBaseGame`

`__init__(game_id, levels, camera, available_actions=[1..7])` —
parent class for all generated games. (Subset of `[1, 2, 3, 4, 5,
6, 7]`; ACTION6 carries click data.)

Override:

- `on_set_level(level: Level) -> None` — called when a level
  starts. Use to (re)populate per-level state.
- `step() -> None` — called once per action. Read `self.action.id`
  and dispatch. MUST end with `self.complete_action()`.
- `_get_hidden_state() -> np.ndarray` — debug hook; return any
  internal state worth exposing.
- `_get_valid_actions() -> list[ActionInput]` — override to gate
  available actions per turn (e.g. only certain actions during a
  drag sub-state).

Engine methods to call:

- `self.next_level()` — advance to next level.
- `self.lose()` / `self.win()` — terminate the run.
- `self.complete_action()` — must be the LAST line of `step()`.

Properties:

- `self.action` — current action (`.id` is GameAction; `.data` may
  be a dict for ACTION6).
- `self._action_count` — number of actions taken in this level.
- `self.current_level` — the Level being played.
- `self.camera` — the Camera.

## `GameAction` enum

`GameAction.ACTION1 .. GameAction.ACTION7`. Each has integer ID
(1..7). `GameAction.from_id(int) -> GameAction` for converting back.

## `ActionInput`

`ActionInput(id=GameAction, data=dict)` — wraps an action value.
Used by `_get_valid_actions`.

## `RenderableUserDisplay`

Base class for HUD widgets. Override `render_interface(frame:
np.ndarray) -> np.ndarray` to draw on top of the frame. Pass
instances to `Camera(interfaces=[...])`.

## `BlockingMode`

Enum with three values controlling how a `Sprite`'s collidable
flag is interpreted:

- `BlockingMode.PIXEL_PERFECT` — collisions are computed at the
  pixel level (default; honours `-1` transparent cells).
- `BlockingMode.BOUNDING_BOX` — collisions are computed at the
  sprite's bounding box only (cheaper, treats every cell as solid).
- `BlockingMode.NOT_BLOCKED` — the sprite never blocks others
  (e.g. visual-only overlays).

Set per-sprite at runtime: `sprite.set_blocking(BlockingMode.BOUNDING_BOX)`.
The `Sprite(...)` constructor also accepts `blocking=BlockingMode...`
as a keyword argument; default is `PIXEL_PERFECT`.

## `InteractionMode`

Enum that controls how a sprite participates in the level at runtime
(complementary to `collidable`/`blocking` which are static
properties). Used to selectively activate/deactivate sprites without
removing them from the level.

- `InteractionMode.TANGIBLE` — sprite is rendered AND participates in
  collision checks (default).
- `InteractionMode.REMOVED` — sprite is hidden from rendering and
  excluded from collision; functionally absent until restored.
- `InteractionMode.INTANGIBLE` — sprite is rendered but does not
  collide (overlay).

Set per-sprite at runtime: `sprite.set_interaction(InteractionMode.REMOVED)`.
The `Sprite(...)` constructor also accepts `interaction=InteractionMode...`
as a keyword argument; default is `TANGIBLE`.

This is the idiomatic way to swap two sprite variants at the same
cell — see "Two-sprite swap (polarity / state toggle)" under Common
patterns below.
