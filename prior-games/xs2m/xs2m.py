"""xs2m."""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 4
PADDING_COLOR = 4
PANEL_COLOR = 1
WALL_COLOR = 5
ACID_COLOR = 8
BASE_COLOR = 9
NEUTRAL_COLOR = 14
STEP_COLOR = 14
STEP_EMPTY = 4

CELL = 4
GRID_CELLS = 16
GRID_W = GRID_CELLS * CELL
GRID_H = GRID_CELLS * CELL

BOARD_X0 = 4
BOARD_Y0 = 2
BOARD_SIZE = 7


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _board_cell(ix: int, iy: int) -> tuple[int, int]:
    return (BOARD_X0 + ix, BOARD_Y0 + iy)


def _panel_pixels() -> list[list[int]]:
    return [[PANEL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _wall_pixels() -> list[list[int]]:
    return [[WALL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _droplet_pixels(state: str) -> list[list[int]]:
    color = {"A": ACID_COLOR, "N": NEUTRAL_COLOR, "B": BASE_COLOR}[state]
    return [
        [-1, color, color, -1],
        [color, WALL_COLOR, WALL_COLOR, color],
        [color, WALL_COLOR, WALL_COLOR, color],
        [-1, color, color, -1],
    ]


def _target_pixels() -> list[list[int]]:
    return [
        [NEUTRAL_COLOR, NEUTRAL_COLOR, NEUTRAL_COLOR, NEUTRAL_COLOR],
        [NEUTRAL_COLOR, -1, -1, NEUTRAL_COLOR],
        [NEUTRAL_COLOR, -1, -1, NEUTRAL_COLOR],
        [NEUTRAL_COLOR, NEUTRAL_COLOR, NEUTRAL_COLOR, NEUTRAL_COLOR],
    ]


def _barrier_pixels(kind: str) -> list[list[int]]:
    color = BASE_COLOR if kind == "b" else ACID_COLOR
    return [
        [color, color, color, color],
        [color, -1, -1, color],
        [color, -1, -1, color],
        [color, color, color, color],
    ]


sprites = {
    "panel": Sprite(_panel_pixels(), "panel", True, False, tags=["panel"], layer=1),
    "wall": Sprite(_wall_pixels(), "wall", True, False, tags=["wall"], layer=3),
    "droplet": Sprite(_droplet_pixels("N"), "droplet", True, False, tags=["droplet"], layer=5),
    "target": Sprite(_target_pixels(), "target", True, False, tags=["target"], layer=2),
    "acid_barrier": Sprite(_barrier_pixels("a"), "acid_barrier", True, False, tags=["acid_barrier"], layer=4),
    "base_barrier": Sprite(_barrier_pixels("b"), "base_barrier", True, False, tags=["base_barrier"], layer=4),
}


def _clone(name: str, cx: int, cy: int) -> Sprite:
    return sprites[name].clone().set_position(*_cell(cx, cy))


def _build_level(
    *,
    start: tuple[int, int],
    target: tuple[int, int],
    walls: list[tuple[int, int]],
    acid_barriers: list[tuple[int, int]],
    base_barriers: list[tuple[int, int]],
    step_budget: int,
) -> Level:
    placed: list[Sprite] = []
    for cy in range(11, 16):
        for cx in range(0, GRID_CELLS):
            placed.append(_clone("panel", cx, cy))
    for iy in range(BOARD_SIZE):
        for ix in range(BOARD_SIZE):
            placed.append(_clone("panel", *_board_cell(ix, iy)))
    for ix in range(BOARD_SIZE):
        placed.append(_clone("wall", *_board_cell(ix, 0)))
        placed.append(_clone("wall", *_board_cell(ix, BOARD_SIZE - 1)))
    for iy in range(BOARD_SIZE):
        placed.append(_clone("wall", *_board_cell(0, iy)))
        placed.append(_clone("wall", *_board_cell(BOARD_SIZE - 1, iy)))
    for wall in walls:
        placed.append(_clone("wall", *_board_cell(*wall)))
    for cell in acid_barriers:
        placed.append(_clone("acid_barrier", *_board_cell(*cell)))
    for cell in base_barriers:
        placed.append(_clone("base_barrier", *_board_cell(*cell)))
    placed.append(_clone("target", *_board_cell(*target)))
    placed.append(_clone("droplet", *_board_cell(*start)))
    return Level(
        sprites=placed,
        grid_size=(GRID_W, GRID_H),
        data={
            "start": list(start),
            "target": list(target),
            "walls": [list(w) for w in walls],
            "acid_barriers": [list(c) for c in acid_barriers],
            "base_barriers": [list(c) for c in base_barriers],
            "step_budget": step_budget,
        },
    )


levels = [
    _build_level(start=(1, 3), target=(4, 3), walls=[], acid_barriers=[], base_barriers=[(2, 3)], step_budget=6),
    _build_level(
        start=(1, 4),
        target=(5, 2),
        walls=[(1, 2), (1, 3), (3, 1), (3, 3), (3, 4), (4, 1), (4, 3), (5, 3)],
        acid_barriers=[(4, 2)],
        base_barriers=[(2, 4)],
        step_budget=9,
    ),
    _build_level(
        start=(1, 1),
        target=(4, 1),
        walls=[(1, 2), (1, 4), (3, 1), (3, 2), (3, 4), (4, 4)],
        acid_barriers=[(3, 3)],
        base_barriers=[(2, 1)],
        step_budget=10,
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
            x0, y0 = _cell(idx + 1, 14)
            frame[y0 + 1 : y0 + 3, x0 + 1 : x0 + 3] = STEP_COLOR if idx < filled else STEP_EMPTY
        return frame


class Xs2m(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = StepHud()
        camera = Camera(width=GRID_W, height=GRID_H, background=BACKGROUND_COLOR, letter_box=PADDING_COLOR, interfaces=[self._hud])
        super().__init__(game_id="xs2m", levels=levels, camera=camera, available_actions=[1, 2, 3, 4, 6])

    def on_set_level(self, level: Level) -> None:
        self.pos = tuple(level.get_data("start") or [1, 1])
        self.target = tuple(level.get_data("target") or [1, 1])
        self.state = "N"
        self.step_budget = int(level.get_data("step_budget") or 1)
        self.steps_used = 0
        self.wall_cells = {tuple(w) for w in level.get_data("walls") or []}
        self.acid_cells = {tuple(c) for c in level.get_data("acid_barriers") or []}
        self.base_cells = {tuple(c) for c in level.get_data("base_barriers") or []}
        self.droplet_sprite = next(sprite for sprite in level.get_sprites() if sprite.name == "droplet")
        self.acid_sprites = {
            (sprite.x // CELL - BOARD_X0, sprite.y // CELL - BOARD_Y0): sprite
            for sprite in level.get_sprites()
            if sprite.name == "acid_barrier"
        }
        self.base_sprites = {
            (sprite.x // CELL - BOARD_X0, sprite.y // CELL - BOARD_Y0): sprite
            for sprite in level.get_sprites()
            if sprite.name == "base_barrier"
        }
        self._refresh_visuals()
        self._refresh_hud()

    def _refresh_hud(self) -> None:
        self._hud.set_state(steps_remaining=self.step_budget - self.steps_used, max_steps=self.step_budget)

    def _refresh_visuals(self) -> None:
        self.droplet_sprite.pixels = np.array(_droplet_pixels(self.state), dtype=np.int16)
        self.droplet_sprite.set_position(*_cell(*_board_cell(*self.pos)))
        for cell, sprite in self.acid_sprites.items():
            sprite.pixels = np.array(_barrier_pixels("a") if cell in self.acid_cells else [[-1] * CELL for _ in range(CELL)], dtype=np.int16)
        for cell, sprite in self.base_sprites.items():
            sprite.pixels = np.array(_barrier_pixels("b") if cell in self.base_cells else [[-1] * CELL for _ in range(CELL)], dtype=np.int16)

    def _move(self, dx: int, dy: int) -> None:
        nx, ny = self.pos[0] + dx, self.pos[1] + dy
        if not (1 <= nx <= 5 and 1 <= ny <= 5):
            return
        if (nx, ny) in self.wall_cells:
            return
        if (nx, ny) in self.base_cells:
            if self.state == "A":
                self.base_cells.remove((nx, ny))
                self.pos = (nx, ny)
                self.state = "N"
            return
        if (nx, ny) in self.acid_cells:
            if self.state == "B":
                self.acid_cells.remove((nx, ny))
                self.pos = (nx, ny)
                self.state = "N"
            return
        self.pos = (nx, ny)

    def step(self) -> None:
        aid = self.action.id
        spent_step = False
        if aid == GameAction.ACTION1:
            self._move(0, -1)
            spent_step = True
        elif aid == GameAction.ACTION2:
            self._move(0, 1)
            spent_step = True
        elif aid == GameAction.ACTION3:
            self._move(-1, 0)
            spent_step = True
        elif aid == GameAction.ACTION4:
            self._move(1, 0)
            spent_step = True
        elif aid == GameAction.ACTION6:
            self.state = {"N": "A", "A": "B", "B": "A"}[self.state]
        else:
            self.complete_action()
            return

        if spent_step:
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
