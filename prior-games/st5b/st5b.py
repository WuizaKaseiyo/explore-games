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


CELL = 4
GRID_CELLS = 8
GRID_SIZE = CELL * GRID_CELLS

BACKGROUND = 1
PADDING = 4
WALL = 5
LAND = 2
PIT = 0
ANCHOR_DRY = 8
ANCHOR_SELECTED = 9
BRIDGE = 12
AVATAR = 14
GOAL = 11
HUD_EMPTY = 4
HUD_FILL = 15


LEVEL_LAYOUTS = [
    (
        (
            "########",
            "#P.O~OG#",
            "########",
            "########",
            "########",
            "########",
            "########",
            "########",
        ),
        14,
    ),
    (
        (
            "########",
            "#P.O~O##",
            "#####.##",
            "###O~OG#",
            "########",
            "########",
            "########",
            "########",
        ),
        20,
    ),
    (
        (
            "########",
            "#P.O~O##",
            "#####.##",
            "#####.##",
            "###O~O##",
            "###~####",
            "##GO####",
            "########",
        ),
        28,
    ),
]


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _wall_pixels() -> list[list[int]]:
    return [[WALL for _ in range(CELL)] for _ in range(CELL)]


def _land_pixels() -> list[list[int]]:
    return [[LAND for _ in range(CELL)] for _ in range(CELL)]


def _goal_pixels() -> list[list[int]]:
    return [
        [GOAL, GOAL, GOAL, GOAL],
        [GOAL, -1, -1, GOAL],
        [GOAL, -1, PIT, GOAL],
        [GOAL, GOAL, GOAL, GOAL],
    ]


def _avatar_pixels() -> list[list[int]]:
    return [
        [-1, AVATAR, AVATAR, -1],
        [AVATAR, PIT, PIT, AVATAR],
        [AVATAR, PIT, PIT, AVATAR],
        [-1, AVATAR, AVATAR, -1],
    ]


def _anchor_pixels(color: int) -> list[list[int]]:
    return [
        [color, color, color, color],
        [color, -1, -1, color],
        [color, -1, PIT, color],
        [color, color, color, color],
    ]


def _bridge_pixels() -> list[list[int]]:
    return [
        [BRIDGE, BRIDGE, BRIDGE, BRIDGE],
        [-1, BRIDGE, BRIDGE, -1],
        [-1, BRIDGE, BRIDGE, -1],
        [BRIDGE, BRIDGE, BRIDGE, BRIDGE],
    ]


SPRITES = {
    "wall": Sprite(
        pixels=_wall_pixels(),
        name="wall",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=1,
    ),
    "land": Sprite(
        pixels=_land_pixels(),
        name="land",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["land"],
        layer=0,
    ),
    "goal": Sprite(
        pixels=_goal_pixels(),
        name="goal",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["goal"],
        layer=2,
    ),
    "avatar": Sprite(
        pixels=_avatar_pixels(),
        name="avatar",
        visible=True,
        collidable=True,
        tags=["avatar"],
        layer=4,
    ),
    "anchor_dry": Sprite(
        pixels=_anchor_pixels(ANCHOR_DRY),
        name="anchor_dry",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["anchor", "dry"],
        layer=2,
    ),
    "anchor_selected": Sprite(
        pixels=_anchor_pixels(ANCHOR_SELECTED),
        name="anchor_selected",
        visible=True,
        collidable=False,
        interaction=InteractionMode.REMOVED,
        tags=["anchor", "selected"],
        layer=3,
    ),
    "bridge": Sprite(
        pixels=_bridge_pixels(),
        name="bridge",
        visible=True,
        collidable=True,
        interaction=InteractionMode.REMOVED,
        tags=["bridge"],
        layer=2,
    ),
}


def _build_level(layout: tuple[str, ...], step_budget: int) -> Level:
    sprites: list[Sprite] = []
    anchor_cells: list[tuple[int, int]] = []
    land_cells: set[tuple[int, int]] = set()
    pit_cells: set[tuple[int, int]] = set()
    for cy, row in enumerate(layout):
        for cx, ch in enumerate(row):
            px, py = _cell(cx, cy)
            cell = (cx, cy)
            if ch == "#":
                sprites.append(SPRITES["wall"].clone().set_position(px, py))
            elif ch == "~":
                pit_cells.add(cell)
            else:
                land_cells.add(cell)
                sprites.append(SPRITES["land"].clone().set_position(px, py))
                if ch == "P":
                    sprites.append(SPRITES["avatar"].clone().set_position(px, py))
                elif ch == "G":
                    sprites.append(SPRITES["goal"].clone().set_position(px, py))
                elif ch == "O":
                    sprites.append(SPRITES["anchor_dry"].clone().set_position(px, py))
                    sprites.append(SPRITES["anchor_selected"].clone().set_position(px, py))
                    anchor_cells.append(cell)
    links: list[dict[str, object]] = []
    for idx, a in enumerate(anchor_cells):
        for b in anchor_cells[idx + 1 :]:
            cells: list[tuple[int, int]] = []
            if a[0] == b[0]:
                y0, y1 = sorted((a[1], b[1]))
                cells = [(a[0], y) for y in range(y0 + 1, y1)]
            elif a[1] == b[1]:
                x0, x1 = sorted((a[0], b[0]))
                cells = [(x, a[1]) for x in range(x0 + 1, x1)]
            if cells and all(cell in pit_cells for cell in cells):
                links.append({"a": a, "b": b, "cells": cells})
                for cx, cy in cells:
                    sprites.append(
                        SPRITES["bridge"]
                        .clone()
                        .set_position(*_cell(cx, cy))
                        .set_interaction(InteractionMode.REMOVED)
                    )
    return Level(
        sprites=sprites,
        grid_size=(GRID_SIZE, GRID_SIZE),
        data={
            "step_budget": step_budget,
            "links": links,
            "land_cells": sorted(land_cells),
        },
    )


LEVELS = [_build_level(layout, budget) for layout, budget in LEVEL_LAYOUTS]


class TopLifeBar(RenderableUserDisplay):
    def __init__(self) -> None:
        self.current = 0
        self.maximum = 1

    def set_state(self, current: int, maximum: int) -> None:
        self.current = max(0, current)
        self.maximum = max(1, maximum)

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        frame[0:4, :] = HUD_EMPTY
        filled = int(round((self.current / self.maximum) * 64))
        if filled > 0:
            frame[0:4, :filled] = HUD_FILL
        return frame


class St5b(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = TopLifeBar()
        camera = Camera(
            background=BACKGROUND,
            letter_box=PADDING,
            interfaces=[self._hud],
        )
        super().__init__(
            game_id="st5b",
            levels=LEVELS,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6, 7],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (GRID_SIZE, GRID_SIZE)
        self.camera.width = gw
        self.camera.height = gh
        self.step_budget = int(level.get_data("step_budget") or 1)
        self.steps_used = 0
        self.history: list[dict[str, object]] = []
        self.avatar = next(sprite for sprite in level.get_sprites() if "avatar" in sprite.tags)
        self.wall_cells = {
            (sprite.x // CELL, sprite.y // CELL)
            for sprite in level.get_sprites()
            if "wall" in sprite.tags
        }
        self.land_cells = {tuple(cell) for cell in level.get_data("land_cells") or []}
        self.links = list(level.get_data("links") or [])
        self.anchor_pairs: dict[tuple[int, int], dict[str, Sprite]] = {}
        for sprite in level.get_sprites():
            if "anchor" in sprite.tags:
                cell = (sprite.x // CELL, sprite.y // CELL)
                self.anchor_pairs.setdefault(cell, {})[
                    "selected" if "selected" in sprite.tags else "dry"
                ] = sprite
        self.bridge_sprites: dict[tuple[int, int], list[Sprite]] = {}
        for sprite in level.get_sprites():
            if "bridge" in sprite.tags:
                cell = (sprite.x // CELL, sprite.y // CELL)
                self.bridge_sprites.setdefault(cell, []).append(sprite)
        self.goal_cells = {
            (sprite.x // CELL, sprite.y // CELL)
            for sprite in level.get_sprites()
            if "goal" in sprite.tags
        }
        self.selected_anchors: list[tuple[int, int]] = []
        self.bridges: set[tuple[int, int]] = set()
        self._sync_anchors()
        self._sync_bridges()
        self._refresh_hud()

    def _avatar_cell(self) -> tuple[int, int]:
        return (self.avatar.x // CELL, self.avatar.y // CELL)

    def _refresh_hud(self) -> None:
        self._hud.set_state(self.step_budget - self.steps_used, self.step_budget)

    def _save_history(self) -> None:
        self.history.append(
            {
                "avatar": self._avatar_cell(),
                "selected": list(self.selected_anchors),
                "bridges": sorted(self.bridges),
                "steps_used": self.steps_used,
            }
        )

    def _restore_snapshot(self, snapshot: dict[str, object]) -> None:
        ax, ay = snapshot["avatar"]  # type: ignore[misc]
        self.avatar.set_position(*_cell(ax, ay))
        self.selected_anchors = list(snapshot["selected"])  # type: ignore[arg-type]
        self.bridges = set(snapshot["bridges"])  # type: ignore[arg-type]
        self.steps_used = int(snapshot["steps_used"])
        self._sync_anchors()
        self._sync_bridges()
        self._refresh_hud()

    def _sync_anchors(self) -> None:
        selected = set(self.selected_anchors)
        for cell, pair in self.anchor_pairs.items():
            pair["dry"].set_interaction(
                InteractionMode.REMOVED if cell in selected else InteractionMode.INTANGIBLE
            )
            pair["selected"].set_interaction(
                InteractionMode.INTANGIBLE if cell in selected else InteractionMode.REMOVED
            )

    def _sync_bridges(self) -> None:
        for cell, sprites in self.bridge_sprites.items():
            mode = InteractionMode.TANGIBLE if cell in self.bridges else InteractionMode.REMOVED
            for sprite in sprites:
                sprite.set_interaction(mode)

    def _walkable(self, cell: tuple[int, int]) -> bool:
        if cell in self.wall_cells:
            return False
        if cell in self.land_cells:
            return True
        return cell in self.bridges

    def _move_avatar(self, dx: int, dy: int) -> None:
        cx, cy = self._avatar_cell()
        cell = (cx + dx, cy + dy)
        if self._walkable(cell):
            self.avatar.set_position(*_cell(*cell))

    def _click_anchor(self, x: int, y: int) -> None:
        grid = self.camera.display_to_grid(int(x), int(y))
        if not grid:
            return
        gx, gy = grid
        cell = (gx // CELL, gy // CELL)
        if cell not in self.anchor_pairs:
            return
        if cell in self.selected_anchors:
            self.selected_anchors = [anchor for anchor in self.selected_anchors if anchor != cell]
        elif len(self.selected_anchors) < 2:
            self.selected_anchors.append(cell)
        else:
            self.selected_anchors = [cell]
        self._sync_anchors()

    def _pair_cells(self, a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]] | None:
        cells: list[tuple[int, int]] = []
        if a[0] == b[0]:
            y0, y1 = sorted((a[1], b[1]))
            cells = [(a[0], y) for y in range(y0 + 1, y1)]
        elif a[1] == b[1]:
            x0, x1 = sorted((a[0], b[0]))
            cells = [(x, a[1]) for x in range(x0 + 1, x1)]
        if not cells:
            return None
        for link in self.links:
            if {tuple(link["a"]), tuple(link["b"])} == {a, b}:  # type: ignore[arg-type]
                return [tuple(cell) for cell in link["cells"]]  # type: ignore[arg-type]
        return None

    def _freeze_selected_bridge(self) -> None:
        if len(self.selected_anchors) != 2:
            return
        cells = self._pair_cells(self.selected_anchors[0], self.selected_anchors[1])
        if cells:
            self.bridges.update(cells)
            self._sync_bridges()
        self.selected_anchors = []
        self._sync_anchors()

    def _at_goal(self) -> bool:
        return self._avatar_cell() in self.goal_cells

    def step(self) -> None:
        if self.action.id == GameAction.ACTION7:
            if self.history:
                self._restore_snapshot(self.history.pop())
            self.complete_action()
            return

        self._save_history()
        if self.action.id == GameAction.ACTION1:
            self._move_avatar(0, -1)
        elif self.action.id == GameAction.ACTION2:
            self._move_avatar(0, 1)
        elif self.action.id == GameAction.ACTION3:
            self._move_avatar(-1, 0)
        elif self.action.id == GameAction.ACTION4:
            self._move_avatar(1, 0)
        elif self.action.id == GameAction.ACTION5:
            self._freeze_selected_bridge()
        elif self.action.id == GameAction.ACTION6:
            self._click_anchor(self.action.data["x"], self.action.data["y"])

        self.steps_used += 1
        self._refresh_hud()
        if self._at_goal():
            self.next_level()
        elif self.steps_used >= self.step_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((2, 8), dtype=np.int16)
        for idx, (cx, cy) in enumerate(self.selected_anchors):
            state[0, idx] = cx * 16 + cy
        for idx, (cx, cy) in enumerate(sorted(self.bridges)):
            if idx >= 8:
                break
            state[1, idx] = cx * 16 + cy
        return state
