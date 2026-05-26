"""Generated game module."""

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

# Tile pixel templates: 8x8 px each. Each tile-kind has a distinguishing
# internal motif so the player can read the cell's role off the screen
# (the motif is preserved across the dark/lit colour variants).
#
# Rook: +-cross. Magenta lit, off-black ink dark.
# Bishop: X-cross. Light-blue lit, off-black ink dark.
# Tri-state: pink ring with a coloured centre encoding the state.

_ROOK_DARK = [
    [3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 4, 4, 3, 3, 3],
    [3, 3, 3, 4, 4, 3, 3, 3],
    [3, 4, 4, 4, 4, 4, 4, 3],
    [3, 4, 4, 4, 4, 4, 4, 3],
    [3, 3, 3, 4, 4, 3, 3, 3],
    [3, 3, 3, 4, 4, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3],
]

_ROOK_LIT = [
    [6, 6, 6, 6, 6, 6, 6, 6],
    [6, 6, 6, 4, 4, 6, 6, 6],
    [6, 6, 6, 4, 4, 6, 6, 6],
    [6, 4, 4, 4, 4, 4, 4, 6],
    [6, 4, 4, 4, 4, 4, 4, 6],
    [6, 6, 6, 4, 4, 6, 6, 6],
    [6, 6, 6, 4, 4, 6, 6, 6],
    [6, 6, 6, 6, 6, 6, 6, 6],
]

_BISHOP_DARK = [
    [3, 3, 3, 3, 3, 3, 3, 3],
    [3, 4, 3, 3, 3, 3, 4, 3],
    [3, 3, 4, 3, 3, 4, 3, 3],
    [3, 3, 3, 4, 4, 3, 3, 3],
    [3, 3, 3, 4, 4, 3, 3, 3],
    [3, 3, 4, 3, 3, 4, 3, 3],
    [3, 4, 3, 3, 3, 3, 4, 3],
    [3, 3, 3, 3, 3, 3, 3, 3],
]

_BISHOP_LIT = [
    [10, 10, 10, 10, 10, 10, 10, 10],
    [10, 4, 10, 10, 10, 10, 4, 10],
    [10, 10, 4, 10, 10, 4, 10, 10],
    [10, 10, 10, 4, 4, 10, 10, 10],
    [10, 10, 10, 4, 4, 10, 10, 10],
    [10, 10, 4, 10, 10, 4, 10, 10],
    [10, 4, 10, 10, 10, 10, 4, 10],
    [10, 10, 10, 10, 10, 10, 10, 10],
]


def _tristate_pixels(centre_color):
    """Build an 8x8 tri-state tile with the centre painted ``centre_color``.

    The pink ring (palette 7) and inner off-black border are constant; only
    the inner 4x4 centre block carries the state colour, so the ring's
    semantic identity is preserved across all three states.
    """
    c = centre_color
    return [
        [4, 7, 7, 7, 7, 7, 7, 4],
        [7, 7, 4, 4, 4, 4, 7, 7],
        [7, 4, c, c, c, c, 4, 7],
        [7, 4, c, c, c, c, 4, 7],
        [7, 4, c, c, c, c, 4, 7],
        [7, 4, c, c, c, c, 4, 7],
        [7, 7, 4, 4, 4, 4, 7, 7],
        [4, 7, 7, 7, 7, 7, 7, 4],
    ]


_TRISTATE_S0 = _tristate_pixels(2)   # state 0 = light-grey centre
_TRISTATE_S1 = _tristate_pixels(6)   # state 1 = magenta centre
_TRISTATE_S2 = _tristate_pixels(10)  # state 2 = light-blue centre


# 4x4 mini-tiles for the target-display mirror grid.

_TARGET_DARK = [
    [3, 3, 3, 3],
    [3, 4, 4, 3],
    [3, 4, 4, 3],
    [3, 3, 3, 3],
]

_TARGET_ROOK_LIT = [
    [4, 6, 6, 4],
    [6, 6, 6, 6],
    [6, 6, 6, 6],
    [4, 6, 6, 4],
]

_TARGET_BISHOP_LIT = [
    [4, 10, 10, 4],
    [10, 10, 10, 10],
    [10, 10, 10, 10],
    [4, 10, 10, 4],
]

_TARGET_TRI_S0 = [
    [7, 7, 7, 7],
    [7, 2, 2, 7],
    [7, 2, 2, 7],
    [7, 7, 7, 7],
]

_TARGET_TRI_S1 = [
    [7, 7, 7, 7],
    [7, 6, 6, 7],
    [7, 6, 6, 7],
    [7, 7, 7, 7],
]

_TARGET_TRI_S2 = [
    [7, 7, 7, 7],
    [7, 10, 10, 7],
    [7, 10, 10, 7],
    [7, 7, 7, 7],
]


# Pre-convert templates to numpy arrays once, so per-cell pixel updates
# are np.array.copy() rather than np.array(list).
_ROOK_DARK_NP = np.array(_ROOK_DARK, dtype=np.int16)
_ROOK_LIT_NP = np.array(_ROOK_LIT, dtype=np.int16)
_BISHOP_DARK_NP = np.array(_BISHOP_DARK, dtype=np.int16)
_BISHOP_LIT_NP = np.array(_BISHOP_LIT, dtype=np.int16)
_TRISTATE_NP = [
    np.array(_TRISTATE_S0, dtype=np.int16),
    np.array(_TRISTATE_S1, dtype=np.int16),
    np.array(_TRISTATE_S2, dtype=np.int16),
]
_TARGET_DARK_NP = np.array(_TARGET_DARK, dtype=np.int16)
_TARGET_ROOK_LIT_NP = np.array(_TARGET_ROOK_LIT, dtype=np.int16)
_TARGET_BISHOP_LIT_NP = np.array(_TARGET_BISHOP_LIT, dtype=np.int16)
_TARGET_TRI_NP = [
    np.array(_TARGET_TRI_S0, dtype=np.int16),
    np.array(_TARGET_TRI_S1, dtype=np.int16),
    np.array(_TARGET_TRI_S2, dtype=np.int16),
]


sprites = {
    "rook_template": Sprite(
        pixels=_ROOK_DARK,
        name="rook_template",
        visible=True,
        collidable=False,
        tags=["cell", "rook"],
    ),
    "bishop_template": Sprite(
        pixels=_BISHOP_DARK,
        name="bishop_template",
        visible=True,
        collidable=False,
        tags=["cell", "bishop"],
    ),
    "tristate_template": Sprite(
        pixels=_TRISTATE_S0,
        name="tristate_template",
        visible=True,
        collidable=False,
        tags=["cell", "tristate"],
    ),
    "target_template": Sprite(
        pixels=_TARGET_DARK,
        name="target_template",
        visible=True,
        collidable=False,
        tags=["target_cell"],
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

PLAYFIELD_X_OFFSET = 2
PLAYFIELD_Y_OFFSET = 2
CELL_PX = 8

TARGET_X_OFFSET = 44
TARGET_Y_OFFSET = 22
TARGET_PX = 4

GRID_W = 5
GRID_H = 5


def _all_cells():
    return [(c, r) for c in range(GRID_W) for r in range(GRID_H)]


# Per-level tile-kind partition. Cells absent from `bishop` and `tristate`
# default to `rook`.
_L1_BISHOP = []
_L1_TRISTATE = []
_L1_ROOK = _all_cells()

_L2_BISHOP = [(1, 1), (3, 3)]
_L2_TRISTATE = []
_L2_ROOK = [c for c in _all_cells() if c not in _L2_BISHOP]

_L3_BISHOP = [(1, 1), (3, 3)]
_L3_TRISTATE = [(2, 2)]
_L3_ROOK = [c for c in _all_cells()
            if c not in _L3_BISHOP and c not in _L3_TRISTATE]


# Target patterns: target[row][col]. Values 0/1 for binary cells; 2 only
# for the tri-state cell at (col=2, row=2) in level 3.

_L1_TARGET = [
    [0, 1, 0, 1, 0],
    [1, 1, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [1, 0, 1, 1, 1],
    [0, 1, 0, 1, 0],
]

_L2_TARGET = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
]

_L3_TARGET = [
    [0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1],
    [0, 0, 2, 0, 0],
    [1, 0, 0, 0, 1],
    [1, 1, 0, 1, 0],
]


def _build_level_sprites(rook_cells, bishop_cells, tristate_cells):
    """Construct the sprite list for one level.

    Each cell is a clone of the matching template, placed at the cell's
    pixel anchor in the playfield. The target-display mirror grid is the
    same 25 cells of mini-tiles, placed to the right of the playfield.
    """
    out = []
    for col, row in rook_cells:
        s = sprites["rook_template"].clone().set_position(
            PLAYFIELD_X_OFFSET + col * CELL_PX,
            PLAYFIELD_Y_OFFSET + row * CELL_PX,
        )
        out.append(s)
    for col, row in bishop_cells:
        s = sprites["bishop_template"].clone().set_position(
            PLAYFIELD_X_OFFSET + col * CELL_PX,
            PLAYFIELD_Y_OFFSET + row * CELL_PX,
        )
        out.append(s)
    for col, row in tristate_cells:
        s = sprites["tristate_template"].clone().set_position(
            PLAYFIELD_X_OFFSET + col * CELL_PX,
            PLAYFIELD_Y_OFFSET + row * CELL_PX,
        )
        out.append(s)
    for r in range(GRID_H):
        for c in range(GRID_W):
            s = sprites["target_template"].clone().set_position(
                TARGET_X_OFFSET + c * TARGET_PX,
                TARGET_Y_OFFSET + r * TARGET_PX,
            )
            out.append(s)
    return out


levels = [
    Level(
        sprites=_build_level_sprites(_L1_ROOK, _L1_BISHOP, _L1_TRISTATE),
        grid_size=(64, 64),
        data={"target": _L1_TARGET, "step_budget": 25},
    ),
    Level(
        sprites=_build_level_sprites(_L2_ROOK, _L2_BISHOP, _L2_TRISTATE),
        grid_size=(64, 64),
        data={"target": _L2_TARGET, "step_budget": 50},
    ),
    Level(
        sprites=_build_level_sprites(_L3_ROOK, _L3_BISHOP, _L3_TRISTATE),
        grid_size=(64, 64),
        data={"target": _L3_TARGET, "step_budget": 60},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 3
PADDING_COLOR = 3


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    """A single-row depleting bar painted on row 63.

    Filled (palette 6 magenta) on the left for the remaining-steps share;
    empty (palette 4 off-black) on the right. Re-armed via ``reset(...)``
    each level.
    """

    BAR_WIDTH = 60
    BAR_X_OFFSET = 2
    FILLED_COLOR = 6
    EMPTY_COLOR = 4

    def __init__(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.remaining = max_steps

    def reset(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.remaining = max_steps

    def set_remaining(self, remaining: int) -> None:
        self.remaining = max(0, min(remaining, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.remaining / self.max_steps
        filled = round(self.BAR_WIDTH * ratio)
        filled = max(0, min(filled, self.BAR_WIDTH))
        for x in range(self.BAR_WIDTH):
            color = self.FILLED_COLOR if x < filled else self.EMPTY_COLOR
            frame[63, self.BAR_X_OFFSET + x] = color
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------

class Qf8m(NovaBaseGame):
    def __init__(self) -> None:
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
        )
        self._step_counter_ui = StepCounterHud(max_steps=25)
        camera.replace_interface([self._step_counter_ui])
        self._cell_sprite: dict[tuple[int, int], Sprite] = {}
        self._cell_kind: dict[tuple[int, int], str] = {}
        self._cell_state: dict[tuple[int, int], int] = {}
        self._target_state: dict[tuple[int, int], int] = {}
        self._target_sprites: dict[tuple[int, int], Sprite] = {}
        self._max_steps: int = 25
        self._steps_remaining: int = 25
        super().__init__(
            game_id="qf8m",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        self._cell_sprite = {}
        self._cell_kind = {}
        self._cell_state = {}
        self._target_state = {}
        self._target_sprites = {}

        for sprite in level.get_sprites_by_tag("cell"):
            col = (sprite.x - PLAYFIELD_X_OFFSET) // CELL_PX
            row = (sprite.y - PLAYFIELD_Y_OFFSET) // CELL_PX
            if "rook" in sprite.tags:
                kind = "rook"
            elif "bishop" in sprite.tags:
                kind = "bishop"
            elif "tristate" in sprite.tags:
                kind = "tristate"
            else:
                continue
            self._cell_sprite[(col, row)] = sprite
            self._cell_kind[(col, row)] = kind
            self._cell_state[(col, row)] = 0
            self._update_cell_visual(col, row)

        for sprite in level.get_sprites_by_tag("target_cell"):
            col = (sprite.x - TARGET_X_OFFSET) // TARGET_PX
            row = (sprite.y - TARGET_Y_OFFSET) // TARGET_PX
            self._target_sprites[(col, row)] = sprite

        target_data = level.get_data("target")
        for row in range(GRID_H):
            for col in range(GRID_W):
                self._target_state[(col, row)] = int(target_data[row][col])
                if (col, row) in self._target_sprites:
                    self._update_target_visual(col, row)

        self._max_steps = int(level.get_data("step_budget"))
        self._steps_remaining = self._max_steps
        self._step_counter_ui.reset(self._max_steps)

    def _update_cell_visual(self, col: int, row: int) -> None:
        sprite = self._cell_sprite[(col, row)]
        kind = self._cell_kind[(col, row)]
        state = self._cell_state[(col, row)]
        if kind == "rook":
            new_pixels = _ROOK_LIT_NP if state == 1 else _ROOK_DARK_NP
        elif kind == "bishop":
            new_pixels = _BISHOP_LIT_NP if state == 1 else _BISHOP_DARK_NP
        else:
            new_pixels = _TRISTATE_NP[state]
        sprite.pixels = new_pixels.copy()

    def _update_target_visual(self, col: int, row: int) -> None:
        sprite = self._target_sprites[(col, row)]
        kind = self._cell_kind[(col, row)]
        state = self._target_state[(col, row)]
        if kind == "rook":
            new_pixels = (_TARGET_ROOK_LIT_NP if state == 1
                          else _TARGET_DARK_NP)
        elif kind == "bishop":
            new_pixels = (_TARGET_BISHOP_LIT_NP if state == 1
                          else _TARGET_DARK_NP)
        else:
            new_pixels = _TARGET_TRI_NP[state]
        sprite.pixels = new_pixels.copy()

    def _cycle_one(self, col: int, row: int) -> None:
        kind = self._cell_kind[(col, row)]
        if kind == "tristate":
            self._cell_state[(col, row)] = (self._cell_state[(col, row)] + 1) % 3
        else:
            self._cell_state[(col, row)] = (self._cell_state[(col, row)] + 1) % 2
        self._update_cell_visual(col, row)

    def _flip_rook(self, click_col: int, click_row: int) -> None:
        affected: set[tuple[int, int]] = set()
        for c in range(GRID_W):
            affected.add((c, click_row))
        for r in range(GRID_H):
            affected.add((click_col, r))
        for (c, r) in affected:
            self._cycle_one(c, r)

    def _flip_bishop(self, click_col: int, click_row: int) -> None:
        affected: set[tuple[int, int]] = set()
        for k in range(-max(GRID_W, GRID_H), max(GRID_W, GRID_H) + 1):
            c1 = click_col + k
            r1 = click_row + k
            if 0 <= c1 < GRID_W and 0 <= r1 < GRID_H:
                affected.add((c1, r1))
            c2 = click_col + k
            r2 = click_row - k
            if 0 <= c2 < GRID_W and 0 <= r2 < GRID_H:
                affected.add((c2, r2))
        for (c, r) in affected:
            self._cycle_one(c, r)

    def _handle_click(self, col: int, row: int) -> None:
        kind = self._cell_kind[(col, row)]
        if kind == "rook":
            self._flip_rook(col, row)
        elif kind == "bishop":
            self._flip_bishop(col, row)
        # Tri-state click is a no-op: the step is consumed by the caller
        # but no state changes anywhere on the grid.

    def _check_win(self) -> bool:
        for cell, state in self._cell_state.items():
            if self._target_state.get(cell, -1) != state:
                return False
        return True

    def step(self) -> None:
        consumed_step = False
        if self.action.id == GameAction.ACTION6:
            data = self.action.data or {}
            px = int(data.get("x", -1))
            py = int(data.get("y", -1))
            grid = self.camera.display_to_grid(px, py)
            if grid is not None:
                gx, gy = grid
                if (PLAYFIELD_X_OFFSET <= gx < PLAYFIELD_X_OFFSET + GRID_W * CELL_PX
                        and PLAYFIELD_Y_OFFSET <= gy < PLAYFIELD_Y_OFFSET + GRID_H * CELL_PX):
                    col = (gx - PLAYFIELD_X_OFFSET) // CELL_PX
                    row = (gy - PLAYFIELD_Y_OFFSET) // CELL_PX
                    if (col, row) in self._cell_kind:
                        self._handle_click(col, row)
                        consumed_step = True

        if consumed_step:
            self._steps_remaining -= 1
            self._step_counter_ui.set_remaining(self._steps_remaining)

        if self._check_win():
            self.next_level()
        elif self._steps_remaining <= 0:
            self.lose()

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((GRID_H, GRID_W), dtype=np.int16)
        for (col, row), state in self._cell_state.items():
            out[row, col] = state
        return out

    def _get_valid_actions(self) -> list[ActionInput]:
        actions: list[ActionInput] = []
        for col in range(GRID_W):
            for row in range(GRID_H):
                px = PLAYFIELD_X_OFFSET + col * CELL_PX + CELL_PX // 2
                py = PLAYFIELD_Y_OFFSET + row * CELL_PX + CELL_PX // 2
                actions.append(
                    ActionInput(
                        id=GameAction.ACTION6,
                        data={"x": px, "y": py},
                    )
                )
        return actions
