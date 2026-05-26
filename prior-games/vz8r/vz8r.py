"""vz8r."""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 4
PADDING_COLOR = 4
PANEL_COLOR = 1
WALL_COLOR = 5
THIN_COLOR = 10
THICK_COLOR = 3
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

PATH = [
    (2, 2),
    (3, 2),
    (4, 2),
    (5, 2),
    (5, 3),
    (5, 4),
    (6, 4),
    (7, 4),
    (8, 4),
    (8, 5),
    (8, 6),
    (9, 6),
    (10, 6),
    (11, 6),
]
CONTROL_CELLS = {
    "T": (4, 10),
    "G": (8, 10),
    "L": (1, 4),
    "R": (12, 4),
}
BUTTON_SIZE = 2


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _panel_pixels() -> list[list[int]]:
    return [[PANEL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _track_pixels(color: int) -> list[list[int]]:
    return [[color for _ in range(CELL)] for _ in range(CELL)]


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


def _button_pixels(fill: int) -> list[list[int]]:
    return [
        [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
        [WALL_COLOR, fill, fill, fill, fill, fill, fill, WALL_COLOR],
        [WALL_COLOR, fill, fill, fill, fill, fill, fill, WALL_COLOR],
        [WALL_COLOR, fill, fill, fill, fill, fill, fill, WALL_COLOR],
        [WALL_COLOR, fill, fill, fill, fill, fill, fill, WALL_COLOR],
        [WALL_COLOR, fill, fill, fill, fill, fill, fill, WALL_COLOR],
        [WALL_COLOR, fill, fill, fill, fill, fill, fill, WALL_COLOR],
        [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
    ]


sprites = {
    "panel": Sprite(_panel_pixels(), "panel", True, False, tags=["panel"], layer=1),
    "track": Sprite(_track_pixels(THIN_COLOR), "track", True, False, tags=["track"], layer=1),
    "red_piece": Sprite(_piece_pixels(RED_COLOR), "red_piece", True, False, tags=["red_piece"], layer=5),
    "blue_piece": Sprite(_piece_pixels(BLUE_COLOR), "blue_piece", True, False, tags=["blue_piece"], layer=5),
    "red_target": Sprite(_target_pixels(RED_COLOR), "red_target", True, False, tags=["red_target"], layer=3),
    "blue_target": Sprite(_target_pixels(BLUE_COLOR), "blue_target", True, False, tags=["blue_target"], layer=3),
    "block": Sprite(_block_pixels(), "block", True, False, tags=["block"], layer=4),
    "control_T": Sprite(_button_pixels(THIN_COLOR), "control_T", True, False, tags=["control_T"], layer=4),
    "control_G": Sprite(_button_pixels(THICK_COLOR), "control_G", True, False, tags=["control_G"], layer=4),
    "control_L": Sprite(_button_pixels(THICK_COLOR), "control_L", True, False, tags=["control_L"], layer=4),
    "control_R": Sprite(_button_pixels(THICK_COLOR), "control_R", True, False, tags=["control_R"], layer=4),
}


def _clone(name: str, cx: int, cy: int) -> Sprite:
    return sprites[name].clone().set_position(*_cell(cx, cy))


def _path_cell(idx: int) -> tuple[int, int]:
    px, py = PATH[idx - 1]
    return (px, py)


def _build_level(
    *,
    mode: str,
    red_start: int,
    red_target: int,
    blue_start: int | None,
    blue_target: int | None,
    block_start: int | None,
    step_budget: int,
) -> Level:
    placed: list[Sprite] = []
    for cy in range(9, 16):
        for cx in range(0, GRID_CELLS):
            placed.append(_clone("panel", cx, cy))
    for x, y in PATH:
        placed.append(_clone("track", x, y))
    placed.append(_clone("red_target", *_path_cell(red_target)))
    placed.append(_clone("red_piece", *_path_cell(red_start)))
    if blue_target is not None:
        placed.append(_clone("blue_target", *_path_cell(blue_target)))
    if blue_start is not None:
        placed.append(_clone("blue_piece", *_path_cell(blue_start)))
    if block_start is not None:
        placed.append(_clone("block", *_path_cell(block_start)))
    for key, cell in CONTROL_CELLS.items():
        placed.append(_clone(f"control_{key}", *cell))
    return Level(
        sprites=placed,
        grid_size=(GRID_W, GRID_H),
        data={
            "mode": mode,
            "red_start": red_start,
            "red_target": red_target,
            "blue_start": blue_start,
            "blue_target": blue_target,
            "block_start": block_start,
            "step_budget": step_budget,
        },
    )


levels = [
    _build_level(mode="thin", red_start=5, red_target=4, blue_start=None, blue_target=None, block_start=None, step_budget=5),
    _build_level(mode="thick", red_start=2, red_target=11, blue_start=None, blue_target=None, block_start=8, step_budget=8),
    _build_level(mode="thin", red_start=4, red_target=2, blue_start=7, blue_target=14, block_start=None, step_budget=8),
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


class Vz8r(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = StepHud()
        camera = Camera(width=GRID_W, height=GRID_H, background=BACKGROUND_COLOR, letter_box=PADDING_COLOR, interfaces=[self._hud])
        super().__init__(game_id="vz8r", levels=levels, camera=camera, available_actions=[6])

    def on_set_level(self, level: Level) -> None:
        self.mode = str(level.get_data("mode") or "thin")
        self.red = int(level.get_data("red_start") or 1)
        self.red_target = int(level.get_data("red_target") or 1)
        raw_blue = level.get_data("blue_start")
        raw_blue_target = level.get_data("blue_target")
        raw_block = level.get_data("block_start")
        self.blue = int(raw_blue) if raw_blue is not None else None
        self.blue_target = int(raw_blue_target) if raw_blue_target is not None else None
        self.block = int(raw_block) if raw_block is not None else None
        self.red_locked = self.red == self.red_target
        self.blue_locked = self.blue is not None and self.blue_target is not None and self.blue == self.blue_target
        self.step_budget = int(level.get_data("step_budget") or 1)
        self.steps_used = 0
        self.red_sprite = next(s for s in level.get_sprites() if s.name == "red_piece")
        self.blue_sprite = next((s for s in level.get_sprites() if s.name == "blue_piece"), None)
        self.block_sprite = next((s for s in level.get_sprites() if s.name == "block"), None)
        self.track_sprites = [s for s in level.get_sprites() if s.name == "track"]
        self._refresh_visuals()
        self._refresh_hud()

    def _refresh_hud(self) -> None:
        self._hud.set_state(steps_remaining=self.step_budget - self.steps_used, max_steps=self.step_budget)

    def _refresh_visuals(self) -> None:
        color = THIN_COLOR if self.mode == "thin" else THICK_COLOR
        for sprite in self.track_sprites:
            sprite.pixels = np.array(_track_pixels(color), dtype=np.int16)
        self.red_sprite.set_position(*_cell(*_path_cell(self.red)))
        if self.blue_sprite is not None and self.blue is not None:
            self.blue_sprite.set_position(*_cell(*_path_cell(self.blue)))
        if self.block_sprite is not None and self.block is not None:
            self.block_sprite.set_position(*_cell(*_path_cell(self.block)))

    def _click_cell(self) -> tuple[int, int] | None:
        click_x = int(self.action.data.get("x", -1000))
        click_y = int(self.action.data.get("y", -1000))
        grid = self.camera.display_to_grid(click_x, click_y)
        if grid is None:
            return None
        return (grid[0] // CELL, grid[1] // CELL)

    def _hit_box(self, clicked: tuple[int, int], origin: tuple[int, int]) -> bool:
        return origin[0] <= clicked[0] < origin[0] + BUTTON_SIZE and origin[1] <= clicked[1] < origin[1] + BUTTON_SIZE

    def _apply_push(self, direction: str) -> None:
        dx = -1 if direction == "L" else 1
        if self.block is not None and self.mode == "thin":
            nb = self.block + dx
            occ = {self.red}
            if self.blue is not None and not self.blue_locked:
                occ.add(self.blue)
            if 1 <= nb <= len(PATH) and nb not in occ:
                self.block = nb

        movers = []
        if not self.red_locked:
            movers.append(("r", self.red))
        if self.blue is not None and not self.blue_locked:
            movers.append(("b", self.blue))
        movers.sort(key=lambda item: (-item[1] if dx > 0 else item[1]))
        occ = set()
        occ.add(self.red if not self.red_locked else self.red_target)
        if self.blue is not None:
            occ.add(self.blue if not self.blue_locked else self.blue_target)
        if self.block is not None:
            occ.add(self.block)

        for name, pos in movers:
            occ.remove(pos)
            if self.mode == "thin":
                nxt = pos
                while True:
                    trial = nxt + dx
                    if trial < 1 or trial > len(PATH) or trial in occ:
                        break
                    nxt = trial
            else:
                trial = pos + dx
                nxt = pos if trial < 1 or trial > len(PATH) or trial in occ else trial
            if name == "r":
                self.red = nxt
                if self.red == self.red_target:
                    self.red_locked = True
            else:
                self.blue = nxt
                if self.blue_target is not None and self.blue == self.blue_target:
                    self.blue_locked = True
            occ.add(nxt)

    def step(self) -> None:
        clicked = self._click_cell()
        if clicked is None:
            self.complete_action()
            return
        action = None
        for key, cell in CONTROL_CELLS.items():
            if self._hit_box(clicked, cell):
                action = key
                break
        if action is None:
            self.complete_action()
            return

        if action == "T":
            self.mode = "thin"
        elif action == "G":
            self.mode = "thick"
        else:
            self._apply_push(action)
        self.steps_used += 1
        self._refresh_visuals()
        self._refresh_hud()
        if self.red_locked and (self.blue is None or self.blue_locked):
            self.next_level()
        elif self.steps_used >= self.step_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
