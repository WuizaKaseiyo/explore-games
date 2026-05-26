"""rt4c."""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 4
PADDING_COLOR = 4
PANEL_COLOR = 1
LANE_COLOR = 1
WALL_COLOR = 5
MEMBRANE_COLOR = 10
PORE_COLOR = 1
SMALL_COLOR = 9
SMALL_EDGE = 5
LARGE_COLOR = 8
LARGE_EDGE = 7
STEP_COLOR = 14
STEP_EMPTY = 4

CELL = 4
GRID_CELLS = 16
GRID_W = GRID_CELLS * CELL
GRID_H = GRID_CELLS * CELL

LANE_Y = 4
SLOT_TO_CELL = {1: 6, 2: 7, 4: 9, 5: 10}
MEMBRANE_CELL = 8
CONTROL_CELLS = {
    "U": (7, 0),
    "D": (7, 10),
    "L": (2, 4),
    "R": (12, 4),
}
BUTTON_SIZE = 2


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _panel_pixels() -> list[list[int]]:
    return [[PANEL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _lane_pixels() -> list[list[int]]:
    return [[LANE_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _wall_pixels() -> list[list[int]]:
    return [[WALL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _small_pixels() -> list[list[int]]:
    return [
        [-1, SMALL_COLOR, SMALL_COLOR, -1],
        [SMALL_COLOR, SMALL_EDGE, SMALL_EDGE, SMALL_COLOR],
        [SMALL_COLOR, SMALL_EDGE, SMALL_EDGE, SMALL_COLOR],
        [-1, SMALL_COLOR, SMALL_COLOR, -1],
    ]


def _large_pixels() -> list[list[int]]:
    return [
        [LARGE_COLOR, LARGE_COLOR, LARGE_COLOR, LARGE_COLOR],
        [LARGE_COLOR, LARGE_EDGE, LARGE_EDGE, LARGE_COLOR],
        [LARGE_COLOR, LARGE_EDGE, LARGE_EDGE, LARGE_COLOR],
        [LARGE_COLOR, LARGE_COLOR, LARGE_COLOR, LARGE_COLOR],
    ]


def _small_target_pixels() -> list[list[int]]:
    return [
        [SMALL_COLOR, SMALL_COLOR, SMALL_COLOR, SMALL_COLOR],
        [SMALL_COLOR, -1, -1, SMALL_COLOR],
        [SMALL_COLOR, -1, -1, SMALL_COLOR],
        [SMALL_COLOR, SMALL_COLOR, SMALL_COLOR, SMALL_COLOR],
    ]


def _large_target_pixels() -> list[list[int]]:
    return [
        [LARGE_COLOR, LARGE_COLOR, LARGE_COLOR, LARGE_COLOR],
        [LARGE_COLOR, -1, -1, LARGE_COLOR],
        [LARGE_COLOR, -1, -1, LARGE_COLOR],
        [LARGE_COLOR, LARGE_COLOR, LARGE_COLOR, LARGE_COLOR],
    ]


def _membrane_pixels(mode: str) -> list[list[int]]:
    pixels = np.full((4, 4), MEMBRANE_COLOR, dtype=np.int16)
    if mode == "narrow":
        pixels[1:3, 1:3] = PORE_COLOR
    else:
        pixels[:, 1:3] = PORE_COLOR
    return pixels.tolist()


def _button_frame(fill: int) -> np.ndarray:
    pixels = np.full((8, 8), fill, dtype=np.int16)
    pixels[0, :] = WALL_COLOR
    pixels[7, :] = WALL_COLOR
    pixels[:, 0] = WALL_COLOR
    pixels[:, 7] = WALL_COLOR
    return pixels


def _narrow_button_pixels() -> list[list[int]]:
    pixels = _button_frame(PANEL_COLOR)
    pixels[2:6, 3:5] = SMALL_COLOR
    return pixels.tolist()


def _wide_button_pixels() -> list[list[int]]:
    pixels = _button_frame(PANEL_COLOR)
    pixels[2:6, 2:6] = LARGE_COLOR
    pixels[3:5, 3:5] = LARGE_EDGE
    return pixels.tolist()


def _blower_pixels(direction: str) -> list[list[int]]:
    pixels = _button_frame(PANEL_COLOR)
    pixels[2:6, 2:6] = WALL_COLOR
    pixels[3:5, 2:6] = PANEL_COLOR
    pixels[2, 3:5] = PANEL_COLOR
    pixels[5, 3:5] = PANEL_COLOR
    if direction == "R":
        pixels[3:5, 5:7] = PANEL_COLOR
        pixels[2:6, 1] = WALL_COLOR
        return pixels.tolist()
    pixels = np.fliplr(pixels)
    pixels[3:5, 1:3] = PANEL_COLOR
    pixels[2:6, 6] = WALL_COLOR
    return pixels.tolist()


sprites = {
    "panel": Sprite(_panel_pixels(), "panel", True, False, tags=["panel"], layer=1),
    "lane": Sprite(_lane_pixels(), "lane", True, False, tags=["lane"], layer=1),
    "wall": Sprite(_wall_pixels(), "wall", True, False, tags=["wall"], layer=3),
    "small_piece": Sprite(_small_pixels(), "small_piece", True, False, tags=["small_piece"], layer=5),
    "large_piece": Sprite(_large_pixels(), "large_piece", True, False, tags=["large_piece"], layer=5),
    "small_target": Sprite(_small_target_pixels(), "small_target", True, False, tags=["small_target"], layer=2),
    "large_target": Sprite(_large_target_pixels(), "large_target", True, False, tags=["large_target"], layer=2),
    "membrane": Sprite(_membrane_pixels("narrow"), "membrane", True, False, tags=["membrane"], layer=4),
    "control_U": Sprite(_narrow_button_pixels(), "control_U", True, False, tags=["control_U"], layer=4),
    "control_D": Sprite(_wide_button_pixels(), "control_D", True, False, tags=["control_D"], layer=4),
    "control_L": Sprite(_blower_pixels("L"), "control_L", True, False, tags=["control_L"], layer=4),
    "control_R": Sprite(_blower_pixels("R"), "control_R", True, False, tags=["control_R"], layer=4),
}


def _clone(name: str, cx: int, cy: int) -> Sprite:
    return sprites[name].clone().set_position(*_cell(cx, cy))


def _build_level(
    *,
    small_start: int | None,
    small_target: int | None,
    large_start: int | None,
    large_target: int | None,
    step_budget: int,
) -> Level:
    placed: list[Sprite] = []
    for cy in range(9, 16):
        for cx in range(0, GRID_CELLS):
            placed.append(_clone("panel", cx, cy))

    for cx in range(5, 12):
        placed.append(_clone("lane", cx, LANE_Y))
    placed.append(_clone("wall", 5, LANE_Y))
    placed.append(_clone("wall", 11, LANE_Y))
    placed.append(_clone("membrane", MEMBRANE_CELL, LANE_Y))

    if small_target is not None:
        placed.append(_clone("small_target", SLOT_TO_CELL[small_target], LANE_Y))
    if large_target is not None:
        placed.append(_clone("large_target", SLOT_TO_CELL[large_target], LANE_Y))
    if small_start is not None:
        placed.append(_clone("small_piece", SLOT_TO_CELL[small_start], LANE_Y))
    if large_start is not None:
        placed.append(_clone("large_piece", SLOT_TO_CELL[large_start], LANE_Y))

    for key, cell in CONTROL_CELLS.items():
        placed.append(_clone(f"control_{key}", *cell))

    return Level(
        sprites=placed,
        grid_size=(GRID_W, GRID_H),
        data={
            "small_start": small_start,
            "small_target": small_target,
            "large_start": large_start,
            "large_target": large_target,
            "step_budget": step_budget,
        },
    )


levels = [
    _build_level(small_start=1, small_target=5, large_start=None, large_target=None, step_budget=4),
    _build_level(small_start=None, small_target=None, large_start=1, large_target=5, step_budget=5),
    _build_level(small_start=1, small_target=2, large_start=2, large_target=4, step_budget=7),
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
            frame[y0 + 1 : y0 + 3, x0 + 1 : x0 + 3] = STEP_COLOR if idx < filled else STEP_EMPTY
        return frame


class Rt4c(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = StepHud()
        camera = Camera(width=GRID_W, height=GRID_H, background=BACKGROUND_COLOR, letter_box=PADDING_COLOR, interfaces=[self._hud])
        super().__init__(game_id="rt4c", levels=levels, camera=camera, available_actions=[6])

    def on_set_level(self, level: Level) -> None:
        self.small = level.get_data("small_start")
        self.small_target = level.get_data("small_target")
        self.large = level.get_data("large_start")
        self.large_target = level.get_data("large_target")
        self.small_locked = self.small is None or self.small_target is None or self.small == self.small_target
        self.large_locked = self.large is None or self.large_target is None or self.large == self.large_target
        self.mode = "narrow"
        self.step_budget = int(level.get_data("step_budget") or 1)
        self.steps_used = 0

        self.small_sprite = next((sprite for sprite in level.get_sprites() if sprite.name == "small_piece"), None)
        self.large_sprite = next((sprite for sprite in level.get_sprites() if sprite.name == "large_piece"), None)
        self.membrane_sprite = next(sprite for sprite in level.get_sprites() if sprite.name == "membrane")
        self._refresh_visuals()
        self._refresh_hud()

    def _refresh_hud(self) -> None:
        self._hud.set_state(steps_remaining=self.step_budget - self.steps_used, max_steps=self.step_budget)

    def _refresh_visuals(self) -> None:
        self.membrane_sprite.pixels = np.array(_membrane_pixels(self.mode), dtype=np.int16)
        if self.small_sprite is not None and self.small is not None:
            self.small_sprite.set_position(*_cell(SLOT_TO_CELL[self.small], LANE_Y))
        if self.large_sprite is not None and self.large is not None:
            self.large_sprite.set_position(*_cell(SLOT_TO_CELL[self.large], LANE_Y))

    def _click_cell(self) -> tuple[int, int] | None:
        click_x = int(self.action.data.get("x", -1000))
        click_y = int(self.action.data.get("y", -1000))
        grid = self.camera.display_to_grid(click_x, click_y)
        if grid is None:
            return None
        return (grid[0] // CELL, grid[1] // CELL)

    def _hit_box(self, clicked: tuple[int, int], origin: tuple[int, int]) -> bool:
        return origin[0] <= clicked[0] < origin[0] + BUTTON_SIZE and origin[1] <= clicked[1] < origin[1] + BUTTON_SIZE

    def _move_piece(self, pos: int, others: set[int], direction: str, can_cross: bool) -> int:
        cell = pos
        while True:
            nxt = None
            if direction == "R":
                if cell == 1:
                    nxt = 2
                elif cell == 2:
                    nxt = 4 if can_cross else None
                elif cell == 4:
                    nxt = 5
            else:
                if cell == 5:
                    nxt = 4
                elif cell == 4:
                    nxt = 2 if can_cross else None
                elif cell == 2:
                    nxt = 1
            if nxt is None or nxt in others:
                break
            cell = nxt
        return cell

    def _flush(self, direction: str) -> None:
        occupied: set[int] = set()
        if self.small_locked and self.small is not None:
            occupied.add(self.small)
        if self.large_locked and self.large is not None:
            occupied.add(self.large)

        movers: list[tuple[str, int]] = []
        if not self.small_locked and self.small is not None:
            movers.append(("small", self.small))
        if not self.large_locked and self.large is not None:
            movers.append(("large", self.large))
        movers.sort(key=lambda item: -item[1] if direction == "R" else item[1])

        for name, pos in movers:
            occupied.discard(pos)
            can_cross = self.mode == "wide" or (self.mode == "narrow" and name == "small")
            new_pos = self._move_piece(pos, occupied, direction, can_cross)
            if name == "small":
                self.small = new_pos
            else:
                self.large = new_pos
            occupied.add(new_pos)

        if self.small is not None and self.small_target is not None and self.small == self.small_target:
            self.small_locked = True
        if self.large is not None and self.large_target is not None and self.large == self.large_target:
            self.large_locked = True

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

        if action == "U":
            self.mode = "narrow"
        elif action == "D":
            self.mode = "wide"
        else:
            self._flush(action)

        self.steps_used += 1
        self._refresh_visuals()
        self._refresh_hud()

        if self.small_locked and self.large_locked:
            self.next_level()
        elif self.steps_used >= self.step_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
