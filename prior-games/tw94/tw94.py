"""tw94."""

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


# Pixel patterns
PLAYER_PIXELS = [
    [4, 0, 0, 0, 4],
    [9, 9, 9, 9, 9],
    [9, 9, 9, 9, 9],
    [4, 9, 4, 9, 4],
    [4, 9, 9, 9, 4],
]
CRATE_PIXELS = [
    [4, 12, 12, 4],
    [12, 13, 13, 12],
    [12, 13, 13, 12],
    [4, 12, 12, 4],
]
TARGET_PIXELS = [
    [4, 11, 4],
    [11, 11, 11],
    [4, 11, 4],
]
WALL_PIXELS = [
    [4, 3, 3, 4],
    [3, 3, 3, 3],
    [3, 3, 3, 3],
    [4, 3, 3, 4],
]
PIP_PIXELS = [[10]]  # 1×1 light-blue indicator

BACKGROUND_COLOR = 1
PADDING_COLOR = 2


def _mk_player(x, y):
    s = Sprite(pixels=PLAYER_PIXELS, name="player", visible=True, collidable=True, tags=["player"])
    s.set_position(x, y)
    s.set_layer(3)
    return s


def _mk_crate(x, y, idx):
    s = Sprite(pixels=CRATE_PIXELS, name=f"crate_{idx}", visible=True, collidable=True, tags=["crate"])
    s.set_position(x, y)
    s.set_layer(2)
    return s


def _mk_target(x, y, idx):
    s = Sprite(
        pixels=TARGET_PIXELS, name=f"target_{idx}", visible=True, collidable=False,
        tags=["target"], interaction=InteractionMode.INTANGIBLE,
    )
    s.set_position(x, y)
    s.set_layer(1)
    return s


def _mk_wall(x, y, idx):
    s = Sprite(pixels=WALL_PIXELS, name=f"wall_{idx}", visible=True, collidable=True, tags=["wall"])
    s.set_position(x, y)
    return s


def _mk_pip(x, y, idx):
    s = Sprite(
        pixels=PIP_PIXELS, name=f"pip_{idx}", visible=True, collidable=False,
        tags=["pip"], interaction=InteractionMode.INTANGIBLE,
    )
    s.set_position(x, y)
    s.set_layer(0)
    return s


def _walls_row(y, x_lo, x_hi, prefix):
    return [_mk_wall(x, y, f"{prefix}_{x}") for x in range(x_lo, x_hi + 1)]


def _walls_col(x, y_lo, y_hi, prefix):
    return [_mk_wall(x, y, f"{prefix}_{y}") for y in range(y_lo, y_hi + 1)]


def _build_l1():
    """8x8: H wrap only. Player (3,4); crate (4,4); target (1,4); wall at (2,4) blocks direct west."""
    sprites = []
    sprites.extend(_walls_row(3, 0, 7, "l1_top"))
    sprites.extend(_walls_row(5, 0, 7, "l1_bot"))
    sprites.append(_mk_wall(2, 4, "l1_block"))
    sprites.append(_mk_player(3, 4))
    sprites.append(_mk_crate(4, 4, "l1a"))
    sprites.append(_mk_target(1, 4, "l1a"))
    # Pips at edges of row 4 (the only wrappable row)
    sprites.append(_mk_pip(0, 4, "l1_w"))
    sprites.append(_mk_pip(7, 4, "l1_e"))
    return Level(sprites=sprites, grid_size=(8, 8))


def _build_l2():
    """12x12: both axes wrap. Open room with 2 critical walls forcing each crate to use its-axis wrap."""
    sprites = []
    # Single wall blocking direct west push of crate_a
    sprites.append(_mk_wall(5, 4, "l2_a_blk"))
    # Single wall blocking direct north push of crate_b
    sprites.append(_mk_wall(4, 5, "l2_b_blk"))
    sprites.append(_mk_player(1, 1))
    # Crate_a delivery: 10→9→...→6→(5)wall blocks. Use east-via-wrap: 10→11→0→1→2=target.
    sprites.append(_mk_crate(10, 4, "l2a"))
    sprites.append(_mk_target(2, 4, "l2a"))
    # Crate_b delivery: 10→9→8→7→6→(5)wall blocks. Use south-via-wrap: 10→11→0→1→2=target.
    sprites.append(_mk_crate(4, 10, "l2b"))
    sprites.append(_mk_target(4, 2, "l2b"))
    # Pips at all 4 edges (both axes wrap at L2)
    for y in range(12):
        sprites.append(_mk_pip(0, y, f"l2pip_w_{y}"))
        sprites.append(_mk_pip(11, y, f"l2pip_e_{y}"))
    for x in range(12):
        sprites.append(_mk_pip(x, 0, f"l2pip_n_{x}"))
        sprites.append(_mk_pip(x, 11, f"l2pip_s_{x}"))
    return Level(sprites=sprites, grid_size=(12, 12))


def _build_l3():
    """14x14: row-parity wrap. Even rows wrap H; even cols wrap V. Same crates as L2 (both on even row/col)."""
    sprites = []
    sprites.append(_mk_wall(5, 4, "l3_a_blk"))
    sprites.append(_mk_crate(10, 4, "l3a"))
    sprites.append(_mk_target(2, 4, "l3a"))
    sprites.append(_mk_wall(4, 5, "l3_b_blk"))
    sprites.append(_mk_crate(4, 10, "l3b"))
    sprites.append(_mk_target(4, 2, "l3b"))
    sprites.append(_mk_player(1, 1))
    # Pips only at even-row/even-col edges (visual cue for M3)
    for y in range(0, 14, 2):
        sprites.append(_mk_pip(0, y, f"l3pip_w_{y}"))
        sprites.append(_mk_pip(13, y, f"l3pip_e_{y}"))
    for x in range(0, 14, 2):
        sprites.append(_mk_pip(x, 0, f"l3pip_n_{x}"))
        sprites.append(_mk_pip(x, 13, f"l3pip_s_{x}"))
    return Level(sprites=sprites, grid_size=(14, 14))


levels = [_build_l1(), _build_l2(), _build_l3()]


class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps=25):
        super().__init__()
        self._max = max_steps
        self._used = 0

    def set_state(self, used, max_steps):
        self._used = used
        self._max = max_steps

    def render_interface(self, frame):
        if self._max <= 0:
            return frame
        bar_y, x_lo, x_hi = 63, 16, 48
        remaining = max(0, self._max - self._used)
        width = x_hi - x_lo
        filled = int(round(width * (remaining / self._max)))
        for i, x in enumerate(range(x_lo, x_hi)):
            frame[bar_y, x] = 9 if i < filled else 3
        return frame


class Tw94(NovaBaseGame):
    def __init__(self):
        self._step_hud = StepCounterHud(25)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_hud],
        )
        super().__init__(
            game_id="tw94",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )
        self._steps_used = 0
        self._max_steps = 25

    def on_set_level(self, level):
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        idx = getattr(self, "_current_level_index", 0)
        self._max_steps = [25, 80, 150][idx]
        self._steps_used = 0
        self._step_hud.set_state(self._steps_used, self._max_steps)

    def _wrap_enabled_h(self, y):
        """Is horizontal wrap enabled at row y for the current level?"""
        idx = getattr(self, "_current_level_index", 0)
        if idx == 0:
            return True   # L1: H wrap always
        if idx == 1:
            return True   # L2: H wrap always
        # L3: only on even rows
        return y % 2 == 0

    def _wrap_enabled_v(self, x):
        """Is vertical wrap enabled at col x for the current level?"""
        idx = getattr(self, "_current_level_index", 0)
        if idx == 0:
            return False  # L1: no V wrap
        if idx == 1:
            return True
        # L3: only on even cols
        return x % 2 == 0

    def _wrap_pos(self, x, y, dx, dy):
        """Compute new position with wrap rules. Returns (nx, ny) or None if blocked."""
        gw, gh = self.current_level.grid_size or (64, 64)
        nx = x + dx
        ny = y + dy
        if dx != 0:  # horizontal motion
            if nx < 0:
                if self._wrap_enabled_h(y):
                    nx = gw - 1
                else:
                    return None
            elif nx >= gw:
                if self._wrap_enabled_h(y):
                    nx = 0
                else:
                    return None
        if dy != 0:  # vertical motion
            if ny < 0:
                if self._wrap_enabled_v(x):
                    ny = gh - 1
                else:
                    return None
            elif ny >= gh:
                if self._wrap_enabled_v(x):
                    ny = 0
                else:
                    return None
        return (nx, ny)

    def _wall_at(self, x, y):
        for w in self.current_level.get_sprites_by_tag("wall"):
            if w.x == x and w.y == y:
                return True
        return False

    def _crate_at(self, x, y):
        for c in self.current_level.get_sprites_by_tag("crate"):
            if c.x == x and c.y == y:
                return c
        return None

    def _player(self):
        return self.current_level.get_sprites_by_tag("player")[0]

    def _direction(self, action_id):
        if action_id == GameAction.ACTION1:
            return (0, -1)
        if action_id == GameAction.ACTION2:
            return (0, 1)
        if action_id == GameAction.ACTION3:
            return (-1, 0)
        if action_id == GameAction.ACTION4:
            return (1, 0)
        return (0, 0)

    def _attempt_move(self, dx, dy, actor):
        new_pos = self._wrap_pos(actor.x, actor.y, dx, dy)
        if new_pos is None:
            return False
        nx, ny = new_pos
        if self._wall_at(nx, ny):
            return False
        crate = self._crate_at(nx, ny)
        if crate is None:
            actor.set_position(nx, ny)
            return True
        # Push: compute crate's new position
        crate_new = self._wrap_pos(crate.x, crate.y, dx, dy)
        if crate_new is None:
            return False
        cx, cy = crate_new
        if self._wall_at(cx, cy):
            return False
        if self._crate_at(cx, cy) is not None:
            return False
        crate.set_position(cx, cy)
        actor.set_position(nx, ny)
        return True

    def _check_win(self):
        crate_pos = {(c.x, c.y) for c in self.current_level.get_sprites_by_tag("crate")}
        target_pos = {(t.x, t.y) for t in self.current_level.get_sprites_by_tag("target")}
        return target_pos.issubset(crate_pos)

    def step(self):
        if self._steps_used >= self._max_steps:
            self.lose()
            self.complete_action()
            return
        if self.action.id in (GameAction.ACTION1, GameAction.ACTION2,
                              GameAction.ACTION3, GameAction.ACTION4):
            dx, dy = self._direction(self.action.id)
            actor = self._player()
            self._attempt_move(dx, dy, actor)
            self._steps_used += 1
            self._step_hud.set_state(self._steps_used, self._max_steps)
            if self._check_win():
                self.next_level()
                self.complete_action()
                return
        self.complete_action()

    def _get_hidden_state(self):
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
