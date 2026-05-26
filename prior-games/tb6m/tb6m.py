"""Generated game tb6m."""

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


def _phase_active(main: int, accent: int) -> list[list[int]]:
    return [
        [main, main, main, main],
        [main, accent, accent, main],
        [main, accent, accent, main],
        [main, main, main, main],
    ]


def _phase_inactive(main: int) -> list[list[int]]:
    return [
        [main, main, main, main],
        [main, -1, -1, main],
        [main, -1, -1, main],
        [main, main, main, main],
    ]


def _switch_pixels(main: int, accent: int) -> list[list[int]]:
    return [
        [main, main, main, main],
        [main, accent, accent, main],
        [main, accent, accent, main],
        [accent, main, main, accent],
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
    "switch_red": Sprite(
        pixels=_switch_pixels(8, 13),
        name="switch_red",
        visible=True,
        collidable=False,
        tags=["switch_red"],
        layer=5,
    ),
    "switch_blue": Sprite(
        pixels=_switch_pixels(10, 9),
        name="switch_blue",
        visible=True,
        collidable=False,
        tags=["switch_blue"],
        layer=5,
    ),
    "switch_green": Sprite(
        pixels=_switch_pixels(14, 11),
        name="switch_green",
        visible=True,
        collidable=False,
        tags=["switch_green"],
        layer=5,
    ),
    "phase_red_active": Sprite(
        pixels=_phase_active(8, 13),
        name="phase_red_active",
        visible=True,
        collidable=False,
        tags=["phase_red_active"],
        layer=4,
    ),
    "phase_red_inactive": Sprite(
        pixels=_phase_inactive(8),
        name="phase_red_inactive",
        visible=True,
        collidable=False,
        tags=["phase_red_inactive"],
        layer=3,
    ),
    "phase_blue_active": Sprite(
        pixels=_phase_active(10, 9),
        name="phase_blue_active",
        visible=True,
        collidable=False,
        tags=["phase_blue_active"],
        layer=4,
    ),
    "phase_blue_inactive": Sprite(
        pixels=_phase_inactive(10),
        name="phase_blue_inactive",
        visible=True,
        collidable=False,
        tags=["phase_blue_inactive"],
        layer=3,
    ),
    "phase_green_active": Sprite(
        pixels=_phase_active(14, 11),
        name="phase_green_active",
        visible=True,
        collidable=False,
        tags=["phase_green_active"],
        layer=4,
    ),
    "phase_green_inactive": Sprite(
        pixels=_phase_inactive(14),
        name="phase_green_inactive",
        visible=True,
        collidable=False,
        tags=["phase_green_inactive"],
        layer=3,
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
    neutral_cells: set[tuple[int, int]],
    switches: list[dict],
    phase_specs: list[dict],
    group_states: dict[str, bool],
    step_budget: int,
) -> Level:
    placed: list[Sprite] = []
    _add_floor(placed, neutral_cells)
    placed.append(_clone("avatar", *avatar_cell))
    placed.append(_clone("goal_pad", *goal_cell))

    for switch in switches:
        placed.append(_clone(f"switch_{switch['group']}", *switch["cell"]))

    stored_phase_specs: list[dict] = []
    for idx, spec in enumerate(phase_specs):
        active = _clone(f"phase_{spec['group']}_active", *spec["cell"])
        inactive = _clone(f"phase_{spec['group']}_inactive", *spec["cell"])
        active.tags.append(f"phase_{idx}_active")
        inactive.tags.append(f"phase_{idx}_inactive")
        placed.append(active)
        placed.append(inactive)
        stored_phase_specs.append(
            {
                "index": idx,
                "group": spec["group"],
                "cell": spec["cell"],
                "polarity": bool(spec["polarity"]),
            }
        )

    return Level(
        sprites=placed,
        grid_size=GRID_SIZE,
        data={
            "avatar_cell": avatar_cell,
            "goal_cell": goal_cell,
            "neutral_cells": sorted(neutral_cells),
            "switches": switches,
            "phase_specs": stored_phase_specs,
            "group_states": group_states,
            "step_budget": step_budget,
        },
    )


LEVEL_1_NEUTRAL = {(1, 11), (2, 11), (3, 11), (4, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11)}
LEVEL_2_NEUTRAL = (
    {(1, 11), (2, 11), (3, 11), (4, 11)}
    | {(9, y) for y in range(8, 12)}
    | {(5, 8), (11, 8)}
)
LEVEL_3_NEUTRAL = (
    {(1, 11), (2, 11), (3, 11), (4, 11)}
    | {(9, y) for y in range(8, 12)}
    | {(5, 8), (14, 8), (14, 5), (10, 5)}
)


levels = [
    _build_level(
        avatar_cell=(2, 11),
        goal_cell=(14, 11),
        neutral_cells=LEVEL_1_NEUTRAL,
        switches=[{"cell": (4, 11), "group": "red"}],
        phase_specs=[
            {"cell": (5, 11), "group": "red", "polarity": True},
            {"cell": (6, 11), "group": "red", "polarity": True},
            {"cell": (7, 11), "group": "red", "polarity": True},
            {"cell": (8, 11), "group": "red", "polarity": True},
            {"cell": (9, 11), "group": "red", "polarity": True},
        ],
        group_states={"red": False},
        step_budget=18,
    ),
    _build_level(
        avatar_cell=(2, 11),
        goal_cell=(13, 10),
        neutral_cells=LEVEL_2_NEUTRAL,
        switches=[
            {"cell": (4, 11), "group": "red"},
            {"cell": (5, 8), "group": "blue"},
            {"cell": (11, 8), "group": "red"},
        ],
        phase_specs=[
            {"cell": (5, 11), "group": "red", "polarity": True},
            {"cell": (6, 11), "group": "red", "polarity": True},
            {"cell": (7, 11), "group": "red", "polarity": True},
            {"cell": (8, 11), "group": "red", "polarity": True},
            {"cell": (8, 8), "group": "red", "polarity": True},
            {"cell": (7, 8), "group": "red", "polarity": True},
            {"cell": (6, 8), "group": "red", "polarity": True},
            {"cell": (9, 8), "group": "blue", "polarity": True},
            {"cell": (10, 8), "group": "blue", "polarity": True},
            {"cell": (11, 9), "group": "red", "polarity": False},
            {"cell": (11, 10), "group": "red", "polarity": False},
            {"cell": (12, 10), "group": "red", "polarity": False},
            {"cell": (13, 10), "group": "red", "polarity": False},
        ],
        group_states={"red": False, "blue": False},
        step_budget=34,
    ),
    _build_level(
        avatar_cell=(2, 11),
        goal_cell=(8, 5),
        neutral_cells=LEVEL_3_NEUTRAL,
        switches=[
            {"cell": (4, 11), "group": "red"},
            {"cell": (5, 8), "group": "blue"},
            {"cell": (14, 8), "group": "red"},
            {"cell": (14, 5), "group": "green"},
            {"cell": (10, 5), "group": "blue"},
        ],
        phase_specs=[
            {"cell": (5, 11), "group": "red", "polarity": True},
            {"cell": (6, 11), "group": "red", "polarity": True},
            {"cell": (7, 11), "group": "red", "polarity": True},
            {"cell": (8, 11), "group": "red", "polarity": True},
            {"cell": (8, 8), "group": "red", "polarity": True},
            {"cell": (7, 8), "group": "red", "polarity": True},
            {"cell": (6, 8), "group": "red", "polarity": True},
            {"cell": (9, 8), "group": "blue", "polarity": True},
            {"cell": (10, 8), "group": "blue", "polarity": True},
            {"cell": (11, 8), "group": "blue", "polarity": True},
            {"cell": (12, 8), "group": "blue", "polarity": True},
            {"cell": (13, 8), "group": "blue", "polarity": True},
            {"cell": (14, 6), "group": "red", "polarity": False},
            {"cell": (14, 7), "group": "red", "polarity": False},
            {"cell": (11, 5), "group": "green", "polarity": True},
            {"cell": (12, 5), "group": "green", "polarity": True},
            {"cell": (13, 5), "group": "green", "polarity": True},
            {"cell": (8, 5), "group": "blue", "polarity": False},
            {"cell": (9, 5), "group": "blue", "polarity": False},
        ],
        group_states={"red": False, "blue": False, "green": False},
        step_budget=46,
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


class Tb6m(NovaBaseGame):
    def __init__(self) -> None:
        self.step_hud = StepBarHud()
        self.avatar: Sprite | None = None
        self.goal_cell = (0, 0)
        self.neutral_cells: set[tuple[int, int]] = set()
        self.step_budget = 0
        self.step_count = 0
        self.switch_groups: dict[tuple[int, int], str] = {}
        self.phase_groups: dict[str, list[tuple[Sprite, Sprite, tuple[int, int], bool]]] = {}
        self.group_state: dict[str, bool] = {}
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_hud],
        )
        super().__init__(
            game_id="tb6m",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    def on_set_level(self, level: Level) -> None:
        self.camera.width = 64
        self.camera.height = 64
        self.avatar = level.get_sprites_by_tag("player")[0]
        self.goal_cell = tuple(level.get_data("goal_cell") or (0, 0))
        self.neutral_cells = {tuple(cell) for cell in (level.get_data("neutral_cells") or [])}
        self.step_budget = int(level.get_data("step_budget") or 20)
        self.step_count = 0
        self.step_hud.reset(self.step_budget)
        self.switch_groups = {}
        self.phase_groups = {}
        self.group_state = dict(level.get_data("group_states") or {})

        for switch in level.get_data("switches") or []:
            self.switch_groups[tuple(switch["cell"])] = switch["group"]

        for spec in level.get_data("phase_specs") or []:
            active = level.get_sprites_by_tag(f"phase_{spec['index']}_active")[0]
            inactive = level.get_sprites_by_tag(f"phase_{spec['index']}_inactive")[0]
            self.phase_groups.setdefault(spec["group"], []).append(
                (
                    active,
                    inactive,
                    tuple(spec["cell"]),
                    bool(spec["polarity"]),
                )
            )

        self._sync_phases()

    def _avatar_cell(self) -> tuple[int, int]:
        if self.avatar is None:
            return (0, 0)
        return (self.avatar.x // CELL_PX, self.avatar.y // CELL_PX)

    def _walkable_cells(self) -> set[tuple[int, int]]:
        cells = set(self.neutral_cells)
        for group, entries in self.phase_groups.items():
            state = self.group_state.get(group, False)
            for _, _, cell, polarity in entries:
                if state == polarity:
                    cells.add(cell)
        return cells

    def _sync_phases(self) -> None:
        for group, entries in self.phase_groups.items():
            state = self.group_state.get(group, False)
            for active, inactive, _, polarity in entries:
                enabled = state == polarity
                active.set_interaction(InteractionMode.INTANGIBLE if enabled else InteractionMode.REMOVED)
                inactive.set_interaction(InteractionMode.REMOVED if enabled else InteractionMode.TANGIBLE)

    def _move_avatar(self, dx: int, dy: int) -> bool:
        target = (self._avatar_cell()[0] + dx, self._avatar_cell()[1] + dy)
        if target not in self._walkable_cells():
            return False
        if self.avatar is not None:
            self.avatar.set_position(*_cell(*target))
        return True

    def _toggle_switch(self) -> None:
        group = self.switch_groups.get(self._avatar_cell())
        if group is None:
            return
        self.group_state[group] = not self.group_state.get(group, False)
        self._sync_phases()

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
            self._toggle_switch()

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
        state = np.zeros((1, 12), dtype=np.int16)
        ax, ay = self._avatar_cell()
        state[0, 0] = ax
        state[0, 1] = ay
        state[0, 2] = self.step_count
        state[0, 3] = self.step_budget
        state[0, 4] = int(self.group_state.get("red", False))
        state[0, 5] = int(self.group_state.get("blue", False))
        state[0, 6] = int(self.group_state.get("green", False))
        state[0, 7] = self._current_level_index
        return state
