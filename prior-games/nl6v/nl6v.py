"""nl6v."""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 4
PADDING_COLOR = 4
PANEL_COLOR = 1
OUTLINE_COLOR = 5
YELLOW_COLOR = 14
CYAN_COLOR = 9
GREEN_COLOR = 3
STEP_COLOR = 14
STEP_EMPTY = 4

CELL = 4
GRID_CELLS = 16
GRID_W = GRID_CELLS * CELL
GRID_H = GRID_CELLS * CELL

CONTROL_CELLS = {
    "Y": (3, 0),
    "C": (9, 0),
    "L": (2, 11),
    "D": (6, 11),
    "R": (10, 11),
}
BUTTON_SIZE = 2

LEFT_VIAL = (4, 8)
BEAKER = (5, 3)
MID_VIAL = (6, 8)
RIGHT_VIAL = (8, 8)


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _panel_pixels() -> list[list[int]]:
    return [[PANEL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _fill_color(code: str) -> int:
    return {
        "E": PANEL_COLOR,
        "Y": YELLOW_COLOR,
        "C": CYAN_COLOR,
        "G": GREEN_COLOR,
    }[code]


def _tap_pixels(color: int) -> list[list[int]]:
    return [
        [OUTLINE_COLOR, OUTLINE_COLOR, color, color, color, color, OUTLINE_COLOR, OUTLINE_COLOR],
        [OUTLINE_COLOR, color, color, color, color, color, color, OUTLINE_COLOR],
        [OUTLINE_COLOR, color, color, color, color, color, color, OUTLINE_COLOR],
        [OUTLINE_COLOR, color, color, color, color, color, color, OUTLINE_COLOR],
        [OUTLINE_COLOR, color, color, OUTLINE_COLOR, OUTLINE_COLOR, color, color, OUTLINE_COLOR],
        [OUTLINE_COLOR, color, color, OUTLINE_COLOR, OUTLINE_COLOR, color, color, OUTLINE_COLOR],
        [OUTLINE_COLOR, OUTLINE_COLOR, OUTLINE_COLOR, OUTLINE_COLOR, OUTLINE_COLOR, OUTLINE_COLOR, OUTLINE_COLOR, OUTLINE_COLOR],
        [PANEL_COLOR, PANEL_COLOR, PANEL_COLOR, PANEL_COLOR, PANEL_COLOR, PANEL_COLOR, PANEL_COLOR, PANEL_COLOR],
    ]


def _spout_pixels(direction: str) -> list[list[int]]:
    pixels = np.full((8, 8), PANEL_COLOR, dtype=np.int16)
    pixels[1:7, 1:7] = OUTLINE_COLOR
    pixels[2:6, 2:6] = PANEL_COLOR
    if direction == "L":
        pixels[3:5, 2:6] = OUTLINE_COLOR
        pixels[2:6, 1:3] = GREEN_COLOR
        pixels[3:5, 3:6] = PANEL_COLOR
    else:
        pixels[3:5, 2:6] = OUTLINE_COLOR
        pixels[2:6, 5:7] = GREEN_COLOR
        pixels[3:5, 2:5] = PANEL_COLOR
    return pixels.tolist()


def _down_spout_pixels() -> list[list[int]]:
    pixels = np.full((8, 8), PANEL_COLOR, dtype=np.int16)
    pixels[1:7, 1:7] = OUTLINE_COLOR
    pixels[2:6, 2:6] = PANEL_COLOR
    pixels[2:5, 3:5] = OUTLINE_COLOR
    pixels[5:7, 2:6] = GREEN_COLOR
    pixels[2:5, 2:6] = PANEL_COLOR
    return pixels.tolist()


def _beaker_pixels(fill: str) -> list[list[int]]:
    color = _fill_color(fill)
    pixels = np.full((16, 16), PANEL_COLOR, dtype=np.int16)
    pixels[0, 3:13] = OUTLINE_COLOR
    pixels[1:16, 2] = OUTLINE_COLOR
    pixels[1:16, 13] = OUTLINE_COLOR
    pixels[15, 2:14] = OUTLINE_COLOR
    if fill != "E":
        pixels[8:15, 3:13] = color
    return pixels.tolist()


def _vial_pixels(target: str, filled: bool) -> list[list[int]]:
    border = _fill_color(target)
    fill = border if filled else PANEL_COLOR
    pixels = np.full((12, 8), PANEL_COLOR, dtype=np.int16)
    pixels[0:2, 2:6] = OUTLINE_COLOR
    pixels[2:12, 1] = border
    pixels[2:12, 6] = border
    pixels[11, 1:7] = border
    pixels[5:11, 2:6] = fill
    return pixels.tolist()


sprites = {
    "panel": Sprite(_panel_pixels(), "panel", True, False, tags=["panel"], layer=1),
    "tap_Y": Sprite(_tap_pixels(YELLOW_COLOR), "tap_Y", True, False, tags=["tap_Y"], layer=3),
    "tap_C": Sprite(_tap_pixels(CYAN_COLOR), "tap_C", True, False, tags=["tap_C"], layer=3),
    "spout_L": Sprite(_spout_pixels("L"), "spout_L", True, False, tags=["spout_L"], layer=3),
    "spout_D": Sprite(_down_spout_pixels(), "spout_D", True, False, tags=["spout_D"], layer=3),
    "spout_R": Sprite(_spout_pixels("R"), "spout_R", True, False, tags=["spout_R"], layer=3),
    "beaker": Sprite(_beaker_pixels("E"), "beaker", True, False, tags=["beaker"], layer=2),
    "left_vial": Sprite(_vial_pixels("Y", False), "left_vial", True, False, tags=["left_vial"], layer=2),
    "mid_vial": Sprite(_vial_pixels("G", False), "mid_vial", True, False, tags=["mid_vial"], layer=2),
    "right_vial": Sprite(_vial_pixels("C", False), "right_vial", True, False, tags=["right_vial"], layer=2),
}


def _clone(name: str, cx: int, cy: int) -> Sprite:
    return sprites[name].clone().set_position(*_cell(cx, cy))


def _build_level(
    *,
    left_target: str | None,
    mid_target: str | None,
    right_target: str | None,
    step_budget: int,
    left_vial_cell: tuple[int, int] = LEFT_VIAL,
    mid_vial_cell: tuple[int, int] = MID_VIAL,
    right_vial_cell: tuple[int, int] = RIGHT_VIAL,
) -> Level:
    placed: list[Sprite] = []
    for cy in range(GRID_CELLS):
        for cx in range(GRID_CELLS):
            placed.append(_clone("panel", cx, cy))
    placed.append(_clone("tap_Y", *CONTROL_CELLS["Y"]))
    placed.append(_clone("tap_C", *CONTROL_CELLS["C"]))
    placed.append(_clone("spout_L", *CONTROL_CELLS["L"]))
    if mid_target is not None:
        placed.append(_clone("spout_D", *CONTROL_CELLS["D"]))
    placed.append(_clone("spout_R", *CONTROL_CELLS["R"]))
    placed.append(_clone("beaker", *BEAKER))
    placed.append(_clone("left_vial", *left_vial_cell))
    if mid_target is not None:
        placed.append(_clone("mid_vial", *mid_vial_cell))
    placed.append(_clone("right_vial", *right_vial_cell))
    return Level(
        sprites=placed,
        grid_size=(GRID_W, GRID_H),
        data={
            "left_target": left_target,
            "mid_target": mid_target,
            "right_target": right_target,
            "step_budget": step_budget,
        },
    )


levels = [
    _build_level(
        left_target="G",
        mid_target=None,
        right_target=None,
        step_budget=5,
        left_vial_cell=(5, 8),
        right_vial_cell=(7, 8),
    ),
    _build_level(left_target="Y", mid_target=None, right_target="G", step_budget=7, left_vial_cell=(5, 8), right_vial_cell=(7, 8)),
    _build_level(
        left_target="Y",
        mid_target="G",
        right_target="C",
        step_budget=9,
        left_vial_cell=(3, 8),
        mid_vial_cell=(6, 8),
        right_vial_cell=(9, 8),
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


class Nl6v(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = StepHud()
        camera = Camera(width=GRID_W, height=GRID_H, background=BACKGROUND_COLOR, letter_box=PADDING_COLOR, interfaces=[self._hud])
        super().__init__(game_id="nl6v", levels=levels, camera=camera, available_actions=[6])

    def on_set_level(self, level: Level) -> None:
        self.left_target = level.get_data("left_target")
        self.mid_target = level.get_data("mid_target")
        self.right_target = level.get_data("right_target")
        self.left_filled = self.left_target is None
        self.mid_filled = self.mid_target is None
        self.right_filled = self.right_target is None
        self.reservoir = "E"
        self.step_budget = int(level.get_data("step_budget") or 1)
        self.steps_used = 0
        self.beaker_sprite = next(sprite for sprite in level.get_sprites() if sprite.name == "beaker")
        self.left_vial_sprite = next(sprite for sprite in level.get_sprites() if sprite.name == "left_vial")
        self.mid_vial_sprite = next((sprite for sprite in level.get_sprites() if sprite.name == "mid_vial"), None)
        self.right_vial_sprite = next(sprite for sprite in level.get_sprites() if sprite.name == "right_vial")
        self._refresh_visuals()
        self._refresh_hud()

    def _refresh_hud(self) -> None:
        self._hud.set_state(steps_remaining=self.step_budget - self.steps_used, max_steps=self.step_budget)

    def _refresh_visuals(self) -> None:
        self.beaker_sprite.pixels = np.array(_beaker_pixels(self.reservoir), dtype=np.int16)
        left_target = self.left_target if self.left_target is not None else "Y"
        mid_target = self.mid_target if self.mid_target is not None else "G"
        right_target = self.right_target if self.right_target is not None else "C"
        self.left_vial_sprite.pixels = np.array(_vial_pixels(left_target, self.left_filled), dtype=np.int16)
        if self.mid_vial_sprite is not None:
            self.mid_vial_sprite.pixels = np.array(_vial_pixels(mid_target, self.mid_filled), dtype=np.int16)
        self.right_vial_sprite.pixels = np.array(_vial_pixels(right_target, self.right_filled), dtype=np.int16)

    def _click_cell(self) -> tuple[int, int] | None:
        click_x = int(self.action.data.get("x", -1000))
        click_y = int(self.action.data.get("y", -1000))
        grid = self.camera.display_to_grid(click_x, click_y)
        if grid is None:
            return None
        return (grid[0] // CELL, grid[1] // CELL)

    def _hit_box(self, clicked: tuple[int, int], origin: tuple[int, int]) -> bool:
        return origin[0] <= clicked[0] < origin[0] + BUTTON_SIZE and origin[1] <= clicked[1] < origin[1] + BUTTON_SIZE

    def _add_reagent(self, reagent: str) -> None:
        if reagent == "Y":
            self.reservoir = {"E": "Y", "Y": "Y", "C": "G", "G": "G"}[self.reservoir]
        else:
            self.reservoir = {"E": "C", "Y": "G", "C": "C", "G": "G"}[self.reservoir]

    def _pour_left(self) -> None:
        if not self.left_filled and self.left_target is not None and self.reservoir == self.left_target:
            self.left_filled = True
        self.reservoir = "E"

    def _pour_right(self) -> None:
        if not self.right_filled and self.right_target is not None and self.reservoir == self.right_target:
            self.right_filled = True
        self.reservoir = "E"

    def _pour_mid(self) -> None:
        if not self.mid_filled and self.mid_target is not None and self.reservoir == self.mid_target:
            self.mid_filled = True
        self.reservoir = "E"

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

        if action in {"Y", "C"}:
            self._add_reagent(action)
        elif action == "L":
            self._pour_left()
        elif action == "D":
            self._pour_mid()
        else:
            self._pour_right()

        self.steps_used += 1
        self._refresh_visuals()
        self._refresh_hud()
        if self.left_filled and self.mid_filled and self.right_filled:
            self.next_level()
        elif self.steps_used >= self.step_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
