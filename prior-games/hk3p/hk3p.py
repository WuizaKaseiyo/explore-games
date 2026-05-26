"""hk3p."""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 4
PADDING_COLOR = 4
PANEL_COLOR = 1
FLOOR_COLOR = 1
WALL_COLOR = 5
HEAT_COLOR = 8
HEAT_CORE = 7
COOL_COLOR = 9
COOL_CORE = 1
VENT_COLOR = 3
VENT_EDGE = 5
VENT_AIR = 1
MATERIAL_COLOR = 14
MATERIAL_EDGE = 7
MATERIAL_DARK = 5
STEP_COLOR = 14
STEP_EMPTY = 4

CELL = 4
GRID_CELLS = 16
GRID_W = GRID_CELLS * CELL
GRID_H = GRID_CELLS * CELL

BOARD_X0 = 4
BOARD_Y0 = 3
BOARD_SIZE = 7

CONTROL_CELLS = {
    "H": (5, 1),
    "C": (8, 1),
    "L": (1, 5),
    "R": (11, 5),
}
BUTTON_SIZE = 2


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _board_cell(ix: int, iy: int) -> tuple[int, int]:
    return (BOARD_X0 + ix, BOARD_Y0 + iy)


def _panel_pixels() -> list[list[int]]:
    return [[PANEL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _floor_pixels() -> list[list[int]]:
    return [[FLOOR_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _wall_pixels() -> list[list[int]]:
    return [[WALL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _target_pixels() -> list[list[int]]:
    return [
        [MATERIAL_COLOR, MATERIAL_COLOR, MATERIAL_COLOR, MATERIAL_COLOR],
        [MATERIAL_COLOR, -1, -1, MATERIAL_COLOR],
        [MATERIAL_COLOR, -1, -1, MATERIAL_COLOR],
        [MATERIAL_COLOR, MATERIAL_COLOR, MATERIAL_COLOR, MATERIAL_COLOR],
    ]


def _solid_pixels() -> list[list[int]]:
    return [
        [MATERIAL_EDGE, MATERIAL_EDGE, MATERIAL_EDGE, MATERIAL_EDGE],
        [MATERIAL_EDGE, MATERIAL_COLOR, MATERIAL_COLOR, MATERIAL_EDGE],
        [MATERIAL_EDGE, MATERIAL_COLOR, MATERIAL_COLOR, MATERIAL_EDGE],
        [MATERIAL_EDGE, MATERIAL_EDGE, MATERIAL_EDGE, MATERIAL_EDGE],
    ]


def _liquid_pixels() -> list[list[int]]:
    return [
        [-1, MATERIAL_COLOR, MATERIAL_COLOR, -1],
        [MATERIAL_COLOR, MATERIAL_COLOR, MATERIAL_COLOR, MATERIAL_COLOR],
        [MATERIAL_COLOR, MATERIAL_DARK, MATERIAL_DARK, MATERIAL_COLOR],
        [-1, MATERIAL_COLOR, MATERIAL_COLOR, -1],
    ]


def _gas_pixels() -> list[list[int]]:
    return [
        [-1, MATERIAL_COLOR, -1, MATERIAL_COLOR],
        [MATERIAL_COLOR, MATERIAL_COLOR, MATERIAL_COLOR, MATERIAL_COLOR],
        [MATERIAL_COLOR, -1, MATERIAL_COLOR, -1],
        [-1, MATERIAL_COLOR, -1, MATERIAL_COLOR],
    ]


def _heater_pixels() -> list[list[int]]:
    return [
        [VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE],
        [VENT_EDGE, HEAT_COLOR, HEAT_COLOR, HEAT_COLOR, HEAT_COLOR, HEAT_COLOR, HEAT_COLOR, VENT_EDGE],
        [VENT_EDGE, HEAT_COLOR, HEAT_CORE, HEAT_CORE, HEAT_CORE, HEAT_CORE, HEAT_COLOR, VENT_EDGE],
        [VENT_EDGE, HEAT_COLOR, HEAT_CORE, HEAT_COLOR, HEAT_COLOR, HEAT_CORE, HEAT_COLOR, VENT_EDGE],
        [VENT_EDGE, HEAT_COLOR, HEAT_CORE, HEAT_CORE, HEAT_CORE, HEAT_CORE, HEAT_COLOR, VENT_EDGE],
        [VENT_EDGE, HEAT_COLOR, HEAT_COLOR, HEAT_CORE, HEAT_CORE, HEAT_COLOR, HEAT_COLOR, VENT_EDGE],
        [VENT_EDGE, HEAT_COLOR, HEAT_COLOR, HEAT_COLOR, HEAT_COLOR, HEAT_COLOR, HEAT_COLOR, VENT_EDGE],
        [VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE],
    ]


def _cooler_pixels() -> list[list[int]]:
    return [
        [VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE],
        [VENT_EDGE, COOL_COLOR, COOL_COLOR, COOL_COLOR, COOL_COLOR, COOL_COLOR, COOL_COLOR, VENT_EDGE],
        [VENT_EDGE, COOL_COLOR, COOL_CORE, COOL_CORE, COOL_CORE, COOL_CORE, COOL_COLOR, VENT_EDGE],
        [VENT_EDGE, COOL_COLOR, COOL_CORE, COOL_COLOR, COOL_COLOR, COOL_CORE, COOL_COLOR, VENT_EDGE],
        [VENT_EDGE, COOL_COLOR, COOL_CORE, COOL_COLOR, COOL_COLOR, COOL_CORE, COOL_COLOR, VENT_EDGE],
        [VENT_EDGE, COOL_COLOR, COOL_CORE, COOL_CORE, COOL_CORE, COOL_CORE, COOL_COLOR, VENT_EDGE],
        [VENT_EDGE, COOL_COLOR, COOL_COLOR, COOL_COLOR, COOL_COLOR, COOL_COLOR, COOL_COLOR, VENT_EDGE],
        [VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE, VENT_EDGE],
    ]


def _blower_pixels(direction: str) -> list[list[int]]:
    pixels = np.full((8, 8), VENT_COLOR, dtype=np.int16)
    pixels[0, :] = VENT_EDGE
    pixels[7, :] = VENT_EDGE
    pixels[:, 0] = VENT_EDGE
    pixels[:, 7] = VENT_EDGE
    pixels[2:6, 2:6] = PANEL_COLOR
    pixels[2:6, 1] = VENT_COLOR
    pixels[2:6, 6] = VENT_COLOR
    pixels[2, 3:5] = VENT_AIR
    pixels[4, 3:5] = VENT_AIR
    pixels[5, 2:6] = VENT_AIR
    if direction == "R":
        return pixels.tolist()
    return np.fliplr(pixels).tolist()


sprites = {
    "panel": Sprite(_panel_pixels(), "panel", True, False, tags=["panel"], layer=1),
    "floor": Sprite(_floor_pixels(), "floor", True, False, tags=["floor"], layer=1),
    "wall": Sprite(_wall_pixels(), "wall", True, False, tags=["wall"], layer=4),
    "target": Sprite(_target_pixels(), "target", True, False, tags=["target"], layer=2),
    "material": Sprite(_solid_pixels(), "material", True, False, tags=["material"], layer=5),
    "control_H": Sprite(_heater_pixels(), "control_H", True, False, tags=["control_H"], layer=4),
    "control_C": Sprite(_cooler_pixels(), "control_C", True, False, tags=["control_C"], layer=4),
    "control_L": Sprite(_blower_pixels("L"), "control_L", True, False, tags=["control_L"], layer=4),
    "control_R": Sprite(_blower_pixels("R"), "control_R", True, False, tags=["control_R"], layer=4),
}


def _clone(name: str, cx: int, cy: int) -> Sprite:
    return sprites[name].clone().set_position(*_cell(cx, cy))


def _border_and_floor() -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    floors: list[tuple[int, int]] = []
    walls: list[tuple[int, int]] = []
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
    start: tuple[int, int],
    target: tuple[int, int],
    internal_walls: list[tuple[int, int]],
    step_budget: int,
) -> Level:
    placed: list[Sprite] = []
    for cy in range(11, 16):
        for cx in range(0, GRID_CELLS):
            placed.append(_clone("panel", cx, cy))

    border_walls, floor_cells = _border_and_floor()
    for cx, cy in floor_cells:
        placed.append(_clone("floor", cx, cy))
    for cx, cy in border_walls:
        placed.append(_clone("wall", cx, cy))
    for wall in internal_walls:
        placed.append(_clone("wall", *_board_cell(*wall)))

    placed.append(_clone("target", *_board_cell(*target)))
    placed.append(_clone("material", *_board_cell(*start)))
    for key, cell in CONTROL_CELLS.items():
        placed.append(_clone(f"control_{key}", *cell))

    return Level(
        sprites=placed,
        grid_size=(GRID_W, GRID_H),
        data={
            "start": list(start),
            "target": list(target),
            "internal_walls": [list(wall) for wall in internal_walls],
            "step_budget": step_budget,
        },
    )


levels = [
    _build_level(start=(1, 5), target=(5, 5), internal_walls=[], step_budget=4),
    _build_level(start=(2, 5), target=(5, 1), internal_walls=[(3, 5)], step_budget=5),
    _build_level(start=(2, 5), target=(4, 5), internal_walls=[(3, 5)], step_budget=6),
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


class Hk3p(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = StepHud()
        camera = Camera(width=GRID_W, height=GRID_H, background=BACKGROUND_COLOR, letter_box=PADDING_COLOR, interfaces=[self._hud])
        super().__init__(game_id="hk3p", levels=levels, camera=camera, available_actions=[6])

    def on_set_level(self, level: Level) -> None:
        self.start = tuple(level.get_data("start") or [1, 1])
        self.target = tuple(level.get_data("target") or [1, 1])
        self.step_budget = int(level.get_data("step_budget") or 1)
        self.steps_used = 0
        border_walls, _ = _border_and_floor()
        self.wall_cells = set(border_walls)
        self.wall_cells.update(_board_cell(*tuple(wall)) for wall in level.get_data("internal_walls") or [])
        self.material_sprite = next(sprite for sprite in level.get_sprites() if sprite.name == "material")
        self.material_cell = _board_cell(*self.start)
        self.phase = "solid"
        self._refresh_visuals()
        self._refresh_hud()

    def _refresh_hud(self) -> None:
        self._hud.set_state(steps_remaining=self.step_budget - self.steps_used, max_steps=self.step_budget)

    def _refresh_visuals(self) -> None:
        if self.phase == "solid":
            self.material_sprite.pixels = np.array(_solid_pixels(), dtype=np.int16)
        elif self.phase == "liquid":
            self.material_sprite.pixels = np.array(_liquid_pixels(), dtype=np.int16)
        else:
            self.material_sprite.pixels = np.array(_gas_pixels(), dtype=np.int16)
        self.material_sprite.set_position(*_cell(*self.material_cell))

    def _click_cell(self) -> tuple[int, int] | None:
        click_x = int(self.action.data.get("x", -1000))
        click_y = int(self.action.data.get("y", -1000))
        grid = self.camera.display_to_grid(click_x, click_y)
        if grid is None:
            return None
        return (grid[0] // CELL, grid[1] // CELL)

    def _hit_box(self, clicked: tuple[int, int], origin: tuple[int, int]) -> bool:
        return origin[0] <= clicked[0] < origin[0] + BUTTON_SIZE and origin[1] <= clicked[1] < origin[1] + BUTTON_SIZE

    def _settle(self, cell: tuple[int, int], phase: str) -> tuple[int, int]:
        x, y = cell
        if phase == "liquid":
            while (x, y + 1) not in self.wall_cells:
                y += 1
        elif phase == "gas":
            while (x, y - 1) not in self.wall_cells:
                y -= 1
        return (x, y)

    def _heat(self) -> None:
        if self.phase == "solid":
            self.phase = "liquid"
        elif self.phase == "liquid":
            self.phase = "gas"
        self.material_cell = self._settle(self.material_cell, self.phase)

    def _cool(self) -> None:
        if self.phase == "gas":
            self.phase = "liquid"
        elif self.phase == "liquid":
            self.phase = "solid"
        self.material_cell = self._settle(self.material_cell, self.phase)

    def _blow(self, direction: str) -> None:
        dx = -1 if direction == "L" else 1
        x, y = self.material_cell
        if self.phase == "solid":
            trial = (x + dx, y)
            if trial not in self.wall_cells:
                self.material_cell = trial
            return

        nx = x
        while (nx + dx, y) not in self.wall_cells:
            nx += dx
        self.material_cell = self._settle((nx, y), self.phase)

    def step(self) -> None:
        clicked = self._click_cell()
        if clicked is None:
            self.complete_action()
            return

        action = None
        for key, origin in CONTROL_CELLS.items():
            if self._hit_box(clicked, origin):
                action = key
                break
        if action is None:
            self.complete_action()
            return

        if action == "H":
            self._heat()
        elif action == "C":
            self._cool()
        else:
            self._blow(action)

        self.steps_used += 1
        self._refresh_visuals()
        self._refresh_hud()

        if self.material_cell == _board_cell(*self.target):
            self.next_level()
        elif self.steps_used >= self.step_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
