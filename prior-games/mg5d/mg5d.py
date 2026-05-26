"""mg5d."""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 4
PADDING_COLOR = 4
PANEL_COLOR = 1
FLOOR_COLOR = 1
WALL_COLOR = 5
BUTTON_BG = 0
BUTTON_BORDER = 5
ARROW_FG = 8
NORTH_COLOR = 8
SOUTH_COLOR = 9
CORE_COLOR = 5
RUN_COLOR = 14
STEP_COLOR = 14
STEP_EMPTY = 4

CELL = 4
GRID_CELLS = 16
GRID_W = GRID_CELLS * CELL
GRID_H = GRID_CELLS * CELL

BOARD_X0 = 3
BOARD_Y0 = 1
BOARD_SIZE = 7

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


def _board_cell(sx: int, sy: int) -> tuple[int, int]:
    return (BOARD_X0 + sx, BOARD_Y0 + sy)


def _panel_pixels() -> list[list[int]]:
    return [[PANEL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _floor_pixels() -> list[list[int]]:
    return [[FLOOR_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _wall_pixels() -> list[list[int]]:
    return [[WALL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _button_canvas(fill: int) -> np.ndarray:
    pixels = np.full((8, 8), fill, dtype=np.int16)
    pixels[0, :] = BUTTON_BORDER
    pixels[7, :] = BUTTON_BORDER
    pixels[:, 0] = BUTTON_BORDER
    pixels[:, 7] = BUTTON_BORDER
    return pixels


def _north_piece_pixels() -> list[list[int]]:
    return [
        [-1, NORTH_COLOR, NORTH_COLOR, -1],
        [NORTH_COLOR, CORE_COLOR, CORE_COLOR, NORTH_COLOR],
        [NORTH_COLOR, CORE_COLOR, CORE_COLOR, NORTH_COLOR],
        [-1, NORTH_COLOR, NORTH_COLOR, -1],
    ]


def _south_piece_pixels() -> list[list[int]]:
    return [
        [-1, SOUTH_COLOR, SOUTH_COLOR, -1],
        [SOUTH_COLOR, CORE_COLOR, CORE_COLOR, SOUTH_COLOR],
        [SOUTH_COLOR, CORE_COLOR, CORE_COLOR, SOUTH_COLOR],
        [-1, SOUTH_COLOR, SOUTH_COLOR, -1],
    ]


def _north_target_pixels() -> list[list[int]]:
    return [
        [NORTH_COLOR, NORTH_COLOR, NORTH_COLOR, NORTH_COLOR],
        [NORTH_COLOR, -1, -1, NORTH_COLOR],
        [NORTH_COLOR, -1, -1, NORTH_COLOR],
        [NORTH_COLOR, NORTH_COLOR, NORTH_COLOR, NORTH_COLOR],
    ]


def _south_target_pixels() -> list[list[int]]:
    return [
        [SOUTH_COLOR, SOUTH_COLOR, SOUTH_COLOR, SOUTH_COLOR],
        [SOUTH_COLOR, -1, -1, SOUTH_COLOR],
        [SOUTH_COLOR, -1, -1, SOUTH_COLOR],
        [SOUTH_COLOR, SOUTH_COLOR, SOUTH_COLOR, SOUTH_COLOR],
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
    pixels[3:5, 3:5] = CORE_COLOR
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
        layer=3,
    ),
    "north_piece": Sprite(
        pixels=_north_piece_pixels(),
        name="north_piece",
        visible=True,
        collidable=False,
        tags=["north_piece"],
        layer=5,
    ),
    "south_piece": Sprite(
        pixels=_south_piece_pixels(),
        name="south_piece",
        visible=True,
        collidable=False,
        tags=["south_piece"],
        layer=5,
    ),
    "north_target": Sprite(
        pixels=_north_target_pixels(),
        name="north_target",
        visible=True,
        collidable=False,
        tags=["north_target"],
        layer=2,
    ),
    "south_target": Sprite(
        pixels=_south_target_pixels(),
        name="south_target",
        visible=True,
        collidable=False,
        tags=["south_target"],
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


def _border_and_floor() -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    floors: list[tuple[int, int]] = []
    walls: list[tuple[int, int]] = []
    for sy in range(BOARD_SIZE):
        for sx in range(BOARD_SIZE):
            world = _board_cell(sx, sy)
            if sx in {0, BOARD_SIZE - 1} or sy in {0, BOARD_SIZE - 1}:
                walls.append(world)
            else:
                floors.append(world)
    return walls, floors


def _build_level(
    *,
    program_length: int,
    north_start: tuple[int, int],
    south_start: tuple[int, int],
    north_target: tuple[int, int],
    south_target: tuple[int, int],
    internal_walls: list[tuple[int, int]],
    run_budget: int,
) -> Level:
    placed: list[Sprite] = []

    for cy in range(12, 16):
        for cx in range(0, GRID_CELLS):
            placed.append(_clone("panel", cx, cy))

    border_walls, floor_cells = _border_and_floor()
    for cx, cy in floor_cells:
        placed.append(_clone("floor", cx, cy))
    for cx, cy in border_walls:
        placed.append(_clone("wall", cx, cy))

    world_internal_walls = [_board_cell(*cell) for cell in internal_walls]
    for cx, cy in world_internal_walls:
        placed.append(_clone("wall", cx, cy))

    placed.append(_clone("north_target", *_board_cell(*north_target)))
    placed.append(_clone("south_target", *_board_cell(*south_target)))
    placed.append(_clone("north_piece", *_board_cell(*north_start)))
    placed.append(_clone("south_piece", *_board_cell(*south_start)))

    for idx in range(program_length):
        placed.append(_clone(f"slot_{idx}", *SLOT_CELLS[idx]))
    placed.append(_clone("run_button", *RUN_CELL))

    return Level(
        sprites=placed,
        grid_size=(GRID_W, GRID_H),
        data={
            "program_length": program_length,
            "north_start": list(north_start),
            "south_start": list(south_start),
            "north_target": list(north_target),
            "south_target": list(south_target),
            "internal_walls": [list(cell) for cell in internal_walls],
            "run_budget": run_budget,
        },
    )


levels = [
    _build_level(
        program_length=1,
        north_start=(2, 5),
        south_start=(3, 4),
        north_target=(5, 5),
        south_target=(1, 4),
        internal_walls=[],
        run_budget=3,
    ),
    _build_level(
        program_length=3,
        north_start=(2, 4),
        south_start=(3, 5),
        north_target=(2, 1),
        south_target=(1, 4),
        internal_walls=[],
        run_budget=4,
    ),
    _build_level(
        program_length=4,
        north_start=(4, 5),
        south_start=(2, 1),
        north_target=(5, 2),
        south_target=(3, 5),
        internal_walls=[(1, 5), (5, 4)],
        run_budget=5,
    ),
]


class RunHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self.runs_remaining = 0
        self.max_runs = 1

    def set_state(self, *, runs_remaining: int, max_runs: int) -> None:
        self.runs_remaining = max(0, runs_remaining)
        self.max_runs = max(1, max_runs)

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        filled = int(round((self.runs_remaining / self.max_runs) * 6))
        for idx in range(6):
            x0, y0 = _cell(idx + 1, 0)
            color = STEP_COLOR if idx < filled else STEP_EMPTY
            frame[y0 + 1 : y0 + 3, x0 + 1 : x0 + 3] = color
        return frame


class Mg5d(NovaBaseGame):
    def __init__(self) -> None:
        self._run_hud = RunHud()
        self._anim_queue: list[tuple[tuple[int, int], tuple[int, int], bool, bool]] = []
        self._pending_run_success = False
        camera = Camera(
            width=GRID_W,
            height=GRID_H,
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._run_hud],
        )
        super().__init__(
            game_id="mg5d",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        self.program_length = int(level.get_data("program_length") or 0)
        self.north_start = tuple(level.get_data("north_start") or [0, 0])
        self.south_start = tuple(level.get_data("south_start") or [0, 0])
        self.north_target = tuple(level.get_data("north_target") or [0, 0])
        self.south_target = tuple(level.get_data("south_target") or [0, 0])
        self.run_budget = int(level.get_data("run_budget") or 1)
        self.runs_used = 0
        self.program = ["U" for _ in range(self.program_length)]
        self._anim_queue = []
        self._pending_run_success = False

        self.wall_cells = set()
        border_walls, _ = _border_and_floor()
        self.wall_cells.update(border_walls)
        self.wall_cells.update(_board_cell(*tuple(cell)) for cell in level.get_data("internal_walls") or [])

        self.slot_sprites = [
            next(sprite for sprite in level.get_sprites() if sprite.name == f"slot_{idx}")
            for idx in range(self.program_length)
        ]
        self.north_sprite = next(sprite for sprite in level.get_sprites() if sprite.name == "north_piece")
        self.south_sprite = next(sprite for sprite in level.get_sprites() if sprite.name == "south_piece")

        self._reset_objects()
        self._sync_slots()
        self._refresh_hud()

    def _refresh_hud(self) -> None:
        self._run_hud.set_state(
            runs_remaining=self.run_budget - self.runs_used,
            max_runs=self.run_budget,
        )

    def _reset_objects(self) -> None:
        self.north_cell = _board_cell(*self.north_start)
        self.south_cell = _board_cell(*self.south_start)
        self.north_locked = self.north_cell == _board_cell(*self.north_target)
        self.south_locked = self.south_cell == _board_cell(*self.south_target)
        self.north_sprite.set_position(*_cell(*self.north_cell))
        self.south_sprite.set_position(*_cell(*self.south_cell))

    def _sync_slots(self) -> None:
        for sprite, direction in zip(self.slot_sprites, self.program):
            sprite.pixels = np.array(_slot_pixels(direction), dtype=np.int16)

    def _cycle_slot(self, idx: int) -> None:
        current = self.program[idx]
        next_idx = (DIRECTION_ORDER.index(current) + 1) % len(DIRECTION_ORDER)
        self.program[idx] = DIRECTION_ORDER[next_idx]
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

    def _order_key(self, pos: tuple[int, int], dx: int, dy: int) -> int:
        return -(pos[0] * dx + pos[1] * dy)

    def _attempt_microstep(self, direction: str) -> bool:
        pieces = [
            ("north", self.north_cell, self.north_locked, DIRECTION_STEP[direction]),
            (
                "south",
                self.south_cell,
                self.south_locked,
                (-DIRECTION_STEP[direction][0], -DIRECTION_STEP[direction][1]),
            ),
        ]
        movable = [
            (self._order_key(pos, dx, dy), name, pos, dx, dy)
            for name, pos, locked, (dx, dy) in pieces
            if not locked
        ]
        movable.sort()

        occupied = {self.north_cell, self.south_cell}
        moved = False
        for _, name, pos, dx, dy in movable:
            next_cell = (pos[0] + dx, pos[1] + dy)
            if next_cell in self.wall_cells:
                continue
            occupied.remove(pos)
            if next_cell in occupied:
                occupied.add(pos)
                continue
            if name == "north":
                self.north_cell = next_cell
                if self.north_cell == _board_cell(*self.north_target):
                    self.north_locked = True
            else:
                self.south_cell = next_cell
                if self.south_cell == _board_cell(*self.south_target):
                    self.south_locked = True
            occupied.add(next_cell)
            moved = True
        return moved

    def _run_field(self) -> bool:
        self._reset_objects()
        self._anim_queue = []
        for direction in self.program:
            while self._attempt_microstep(direction):
                self._anim_queue.append(
                    (
                        self.north_cell,
                        self.south_cell,
                        self.north_locked,
                        self.south_locked,
                    )
                )
        return self.north_locked and self.south_locked

    def _advance_anim_frame(self) -> None:
        north_cell, south_cell, north_locked, south_locked = self._anim_queue.pop(0)
        self.north_cell = tuple(north_cell)
        self.south_cell = tuple(south_cell)
        self.north_locked = bool(north_locked)
        self.south_locked = bool(south_locked)
        self.north_sprite.set_position(*_cell(*self.north_cell))
        self.south_sprite.set_position(*_cell(*self.south_cell))

    def _resolve_after_run(self) -> None:
        self._refresh_hud()
        if self._pending_run_success:
            self.next_level()
            self.complete_action()
            return
        if self.runs_used >= self.run_budget:
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
        if clicked is None:
            self.complete_action()
            return

        for idx, slot_cell in enumerate(SLOT_CELLS[: self.program_length]):
            if self._hit_box(clicked, slot_cell):
                self._cycle_slot(idx)
                self.complete_action()
                return

        success = False
        if self._hit_box(clicked, RUN_CELL):
            success = self._run_field()
            self.runs_used += 1

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
        elif self._hit_box(clicked, RUN_CELL) and self.runs_used >= self.run_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
