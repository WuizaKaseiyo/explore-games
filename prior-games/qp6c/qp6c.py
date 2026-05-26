"""qp6c."""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 4
PADDING_COLOR = 4
PANEL_COLOR = 1
WALL_COLOR = 5
BUTTON_BG = 0
BUTTON_BORDER = 5
ARROW_FG = 8
BALL_COLOR = 12
BALL_CORE = 8
CRATE_COLOR = 11
CRATE_EDGE = 5
GOAL_COLOR = 8
DOCK_COLOR = 14
RUN_COLOR = 14
STEP_COLOR = 14
STEP_EMPTY = 4

CELL = 4
GRID_CELLS = 16
GRID_W = GRID_CELLS * CELL
GRID_H = GRID_CELLS * CELL

CHAMBER_X0 = 3
CHAMBER_X1 = 12
CHAMBER_Y0 = 1
CHAMBER_Y1 = 10

DIRECTION_ORDER = ["U", "R", "D", "L"]
DIRECTION_STEP = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
}
SLOT_CELLS = [(1, 12), (4, 12), (7, 12), (10, 12)]
RUN_CELL = (13, 12)
BUTTON_SIZE = 2


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _panel_pixels() -> list[list[int]]:
    return [
        [PANEL_COLOR, PANEL_COLOR, PANEL_COLOR, PANEL_COLOR],
        [PANEL_COLOR, PANEL_COLOR, PANEL_COLOR, PANEL_COLOR],
        [PANEL_COLOR, PANEL_COLOR, PANEL_COLOR, PANEL_COLOR],
        [PANEL_COLOR, PANEL_COLOR, PANEL_COLOR, PANEL_COLOR],
    ]


def _button_canvas(fill: int) -> np.ndarray:
    pixels = np.full((8, 8), fill, dtype=np.int16)
    pixels[0, :] = BUTTON_BORDER
    pixels[7, :] = BUTTON_BORDER
    pixels[:, 0] = BUTTON_BORDER
    pixels[:, 7] = BUTTON_BORDER
    return pixels


def _wall_pixels() -> list[list[int]]:
    return [
        [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
        [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
        [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
        [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
    ]


def _ball_pixels() -> list[list[int]]:
    return [
        [-1, BALL_COLOR, BALL_COLOR, -1],
        [BALL_COLOR, BALL_CORE, BALL_CORE, BALL_COLOR],
        [BALL_COLOR, BALL_CORE, BALL_CORE, BALL_COLOR],
        [-1, BALL_COLOR, BALL_COLOR, -1],
    ]


def _crate_pixels(*, docked: bool = False) -> list[list[int]]:
    if docked:
        return [
            [DOCK_COLOR, DOCK_COLOR, DOCK_COLOR, DOCK_COLOR],
            [DOCK_COLOR, CRATE_COLOR, CRATE_COLOR, DOCK_COLOR],
            [DOCK_COLOR, CRATE_COLOR, CRATE_COLOR, DOCK_COLOR],
            [DOCK_COLOR, DOCK_COLOR, DOCK_COLOR, DOCK_COLOR],
        ]
    return [
        [-1, CRATE_COLOR, CRATE_COLOR, -1],
        [CRATE_COLOR, CRATE_EDGE, CRATE_EDGE, CRATE_COLOR],
        [CRATE_COLOR, CRATE_EDGE, CRATE_EDGE, CRATE_COLOR],
        [-1, CRATE_COLOR, CRATE_COLOR, -1],
    ]


def _goal_pixels() -> list[list[int]]:
    return [
        [GOAL_COLOR, BALL_COLOR, BALL_COLOR, GOAL_COLOR],
        [BALL_COLOR, -1, -1, BALL_COLOR],
        [BALL_COLOR, -1, -1, BALL_COLOR],
        [GOAL_COLOR, BALL_COLOR, BALL_COLOR, GOAL_COLOR],
    ]


def _dock_pixels() -> list[list[int]]:
    return [
        [DOCK_COLOR, DOCK_COLOR, DOCK_COLOR, DOCK_COLOR],
        [DOCK_COLOR, -1, -1, DOCK_COLOR],
        [DOCK_COLOR, -1, -1, DOCK_COLOR],
        [DOCK_COLOR, DOCK_COLOR, DOCK_COLOR, DOCK_COLOR],
    ]


def _slot_pixels(direction: str) -> list[list[int]]:
    pixels = _button_canvas(BUTTON_BG)
    base_up = [
        (3, 2),
        (4, 2),
        (2, 3),
        (5, 3),
        (1, 4),
        (6, 4),
    ]
    for x, y in base_up:
        pixels[y, x] = ARROW_FG

    if direction == "U":
        return pixels.tolist()
    if direction == "R":
        pixels = np.rot90(pixels, 3)
    elif direction == "D":
        pixels = np.rot90(pixels, 2)
    else:
        pixels = np.rot90(pixels, 1)
    return pixels.tolist()


def _run_pixels() -> list[list[int]]:
    pixels = _button_canvas(RUN_COLOR)
    pixels[3:5, 3:5] = 5
    return pixels.tolist()


sprites = {
    "panel": Sprite(
        pixels=_panel_pixels(),
        name="panel",
        visible=True,
        collidable=False,
        tags=["panel"],
        layer=1,
    ),
    "wall": Sprite(
        pixels=_wall_pixels(),
        name="wall",
        visible=True,
        collidable=False,
        tags=["wall"],
        layer=3,
    ),
    "ball": Sprite(
        pixels=_ball_pixels(),
        name="ball",
        visible=True,
        collidable=False,
        tags=["ball"],
        layer=5,
    ),
    "crate": Sprite(
        pixels=_crate_pixels(),
        name="crate",
        visible=True,
        collidable=False,
        tags=["crate"],
        layer=5,
    ),
    "goal": Sprite(
        pixels=_goal_pixels(),
        name="goal",
        visible=True,
        collidable=False,
        tags=["goal"],
        layer=2,
    ),
    "dock": Sprite(
        pixels=_dock_pixels(),
        name="dock",
        visible=True,
        collidable=False,
        tags=["dock"],
        layer=2,
    ),
    "run_button": Sprite(
        pixels=_run_pixels(),
        name="run_button",
        visible=True,
        collidable=False,
        tags=["run_button"],
        layer=4,
    ),
    "slot_0": Sprite(
        pixels=_slot_pixels("U"),
        name="slot_0",
        visible=True,
        collidable=False,
        tags=["slot_0"],
        layer=4,
    ),
    "slot_1": Sprite(
        pixels=_slot_pixels("U"),
        name="slot_1",
        visible=True,
        collidable=False,
        tags=["slot_1"],
        layer=4,
    ),
    "slot_2": Sprite(
        pixels=_slot_pixels("U"),
        name="slot_2",
        visible=True,
        collidable=False,
        tags=["slot_2"],
        layer=4,
    ),
    "slot_3": Sprite(
        pixels=_slot_pixels("U"),
        name="slot_3",
        visible=True,
        collidable=False,
        tags=["slot_3"],
        layer=4,
    ),
}


def _clone(name: str, cx: int, cy: int) -> Sprite:
    return sprites[name].clone().set_position(*_cell(cx, cy))


def _build_level(
    *,
    program_length: int,
    ball_start: tuple[int, int],
    crate_starts: list[tuple[int, int]],
    goal_cell: tuple[int, int],
    dock_cells: list[tuple[int, int]],
    internal_walls: list[tuple[int, int]],
    step_budget: int,
) -> Level:
    placed: list[Sprite] = []

    for cy in range(12, 16):
        for cx in range(0, GRID_CELLS):
            placed.append(_clone("panel", cx, cy))

    border_walls = []
    for x in range(CHAMBER_X0, CHAMBER_X1 + 1):
        border_walls.append((x, CHAMBER_Y0))
        border_walls.append((x, CHAMBER_Y1))
    for y in range(CHAMBER_Y0 + 1, CHAMBER_Y1):
        border_walls.append((CHAMBER_X0, y))
        border_walls.append((CHAMBER_X1, y))
    for cx, cy in border_walls:
        placed.append(_clone("wall", cx, cy))
    for cx, cy in internal_walls:
        placed.append(_clone("wall", cx, cy))

    placed.append(_clone("goal", *goal_cell))
    for cx, cy in dock_cells:
        placed.append(_clone("dock", cx, cy))
    placed.append(_clone("ball", *ball_start))
    for cx, cy in crate_starts:
        placed.append(_clone("crate", cx, cy))

    for i in range(program_length):
        placed.append(_clone(f"slot_{i}", *SLOT_CELLS[i]))
    placed.append(_clone("run_button", *RUN_CELL))

    return Level(
        sprites=placed,
        grid_size=(GRID_W, GRID_H),
        data={
            "program_length": program_length,
            "ball_start": list(ball_start),
            "crate_starts": [list(c) for c in crate_starts],
            "goal_cell": list(goal_cell),
            "dock_cells": [list(c) for c in dock_cells],
            "internal_walls": [list(c) for c in internal_walls],
            "step_budget": step_budget,
        },
    )


levels = [
    _build_level(
        program_length=2,
        ball_start=(4, 7),
        crate_starts=[],
        goal_cell=(10, 3),
        dock_cells=[],
        internal_walls=[(10, 2), (11, 7)],
        step_budget=6,
    ),
    _build_level(
        program_length=2,
        ball_start=(4, 7),
        crate_starts=[(7, 7)],
        goal_cell=(8, 9),
        dock_cells=[],
        internal_walls=[(10, 9)],
        step_budget=6,
    ),
    _build_level(
        program_length=4,
        ball_start=(4, 7),
        crate_starts=[(7, 7)],
        goal_cell=(8, 3),
        dock_cells=[(6, 3)],
        internal_walls=[(4, 2), (7, 2), (8, 4), (9, 3)],
        step_budget=12,
    ),
]


class TraceHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self.trace_cells: list[tuple[int, int]] = []
        self.steps_remaining = 0
        self.max_steps = 1

    def set_state(
        self,
        *,
        trace_cells: list[tuple[int, int]],
        steps_remaining: int,
        max_steps: int,
    ) -> None:
        self.trace_cells = list(trace_cells)
        self.steps_remaining = max(0, steps_remaining)
        self.max_steps = max(1, max_steps)

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        filled = int(round((self.steps_remaining / self.max_steps) * 6))
        for idx in range(6):
            x0, y0 = _cell(idx + 1, 0)
            color = STEP_COLOR if idx < filled else STEP_EMPTY
            frame[y0 + 1 : y0 + 3, x0 + 1 : x0 + 3] = color
        return frame


class Qp6c(NovaBaseGame):
    def __init__(self) -> None:
        self._trace_hud = TraceHud()
        self._anim_queue: list[tuple[tuple[int, int], list[tuple[int, int]], list[bool]]] = []
        self._pending_run_success = False
        camera = Camera(
            width=GRID_W,
            height=GRID_H,
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._trace_hud],
        )
        super().__init__(
            game_id="qp6c",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        self.program_length = int(level.get_data("program_length") or 0)
        self.ball_start = tuple(level.get_data("ball_start") or [0, 0])
        self.crate_starts = [tuple(c) for c in level.get_data("crate_starts") or []]
        self.goal_cell = tuple(level.get_data("goal_cell") or [0, 0])
        self.dock_cells = {tuple(c) for c in level.get_data("dock_cells") or []}
        self.internal_walls = {tuple(c) for c in level.get_data("internal_walls") or []}
        self.wall_cells = set(self.internal_walls)
        for x in range(CHAMBER_X0, CHAMBER_X1 + 1):
            self.wall_cells.add((x, CHAMBER_Y0))
            self.wall_cells.add((x, CHAMBER_Y1))
        for y in range(CHAMBER_Y0 + 1, CHAMBER_Y1):
            self.wall_cells.add((CHAMBER_X0, y))
            self.wall_cells.add((CHAMBER_X1, y))
        self.step_budget = int(level.get_data("step_budget") or 1)
        self.steps_used = 0
        self.trace_cells: list[tuple[int, int]] = []
        self.program = ["U" for _ in range(self.program_length)]
        self._anim_queue = []
        self._pending_run_success = False

        self.slot_sprites = []
        for i in range(self.program_length):
            self.slot_sprites.append(next(s for s in level.get_sprites() if s.name == f"slot_{i}"))
        self.ball_sprite = next(s for s in level.get_sprites() if s.name == "ball")
        self.crate_sprites = [s for s in level.get_sprites() if s.name == "crate"]

        self._reset_objects()
        self._sync_slots()
        self._refresh_hud()

    def _refresh_hud(self) -> None:
        self._trace_hud.set_state(
            trace_cells=self.trace_cells,
            steps_remaining=self.step_budget - self.steps_used,
            max_steps=self.step_budget,
        )

    def _reset_objects(self) -> None:
        self.ball_cell = self.ball_start
        self.crates = [tuple(c) for c in self.crate_starts]
        self.docked = [False for _ in self.crates]
        self.ball_sprite.set_position(*_cell(*self.ball_cell))
        for idx, (sprite, cell) in enumerate(zip(self.crate_sprites, self.crates)):
            sprite.pixels = np.array(_crate_pixels(docked=self.docked[idx]), dtype=np.int16)
            sprite.set_position(*_cell(*cell))

    def _sync_slots(self) -> None:
        for sprite, direction in zip(self.slot_sprites, self.program):
            sprite.pixels = np.array(_slot_pixels(direction), dtype=np.int16)

    def _cycle_slot(self, idx: int) -> None:
        current = self.program[idx]
        next_idx = (DIRECTION_ORDER.index(current) + 1) % len(DIRECTION_ORDER)
        self.program[idx] = DIRECTION_ORDER[next_idx]
        self.trace_cells = []
        self._sync_slots()

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

    def _order_key(self, pos: tuple[int, int], direction: str) -> int:
        x, y = pos
        if direction == "R":
            return -x
        if direction == "L":
            return x
        if direction == "D":
            return -y
        return y

    def _in_bounds(self, cell: tuple[int, int]) -> bool:
        x, y = cell
        return CHAMBER_X0 <= x <= CHAMBER_X1 and CHAMBER_Y0 <= y <= CHAMBER_Y1

    def _run_gravity(self) -> bool:
        self._reset_objects()
        self.trace_cells = []
        self._anim_queue = []
        for direction in self.program:
            dx, dy = DIRECTION_STEP[direction]
            while True:
                moved = False
                objects: list[tuple[str, tuple[int, int]]] = [("ball", self.ball_cell)]
                objects.extend(
                    (f"crate_{idx}", self.crates[idx])
                    for idx in range(len(self.crates))
                    if not self.docked[idx]
                )
                objects.sort(key=lambda item: self._order_key(item[1], direction))
                occupied = set(self.crates + [self.ball_cell])
                for name, pos in objects:
                    next_cell = (pos[0] + dx, pos[1] + dy)
                    if not self._in_bounds(next_cell):
                        continue
                    if next_cell in self.wall_cells:
                        continue
                    occupied.remove(pos)
                    if next_cell in occupied:
                        occupied.add(pos)
                        continue
                    if name == "ball":
                        self.ball_cell = next_cell
                    else:
                        idx = int(name.split("_")[1])
                        self.crates[idx] = next_cell
                        if next_cell in self.dock_cells:
                            self.docked[idx] = True
                    occupied.add(next_cell)
                    moved = True
                if not moved:
                    break
                self._anim_queue.append(
                    (
                        self.ball_cell,
                        [tuple(cell) for cell in self.crates],
                        [bool(flag) for flag in self.docked],
                    )
                )

        crate_cells = set(self.crates)
        return self.ball_cell == self.goal_cell and all(dock in crate_cells for dock in self.dock_cells)

    def _advance_anim_frame(self) -> None:
        ball_cell, crates, docked = self._anim_queue.pop(0)
        self.ball_cell = tuple(ball_cell)
        self.crates = [tuple(cell) for cell in crates]
        self.docked = [bool(flag) for flag in docked]
        self.ball_sprite.set_position(*_cell(*self.ball_cell))
        for idx, (sprite, cell) in enumerate(zip(self.crate_sprites, self.crates)):
            sprite.pixels = np.array(_crate_pixels(docked=self.docked[idx]), dtype=np.int16)
            sprite.set_position(*_cell(*cell))

    def _resolve_after_run(self) -> None:
        self._refresh_hud()
        if self._pending_run_success:
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
            self._resolve_after_run()
            return

        clicked = self._click_cell()
        success = False
        spent_step = False
        if clicked is not None:
            if self._hit_box(clicked, RUN_CELL):
                success = self._run_gravity()
                spent_step = True
            else:
                for idx, slot_cell in enumerate(SLOT_CELLS[: self.program_length]):
                    if self._hit_box(clicked, slot_cell):
                        self._cycle_slot(idx)
                        spent_step = True
                        break

        if spent_step:
            self.steps_used += 1
        self._pending_run_success = success
        self._refresh_hud()
        if self._anim_queue:
            self._advance_anim_frame()
            if self._anim_queue:
                return
            self._resolve_after_run()
            return
        if success:
            self.next_level()
        elif spent_step and self.steps_used >= self.step_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
