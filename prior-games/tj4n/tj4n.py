"""."""

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
    "avatar": Sprite(
        pixels=[
            [-1, 9, 9, -1],
            [9, 4, 4, 9],
            [9, 4, 4, 9],
            [-1, 9, 9, -1],
        ],
        name="avatar",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=3,
    ),
    "trail_cell": Sprite(
        pixels=[
            [-1, 7, 7, -1],
            [7, 4, 4, 7],
            [7, 4, 4, 7],
            [-1, 7, 7, -1],
        ],
        name="trail_cell",
        visible=True,
        collidable=False,
        tags=["trail"],
        layer=1,
    ),
    "target": Sprite(
        pixels=[
            [11, 11, 11, 11],
            [11, 12, 12, 11],
            [11, 12, 12, 11],
            [11, 11, 11, 11],
        ],
        name="target",
        visible=True,
        collidable=True,
        tags=["target"],
        layer=2,
    ),
    "forbidden": Sprite(
        pixels=[
            [8, 8, 8, 8],
            [8, 4, 4, 8],
            [8, 4, 4, 8],
            [8, 8, 8, 8],
        ],
        name="forbidden",
        visible=True,
        collidable=True,
        tags=["forbidden"],
        layer=2,
    ),
    "pink_marker": Sprite(
        pixels=[
            [-1, -1, -1, -1],
            [-1, 7, 7, -1],
            [-1, 7, 7, -1],
            [-1, -1, -1, -1],
        ],
        name="pink_marker",
        visible=True,
        collidable=False,
        tags=["pink_marker"],
        layer=2,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
CELL = 4  # display pixels per logical cell
GRID_CELLS = 16


def _cp(cx, cy):
    return (cx * CELL, cy * CELL)


levels = [
    Level(
        sprites=[
            sprites["avatar"].clone().set_position(*_cp(5, 8)),
            sprites["target"].clone().set_position(*_cp(8, 8)),
            sprites["target"].clone().set_position(*_cp(9, 8)),
            sprites["target"].clone().set_position(*_cp(10, 8)),
        ],
        grid_size=(64, 64),
        data={"step_budget": 50, "level_num": 1},
    ),
    Level(
        sprites=[
            sprites["avatar"].clone().set_position(*_cp(8, 13)),
            sprites["target"].clone().set_position(*_cp(4, 6)),
            sprites["target"].clone().set_position(*_cp(4, 9)),
            sprites["target"].clone().set_position(*_cp(12, 6)),
            sprites["target"].clone().set_position(*_cp(12, 9)),
            sprites["forbidden"].clone().set_position(*_cp(8, 5)),
            sprites["forbidden"].clone().set_position(*_cp(8, 7)),
            sprites["forbidden"].clone().set_position(*_cp(8, 9)),
        ],
        grid_size=(64, 64),
        data={"step_budget": 110, "level_num": 2},
    ),
    Level(
        sprites=[
            sprites["avatar"].clone().set_position(*_cp(8, 13)),
            sprites["target"].clone().set_position(*_cp(4, 6)),
            sprites["target"].clone().set_position(*_cp(4, 9)),
            sprites["target"].clone().set_position(*_cp(12, 6)),
            sprites["target"].clone().set_position(*_cp(12, 9)),
            sprites["forbidden"].clone().set_position(*_cp(8, 5)),
            sprites["forbidden"].clone().set_position(*_cp(8, 7)),
            sprites["forbidden"].clone().set_position(*_cp(8, 9)),
            sprites["pink_marker"].clone().set_position(*_cp(2, 7)),
            sprites["pink_marker"].clone().set_position(*_cp(14, 7)),
            sprites["pink_marker"].clone().set_position(*_cp(8, 14)),
        ],
        grid_size=(64, 64),
        data={"step_budget": 200, "level_num": 3},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 1
PADDING_COLOR = 1
FLASH_FRAMES = 4


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame):
        budget = self.game._step_budget
        if budget <= 0:
            return frame
        remaining = max(0, budget - self.game._action_count)
        filled = int(round(64 * remaining / budget))
        for x in range(64):
            frame[0, x] = 14 if x < filled else 4
        return frame


class StrikeHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame):
        if self.game._level_num == 1:
            return frame
        for i in range(3):
            color = 8 if i < self.game._strikes else 3
            base_x = 50 + i * 5
            for dy in (1, 2):
                for dx in range(3):
                    frame[dy, base_x + dx] = color
        return frame


# ---------------------------------------------------------------------
# 5. GAME CLASS
# ---------------------------------------------------------------------
class Tj4n(NovaBaseGame):
    def __init__(self):
        camera = Camera(background=BACKGROUND_COLOR, letter_box=PADDING_COLOR)
        self._step_counter_hud = StepCounterHud(self)
        self._strike_hud = StrikeHud(self)
        camera.replace_interface([self._step_counter_hud, self._strike_hud])
        self._avatar_pos = (0, 0)
        self._trail_seq = []
        self._trail_sprites = []
        self._strikes = 0
        self._step_budget = 50
        self._level_num = 1
        self._post_closure_flash = -1
        self._pending_capture = []
        self._pending_strike_sprites = []
        super().__init__(
            game_id="tj4n",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    def on_set_level(self, level):
        self._step_budget = level.get_data("step_budget") or 50
        self._level_num = level.get_data("level_num") or 1
        self._strikes = 0
        self._post_closure_flash = -1
        self._pending_capture = []
        self._pending_strike_sprites = []
        self._trail_seq = []
        self._trail_sprites = []
        avatars = level.get_sprites_by_tag("player")
        if avatars:
            self._avatar_pos = (avatars[0].x, avatars[0].y)
        else:
            self._avatar_pos = (0, 0)
        # On entering each cell, the avatar consumes any pink_marker present
        # at that cell. If the avatar starts a level on a pink-marker cell,
        # consume it immediately.
        self._consume_pink_at(self._avatar_pos)

    # -----------------------------------------------------------------
    # Movement validity
    # -----------------------------------------------------------------
    def _is_blocked_for_avatar(self, x, y):
        if x < 0 or y < 0 or x + CELL > 64 or y + CELL > 64:
            return True
        for sp in self.current_level.get_sprites():
            if sp.interaction == InteractionMode.REMOVED:
                continue
            if sp.x != x or sp.y != y:
                continue
            tags = sp.tags or []
            # Avatar walks freely through its own trail and onto pink markers
            # (they get consumed); only solid game-objects block.
            if any(t in tags for t in ("forbidden", "target")):
                return True
        return False

    def _consume_pink_at(self, pos):
        """If a pink_marker sits at the avatar's cell `pos`, set it REMOVED."""
        x, y = pos
        for sp in self.current_level.get_sprites_by_tag("pink_marker"):
            if sp.interaction == InteractionMode.REMOVED:
                continue
            if sp.x == x and sp.y == y:
                sp.set_interaction(InteractionMode.REMOVED)

    # -----------------------------------------------------------------
    # Trail management
    # -----------------------------------------------------------------
    def _add_trail_at(self, x, y):
        sp = sprites["trail_cell"].clone().set_position(x, y)
        self.current_level.add_sprite(sp)
        self._trail_seq.append((x, y))
        self._trail_sprites.append(sp)
        return sp

    def _trail_index(self, pos):
        for i, p in enumerate(self._trail_seq):
            if p == pos:
                return i
        return -1

    # -----------------------------------------------------------------
    # Closure: point-in-polygon ray casting
    # -----------------------------------------------------------------
    @staticmethod
    def _point_in_polygon(px, py, poly):
        n = len(poly)
        if n < 3:
            return False
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = poly[i]
            xj, yj = poly[j]
            if (yi > py) != (yj > py):
                x_intersect = (xj - xi) * (py - yi) / (yj - yi) + xi
                if px < x_intersect:
                    inside = not inside
            j = i
        return inside

    def _process_closure(self, closure_idx, closure_cell):
        polygon = list(self._trail_seq[closure_idx:])
        polygon.append(closure_cell)
        captures = []
        strike_sprites = []
        for cy in range(GRID_CELLS):
            for cx in range(GRID_CELLS):
                px_pos = cx * CELL
                py_pos = cy * CELL
                centre_x = px_pos + CELL // 2
                centre_y = py_pos + CELL // 2
                if not self._point_in_polygon(centre_x, centre_y, polygon):
                    continue
                target_sprite = None
                for sp in self.current_level.get_sprites():
                    if sp.interaction == InteractionMode.REMOVED:
                        continue
                    if sp.x != px_pos or sp.y != py_pos:
                        continue
                    tags = sp.tags or []
                    if "target" in tags or "forbidden" in tags:
                        target_sprite = sp
                        break
                if target_sprite is None:
                    continue
                tags = target_sprite.tags or []
                if "target" in tags:
                    captures.append(target_sprite)
                elif "forbidden" in tags:
                    strike_sprites.append(target_sprite)
        self._pending_capture = captures
        self._pending_strike_sprites = strike_sprites
        self._post_closure_flash = 0

    def _flash_tick(self):
        flash_on = (self._post_closure_flash % 2) == 0
        for sp in self._pending_capture:
            sp.color_remap(None, 0 if flash_on else 11)
        for sp in self._trail_sprites:
            sp.color_remap(None, 0 if flash_on else 7)
        self._post_closure_flash += 1

    def _commit_closure(self):
        for sp in self._pending_capture:
            sp.set_interaction(InteractionMode.REMOVED)
        self._strikes += len(self._pending_strike_sprites)
        for sp in self._trail_sprites:
            self.current_level.remove_sprite(sp)
        self._trail_sprites = []
        self._trail_seq = []
        self._pending_capture = []
        self._pending_strike_sprites = []
        self._post_closure_flash = -1

    # -----------------------------------------------------------------
    # Win / lose predicates
    # -----------------------------------------------------------------
    def _check_win(self):
        if self._strikes >= 3:
            return False
        for sp in self.current_level.get_sprites_by_tag("target"):
            if sp.interaction != InteractionMode.REMOVED:
                return False
        for sp in self.current_level.get_sprites_by_tag("pink_marker"):
            if sp.interaction != InteractionMode.REMOVED:
                return False
        return True

    def _check_lose(self):
        if self._strikes >= 3:
            return True
        if self._action_count >= self._step_budget:
            return True
        return False

    # -----------------------------------------------------------------
    # Main step
    # -----------------------------------------------------------------
    def step(self):
        # Mid-flash animation: return without complete_action so engine re-invokes
        # step() until the flash finishes. Single agent action covers the whole
        # closure animation.
        if self._post_closure_flash >= 0:
            self._flash_tick()
            if self._post_closure_flash >= FLASH_FRAMES:
                self._commit_closure()
                if self._strikes >= 3:
                    self.lose()
                    self.complete_action()
                    return
                if self._check_win():
                    self.next_level()
                    self.complete_action()
                    return
                self.complete_action()
                return
            return

        # Step budget exhausted
        if self._action_count >= self._step_budget:
            self.lose()
            self.complete_action()
            return

        # Direction lookup
        dx, dy = 0, 0
        if self.action.id == GameAction.ACTION1:
            dy = -CELL
        elif self.action.id == GameAction.ACTION2:
            dy = CELL
        elif self.action.id == GameAction.ACTION3:
            dx = -CELL
        elif self.action.id == GameAction.ACTION4:
            dx = CELL
        else:
            self.complete_action()
            return

        old_pos = self._avatar_pos
        new_pos = (old_pos[0] + dx, old_pos[1] + dy)

        if self._is_blocked_for_avatar(*new_pos):
            self.complete_action()
            return

        # Move avatar
        avatars = self.current_level.get_sprites_by_tag("player")
        if avatars:
            avatars[0].set_position(*new_pos)
        self._avatar_pos = new_pos

        # Stepping onto a pink_marker cell consumes the marker (M5 — the
        # avatar's trail-head must visit every pink marker for the level to
        # win).
        self._consume_pink_at(new_pos)

        # Closure check — flash will animate over the next few step() calls.
        # Do NOT complete_action here; engine re-invokes step() with the same
        # action to tick the flash through to completion.
        idx = self._trail_index(new_pos)
        if idx >= 0:
            self._process_closure(idx, new_pos)
            return

        # Deposit trail at OLD position
        self._add_trail_at(*old_pos)

        if self._check_win():
            self.next_level()
            self.complete_action()
            return

        self.complete_action()

    # -----------------------------------------------------------------
    # Engine hooks
    # -----------------------------------------------------------------
    def _get_hidden_state(self):
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._action_count
        state[0, 1] = self._strikes
        state[0, 2] = len(self._trail_seq)
        state[0, 3] = self._post_closure_flash
        return state

    def _get_valid_actions(self):
        if self._post_closure_flash >= 0:
            return []
        return super()._get_valid_actions()
