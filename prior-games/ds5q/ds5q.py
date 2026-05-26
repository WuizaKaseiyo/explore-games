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


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------
TILE = 8
GRID_W = 64
GRID_H = 64

BACKGROUND_COLOR = 2
PADDING_COLOR = 2

CHARGE_NONE = "none"
CHARGE_GREY = "grey"
CHARGE_RED = "red"
CHARGE_BLUE = "blue"


# ---------------------------------------------------------------------
# Sprite bank
# ---------------------------------------------------------------------
sprites = {
    "avatar_uncharged": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 13, 13, 13, 13, 0, 0, 4],
            [4, 13, 13, 13, 13, 0, 0, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="avatar_uncharged",
        visible=True,
        collidable=True,
        tags=["avatar"],
    ),
    "avatar_red": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 13, 13, 13, 13, 8, 8, 4],
            [4, 13, 13, 13, 13, 8, 8, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="avatar_red",
        visible=True,
        collidable=True,
        tags=["avatar"],
    ),
    "avatar_blue": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 13, 13, 13, 13, 9, 9, 4],
            [4, 13, 13, 13, 13, 9, 9, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="avatar_blue",
        visible=True,
        collidable=True,
        tags=["avatar"],
    ),
    "wall_grey_h1": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 3, 3, 3, 3, 3, 3, 4],
            [4, 3, 3, 3, 3, 3, 3, 4],
            [4, 5, 5, 5, 5, 5, 5, 4],
            [4, 3, 3, 3, 3, 3, 3, 4],
            [4, 3, 3, 3, 3, 3, 3, 4],
            [4, 3, 3, 3, 3, 3, 3, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="wall_grey_h1",
        visible=True,
        collidable=True,
        tags=["wall", "grey"],
    ),
    "wall_red_h1": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="wall_red_h1",
        visible=True,
        collidable=True,
        tags=["wall", "red"],
    ),
    "wall_red_h2": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="wall_red_h2",
        visible=True,
        collidable=True,
        tags=["wall", "red"],
    ),
    "wall_red_h3": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 13, 13, 13, 13, 13, 13, 4],
            [4, 8, 8, 8, 8, 8, 8, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="wall_red_h3",
        visible=True,
        collidable=True,
        tags=["wall", "red"],
    ),
    "wall_blue_h1": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 15, 15, 15, 15, 15, 15, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="wall_blue_h1",
        visible=True,
        collidable=True,
        tags=["wall", "blue"],
    ),
    "wall_blue_h2": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 15, 15, 15, 15, 15, 15, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 15, 15, 15, 15, 15, 15, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="wall_blue_h2",
        visible=True,
        collidable=True,
        tags=["wall", "blue"],
    ),
    "wall_blue_h3": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 15, 15, 15, 15, 15, 15, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 15, 15, 15, 15, 15, 15, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 15, 15, 15, 15, 15, 15, 4],
            [4, 9, 9, 9, 9, 9, 9, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="wall_blue_h3",
        visible=True,
        collidable=True,
        tags=["wall", "blue"],
    ),
    "stone": Sprite(
        pixels=[
            [5, 4, 4, 4, 4, 4, 4, 5],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [5, 4, 4, 4, 4, 4, 4, 5],
        ],
        name="stone",
        visible=True,
        collidable=True,
        tags=["stone"],
    ),
    "charge_pad_red": Sprite(
        pixels=[
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 8, 8, 8, 8, 8, 8, 2],
            [2, 8, 2, 2, 2, 2, 8, 2],
            [2, 8, 2, 0, 0, 2, 8, 2],
            [2, 8, 2, 0, 0, 2, 8, 2],
            [2, 8, 2, 2, 2, 2, 8, 2],
            [2, 8, 8, 8, 8, 8, 8, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
        ],
        name="charge_pad_red",
        visible=True,
        collidable=True,
        interaction=InteractionMode.INTANGIBLE,
        tags=["pad", "red"],
    ),
    "charge_pad_blue": Sprite(
        pixels=[
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 9, 9, 9, 9, 9, 9, 2],
            [2, 9, 2, 2, 2, 2, 9, 2],
            [2, 9, 2, 0, 0, 2, 9, 2],
            [2, 9, 2, 0, 0, 2, 9, 2],
            [2, 9, 2, 2, 2, 2, 9, 2],
            [2, 9, 9, 9, 9, 9, 9, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
        ],
        name="charge_pad_blue",
        visible=True,
        collidable=True,
        interaction=InteractionMode.INTANGIBLE,
        tags=["pad", "blue"],
    ),
    "exit": Sprite(
        pixels=[
            [14, 14, 14, 14, 14, 14, 14, 14],
            [14, 0, 0, 0, 0, 0, 0, 14],
            [14, 0, 14, 14, 14, 14, 0, 14],
            [14, 0, 14, 0, 0, 14, 0, 14],
            [14, 0, 14, 0, 0, 14, 0, 14],
            [14, 0, 14, 14, 14, 14, 0, 14],
            [14, 0, 0, 0, 0, 0, 0, 14],
            [14, 14, 14, 14, 14, 14, 14, 14],
        ],
        name="exit",
        visible=True,
        collidable=True,
        interaction=InteractionMode.INTANGIBLE,
        tags=["exit"],
    ),
}


# ---------------------------------------------------------------------
# Level builders
# ---------------------------------------------------------------------
def _placed(name: str, gx: int, gy: int, removed: bool = False) -> Sprite:
    s = sprites[name].clone().set_position(gx * TILE, gy * TILE)
    if removed:
        s.set_interaction(InteractionMode.REMOVED)
    return s


def _wall_variants(gx: int, gy: int, color: str, initial_hardness: int) -> list[Sprite]:
    out = []
    for h in range(1, initial_hardness + 1):
        out.append(_placed(f"wall_{color}_h{h}", gx, gy, removed=(h != initial_hardness)))
    return out


def _avatar_at(gx: int, gy: int) -> list[Sprite]:
    return [
        _placed("avatar_uncharged", gx, gy),
        _placed("avatar_red", gx, gy, removed=True),
        _placed("avatar_blue", gx, gy, removed=True),
    ]


def _build_level_1() -> list[Sprite]:
    out: list[Sprite] = []
    out.extend(_avatar_at(0, 4))
    out.append(_placed("exit", 7, 4))
    out.extend(_wall_variants(3, 4, "grey", 1))
    out.extend(_wall_variants(5, 4, "grey", 1))
    for col in range(8):
        out.append(_placed("stone", col, 3))
        out.append(_placed("stone", col, 5))
    return out


def _build_level_2() -> list[Sprite]:
    out: list[Sprite] = []
    out.extend(_avatar_at(0, 4))
    out.append(_placed("exit", 7, 4))
    out.append(_placed("charge_pad_red", 1, 0))
    out.append(_placed("charge_pad_blue", 6, 2))
    out.extend(_wall_variants(3, 4, "red", 1))
    out.extend(_wall_variants(5, 4, "blue", 1))
    for row in range(8):
        if row != 4:
            out.append(_placed("stone", 3, row))
    for row in range(8):
        if row != 4:
            out.append(_placed("stone", 7, row))
    out.append(_placed("stone", 5, 1))
    out.append(_placed("stone", 5, 3))
    out.append(_placed("stone", 5, 5))
    out.append(_placed("stone", 6, 3))
    out.append(_placed("stone", 6, 5))
    return out


def _build_level_3() -> list[Sprite]:
    out: list[Sprite] = []
    out.extend(_avatar_at(0, 4))
    out.append(_placed("exit", 7, 4))
    out.append(_placed("charge_pad_red", 1, 0))
    out.append(_placed("charge_pad_blue", 6, 2))
    out.extend(_wall_variants(3, 1, "red", 2))
    out.extend(_wall_variants(3, 4, "red", 3))
    out.extend(_wall_variants(5, 4, "blue", 1))
    for row in range(8):
        if row not in (1, 4):
            out.append(_placed("stone", 3, row))
    for row in range(8):
        if row != 4:
            out.append(_placed("stone", 7, row))
    out.append(_placed("stone", 5, 1))
    out.append(_placed("stone", 5, 3))
    out.append(_placed("stone", 5, 5))
    out.append(_placed("stone", 6, 3))
    out.append(_placed("stone", 6, 5))
    return out


levels = [
    Level(
        sprites=_build_level_1(),
        grid_size=(GRID_W, GRID_H),
        data={"step_budget": 30, "charge_initial": CHARGE_GREY},
    ),
    Level(
        sprites=_build_level_2(),
        grid_size=(GRID_W, GRID_H),
        data={"step_budget": 80, "charge_initial": CHARGE_NONE},
    ),
    Level(
        sprites=_build_level_3(),
        grid_size=(GRID_W, GRID_H),
        data={"step_budget": 90, "charge_initial": CHARGE_NONE},
    ),
]


# ---------------------------------------------------------------------
# HUD widget
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0) -> None:
        self._max = max_steps
        self._current = max_steps

    def set_max(self, m: int) -> None:
        self._max = m
        self._current = m

    def set_current(self, c: int) -> None:
        if self._max <= 0:
            return
        self._current = max(0, min(c, self._max))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self._max <= 0:
            return frame
        ratio = self._current / self._max
        filled = int(round(64 * ratio))
        for x in range(64):
            if x < filled:
                frame[0, x] = 4
            else:
                frame[0, x] = 0
        return frame


# ---------------------------------------------------------------------
# Game class
# ---------------------------------------------------------------------
class Ds5q(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter = StepCounterHud(0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter],
        )
        self.charge_state: str = CHARGE_NONE
        self.step_budget: int = 30
        self.wall_hardness: dict = {}
        self.wall_color_at: dict = {}
        self.wall_variants: dict = {}
        self.stone_tiles: set = set()
        self.pad_at: dict = {}
        self.exit_tile = (0, 0)
        self.avatar_variants: dict = {}
        super().__init__(
            game_id="ds5q",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    def on_set_level(self, level: Level) -> None:
        self.camera.width = GRID_W
        self.camera.height = GRID_H

        self.wall_hardness = {}
        self.wall_color_at = {}
        self.wall_variants = {}
        self.stone_tiles = set()
        self.pad_at = {}
        self.avatar_variants = {}
        self.exit_tile = (0, 0)
        self.charge_state = CHARGE_NONE

        self.step_budget = int(level.get_data("step_budget") or 30)
        initial_charge = level.get_data("charge_initial") or CHARGE_NONE
        self._step_counter.set_max(self.step_budget)

        for sprite in level.get_sprites():
            gx = sprite.x // TILE
            gy = sprite.y // TILE
            tile = (gx, gy)
            if "wall" in sprite.tags:
                parts = sprite.name.split("_")
                color = parts[1]
                hardness = int(parts[2][1:])
                self.wall_color_at[tile] = color
                self.wall_variants.setdefault(tile, {})[hardness] = sprite
                if sprite.interaction == InteractionMode.TANGIBLE:
                    self.wall_hardness[tile] = hardness
            elif "stone" in sprite.tags:
                self.stone_tiles.add(tile)
            elif "pad" in sprite.tags:
                pad_color = "red" if "red" in sprite.tags else "blue"
                self.pad_at[tile] = pad_color
            elif "exit" in sprite.tags:
                self.exit_tile = tile
            elif "avatar" in sprite.tags:
                if sprite.name == "avatar_uncharged":
                    self.avatar_variants[CHARGE_NONE] = sprite
                    self.avatar_variants[CHARGE_GREY] = sprite
                elif sprite.name == "avatar_red":
                    self.avatar_variants[CHARGE_RED] = sprite
                elif sprite.name == "avatar_blue":
                    self.avatar_variants[CHARGE_BLUE] = sprite

        self._set_charge(initial_charge)

    def _set_charge(self, new_state: str) -> None:
        if not self.avatar_variants:
            self.charge_state = new_state
            return
        current = self._active_avatar()
        cx, cy = current.x, current.y
        for variant in set(self.avatar_variants.values()):
            variant.set_interaction(InteractionMode.REMOVED)
        self.charge_state = new_state
        active = self.avatar_variants.get(new_state)
        if active is None:
            active = self.avatar_variants[CHARGE_NONE]
        active.set_interaction(InteractionMode.TANGIBLE)
        for variant in set(self.avatar_variants.values()):
            variant.set_position(cx, cy)

    def _active_avatar(self) -> Sprite:
        return self.avatar_variants.get(self.charge_state, self.avatar_variants[CHARGE_NONE])

    def step(self) -> None:
        if self._action_count >= self.step_budget:
            self.lose()
            self.complete_action()
            return

        self._step_counter.set_current(self.step_budget - self._action_count - 1)

        action_id = self.action.id
        if action_id == GameAction.ACTION1:
            self._try_walk(0, -TILE)
        elif action_id == GameAction.ACTION2:
            self._try_walk(0, TILE)
        elif action_id == GameAction.ACTION3:
            self._try_walk(-TILE, 0)
        elif action_id == GameAction.ACTION4:
            self._try_walk(TILE, 0)
        elif action_id == GameAction.ACTION5:
            self._erode_adjacent()

        avatar = self._active_avatar()
        avatar_tile = (avatar.x // TILE, avatar.y // TILE)
        if avatar_tile in self.pad_at:
            new_charge = self.pad_at[avatar_tile]
            if new_charge != self.charge_state:
                self._set_charge(new_charge)

        if avatar_tile == self.exit_tile:
            self.next_level()

        self.complete_action()

    def _try_walk(self, dx: int, dy: int) -> bool:
        avatar = self._active_avatar()
        new_x = avatar.x + dx
        new_y = avatar.y + dy
        if new_x < 0 or new_y < 0 or new_x + TILE > GRID_W or new_y + TILE > GRID_H:
            return False
        target_tile = (new_x // TILE, new_y // TILE)
        if target_tile in self.stone_tiles:
            return False
        if target_tile in self.wall_hardness:
            return False
        for variant in set(self.avatar_variants.values()):
            variant.set_position(new_x, new_y)
        return True

    def _erode_adjacent(self) -> None:
        if self.charge_state == CHARGE_NONE:
            return
        avatar = self._active_avatar()
        ax = avatar.x // TILE
        ay = avatar.y // TILE
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            tile = (ax + dx, ay + dy)
            if tile not in self.wall_hardness:
                continue
            wall_color = self.wall_color_at.get(tile)
            if wall_color != self.charge_state:
                continue
            current_h = self.wall_hardness[tile]
            new_h = current_h - 1
            current_sprite = self.wall_variants[tile].get(current_h)
            if current_sprite is not None:
                current_sprite.set_interaction(InteractionMode.REMOVED)
            if new_h > 0:
                next_sprite = self.wall_variants[tile].get(new_h)
                if next_sprite is not None:
                    next_sprite.set_interaction(InteractionMode.TANGIBLE)
                self.wall_hardness[tile] = new_h
            else:
                del self.wall_hardness[tile]

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._action_count
        state[0, 1] = {CHARGE_NONE: 0, CHARGE_GREY: 1, CHARGE_RED: 2, CHARGE_BLUE: 3}.get(
            self.charge_state, 0
        )
        return state
