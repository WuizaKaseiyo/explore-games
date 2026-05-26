"""hl4n."""

import numpy as np
from novaengine import (
    ActionInput,
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
    "cell": Sprite(
        pixels=[
            [2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2],
        ],
        name="cell",
        visible=True,
        collidable=True,
        tags=["cell"],
    ),
    "row_marker": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4],
            [4, 2, 2, 2, 2, 4],
            [4, 2, 2, 2, 2, 4],
            [4, 2, 2, 2, 2, 4],
            [4, 2, 2, 2, 2, 4],
            [4, 4, 4, 4, 4, 4],
        ],
        name="row_marker",
        visible=True,
        collidable=True,
        tags=["row_marker", "sys_click"],
    ),
    "col_marker": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4],
            [4, 2, 2, 2, 2, 4],
            [4, 2, 2, 2, 2, 4],
            [4, 2, 2, 2, 2, 4],
            [4, 2, 2, 2, 2, 4],
            [4, 4, 4, 4, 4, 4],
        ],
        name="col_marker",
        visible=True,
        collidable=True,
        tags=["col_marker", "sys_click"],
    ),
    "lock_red": Sprite(
        pixels=[
            [8, 8, 8, 8, 8, 8],
            [8, -1, -1, -1, -1, 8],
            [8, -1, -1, -1, -1, 8],
            [8, -1, -1, -1, -1, 8],
            [8, -1, -1, -1, -1, 8],
            [8, 8, 8, 8, 8, 8],
        ],
        name="lock_red",
        visible=True,
        collidable=False,
        tags=["lock_target", "req_8"],
    ),
    "lock_yellow": Sprite(
        pixels=[
            [11, 11, 11, 11, 11, 11],
            [11, -1, -1, -1, -1, 11],
            [11, -1, -1, -1, -1, 11],
            [11, -1, -1, -1, -1, 11],
            [11, -1, -1, -1, -1, 11],
            [11, 11, 11, 11, 11, 11],
        ],
        name="lock_yellow",
        visible=True,
        collidable=False,
        tags=["lock_target", "req_11"],
    ),
    "lock_green": Sprite(
        pixels=[
            [14, 14, 14, 14, 14, 14],
            [14, -1, -1, -1, -1, 14],
            [14, -1, -1, -1, -1, 14],
            [14, -1, -1, -1, -1, 14],
            [14, -1, -1, -1, -1, 14],
            [14, 14, 14, 14, 14, 14],
        ],
        name="lock_green",
        visible=True,
        collidable=False,
        tags=["lock_target", "req_14"],
    ),
}

# ---------------------------------------------------------------------
# 2. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 2
PADDING_COLOR = 5
CELL_SIZE = 6
GRID_DIM = 8
PLAYFIELD_OFFSET = 8
HUD_ROW = 60
HUD_X_START = 8
HUD_X_END = 56
HUD_FILL_COLOR = 14
HUD_EMPTY_COLOR = 4
TINT_CYCLE = [2, 8, 11, 14]
LOCK_BY_REQ = {8: "lock_red", 11: "lock_yellow", 14: "lock_green"}


def _cell_pos(gx, gy):
    return (PLAYFIELD_OFFSET + CELL_SIZE * gx, PLAYFIELD_OFFSET + CELL_SIZE * gy)


def _row_marker_pos(r):
    return (1, PLAYFIELD_OFFSET + CELL_SIZE * r)


def _col_marker_pos(c):
    return (PLAYFIELD_OFFSET + CELL_SIZE * c, 1)


def _build_cells():
    return [
        sprites["cell"].clone().set_position(*_cell_pos(gx, gy))
        for gy in range(GRID_DIM)
        for gx in range(GRID_DIM)
    ]


def _build_row_markers():
    return [
        sprites["row_marker"].clone().set_position(*_row_marker_pos(r))
        for r in range(GRID_DIM)
    ]


def _build_col_markers():
    return [
        sprites["col_marker"].clone().set_position(*_col_marker_pos(c))
        for c in range(GRID_DIM)
    ]


def _build_lock(gx, gy, required):
    s = sprites[LOCK_BY_REQ[required]].clone().set_position(*_cell_pos(gx, gy))
    s.set_layer(1)
    return s


# ---------------------------------------------------------------------
# 3. LEVELS
# ---------------------------------------------------------------------

levels = [
    Level(
        sprites=_build_cells()
        + _build_row_markers()
        + [
            _build_lock(2, 2, 8),
            _build_lock(5, 4, 11),
            _build_lock(3, 6, 14),
        ],
        grid_size=(64, 64),
        data={"step_budget": 30},
    ),
    Level(
        sprites=_build_cells()
        + _build_row_markers()
        + _build_col_markers()
        + [
            _build_lock(1, 2, 8),
            _build_lock(1, 5, 14),
            _build_lock(4, 2, 11),
            _build_lock(6, 6, 14),
            _build_lock(3, 4, 8),
        ],
        grid_size=(64, 64),
        data={"step_budget": 60},
    ),
    Level(
        sprites=_build_cells()
        + _build_row_markers()
        + _build_col_markers()
        + [
            _build_lock(1, 2, 14),
            _build_lock(4, 2, 11),
            _build_lock(2, 6, 8),
            _build_lock(5, 5, 14),
            _build_lock(7, 7, 11),
            _build_lock(6, 6, 8),
            _build_lock(2, 3, 14),
        ],
        grid_size=(64, 64),
        data={"step_budget": 80},
    ),
]

# ---------------------------------------------------------------------
# 4. HUD
# ---------------------------------------------------------------------


class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int):
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_max(self, n: int) -> None:
        self.max_steps = n
        self.current_steps = n

    def set_current(self, n: int) -> None:
        self.current_steps = max(0, min(n, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        bar_width = HUD_X_END - HUD_X_START
        ratio = self.current_steps / self.max_steps
        filled = round(bar_width * ratio)
        for x in range(bar_width):
            color = HUD_FILL_COLOR if x < filled else HUD_EMPTY_COLOR
            frame[HUD_ROW, HUD_X_START + x] = color
        return frame


# ---------------------------------------------------------------------
# 5. GAME CLASS
# ---------------------------------------------------------------------


class Hl4n(NovaBaseGame):
    def __init__(self) -> None:
        self.row_tints = [BACKGROUND_COLOR] * GRID_DIM
        self.col_tints = [BACKGROUND_COLOR] * GRID_DIM
        self._cells_by_pos: dict[tuple[int, int], Sprite] = {}
        self.step_counter_hud = StepCounterHud(0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_counter_hud],
        )
        super().__init__(
            game_id="hl4n",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        self.row_tints = [BACKGROUND_COLOR] * GRID_DIM
        self.col_tints = [BACKGROUND_COLOR] * GRID_DIM
        budget = level.get_data("step_budget") or 30
        self.step_counter_hud.set_max(budget)
        self._cells_by_pos = {}
        for s in level.get_sprites_by_tag("cell"):
            gx = (s.x - PLAYFIELD_OFFSET) // CELL_SIZE
            gy = (s.y - PLAYFIELD_OFFSET) // CELL_SIZE
            self._cells_by_pos[(gx, gy)] = s
            s.pixels[:, :] = BACKGROUND_COLOR
        for m in level.get_sprites_by_tag("row_marker"):
            m.pixels[1:5, 1:5] = BACKGROUND_COLOR
        for m in level.get_sprites_by_tag("col_marker"):
            m.pixels[1:5, 1:5] = BACKGROUND_COLOR
        self._render_lock_state()

    def _cycle_next(self, current: int) -> int:
        if current in TINT_CYCLE:
            idx = TINT_CYCLE.index(current)
        else:
            idx = 0
        return TINT_CYCLE[(idx + 1) % len(TINT_CYCLE)]

    def _paint_marker(self, marker: Sprite, tint: int) -> None:
        marker.pixels[1:5, 1:5] = tint

    def _paint_row(self, r: int, tint: int) -> None:
        for (gx, gy), cell in self._cells_by_pos.items():
            if gy == r:
                cell.pixels[:, :] = tint

    def _paint_col(self, c: int, tint: int) -> None:
        for (gx, gy), cell in self._cells_by_pos.items():
            if gx == c:
                cell.pixels[:, :] = tint

    def _lock_required(self, lock: Sprite):
        for t in lock.tags:
            if t.startswith("req_"):
                return int(t.split("_", 1)[1])
        return None

    def _render_lock_state(self) -> None:
        for lock in self.current_level.get_sprites_by_tag("lock_target"):
            gx = (lock.x - PLAYFIELD_OFFSET) // CELL_SIZE
            gy = (lock.y - PLAYFIELD_OFFSET) // CELL_SIZE
            cell = self._cells_by_pos.get((gx, gy))
            if cell is None:
                continue
            req = self._lock_required(lock)
            if req is None:
                continue
            current = int(cell.pixels[0, 0])
            satisfied = current == req
            corner = 0 if satisfied else req
            lock.pixels[0, 0] = corner
            lock.pixels[0, CELL_SIZE - 1] = corner
            lock.pixels[CELL_SIZE - 1, 0] = corner
            lock.pixels[CELL_SIZE - 1, CELL_SIZE - 1] = corner

    def _check_win(self) -> bool:
        for lock in self.current_level.get_sprites_by_tag("lock_target"):
            gx = (lock.x - PLAYFIELD_OFFSET) // CELL_SIZE
            gy = (lock.y - PLAYFIELD_OFFSET) // CELL_SIZE
            cell = self._cells_by_pos.get((gx, gy))
            if cell is None:
                return False
            req = self._lock_required(lock)
            if req is None:
                return False
            if int(cell.pixels[0, 0]) != req:
                return False
        return True

    def step(self) -> None:
        remaining = max(0, self.step_counter_hud.max_steps - self._action_count)
        self.step_counter_hud.set_current(remaining)
        if self._action_count >= self.step_counter_hud.max_steps:
            self.lose()
            self.complete_action()
            return
        if self.action.id == GameAction.ACTION6:
            x = int(self.action.data["x"])
            y = int(self.action.data["y"])
            grid = self.camera.display_to_grid(x, y)
            if grid:
                gx, gy = grid
                clicked = self.current_level.get_sprite_at(gx, gy)
                if clicked is not None:
                    if "row_marker" in clicked.tags:
                        r = (clicked.y - PLAYFIELD_OFFSET) // CELL_SIZE
                        if 0 <= r < GRID_DIM:
                            self.row_tints[r] = self._cycle_next(self.row_tints[r])
                            self._paint_marker(clicked, self.row_tints[r])
                            self._paint_row(r, self.row_tints[r])
                            self._render_lock_state()
                            if self._check_win():
                                self.next_level()
                    elif "col_marker" in clicked.tags:
                        c = (clicked.x - PLAYFIELD_OFFSET) // CELL_SIZE
                        if 0 <= c < GRID_DIM:
                            self.col_tints[c] = self._cycle_next(self.col_tints[c])
                            self._paint_marker(clicked, self.col_tints[c])
                            self._paint_col(c, self.col_tints[c])
                            self._render_lock_state()
                            if self._check_win():
                                self.next_level()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self.step_counter_hud.current_steps
        for r in range(GRID_DIM):
            state[1, r % 4] = self.row_tints[r] if r < 4 else state[1, r % 4]
        return state

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()
