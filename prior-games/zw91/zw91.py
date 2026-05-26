"""NovaPlay environment zw91."""

from __future__ import annotations

import numpy as np
from novaengine import (
    ActionInput,
    NovaBaseGame,
    Camera,
    GameAction,
    InteractionMode,
    Level,
    RenderableUserDisplay,
    Sprite,
)


# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "avatar_small": Sprite(
        pixels=[
            [13, 12, 12, 13],
            [12,  1,  1, 12],
            [12,  1,  1, 12],
            [13, 12, 12, 13],
        ],
        name="avatar_small",
        visible=True,
        collidable=True,
        tags=["avatar"],
        layer=3,
    ),
    "avatar_med": Sprite(
        pixels=[
            [13, 12, 12, 12, 12, 12, 12, 13],
            [12, 13, 13, 12, 12, 13, 13, 12],
            [12, 13,  1,  1,  1,  1, 13, 12],
            [12, 12,  1, 12, 12,  1, 12, 12],
            [12, 12,  1, 12, 12,  1, 12, 12],
            [12, 13,  1,  1,  1,  1, 13, 12],
            [12, 13, 13, 12, 12, 13, 13, 12],
            [13, 12, 12, 12, 12, 12, 12, 13],
        ],
        name="avatar_med",
        visible=True,
        collidable=True,
        tags=["avatar"],
        layer=3,
    ),
    "avatar_large": Sprite(
        pixels=[
            [13, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13],
            [12, 13, 12, 12, 12, 12, 12, 12, 12, 12, 13, 12],
            [12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12],
            [12, 12, 13,  1,  1,  1,  1,  1,  1, 13, 12, 12],
            [12, 12, 13,  1, 12, 12, 12, 12,  1, 13, 12, 12],
            [12, 12, 13,  1, 12,  1,  1, 12,  1, 13, 12, 12],
            [12, 12, 13,  1, 12,  1,  1, 12,  1, 13, 12, 12],
            [12, 12, 13,  1, 12, 12, 12, 12,  1, 13, 12, 12],
            [12, 12, 13,  1,  1,  1,  1,  1,  1, 13, 12, 12],
            [12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12],
            [12, 13, 12, 12, 12, 12, 12, 12, 12, 12, 13, 12],
            [13, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13],
        ],
        name="avatar_large",
        visible=True,
        collidable=True,
        tags=["avatar"],
        layer=3,
    ),
    "overload_halo": Sprite(
        pixels=[
            [-1,  7, -1, -1, -1, -1, -1,  7,  7, -1, -1, -1, -1, -1,  7, -1],
            [ 7, -1, -1, -1, -1, -1, -1,  7,  7, -1, -1, -1, -1, -1, -1,  7],
            [-1, -1,  7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  7, -1, -1],
            [-1, -1, -1,  7, -1, -1, -1, -1, -1, -1, -1, -1,  7, -1, -1, -1],
            [-1, -1, -1, -1,  7, -1, -1, -1, -1, -1, -1,  7, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1,  7, -1, -1, -1, -1,  7, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [ 7,  7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  7,  7],
            [ 7,  7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  7,  7],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1,  7, -1, -1, -1, -1,  7, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1,  7, -1, -1, -1, -1, -1, -1,  7, -1, -1, -1, -1],
            [-1, -1, -1,  7, -1, -1, -1, -1, -1, -1, -1, -1,  7, -1, -1, -1],
            [-1, -1,  7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  7, -1, -1],
            [ 7, -1, -1, -1, -1, -1, -1,  7,  7, -1, -1, -1, -1, -1, -1,  7],
            [-1,  7, -1, -1, -1, -1, -1,  7,  7, -1, -1, -1, -1, -1,  7, -1],
        ],
        name="overload_halo",
        visible=True,
        collidable=False,
        tags=["overload"],
        layer=5,
        interaction=InteractionMode.REMOVED,
    ),
    "wall_block": Sprite(
        pixels=[
            [4, 4, 5, 4],
            [4, 5, 5, 4],
            [5, 4, 4, 5],
            [4, 4, 5, 5],
        ],
        name="wall_block",
        visible=True,
        collidable=True,
        tags=["wall"],
    ),
    "wall_strip_h": Sprite(
        pixels=[
            [4, 4, 5, 4] * 16,
            [4, 5, 5, 4] * 16,
            [5, 4, 4, 5] * 16,
            [4, 4, 5, 5] * 16,
        ],
        name="wall_strip_h",
        visible=True,
        collidable=True,
        tags=["wall"],
    ),
    "wall_strip_v": Sprite(
        pixels=(
            [
                [4, 4, 5, 4],
                [4, 5, 5, 4],
                [5, 4, 4, 5],
                [4, 4, 5, 5],
            ] * 14
        ),
        name="wall_strip_v",
        visible=True,
        collidable=True,
        tags=["wall"],
    ),
    "breakaway_wall": Sprite(
        pixels=[
            [4, 7, 4, 7],
            [7, 4, 7, 4],
            [4, 7, 4, 4],
            [7, 4, 4, 7],
        ],
        name="breakaway_wall",
        visible=True,
        collidable=True,
        tags=["wall", "breakaway"],
    ),
    "shove_block": Sprite(
        pixels=[
            [15,  6,  6, 15],
            [ 6, 15, 15,  6],
            [ 6, 15, 15,  6],
            [15,  6,  6, 15],
        ],
        name="shove_block",
        visible=True,
        collidable=True,
        tags=["shove_block"],
    ),
    "socket_small": Sprite(
        pixels=[
            [12, 11, 11, 12],
            [11, -1, -1, 11],
            [11, -1, -1, 11],
            [12, 11, 11, 12],
        ],
        name="socket_small",
        visible=True,
        collidable=False,
        tags=["socket"],
        interaction=InteractionMode.INTANGIBLE,
        layer=2,
    ),
    "socket_med": Sprite(
        pixels=[
            [12, 11, 11, 11, 11, 11, 11, 12],
            [11, -1, -1, -1, -1, -1, -1, 11],
            [11, -1, -1, 11, 11, -1, -1, 11],
            [11, -1, 11, -1, -1, 11, -1, 11],
            [11, -1, 11, -1, -1, 11, -1, 11],
            [11, -1, -1, 11, 11, -1, -1, 11],
            [11, -1, -1, -1, -1, -1, -1, 11],
            [12, 11, 11, 11, 11, 11, 11, 12],
        ],
        name="socket_med",
        visible=True,
        collidable=False,
        tags=["socket"],
        interaction=InteractionMode.INTANGIBLE,
        layer=2,
    ),
    "socket_large": Sprite(
        pixels=[
            [12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12],
            [11, 11, -1, -1, -1, -1, -1, -1, -1, -1, 11, 11],
            [11, -1, -1, -1, -1, 11, 11, -1, -1, -1, -1, 11],
            [11, -1, -1, -1, 11, -1, -1, 11, -1, -1, -1, 11],
            [11, -1, -1, 11, -1, -1, -1, -1, 11, -1, -1, 11],
            [11, -1, 11, -1, -1, -1, -1, -1, -1, 11, -1, 11],
            [11, -1, 11, -1, -1, -1, -1, -1, -1, 11, -1, 11],
            [11, -1, -1, 11, -1, -1, -1, -1, 11, -1, -1, 11],
            [11, -1, -1, -1, 11, -1, -1, 11, -1, -1, -1, 11],
            [11, -1, -1, -1, -1, 11, 11, -1, -1, -1, -1, 11],
            [11, 11, -1, -1, -1, -1, -1, -1, -1, -1, 11, 11],
            [12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12],
        ],
        name="socket_large",
        visible=True,
        collidable=False,
        tags=["socket"],
        interaction=InteractionMode.INTANGIBLE,
        layer=2,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
def _perimeter_walls() -> list[Sprite]:
    return [
        sprites["wall_strip_h"].clone().set_position(0, 0),
        sprites["wall_strip_h"].clone().set_position(0, 60),
        sprites["wall_strip_v"].clone().set_position(0, 4),
        sprites["wall_strip_v"].clone().set_position(60, 4),
    ]


def _avatar_set_at(x: int, y: int) -> list[Sprite]:
    return [
        sprites["avatar_small"].clone().set_position(x, y),
        sprites["avatar_med"]
        .clone()
        .set_position(x, y)
        .set_interaction(InteractionMode.REMOVED),
        sprites["avatar_large"]
        .clone()
        .set_position(x, y)
        .set_interaction(InteractionMode.REMOVED),
        sprites["overload_halo"].clone().set_position(x - 2, y - 2),
    ]


levels = [
    Level(
        sprites=[
            *_perimeter_walls(),
            *_avatar_set_at(8, 8),
            sprites["socket_large"].clone().set_position(48, 48),
        ],
        grid_size=(64, 64),
        data={"step_budget": 50},
    ),
    Level(
        sprites=[
            *_perimeter_walls(),
            *[
                sprites["wall_block"].clone().set_position(32, ty * 4)
                for ty in (1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14)
            ],
            sprites["shove_block"].clone().set_position(32, 24),
            sprites["shove_block"].clone().set_position(32, 28),
            *_avatar_set_at(8, 28),
            sprites["socket_med"].clone().set_position(48, 24),
        ],
        grid_size=(64, 64),
        data={"step_budget": 60},
    ),
    Level(
        sprites=[
            *_perimeter_walls(),
            *[
                sprites["wall_block"].clone().set_position(32, ty * 4)
                for ty in (1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14)
            ],
            sprites["shove_block"].clone().set_position(32, 24),
            sprites["shove_block"].clone().set_position(32, 28),
            sprites["shove_block"].clone().set_position(32, 32),
            *[
                sprites["wall_block"].clone().set_position(44, ty * 4)
                for ty in (1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14)
            ],
            sprites["breakaway_wall"].clone().set_position(44, 24),
            sprites["breakaway_wall"].clone().set_position(44, 28),
            sprites["breakaway_wall"].clone().set_position(44, 32),
            *_avatar_set_at(8, 28),
            sprites["socket_large"].clone().set_position(48, 24),
        ],
        grid_size=(64, 64),
        data={"step_budget": 100},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 2
PADDING_COLOR = 4

AVATAR_DIM = {1: 4, 2: 8, 3: 12}
AVATAR_NAMES = {1: "avatar_small", 2: "avatar_med", 3: "avatar_large"}
HOP = 4
BURST_RADIUS = 12
GRID_SIDE = 64


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0) -> None:
        self.max_steps = max_steps
        self.current = max_steps

    def set_remaining(self, n: int) -> None:
        self.current = max(0, min(n, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.current / self.max_steps
        filled = round(64 * ratio)
        for x in range(64):
            frame[0, x] = 9 if x < filled else 0
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Zw91(NovaBaseGame):
    def __init__(self) -> None:
        self._step_hud = StepCounterHud(0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_hud],
        )
        self.size = 1
        self.overloaded = False
        super().__init__(
            game_id="zw91",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    # -- per-level state ------------------------------------------------
    def on_set_level(self, level: Level) -> None:
        self.size = 1
        self.overloaded = False
        budget = level.get_data("step_budget") or 50
        self._step_hud.max_steps = budget
        self._step_hud.set_remaining(budget)
        for av in level.get_sprites_by_tag("avatar"):
            if av.name == "avatar_small":
                av.set_interaction(InteractionMode.TANGIBLE)
            else:
                av.set_interaction(InteractionMode.REMOVED)
        for h in level.get_sprites_by_tag("overload"):
            h.set_interaction(InteractionMode.REMOVED)
        avs = level.get_sprites_by_name("avatar_small")
        if avs:
            ax, ay = avs[0].x, avs[0].y
            for h in level.get_sprites_by_tag("overload"):
                h.set_position(ax - 2, ay - 2)

    # -- helpers --------------------------------------------------------
    def _avatar_active(self) -> Sprite:
        return self.current_level.get_sprites_by_name(AVATAR_NAMES[self.size])[0]

    def _avatar_top_left(self) -> tuple[int, int]:
        a = self._avatar_active()
        return (a.x, a.y)

    def _move_all_avatars(self, x: int, y: int) -> None:
        for av in self.current_level.get_sprites_by_tag("avatar"):
            av.set_position(x, y)
        for h in self.current_level.get_sprites_by_tag("overload"):
            h.set_position(x - 2, y - 2)

    def _swap_active_size(self, new_size: int) -> None:
        for av in self.current_level.get_sprites_by_tag("avatar"):
            if av.name == AVATAR_NAMES[new_size]:
                av.set_interaction(InteractionMode.TANGIBLE)
            else:
                av.set_interaction(InteractionMode.REMOVED)
        self.size = new_size

    def _footprint_box(
        self, top_left: tuple[int, int], size: int
    ) -> tuple[int, int, int, int]:
        x, y = top_left
        d = AVATAR_DIM[size]
        return (x, y, x + d - 1, y + d - 1)

    @staticmethod
    def _box_intersect(
        a: tuple[int, int, int, int], b: tuple[int, int, int, int]
    ) -> bool:
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        return not (ax1 > bx2 or ax2 < bx1 or ay1 > by2 or ay2 < by1)

    def _footprint_overlaps_tag(
        self, top_left: tuple[int, int], size: int, tag: str
    ) -> bool:
        fp = self._footprint_box(top_left, size)
        for sp in self.current_level.get_sprites_by_tag(tag):
            if sp.interaction != InteractionMode.TANGIBLE:
                continue
            sp_box = (sp.x, sp.y, sp.x + sp.width - 1, sp.y + sp.height - 1)
            if self._box_intersect(fp, sp_box):
                return True
        return False

    def _shove_blocks_in_footprint(
        self, top_left: tuple[int, int], size: int
    ) -> list[Sprite]:
        fp = self._footprint_box(top_left, size)
        result: list[Sprite] = []
        for sp in self.current_level.get_sprites_by_tag("shove_block"):
            if sp.interaction != InteractionMode.TANGIBLE:
                continue
            sp_box = (sp.x, sp.y, sp.x + sp.width - 1, sp.y + sp.height - 1)
            if self._box_intersect(fp, sp_box):
                result.append(sp)
        return result

    def _block_dest_blocked(self, x: int, y: int, exclude: Sprite) -> bool:
        if x < 0 or y < 0 or x + 4 > GRID_SIDE or y + 4 > GRID_SIDE:
            return True
        dest_box = (x, y, x + 3, y + 3)
        for tag in ("wall", "shove_block"):
            for sp in self.current_level.get_sprites_by_tag(tag):
                if sp is exclude:
                    continue
                if sp.interaction != InteractionMode.TANGIBLE:
                    continue
                sp_box = (sp.x, sp.y, sp.x + sp.width - 1, sp.y + sp.height - 1)
                if self._box_intersect(dest_box, sp_box):
                    return True
        return False

    # -- mechanics ------------------------------------------------------
    def _try_move(self, dx: int, dy: int) -> None:
        cur = self._avatar_top_left()
        new_top = (cur[0] + dx, cur[1] + dy)
        d = AVATAR_DIM[self.size]
        if (
            new_top[0] < 0
            or new_top[1] < 0
            or new_top[0] + d > GRID_SIDE
            or new_top[1] + d > GRID_SIDE
        ):
            return
        if self._footprint_overlaps_tag(new_top, self.size, "wall"):
            return
        if self._footprint_overlaps_tag(new_top, self.size, "shove_block"):
            return
        self._move_all_avatars(new_top[0], new_top[1])

    def _try_inflate(self) -> None:
        if self.size >= 3:
            return
        new_size = self.size + 1
        cur = self._avatar_top_left()
        d = AVATAR_DIM[new_size]
        if (
            cur[0] < 0
            or cur[1] < 0
            or cur[0] + d > GRID_SIDE
            or cur[1] + d > GRID_SIDE
        ):
            return
        if self._footprint_overlaps_tag(cur, new_size, "wall"):
            return
        blocks = self._shove_blocks_in_footprint(cur, new_size)
        original_positions = [(b, b.x, b.y) for b in blocks]
        new_dim = AVATAR_DIM[new_size]
        avatar_cx = cur[0] + new_dim // 2
        avatar_cy = cur[1] + new_dim // 2
        for b in blocks:
            block_cx = b.x + 2
            block_cy = b.y + 2
            ddx = block_cx - avatar_cx
            ddy = block_cy - avatar_cy
            if abs(ddx) >= abs(ddy):
                push_dx, push_dy = (HOP if ddx >= 0 else -HOP), 0
            else:
                push_dx, push_dy = 0, (HOP if ddy >= 0 else -HOP)
            moved = False
            while True:
                next_x = b.x + push_dx
                next_y = b.y + push_dy
                if self._block_dest_blocked(next_x, next_y, exclude=b):
                    break
                b.set_position(next_x, next_y)
                moved = True
            if not moved:
                for s, ox, oy in original_positions:
                    s.set_position(ox, oy)
                return
        self._swap_active_size(new_size)

    def _enter_overload(self) -> None:
        self.overloaded = True
        ax, ay = self._avatar_top_left()
        for h in self.current_level.get_sprites_by_tag("overload"):
            h.set_position(ax - 2, ay - 2)
            h.set_interaction(InteractionMode.TANGIBLE)

    def _fire_burst(self) -> None:
        cur = self._avatar_top_left()
        xmin, ymin, xmax, ymax = self._footprint_box(cur, self.size)
        zone = (
            xmin - BURST_RADIUS,
            ymin - BURST_RADIUS,
            xmax + BURST_RADIUS,
            ymax + BURST_RADIUS,
        )
        for tag in ("shove_block", "breakaway"):
            for sp in self.current_level.get_sprites_by_tag(tag):
                if sp.interaction != InteractionMode.TANGIBLE:
                    continue
                sp_box = (sp.x, sp.y, sp.x + sp.width - 1, sp.y + sp.height - 1)
                if self._box_intersect(zone, sp_box):
                    sp.set_interaction(InteractionMode.REMOVED)
        self._swap_active_size(1)
        self.overloaded = False
        for h in self.current_level.get_sprites_by_tag("overload"):
            h.set_interaction(InteractionMode.REMOVED)

    # -- win / lose -----------------------------------------------------
    def _socket_size(self, sprite: Sprite) -> int:
        return {4: 1, 8: 2, 12: 3}[sprite.width]

    def _check_win(self) -> bool:
        sockets = self.current_level.get_sprites_by_tag("socket")
        if not sockets:
            return False
        cur = self._avatar_top_left()
        for sock in sockets:
            if sock.x != cur[0] or sock.y != cur[1]:
                return False
            if self.size != self._socket_size(sock):
                return False
        return True

    # -- step -----------------------------------------------------------
    def step(self) -> None:
        if self.action.id == GameAction.RESET:
            self.complete_action()
            return

        if self.action.id == GameAction.ACTION1:
            self._try_move(0, -HOP)
        elif self.action.id == GameAction.ACTION2:
            self._try_move(0, HOP)
        elif self.action.id == GameAction.ACTION3:
            self._try_move(-HOP, 0)
        elif self.action.id == GameAction.ACTION4:
            self._try_move(HOP, 0)
        elif self.action.id == GameAction.ACTION5:
            if self.size in (1, 2):
                self._try_inflate()
            elif self.size == 3 and not self.overloaded:
                self._enter_overload()
            elif self.size == 3 and self.overloaded:
                self._fire_burst()

        self._step_hud.set_remaining(self._step_hud.current - 1)

        if self._check_win():
            self.next_level()
            self.complete_action()
            return

        if self._step_hud.current <= 0:
            self.lose()
            self.complete_action()
            return

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 4), dtype=np.int16)
        state[0, 0] = self.size
        state[0, 1] = 1 if self.overloaded else 0
        state[0, 2] = self._step_hud.current
        state[0, 3] = self._current_level_index
        return state
