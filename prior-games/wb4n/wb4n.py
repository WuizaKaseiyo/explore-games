"""wb4n."""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 4
PADDING_COLOR = 4
PANEL_COLOR = 1
FLOOR_COLOR = 1
WALL_COLOR = 5
WATER_COLOR = 10
BUOY_COLOR = 12
BUOY_EDGE = 8
BUOY_TARGET_COLOR = 8
BLOCK_COLOR = 11
BLOCK_EDGE = 5
BLOCK_TARGET_COLOR = 14
PIPE_BODY = 3
PIPE_EDGE = 5
PIPE_PORT = 14
GATE_COLOR = 14
GATE_EDGE = 5
STEP_COLOR = 14
STEP_EMPTY = 4

CELL = 4
GRID_CELLS = 16
GRID_W = GRID_CELLS * CELL
GRID_H = GRID_CELLS * CELL

BOARD_X0 = 4
BOARD_Y0 = 2
BOARD_SIZE = 7
INTERIOR_SIZE = 5

CONTROL_CELLS = {
    "F": (7, 0),
    "D": (7, 10),
    "L": (2, 4),
    "R": (10, 4),
}
BUTTON_SIZE = 2


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _board_cell(ix: int, iy: int) -> tuple[int, int]:
    return (BOARD_X0 + ix, BOARD_Y0 + iy)


def _surface_row(water_level: int) -> int:
    return INTERIOR_SIZE - water_level + 1


def _panel_pixels() -> list[list[int]]:
    return [[PANEL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _floor_pixels() -> list[list[int]]:
    return [[FLOOR_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _wall_pixels() -> list[list[int]]:
    return [[WALL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _water_pixels(on: bool) -> list[list[int]]:
    if not on:
        return [[-1 for _ in range(CELL)] for _ in range(CELL)]
    return [[WATER_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _buoy_pixels() -> list[list[int]]:
    return [
        [-1, BUOY_COLOR, BUOY_COLOR, -1],
        [BUOY_COLOR, BUOY_EDGE, BUOY_EDGE, BUOY_COLOR],
        [BUOY_COLOR, BUOY_EDGE, BUOY_EDGE, BUOY_COLOR],
        [-1, BUOY_COLOR, BUOY_COLOR, -1],
    ]


def _buoy_target_pixels() -> list[list[int]]:
    return [
        [BUOY_TARGET_COLOR, BUOY_COLOR, BUOY_COLOR, BUOY_TARGET_COLOR],
        [BUOY_COLOR, -1, -1, BUOY_COLOR],
        [BUOY_COLOR, -1, -1, BUOY_COLOR],
        [BUOY_TARGET_COLOR, BUOY_COLOR, BUOY_COLOR, BUOY_TARGET_COLOR],
    ]


def _block_pixels() -> list[list[int]]:
    return [
        [BLOCK_COLOR, BLOCK_COLOR, BLOCK_COLOR, BLOCK_COLOR],
        [BLOCK_COLOR, BLOCK_EDGE, BLOCK_EDGE, BLOCK_COLOR],
        [BLOCK_COLOR, BLOCK_EDGE, BLOCK_EDGE, BLOCK_COLOR],
        [BLOCK_COLOR, BLOCK_COLOR, BLOCK_COLOR, BLOCK_COLOR],
    ]


def _block_target_pixels() -> list[list[int]]:
    return [
        [BLOCK_TARGET_COLOR, BLOCK_COLOR, BLOCK_COLOR, BLOCK_TARGET_COLOR],
        [BLOCK_COLOR, -1, -1, BLOCK_COLOR],
        [BLOCK_COLOR, -1, -1, BLOCK_COLOR],
        [BLOCK_TARGET_COLOR, BLOCK_COLOR, BLOCK_COLOR, BLOCK_TARGET_COLOR],
    ]


def _gate_pixels(opened: bool) -> list[list[int]]:
    if opened:
        return [
            [GATE_EDGE, GATE_COLOR, GATE_COLOR, GATE_EDGE],
            [GATE_COLOR, -1, -1, GATE_COLOR],
            [GATE_COLOR, -1, -1, GATE_COLOR],
            [GATE_EDGE, GATE_COLOR, GATE_COLOR, GATE_EDGE],
        ]
    return _wall_pixels()


def _side_jet_pixels(direction: str) -> list[list[int]]:
    pixels = np.full((8, 8), PIPE_BODY, dtype=np.int16)
    pixels[0, :] = PIPE_EDGE
    pixels[7, :] = PIPE_EDGE
    pixels[:, 0] = PIPE_EDGE
    pixels[:, 7] = PIPE_EDGE
    pixels[2:6, 2:6] = PANEL_COLOR
    pixels[3:5, 2:6] = PIPE_BODY
    pixels[3:5, 1] = PIPE_PORT
    pixels[3:5, 6] = PIPE_PORT
    if direction == "R":
        return pixels.tolist()
    return np.fliplr(pixels).tolist()


def _fill_pixels() -> list[list[int]]:
    pixels = np.full((8, 8), PIPE_BODY, dtype=np.int16)
    pixels[0, :] = PIPE_EDGE
    pixels[7, :] = PIPE_EDGE
    pixels[:, 0] = PIPE_EDGE
    pixels[:, 7] = PIPE_EDGE
    pixels[1:7, 3:5] = PIPE_BODY
    pixels[5:7, 2:6] = PIPE_PORT
    pixels[2:4, 2:6] = PANEL_COLOR
    return pixels.tolist()


def _drain_pixels() -> list[list[int]]:
    pixels = np.array(_fill_pixels(), dtype=np.int16)
    return np.rot90(pixels, 2).tolist()


sprites = {
    "panel": Sprite(
        pixels=_panel_pixels(),
        name="panel",
        visible=True,
        collidable=False,
        tags=["panel"],
        layer=1,
    ),
    "floor": Sprite(
        pixels=_floor_pixels(),
        name="floor",
        visible=True,
        collidable=False,
        tags=["floor"],
        layer=1,
    ),
    "wall": Sprite(
        pixels=_wall_pixels(),
        name="wall",
        visible=True,
        collidable=False,
        tags=["wall"],
        layer=4,
    ),
    "water": Sprite(
        pixels=_water_pixels(True),
        name="water",
        visible=True,
        collidable=False,
        tags=["water"],
        layer=2,
    ),
    "buoy": Sprite(
        pixels=_buoy_pixels(),
        name="buoy",
        visible=True,
        collidable=False,
        tags=["buoy"],
        layer=6,
    ),
    "buoy_target": Sprite(
        pixels=_buoy_target_pixels(),
        name="buoy_target",
        visible=True,
        collidable=False,
        tags=["buoy_target"],
        layer=3,
    ),
    "block": Sprite(
        pixels=_block_pixels(),
        name="block",
        visible=True,
        collidable=False,
        tags=["block"],
        layer=5,
    ),
    "block_target": Sprite(
        pixels=_block_target_pixels(),
        name="block_target",
        visible=True,
        collidable=False,
        tags=["block_target"],
        layer=3,
    ),
    "gate": Sprite(
        pixels=_gate_pixels(False),
        name="gate",
        visible=True,
        collidable=False,
        tags=["gate"],
        layer=4,
    ),
    "control_F": Sprite(
        pixels=_fill_pixels(),
        name="control_F",
        visible=True,
        collidable=False,
        tags=["control_F"],
        layer=4,
    ),
    "control_D": Sprite(
        pixels=_drain_pixels(),
        name="control_D",
        visible=True,
        collidable=False,
        tags=["control_D"],
        layer=4,
    ),
    "control_L": Sprite(
        pixels=_side_jet_pixels("L"),
        name="control_L",
        visible=True,
        collidable=False,
        tags=["control_L"],
        layer=4,
    ),
    "control_R": Sprite(
        pixels=_side_jet_pixels("R"),
        name="control_R",
        visible=True,
        collidable=False,
        tags=["control_R"],
        layer=4,
    ),
}


def _clone(name: str, cx: int, cy: int) -> Sprite:
    return sprites[name].clone().set_position(*_cell(cx, cy))


def _border_and_floor() -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    walls: list[tuple[int, int]] = []
    floors: list[tuple[int, int]] = []
    for iy in range(BOARD_SIZE):
        for ix in range(BOARD_SIZE):
            cell = _board_cell(ix, iy)
            if ix in {0, BOARD_SIZE - 1} or iy in {0, BOARD_SIZE - 1}:
                walls.append(cell)
            else:
                floors.append(cell)
    return walls, floors


def _build_level(
    *,
    water_level: int,
    buoy_x: int,
    buoy_target: tuple[int, int],
    block_start: tuple[int, int] | None,
    block_target: tuple[int, int] | None,
    internal_walls: list[tuple[int, int]],
    gates: list[tuple[int, int]],
    step_budget: int,
) -> Level:
    placed: list[Sprite] = []

    for cy in range(11, 16):
        for cx in range(0, GRID_CELLS):
            placed.append(_clone("panel", cx, cy))

    border_walls, floor_cells = _border_and_floor()
    for cx, cy in floor_cells:
        placed.append(_clone("floor", cx, cy))
        placed.append(_clone("water", cx, cy))
    for cx, cy in border_walls:
        placed.append(_clone("wall", cx, cy))
    for wall in internal_walls:
        placed.append(_clone("wall", *_board_cell(*wall)))
    for gate in gates:
        placed.append(_clone("gate", *_board_cell(*gate)))

    placed.append(_clone("buoy_target", *_board_cell(*buoy_target)))
    if block_target is not None:
        placed.append(_clone("block_target", *_board_cell(*block_target)))
    placed.append(_clone("buoy", *_board_cell(buoy_x, _surface_row(water_level))))
    if block_start is not None:
        placed.append(_clone("block", *_board_cell(*block_start)))

    for control, cell in CONTROL_CELLS.items():
        placed.append(_clone(f"control_{control}", *cell))

    return Level(
        sprites=placed,
        grid_size=(GRID_W, GRID_H),
        data={
            "water_level": water_level,
            "buoy_x": buoy_x,
            "buoy_target": list(buoy_target),
            "block_start": list(block_start) if block_start is not None else None,
            "block_target": list(block_target) if block_target is not None else None,
            "internal_walls": [list(wall) for wall in internal_walls],
            "gates": [list(gate) for gate in gates],
            "step_budget": step_budget,
        },
    )


levels = [
    _build_level(
        water_level=3,
        buoy_x=1,
        buoy_target=(5, 2),
        block_start=None,
        block_target=None,
        internal_walls=[(2, 1), (3, 1)],
        gates=[],
        step_budget=4,
    ),
    _build_level(
        water_level=2,
        buoy_x=5,
        buoy_target=(5, 2),
        block_start=(1, 2),
        block_target=(2, 2),
        internal_walls=[(4, 5), (2, 4)],
        gates=[],
        step_budget=6,
    ),
    _build_level(
        water_level=2,
        buoy_x=5,
        buoy_target=(1, 1),
        block_start=(2, 4),
        block_target=(1, 4),
        internal_walls=[(1, 3)],
        gates=[(2, 1)],
        step_budget=8,
    ),
]


class StepHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self.steps_remaining = 0
        self.max_steps = 1

    def set_state(self, *, steps_remaining: int, max_steps: int) -> None:
        self.steps_remaining = max(0, steps_remaining)
        self.max_steps = max(1, max_steps)

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        filled = int(round((self.steps_remaining / self.max_steps) * 6))
        for idx in range(6):
            x0, y0 = _cell(idx + 1, 0)
            color = STEP_COLOR if idx < filled else STEP_EMPTY
            frame[y0 + 1 : y0 + 3, x0 + 1 : x0 + 3] = color
        return frame


class Wb4n(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = StepHud()
        self._anim_queue: list[tuple[int, tuple[int, int], tuple[int, int] | None]] = []
        self._pending_success = False
        camera = Camera(
            width=GRID_W,
            height=GRID_H,
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._hud],
        )
        super().__init__(
            game_id="wb4n",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        self.start_water_level = int(level.get_data("water_level") or 1)
        self.start_buoy_x = int(level.get_data("buoy_x") or 1)
        self.buoy_target = tuple(level.get_data("buoy_target") or [1, 1])
        raw_block_start = level.get_data("block_start")
        raw_block_target = level.get_data("block_target")
        self.block_start = tuple(raw_block_start) if raw_block_start is not None else None
        self.block_target = tuple(raw_block_target) if raw_block_target is not None else None
        self.internal_walls = {tuple(wall) for wall in level.get_data("internal_walls") or []}
        self.gates = {tuple(gate) for gate in level.get_data("gates") or []}
        self.step_budget = int(level.get_data("step_budget") or 1)
        self.steps_used = 0
        self._pending_success = False
        self._anim_queue = []

        border_walls, floor_cells = _border_and_floor()
        self.border_wall_cells = set(border_walls)
        self.interior_floor_cells = [
            _board_cell(ix, iy)
            for iy in range(1, INTERIOR_SIZE + 1)
            for ix in range(1, INTERIOR_SIZE + 1)
        ]
        self.static_wall_cells = set(self.border_wall_cells)
        self.static_wall_cells.update(_board_cell(*wall) for wall in self.internal_walls)

        self.buoy_sprite = next(sprite for sprite in level.get_sprites() if sprite.name == "buoy")
        block_sprites = [sprite for sprite in level.get_sprites() if sprite.name == "block"]
        self.block_sprite = block_sprites[0] if block_sprites else None
        self.gate_sprites = {
            (sprite.x // CELL - BOARD_X0, sprite.y // CELL - BOARD_Y0): sprite
            for sprite in level.get_sprites()
            if sprite.name == "gate"
        }
        self.water_sprites = {
            (sprite.x // CELL, sprite.y // CELL): sprite
            for sprite in level.get_sprites()
            if sprite.name == "water"
        }

        self._reset_state()
        self._refresh_visuals()
        self._refresh_hud()

    def _reset_state(self) -> None:
        self.water_level = self.start_water_level
        self.buoy_x = self.start_buoy_x
        self.block_cell = _board_cell(*self.block_start) if self.block_start is not None else None

    def _refresh_hud(self) -> None:
        self._hud.set_state(
            steps_remaining=self.step_budget - self.steps_used,
            max_steps=self.step_budget,
        )

    def _gate_is_open(self) -> bool:
        return self.water_level == INTERIOR_SIZE

    def _active_wall_cells(self) -> set[tuple[int, int]]:
        cells = set(self.static_wall_cells)
        if not self._gate_is_open():
            cells.update(_board_cell(*gate) for gate in self.gates)
        return cells

    def _buoy_cell(self) -> tuple[int, int]:
        return _board_cell(self.buoy_x, _surface_row(self.water_level))

    def _refresh_visuals(self) -> None:
        flooded_from = _surface_row(self.water_level)
        for iy in range(1, INTERIOR_SIZE + 1):
            for ix in range(1, INTERIOR_SIZE + 1):
                world = _board_cell(ix, iy)
                sprite = self.water_sprites[world]
                sprite.pixels = np.array(_water_pixels(iy >= flooded_from), dtype=np.int16)

        gate_open = self._gate_is_open()
        for gate, sprite in self.gate_sprites.items():
            sprite.pixels = np.array(_gate_pixels(gate_open), dtype=np.int16)

        buoy_cell = self._buoy_cell()
        self.buoy_sprite.set_position(*_cell(*buoy_cell))
        if self.block_sprite is not None and self.block_cell is not None:
            self.block_sprite.set_position(*_cell(*self.block_cell))

    def _click_cell(self) -> tuple[int, int] | None:
        click_x = int(self.action.data.get("x", -1000))
        click_y = int(self.action.data.get("y", -1000))
        grid = self.camera.display_to_grid(click_x, click_y)
        if grid is None:
            return None
        return (grid[0] // CELL, grid[1] // CELL)

    def _hit_box(self, clicked: tuple[int, int], origin: tuple[int, int]) -> bool:
        return (
            origin[0] <= clicked[0] < origin[0] + BUTTON_SIZE
            and origin[1] <= clicked[1] < origin[1] + BUTTON_SIZE
        )

    def _apply_fill(self) -> None:
        self.water_level = min(INTERIOR_SIZE, self.water_level + 1)

    def _apply_drain(self) -> None:
        self.water_level = max(1, self.water_level - 1)

    def _apply_current(self, direction: str) -> None:
        dx = -1 if direction == "L" else 1
        buoy_cell = self._buoy_cell()
        surface_world_y = buoy_cell[1]
        active_walls = self._active_wall_cells()

        if self.block_cell is not None and self.block_cell[1] >= surface_world_y:
            next_block = (self.block_cell[0] + dx, self.block_cell[1])
            if next_block not in active_walls and next_block != buoy_cell:
                self.block_cell = next_block

        occupied = {self.block_cell} if self.block_cell is not None else set()
        next_x = self.buoy_x
        while True:
            trial_x = next_x + dx
            trial_world = _board_cell(trial_x, _surface_row(self.water_level))
            if trial_x < 1 or trial_x > INTERIOR_SIZE:
                break
            if trial_world in active_walls or trial_world in occupied:
                break
            next_x = trial_x
        self.buoy_x = next_x

    def _win_now(self) -> bool:
        buoy_ok = self._buoy_cell() == _board_cell(*self.buoy_target)
        block_ok = self.block_target is None or self.block_cell == _board_cell(*self.block_target)
        return buoy_ok and block_ok

    def _queue_state(self) -> None:
        self._anim_queue.append((self.water_level, self._buoy_cell(), self.block_cell))

    def _advance_anim_frame(self) -> None:
        water_level, buoy_cell, block_cell = self._anim_queue.pop(0)
        self.water_level = int(water_level)
        self.buoy_x = buoy_cell[0] - BOARD_X0
        self.block_cell = tuple(block_cell) if block_cell is not None else None
        self._refresh_visuals()

    def _resolve_after_action(self) -> None:
        self._refresh_hud()
        if self._pending_success:
            self.next_level()
            self.complete_action()
            return
        if self.steps_used >= self.step_budget:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def step(self) -> None:
        if self._anim_queue:
            self._advance_anim_frame()
            if self._anim_queue:
                return
            self._resolve_after_action()
            return

        clicked = self._click_cell()
        if clicked is None:
            self.complete_action()
            return

        control = None
        for name, origin in CONTROL_CELLS.items():
            if self._hit_box(clicked, origin):
                control = name
                break
        if control is None:
            self.complete_action()
            return

        if control == "F":
            self._apply_fill()
        elif control == "D":
            self._apply_drain()
        else:
            self._apply_current(control)
        self._queue_state()
        self.steps_used += 1
        self._pending_success = self._win_now()
        self._refresh_hud()

        if self._anim_queue:
            self._advance_anim_frame()
            if self._anim_queue:
                return
            self._resolve_after_action()
            return

        if self._pending_success:
            self.next_level()
        elif self.steps_used >= self.step_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
