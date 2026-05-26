"""tm5x — a generated NovaPlay game."""

import numpy as np
from novaengine import (
    ActionInput,
    NovaBaseGame,
    Camera,
    GameAction,
    InteractionMode,
    Level,
    RenderableUserDisplay,
    Sprite,
)


# ======================================================================
# 1. Sprite bank
# ======================================================================

PAWN_HOT_PIXELS = [
    [5, 8, 8, 5],
    [8, 7, 7, 8],
    [8, 7, 7, 8],
    [5, 8, 8, 5],
]
PAWN_COLD_PIXELS = [
    [5, 9, 9, 5],
    [9, 10, 10, 9],
    [9, 10, 10, 9],
    [5, 9, 9, 5],
]

TARGET_HOT_PIXELS = [
    [14, 14, 14, 14],
    [14, 8, 8, 14],
    [14, 8, 8, 14],
    [14, 14, 14, 14],
]
TARGET_COLD_PIXELS = [
    [14, 14, 14, 14],
    [14, 9, 9, 14],
    [14, 9, 9, 14],
    [14, 14, 14, 14],
]

TARGET_HOT_SATISFIED_PIXELS = [
    [11, 11, 11, 11],
    [11, 8, 8, 11],
    [11, 8, 8, 11],
    [11, 11, 11, 11],
]
TARGET_COLD_SATISFIED_PIXELS = [
    [11, 11, 11, 11],
    [11, 9, 9, 11],
    [11, 9, 9, 11],
    [11, 11, 11, 11],
]

WALL_PIXELS = [
    [5, 5, 5, 5],
    [5, 3, 3, 5],
    [5, 3, 3, 5],
    [5, 5, 5, 5],
]

EMPTY_FIELD_PIXELS = [[0] * 64 for _ in range(64)]


sprites = {
    "pawn_cold": Sprite(
        pixels=PAWN_COLD_PIXELS,
        name="pawn_cold",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=2,
    ),
    "pawn_hot": Sprite(
        pixels=PAWN_HOT_PIXELS,
        name="pawn_hot",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=2,
    ),
    "target_cold": Sprite(
        pixels=TARGET_COLD_PIXELS,
        name="target_cold",
        visible=True,
        collidable=False,
        tags=["target"],
        layer=1,
    ),
    "target_cold_satisfied": Sprite(
        pixels=TARGET_COLD_SATISFIED_PIXELS,
        name="target_cold_satisfied",
        visible=True,
        collidable=False,
        tags=["target_satisfied"],
        layer=1,
    ),
    "target_hot": Sprite(
        pixels=TARGET_HOT_PIXELS,
        name="target_hot",
        visible=True,
        collidable=False,
        tags=["target"],
        layer=1,
    ),
    "target_hot_satisfied": Sprite(
        pixels=TARGET_HOT_SATISFIED_PIXELS,
        name="target_hot_satisfied",
        visible=True,
        collidable=False,
        tags=["target_satisfied"],
        layer=1,
    ),
    "temperature_field": Sprite(
        pixels=EMPTY_FIELD_PIXELS,
        name="temperature_field",
        visible=True,
        collidable=False,
        tags=["thermal_field"],
        layer=-1,
    ),
    "wall_insulator": Sprite(
        pixels=WALL_PIXELS,
        name="wall_insulator",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=3,
    ),
}


# ======================================================================
# 2. Levels
# ======================================================================

CELL_STRIDE = 4
THERMAL_GRID = 16


def _cell_to_display(cx, cy):
    return cx * CELL_STRIDE, cy * CELL_STRIDE


def _build_pawn_pair(start_cell_x, start_cell_y):
    px, py = _cell_to_display(start_cell_x, start_cell_y)
    hot = sprites["pawn_hot"].clone().set_position(px, py)
    cold = sprites["pawn_cold"].clone().set_position(px, py)
    cold.set_interaction(InteractionMode.REMOVED)
    return [hot, cold]


def _build_target(name, cell_x, cell_y):
    px, py = _cell_to_display(cell_x, cell_y)
    return sprites[name].clone().set_position(px, py)


def _build_l3_walls():
    """Column-8 wall, thermal rows 4..15. Gap rows 0..3."""
    walls = []
    for cy in range(4, THERMAL_GRID):
        wx, wy = _cell_to_display(8, cy)
        walls.append(sprites["wall_insulator"].clone().set_position(wx, wy))
    return walls


def _build_field():
    return sprites["temperature_field"].clone().set_position(0, 0)


levels = [
    Level(
        sprites=[
            _build_field(),
            *_build_pawn_pair(8, 8),
            _build_target("target_hot", 8, 13),
        ],
        grid_size=(64, 64),
        data={"step_budget": 30},
    ),
    Level(
        sprites=[
            _build_field(),
            *_build_pawn_pair(8, 8),
            _build_target("target_hot", 3, 8),
            _build_target("target_cold", 13, 8),
        ],
        grid_size=(64, 64),
        data={"step_budget": 60},
    ),
    Level(
        sprites=[
            _build_field(),
            *_build_pawn_pair(3, 1),
            _build_target("target_hot", 3, 13),
            _build_target("target_cold", 13, 13),
            *_build_l3_walls(),
        ],
        grid_size=(64, 64),
        data={"step_budget": 100},
    ),
]


# ======================================================================
# 3. Constants
# ======================================================================

BACKGROUND_COLOR = 4
PADDING_COLOR = 4

POLARITY_HOT = 1
POLARITY_COLD = -1

TARGET_REQUIRED = {
    "target_hot": 2,
    "target_cold": -2,
}

TARGET_SATISFIED_NAME = {
    "target_hot": "target_hot_satisfied",
    "target_cold": "target_cold_satisfied",
}

THERMAL_PATTERNS = {
    -2: np.array(
        [
            [10, 4, 4, 10],
            [4, 4, 4, 4],
            [4, 4, 4, 4],
            [10, 4, 4, 10],
        ],
        dtype=np.int8,
    ),
    -1: np.array(
        [
            [0, 10, 10, 0],
            [10, 10, 10, 10],
            [10, 10, 10, 10],
            [0, 10, 10, 0],
        ],
        dtype=np.int8,
    ),
    0: np.array(
        [
            [1, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 0, 0, 1],
        ],
        dtype=np.int8,
    ),
    1: np.array(
        [
            [0, 7, 7, 0],
            [7, 7, 7, 7],
            [7, 7, 7, 7],
            [0, 7, 7, 0],
        ],
        dtype=np.int8,
    ),
    2: np.array(
        [
            [7, 8, 8, 7],
            [8, 8, 8, 8],
            [8, 8, 8, 8],
            [7, 8, 8, 7],
        ],
        dtype=np.int8,
    ),
}


# ======================================================================
# 4. HUD
# ======================================================================


class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int) -> None:
        self._max = max(1, max_steps)
        self._current = self._max

    def set_state(self, current: int, max_steps: int) -> None:
        self._max = max(1, max_steps)
        self._current = max(0, min(current, self._max))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self._max == 0:
            return frame
        ratio = self._current / self._max
        filled = int(round(64 * ratio))
        filled = max(0, min(64, filled))
        for x in range(64):
            frame[0, x] = 5 if x < filled else 0
        return frame


# ======================================================================
# 5. Game class
# ======================================================================


class Tm5x(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_hud = StepCounterHud(max_steps=30)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_hud],
        )
        self._polarity = POLARITY_HOT
        self._temperature = np.zeros((THERMAL_GRID, THERMAL_GRID), dtype=np.int8)
        self._satisfied: set[str] = set()
        self._initial_target_names: set[str] = set()
        super().__init__(
            game_id="tm5x",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    # ---------- per-level setup ----------

    def on_set_level(self, level: Level) -> None:
        budget = level.get_data("step_budget") or 30
        self._step_counter_hud.set_state(budget, budget)
        self._polarity = POLARITY_HOT
        self._satisfied = set()
        self._initial_target_names = {
            t.name for t in level.get_sprites_by_tag("target")
        }
        self._init_pawn_variants()
        self._recompute_temperature()
        self._update_field_pixels()

    def _init_pawn_variants(self) -> None:
        # Levels place both pawn_hot and pawn_cold at the same start cell.
        # Ensure pawn_hot is TANGIBLE (default) and pawn_cold is REMOVED;
        # they share the same display position.
        hot_list = self.current_level.get_sprites_by_name("pawn_hot")
        cold_list = self.current_level.get_sprites_by_name("pawn_cold")
        if not hot_list or not cold_list:
            return
        hot = hot_list[0]
        cold = cold_list[0]
        hot.set_interaction(InteractionMode.TANGIBLE)
        cold.set_position(hot.x, hot.y)
        cold.set_interaction(InteractionMode.REMOVED)

    # ---------- pawn helpers ----------

    def _active_pawn(self) -> Sprite | None:
        active_name = "pawn_hot" if self._polarity == POLARITY_HOT else "pawn_cold"
        sprites_list = self.current_level.get_sprites_by_name(active_name)
        if not sprites_list:
            return None
        return sprites_list[0]

    def _toggle_polarity(self) -> None:
        active = self._active_pawn()
        if active is None:
            self._polarity = -self._polarity
            return
        px, py = active.x, active.y

        self._polarity = -self._polarity

        new_active_name = (
            "pawn_hot" if self._polarity == POLARITY_HOT else "pawn_cold"
        )
        new_inactive_name = (
            "pawn_cold" if self._polarity == POLARITY_HOT else "pawn_hot"
        )
        new_active_list = self.current_level.get_sprites_by_name(new_active_name)
        new_inactive_list = self.current_level.get_sprites_by_name(new_inactive_name)
        if not new_active_list or not new_inactive_list:
            return
        new_active = new_active_list[0]
        new_inactive = new_inactive_list[0]
        new_active.set_position(px, py)
        new_active.set_interaction(InteractionMode.TANGIBLE)
        new_inactive.set_position(px, py)
        new_inactive.set_interaction(InteractionMode.REMOVED)

    def _is_wall_at(self, cell_x: int, cell_y: int) -> bool:
        wx, wy = _cell_to_display(cell_x, cell_y)
        for wall in self.current_level.get_sprites_by_tag("wall"):
            if wall.x == wx and wall.y == wy:
                return True
        return False

    def _try_move(self, dx_cells: int, dy_cells: int) -> None:
        pawn = self._active_pawn()
        if pawn is None:
            return
        cx, cy = pawn.x // CELL_STRIDE, pawn.y // CELL_STRIDE
        nx, ny = cx + dx_cells, cy + dy_cells
        if not (0 <= nx < THERMAL_GRID and 0 <= ny < THERMAL_GRID):
            return
        if self._is_wall_at(nx, ny):
            return
        npx, npy = _cell_to_display(nx, ny)
        pawn.set_position(npx, npy)
        # Keep the inactive variant aligned with the active pawn so a
        # subsequent ACTION5 toggles in place.
        inactive_name = (
            "pawn_cold" if self._polarity == POLARITY_HOT else "pawn_hot"
        )
        inactive_list = self.current_level.get_sprites_by_name(inactive_name)
        if inactive_list:
            inactive_list[0].set_position(npx, npy)

    # ---------- thermal field ----------

    def _recompute_temperature(self) -> None:
        self._temperature[:] = 0
        pawn = self._active_pawn()
        if pawn is None:
            return
        cx, cy = pawn.x // CELL_STRIDE, pawn.y // CELL_STRIDE
        if 0 <= cx < THERMAL_GRID and 0 <= cy < THERMAL_GRID:
            self._temperature[cy, cx] = 2 * self._polarity
        for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
            if not (0 <= nx < THERMAL_GRID and 0 <= ny < THERMAL_GRID):
                continue
            if self._is_wall_at(nx, ny):
                continue
            self._temperature[ny, nx] = 1 * self._polarity

    def _update_field_pixels(self) -> None:
        field_list = self.current_level.get_sprites_by_name("temperature_field")
        if not field_list:
            return
        field = field_list[0]
        new_pixels = np.zeros((64, 64), dtype=np.int8)
        for cy in range(THERMAL_GRID):
            for cx in range(THERMAL_GRID):
                t = int(self._temperature[cy, cx])
                pattern = THERMAL_PATTERNS[t]
                py, px = cy * CELL_STRIDE, cx * CELL_STRIDE
                new_pixels[py : py + CELL_STRIDE, px : px + CELL_STRIDE] = pattern
        field.pixels = new_pixels

    def _check_targets(self) -> None:
        for target in list(self.current_level.get_sprites_by_tag("target")):
            if target.name in self._satisfied:
                continue
            required = TARGET_REQUIRED.get(target.name)
            if required is None:
                continue
            cx = target.x // CELL_STRIDE
            cy = target.y // CELL_STRIDE
            if not (0 <= cx < THERMAL_GRID and 0 <= cy < THERMAL_GRID):
                continue
            if int(self._temperature[cy, cx]) == required:
                self._satisfied.add(target.name)
                satisfied_name = TARGET_SATISFIED_NAME.get(target.name)
                if satisfied_name and satisfied_name in sprites:
                    badge = (
                        sprites[satisfied_name]
                        .clone()
                        .set_position(target.x, target.y)
                    )
                    self.current_level.add_sprite(badge)
                    target.set_interaction(InteractionMode.REMOVED)

    # ---------- step ----------

    def step(self) -> None:
        budget = self.current_level.get_data("step_budget") or 30

        if self.action.id == GameAction.ACTION1:
            self._try_move(0, -1)
        elif self.action.id == GameAction.ACTION2:
            self._try_move(0, 1)
        elif self.action.id == GameAction.ACTION3:
            self._try_move(-1, 0)
        elif self.action.id == GameAction.ACTION4:
            self._try_move(1, 0)
        elif self.action.id == GameAction.ACTION5:
            self._toggle_polarity()

        self._recompute_temperature()
        self._update_field_pixels()
        self._check_targets()

        remaining = max(0, budget - self._action_count)
        self._step_counter_hud.set_state(remaining, budget)

        if (
            self._initial_target_names
            and self._initial_target_names.issubset(self._satisfied)
        ):
            self.next_level()
            self.complete_action()
            return

        if self._action_count >= budget:
            self.lose()

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._polarity
        state[0, 1] = len(self._satisfied)
        state[0, 2] = int(self._action_count)
        return state

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()
