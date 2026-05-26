"""jc9r."""

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


BACKGROUND_COLOR = 1
PADDING_COLOR = 4
WALL_COLOR = 5
HUD_BG = 4
HUD_EMPTY = 2
AMBER = 12
CYAN = 9
INVERTER_COLOR = 14
TARGET_CORE = 0
TARGET_OFF = 2

CELL = 5
GRID_CELLS = 12
GRID_SIZE = GRID_CELLS * CELL


def _frame_pixels() -> list[list[int]]:
    rows: list[list[int]] = []
    for y in range(GRID_SIZE):
        row: list[int] = []
        cy = y // CELL
        for x in range(GRID_SIZE):
            cx = x // CELL
            if cx in (0, GRID_CELLS - 1) or cy in (0, GRID_CELLS - 1):
                row.append(WALL_COLOR)
            else:
                row.append(-1)
        rows.append(row)
    return rows


def _wall_block_pixels() -> list[list[int]]:
    return [[WALL_COLOR for _ in range(CELL)] for _ in range(CELL)]


def _target_pixels(color: int) -> list[list[int]]:
    return [
        [color, color, color, color, color],
        [color, -1, -1, -1, color],
        [color, -1, -1, -1, color],
        [color, -1, -1, -1, color],
        [color, color, color, color, color],
    ]


def _avatar_pixels(color: int) -> list[list[int]]:
    return [
        [-1, -1, color, -1, -1],
        [-1, color, color, color, -1],
        [color, color, WALL_COLOR, color, color],
        [-1, color, color, color, -1],
        [-1, -1, color, -1, -1],
    ]


def _bead_pixels(color: int) -> list[list[int]]:
    return [
        [-1, -1, color, -1, -1],
        [-1, color, color, color, -1],
        [color, color, color, color, color],
        [-1, color, color, color, -1],
        [-1, -1, color, -1, -1],
    ]


def _inverter_pixels() -> list[list[int]]:
    return [
        [INVERTER_COLOR, -1, -1, -1, INVERTER_COLOR],
        [-1, INVERTER_COLOR, -1, INVERTER_COLOR, -1],
        [-1, -1, INVERTER_COLOR, -1, -1],
        [-1, INVERTER_COLOR, -1, INVERTER_COLOR, -1],
        [INVERTER_COLOR, -1, -1, -1, INVERTER_COLOR],
    ]


sprites = {
    "avatar_amber": Sprite(
        pixels=_avatar_pixels(AMBER),
        name="avatar_amber",
        visible=True,
        collidable=True,
        tags=["avatar", "amber"],
        layer=3,
    ),
    "avatar_cyan": Sprite(
        pixels=_avatar_pixels(CYAN),
        name="avatar_cyan",
        visible=True,
        collidable=True,
        tags=["avatar", "cyan"],
        layer=3,
    ),
    "bead_amber": Sprite(
        pixels=_bead_pixels(AMBER),
        name="bead_amber",
        visible=True,
        collidable=True,
        tags=["bead", "amber"],
        layer=2,
    ),
    "bead_cyan": Sprite(
        pixels=_bead_pixels(CYAN),
        name="bead_cyan",
        visible=True,
        collidable=True,
        tags=["bead", "cyan"],
        layer=2,
    ),
    "frame_wall": Sprite(
        pixels=_frame_pixels(),
        name="frame_wall",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    ),
    "inverter": Sprite(
        pixels=_inverter_pixels(),
        name="inverter",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["inverter"],
        layer=1,
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
    "wall_block": Sprite(
        pixels=_wall_block_pixels(),
        name="wall_block",
        visible=True,
        collidable=True,
        tags=["wall", "cell_wall"],
        layer=0,
    ),
}


def _at(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _avatar_pair(cx: int, cy: int, start_charge: str) -> list[Sprite]:
    amber = sprites["avatar_amber"].clone().set_position(*_at(cx, cy))
    cyan = sprites["avatar_cyan"].clone().set_position(*_at(cx, cy))
    if start_charge == "amber":
        cyan.set_interaction(InteractionMode.REMOVED)
    else:
        amber.set_interaction(InteractionMode.REMOVED)
    return [amber, cyan]


def _bead_pair(cx: int, cy: int, start_charge: str) -> list[Sprite]:
    amber = sprites["bead_amber"].clone().set_position(*_at(cx, cy))
    cyan = sprites["bead_cyan"].clone().set_position(*_at(cx, cy))
    if start_charge == "amber":
        cyan.set_interaction(InteractionMode.REMOVED)
    else:
        amber.set_interaction(InteractionMode.REMOVED)
    return [amber, cyan]


def _wall_sprites(cells: list[tuple[int, int]]) -> list[Sprite]:
    return [sprites["wall_block"].clone().set_position(*_at(cx, cy)) for cx, cy in cells]


L2_WALLS = [(5, cy) for cy in range(1, 11) if cy != 6]


levels = [
    Level(
        sprites=[
            sprites["frame_wall"].clone().set_position(0, 0),
            sprites["target_amber"].clone().set_position(*_at(7, 4)),
            *_avatar_pair(3, 5, "cyan"),
            *_bead_pair(6, 4, "amber"),
        ],
        grid_size=(GRID_SIZE, GRID_SIZE),
        data={
            "step_budget": 10,
            "internal_walls": [],
            "inverters": [],
        },
    ),
    Level(
        sprites=[
            sprites["frame_wall"].clone().set_position(0, 0),
            *_wall_sprites(L2_WALLS),
            sprites["target_amber"].clone().set_position(*_at(8, 3)),
            sprites["target_cyan"].clone().set_position(*_at(8, 9)),
            *_avatar_pair(3, 6, "cyan"),
            *_bead_pair(7, 3, "amber"),
            *_bead_pair(8, 8, "cyan"),
        ],
        grid_size=(GRID_SIZE, GRID_SIZE),
        data={
            "step_budget": 20,
            "internal_walls": L2_WALLS,
            "inverters": [],
        },
    ),
    Level(
        sprites=[
            sprites["frame_wall"].clone().set_position(0, 0),
            *_wall_sprites(L2_WALLS),
            sprites["inverter"].clone().set_position(*_at(8, 3)),
            sprites["target_cyan"].clone().set_position(*_at(9, 2)),
            sprites["target_amber"].clone().set_position(*_at(9, 9)),
            *_avatar_pair(3, 6, "amber"),
            *_bead_pair(7, 3, "amber"),
            *_bead_pair(9, 8, "amber"),
        ],
        grid_size=(GRID_SIZE, GRID_SIZE),
        data={
            "step_budget": 30,
            "internal_walls": L2_WALLS,
            "inverters": [(8, 3)],
        },
    ),
]


class ChargeHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self.steps_remaining = 0
        self.max_steps = 1
        self.charge = "amber"

    def set_state(self, steps_remaining: int, max_steps: int, charge: str) -> None:
        self.steps_remaining = max(0, steps_remaining)
        self.max_steps = max(1, max_steps)
        self.charge = charge

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        frame[60:64, :] = HUD_BG
        usable = 48
        filled = int(round((self.steps_remaining / self.max_steps) * usable))
        frame[60:64, 2 : 2 + usable] = HUD_EMPTY
        if filled > 0:
            frame[60:64, 2 : 2 + filled] = AMBER if self.charge == "amber" else CYAN
        frame[60:64, 54:62] = AMBER if self.charge == "amber" else CYAN
        frame[61:63, 56:60] = TARGET_CORE
        return frame


class Jc9r(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = ChargeHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._hud],
        )
        super().__init__(
            game_id="jc9r",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        self.step_budget = int(level.get_data("step_budget") or 1)
        self.steps_used = 0
        self.wall_cells = set()
        for i in range(GRID_CELLS):
            self.wall_cells.add((i, 0))
            self.wall_cells.add((i, GRID_CELLS - 1))
            self.wall_cells.add((0, i))
            self.wall_cells.add((GRID_CELLS - 1, i))
        for cell in level.get_data("internal_walls") or []:
            self.wall_cells.add(tuple(cell))
        self.inverter_cells = {tuple(cell) for cell in level.get_data("inverters") or []}

        avatar_variants = [s for s in level.get_sprites() if "avatar" in s.tags]
        self.avatar_variants = {
            self._charge_from_tags(sprite): sprite for sprite in avatar_variants
        }
        self.avatar_charge = (
            "amber"
            if self.avatar_variants["amber"].interaction != InteractionMode.REMOVED
            else "cyan"
        )

        bead_groups: dict[tuple[int, int], dict[str, Sprite]] = {}
        for sprite in level.get_sprites():
            if "bead" not in sprite.tags:
                continue
            bead_groups.setdefault((sprite.x, sprite.y), {})[
                self._charge_from_tags(sprite)
            ] = sprite
        self.beads: list[dict[str, object]] = []
        for key in sorted(bead_groups):
            variants = bead_groups[key]
            charge = (
                "amber"
                if variants["amber"].interaction != InteractionMode.REMOVED
                else "cyan"
            )
            self.beads.append(
                {
                    "amber": variants["amber"],
                    "cyan": variants["cyan"],
                    "charge": charge,
                }
            )

        self.targets = []
        for sprite in level.get_sprites():
            if "target" not in sprite.tags:
                continue
            self.targets.append(
                (
                    sprite.x // CELL,
                    sprite.y // CELL,
                    self._charge_from_tags(sprite),
                )
            )
        self._sync_avatar()
        for bead in self.beads:
            self._sync_bead(bead)
        self._refresh_hud()

    def _charge_from_tags(self, sprite: Sprite) -> str:
        return "amber" if "amber" in sprite.tags else "cyan"

    def _avatar_cell(self) -> tuple[int, int]:
        sprite = self.avatar_variants[self.avatar_charge]
        return (sprite.x // CELL, sprite.y // CELL)

    def _bead_cell(self, bead: dict[str, object]) -> tuple[int, int]:
        sprite = bead[bead["charge"]]  # type: ignore[index]
        return (sprite.x // CELL, sprite.y // CELL)

    def _set_pair_cell(self, pair: dict[str, Sprite], cx: int, cy: int) -> None:
        px, py = _at(cx, cy)
        pair["amber"].set_position(px, py)
        pair["cyan"].set_position(px, py)

    def _set_bead_cell(self, bead: dict[str, object], cx: int, cy: int) -> None:
        self._set_pair_cell(
            {"amber": bead["amber"], "cyan": bead["cyan"]},  # type: ignore[arg-type]
            cx,
            cy,
        )

    def _sync_avatar(self) -> None:
        if self.avatar_charge == "amber":
            self.avatar_variants["amber"].set_interaction(InteractionMode.TANGIBLE)
            self.avatar_variants["cyan"].set_interaction(InteractionMode.REMOVED)
        else:
            self.avatar_variants["amber"].set_interaction(InteractionMode.REMOVED)
            self.avatar_variants["cyan"].set_interaction(InteractionMode.TANGIBLE)

    def _sync_bead(self, bead: dict[str, object]) -> None:
        if bead["charge"] == "amber":
            bead["amber"].set_interaction(InteractionMode.TANGIBLE)  # type: ignore[index]
            bead["cyan"].set_interaction(InteractionMode.REMOVED)  # type: ignore[index]
        else:
            bead["amber"].set_interaction(InteractionMode.REMOVED)  # type: ignore[index]
            bead["cyan"].set_interaction(InteractionMode.TANGIBLE)  # type: ignore[index]

    def _refresh_hud(self) -> None:
        self._hud.set_state(self.step_budget - self.steps_used, self.step_budget, self.avatar_charge)

    def _cell_open_for_avatar(self, cx: int, cy: int) -> bool:
        if (cx, cy) in self.wall_cells:
            return False
        return self._find_bead_at(cx, cy) is None

    def _find_bead_at(self, cx: int, cy: int):
        for bead in self.beads:
            if self._bead_cell(bead) == (cx, cy):
                return bead
        return None

    def _move_avatar(self, dx: int, dy: int) -> None:
        cx, cy = self._avatar_cell()
        nx, ny = cx + dx, cy + dy
        if self._cell_open_for_avatar(nx, ny):
            self.avatar_variants["amber"].move(dx * CELL, dy * CELL)
            self.avatar_variants["cyan"].move(dx * CELL, dy * CELL)

    def _toggle_avatar(self) -> None:
        self.avatar_charge = "cyan" if self.avatar_charge == "amber" else "amber"
        self._sync_avatar()

    def _emit_pulse(self) -> None:
        ax, ay = self._avatar_cell()
        plans: list[tuple[dict[str, object], int, int]] = []
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            bead = self._first_bead_on_ray(ax, ay, dx, dy)
            if bead is None or bead["charge"] != self.avatar_charge:
                continue
            bx, by = self._bead_cell(bead)
            plans.append((bead, bx + dx, by + dy))
        dest_counts: dict[tuple[int, int], int] = {}
        for _, tx, ty in plans:
            dest_counts[(tx, ty)] = dest_counts.get((tx, ty), 0) + 1
        for bead, tx, ty in plans:
            if dest_counts[(tx, ty)] > 1:
                continue
            if (tx, ty) in self.wall_cells or (tx, ty) == (ax, ay):
                continue
            if self._find_bead_at(tx, ty) is not None:
                continue
            self._set_bead_cell(bead, tx, ty)
            if (tx, ty) in self.inverter_cells:
                bead["charge"] = "cyan" if bead["charge"] == "amber" else "amber"
                self._sync_bead(bead)

    def _first_bead_on_ray(self, ax: int, ay: int, dx: int, dy: int):
        cx, cy = ax + dx, ay + dy
        while 0 <= cx < GRID_CELLS and 0 <= cy < GRID_CELLS:
            if (cx, cy) in self.wall_cells:
                return None
            bead = self._find_bead_at(cx, cy)
            if bead is not None:
                return bead
            cx += dx
            cy += dy
        return None

    def _all_targets_filled(self) -> bool:
        occupied = {
            (*self._bead_cell(bead), bead["charge"])
            for bead in self.beads
        }
        return all(target in occupied for target in self.targets)

    def step(self) -> None:
        if self.action.id == GameAction.ACTION1:
            self._move_avatar(0, -1)
        elif self.action.id == GameAction.ACTION2:
            self._move_avatar(0, 1)
        elif self.action.id == GameAction.ACTION3:
            self._move_avatar(-1, 0)
        elif self.action.id == GameAction.ACTION4:
            self._move_avatar(1, 0)
        elif self.action.id == GameAction.ACTION5:
            self._toggle_avatar()
        elif self.action.id == GameAction.ACTION6:
            self._emit_pulse()

        self.steps_used += 1
        self._refresh_hud()
        if self._all_targets_filled():
            self.next_level()
        elif self.steps_used >= self.step_budget:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
