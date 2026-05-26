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
FLOOR = 2
HUD_EMPTY = 4
HUD_FILL = 15
AMBER = 12
CYAN = 9
TARGET_CORE = 0
BLOCK = 8
FILTER = 14
AVATAR = 6


LEVEL_LAYOUTS = [
    (
        (
            "########",
            "#..a...#",
            "#..#...#",
            "#.P.#..#",
            "#..A...#",
            "#......#",
            "#......#",
            "########",
        ),
        14,
    ),
    (
        (
            "########",
            "#..a.c.#",
            "#..#.#.#",
            "#.P.#..#",
            "#..A.C.#",
            "#......#",
            "#......#",
            "########",
        ),
        22,
    ),
    (
        (
            "########",
            "#.a..c.#",
            "#.#..#.#",
            "#..PB..#",
            "#....###",
            "#.A..C.#",
            "#......#",
            "########",
        ),
        28,
    ),
]


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _wall_pixels() -> list[list[int]]:
    return [[WALL for _ in range(CELL)] for _ in range(CELL)]


def _block_pixels() -> list[list[int]]:
    return [
        [BLOCK, BLOCK, BLOCK, BLOCK],
        [BLOCK, 4, 4, BLOCK],
        [BLOCK, 4, 4, BLOCK],
        [BLOCK, BLOCK, BLOCK, BLOCK],
    ]


def _avatar_pixels() -> list[list[int]]:
    return [
        [-1, AVATAR, AVATAR, -1],
        [AVATAR, TARGET_CORE, TARGET_CORE, AVATAR],
        [AVATAR, TARGET_CORE, TARGET_CORE, AVATAR],
        [-1, AVATAR, AVATAR, -1],
    ]


def _seed_pixels(color: int) -> list[list[int]]:
    return [
        [-1, color, color, -1],
        [color, TARGET_CORE, TARGET_CORE, color],
        [color, TARGET_CORE, TARGET_CORE, color],
        [-1, color, color, -1],
    ]


def _selector_pixels(color: int) -> list[list[int]]:
    return [
        [color, color, color, color],
        [color, -1, -1, color],
        [color, -1, -1, color],
        [color, color, color, color],
    ]


def _target_pixels(color: int) -> list[list[int]]:
    return [
        [color, color, color, color],
        [color, -1, -1, color],
        [color, -1, TARGET_CORE, color],
        [color, color, color, color],
    ]


def _filter_pixels(color: int) -> list[list[int]]:
    return [
        [TARGET_CORE, TARGET_CORE, TARGET_CORE, TARGET_CORE],
        [TARGET_CORE, FILTER, FILTER, TARGET_CORE],
        [TARGET_CORE, FILTER, FILTER, TARGET_CORE],
        [TARGET_CORE, TARGET_CORE, TARGET_CORE, TARGET_CORE],
    ]


def _crystal_pixels(color: int) -> list[list[int]]:
    return [
        [color, -1, color, -1],
        [-1, color, color, color],
        [color, color, color, -1],
        [-1, color, -1, color],
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
    "block": Sprite(
        pixels=_block_pixels(),
        name="block",
        visible=True,
        collidable=True,
        tags=["block"],
        layer=3,
    ),
    "avatar": Sprite(
        pixels=_avatar_pixels(),
        name="avatar",
        visible=True,
        collidable=True,
        tags=["avatar"],
        layer=4,
    ),
    "seed_amber": Sprite(
        pixels=_seed_pixels(AMBER),
        name="seed_amber",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["seed", "amber"],
        layer=2,
    ),
    "seed_cyan": Sprite(
        pixels=_seed_pixels(CYAN),
        name="seed_cyan",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["seed", "cyan"],
        layer=2,
    ),
    "selector_amber": Sprite(
        pixels=_selector_pixels(AMBER),
        name="selector_amber",
        visible=True,
        collidable=False,
        interaction=InteractionMode.REMOVED,
        tags=["selector", "amber"],
        layer=4,
    ),
    "selector_cyan": Sprite(
        pixels=_selector_pixels(CYAN),
        name="selector_cyan",
        visible=True,
        collidable=False,
        interaction=InteractionMode.REMOVED,
        tags=["selector", "cyan"],
        layer=4,
    ),
    "target_amber": Sprite(
        pixels=_target_pixels(AMBER),
        name="target_amber",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target", "amber"],
        layer=1,
    ),
    "target_cyan": Sprite(
        pixels=_target_pixels(CYAN),
        name="target_cyan",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target", "cyan"],
        layer=1,
    ),
    "filter_amber": Sprite(
        pixels=_filter_pixels(AMBER),
        name="filter_amber",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["filter", "amber"],
        layer=2,
    ),
    "filter_cyan": Sprite(
        pixels=_filter_pixels(CYAN),
        name="filter_cyan",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["filter", "cyan"],
        layer=2,
    ),
    "crystal_amber": Sprite(
        pixels=_crystal_pixels(AMBER),
        name="crystal_amber",
        visible=True,
        collidable=True,
        interaction=InteractionMode.REMOVED,
        tags=["crystal", "amber"],
        layer=3,
    ),
    "crystal_cyan": Sprite(
        pixels=_crystal_pixels(CYAN),
        name="crystal_cyan",
        visible=True,
        collidable=True,
        interaction=InteractionMode.REMOVED,
        tags=["crystal", "cyan"],
        layer=3,
    ),
}


def _build_level(layout: tuple[str, ...], step_budget: int) -> Level:
    sprites: list[Sprite] = []
    for cy, row in enumerate(layout):
        for cx, ch in enumerate(row):
            px, py = _cell(cx, cy)
            if ch == "#":
                sprites.append(SPRITES["wall"].clone().set_position(px, py))
                continue

            sprites.append(
                SPRITES["crystal_amber"]
                .clone()
                .set_position(px, py)
                .set_interaction(InteractionMode.REMOVED)
            )
            sprites.append(
                SPRITES["crystal_cyan"]
                .clone()
                .set_position(px, py)
                .set_interaction(InteractionMode.REMOVED)
            )

            if ch == "P":
                sprites.append(SPRITES["avatar"].clone().set_position(px, py))
            elif ch == "B":
                sprites.append(SPRITES["block"].clone().set_position(px, py))
            elif ch == "A":
                sprites.append(SPRITES["seed_amber"].clone().set_position(px, py))
                sprites.append(SPRITES["selector_amber"].clone().set_position(px, py))
            elif ch == "C":
                sprites.append(SPRITES["seed_cyan"].clone().set_position(px, py))
                sprites.append(SPRITES["selector_cyan"].clone().set_position(px, py))
            elif ch == "a":
                sprites.append(SPRITES["target_amber"].clone().set_position(px, py))
            elif ch == "c":
                sprites.append(SPRITES["target_cyan"].clone().set_position(px, py))
            elif ch == "F":
                sprites.append(SPRITES["filter_amber"].clone().set_position(px, py))
            elif ch == "G":
                sprites.append(SPRITES["filter_cyan"].clone().set_position(px, py))
    return Level(
        sprites=sprites,
        grid_size=(GRID_SIZE, GRID_SIZE),
        data={"step_budget": step_budget},
    )


LEVELS = [_build_level(layout, budget) for layout, budget in LEVEL_LAYOUTS]


class TopLifeBar(RenderableUserDisplay):
    def __init__(self) -> None:
        self.current = 0
        self.maximum = 1
        self.color = HUD_FILL

    def set_state(self, current: int, maximum: int, color: int) -> None:
        self.current = max(0, current)
        self.maximum = max(1, maximum)
        self.color = color

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        frame[0:4, :] = HUD_EMPTY
        filled = int(round((self.current / self.maximum) * 64))
        if filled > 0:
            frame[0:4, :filled] = self.color
        return frame


class Cf7m(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = TopLifeBar()
        camera = Camera(
            background=BACKGROUND,
            letter_box=PADDING,
            interfaces=[self._hud],
        )
        super().__init__(
            game_id="cf7m",
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
        self.blocks = [sprite for sprite in level.get_sprites() if "block" in sprite.tags]
        self.seed_cells: dict[str, tuple[int, int]] = {}
        self.seed_markers: dict[str, Sprite] = {}
        self.targets: dict[str, set[tuple[int, int]]] = {"amber": set(), "cyan": set()}
        self.filters: dict[str, set[tuple[int, int]]] = {"amber": set(), "cyan": set()}
        self.crystal_sprites: dict[str, dict[tuple[int, int], Sprite]] = {"amber": {}, "cyan": {}}
        for sprite in level.get_sprites():
            cell = (sprite.x // CELL, sprite.y // CELL)
            if "seed" in sprite.tags:
                color = self._color_from_tags(sprite)
                self.seed_cells[color] = cell
            elif "selector" in sprite.tags:
                color = self._color_from_tags(sprite)
                self.seed_markers[color] = sprite
            elif "target" in sprite.tags:
                self.targets[self._color_from_tags(sprite)].add(cell)
            elif "filter" in sprite.tags:
                self.filters[self._color_from_tags(sprite)].add(cell)
            elif "crystal" in sprite.tags:
                self.crystal_sprites[self._color_from_tags(sprite)][cell] = sprite

        self.crystals: dict[str, set[tuple[int, int]]] = {"amber": set(), "cyan": set()}
        self.selected_color: str | None = None
        self._sync_markers()
        self._refresh_hud()

    def _color_from_tags(self, sprite: Sprite) -> str:
        return "amber" if "amber" in sprite.tags else "cyan"

    def _avatar_cell(self) -> tuple[int, int]:
        return (self.avatar.x // CELL, self.avatar.y // CELL)

    def _block_cells(self) -> set[tuple[int, int]]:
        return {(sprite.x // CELL, sprite.y // CELL) for sprite in self.blocks}

    def _occupied_crystal_cells(self) -> set[tuple[int, int]]:
        return self.crystals["amber"] | self.crystals["cyan"]

    def _sync_markers(self) -> None:
        for color, marker in self.seed_markers.items():
            marker.set_interaction(
                InteractionMode.TANGIBLE if self.selected_color == color else InteractionMode.REMOVED
            )

    def _hud_color(self) -> int:
        return HUD_FILL

    def _refresh_hud(self) -> None:
        self._hud.set_state(
            self.step_budget - self.steps_used,
            self.step_budget,
            self._hud_color(),
        )

    def _save_history(self) -> None:
        self.history.append(
            {
                "avatar": self._avatar_cell(),
                "blocks": sorted(self._block_cells()),
                "crystals_amber": sorted(self.crystals["amber"]),
                "crystals_cyan": sorted(self.crystals["cyan"]),
                "selected": self.selected_color,
                "steps_used": self.steps_used,
            }
        )

    def _restore_snapshot(self, snapshot: dict[str, object]) -> None:
        ax, ay = snapshot["avatar"]  # type: ignore[misc]
        self.avatar.set_position(*_cell(ax, ay))
        for sprite, (bx, by) in zip(self.blocks, snapshot["blocks"], strict=True):  # type: ignore[arg-type]
            sprite.set_position(*_cell(bx, by))
        self.crystals["amber"] = set(snapshot["crystals_amber"])  # type: ignore[arg-type]
        self.crystals["cyan"] = set(snapshot["crystals_cyan"])  # type: ignore[arg-type]
        self.selected_color = snapshot["selected"]  # type: ignore[assignment]
        self.steps_used = int(snapshot["steps_used"])
        self._sync_crystals()
        self._sync_markers()
        self._refresh_hud()

    def _sync_crystals(self) -> None:
        for color in ("amber", "cyan"):
            active = self.crystals[color]
            for cell, sprite in self.crystal_sprites[color].items():
                sprite.set_interaction(
                    InteractionMode.TANGIBLE if cell in active else InteractionMode.REMOVED
                )

    def _open_for_avatar(self, cx: int, cy: int) -> bool:
        if (cx, cy) in self.wall_cells:
            return False
        if (cx, cy) in self._block_cells():
            return False
        if (cx, cy) in self._occupied_crystal_cells():
            return False
        return True

    def _open_for_block(self, cx: int, cy: int) -> bool:
        if (cx, cy) in self.wall_cells:
            return False
        if (cx, cy) in self._block_cells():
            return False
        if (cx, cy) in self._occupied_crystal_cells():
            return False
        if (cx, cy) in self.seed_cells.values():
            return False
        if (cx, cy) in self.targets["amber"] | self.targets["cyan"]:
            return False
        if (cx, cy) in self.filters["amber"] | self.filters["cyan"]:
            return False
        return True

    def _move_avatar(self, dx: int, dy: int) -> None:
        cx, cy = self._avatar_cell()
        nx, ny = cx + dx, cy + dy
        if (nx, ny) in self.wall_cells:
            return
        block_sprite = next(
            (sprite for sprite in self.blocks if (sprite.x // CELL, sprite.y // CELL) == (nx, ny)),
            None,
        )
        if block_sprite is not None:
            bx, by = nx + dx, ny + dy
            if not self._open_for_block(bx, by):
                return
            block_sprite.set_position(*_cell(bx, by))
        if self._open_for_avatar(nx, ny):
            self.avatar.set_position(*_cell(nx, ny))

    def _click_select(self, x: int, y: int) -> None:
        grid = self.camera.display_to_grid(int(x), int(y))
        if not grid:
            return
        gx, gy = grid
        cell = (gx // CELL, gy // CELL)
        for color, seed_cell in self.seed_cells.items():
            if seed_cell == cell:
                self.selected_color = color
                self._sync_markers()
                return

    def _can_grow_into(self, color: str, cell: tuple[int, int]) -> bool:
        if cell in self.wall_cells:
            return False
        if cell in self._block_cells():
            return False
        if cell in self._occupied_crystal_cells():
            return False
        if cell in self.seed_cells.values():
            return False
        if cell == self._avatar_cell():
            return False
        amber_filters = self.filters["amber"]
        cyan_filters = self.filters["cyan"]
        if color == "amber" and cell in cyan_filters:
            return False
        if color == "cyan" and cell in amber_filters:
            return False
        return 0 <= cell[0] < GRID_CELLS and 0 <= cell[1] < GRID_CELLS

    def _pulse_growth(self) -> None:
        if self.selected_color is None:
            return
        frontier = set(self.crystals[self.selected_color])
        frontier.add(self.seed_cells[self.selected_color])
        additions: set[tuple[int, int]] = set()
        for cx, cy in frontier:
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                cell = (cx + dx, cy + dy)
                if self._can_grow_into(self.selected_color, cell):
                    additions.add(cell)
        if additions:
            self.crystals[self.selected_color].update(additions)
            self._sync_crystals()

    def _all_targets_filled(self) -> bool:
        return all(
            target in self.crystals[color]
            for color, target_cells in self.targets.items()
            for target in target_cells
        )

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
            self._pulse_growth()
        elif self.action.id == GameAction.ACTION6:
            self._click_select(self.action.data["x"], self.action.data["y"])

        self.steps_used += 1
        self._refresh_hud()
        if self._all_targets_filled():
            self.next_level()
        elif self.steps_used >= self.step_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((3, GRID_CELLS), dtype=np.int16)
        for idx, (cx, cy) in enumerate(sorted(self.crystals["amber"])):
            if idx >= GRID_CELLS:
                break
            state[0, idx] = cx * 16 + cy
        for idx, (cx, cy) in enumerate(sorted(self.crystals["cyan"])):
            if idx >= GRID_CELLS:
                break
            state[1, idx] = cx * 16 + cy
        state[2, 0] = self.steps_used
        state[2, 1] = self.step_budget
        state[2, 2] = 1 if self.selected_color == "amber" else 2 if self.selected_color == "cyan" else 0
        return state
