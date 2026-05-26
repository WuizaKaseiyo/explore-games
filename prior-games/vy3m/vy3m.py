"""vy3m."""

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
# Pixel patterns
# ---------------------------------------------------------------------
PUSHER_PIXELS = [  # 5×5 blue body
    [4, 0, 0, 0, 4],
    [9, 9, 9, 9, 9],
    [9, 9, 9, 9, 9],
    [4, 9, 4, 9, 4],
    [4, 9, 9, 9, 4],
]
PULLER_PIXELS = [  # 5×5 green body
    [4, 0, 0, 0, 4],
    [14, 14, 14, 14, 14],
    [14, 14, 14, 14, 14],
    [4, 14, 4, 14, 4],
    [4, 14, 14, 14, 4],
]
STOMPER_PIXELS = [  # 5×5 orange body
    [4, 0, 0, 0, 4],
    [12, 12, 12, 12, 12],
    [12, 12, 12, 12, 12],
    [4, 12, 4, 12, 4],
    [4, 12, 12, 12, 4],
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


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 1
PADDING_COLOR = 2

CLASS_COLORS = {"pusher": 9, "puller": 14, "stomper": 12}


# ---------------------------------------------------------------------
# Sprite factories
# ---------------------------------------------------------------------
def _mk_pusher(x, y):
    s = Sprite(pixels=PUSHER_PIXELS, name="pusher", visible=True, collidable=True, tags=["pusher", "actor"])
    s.set_position(x, y)
    s.set_layer(3)
    return s


def _mk_puller(x, y):
    s = Sprite(pixels=PULLER_PIXELS, name="puller", visible=True, collidable=True, tags=["puller", "actor"])
    s.set_position(x, y)
    s.set_layer(3)
    return s


def _mk_stomper(x, y):
    s = Sprite(pixels=STOMPER_PIXELS, name="stomper", visible=True, collidable=True, tags=["stomper", "actor"])
    s.set_position(x, y)
    s.set_layer(3)
    return s


def _mk_crate(x, y, idx):
    s = Sprite(pixels=CRATE_PIXELS, name=f"crate_{idx}", visible=True, collidable=True, tags=["crate", "pushable"])
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


def _walls_row(y, x_lo, x_hi, prefix):
    return [_mk_wall(x, y, f"{prefix}_{x}") for x in range(x_lo, x_hi + 1)]


# ---------------------------------------------------------------------
# Levels
# ---------------------------------------------------------------------
def _build_l1():
    sprites = []
    sprites.extend(_walls_row(3, 2, 8, "l1_top"))
    sprites.extend(_walls_row(5, 2, 8, "l1_bot"))
    sprites.append(_mk_pusher(2, 4))
    sprites.append(_mk_crate(5, 4, "l1a"))
    sprites.append(_mk_target(8, 4, "l1a"))
    return Level(sprites=sprites, grid_size=(10, 10))


def _build_l2():
    sprites = []
    # Push lane row 2
    sprites.extend(_walls_row(1, 1, 10, "l2_pt"))
    sprites.extend(_walls_row(3, 1, 10, "l2_pb"))
    sprites.append(_mk_pusher(1, 2))
    sprites.append(_mk_crate(4, 2, "l2a"))
    sprites.append(_mk_target(8, 2, "l2a"))
    # Pull lane row 7
    sprites.extend(_walls_row(6, 1, 10, "l2_lt"))
    sprites.extend(_walls_row(8, 1, 10, "l2_lb"))
    sprites.append(_mk_puller(4, 7))
    sprites.append(_mk_crate(5, 7, "l2b"))
    sprites.append(_mk_target(3, 7, "l2b"))
    return Level(sprites=sprites, grid_size=(12, 12))


def _build_l3():
    sprites = []
    # Push lane row 2
    sprites.extend(_walls_row(1, 1, 12, "l3_pt"))
    sprites.extend(_walls_row(3, 1, 12, "l3_pb"))
    sprites.append(_mk_pusher(1, 2))
    sprites.append(_mk_crate(4, 2, "l3a"))
    sprites.append(_mk_target(8, 2, "l3a"))
    # Pull lane row 7
    sprites.extend(_walls_row(6, 1, 12, "l3_lt"))
    sprites.extend(_walls_row(8, 1, 12, "l3_lb"))
    sprites.append(_mk_puller(4, 7))
    sprites.append(_mk_crate(5, 7, "l3b"))
    sprites.append(_mk_target(3, 7, "l3b"))
    # Chain lane row 12
    sprites.extend(_walls_row(11, 1, 12, "l3_ct"))
    sprites.extend(_walls_row(13, 1, 12, "l3_cb"))
    sprites.append(_mk_stomper(1, 12))
    sprites.append(_mk_crate(3, 12, "l3c1"))
    sprites.append(_mk_crate(4, 12, "l3c2"))
    sprites.append(_mk_target(7, 12, "l3c"))
    return Level(sprites=sprites, grid_size=(14, 14))


levels = [_build_l1(), _build_l2(), _build_l3()]


# ---------------------------------------------------------------------
# HUD widgets
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps=30):
        super().__init__()
        self._max = max_steps
        self._used = 0

    def set_state(self, used, max_steps):
        self._used = used
        self._max = max_steps

    def render_interface(self, frame):
        bar_y, x_lo, x_hi = 63, 16, 48
        if self._max <= 0:
            return frame
        remaining = max(0, self._max - self._used)
        width = x_hi - x_lo
        filled = int(round(width * (remaining / self._max)))
        for i, x in enumerate(range(x_lo, x_hi)):
            frame[bar_y, x] = 9 if i < filled else 3
        return frame


class ActiveClassHud(RenderableUserDisplay):
    def __init__(self):
        super().__init__()
        self._color = 9  # default Pusher blue

    def set_state(self, active_class):
        self._color = CLASS_COLORS.get(active_class, 9)

    def render_interface(self, frame):
        # 4×4 badge top-left rows 0-3, cols 0-3
        for y in range(0, 4):
            for x in range(0, 4):
                frame[y, x] = self._color
        return frame


# ---------------------------------------------------------------------
# Game class
# ---------------------------------------------------------------------
class Vy3m(NovaBaseGame):
    def __init__(self):
        self._step_hud = StepCounterHud(30)
        self._class_hud = ActiveClassHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._class_hud, self._step_hud],
        )
        super().__init__(
            game_id="vy3m",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )
        self._active_class = "pusher"
        self._steps_used = 0
        self._max_steps = 30

    def on_set_level(self, level):
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        idx = getattr(self, "_current_level_index", 0)
        if idx == 0:
            self._max_steps = 30
        elif idx == 1:
            self._max_steps = 50
        else:
            self._max_steps = 80
        self._steps_used = 0
        self._active_class = "pusher"
        self._step_hud.set_state(self._steps_used, self._max_steps)
        self._class_hud.set_state(self._active_class)

    def _classes_in_level(self):
        idx = getattr(self, "_current_level_index", 0)
        if idx == 0:
            return ["pusher"]
        elif idx == 1:
            return ["pusher", "puller"]
        else:
            return ["pusher", "puller", "stomper"]

    def _active_actor(self):
        actors = self.current_level.get_sprites_by_tag(self._active_class)
        if not actors:
            return None
        return actors[0]

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

    def _wall_at(self, x, y):
        gw, gh = self.current_level.grid_size or (64, 64)
        if x < 0 or x >= gw or y < 0 or y >= gh:
            return True
        for w in self.current_level.get_sprites_by_tag("wall"):
            if w.x == x and w.y == y:
                return True
        return False

    def _crate_at(self, x, y):
        for c in self.current_level.get_sprites_by_tag("crate"):
            if c.x == x and c.y == y:
                return c
        return None

    def _actor_at(self, x, y):
        for a in self.current_level.get_sprites_by_tag("actor"):
            if a.x == x and a.y == y:
                return a
        return None

    def _attempt_pusher_move(self, dx, dy, actor):
        tx, ty = actor.x + dx, actor.y + dy
        if self._wall_at(tx, ty):
            return False
        if self._actor_at(tx, ty):
            return False
        crate = self._crate_at(tx, ty)
        if crate is None:
            actor.move(dx, dy)
            return True
        # Push: dest cell beyond crate must be empty
        cx, cy = tx + dx, ty + dy
        if self._wall_at(cx, cy):
            return False
        if self._crate_at(cx, cy) is not None:
            return False  # pusher cannot chain
        if self._actor_at(cx, cy):
            return False
        crate.move(dx, dy)
        actor.move(dx, dy)
        return True

    def _attempt_puller_move(self, dx, dy, actor):
        tx, ty = actor.x + dx, actor.y + dy
        if self._wall_at(tx, ty):
            return False
        if self._actor_at(tx, ty):
            return False
        if self._crate_at(tx, ty) is not None:
            # Puller blocked by crate in direction of motion
            return False
        # Crate behind (opposite direction): if exists, drag it
        bx, by = actor.x - dx, actor.y - dy
        crate = self._crate_at(bx, by)
        actor.move(dx, dy)
        if crate is not None:
            crate.move(dx, dy)
        return True

    def _attempt_stomper_move(self, dx, dy, actor):
        tx, ty = actor.x + dx, actor.y + dy
        if self._wall_at(tx, ty):
            return False
        if self._actor_at(tx, ty):
            return False
        crate = self._crate_at(tx, ty)
        if crate is None:
            actor.move(dx, dy)
            return True
        cx, cy = tx + dx, ty + dy
        # Stomper: try chain push of 2
        crate2 = self._crate_at(cx, cy)
        if crate2 is not None:
            # Cell beyond crate2
            ex, ey = cx + dx, cy + dy
            if self._wall_at(ex, ey):
                return False
            if self._crate_at(ex, ey) is not None:
                return False
            if self._actor_at(ex, ey):
                return False
            # Move crate2 first to avoid overlap
            crate2.move(dx, dy)
            crate.move(dx, dy)
            actor.move(dx, dy)
            return True
        # Single push (cell beyond crate is not a crate)
        if self._wall_at(cx, cy):
            return False
        if self._actor_at(cx, cy):
            return False
        crate.move(dx, dy)
        actor.move(dx, dy)
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

        if self.action.id == GameAction.ACTION5:
            classes = self._classes_in_level()
            i = classes.index(self._active_class)
            self._active_class = classes[(i + 1) % len(classes)]
            self._class_hud.set_state(self._active_class)
            self._steps_used += 1
            self._step_hud.set_state(self._steps_used, self._max_steps)
            self.complete_action()
            return

        if self.action.id in (GameAction.ACTION1, GameAction.ACTION2,
                              GameAction.ACTION3, GameAction.ACTION4):
            dx, dy = self._direction(self.action.id)
            actor = self._active_actor()
            if actor is None:
                self.complete_action()
                return
            if self._active_class == "pusher":
                self._attempt_pusher_move(dx, dy, actor)
            elif self._active_class == "puller":
                self._attempt_puller_move(dx, dy, actor)
            elif self._active_class == "stomper":
                self._attempt_stomper_move(dx, dy, actor)
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
