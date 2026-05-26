"""Generated game ym4k."""

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

ORIENTATION_ORDER = ("north", "east", "south", "west")
ORIENTATION_VECTORS = {
    "north": (0, -1),
    "east": (1, 0),
    "south": (0, 1),
    "west": (-1, 0),
}


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL_PX, cy * CELL_PX)


def _bridge_pixels(main: int, accent: int) -> list[list[int]]:
    return [
        [main, main, main, main],
        [main, accent, accent, main],
        [main, accent, accent, main],
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
    "bridge_blue": Sprite(
        pixels=_bridge_pixels(10, 9),
        name="bridge_blue",
        visible=True,
        collidable=False,
        tags=["bridge_blue"],
        layer=3,
    ),
    "bridge_green": Sprite(
        pixels=_bridge_pixels(14, 11),
        name="bridge_green",
        visible=True,
        collidable=False,
        tags=["bridge_green"],
        layer=3,
    ),
    "bridge_red": Sprite(
        pixels=_bridge_pixels(8, 13),
        name="bridge_red",
        visible=True,
        collidable=False,
        tags=["bridge_red"],
        layer=3,
    ),
    "floor_tile": Sprite(
        pixels=[
            [2, 2, 2, 2],
            [2, 1, 1, 2],
            [2, 1, 1, 2],
            [2, 2, 2, 2],
        ],
        name="floor_tile",
        visible=True,
        collidable=False,
        tags=["floor"],
        layer=1,
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
    "pivot_blue": Sprite(
        pixels=[
            [10, 10, 10, 10],
            [10, 0, 0, 10],
            [10, 0, 0, 10],
            [10, 10, 10, 10],
        ],
        name="pivot_blue",
        visible=True,
        collidable=False,
        tags=["pivot_blue"],
        layer=4,
    ),
    "pivot_green": Sprite(
        pixels=[
            [14, 14, 14, 14],
            [14, 0, 0, 14],
            [14, 0, 0, 14],
            [14, 14, 14, 14],
        ],
        name="pivot_green",
        visible=True,
        collidable=False,
        tags=["pivot_green"],
        layer=4,
    ),
    "pivot_red": Sprite(
        pixels=[
            [8, 8, 8, 8],
            [8, 0, 0, 8],
            [8, 0, 0, 8],
            [8, 8, 8, 8],
        ],
        name="pivot_red",
        visible=True,
        collidable=False,
        tags=["pivot_red"],
        layer=4,
    ),
}


def _clone(name: str, cx: int, cy: int) -> Sprite:
    return sprites[name].clone().set_position(*_cell(cx, cy))


def _add_floor(placed: list[Sprite], cells: set[tuple[int, int]]) -> None:
    for cx, cy in sorted(cells):
        placed.append(_clone("floor_tile", cx, cy))


def _build_level(
    *,
    avatar_cell: tuple[int, int],
    goal_cell: tuple[int, int],
    static_cells: set[tuple[int, int]],
    arm_specs: list[dict],
    step_budget: int,
) -> Level:
    placed: list[Sprite] = []
    _add_floor(placed, static_cells)
    placed.append(_clone("avatar", *avatar_cell))
    placed.append(_clone("goal_pad", *goal_cell))

    for spec in arm_specs:
        placed.append(_clone(spec["pivot_sprite"], *spec["pivot"]))
        for seg_idx in range(spec["length"]):
            seg = sprites[spec["segment_sprite"]].clone().set_position(*_cell(*spec["pivot"]))
            seg.tags.append(f"arm_{spec['arm_id']}")
            placed.append(seg)

    return Level(
        sprites=placed,
        grid_size=GRID_SIZE,
        data={
            "avatar_cell": avatar_cell,
            "goal_cell": goal_cell,
            "step_budget": step_budget,
            "static_cells": sorted(static_cells),
            "arm_specs": arm_specs,
        },
    )


LEVEL_1_STATIC = {(1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11)}
LEVEL_2_STATIC = (
    {(1, 11), (2, 11), (3, 11), (4, 11), (5, 11)}
    | {(9, y) for y in range(7, 12)}
    | {(12, 7), (13, 7), (14, 7)}
)
LEVEL_3_STATIC = (
    {(1, 11), (2, 11), (3, 11), (4, 11), (5, 11)}
    | {(9, y) for y in range(7, 12)}
    | {(9, 3)}
    | {(12, 3), (13, 3), (14, 3)}
)

levels = [
    _build_level(
        avatar_cell=(3, 11),
        goal_cell=(14, 11),
        static_cells=LEVEL_1_STATIC,
        arm_specs=[
            {
                "arm_id": "a",
                "pivot": (5, 11),
                "length": 4,
                "orientation": "north",
                "segment_sprite": "bridge_red",
                "pivot_sprite": "pivot_red",
            }
        ],
        step_budget=20,
    ),
    _build_level(
        avatar_cell=(3, 11),
        goal_cell=(14, 7),
        static_cells=LEVEL_2_STATIC,
        arm_specs=[
            {
                "arm_id": "a",
                "pivot": (5, 11),
                "length": 4,
                "orientation": "north",
                "segment_sprite": "bridge_red",
                "pivot_sprite": "pivot_red",
            },
            {
                "arm_id": "b",
                "pivot": (9, 7),
                "length": 2,
                "orientation": "north",
                "segment_sprite": "bridge_blue",
                "pivot_sprite": "pivot_blue",
            },
        ],
        step_budget=32,
    ),
    _build_level(
        avatar_cell=(3, 11),
        goal_cell=(14, 3),
        static_cells=LEVEL_3_STATIC,
        arm_specs=[
            {
                "arm_id": "a",
                "pivot": (5, 11),
                "length": 4,
                "orientation": "north",
                "segment_sprite": "bridge_red",
                "pivot_sprite": "pivot_red",
            },
            {
                "arm_id": "b",
                "pivot": (9, 7),
                "length": 3,
                "orientation": "west",
                "segment_sprite": "bridge_blue",
                "pivot_sprite": "pivot_blue",
            },
            {
                "arm_id": "c",
                "pivot": (9, 3),
                "length": 2,
                "orientation": "north",
                "segment_sprite": "bridge_green",
                "pivot_sprite": "pivot_green",
            },
        ],
        step_budget=40,
    ),
]


class StepBarHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self.max_steps = 0
        self.remaining = 0

    def reset(self, budget: int) -> None:
        self.max_steps = max(0, budget)
        self.remaining = max(0, budget)

    def set_remaining(self, remaining: int) -> None:
        self.remaining = max(0, min(remaining, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        fill = round((self.remaining / self.max_steps) * 64)
        for x in range(64):
            frame[63, x] = 11 if x < fill else 4
        return frame


class Ym4k(NovaBaseGame):
    def __init__(self) -> None:
        self.step_hud = StepBarHud()
        self.avatar: Sprite | None = None
        self.goal_cell = (0, 0)
        self.static_cells: set[tuple[int, int]] = set()
        self.step_budget = 0
        self.step_count = 0
        self.arm_states: dict[str, dict] = {}
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_hud],
        )
        super().__init__(
            game_id="ym4k",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        players = level.get_sprites_by_tag("player")
        self.avatar = players[0] if players else None
        self.goal_cell = tuple(level.get_data("goal_cell") or (0, 0))
        self.static_cells = {tuple(cell) for cell in (level.get_data("static_cells") or [])}
        self.step_budget = int(level.get_data("step_budget") or 30)
        self.step_count = 0
        self.step_hud.reset(self.step_budget)

        self.arm_states = {}
        for spec in level.get_data("arm_specs") or []:
            arm_id = spec["arm_id"]
            self.arm_states[arm_id] = {
                "pivot": tuple(spec["pivot"]),
                "length": int(spec["length"]),
                "orientation": spec["orientation"],
                "segments": list(level.get_sprites_by_tag(f"arm_{arm_id}")),
            }
            self._sync_arm(arm_id)

    def _avatar_cell(self) -> tuple[int, int]:
        if self.avatar is None:
            return (0, 0)
        return (self.avatar.x // CELL_PX, self.avatar.y // CELL_PX)

    def _occupied_arm_cells(self, arm_id: str) -> list[tuple[int, int]]:
        arm = self.arm_states[arm_id]
        dx, dy = ORIENTATION_VECTORS[arm["orientation"]]
        px, py = arm["pivot"]
        return [(px + dx * step, py + dy * step) for step in range(1, arm["length"] + 1)]

    def _walkable_cells(self) -> set[tuple[int, int]]:
        cells = set(self.static_cells)
        for arm_id in self.arm_states:
            cells.update(self._occupied_arm_cells(arm_id))
        return cells

    def _sync_arm(self, arm_id: str) -> None:
        arm = self.arm_states[arm_id]
        occupied = self._occupied_arm_cells(arm_id)
        for idx, sprite in enumerate(arm["segments"]):
            if idx < len(occupied):
                sprite.set_interaction(InteractionMode.INTANGIBLE)
                sprite.set_position(*_cell(*occupied[idx]))
            else:
                sprite.set_interaction(InteractionMode.REMOVED)

    def _rotate_arm(self, arm_id: str) -> None:
        arm = self.arm_states[arm_id]
        current_idx = ORIENTATION_ORDER.index(arm["orientation"])
        arm["orientation"] = ORIENTATION_ORDER[(current_idx + 1) % len(ORIENTATION_ORDER)]
        self._sync_arm(arm_id)

    def _move_avatar(self, dx: int, dy: int) -> bool:
        current = self._avatar_cell()
        target = (current[0] + dx, current[1] + dy)
        if target[0] < 0 or target[0] >= GRID_CELLS or target[1] < 0 or target[1] >= GRID_CELLS:
            return False
        if target not in self._walkable_cells():
            return False
        if self.avatar is not None:
            self.avatar.set_position(*_cell(*target))
        return True

    def _handle_rotate(self) -> None:
        cell = self._avatar_cell()
        for arm_id, arm in self.arm_states.items():
            if cell == arm["pivot"]:
                self._rotate_arm(arm_id)
                return

    def _check_win(self) -> bool:
        return self._avatar_cell() == self.goal_cell

    def step(self) -> None:
        action_id = self.action.id
        self.step_count += 1

        if action_id == GameAction.ACTION1:
            self._move_avatar(0, -1)
        elif action_id == GameAction.ACTION2:
            self._move_avatar(0, 1)
        elif action_id == GameAction.ACTION3:
            self._move_avatar(-1, 0)
        elif action_id == GameAction.ACTION4:
            self._move_avatar(1, 0)
        elif action_id == GameAction.ACTION5:
            self._handle_rotate()

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
        for idx, arm_id in enumerate(sorted(self.arm_states.keys())[:3]):
            arm = self.arm_states[arm_id]
            state[0, 4 + idx * 4] = arm["pivot"][0]
            state[0, 5 + idx * 4] = arm["pivot"][1]
            state[0, 6 + idx * 4] = arm["length"]
            state[0, 7 + idx * 4] = ORIENTATION_ORDER.index(arm["orientation"])
        return state
