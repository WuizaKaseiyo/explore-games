"""Generated game wr2h."""

from __future__ import annotations

import numpy as np
from novaengine import (
    NovaBaseGame,
    Camera,
    GameAction,
    InteractionMode,
    Level,
    RenderableUserDisplay,
    Sprite,
)


CELL_PX = 4
GRID_CELLS = 16
GRID_SIZE = (64, 64)

BACKGROUND_COLOR = 5
PADDING_COLOR = 4


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL_PX, cy * CELL_PX)


def _floor_pixels() -> list[list[int]]:
    return [
        [2, 2, 2, 2],
        [2, 1, 1, 2],
        [2, 1, 1, 2],
        [2, 2, 2, 2],
    ]


def _rail_pixels() -> list[list[int]]:
    return [
        [4, 4, 4, 4],
        [5, 5, 5, 5],
        [5, 5, 5, 5],
        [4, 4, 4, 4],
    ]


def _strip_pixels(main: int, accent: int) -> list[list[int]]:
    return [
        [main, main, main, main],
        [main, accent, accent, main],
        [main, accent, accent, main],
        [main, main, main, main],
    ]


def _control_pixels(main: int, accent: int) -> list[list[int]]:
    return [
        [main, main, main, main],
        [main, accent, accent, main],
        [main, 0, 0, main],
        [main, main, main, main],
    ]


sprites = {
    "avatar": Sprite(
        pixels=[
            [-1, 11, 11, -1],
            [11, 11, 11, 11],
            [11, 8, 8, 11],
            [-1, 5, 5, -1],
        ],
        name="avatar",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=6,
    ),
    "floor_tile": Sprite(
        pixels=_floor_pixels(),
        name="floor_tile",
        visible=True,
        collidable=False,
        tags=["floor"],
        layer=1,
    ),
    "rail_tile": Sprite(
        pixels=_rail_pixels(),
        name="rail_tile",
        visible=True,
        collidable=False,
        tags=["rail"],
        layer=2,
    ),
    "goal_pad": Sprite(
        pixels=[
            [14, 14, 14, 14],
            [14, 11, 11, 14],
            [14, 11, 11, 14],
            [14, 14, 14, 14],
        ],
        name="goal_pad",
        visible=True,
        collidable=False,
        tags=["goal"],
        layer=5,
    ),
    "strip_red": Sprite(
        pixels=_strip_pixels(8, 13),
        name="strip_red",
        visible=True,
        collidable=False,
        tags=["strip_red"],
        layer=4,
    ),
    "strip_red_control": Sprite(
        pixels=_control_pixels(8, 13),
        name="strip_red_control",
        visible=True,
        collidable=False,
        tags=["strip_red_control"],
        layer=5,
    ),
    "strip_blue": Sprite(
        pixels=_strip_pixels(10, 9),
        name="strip_blue",
        visible=True,
        collidable=False,
        tags=["strip_blue"],
        layer=4,
    ),
    "strip_blue_control": Sprite(
        pixels=_control_pixels(10, 9),
        name="strip_blue_control",
        visible=True,
        collidable=False,
        tags=["strip_blue_control"],
        layer=5,
    ),
    "strip_green": Sprite(
        pixels=_strip_pixels(14, 11),
        name="strip_green",
        visible=True,
        collidable=False,
        tags=["strip_green"],
        layer=4,
    ),
    "strip_green_control": Sprite(
        pixels=_control_pixels(14, 11),
        name="strip_green_control",
        visible=True,
        collidable=False,
        tags=["strip_green_control"],
        layer=5,
    ),
}


def _clone(name: str, cx: int, cy: int) -> Sprite:
    return sprites[name].clone().set_position(*_cell(cx, cy))


def _add_floor(placed: list[Sprite], cells: set[tuple[int, int]]) -> None:
    for cx, cy in sorted(cells):
        placed.append(_clone("floor_tile", cx, cy))


def _strip_cells_from_spec(spec: dict, base: tuple[int, int]) -> list[tuple[int, int]]:
    bx, by = base
    cells = []
    for offset in range(spec["length"]):
        if spec["orientation"] == "horizontal":
            cells.append((bx + offset, by))
        else:
            cells.append((bx, by + offset))
    return cells


def _build_level(
    *,
    avatar_cell: tuple[int, int],
    goal_cell: tuple[int, int],
    neutral_cells: set[tuple[int, int]],
    strips: list[dict],
    step_budget: int,
) -> Level:
    placed: list[Sprite] = []
    _add_floor(placed, neutral_cells)

    rail_cells: set[tuple[int, int]] = set()
    for spec in strips:
        for base in spec["positions"]:
            rail_cells.update(_strip_cells_from_spec(spec, tuple(base)))
    for cx, cy in sorted(rail_cells):
        placed.append(_clone("rail_tile", cx, cy))

    placed.append(_clone("avatar", *avatar_cell))
    placed.append(_clone("goal_pad", *goal_cell))

    stored_specs: list[dict] = []
    for spec in strips:
        for idx in range(spec["length"]):
            name = f"strip_{spec['color']}_control" if idx == spec["control_offset"] else f"strip_{spec['color']}"
            seg = _clone(name, *tuple(spec["positions"][spec["index"]]))
            seg.tags.append(f"strip_{spec['strip_id']}")
            placed.append(seg)
        stored_specs.append(
            {
                "strip_id": spec["strip_id"],
                "color": spec["color"],
                "orientation": spec["orientation"],
                "length": spec["length"],
                "positions": spec["positions"],
                "index": spec["index"],
                "control_offset": spec["control_offset"],
            }
        )

    return Level(
        sprites=placed,
        grid_size=GRID_SIZE,
        data={
            "avatar_cell": avatar_cell,
            "goal_cell": goal_cell,
            "neutral_cells": sorted(neutral_cells),
            "strips": stored_specs,
            "step_budget": step_budget,
        },
    )


LEVEL_1_NEUTRAL = {(1, 11), (2, 11), (3, 11), (4, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11)}
LEVEL_2_NEUTRAL = (
    {(1, 11), (2, 11), (3, 11), (4, 11)}
    | {(10, 11), (11, 11)}
    | {(11, 5), (12, 5), (13, 5), (14, 5)}
)
LEVEL_3_NEUTRAL = (
    {(1, 11), (2, 11), (3, 11), (4, 11)}
    | {(10, 11), (11, 11)}
    | {(8, 7), (9, 7)}
    | {(14, 7)}
)


levels = [
    _build_level(
        avatar_cell=(2, 11),
        goal_cell=(14, 11),
        neutral_cells=LEVEL_1_NEUTRAL,
        strips=[
            {
                "strip_id": "a",
                "color": "red",
                "orientation": "horizontal",
                "length": 5,
                "positions": [(4, 11), (5, 11)],
                "index": 0,
                "control_offset": 0,
            }
        ],
        step_budget=18,
    ),
    _build_level(
        avatar_cell=(2, 11),
        goal_cell=(14, 5),
        neutral_cells=LEVEL_2_NEUTRAL,
        strips=[
            {
                "strip_id": "a",
                "color": "red",
                "orientation": "horizontal",
                "length": 5,
                "positions": [(4, 11), (5, 11)],
                "index": 0,
                "control_offset": 0,
            },
            {
                "strip_id": "b",
                "color": "blue",
                "orientation": "vertical",
                "length": 3,
                "positions": [(11, 8), (11, 5)],
                "index": 0,
                "control_offset": 2,
            },
        ],
        step_budget=28,
    ),
    _build_level(
        avatar_cell=(2, 11),
        goal_cell=(14, 7),
        neutral_cells=LEVEL_3_NEUTRAL,
        strips=[
            {
                "strip_id": "a",
                "color": "red",
                "orientation": "horizontal",
                "length": 5,
                "positions": [(4, 11), (5, 11)],
                "index": 0,
                "control_offset": 0,
            },
            {
                "strip_id": "b",
                "color": "blue",
                "orientation": "vertical",
                "length": 3,
                "positions": [(11, 8), (11, 5)],
                "index": 0,
                "control_offset": 2,
            },
            {
                "strip_id": "c",
                "color": "green",
                "orientation": "horizontal",
                "length": 4,
                "positions": [(7, 7), (10, 7)],
                "index": 0,
                "control_offset": 3,
            },
        ],
        step_budget=34,
    ),
]


class StepBarHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self.max_steps = 0
        self.remaining = 0

    def reset(self, budget: int) -> None:
        self.max_steps = max(1, budget)
        self.remaining = max(0, budget)

    def set_remaining(self, remaining: int) -> None:
        self.remaining = max(0, min(remaining, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        fill = round((self.remaining / self.max_steps) * 64)
        for x in range(64):
            frame[63, x] = 11 if x < fill else 4
        return frame


class Wr2h(NovaBaseGame):
    def __init__(self) -> None:
        self.step_hud = StepBarHud()
        self.avatar: Sprite | None = None
        self.neutral_cells: set[tuple[int, int]] = set()
        self.goal_cell = (0, 0)
        self.step_budget = 0
        self.step_count = 0
        self.strips: dict[str, dict] = {}
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_hud],
        )
        super().__init__(
            game_id="wr2h",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    def on_set_level(self, level: Level) -> None:
        self.camera.width = 64
        self.camera.height = 64
        self.avatar = level.get_sprites_by_tag("player")[0]
        self.neutral_cells = {tuple(cell) for cell in (level.get_data("neutral_cells") or [])}
        self.goal_cell = tuple(level.get_data("goal_cell") or (0, 0))
        self.step_budget = int(level.get_data("step_budget") or 20)
        self.step_count = 0
        self.step_hud.reset(self.step_budget)
        self.strips = {}
        for spec in level.get_data("strips") or []:
            sid = spec["strip_id"]
            self.strips[sid] = {
                "orientation": spec["orientation"],
                "length": int(spec["length"]),
                "positions": [tuple(pos) for pos in spec["positions"]],
                "index": int(spec["index"]),
                "control_offset": int(spec["control_offset"]),
                "segments": list(level.get_sprites_by_tag(f"strip_{sid}")),
            }
            self._sync_strip(sid)

    def _avatar_cell(self) -> tuple[int, int]:
        if self.avatar is None:
            return (0, 0)
        return (self.avatar.x // CELL_PX, self.avatar.y // CELL_PX)

    def _strip_cells(self, sid: str) -> list[tuple[int, int]]:
        strip = self.strips[sid]
        bx, by = strip["positions"][strip["index"]]
        cells = []
        for offset in range(strip["length"]):
            if strip["orientation"] == "horizontal":
                cells.append((bx + offset, by))
            else:
                cells.append((bx, by + offset))
        return cells

    def _control_cell(self, sid: str) -> tuple[int, int]:
        return self._strip_cells(sid)[self.strips[sid]["control_offset"]]

    def _walkable_cells(self) -> set[tuple[int, int]]:
        cells = set(self.neutral_cells)
        for sid in self.strips:
            cells.update(self._strip_cells(sid))
        return cells

    def _sync_strip(self, sid: str) -> None:
        cells = self._strip_cells(sid)
        for seg, cell in zip(self.strips[sid]["segments"], cells):
            seg.set_position(*_cell(*cell))
            seg.set_interaction(InteractionMode.INTANGIBLE)

    def _move_avatar(self, dx: int, dy: int) -> bool:
        target = (self._avatar_cell()[0] + dx, self._avatar_cell()[1] + dy)
        if target not in self._walkable_cells():
            return False
        if self.avatar is not None:
            self.avatar.set_position(*_cell(*target))
        return True

    def _shift_strip(self) -> None:
        avatar_cell = self._avatar_cell()
        for sid, strip in self.strips.items():
            if avatar_cell != self._control_cell(sid):
                continue
            old_base = strip["positions"][strip["index"]]
            old_cells = self._strip_cells(sid)
            strip["index"] = (strip["index"] + 1) % len(strip["positions"])
            new_base = strip["positions"][strip["index"]]
            dx = new_base[0] - old_base[0]
            dy = new_base[1] - old_base[1]
            if avatar_cell in old_cells and self.avatar is not None:
                self.avatar.set_position(*_cell(avatar_cell[0] + dx, avatar_cell[1] + dy))
            self._sync_strip(sid)
            return

    def _check_win(self) -> bool:
        return self._avatar_cell() == self.goal_cell

    def step(self) -> None:
        self.step_count += 1
        aid = self.action.id
        if aid == GameAction.ACTION1:
            self._move_avatar(0, -1)
        elif aid == GameAction.ACTION2:
            self._move_avatar(0, 1)
        elif aid == GameAction.ACTION3:
            self._move_avatar(-1, 0)
        elif aid == GameAction.ACTION4:
            self._move_avatar(1, 0)
        elif aid == GameAction.ACTION5:
            self._shift_strip()

        self.step_hud.set_remaining(self.step_budget - self.step_count)
        if self._check_win():
            if self._current_level_index == len(self._levels) - 1:
                self.win()
            else:
                self.next_level()
            self.complete_action()
            return
        if self.step_count >= self.step_budget:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 16), dtype=np.int16)
        ax, ay = self._avatar_cell()
        state[0, 0] = ax
        state[0, 1] = ay
        state[0, 2] = self.step_count
        state[0, 3] = self.step_budget
        for idx, sid in enumerate(sorted(self.strips.keys())[:3]):
            strip = self.strips[sid]
            base_x, base_y = strip["positions"][strip["index"]]
            state[0, 4 + idx * 4] = strip["index"]
            state[0, 5 + idx * 4] = strip["control_offset"]
            state[0, 6 + idx * 4] = base_x
            state[0, 7 + idx * 4] = base_y
        return state
