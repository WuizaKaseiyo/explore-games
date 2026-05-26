"""NovaPlay generated game tk6n."""

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

# Avatar: 5x5 with palette-9 (blue) body, palette-11 (yellow) rim,
# palette-4 (off-black) eye-dot. The eye-dot is on the right edge by
# default (rotation=0 means facing right). Use sprite.set_rotation
# to rotate the whole sprite to indicate facing direction.
sprites = {
    "avatar": Sprite(
        pixels=[
            [11, 11, 11, 11, 11],
            [11,  9,  9,  9, 11],
            [11,  9,  9,  9,  4],
            [11,  9,  9,  9, 11],
            [11, 11, 11, 11, 11],
        ],
        name="avatar",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=2,
    ),
    "boomerang": Sprite(
        pixels=[
            [12, 12, -1],
            [12,  8, 12],
            [-1, 12, 12],
        ],
        name="boomerang",
        visible=True,
        collidable=False,
        tags=["boomerang"],
        layer=3,
    ),
    "target_dim": Sprite(
        pixels=[
            [-1,  6,  6, -1],
            [ 6,  7,  7,  6],
            [ 6,  7,  7,  6],
            [-1,  6,  6, -1],
        ],
        name="target_dim",
        visible=True,
        collidable=False,
        tags=["target"],
        layer=0,
    ),
    "target_lit": Sprite(
        pixels=[
            [11, 11, 11, 11],
            [11, 12, 12, 11],
            [11, 12, 12, 11],
            [11, 11, 11, 11],
        ],
        name="target_lit",
        visible=True,
        collidable=False,
        tags=["target", "lit"],
        layer=0,
    ),
    "wall_tall": Sprite(
        pixels=[
            [ 5,  5,  5,  5],
            [ 5,  4,  4,  5],
            [ 5,  4,  4,  5],
            [ 5,  5,  5,  5],
        ],
        name="wall_tall",
        visible=True,
        collidable=True,
        tags=["wall", "wall_tall"],
        layer=1,
    ),
    "wall_short": Sprite(
        pixels=[
            [ 4,  3,  4,  3],
            [ 3,  2,  3,  2],
            [ 4,  3,  4,  3],
            [ 3,  2,  3,  2],
        ],
        name="wall_short",
        visible=True,
        collidable=True,
        tags=["wall", "wall_short"],
        layer=1,
    ),
    "guard": Sprite(
        pixels=[
            [ 4, 13, 13,  4],
            [13,  8, 13, 13],
            [13, 13,  8, 13],
            [ 4, 13, 13,  4],
        ],
        name="guard",
        visible=True,
        collidable=True,
        tags=["guard"],
        layer=2,
    ),
    "guard_frozen": Sprite(
        pixels=[
            [ 4,  3,  3,  4],
            [ 3,  2,  3,  3],
            [ 3,  3,  2,  3],
            [ 4,  3,  3,  4],
        ],
        name="guard_frozen",
        visible=True,
        collidable=True,
        tags=["guard", "frozen"],
        layer=2,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

def _build_horizontal_wall(x_start: int, x_end: int, y: int, sprite_key: str) -> list:
    """Place 4x4 wall sprites along row y from x_start to x_end (inclusive)."""
    placed = []
    x = x_start
    while x <= x_end - 3:
        placed.append(sprites[sprite_key].clone().set_position(x, y))
        x += 4
    return placed


def _build_vertical_wall(x: int, y_start: int, y_end: int, sprite_key: str) -> list:
    """Place 4x4 wall sprites along column x from y_start to y_end (inclusive)."""
    placed = []
    y = y_start
    while y <= y_end - 3:
        placed.append(sprites[sprite_key].clone().set_position(x, y))
        y += 4
    return placed


# --- Level 1: open arena, single target offset on both axes ---
_l1_sprites = [
    sprites["target_dim"].clone().set_position(32, 22),
    sprites["avatar"].clone().set_position(20, 36),
    sprites["boomerang"].clone().set_position(20, 36),
]

# --- Level 2: sealed corridor with wall_short barrier between
#     avatar and target.
_l2_sprites = []
_l2_sprites += _build_horizontal_wall(4, 56, 24, "wall_tall")
_l2_sprites += _build_horizontal_wall(4, 56, 40, "wall_tall")
_l2_sprites += _build_vertical_wall(56, 24, 43, "wall_tall")
_l2_sprites += _build_vertical_wall(0, 24, 43, "wall_tall")
_l2_sprites += _build_vertical_wall(22, 24, 39, "wall_short")
_l2_sprites.append(sprites["target_dim"].clone().set_position(28, 32))
_l2_sprites.append(sprites["avatar"].clone().set_position(10, 32))
_l2_sprites.append(sprites["boomerang"].clone().set_position(10, 32))

# --- Level 3: corridor + wall_short + guard.
_l3_sprites = []
_l3_sprites += _build_horizontal_wall(4, 56, 24, "wall_tall")
_l3_sprites += _build_horizontal_wall(4, 56, 40, "wall_tall")
_l3_sprites += _build_vertical_wall(56, 24, 43, "wall_tall")
_l3_sprites += _build_vertical_wall(0, 24, 43, "wall_tall")
_l3_sprites += _build_vertical_wall(28, 24, 39, "wall_short")
_l3_sprites.append(sprites["target_dim"].clone().set_position(40, 32))
_l3_sprites.append(sprites["avatar"].clone().set_position(6, 32))
_l3_sprites.append(sprites["boomerang"].clone().set_position(6, 32))
_l3_sprites.append(sprites["guard"].clone().set_position(20, 32))

levels = [
    Level(
        sprites=_l1_sprites,
        grid_size=(64, 64),
        data={
            "throw_range": 14,
            "step_budget": 50,
            "guard_min_x": -1,
            "guard_max_x": -1,
        },
    ),
    Level(
        sprites=_l2_sprites,
        grid_size=(64, 64),
        data={
            "throw_range": 18,
            "step_budget": 60,
            "guard_min_x": -1,
            "guard_max_x": -1,
        },
    ),
    Level(
        sprites=_l3_sprites,
        grid_size=(64, 64),
        data={
            "throw_range": 36,
            "step_budget": 100,
            "guard_min_x": 12,
            "guard_max_x": 24,
            "freeze_duration": 4,
        },
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 1
PADDING_COLOR = 4
GRID_W = 64
GRID_H = 64

# Direction tuples (dx, dy). Note: positive y is downward in the grid.
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)

# Avatar rotation per facing direction (degrees clockwise from "right").
_ROTATION_FOR_FACING = {
    DIR_RIGHT: 0,
    DIR_DOWN: 90,
    DIR_LEFT: 180,
    DIR_UP: 270,
}


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    """Bottom-row bar that depletes one cell per remaining step."""

    def __init__(self) -> None:
        self._max = 1
        self._current = 0

    def configure(self, max_steps: int) -> None:
        self._max = max(1, max_steps)
        self._current = max_steps

    def set_current(self, current: int) -> None:
        self._current = max(0, min(current, self._max))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        bar_row = frame.shape[0] - 1
        width = frame.shape[1]
        ratio = self._current / self._max if self._max > 0 else 0.0
        filled = int(round(width * ratio))
        for x in range(width):
            frame[bar_row, x] = 11 if x < filled else 4
        return frame


class BoomerangPhaseIndicator(RenderableUserDisplay):
    """Top-left 3-cell indicator showing boomerang phase."""

    PALETTE_FOR_PHASE = {
        "held": 12,
        "outbound": 8,
        "returning": 8,
        "dropped": 3,
    }

    def __init__(self) -> None:
        self._phase = "held"

    def set_phase(self, phase: str) -> None:
        self._phase = phase

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        colour = self.PALETTE_FOR_PHASE.get(self._phase, 4)
        for x in range(3):
            frame[0, x] = colour
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------

class Tk6n(NovaBaseGame):

    def __init__(self) -> None:
        self._step_hud = StepCounterHud()
        self._phase_hud = BoomerangPhaseIndicator()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_hud, self._phase_hud],
        )
        # Per-game state placeholders; populated in on_set_level.
        self.avatar = None
        self.boomerang = None
        self.guard = None
        self.facing = DIR_RIGHT
        self.boomerang_phase = "held"
        self.boomerang_throw_dir = None
        self.boomerang_outbound_remaining = 0
        self.boomerang_pos = None
        self.lit_targets = set()
        self.steps_remaining = 0
        self.guard_patrol_dir = None
        self.guard_min_x = -1
        self.guard_max_x = -1
        self.guard_freeze_remaining = 0
        self.freeze_duration = 0
        self.throw_range = 0

        super().__init__(
            game_id="tk6n",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    # -------------------------------------------------------------
    # Level setup
    # -------------------------------------------------------------

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (GRID_W, GRID_H)
        self.camera.width = gw
        self.camera.height = gh

        self.avatar = level.get_sprites_by_name("avatar")[0]
        self.boomerang = level.get_sprites_by_name("boomerang")[0]
        guard_list = level.get_sprites_by_name("guard")
        self.guard = guard_list[0] if guard_list else None

        self.facing = DIR_RIGHT
        self.avatar.set_rotation(_ROTATION_FOR_FACING[self.facing])

        self.boomerang_phase = "held"
        self.boomerang_throw_dir = None
        self.boomerang_outbound_remaining = 0
        self.boomerang_pos = None
        self._hide_boomerang()

        self.lit_targets = set()

        self.throw_range = int(level.get_data("throw_range") or 8)
        self.steps_remaining = int(level.get_data("step_budget") or 30)
        self._step_hud.configure(self.steps_remaining)
        self._phase_hud.set_phase(self.boomerang_phase)

        if self.guard is not None:
            self.guard_min_x = int(level.get_data("guard_min_x") or 0)
            self.guard_max_x = int(level.get_data("guard_max_x") or 0)
            self.guard_patrol_dir = DIR_RIGHT
            self.guard_freeze_remaining = 0
            self.freeze_duration = int(level.get_data("freeze_duration") or 4)
        else:
            self.guard_min_x = -1
            self.guard_max_x = -1
            self.guard_patrol_dir = None
            self.guard_freeze_remaining = 0
            self.freeze_duration = 0

    # -------------------------------------------------------------
    # Avatar / boomerang helpers
    # -------------------------------------------------------------

    def _hide_boomerang(self) -> None:
        self.boomerang.set_interaction(InteractionMode.REMOVED)

    def _show_boomerang_at(self, x: int, y: int) -> None:
        self.boomerang.set_position(x, y)
        self.boomerang.set_interaction(InteractionMode.INTANGIBLE)

    def _avatar_cell(self) -> tuple:
        return (self.avatar.x, self.avatar.y)

    def _is_walk_blocked(self, x: int, y: int) -> bool:
        # Avatar's 5x5 footprint at (x, y) extends to (x+4, y+4).
        if x < 0 or y < 0:
            return True
        if x + self.avatar.width > GRID_W or y + self.avatar.height > GRID_H:
            return True
        for sprite in self.current_level.get_sprites():
            if sprite is self.avatar or sprite is self.boomerang:
                continue
            if sprite.interaction != InteractionMode.TANGIBLE:
                continue
            if not sprite.is_collidable:
                continue
            if self._rects_overlap(
                x, y, self.avatar.width, self.avatar.height,
                sprite.x, sprite.y, sprite.width, sprite.height,
            ):
                return True
        return False

    @staticmethod
    def _rects_overlap(ax: int, ay: int, aw: int, ah: int,
                       bx: int, by: int, bw: int, bh: int) -> bool:
        return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah

    def _try_walk_avatar(self, dx: int, dy: int) -> None:
        new_x = self.avatar.x + dx
        new_y = self.avatar.y + dy
        if not self._is_walk_blocked(new_x, new_y):
            self.avatar.set_position(new_x, new_y)

    # -------------------------------------------------------------
    # Boomerang flight
    # -------------------------------------------------------------

    def _tall_wall_at_cell(self, x: int, y: int) -> bool:
        for sprite in self.current_level.get_sprites_by_tag("wall_tall"):
            if sprite.interaction != InteractionMode.TANGIBLE:
                continue
            if (sprite.x <= x < sprite.x + sprite.width
                    and sprite.y <= y < sprite.y + sprite.height):
                return True
        return False

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < GRID_W and 0 <= y < GRID_H

    def _light_targets_overlapping(self, bx: int, by: int) -> None:
        # Boomerang sprite is 3x3 anchored at (bx, by).
        for target in self.current_level.get_sprites_by_tag("target"):
            if "lit" in (target.tags or []):
                continue
            if self._rects_overlap(
                bx, by, self.boomerang.width, self.boomerang.height,
                target.x, target.y, target.width, target.height,
            ):
                # Swap target_dim → target_lit by replacing the sprite.
                lit = sprites["target_lit"].clone().set_position(
                    target.x, target.y
                )
                self.current_level.add_sprite(lit)
                self.current_level.remove_sprite(target)
                self.lit_targets.add(lit)

    def _boomerang_overlaps_avatar(self) -> bool:
        if self.boomerang_pos is None:
            return False
        bx, by = self.boomerang_pos
        return self._rects_overlap(
            bx, by, self.boomerang.width, self.boomerang.height,
            self.avatar.x, self.avatar.y,
            self.avatar.width, self.avatar.height,
        )

    def _boomerang_overlaps_guard(self) -> bool:
        if self.boomerang_pos is None or self.guard is None:
            return False
        bx, by = self.boomerang_pos
        return self._rects_overlap(
            bx, by, self.boomerang.width, self.boomerang.height,
            self.guard.x, self.guard.y,
            self.guard.width, self.guard.height,
        )

    def _catch_boomerang(self) -> None:
        self.boomerang_phase = "held"
        self.boomerang_throw_dir = None
        self.boomerang_outbound_remaining = 0
        self.boomerang_pos = None
        self._hide_boomerang()
        self._phase_hud.set_phase("held")

    def _drop_boomerang_at(self, x: int, y: int) -> None:
        self.boomerang_phase = "dropped"
        self.boomerang_throw_dir = None
        self.boomerang_outbound_remaining = 0
        self.boomerang_pos = (x, y)
        self._show_boomerang_at(x, y)
        self._phase_hud.set_phase("dropped")

    def _launch_boomerang(self) -> None:
        # Launch from avatar's centre cell (anchor + 1, +1).
        ax, ay = self.avatar.x + 1, self.avatar.y + 1
        self.boomerang_throw_dir = self.facing
        self.boomerang_outbound_remaining = self.throw_range
        self.boomerang_phase = "outbound"
        self.boomerang_pos = (ax, ay)
        self._show_boomerang_at(ax, ay)
        self._phase_hud.set_phase("outbound")
        # Apply one tick of advance immediately.
        self._advance_boomerang_one_tick()

    def _advance_boomerang_one_tick(self) -> None:
        if self.boomerang_pos is None:
            return
        bx, by = self.boomerang_pos
        if self.boomerang_phase == "outbound":
            ddx, ddy = self.boomerang_throw_dir
            new_x, new_y = bx + ddx, by + ddy
            if (not self._in_bounds(new_x, new_y)
                    or self._tall_wall_at_cell(new_x, new_y)):
                # Hit wall or boundary; bounce to returning at current cell.
                self.boomerang_phase = "returning"
                self._phase_hud.set_phase("returning")
                return
            self.boomerang_pos = (new_x, new_y)
            self._show_boomerang_at(new_x, new_y)
            self._light_targets_overlapping(new_x, new_y)
            self.boomerang_outbound_remaining -= 1
            if self.boomerang_outbound_remaining <= 0:
                self.boomerang_phase = "returning"
                self._phase_hud.set_phase("returning")
        elif self.boomerang_phase == "returning":
            ax = self.avatar.x + 1
            ay = self.avatar.y + 1
            ddx = ax - bx
            ddy = ay - by
            if ddx == 0 and ddy == 0:
                self._catch_boomerang()
                return
            if abs(ddx) >= abs(ddy):
                step = (1 if ddx > 0 else -1, 0)
            else:
                step = (0, 1 if ddy > 0 else -1)
            new_x, new_y = bx + step[0], by + step[1]
            if (not self._in_bounds(new_x, new_y)
                    or self._tall_wall_at_cell(new_x, new_y)):
                # Boomerang dies at current cell.
                self._drop_boomerang_at(bx, by)
                return
            self.boomerang_pos = (new_x, new_y)
            self._show_boomerang_at(new_x, new_y)
            self._light_targets_overlapping(new_x, new_y)
            if self._boomerang_overlaps_avatar():
                self._catch_boomerang()

    # -------------------------------------------------------------
    # Guard patrol
    # -------------------------------------------------------------

    def _avatar_overlaps_guard(self) -> bool:
        if self.guard is None:
            return False
        return self._rects_overlap(
            self.avatar.x, self.avatar.y,
            self.avatar.width, self.avatar.height,
            self.guard.x, self.guard.y,
            self.guard.width, self.guard.height,
        )

    def _swap_guard_to_frozen(self) -> None:
        if self.guard is None or "frozen" in (self.guard.tags or []):
            return
        gx, gy = self.guard.x, self.guard.y
        frozen = sprites["guard_frozen"].clone().set_position(gx, gy)
        self.current_level.add_sprite(frozen)
        self.current_level.remove_sprite(self.guard)
        self.guard = frozen

    def _swap_guard_to_active(self) -> None:
        if self.guard is None or "frozen" not in (self.guard.tags or []):
            return
        gx, gy = self.guard.x, self.guard.y
        active = sprites["guard"].clone().set_position(gx, gy)
        self.current_level.add_sprite(active)
        self.current_level.remove_sprite(self.guard)
        self.guard = active

    def _advance_guard_one_tick(self) -> None:
        if self.guard is None or self.guard_patrol_dir is None:
            return
        if self.guard_freeze_remaining > 0:
            self.guard_freeze_remaining -= 1
            if self.guard_freeze_remaining == 0:
                self._swap_guard_to_active()
            return
        gx = self.guard.x
        ddx, _ = self.guard_patrol_dir
        new_x = gx + ddx
        if new_x < self.guard_min_x:
            self.guard_patrol_dir = DIR_RIGHT
            new_x = gx + 1
        elif new_x > self.guard_max_x:
            self.guard_patrol_dir = DIR_LEFT
            new_x = gx - 1
        self.guard.set_position(new_x, self.guard.y)

    def _trigger_guard_freeze(self) -> None:
        if self.guard is None or self.freeze_duration <= 0:
            return
        if self.guard_freeze_remaining > 0:
            return
        self.guard_freeze_remaining = self.freeze_duration
        self._swap_guard_to_frozen()

    # -------------------------------------------------------------
    # Win/lose checks
    # -------------------------------------------------------------

    def _all_targets_lit(self) -> bool:
        unlit = [s for s in self.current_level.get_sprites_by_tag("target")
                 if "lit" not in (s.tags or [])]
        return len(unlit) == 0

    def _check_win(self) -> bool:
        return self._all_targets_lit() and self.boomerang_phase == "held"

    # -------------------------------------------------------------
    # Step
    # -------------------------------------------------------------

    def step(self) -> None:
        action_id = self.action.id

        # 1. Avatar action.
        if action_id in (GameAction.ACTION1, GameAction.ACTION2,
                         GameAction.ACTION3, GameAction.ACTION4):
            if action_id == GameAction.ACTION1:
                d = DIR_UP
            elif action_id == GameAction.ACTION2:
                d = DIR_DOWN
            elif action_id == GameAction.ACTION3:
                d = DIR_LEFT
            else:
                d = DIR_RIGHT
            self.facing = d
            self.avatar.set_rotation(_ROTATION_FOR_FACING[d])
            self._try_walk_avatar(d[0], d[1])
        elif action_id == GameAction.ACTION5:
            if self.boomerang_phase == "held":
                self._launch_boomerang()
            elif self.boomerang_phase == "dropped":
                # Pick up if avatar overlaps the dropped cell.
                if self._boomerang_overlaps_avatar():
                    self._catch_boomerang()

        # 2. Advance boomerang if it was already in flight (the launch
        # case advances inside _launch_boomerang).
        if (action_id != GameAction.ACTION5
                and self.boomerang_phase in ("outbound", "returning")):
            self._advance_boomerang_one_tick()

        # 3. Boomerang-guard overlap check (post-boomerang, pre-guard).
        if self._boomerang_overlaps_guard():
            self._trigger_guard_freeze()

        # 4. Guard advance.
        self._advance_guard_one_tick()

        # 5. Avatar-guard collision check.
        if self._avatar_overlaps_guard():
            # Don't lose if guard is frozen (frozen guards still
            # collidable for walking, but stationary - no kill).
            if self.guard is not None and "frozen" not in (self.guard.tags or []):
                self.lose()
                self.complete_action()
                return

        # 6. Decrement step counter.
        self.steps_remaining -= 1
        self._step_hud.set_current(self.steps_remaining)

        # 7. Check win.
        if self._check_win():
            self.next_level()
            self.complete_action()
            return

        # 8. Check lose by step exhaustion.
        if self.steps_remaining <= 0:
            self.lose()
            self.complete_action()
            return

        self.complete_action()

    # -------------------------------------------------------------
    # Engine hooks
    # -------------------------------------------------------------

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self.steps_remaining
        state[0, 1] = {"held": 0, "outbound": 1,
                       "returning": 2, "dropped": 3}.get(
                          self.boomerang_phase, 0)
        state[0, 2] = self.boomerang_outbound_remaining
        state[0, 3] = self.guard_freeze_remaining
        if self.boomerang_pos is not None:
            state[1, 0] = self.boomerang_pos[0]
            state[1, 1] = self.boomerang_pos[1]
        if self.guard is not None:
            state[2, 0] = self.guard.x
            state[2, 1] = self.guard.y
        return state

    def _get_valid_actions(self) -> list:
        valid = []
        for aid in self._available_actions:
            if aid == 5:
                # ACTION5 is invalid mid-flight.
                if self.boomerang_phase in ("outbound", "returning"):
                    continue
            valid.append(ActionInput(id=GameAction.from_id(aid)))
        return valid
