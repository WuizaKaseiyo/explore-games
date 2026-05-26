"""pv2k."""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 4
PADDING_COLOR = 4
PANEL_COLOR = 1
FLOOR_COLOR = 1
WALL_COLOR = 5
PUMP_BODY = 3
PUMP_EDGE = 5
PUMP_PORT = 14
RED_COLOR = 8
BLUE_COLOR = 9
CORE_COLOR = 5
BLOCK_COLOR = 11
BLOCK_EDGE = 5
STEP_COLOR = 14
STEP_EMPTY = 4

CELL = 4
GRID_CELLS = 16
GRID_W = GRID_CELLS * CELL
GRID_H = GRID_CELLS * CELL

BOARD_X0 = 4
BOARD_Y0 = 3
BOARD_SIZE = 7

DIRECTION_STEP = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
}
PUMP_CELLS = {
    "L": (1, 5),
    "R": (11, 5),
    "U": (6, 1),
    "D": (6, 11),
}
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


def _piece_pixels(color: int) -> list[list[int]]:
    return [
        [-1, color, color, -1],
        [color, CORE_COLOR, CORE_COLOR, color],
        [color, CORE_COLOR, CORE_COLOR, color],
        [-1, color, color, -1],
    ]


def _target_pixels(color: int) -> list[list[int]]:
    return [
        [color, color, color, color],
        [color, -1, -1, color],
        [color, -1, -1, color],
        [color, color, color, color],
    ]


def _block_pixels() -> list[list[int]]:
    return [
        [BLOCK_COLOR, BLOCK_COLOR, BLOCK_COLOR, BLOCK_COLOR],
        [BLOCK_COLOR, BLOCK_EDGE, BLOCK_EDGE, BLOCK_COLOR],
        [BLOCK_COLOR, BLOCK_EDGE, BLOCK_EDGE, BLOCK_COLOR],
        [BLOCK_COLOR, BLOCK_COLOR, BLOCK_COLOR, BLOCK_COLOR],
    ]


def _pump_pixels(direction: str) -> list[list[int]]:
    pixels = np.full((8, 8), PUMP_BODY, dtype=np.int16)
    pixels[0, :] = PUMP_EDGE
    pixels[7, :] = PUMP_EDGE
    pixels[:, 0] = PUMP_EDGE
    pixels[:, 7] = PUMP_EDGE
    pixels[2:6, 2:6] = PANEL_COLOR
    pixels[3:5, 1:3] = PUMP_BODY
    pixels[3:5, 5:7] = PUMP_BODY
    pixels[2:6, 3:5] = PUMP_BODY
    pixels[3:5, 6] = PUMP_PORT
    if direction == "R":
        return pixels.tolist()
    if direction == "L":
        return np.fliplr(pixels).tolist()
    if direction == "U":
        return np.rot90(pixels, 1).tolist()
    return np.rot90(pixels, 3).tolist()


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
    "red_piece": Sprite(
        pixels=_piece_pixels(RED_COLOR),
        name="red_piece",
        visible=True,
        collidable=False,
        tags=["red_piece"],
        layer=5,
    ),
    "blue_piece": Sprite(
        pixels=_piece_pixels(BLUE_COLOR),
        name="blue_piece",
        visible=True,
        collidable=False,
        tags=["blue_piece"],
        layer=5,
    ),
    "red_target": Sprite(
        pixels=_target_pixels(RED_COLOR),
        name="red_target",
        visible=True,
        collidable=False,
        tags=["red_target"],
        layer=2,
    ),
    "blue_target": Sprite(
        pixels=_target_pixels(BLUE_COLOR),
        name="blue_target",
        visible=True,
        collidable=False,
        tags=["blue_target"],
        layer=2,
    ),
    "block": Sprite(
        pixels=_block_pixels(),
        name="block",
        visible=True,
        collidable=False,
        tags=["block"],
        layer=4,
    ),
    "pump_L": Sprite(
        pixels=_pump_pixels("L"),
        name="pump_L",
        visible=True,
        collidable=False,
        tags=["pump_L"],
        layer=4,
    ),
    "pump_R": Sprite(
        pixels=_pump_pixels("R"),
        name="pump_R",
        visible=True,
        collidable=False,
        tags=["pump_R"],
        layer=4,
    ),
    "pump_U": Sprite(
        pixels=_pump_pixels("U"),
        name="pump_U",
        visible=True,
        collidable=False,
        tags=["pump_U"],
        layer=4,
    ),
    "pump_D": Sprite(
        pixels=_pump_pixels("D"),
        name="pump_D",
        visible=True,
        collidable=False,
        tags=["pump_D"],
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
            cell = _board_cell(sx, sy)
            if sx in {0, BOARD_SIZE - 1} or sy in {0, BOARD_SIZE - 1}:
                walls.append(cell)
            else:
                floors.append(cell)
    return walls, floors


def _build_level(
    *,
    red_start: tuple[int, int],
    red_target: tuple[int, int],
    blue_start: tuple[int, int] | None,
    blue_target: tuple[int, int] | None,
    block_start: tuple[int, int] | None,
    internal_walls: list[tuple[int, int]],
    pulse_budget: int,
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

    placed.append(_clone("red_target", *_board_cell(*red_target)))
    placed.append(_clone("red_piece", *_board_cell(*red_start)))
    if blue_target is not None:
        placed.append(_clone("blue_target", *_board_cell(*blue_target)))
    if blue_start is not None:
        placed.append(_clone("blue_piece", *_board_cell(*blue_start)))
    if block_start is not None:
        placed.append(_clone("block", *_board_cell(*block_start)))

    for direction, cell in PUMP_CELLS.items():
        placed.append(_clone(f"pump_{direction}", *cell))

    return Level(
        sprites=placed,
        grid_size=(GRID_W, GRID_H),
        data={
            "red_start": list(red_start),
            "red_target": list(red_target),
            "blue_start": list(blue_start) if blue_start is not None else None,
            "blue_target": list(blue_target) if blue_target is not None else None,
            "block_start": list(block_start) if block_start is not None else None,
            "internal_walls": [list(wall) for wall in internal_walls],
            "pulse_budget": pulse_budget,
        },
    )


levels = [
    _build_level(
        red_start=(2, 1),
        red_target=(5, 1),
        blue_start=None,
        blue_target=None,
        block_start=None,
        internal_walls=[],
        pulse_budget=4,
    ),
    _build_level(
        red_start=(1, 5),
        red_target=(1, 4),
        blue_start=None,
        blue_target=None,
        block_start=(1, 4),
        internal_walls=[(2, 5)],
        pulse_budget=4,
    ),
    _build_level(
        red_start=(4, 2),
        red_target=(1, 3),
        blue_start=(2, 4),
        blue_target=(5, 5),
        block_start=(3, 2),
        internal_walls=[(5, 3), (4, 5), (1, 5)],
        pulse_budget=8,
    ),
]


class PulseHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self.pulses_remaining = 0
        self.max_pulses = 1

    def set_state(self, *, pulses_remaining: int, max_pulses: int) -> None:
        self.pulses_remaining = max(0, pulses_remaining)
        self.max_pulses = max(1, max_pulses)

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        filled = int(round((self.pulses_remaining / self.max_pulses) * 6))
        for idx in range(6):
            x0, y0 = _cell(idx + 1, 0)
            color = STEP_COLOR if idx < filled else STEP_EMPTY
            frame[y0 + 1 : y0 + 3, x0 + 1 : x0 + 3] = color
        return frame


class Pv2k(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = PulseHud()
        self._anim_queue: list[tuple[tuple[int, int], tuple[int, int] | None, tuple[int, int] | None, bool, bool]] = []
        self._pending_success = False
        camera = Camera(
            width=GRID_W,
            height=GRID_H,
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._hud],
        )
        super().__init__(
            game_id="pv2k",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        self.red_start = tuple(level.get_data("red_start") or [0, 0])
        self.red_target = tuple(level.get_data("red_target") or [0, 0])
        raw_blue_start = level.get_data("blue_start")
        raw_blue_target = level.get_data("blue_target")
        raw_block_start = level.get_data("block_start")
        self.blue_start = tuple(raw_blue_start) if raw_blue_start is not None else None
        self.blue_target = tuple(raw_blue_target) if raw_blue_target is not None else None
        self.block_start = tuple(raw_block_start) if raw_block_start is not None else None
        self.pulse_budget = int(level.get_data("pulse_budget") or 1)
        self.pulses_used = 0
        self._pending_success = False
        self._anim_queue = []

        border_walls, _ = _border_and_floor()
        self.wall_cells = set(border_walls)
        self.wall_cells.update(_board_cell(*tuple(wall)) for wall in level.get_data("internal_walls") or [])

        self.red_sprite = next(sprite for sprite in level.get_sprites() if sprite.name == "red_piece")
        blue_sprites = [sprite for sprite in level.get_sprites() if sprite.name == "blue_piece"]
        self.blue_sprite = blue_sprites[0] if blue_sprites else None
        block_sprites = [sprite for sprite in level.get_sprites() if sprite.name == "block"]
        self.block_sprite = block_sprites[0] if block_sprites else None

        self._reset_objects()
        self._refresh_hud()

    def _refresh_hud(self) -> None:
        self._hud.set_state(
            pulses_remaining=self.pulse_budget - self.pulses_used,
            max_pulses=self.pulse_budget,
        )

    def _reset_objects(self) -> None:
        self.red_cell = _board_cell(*self.red_start)
        self.red_locked = self.red_cell == _board_cell(*self.red_target)
        self.red_sprite.set_position(*_cell(*self.red_cell))

        if self.blue_sprite is not None and self.blue_start is not None and self.blue_target is not None:
            self.blue_cell = _board_cell(*self.blue_start)
            self.blue_locked = self.blue_cell == _board_cell(*self.blue_target)
            self.blue_sprite.set_position(*_cell(*self.blue_cell))
        else:
            self.blue_cell = None
            self.blue_locked = True

        if self.block_sprite is not None and self.block_start is not None:
            self.block_cell = _board_cell(*self.block_start)
            self.block_sprite.set_position(*_cell(*self.block_cell))
        else:
            self.block_cell = None

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

    def _attempt_microstep(self, direction: str, block_available: bool) -> tuple[bool, bool]:
        dx, dy = DIRECTION_STEP[direction]
        occupied = {self.red_cell}
        if self.blue_cell is not None:
            occupied.add(self.blue_cell)
        if self.block_cell is not None:
            occupied.add(self.block_cell)

        movers: list[tuple[int, str]] = []
        if not self.red_locked:
            movers.append((self._order_key(self.red_cell, dx, dy), "red"))
        if self.blue_cell is not None and not self.blue_locked:
            movers.append((self._order_key(self.blue_cell, dx, dy), "blue"))
        if self.block_cell is not None and block_available:
            movers.append((self._order_key(self.block_cell, dx, dy), "block"))
        movers.sort()

        moved_any = False
        block_moved = False
        for _, name in movers:
            if name == "red":
                current = self.red_cell
            elif name == "blue":
                current = self.blue_cell
                if current is None:
                    continue
            else:
                current = self.block_cell
                if current is None:
                    continue

            next_cell = (current[0] + dx, current[1] + dy)
            occupied.remove(current)
            if next_cell in self.wall_cells or next_cell in occupied:
                occupied.add(current)
                continue

            if name == "red":
                self.red_cell = next_cell
                if self.red_cell == _board_cell(*self.red_target):
                    self.red_locked = True
            elif name == "blue":
                self.blue_cell = next_cell
                if self.blue_target is not None and self.blue_cell == _board_cell(*self.blue_target):
                    self.blue_locked = True
            else:
                self.block_cell = next_cell
                block_moved = True

            occupied.add(next_cell)
            moved_any = True

        return moved_any, block_moved

    def _apply_pulse(self, direction: str) -> bool:
        self._anim_queue = []
        block_available = self.block_cell is not None
        while True:
            moved_any, block_moved = self._attempt_microstep(direction, block_available)
            if not moved_any:
                break
            if block_moved:
                block_available = False
            self._anim_queue.append(
                (
                    self.red_cell,
                    self.blue_cell,
                    self.block_cell,
                    self.red_locked,
                    self.blue_locked,
                )
            )

        return self.red_locked and self.blue_locked

    def _advance_anim_frame(self) -> None:
        red_cell, blue_cell, block_cell, red_locked, blue_locked = self._anim_queue.pop(0)
        self.red_cell = tuple(red_cell)
        self.red_locked = bool(red_locked)
        self.red_sprite.set_position(*_cell(*self.red_cell))

        self.blue_locked = bool(blue_locked)
        if blue_cell is not None:
            self.blue_cell = tuple(blue_cell)
            if self.blue_sprite is not None:
                self.blue_sprite.set_position(*_cell(*self.blue_cell))
        else:
            self.blue_cell = None

        if block_cell is not None:
            self.block_cell = tuple(block_cell)
            if self.block_sprite is not None:
                self.block_sprite.set_position(*_cell(*self.block_cell))
        else:
            self.block_cell = None

    def _resolve_after_pulse(self) -> None:
        self._refresh_hud()
        if self._pending_success:
            self.next_level()
            self.complete_action()
            return
        if self.pulses_used >= self.pulse_budget:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def step(self) -> None:
        if self._anim_queue:
            self._advance_anim_frame()
            if self._anim_queue:
                return
            self._resolve_after_pulse()
            return

        clicked = self._click_cell()
        if clicked is None:
            self.complete_action()
            return

        direction = None
        for candidate, origin in PUMP_CELLS.items():
            if self._hit_box(clicked, origin):
                direction = candidate
                break

        if direction is None:
            self.complete_action()
            return

        success = self._apply_pulse(direction)
        self.pulses_used += 1
        self._pending_success = success
        self._refresh_hud()
        if self._anim_queue:
            self._advance_anim_frame()
            if self._anim_queue:
                return
            self._resolve_after_pulse()
            return
        if success:
            self.next_level()
        elif self.pulses_used >= self.pulse_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
