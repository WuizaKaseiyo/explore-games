"""ej4t."""

import numpy as np
from novaengine import (
    NovaBaseGame,
    Camera,
    GameAction,
    InteractionMode,
    Level,
    RenderableUserDisplay,
    Sprite,
)


# ---------------------------------------------------------------------
# Pixel patterns (constants reused across sprite instances)
# ---------------------------------------------------------------------
PLAYER_PIXELS = [
    [4, 0, 0, 0, 4],
    [9, 9, 9, 9, 9],
    [9, 9, 9, 9, 9],
    [4, 9, 4, 9, 4],
    [4, 9, 9, 9, 4],
]

WALL_PIXELS = [
    [4, 3, 3, 4],
    [3, 3, 3, 3],
    [3, 3, 3, 3],
    [4, 3, 3, 4],
]

CRATE_PIXELS = [
    [4, 12, 12, 4],
    [12, 13, 13, 12],
    [12, 13, 13, 12],
    [4, 12, 12, 4],
]

TARGET_PIXELS = [
    [4, 11, 4],
    [11, 11, 11],
    [4, 11, 4],
]

EXTENDER_PIXELS = [
    [-1, 14, -1],
    [14, 11, 14],
    [-1, 14, -1],
]

SHRINKER_PIXELS = [
    [4, 8, 4],
    [8, 4, 8],
    [4, 8, 4],
]

SHRINKER_SPENT_PIXELS = [
    [4, 3, 4],
    [3, 4, 3],
    [4, 3, 4],
]


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 1   # off-white
PADDING_COLOR = 2      # light-grey letter-box
RING_OVERLAY_COLOR = 10  # light-blue translucent halo

# Per-level parameters (matches mechanic-spec.md § 4)
L1_INIT_R = 2
L1_STEP_BUDGET = 25

L2_INIT_R = 1
L2_STEP_BUDGET = 30

L3_INIT_R = 2
L3_STEP_BUDGET = 35


# ---------------------------------------------------------------------
# Helpers for declaring sprite instances per level
# ---------------------------------------------------------------------
def _make_player(x, y):
    s = Sprite(
        pixels=PLAYER_PIXELS,
        name="player",
        visible=True,
        collidable=True,
        tags=["player"],
    )
    s.set_position(x, y)
    s.set_layer(3)
    return s


def _make_wall(x, y, idx):
    s = Sprite(
        pixels=WALL_PIXELS,
        name=f"wall_{idx}",
        visible=True,
        collidable=True,
        tags=["wall"],
    )
    s.set_position(x, y)
    return s


def _make_crate(x, y, idx):
    s = Sprite(
        pixels=CRATE_PIXELS,
        name=f"crate_{idx}",
        visible=True,
        collidable=True,
        tags=["crate", "pushable"],
    )
    s.set_position(x, y)
    s.set_layer(2)
    return s


def _make_target(x, y, idx):
    s = Sprite(
        pixels=TARGET_PIXELS,
        name=f"target_{idx}",
        visible=True,
        collidable=False,
        tags=["target"],
        interaction=InteractionMode.INTANGIBLE,
    )
    s.set_position(x, y)
    s.set_layer(1)
    return s


def _make_extender(x, y, idx):
    s = Sprite(
        pixels=EXTENDER_PIXELS,
        name=f"extender_{idx}",
        visible=True,
        collidable=False,
        tags=["extender"],
        interaction=InteractionMode.INTANGIBLE,
    )
    s.set_position(x, y)
    s.set_layer(1)
    return s


def _make_shrinker(x, y, idx):
    s = Sprite(
        pixels=SHRINKER_PIXELS,
        name=f"shrinker_{idx}",
        visible=True,
        collidable=False,
        tags=["shrinker"],
        interaction=InteractionMode.INTANGIBLE,
    )
    s.set_position(x, y)
    s.set_layer(1)
    return s


def _make_walls_corridor(left_x, right_x, top_y, bot_y, start_idx=0):
    """Create wall sprites along the top and bottom of a horizontal corridor."""
    walls = []
    idx = start_idx
    for x in range(left_x, right_x + 1):
        walls.append(_make_wall(x, top_y, idx))
        idx += 1
        walls.append(_make_wall(x, bot_y, idx))
        idx += 1
    return walls


# ---------------------------------------------------------------------
# Level construction
# ---------------------------------------------------------------------
def _build_level_1():
    # 12x12 grid; corridor at row 6 (cells y=6).
    # Each grid cell is 1x1 in conceptual space, but our sprites are
    # 4x4 (walls, crates) and 5x5 (player). To fit on a 12x12 grid
    # we treat each "logical" cell as one sprite-anchor; sprite
    # bounds are evaluated cell-by-cell during push.
    # Walls are 4x4 sprites placed at integer cell coords; they
    # will visually overlap into adjacent cells which is fine for
    # rendering since the corridor logic gates on top-left coords.
    sprites = []
    # Walls top + bottom of corridor (row 5 and row 7, cols 4-10)
    for x in range(4, 11):
        sprites.append(_make_wall(x, 5, 100 + x))
        sprites.append(_make_wall(x, 7, 200 + x))
    # Player at (3, 6)
    sprites.append(_make_player(3, 6))
    # Crates at (8, 6) and (9, 6); target at (10, 6)
    sprites.append(_make_crate(8, 6, 1))
    sprites.append(_make_crate(9, 6, 2))
    sprites.append(_make_target(10, 6, 1))
    return Level(sprites=sprites, grid_size=(12, 12))


def _build_level_2():
    # 14x14 grid; corridor at row 7 (cells y=7), walls at row 6 and row 8
    sprites = []
    for x in range(4, 13):
        sprites.append(_make_wall(x, 6, 300 + x))
        sprites.append(_make_wall(x, 8, 400 + x))
    sprites.append(_make_player(3, 7))
    # Extender_a at (5, 7)
    sprites.append(_make_extender(5, 7, "a"))
    # Crates at (8, 7) and (9, 7); target at (10, 7)
    sprites.append(_make_crate(8, 7, 1))
    sprites.append(_make_crate(9, 7, 2))
    sprites.append(_make_target(10, 7, 1))
    return Level(sprites=sprites, grid_size=(14, 14))


def _build_level_3():
    # 16x16 grid; corridor at row 7 (cells y=7), walls at row 6 and row 8
    sprites = []
    for x in range(4, 14):
        sprites.append(_make_wall(x, 6, 500 + x))
        sprites.append(_make_wall(x, 8, 600 + x))
    sprites.append(_make_player(3, 7))
    sprites.append(_make_extender(5, 7, "a"))
    sprites.append(_make_shrinker(7, 7, "a"))
    sprites.append(_make_extender(8, 7, "b"))
    sprites.append(_make_crate(10, 7, 1))
    sprites.append(_make_crate(11, 7, 2))
    sprites.append(_make_crate(12, 7, 3))
    sprites.append(_make_target(13, 7, 1))
    return Level(sprites=sprites, grid_size=(16, 16))


levels = [
    _build_level_1(),
    _build_level_2(),
    _build_level_3(),
]


# ---------------------------------------------------------------------
# HUD widgets
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    """Bottom-row depleting bar showing remaining step budget."""

    def __init__(self, max_steps: int = 25):
        super().__init__()
        self._max = max_steps
        self._used = 0

    def set_state(self, used: int, max_steps: int) -> None:
        self._used = used
        self._max = max_steps

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        # Draw 32-cell-wide horizontal bar at row 63, cols 16-47
        bar_y = 63
        x_start = 16
        x_end = 48
        bar_width = x_end - x_start
        if self._max <= 0:
            return frame
        remaining = max(0, self._max - self._used)
        filled_cells = int(round(bar_width * (remaining / self._max)))
        for i, x in enumerate(range(x_start, x_end)):
            if i < filled_cells:
                frame[bar_y, x] = 9   # blue (remaining)
            else:
                frame[bar_y, x] = 3   # grey (depleted)
        return frame


class RingOverlayHud(RenderableUserDisplay):
    """Translucent halo over cells within Manhattan distance R of player."""

    def __init__(self):
        super().__init__()
        self._player_x = 0
        self._player_y = 0
        self._radius = 0
        self._grid_w = 12
        self._grid_h = 12
        self._scale = 1
        self._x_offset = 0
        self._y_offset = 0

    def set_state(self, px: int, py: int, r: int, gw: int, gh: int) -> None:
        self._player_x = px
        self._player_y = py
        self._radius = r
        self._grid_w = gw
        self._grid_h = gh
        # Match camera's scale calculation: scale = 64 // grid_size
        self._scale = max(1, 64 // max(gw, gh))
        # Centre the playfield
        self._x_offset = (64 - self._scale * gw) // 2
        self._y_offset = (64 - self._scale * gh) // 2

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        # Paint a thin translucent overlay on cells within R Manhattan of player.
        # Skip the player's own cell.
        for cy in range(self._grid_h):
            for cx in range(self._grid_w):
                # Manhattan distance from player to this cell (cell-anchor coords).
                dist = abs(cx - self._player_x) + abs(cy - self._player_y)
                if 0 < dist <= self._radius:
                    # Map to display pixel range
                    px_start = self._x_offset + cx * self._scale
                    py_start = self._y_offset + cy * self._scale
                    px_end = min(64, px_start + self._scale)
                    py_end = min(64, py_start + self._scale)
                    # Draw a 1-pixel-thick ring around the cell border for halo effect
                    # without obscuring the underlying sprite.
                    if 0 <= py_start < 64 and 0 <= px_start < 64:
                        # Top edge
                        frame[py_start, px_start:px_end] = RING_OVERLAY_COLOR
                        # Bottom edge
                        if py_end - 1 < 64:
                            frame[py_end - 1, px_start:px_end] = RING_OVERLAY_COLOR
                        # Left edge
                        frame[py_start:py_end, px_start] = RING_OVERLAY_COLOR
                        # Right edge
                        if px_end - 1 < 64:
                            frame[py_start:py_end, px_end - 1] = RING_OVERLAY_COLOR
        return frame


# ---------------------------------------------------------------------
# The game class
# ---------------------------------------------------------------------
class Ej4t(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_hud = StepCounterHud(max_steps=25)
        self._ring_hud = RingOverlayHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._ring_hud, self._step_counter_hud],
        )
        super().__init__(
            game_id="ej4t",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )
        # Per-game state initialised in on_set_level
        self._R = 2
        self._steps_used = 0
        self._max_steps = 25

    def on_set_level(self, level: Level) -> None:
        # Resize camera viewport to match level grid size
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        # Determine per-level params from the engine's _current_level_index
        idx = getattr(self, "_current_level_index", 0)
        if idx == 0:
            self._R = L1_INIT_R
            self._max_steps = L1_STEP_BUDGET
        elif idx == 1:
            self._R = L2_INIT_R
            self._max_steps = L2_STEP_BUDGET
        else:
            self._R = L3_INIT_R
            self._max_steps = L3_STEP_BUDGET
        self._steps_used = 0
        # Sync HUDs
        self._step_counter_hud.set_state(self._steps_used, self._max_steps)
        self._update_ring_hud(level)

    def _update_ring_hud(self, level: Level) -> None:
        players = level.get_sprites_by_tag("player")
        if not players:
            return
        p = players[0]
        gw, gh = level.grid_size or (64, 64)
        self._ring_hud.set_state(p.x, p.y, self._R, gw, gh)

    def _player(self):
        return self.current_level.get_sprites_by_tag("player")[0]

    def _direction(self, action_id) -> tuple[int, int]:
        if action_id == GameAction.ACTION1:
            return (0, -1)
        if action_id == GameAction.ACTION2:
            return (0, 1)
        if action_id == GameAction.ACTION3:
            return (-1, 0)
        if action_id == GameAction.ACTION4:
            return (1, 0)
        return (0, 0)

    def _cell_blocked_by_wall(self, x, y) -> bool:
        gw, gh = self.current_level.grid_size or (64, 64)
        if x < 0 or x >= gw or y < 0 or y >= gh:
            return True
        for w in self.current_level.get_sprites_by_tag("wall"):
            if w.x == x and w.y == y:
                return True
        return False

    def _crate_at(self, x, y):
        for c in self.current_level.get_sprites_by_tag("crate"):
            if c.x == x and c.y == y:
                return c
        return None

    def _attempt_push_chain(self, dx, dy, p) -> bool:
        """Try to walk the player; if pushing into a crate, attempt push.
        Returns True if any movement happened (player and/or crates moved)."""
        target_x = p.x + dx
        target_y = p.y + dy
        # Wall blocks player walk
        if self._cell_blocked_by_wall(target_x, target_y):
            return False
        # Build the chain: starting at the cell the player walks into,
        # follow consecutive crates in direction (dx, dy).
        chain = []
        cx, cy = target_x, target_y
        while True:
            crate = self._crate_at(cx, cy)
            if crate is None:
                break
            chain.append(crate)
            cx, cy = cx + dx, cy + dy
        if not chain:
            # No crate at target — simple walk
            p.move(dx, dy)
            return True
        # There is a chain of crates. Check radius gate for ALL crates beyond
        # the first one (the first crate is always pushable by player; chain
        # rule applies to crate-crate links).
        for i in range(1, len(chain)):
            c = chain[i]
            dist = abs(c.x - p.x) + abs(c.y - p.y)
            if dist > self._R:
                # Chain breaks at this crate; entire push fails (atomic).
                return False
        # Final cell beyond last crate must be empty (not wall, not another
        # crate — we already chained all crates).
        last_cx = chain[-1].x + dx
        last_cy = chain[-1].y + dy
        if self._cell_blocked_by_wall(last_cx, last_cy):
            return False
        # All checks passed; commit movement.
        # Move crates from rear to front to avoid overlap.
        for c in reversed(chain):
            c.move(dx, dy)
        p.move(dx, dy)
        return True

    def _consume_pickups_at_player(self, p) -> None:
        """Walk through extender / shrinker pickups consumes them."""
        for ext in self.current_level.get_sprites_by_tag("extender"):
            if ext.interaction == InteractionMode.INTANGIBLE and ext.x == p.x and ext.y == p.y:
                self._R += 1
                ext.set_interaction(InteractionMode.REMOVED)
        for sh in self.current_level.get_sprites_by_tag("shrinker"):
            if sh.interaction == InteractionMode.INTANGIBLE and sh.x == p.x and sh.y == p.y:
                self._R = max(0, self._R - 1)
                # Recolour shrinker to "spent" (palette 3, no longer red)
                sh.pixels = np.array(SHRINKER_SPENT_PIXELS, dtype=np.int16)
                sh.set_interaction(InteractionMode.REMOVED)

    def _check_win(self) -> bool:
        crate_positions = {(c.x, c.y) for c in self.current_level.get_sprites_by_tag("crate")}
        target_positions = {(t.x, t.y) for t in self.current_level.get_sprites_by_tag("target")}
        return target_positions.issubset(crate_positions)

    def step(self) -> None:
        # Check lose at top
        if self._steps_used >= self._max_steps:
            self.lose()
            self.complete_action()
            return

        if self.action.id in (GameAction.ACTION1, GameAction.ACTION2,
                              GameAction.ACTION3, GameAction.ACTION4):
            dx, dy = self._direction(self.action.id)
            p = self._player()
            moved = self._attempt_push_chain(dx, dy, p)
            if moved:
                self._consume_pickups_at_player(p)
                self._steps_used += 1
                self._step_counter_hud.set_state(self._steps_used, self._max_steps)
                self._update_ring_hud(self.current_level)
                if self._check_win():
                    self.next_level()
                    self.complete_action()
                    return
            else:
                # Failed action still consumes a step
                self._steps_used += 1
                self._step_counter_hud.set_state(self._steps_used, self._max_steps)
            # Re-check lose after step
            if self._steps_used >= self._max_steps:
                self.lose()
                self.complete_action()
                return

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.array([[self._R]], dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
