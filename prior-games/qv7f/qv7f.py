"""qv7f."""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 4
PADDING_COLOR = 4
PANEL_COLOR = 1
LANE_COLOR = 1
OUTLINE_COLOR = 5
SPARK_COLOR = 14
LOW_LOCK_COLOR = 8
HIGH_LOCK_COLOR = 9
HIGH_LOCK_LIGHT = 10
STEP_COLOR = 14
STEP_EMPTY = 4

CELL = 4
GRID_CELLS = 16
GRID_W = GRID_CELLS * CELL
GRID_H = GRID_CELLS * CELL

CONTROL_CELLS = {
    "+": (3, 0),
    "-": (9, 0),
    "L": (1, 4),
    "R": (12, 4),
}
BUTTON_SIZE = 2

PATH_LEVELS = [
    [(3, 4), (5, 4), (7, 4), (9, 4), (11, 4)],
    [(3, 5), (5, 5), (7, 5), (7, 3), (9, 3)],
    [(3, 6), (5, 6), (5, 4), (7, 4), (9, 4)],
]
LOCK_LEVELS = [
    [(4, 4), (6, 4), (8, 4), (10, 4)],
    [(4, 5), (6, 5), (7, 4), (8, 3)],
    [(4, 6), (5, 5), (6, 4), (8, 4)],
]


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _panel_pixels() -> list[list[int]]:
    return [[PANEL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _lane_pixels() -> list[list[int]]:
    return [[LANE_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _spark_pixels(charge: int) -> list[list[int]]:
    if charge == 0:
        return [
            [-1, PANEL_COLOR, PANEL_COLOR, -1],
            [PANEL_COLOR, OUTLINE_COLOR, OUTLINE_COLOR, PANEL_COLOR],
            [PANEL_COLOR, OUTLINE_COLOR, OUTLINE_COLOR, PANEL_COLOR],
            [-1, PANEL_COLOR, PANEL_COLOR, -1],
        ]
    if charge == 1:
        return [
            [-1, SPARK_COLOR, SPARK_COLOR, -1],
            [SPARK_COLOR, OUTLINE_COLOR, OUTLINE_COLOR, SPARK_COLOR],
            [SPARK_COLOR, OUTLINE_COLOR, OUTLINE_COLOR, SPARK_COLOR],
            [-1, SPARK_COLOR, SPARK_COLOR, -1],
        ]
    return [
        [SPARK_COLOR, -1, -1, SPARK_COLOR],
        [-1, SPARK_COLOR, SPARK_COLOR, -1],
        [-1, SPARK_COLOR, SPARK_COLOR, -1],
        [SPARK_COLOR, -1, -1, SPARK_COLOR],
    ]


def _target_pixels() -> list[list[int]]:
    return [
        [SPARK_COLOR, SPARK_COLOR, SPARK_COLOR, SPARK_COLOR],
        [SPARK_COLOR, -1, -1, SPARK_COLOR],
        [SPARK_COLOR, -1, -1, SPARK_COLOR],
        [SPARK_COLOR, SPARK_COLOR, SPARK_COLOR, SPARK_COLOR],
    ]


def _lock_pixels(kind: str | None) -> list[list[int]]:
    if kind is None or kind == ".":
        return [[-1 for _ in range(CELL)] for _ in range(CELL)]
    if kind == "l":
        return [
            [LOW_LOCK_COLOR, LOW_LOCK_COLOR, LOW_LOCK_COLOR, LOW_LOCK_COLOR],
            [LOW_LOCK_COLOR, -1, -1, LOW_LOCK_COLOR],
            [LOW_LOCK_COLOR, -1, -1, LOW_LOCK_COLOR],
            [LOW_LOCK_COLOR, LOW_LOCK_COLOR, LOW_LOCK_COLOR, LOW_LOCK_COLOR],
        ]
    return [
        [HIGH_LOCK_COLOR, HIGH_LOCK_COLOR, HIGH_LOCK_COLOR, HIGH_LOCK_COLOR],
        [HIGH_LOCK_COLOR, HIGH_LOCK_LIGHT, HIGH_LOCK_LIGHT, HIGH_LOCK_COLOR],
        [HIGH_LOCK_COLOR, HIGH_LOCK_LIGHT, HIGH_LOCK_LIGHT, HIGH_LOCK_COLOR],
        [HIGH_LOCK_COLOR, HIGH_LOCK_COLOR, HIGH_LOCK_COLOR, HIGH_LOCK_COLOR],
    ]


def _charge_pad_pixels() -> list[list[int]]:
    pixels = np.full((8, 8), PANEL_COLOR, dtype=np.int16)
    pixels[0, :] = OUTLINE_COLOR
    pixels[7, :] = OUTLINE_COLOR
    pixels[:, 0] = OUTLINE_COLOR
    pixels[:, 7] = OUTLINE_COLOR
    pixels[1:7, 1:7] = PANEL_COLOR
    pixels[3:5, 2:6] = OUTLINE_COLOR
    pixels[2:6, 3:5] = OUTLINE_COLOR
    return pixels.tolist()


def _drain_pad_pixels() -> list[list[int]]:
    pixels = np.full((8, 8), PANEL_COLOR, dtype=np.int16)
    pixels[0, :] = OUTLINE_COLOR
    pixels[7, :] = OUTLINE_COLOR
    pixels[:, 0] = OUTLINE_COLOR
    pixels[:, 7] = OUTLINE_COLOR
    pixels[1:7, 1:7] = PANEL_COLOR
    pixels[3:5, 2:6] = OUTLINE_COLOR
    return pixels.tolist()


def _blower_pixels(direction: str) -> list[list[int]]:
    pixels = np.full((8, 8), PANEL_COLOR, dtype=np.int16)
    pixels[1:7, 1:7] = OUTLINE_COLOR
    pixels[2:6, 2:6] = PANEL_COLOR
    pixels[3:5, 2:6] = OUTLINE_COLOR
    if direction == "L":
        pixels[2:6, 1:3] = OUTLINE_COLOR
    else:
        pixels[2:6, 5:7] = OUTLINE_COLOR
    return pixels.tolist()


sprites = {
    "panel": Sprite(_panel_pixels(), "panel", True, False, tags=["panel"], layer=1),
    "lane": Sprite(_lane_pixels(), "lane", True, False, tags=["lane"], layer=1),
    "spark": Sprite(_spark_pixels(0), "spark", True, False, tags=["spark"], layer=5),
    "target": Sprite(_target_pixels(), "target", True, False, tags=["target"], layer=2),
    "lock_1": Sprite(_lock_pixels("."), "lock_1", True, False, tags=["lock_1"], layer=4),
    "lock_2": Sprite(_lock_pixels("."), "lock_2", True, False, tags=["lock_2"], layer=4),
    "lock_3": Sprite(_lock_pixels("."), "lock_3", True, False, tags=["lock_3"], layer=4),
    "lock_4": Sprite(_lock_pixels("."), "lock_4", True, False, tags=["lock_4"], layer=4),
    "control_+": Sprite(_charge_pad_pixels(), "control_+", True, False, tags=["control_+"], layer=3),
    "control_-": Sprite(_drain_pad_pixels(), "control_-", True, False, tags=["control_-"], layer=3),
    "control_L": Sprite(_blower_pixels("L"), "control_L", True, False, tags=["control_L"], layer=3),
    "control_R": Sprite(_blower_pixels("R"), "control_R", True, False, tags=["control_R"], layer=3),
}


def _clone(name: str, cx: int, cy: int) -> Sprite:
    return sprites[name].clone().set_position(*_cell(cx, cy))


def _track_cells(path_cells: list[tuple[int, int]]) -> list[tuple[int, int]]:
    cells: list[tuple[int, int]] = []
    for idx, current in enumerate(path_cells):
        if current not in cells:
            cells.append(current)
        if idx == len(path_cells) - 1:
            continue
        nxt = path_cells[idx + 1]
        if current[0] == nxt[0]:
            x = current[0]
            for y in range(min(current[1], nxt[1]), max(current[1], nxt[1]) + 1):
                cell = (x, y)
                if cell not in cells:
                    cells.append(cell)
        else:
            y = current[1]
            for x in range(min(current[0], nxt[0]), max(current[0], nxt[0]) + 1):
                cell = (x, y)
                if cell not in cells:
                    cells.append(cell)
    return cells


def _build_level(
    *,
    start: int,
    target: int,
    locks: str,
    step_budget: int,
    path_cells: list[tuple[int, int]],
    lock_cells: list[tuple[int, int]],
) -> Level:
    placed: list[Sprite] = []
    for cy in range(9, 16):
        for cx in range(GRID_CELLS):
            placed.append(_clone("panel", cx, cy))
    for cx, cy in _track_cells(path_cells):
        placed.append(_clone("lane", cx, cy))
    placed.append(_clone("target", *path_cells[target - 1]))
    placed.append(_clone("spark", *path_cells[start - 1]))
    for idx in range(1, 5):
        placed.append(_clone(f"lock_{idx}", *lock_cells[idx - 1]))
    for key, cell in CONTROL_CELLS.items():
        placed.append(_clone(f"control_{key}", *cell))
    return Level(
        sprites=placed,
        grid_size=(GRID_W, GRID_H),
        data={
            "start": start,
            "target": target,
            "locks": locks,
            "step_budget": step_budget,
            "path_cells": [list(cell) for cell in path_cells],
            "lock_cells": [list(cell) for cell in lock_cells],
        },
    )


levels = [
    _build_level(start=1, target=2, locks="l...", step_budget=4, path_cells=PATH_LEVELS[0], lock_cells=LOCK_LEVELS[0]),
    _build_level(start=1, target=5, locks="h.l.", step_budget=8, path_cells=PATH_LEVELS[1], lock_cells=LOCK_LEVELS[1]),
    _build_level(start=1, target=5, locks="hlh.", step_budget=10, path_cells=PATH_LEVELS[2], lock_cells=LOCK_LEVELS[2]),
]


class StepHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self.steps_remaining = 0
        self.max_steps = 1

    def set_state(self, *, steps_remaining: int, max_steps: int) -> None:
        self.steps_remaining = max(0, steps_remaining)
        self.max_steps = max(1, max_steps)

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        filled = int(round((self.steps_remaining / self.max_steps) * GRID_W))
        frame[0, :filled] = STEP_COLOR
        frame[0, filled:] = STEP_EMPTY
        return frame


class Qv7f(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = StepHud()
        camera = Camera(width=GRID_W, height=GRID_H, background=BACKGROUND_COLOR, letter_box=PADDING_COLOR, interfaces=[self._hud])
        super().__init__(game_id="qv7f", levels=levels, camera=camera, available_actions=[6])

    def on_set_level(self, level: Level) -> None:
        self.pos = int(level.get_data("start") or 1)
        self.target = int(level.get_data("target") or 1)
        self.charge = 0
        self.locks = list(level.get_data("locks") or "....")
        self.path_cells = [tuple(cell) for cell in level.get_data("path_cells") or []]
        self.lock_cells = [tuple(cell) for cell in level.get_data("lock_cells") or []]
        self.step_budget = int(level.get_data("step_budget") or 1)
        self.steps_used = 0
        self.spark_sprite = next(sprite for sprite in level.get_sprites() if sprite.name == "spark")
        self.lock_sprites = [next(sprite for sprite in level.get_sprites() if sprite.name == f"lock_{idx}") for idx in range(1, 5)]
        self._refresh_visuals()
        self._refresh_hud()

    def _refresh_hud(self) -> None:
        self._hud.set_state(steps_remaining=self.step_budget - self.steps_used, max_steps=self.step_budget)

    def _refresh_visuals(self) -> None:
        self.spark_sprite.pixels = np.array(_spark_pixels(self.charge), dtype=np.int16)
        self.spark_sprite.set_position(*_cell(*self.path_cells[self.pos - 1]))
        for idx, sprite in enumerate(self.lock_sprites):
            sprite.pixels = np.array(_lock_pixels(self.locks[idx]), dtype=np.int16)
            sprite.set_position(*_cell(*self.lock_cells[idx]))

    def _click_cell(self) -> tuple[int, int] | None:
        click_x = int(self.action.data.get("x", -1000))
        click_y = int(self.action.data.get("y", -1000))
        grid = self.camera.display_to_grid(click_x, click_y)
        if grid is None:
            return None
        return (grid[0] // CELL, grid[1] // CELL)

    def _hit_box(self, clicked: tuple[int, int], origin: tuple[int, int]) -> bool:
        return origin[0] <= clicked[0] < origin[0] + BUTTON_SIZE and origin[1] <= clicked[1] < origin[1] + BUTTON_SIZE

    def _move(self, direction: str) -> None:
        delta = -1 if direction == "L" else 1
        nxt = self.pos + delta
        if not (1 <= nxt <= 5):
            return
        idx = min(self.pos, nxt) - 1
        lock = self.locks[idx]
        if lock == ".":
            self.pos = nxt
            return
        req = 1 if lock == "l" else 2
        if self.charge >= req:
            self.charge -= req
            self.pos = nxt

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

        if action == "+":
            self.charge = min(2, self.charge + 1)
        elif action == "-":
            self.charge = max(0, self.charge - 1)
        else:
            self._move(action)

        self.steps_used += 1
        self._refresh_visuals()
        self._refresh_hud()
        if self.pos == self.target:
            self.next_level()
        elif self.steps_used >= self.step_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
