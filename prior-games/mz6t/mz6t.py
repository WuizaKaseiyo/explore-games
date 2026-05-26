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

# Voting cells are 8x8 px tiles. Each colour state has a distinguishing
# motif (solid disc / hollow ring / plus-sign) so the cell's role reads
# from shape, not just colour.

_VOTE_LB = [
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 10, 10, 10, 10, 4, 4],
    [4, 10, 10, 10, 10, 10, 10, 4],
    [4, 10, 10, 10, 10, 10, 10, 4],
    [4, 10, 10, 10, 10, 10, 10, 4],
    [4, 10, 10, 10, 10, 10, 10, 4],
    [4, 4, 10, 10, 10, 10, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
]
_VOTE_OR = [
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 12, 12, 12, 12, 4, 4],
    [4, 12, 12, 4, 4, 12, 12, 4],
    [4, 12, 4, 4, 4, 4, 12, 4],
    [4, 12, 4, 4, 4, 4, 12, 4],
    [4, 12, 12, 4, 4, 12, 12, 4],
    [4, 4, 12, 12, 12, 12, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
]
_VOTE_PK = [
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 7, 7, 4, 4, 4],
    [4, 4, 4, 7, 7, 4, 4, 4],
    [4, 7, 7, 7, 7, 7, 7, 4],
    [4, 7, 7, 7, 7, 7, 7, 4],
    [4, 4, 4, 7, 7, 4, 4, 4],
    [4, 4, 4, 7, 7, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
]

_WALL_TILE = [
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 13, 13, 4, 4, 13, 13, 4],
    [4, 13, 13, 13, 13, 13, 13, 4],
    [4, 4, 13, 13, 13, 13, 4, 4],
    [4, 4, 13, 13, 13, 13, 4, 4],
    [4, 13, 13, 13, 13, 13, 13, 4],
    [4, 13, 13, 4, 4, 13, 13, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
]


def _anchor_pixels(base_pixels, pip_color):
    """Build an anchor variant by replacing the 4 outer corners of base."""
    out = [row[:] for row in base_pixels]
    out[0][0] = pip_color
    out[0][7] = pip_color
    out[7][0] = pip_color
    out[7][7] = pip_color
    return out


_ANCHOR_ARMED_LB = _anchor_pixels(_VOTE_LB, 5)
_ANCHOR_ARMED_OR = _anchor_pixels(_VOTE_OR, 5)
_ANCHOR_ARMED_PK = _anchor_pixels(_VOTE_PK, 5)
_ANCHOR_LOCKED_LB = _anchor_pixels(_VOTE_LB, 14)
_ANCHOR_LOCKED_OR = _anchor_pixels(_VOTE_OR, 14)
_ANCHOR_LOCKED_PK = _anchor_pixels(_VOTE_PK, 14)


# Pre-converted numpy arrays for fast per-state assignment.
_VOTE_NP = [
    np.array(_VOTE_LB, dtype=np.int16),
    np.array(_VOTE_OR, dtype=np.int16),
    np.array(_VOTE_PK, dtype=np.int16),
]
_ANCHOR_ARMED_NP = [
    np.array(_ANCHOR_ARMED_LB, dtype=np.int16),
    np.array(_ANCHOR_ARMED_OR, dtype=np.int16),
    np.array(_ANCHOR_ARMED_PK, dtype=np.int16),
]
_ANCHOR_LOCKED_NP = [
    np.array(_ANCHOR_LOCKED_LB, dtype=np.int16),
    np.array(_ANCHOR_LOCKED_OR, dtype=np.int16),
    np.array(_ANCHOR_LOCKED_PK, dtype=np.int16),
]


sprites = {
    "vote_cell": Sprite(
        pixels=_VOTE_LB,
        name="vote_cell",
        visible=True,
        collidable=False,
        tags=["voter"],
    ),
    "wall_cell": Sprite(
        pixels=_WALL_TILE,
        name="wall_cell",
        visible=True,
        collidable=False,
        tags=["wall"],
    ),
    "anchor_cell": Sprite(
        pixels=_ANCHOR_ARMED_LB,
        name="anchor_cell",
        visible=True,
        collidable=False,
        tags=["voter", "anchor"],
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

PLAYFIELD_X = 2
PLAYFIELD_Y = 2
CELL_PX = 8
GRID_W = 5
GRID_H = 5

TARGET_X = 44
TARGET_Y = 13
TARGET_PX = 3


# 5x5 cell-state arrays. Walls are listed separately in walls=[...].
# At wall positions the values in initial/target arrays are filler (ignored).

_L1_INITIAL = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]
_L1_TARGET = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]
_L1_WALLS = []
_L1_ANCHORS = {}
_L1_BUDGET = 25


_L2_INITIAL = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
_L2_TARGET = [
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
]
_L2_WALLS = [(1, 1), (3, 1), (1, 3), (3, 3)]
_L2_ANCHORS = {}
_L2_BUDGET = 30


_L3_INITIAL = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]
_L3_TARGET = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 2, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
_L3_WALLS = [(1, 1), (3, 1), (1, 3), (3, 3)]
_L3_ANCHORS = {(2, 2): 2}
_L3_BUDGET = 35


def _build_level_sprites(walls, anchors):
    """Place sprites for one level.

    Voting cells go at non-wall non-anchor positions; wall cells at wall
    positions; anchor cells at anchor positions. The target panel is
    rendered by TargetPanelHud, not via sprites.
    """
    out = []
    wall_set = set(walls)
    anchor_set = set(anchors.keys())
    for col in range(GRID_W):
        for row in range(GRID_H):
            x = PLAYFIELD_X + col * CELL_PX
            y = PLAYFIELD_Y + row * CELL_PX
            if (col, row) in wall_set:
                s = sprites["wall_cell"].clone()
            elif (col, row) in anchor_set:
                s = sprites["anchor_cell"].clone()
            else:
                s = sprites["vote_cell"].clone()
            s.set_position(x, y)
            out.append(s)
    return out


levels = [
    Level(
        sprites=_build_level_sprites(_L1_WALLS, _L1_ANCHORS),
        grid_size=(64, 64),
        data={
            "initial": _L1_INITIAL,
            "target": _L1_TARGET,
            "walls": _L1_WALLS,
            "anchors": _L1_ANCHORS,
            "step_budget": _L1_BUDGET,
        },
    ),
    Level(
        sprites=_build_level_sprites(_L2_WALLS, _L2_ANCHORS),
        grid_size=(64, 64),
        data={
            "initial": _L2_INITIAL,
            "target": _L2_TARGET,
            "walls": _L2_WALLS,
            "anchors": _L2_ANCHORS,
            "step_budget": _L2_BUDGET,
        },
    ),
    Level(
        sprites=_build_level_sprites(_L3_WALLS, _L3_ANCHORS),
        grid_size=(64, 64),
        data={
            "initial": _L3_INITIAL,
            "target": _L3_TARGET,
            "walls": _L3_WALLS,
            "anchors": _L3_ANCHORS,
            "step_budget": _L3_BUDGET,
        },
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 4
PADDING_COLOR = 4


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    """Horizontal bar painted on row 62 showing remaining steps."""

    BAR_WIDTH = 60
    BAR_X = 2
    BAR_Y = 62
    FILLED_COLOR = 12
    EMPTY_COLOR = 5

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
            frame[self.BAR_Y, self.BAR_X + x] = color
        return frame


# Quarter-scale (3x3) target tile palettes.
_TARGET_LB = [[4, 10, 4], [10, 10, 10], [4, 10, 4]]
_TARGET_OR = [[12, 12, 12], [12, 4, 12], [12, 12, 12]]
_TARGET_PK = [[4, 7, 4], [7, 7, 7], [4, 7, 4]]
_TARGET_WALL = [[13, 13, 13], [13, 4, 13], [13, 13, 13]]
_TARGET_ANCHOR_LB = [[5, 10, 5], [10, 10, 10], [5, 10, 5]]
_TARGET_ANCHOR_OR = [[5, 12, 5], [12, 4, 12], [5, 12, 5]]
_TARGET_ANCHOR_PK = [[5, 7, 5], [7, 7, 7], [5, 7, 5]]

_TARGET_BY_STATE = [_TARGET_LB, _TARGET_OR, _TARGET_PK]
_TARGET_ANCHOR_BY_STATE = [_TARGET_ANCHOR_LB, _TARGET_ANCHOR_OR, _TARGET_ANCHOR_PK]


class TargetPanelHud(RenderableUserDisplay):
    """Render the per-level target panel as a 5x5 mosaic of 3x3 mini-tiles
    at top-left pixel (44, 13)."""

    PANEL_X = 44
    PANEL_Y = 13
    MINI_PX = 3

    def __init__(self) -> None:
        self._target = None
        self._walls: set = set()
        self._anchors: dict = {}

    def reset(self, target_grid, walls, anchors) -> None:
        self._target = target_grid
        self._walls = set(tuple(w) for w in walls)
        self._anchors = dict(anchors)

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self._target is None:
            return frame
        for row in range(GRID_H):
            for col in range(GRID_W):
                if (col, row) in self._walls:
                    pixels = _TARGET_WALL
                elif (col, row) in self._anchors:
                    target_state = int(self._anchors[(col, row)])
                    pixels = _TARGET_ANCHOR_BY_STATE[target_state]
                else:
                    target_state = int(self._target[row][col])
                    pixels = _TARGET_BY_STATE[target_state]
                px_x = self.PANEL_X + col * self.MINI_PX
                px_y = self.PANEL_Y + row * self.MINI_PX
                for dy in range(self.MINI_PX):
                    for dx in range(self.MINI_PX):
                        frame[px_y + dy, px_x + dx] = pixels[dy][dx]
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------

class Mz6t(NovaBaseGame):
    def __init__(self) -> None:
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
        )
        self._step_counter_ui = StepCounterHud(max_steps=25)
        self._target_panel_ui = TargetPanelHud()
        camera.replace_interface([self._step_counter_ui, self._target_panel_ui])

        # per-level state
        self._cell_sprite: dict = {}
        self._cell_state: dict = {}
        self._is_wall: set = set()
        self._is_anchor: set = set()
        self._anchor_target: dict = {}
        self._anchor_locked: set = set()
        self._target_state: dict = {}
        self._max_steps: int = 25
        self._steps_used: int = 0

        super().__init__(
            game_id="mz6t",
            levels=levels,
            camera=camera,
            available_actions=[5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        self._cell_sprite = {}
        self._cell_state = {}
        self._is_wall = set()
        self._is_anchor = set()
        self._anchor_target = {}
        self._anchor_locked = set()
        self._target_state = {}
        self._steps_used = 0

        walls = level.get_data("walls") or []
        anchors = level.get_data("anchors") or {}
        initial = level.get_data("initial")
        target = level.get_data("target")

        self._is_wall = set(tuple(w) for w in walls)
        self._is_anchor = set(anchors.keys())
        self._anchor_target = {tuple(k): int(v) for k, v in anchors.items()}

        # Map placed sprites back to (col, row).
        for sprite in level.get_sprites():
            col = (sprite.x - PLAYFIELD_X) // CELL_PX
            row = (sprite.y - PLAYFIELD_Y) // CELL_PX
            if 0 <= col < GRID_W and 0 <= row < GRID_H:
                self._cell_sprite[(col, row)] = sprite

        # Set initial states for non-wall cells.
        for col in range(GRID_W):
            for row in range(GRID_H):
                if (col, row) in self._is_wall:
                    continue
                state = int(initial[row][col])
                self._cell_state[(col, row)] = state
                self._target_state[(col, row)] = int(target[row][col])
                self._update_cell_visual(col, row)

        # Lock any anchors whose initial state already matches their target.
        for cell in list(self._is_anchor):
            if self._cell_state.get(cell) == self._anchor_target[cell]:
                self._anchor_locked.add(cell)
                self._update_cell_visual(*cell)

        self._max_steps = int(level.get_data("step_budget"))
        self._steps_used = 0
        self._step_counter_ui.reset(self._max_steps)
        self._target_panel_ui.reset(target, walls, anchors)

    def _update_cell_visual(self, col: int, row: int) -> None:
        sprite = self._cell_sprite.get((col, row))
        if sprite is None:
            return
        if (col, row) in self._is_wall:
            return
        state = self._cell_state[(col, row)]
        if (col, row) in self._is_anchor:
            if (col, row) in self._anchor_locked:
                new_pixels = _ANCHOR_LOCKED_NP[state]
            else:
                new_pixels = _ANCHOR_ARMED_NP[state]
        else:
            new_pixels = _VOTE_NP[state]
        sprite.pixels = new_pixels.copy()

    def _check_anchor_lock(self, cell) -> None:
        if cell not in self._is_anchor:
            return
        if cell in self._anchor_locked:
            return
        if self._cell_state[cell] == self._anchor_target[cell]:
            self._anchor_locked.add(cell)
            self._update_cell_visual(*cell)

    def _handle_click(self, gx: int, gy: int) -> bool:
        """Return True if the click consumed a step."""
        if not (PLAYFIELD_X <= gx < PLAYFIELD_X + GRID_W * CELL_PX):
            return False
        if not (PLAYFIELD_Y <= gy < PLAYFIELD_Y + GRID_H * CELL_PX):
            return False
        col = (gx - PLAYFIELD_X) // CELL_PX
        row = (gy - PLAYFIELD_Y) // CELL_PX
        cell = (col, row)
        if cell in self._is_wall:
            return True
        if cell in self._anchor_locked:
            return True
        self._cell_state[cell] = (self._cell_state[cell] + 1) % 3
        self._update_cell_visual(col, row)
        self._check_anchor_lock(cell)
        return True

    def _apply_tick(self) -> None:
        """Apply one synchronous majority-vote tick.

        Walls don't vote (excluded from neighbour counts) and aren't voted
        on (immutable). Locked anchors don't get voted on but their colour
        still contributes to neighbours' counts.
        """
        old_state = dict(self._cell_state)
        new_state = dict(old_state)
        for col in range(GRID_W):
            for row in range(GRID_H):
                cell = (col, row)
                if cell in self._is_wall:
                    continue
                if cell in self._anchor_locked:
                    continue
                counts = [0, 0, 0]
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nc, nr = col + dx, row + dy
                    if not (0 <= nc < GRID_W and 0 <= nr < GRID_H):
                        continue
                    if (nc, nr) in self._is_wall:
                        continue
                    counts[old_state[(nc, nr)]] += 1
                new = old_state[cell]
                for c in range(3):
                    if counts[c] >= 3:
                        new = c
                        break
                new_state[cell] = new
        for cell, new in new_state.items():
            if old_state[cell] != new:
                self._cell_state[cell] = new
                self._update_cell_visual(*cell)
                self._check_anchor_lock(cell)

    def _check_win(self) -> bool:
        for cell, state in self._cell_state.items():
            if cell in self._is_wall:
                continue
            target = self._target_state.get(cell)
            if target is None:
                continue
            if state != target:
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
                consumed_step = self._handle_click(gx, gy)
        elif self.action.id == GameAction.ACTION5:
            self._apply_tick()
            consumed_step = True

        if consumed_step:
            self._steps_used += 1
            self._step_counter_ui.set_remaining(self._max_steps - self._steps_used)

        if self.action.id == GameAction.ACTION5 and self._check_win():
            self.next_level()
            self.complete_action()
            return

        if self._steps_used >= self._max_steps:
            self.lose()
            self.complete_action()
            return

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((GRID_H, GRID_W), dtype=np.int16)
        for col in range(GRID_W):
            for row in range(GRID_H):
                cell = (col, row)
                if cell in self._is_wall:
                    out[row, col] = -1
                elif cell in self._anchor_locked:
                    out[row, col] = self._cell_state[cell] + 10
                else:
                    out[row, col] = self._cell_state[cell]
        return out

    def _get_valid_actions(self) -> list:
        return super()._get_valid_actions()
