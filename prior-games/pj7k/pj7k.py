"""pj7k — generated game module."""

from typing import Dict, Optional, Set, Tuple

import numpy as np
from novaengine import (
    NovaBaseGame,
    BlockingMode,
    Camera,
    GameAction,
    Level,
    RenderableUserDisplay,
    Sprite,
)


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------
STRIDE = 4

YELLOW = 11
BLUE = 9
GREEN = 14
RED = 8
PURPLE = 15
ORANGE = 12
WALL_COLOUR = 4

INITIAL_FACES: Dict[str, int] = {
    "top": YELLOW,
    "bottom": BLUE,
    "front": GREEN,
    "back": RED,
    "left": PURPLE,
    "right": ORANGE,
}

BACKGROUND_COLOR = 1
PADDING_COLOR = 1
BAR_FILL = 14
BAR_EMPTY = 0

COLOUR_NAMES: Dict[int, str] = {
    YELLOW: "yellow",
    BLUE: "blue",
    GREEN: "green",
    RED: "red",
    PURPLE: "purple",
    ORANGE: "orange",
}
NAME_TO_COLOUR: Dict[str, int] = {v: k for k, v in COLOUR_NAMES.items()}


# ---------------------------------------------------------------------
# Sprite factory helpers
# ---------------------------------------------------------------------
def _make_target_sprite(colour: int) -> Sprite:
    c = colour
    name = f"target_{COLOUR_NAMES[colour]}"
    return Sprite(
        pixels=[
            [c, c, c],
            [c, -1, c],
            [c, c, c],
        ],
        name=name,
        visible=True,
        collidable=True,
        blocking=BlockingMode.NOT_BLOCKED,
        tags=["target", name],
        layer=1,
    )


def _make_paint_sprite(colour: int, suffix: str) -> Sprite:
    c = colour
    name = f"paint_{COLOUR_NAMES[colour]}_{suffix}"
    return Sprite(
        pixels=[
            [c, c, c],
            [c, c, c],
            [c, c, c],
        ],
        name=name,
        visible=True,
        collidable=False,
        blocking=BlockingMode.NOT_BLOCKED,
        tags=["paint", f"paint_{COLOUR_NAMES[colour]}"],
        layer=-1,
    )


def _make_wall_sprite(suffix: str) -> Sprite:
    return Sprite(
        pixels=[
            [WALL_COLOUR, WALL_COLOUR, WALL_COLOUR],
            [WALL_COLOUR, WALL_COLOUR, WALL_COLOUR],
            [WALL_COLOUR, WALL_COLOUR, WALL_COLOUR],
        ],
        name=f"wall_{suffix}",
        visible=True,
        collidable=True,
        blocking=BlockingMode.PIXEL_PERFECT,
        tags=["wall"],
        layer=0,
    )


def _make_cube_template() -> Sprite:
    f = INITIAL_FACES
    return Sprite(
        pixels=[
            [f["back"], f["back"], f["back"]],
            [f["left"], f["top"], f["right"]],
            [f["front"], f["front"], f["front"]],
        ],
        name="cube",
        visible=True,
        collidable=True,
        blocking=BlockingMode.PIXEL_PERFECT,
        tags=["cube"],
        layer=2,
    )


# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites: Dict[str, Sprite] = {
    "cube": _make_cube_template(),
}
for _col in (YELLOW, BLUE, GREEN, RED, PURPLE, ORANGE):
    sprites[f"target_{COLOUR_NAMES[_col]}"] = _make_target_sprite(_col)


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
def _at(lx: int, ly: int) -> Tuple[int, int]:
    return (lx * STRIDE, ly * STRIDE)


# --- L1 -------------------------------------------------------------
# 6x6 logical board (grid_size 24). Cube starts at (0, 2), the unfolded
# cube net occupies (1,2),(2,1),(2,2),(2,3),(3,2),(4,2). Walls at every
# cell adjacent to the 7-cell shape so the cube is funnelled along the
# net. Once the cube leaves (0, 2), it cannot return.
#
# Witness [E, E, S, N, N, S, E, E] deposits the 6 face colours
# uniquely on the 6 target cells. Target colours match those deposits.
L1_GRID = 24
L1_LOGICAL = 6
L1_ALLOWED = {(0, 2), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (4, 2)}
L1_START = (0, 2)
# Border = every cell on the 6×6 board NOT in the allowed set (walls
# render the playable region as a black-bordered net).
_L1_BORDER = [
    (lx, ly)
    for ly in range(L1_LOGICAL)
    for lx in range(L1_LOGICAL)
    if (lx, ly) not in L1_ALLOWED
]
L1 = Level(
    sprites=[
        sprites["cube"].clone().set_position(*_at(*L1_START)),
        # Targets — colours derived from the witness face-permutation:
        sprites["target_orange"].clone().set_position(*_at(1, 2)),
        sprites["target_red"].clone().set_position(*_at(2, 1)),
        sprites["target_yellow"].clone().set_position(*_at(2, 2)),
        sprites["target_green"].clone().set_position(*_at(2, 3)),
        sprites["target_purple"].clone().set_position(*_at(3, 2)),
        sprites["target_blue"].clone().set_position(*_at(4, 2)),
    ]
    + [
        _make_wall_sprite(f"L1_{lx}_{ly}").set_position(*_at(lx, ly))
        for lx, ly in _L1_BORDER
    ],
    grid_size=(L1_GRID, L1_GRID),
    data={
        "step_budget": 30,
        "win_mode": "exact",
        "start_cell": L1_START,
        "lock_start_after_leave": True,
    },
)


# --- L2 -------------------------------------------------------------
# 4x4 logical board. Cube top-left, target bottom-right (diagonal).
# Natural axis-by-axis path [E, E, E, S, S, S] deposits red at (3, 3),
# so target colour = red. First-arrival path solves naturally.
L2_GRID = 16
L2_LOGICAL = 4
L2 = Level(
    sprites=[
        sprites["cube"].clone().set_position(*_at(0, 0)),
        sprites["target_red"].clone().set_position(*_at(3, 3)),
    ],
    grid_size=(L2_GRID, L2_GRID),
    data={"step_budget": 40, "win_mode": "exact"},
)


# --- L3 -------------------------------------------------------------
# 4x4 logical board. Three targets requiring specific colours; rolling-
# only solve via a non-trivial 8-action path.
L3_GRID = 16
L3_LOGICAL = 4
L3 = Level(
    sprites=[
        sprites["cube"].clone().set_position(*_at(0, 0)),
        sprites["target_green"].clone().set_position(*_at(1, 0)),
        sprites["target_red"].clone().set_position(*_at(3, 0)),
        sprites["target_yellow"].clone().set_position(*_at(3, 1)),
    ],
    grid_size=(L3_GRID, L3_GRID),
    data={"step_budget": 80, "win_mode": "exact"},
)

levels = [L1, L2, L3]


# ---------------------------------------------------------------------
# 3. Face permutations
# ---------------------------------------------------------------------
def _roll_north(f: Dict[str, int]) -> Dict[str, int]:
    return {
        "top": f["front"], "bottom": f["back"],
        "front": f["bottom"], "back": f["top"],
        "left": f["left"], "right": f["right"],
    }


def _roll_south(f: Dict[str, int]) -> Dict[str, int]:
    return {
        "top": f["back"], "bottom": f["front"],
        "front": f["top"], "back": f["bottom"],
        "left": f["left"], "right": f["right"],
    }


def _roll_west(f: Dict[str, int]) -> Dict[str, int]:
    return {
        "top": f["right"], "bottom": f["left"],
        "right": f["bottom"], "left": f["top"],
        "front": f["front"], "back": f["back"],
    }


def _roll_east(f: Dict[str, int]) -> Dict[str, int]:
    return {
        "top": f["left"], "bottom": f["right"],
        "left": f["bottom"], "right": f["top"],
        "front": f["front"], "back": f["back"],
    }


# ---------------------------------------------------------------------
# 4. HUD widget
# ---------------------------------------------------------------------
class StepBarHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0):
        super().__init__()
        self.max_steps = max_steps
        self.current_steps = max_steps

    def reset(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def tick(self) -> None:
        if self.current_steps > 0:
            self.current_steps -= 1

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        ratio = self.current_steps / self.max_steps
        filled = int(round(64 * ratio))
        for x in range(64):
            frame[0, x] = BAR_FILL if x < filled else BAR_EMPTY
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Pj7k(NovaBaseGame):
    def __init__(self) -> None:
        self.step_counter = StepBarHud(0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_counter],
        )
        self.faces: Dict[str, int] = dict(INITIAL_FACES)
        self.cube_x: int = 0
        self.cube_y: int = 0
        self._paint_seq: int = 0
        self._win_mode: str = "exact"
        self._logical_size: int = 4
        self._start_cell: Optional[Tuple[int, int]] = None
        self._lock_start: bool = False
        self._left_start: bool = False
        super().__init__(
            game_id="pj7k",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (16, 16)
        self.camera.width = gw
        self.camera.height = gh
        self._logical_size = gw // STRIDE
        budget = level.get_data("step_budget") or 50
        self.step_counter.reset(budget)
        self._win_mode = level.get_data("win_mode") or "exact"
        sc = level.get_data("start_cell")
        self._start_cell = tuple(sc) if sc is not None else None
        self._lock_start = bool(level.get_data("lock_start_after_leave"))
        self._left_start = False
        self.faces = dict(INITIAL_FACES)
        self._paint_seq = 0
        cube = self._cube_sprite()
        if cube is not None:
            self.cube_x = cube.x
            self.cube_y = cube.y
            self._refresh_cube_pixels()

    # --- helpers -----------------------------------------------------

    def _cube_sprite(self) -> Optional[Sprite]:
        cubes = self.current_level.get_sprites_by_tag("cube")
        return cubes[0] if cubes else None

    def _refresh_cube_pixels(self) -> None:
        cube = self._cube_sprite()
        if cube is None:
            return
        f = self.faces
        cube.pixels = np.array(
            [
                [f["back"], f["back"], f["back"]],
                [f["left"], f["top"], f["right"]],
                [f["front"], f["front"], f["front"]],
            ],
            dtype=cube.pixels.dtype,
        )

    def _wall_at_cell(self, lx: int, ly: int) -> bool:
        gx, gy = lx * STRIDE, ly * STRIDE
        for s in self.current_level.get_sprites_by_tag("wall"):
            if s.x == gx and s.y == gy:
                return True
        return False

    def _paint_at_cell(self, lx: int, ly: int) -> Optional[Sprite]:
        gx, gy = lx * STRIDE, ly * STRIDE
        for s in self.current_level.get_sprites_by_tag("paint"):
            if s.x == gx and s.y == gy:
                return s
        return None

    @staticmethod
    def _colour_from_subtag(prefix: str, sprite: Sprite) -> Optional[int]:
        for tag in sprite.tags:
            if tag.startswith(prefix) and tag != prefix.rstrip("_"):
                name = tag[len(prefix):]
                return NAME_TO_COLOUR.get(name)
        return None

    def _required_target_colour(self, target: Sprite) -> Optional[int]:
        return self._colour_from_subtag("target_", target)

    def _paint_colour(self, paint: Sprite) -> Optional[int]:
        return self._colour_from_subtag("paint_", paint)

    def _deposit_paint(self, lx: int, ly: int, colour: int) -> None:
        existing = self._paint_at_cell(lx, ly)
        if existing is not None:
            self.current_level.remove_sprite(existing)
        self._paint_seq += 1
        new_sprite = _make_paint_sprite(colour, str(self._paint_seq)).set_position(
            lx * STRIDE, ly * STRIDE
        )
        self.current_level.add_sprite(new_sprite)

    def _try_roll(self, dx: int, dy: int, new_faces: Dict[str, int]) -> bool:
        cube = self._cube_sprite()
        if cube is None:
            return False
        cur_lx = cube.x // STRIDE
        cur_ly = cube.y // STRIDE
        new_lx = cur_lx + dx
        new_ly = cur_ly + dy
        if not (0 <= new_lx < self._logical_size and 0 <= new_ly < self._logical_size):
            return False
        if self._wall_at_cell(new_lx, new_ly):
            return False
        if (
            self._lock_start
            and self._left_start
            and self._start_cell is not None
            and (new_lx, new_ly) == self._start_cell
        ):
            return False
        self.faces = new_faces
        cube.set_position(new_lx * STRIDE, new_ly * STRIDE)
        self.cube_x = cube.x
        self.cube_y = cube.y
        self._refresh_cube_pixels()
        if self._start_cell is not None and (cur_lx, cur_ly) == self._start_cell:
            self._left_start = True
        self._deposit_paint(new_lx, new_ly, new_faces["bottom"])
        return True

    def _check_win(self) -> bool:
        targets = self.current_level.get_sprites_by_tag("target")
        if not targets:
            return False
        for target in targets:
            lx = target.x // STRIDE
            ly = target.y // STRIDE
            paint = self._paint_at_cell(lx, ly)
            if paint is None:
                return False
            if self._win_mode == "exact":
                required = self._required_target_colour(target)
                if self._paint_colour(paint) != required:
                    return False
        return True

    # --- engine hooks ------------------------------------------------

    def step(self) -> None:
        self.step_counter.tick()
        aid = self.action.id
        if aid == GameAction.ACTION1:
            self._try_roll(0, -1, _roll_north(self.faces))
        elif aid == GameAction.ACTION2:
            self._try_roll(0, 1, _roll_south(self.faces))
        elif aid == GameAction.ACTION3:
            self._try_roll(-1, 0, _roll_west(self.faces))
        elif aid == GameAction.ACTION4:
            self._try_roll(1, 0, _roll_east(self.faces))
        if self._check_win():
            self.next_level()
        elif self.step_counter.current_steps <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        f = self.faces
        state[0, 0] = f["top"]
        state[0, 1] = f["bottom"]
        state[0, 2] = f["front"]
        state[0, 3] = f["back"]
        state[1, 0] = f["left"]
        state[1, 1] = f["right"]
        state[1, 2] = self.cube_x
        state[1, 3] = self.cube_y
        state[2, 0] = self.step_counter.current_steps
        return state
