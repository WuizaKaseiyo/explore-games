"""vd3g — generated game."""

import numpy as np
from novaengine import (
    ActionInput,
    NovaBaseGame,
    BlockingMode,
    Camera,
    GameAction,
    Level,
    RenderableUserDisplay,
    Sprite,
)


# ---------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------

GRID_CELLS = 16
CELL_PIXELS = 4
FRAME_SIZE = GRID_CELLS * CELL_PIXELS  # 64

BACKGROUND_COLOR = 4
PADDING_COLOR = 4

# Cell-kind enum (per-cell typing held in self.cell_kind grid)
CELL_NORMAL = 0
CELL_WALL = 1
CELL_TARGET_RED = 2
CELL_TARGET_BLUE = 3
CELL_ANCHOR_MAGENTA = 5

# Cell heights
HEIGHT_LOW = 0
HEIGHT_HIGH = 1

# Pre-baked 4x4 cell pixel patterns (one logical cell of the playfield).
# Each pattern is multi-palette to satisfy the no-flat-coloured-blocks
# rule and give the player a clear visual read of the cell type.

PATTERN_LOW = np.array([
    [12, 11, 11, 12],
    [11,  1,  1, 11],
    [11,  1,  1, 11],
    [12, 11, 11, 12],
], dtype=np.int16)

PATTERN_HIGH = np.array([
    [4, 3, 3, 4],
    [3, 2, 2, 3],
    [3, 2, 2, 3],
    [4, 3, 3, 4],
], dtype=np.int16)

PATTERN_WALL = np.array([
    [5, 5, 5, 5],
    [5, 4, 4, 5],
    [5, 4, 4, 5],
    [5, 5, 5, 5],
], dtype=np.int16)

PATTERN_TARGET_RED = np.array([
    [8, 8, 8, 8],
    [8, 1, 1, 8],
    [8, 1, 1, 8],
    [8, 8, 8, 8],
], dtype=np.int16)

PATTERN_TARGET_BLUE = np.array([
    [9, 9, 9, 9],
    [9, 1, 1, 9],
    [9, 1, 1, 9],
    [9, 9, 9, 9],
], dtype=np.int16)

PATTERN_ANCHOR_LOW_MAGENTA = np.array([
    [ 6, 11, 11, 12],
    [11,  1,  1, 11],
    [11,  1,  1, 11],
    [12, 11, 11, 12],
], dtype=np.int16)

PATTERN_ANCHOR_HIGH_MAGENTA = np.array([
    [6, 3, 3, 4],
    [3, 2, 2, 3],
    [3, 2, 2, 3],
    [4, 3, 3, 4],
], dtype=np.int16)

# Settling priority: cardinal neighbours in N -> E -> S -> W order.
PRIORITY_DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


# ---------------------------------------------------------------------
# SPRITE BANK
# ---------------------------------------------------------------------

def _initial_terrain_pixels():
    """Build a 64x64 placeholder terrain pixel array (all HIGH cells).

    The actual per-level terrain is painted in `on_set_level` via
    `_repaint_terrain`; this constructor-time array exists so the
    Sprite has a valid pixel buffer at import time.
    """
    arr = np.zeros((FRAME_SIZE, FRAME_SIZE), dtype=np.int16)
    for cy in range(GRID_CELLS):
        for cx in range(GRID_CELLS):
            arr[cy * CELL_PIXELS:(cy + 1) * CELL_PIXELS,
                cx * CELL_PIXELS:(cx + 1) * CELL_PIXELS] = PATTERN_HIGH
    return arr.tolist()


sprites = {
    "terrain": Sprite(
        pixels=_initial_terrain_pixels(),
        name="terrain",
        visible=True,
        collidable=False,
        blocking=BlockingMode.NOT_BLOCKED,
        tags=["terrain"],
        layer=0,
    ),
    "marble_blue": Sprite(
        pixels=[
            [-1, 9, 9, -1],
            [ 9, 1, 9,  9],
            [ 9, 9, 9,  9],
            [-1, 9, 9, -1],
        ],
        name="marble_blue",
        visible=True,
        collidable=False,
        blocking=BlockingMode.NOT_BLOCKED,
        tags=["marble", "marble_blue"],
        layer=2,
    ),
    "marble_red": Sprite(
        pixels=[
            [-1, 8, 8, -1],
            [ 8, 1, 8,  8],
            [ 8, 8, 8,  8],
            [-1, 8, 8, -1],
        ],
        name="marble_red",
        visible=True,
        collidable=False,
        blocking=BlockingMode.NOT_BLOCKED,
        tags=["marble", "marble_red"],
        layer=2,
    ),
}


# ---------------------------------------------------------------------
# LEVEL LAYOUTS
# ---------------------------------------------------------------------
#
# Each layout is a 16-row list of 16-character strings.
# Character codes:
#   '.' = NORMAL HIGH cell (toggleable)
#   'W' = WALL (immutable, marbles never enter)
#   'r' = TARGET-RED (immutable LOW; red ring around cream interior)
#   'b' = TARGET-BLUE (immutable LOW; blue ring around cream interior)
#   'A' / 'B' = ANCHOR cell (toggleable; paired with another anchor)
#
# Anchor pairs are declared separately in `level.data["anchor_pairs"]`
# as a list of `((col_a, row_a), (col_b, row_b))` tuples.

LEVEL_1_LAYOUT = [
    "WWWWWWWWWWWWWWWW",
    "W..............W",
    "W..............W",
    "W..............W",
    "W..............W",
    "W..............W",
    "W..............W",
    "W..............W",
    "W..............W",
    "W....r.........W",
    "W..............W",
    "W..............W",
    "W..............W",
    "W..............W",
    "W..............W",
    "WWWWWWWWWWWWWWWW",
]

LEVEL_2_LAYOUT = [
    "WWWWWWWWWWWWWWWW",
    "W......W.......W",
    "W......W.......W",
    "W......W.......W",
    "W......W....r..W",
    "W......W.......W",
    "W......W.......W",
    "W......W.......W",
    "W..............W",
    "W......W.......W",
    "W......W.......W",
    "W......W.......W",
    "W......W.......W",
    "W......W.......W",
    "W......W.......W",
    "WWWWWWWWWWWWWWWW",
]

LEVEL_3_LAYOUT = [
    "WWWWWWWWWWWWWWWW",
    "W.......W......W",
    "W.......W......W",
    "W.......W......W",
    "W.......W......W",
    "W.......W......W",
    "W.......A...r..W",
    "W.......W......W",
    "W.......W......W",
    "W..b....B......W",
    "W.......W......W",
    "W.......W......W",
    "W.......W......W",
    "W.......W......W",
    "W.......W......W",
    "WWWWWWWWWWWWWWWW",
]


# ---------------------------------------------------------------------
# LEVELS
# ---------------------------------------------------------------------

levels = [
    # Level 1: marble red at (5, 5), target red at (5, 9).
    Level(
        sprites=[
            sprites["terrain"].clone(),
            sprites["marble_red"].clone().set_position(
                5 * CELL_PIXELS, 5 * CELL_PIXELS
            ),
        ],
        grid_size=(FRAME_SIZE, FRAME_SIZE),
        data={
            "layout": LEVEL_1_LAYOUT,
            "anchor_pairs": [],
            "max_steps": 16,
        },
    ),
    # Level 2: marble red at (3, 4), target red at (12, 4).
    Level(
        sprites=[
            sprites["terrain"].clone(),
            sprites["marble_red"].clone().set_position(
                3 * CELL_PIXELS, 4 * CELL_PIXELS
            ),
        ],
        grid_size=(FRAME_SIZE, FRAME_SIZE),
        data={
            "layout": LEVEL_2_LAYOUT,
            "anchor_pairs": [],
            "max_steps": 50,
        },
    ),
    # Level 3: marble red at (3, 6), marble blue at (12, 9);
    #          target red at (12, 6), target blue at (3, 9);
    #          anchor pair at (8, 6) <-> (8, 9).
    Level(
        sprites=[
            sprites["terrain"].clone(),
            sprites["marble_red"].clone().set_position(
                3 * CELL_PIXELS, 6 * CELL_PIXELS
            ),
            sprites["marble_blue"].clone().set_position(
                12 * CELL_PIXELS, 9 * CELL_PIXELS
            ),
        ],
        grid_size=(FRAME_SIZE, FRAME_SIZE),
        data={
            "layout": LEVEL_3_LAYOUT,
            "anchor_pairs": [((8, 6), (8, 9))],
            "max_steps": 80,
        },
    ),
]


# ---------------------------------------------------------------------
# HUD WIDGET
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    """Top-row depleting bar showing the remaining step budget."""

    def __init__(self, max_steps: int = 0) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps
        super().__init__()

    def set_max(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_current(self, current: int) -> None:
        self.current_steps = max(0, min(current, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.current_steps / self.max_steps
        filled = int(round(FRAME_SIZE * ratio))
        for x in range(FRAME_SIZE):
            if x < filled:
                frame[0, x] = 14
            else:
                frame[0, x] = 4
        return frame


# ---------------------------------------------------------------------
# THE GAME
# ---------------------------------------------------------------------

class Vd3g(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_ui = StepCounterHud()
        # Per-level state attributes — declared BEFORE super().__init__()
        # because the engine's __init__ calls set_level(0), which triggers
        # on_set_level, which expects these attributes to be writable.
        self.heights: np.ndarray = np.zeros(
            (GRID_CELLS, GRID_CELLS), dtype=np.int8
        )
        self.cell_kind: np.ndarray = np.zeros(
            (GRID_CELLS, GRID_CELLS), dtype=np.int8
        )
        self.anchor_pairs: dict = {}
        self.marble_targets: dict = {}
        self.max_steps: int = 0
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        super().__init__(
            game_id="vd3g",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    # -----------------------------------------------------------------
    # Level setup
    # -----------------------------------------------------------------

    def on_set_level(self, level: Level) -> None:
        # Camera viewport matches level grid_size for correct scale.
        gw, gh = level.grid_size or (FRAME_SIZE, FRAME_SIZE)
        self.camera.width = gw
        self.camera.height = gh

        layout = level.get_data("layout")
        self.max_steps = int(level.get_data("max_steps") or 0)
        self._step_counter_ui.set_max(self.max_steps)
        anchor_data = level.get_data("anchor_pairs") or []

        self.heights = np.full(
            (GRID_CELLS, GRID_CELLS), HEIGHT_HIGH, dtype=np.int8
        )
        self.cell_kind = np.full(
            (GRID_CELLS, GRID_CELLS), CELL_NORMAL, dtype=np.int8
        )
        self.anchor_pairs = {}
        self.marble_targets = {}

        for row in range(GRID_CELLS):
            line = layout[row]
            for col in range(GRID_CELLS):
                ch = line[col]
                if ch == "W":
                    self.cell_kind[row, col] = CELL_WALL
                    self.heights[row, col] = HEIGHT_HIGH
                elif ch == "r":
                    self.cell_kind[row, col] = CELL_TARGET_RED
                    self.heights[row, col] = HEIGHT_LOW
                elif ch == "b":
                    self.cell_kind[row, col] = CELL_TARGET_BLUE
                    self.heights[row, col] = HEIGHT_LOW
                elif ch in ("A", "B"):
                    self.cell_kind[row, col] = CELL_ANCHOR_MAGENTA
                    self.heights[row, col] = HEIGHT_HIGH
                else:
                    self.cell_kind[row, col] = CELL_NORMAL
                    self.heights[row, col] = HEIGHT_HIGH

        for (ax, ay), (bx, by) in anchor_data:
            self.anchor_pairs[(ax, ay)] = (bx, by)
            self.anchor_pairs[(bx, by)] = (ax, ay)

        # Map each marble to its target cell by colour-tag matching.
        marbles = level.get_sprites_by_tag("marble")
        for marble in marbles:
            if "marble_red" in marble.tags:
                tcell = self._find_target_cell(CELL_TARGET_RED)
            elif "marble_blue" in marble.tags:
                tcell = self._find_target_cell(CELL_TARGET_BLUE)
            else:
                tcell = None
            if tcell is not None:
                self.marble_targets[marble.name] = tcell

        self._repaint_terrain()

    # -----------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------

    def _find_target_cell(self, kind_value: int):
        ys, xs = np.where(self.cell_kind == kind_value)
        if len(xs) == 0:
            return None
        return (int(xs[0]), int(ys[0]))

    def _cell_pattern(self, kind_value: int, height: int) -> np.ndarray:
        if kind_value == CELL_WALL:
            return PATTERN_WALL
        if kind_value == CELL_TARGET_RED:
            return PATTERN_TARGET_RED
        if kind_value == CELL_TARGET_BLUE:
            return PATTERN_TARGET_BLUE
        if kind_value == CELL_ANCHOR_MAGENTA:
            if height == HEIGHT_LOW:
                return PATTERN_ANCHOR_LOW_MAGENTA
            return PATTERN_ANCHOR_HIGH_MAGENTA
        if height == HEIGHT_LOW:
            return PATTERN_LOW
        return PATTERN_HIGH

    def _repaint_terrain(self) -> None:
        terrain_sprites = self.current_level.get_sprites_by_tag("terrain")
        if not terrain_sprites:
            return
        terrain = terrain_sprites[0]
        new_pixels = np.zeros((FRAME_SIZE, FRAME_SIZE), dtype=np.int16)
        for cy in range(GRID_CELLS):
            for cx in range(GRID_CELLS):
                pat = self._cell_pattern(
                    int(self.cell_kind[cy, cx]),
                    int(self.heights[cy, cx]),
                )
                new_pixels[
                    cy * CELL_PIXELS:(cy + 1) * CELL_PIXELS,
                    cx * CELL_PIXELS:(cx + 1) * CELL_PIXELS,
                ] = pat
        terrain.pixels = new_pixels

    def _toggle_cell(self, cx: int, cy: int) -> None:
        if not (0 <= cx < GRID_CELLS and 0 <= cy < GRID_CELLS):
            return
        kind = int(self.cell_kind[cy, cx])
        if kind != CELL_NORMAL and kind != CELL_ANCHOR_MAGENTA:
            return
        self.heights[cy, cx] = (
            HEIGHT_HIGH if self.heights[cy, cx] == HEIGHT_LOW else HEIGHT_LOW
        )
        if kind == CELL_ANCHOR_MAGENTA:
            partner = self.anchor_pairs.get((cx, cy))
            if partner is not None:
                px, py = partner
                self.heights[py, px] = (
                    HEIGHT_HIGH
                    if self.heights[py, px] == HEIGHT_LOW
                    else HEIGHT_LOW
                )

    def _settling_pass(self) -> None:
        marbles = self.current_level.get_sprites_by_tag("marble")
        marbles = sorted(marbles, key=lambda m: m.name)

        occupied = {
            (m.x // CELL_PIXELS, m.y // CELL_PIXELS) for m in marbles
        }

        for marble in marbles:
            cx = marble.x // CELL_PIXELS
            cy = marble.y // CELL_PIXELS
            target = self.marble_targets.get(marble.name)
            if target is not None and (cx, cy) == target:
                continue
            if int(self.heights[cy, cx]) == HEIGHT_LOW:
                continue
            for dx, dy in PRIORITY_DIRS:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < GRID_CELLS and 0 <= ny < GRID_CELLS):
                    continue
                if int(self.cell_kind[ny, nx]) == CELL_WALL:
                    continue
                if int(self.heights[ny, nx]) != HEIGHT_LOW:
                    continue
                if (nx, ny) in occupied:
                    continue
                occupied.discard((cx, cy))
                occupied.add((nx, ny))
                marble.set_position(nx * CELL_PIXELS, ny * CELL_PIXELS)
                break

    def _check_win(self) -> bool:
        marbles = self.current_level.get_sprites_by_tag("marble")
        for marble in marbles:
            cx = marble.x // CELL_PIXELS
            cy = marble.y // CELL_PIXELS
            target = self.marble_targets.get(marble.name)
            if target is None or (cx, cy) != target:
                return False
        return True

    # -----------------------------------------------------------------
    # Step
    # -----------------------------------------------------------------

    def step(self) -> None:
        self._step_counter_ui.set_current(
            self.max_steps - self._action_count
        )
        if self._action_count >= self.max_steps:
            self.lose()
            self.complete_action()
            return

        if self.action.id == GameAction.ACTION6:
            x = self.action.data.get("x", 0)
            y = self.action.data.get("y", 0)
            grid = self.camera.display_to_grid(int(x), int(y))
            if grid is not None:
                gx, gy = grid
                cx = int(gx) // CELL_PIXELS
                cy = int(gy) // CELL_PIXELS
                self._toggle_cell(cx, cy)
            self._settling_pass()
            self._repaint_terrain()
            if self._check_win():
                self.next_level()

        self.complete_action()

    # -----------------------------------------------------------------
    # Hidden state (for engine introspection)
    # -----------------------------------------------------------------

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((4, 4), dtype=np.int16)
        out[0, 0] = self.max_steps - self._action_count
        return out

    def _get_valid_actions(self):
        return super()._get_valid_actions()
