"""pq5w generated game source."""

import numpy as np
from novaengine import (
    ActionInput,
    NovaBaseGame,
    Camera,
    GameAction,
    Level,
    RenderableUserDisplay,
    Sprite,
)


# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------

# Palette assignments (per skills/global/color-legend.md):
#   0  white      — playfield background
#   3  grey       — wall interior, goal interior
#   4  off-black  — anchor portal outer ring, forbidden interior
#   5  black      — wall outline, avatar centre dots, HUD empty
#   6  magenta    — both portals' shared centre core (pairing cue)
#   7  pink       — float portal outer ring + corner pips (unselected)
#   8  red        — forbidden corners
#   10 light-blue — float portal's 4 corner pips when selected
#   11 yellow     — avatar body
#   14 green      — goal frame, HUD fill

sprites = {
    "avatar": Sprite(
        pixels=[
            [-1, 11, 11, -1],
            [11,  5,  5, 11],
            [11,  5,  5, 11],
            [-1, 11, 11, -1],
        ],
        name="avatar",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=3,
    ),
    "anchor_portal": Sprite(
        pixels=[
            [4, 4, 4, 4],
            [4, 6, 6, 4],
            [4, 6, 6, 4],
            [4, 4, 4, 4],
        ],
        name="anchor_portal",
        visible=True,
        collidable=False,
        tags=["portal", "anchor"],
        layer=1,
    ),
    "float_portal": Sprite(
        pixels=[
            [7, 7, 7, 7],
            [7, 6, 6, 7],
            [7, 6, 6, 7],
            [7, 7, 7, 7],
        ],
        name="float_portal",
        visible=True,
        collidable=False,
        tags=["portal", "float"],
        layer=1,
    ),
    "wall": Sprite(
        pixels=[
            [5, 5, 5, 5],
            [5, 3, 3, 5],
            [5, 3, 3, 5],
            [5, 5, 5, 5],
        ],
        name="wall",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=1,
    ),
    "goal": Sprite(
        pixels=[
            [14, 14, 14, 14],
            [14,  3,  3, 14],
            [14,  3,  3, 14],
            [14, 14, 14, 14],
        ],
        name="goal",
        visible=True,
        collidable=False,
        tags=["goal"],
        layer=0,
    ),
    "forbidden": Sprite(
        pixels=[
            [8, 3, 3, 8],
            [3, 4, 4, 3],
            [3, 4, 4, 3],
            [8, 3, 3, 8],
        ],
        name="forbidden",
        visible=True,
        collidable=False,
        tags=["forbidden"],
        layer=0,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS — exactly 3 entries
# ---------------------------------------------------------------------

STRIDE = 4
GRID_W = 64
GRID_H = 60


def _level_1_sprites():
    placed = []
    # Full-height wall column at logical x=8 (pixel x=32), y=0..14.
    for gy in range(15):
        placed.append(sprites["wall"].clone().set_position(32, gy * 4))
    # Avatar at logical (1, 7) = pixel (4, 28).
    placed.append(sprites["avatar"].clone().set_position(4, 28))
    # Anchor portal at (3, 7) = pixel (12, 28).
    placed.append(sprites["anchor_portal"].clone().set_position(12, 28))
    # Float portal at (12, 7) = pixel (48, 28).
    placed.append(sprites["float_portal"].clone().set_position(48, 28))
    # Goal at (14, 7) = pixel (56, 28).
    placed.append(sprites["goal"].clone().set_position(56, 28))
    return placed


def _level_2_sprites():
    placed = []
    # Closed-room walls: rectangle x=4..11, y=2..6 (outer cells).
    # Top row (y=2) and bottom row (y=6), x=4..11.
    for gx in range(4, 12):
        placed.append(sprites["wall"].clone().set_position(gx * 4, 2 * 4))
        placed.append(sprites["wall"].clone().set_position(gx * 4, 6 * 4))
    # Left column (x=4) and right column (x=11), y=3..5.
    for gy in range(3, 6):
        placed.append(sprites["wall"].clone().set_position(4 * 4, gy * 4))
        placed.append(sprites["wall"].clone().set_position(11 * 4, gy * 4))
    # Avatar at logical (1, 9) = pixel (4, 36) (outside the room).
    placed.append(sprites["avatar"].clone().set_position(4, 36))
    # Anchor portal at (6, 4) = pixel (24, 16) (inside).
    placed.append(sprites["anchor_portal"].clone().set_position(24, 16))
    # Float portal initial at (10, 3) = pixel (40, 12) (inside, upper-right).
    placed.append(sprites["float_portal"].clone().set_position(40, 12))
    # Goal at (10, 4) = pixel (40, 16) (inside).
    placed.append(sprites["goal"].clone().set_position(40, 16))
    return placed


def _level_3_sprites():
    placed = _level_2_sprites()
    # Forbidden column at x=8, y=3..5 inside the room.
    for gy in range(3, 6):
        placed.append(sprites["forbidden"].clone().set_position(8 * 4, gy * 4))
    return placed


levels = [
    Level(
        sprites=_level_1_sprites(),
        grid_size=(GRID_W, GRID_H),
        data={"step_budget": 30},
    ),
    Level(
        sprites=_level_2_sprites(),
        grid_size=(GRID_W, GRID_H),
        data={"step_budget": 50},
    ),
    Level(
        sprites=_level_3_sprites(),
        grid_size=(GRID_W, GRID_H),
        data={"step_budget": 80},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 0
PADDING_COLOR = 0
HUD_FILL_COLOUR = 14
HUD_EMPTY_COLOUR = 5

# When the float portal is "selected", only its FOUR CORNER PIXELS
# change colour (pink → light-blue) so the player sees a subtle but
# unmistakable cue. The rest of the outer ring and the magenta core
# stay the same.
FLOAT_CORNER_UNSELECTED = 7    # pink (matches the rest of the outer ring)
FLOAT_CORNER_SELECTED = 10     # light-blue corner pip
FLOAT_CORNER_COORDS = ((0, 0), (0, 3), (3, 0), (3, 3))  # (y, x)


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------


class StepCounterHud(RenderableUserDisplay):
    """Bottom 4-row horizontal depleting bar at pixel rows 60..63."""

    def __init__(self) -> None:
        self.step_budget = 0
        self.steps_remaining = 0

    def configure(self, step_budget: int) -> None:
        self.step_budget = step_budget
        self.steps_remaining = step_budget

    def set_remaining(self, value: int) -> None:
        self.steps_remaining = max(0, min(value, self.step_budget))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.step_budget == 0:
            return frame
        ratio = self.steps_remaining / self.step_budget
        filled = round(64 * ratio)
        for hud_row in range(60, 64):
            for x in range(64):
                if x < filled:
                    frame[hud_row, x] = HUD_FILL_COLOUR
                else:
                    frame[hud_row, x] = HUD_EMPTY_COLOUR
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------


class Pq5w(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_hud = StepCounterHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_hud],
        )
        super().__init__(
            game_id="pq5w",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 6],
        )
        self._step_budget = 0
        self._steps_used = 0
        self._teleport_pending: tuple[int, int] | None = None
        self._float_selected = False

    # -- per-level setup ------------------------------------------------

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (GRID_W, GRID_H)
        self.camera.width = gw
        self.camera.height = gh
        self._step_budget = level.get_data("step_budget") or 30
        self._steps_used = 0
        self._teleport_pending = None
        self._step_counter_hud.configure(self._step_budget)
        # Ensure the float portal starts each level in the unselected
        # state — sprites persist across resets, so a previous run that
        # left the corner pips light-blue must be reverted here.
        self._float_selected = False
        float_p = self._float_portal()
        for cy, cx in FLOAT_CORNER_COORDS:
            float_p.pixels[cy, cx] = FLOAT_CORNER_UNSELECTED

    # -- helpers --------------------------------------------------------

    def _avatar(self) -> Sprite:
        return self.current_level.get_sprites_by_tag("player")[0]

    def _anchor_portal(self) -> Sprite:
        return self.current_level.get_sprites_by_tag("anchor")[0]

    def _float_portal(self) -> Sprite:
        return self.current_level.get_sprites_by_tag("float")[0]

    def _goal(self) -> Sprite:
        return self.current_level.get_sprites_by_tag("goal")[0]

    def _wall_at(self, px: int, py: int) -> Sprite | None:
        for s in self.current_level.get_sprites_by_tag("wall"):
            if s.x == px and s.y == py:
                return s
        return None

    def _forbidden_at(self, px: int, py: int) -> Sprite | None:
        for s in self.current_level.get_sprites_by_tag("forbidden"):
            if s.x == px and s.y == py:
                return s
        return None

    def _portal_at(self, px: int, py: int) -> Sprite | None:
        for s in self.current_level.get_sprites_by_tag("portal"):
            if s.x == px and s.y == py:
                return s
        return None

    def _is_walkable(self, px: int, py: int) -> bool:
        gw, gh = self.current_level.grid_size or (GRID_W, GRID_H)
        if px < 0 or py < 0:
            return False
        if px + STRIDE > gw or py + STRIDE > gh:
            return False
        if self._wall_at(px, py) is not None:
            return False
        return True

    def _is_valid_relocate_target(self, px: int, py: int) -> bool:
        if px % STRIDE != 0 or py % STRIDE != 0:
            return False
        gw, gh = self.current_level.grid_size or (GRID_W, GRID_H)
        if px < 0 or py < 0:
            return False
        if px + STRIDE > gw or py + STRIDE > gh:
            return False
        if self._wall_at(px, py) is not None:
            return False
        anchor = self._anchor_portal()
        if anchor.x == px and anchor.y == py:
            return False
        goal = self._goal()
        if goal.x == px and goal.y == py:
            return False
        if self._forbidden_at(px, py) is not None:
            return False
        avatar = self._avatar()
        if avatar.x == px and avatar.y == py:
            return False
        return True

    # -- step dispatch --------------------------------------------------

    def step(self) -> None:
        # Resolve a pending teleport first; the action's id is consumed.
        if self._teleport_pending is not None:
            dst_x, dst_y = self._teleport_pending
            self._avatar().set_position(dst_x, dst_y)
            self._teleport_pending = None
            self._steps_used += 1
            self._step_counter_hud.set_remaining(self._step_budget - self._steps_used)
            self._post_action_resolve()
            self.complete_action()
            return

        action_id = self.action.id
        if action_id == GameAction.ACTION1:
            self._attempt_walk(0, -STRIDE)
        elif action_id == GameAction.ACTION2:
            self._attempt_walk(0, STRIDE)
        elif action_id == GameAction.ACTION3:
            self._attempt_walk(-STRIDE, 0)
        elif action_id == GameAction.ACTION4:
            self._attempt_walk(STRIDE, 0)
        elif action_id == GameAction.ACTION6:
            self._handle_click()

        self._steps_used += 1
        self._step_counter_hud.set_remaining(self._step_budget - self._steps_used)
        self._post_action_resolve()
        self.complete_action()

    def _attempt_walk(self, dx: int, dy: int) -> None:
        avatar = self._avatar()
        new_x = avatar.x + dx
        new_y = avatar.y + dy
        if not self._is_walkable(new_x, new_y):
            return
        avatar.set_position(new_x, new_y)
        portal = self._portal_at(new_x, new_y)
        if portal is None:
            return
        anchor = self._anchor_portal()
        float_p = self._float_portal()
        if portal is anchor:
            self._teleport_pending = (float_p.x, float_p.y)
        else:
            self._teleport_pending = (anchor.x, anchor.y)

    def _handle_click(self) -> None:
        data = self.action.data
        if not isinstance(data, dict):
            return
        try:
            cx_raw = int(data.get("x", 0))
            cy_raw = int(data.get("y", 0))
        except (TypeError, ValueError):
            return
        grid = self.camera.display_to_grid(cx_raw, cy_raw)
        if grid is None:
            return
        gx, gy = grid
        cell_x = gx - (gx % STRIDE)
        cell_y = gy - (gy % STRIDE)
        float_p = self._float_portal()
        # Click on the float portal's own cell toggles the selected
        # state. The selected state is visualised by re-tinting the
        # float portal's outer ring (pink → light-blue).
        if cell_x == float_p.x and cell_y == float_p.y:
            self._set_float_selected(not self._float_selected)
            return
        # Click elsewhere only relocates the float portal if it is
        # currently selected AND the target cell is valid. Otherwise
        # the click is a no-op (the selected state persists so the
        # player can try a different cell).
        if not self._float_selected:
            return
        if not self._is_valid_relocate_target(cell_x, cell_y):
            return
        float_p.set_position(cell_x, cell_y)
        self._set_float_selected(False)

    def _set_float_selected(self, value: bool) -> None:
        if value == self._float_selected:
            return
        float_p = self._float_portal()
        new_corner = FLOAT_CORNER_SELECTED if value else FLOAT_CORNER_UNSELECTED
        for cy, cx in FLOAT_CORNER_COORDS:
            float_p.pixels[cy, cx] = new_corner
        self._float_selected = value

    def _post_action_resolve(self) -> None:
        avatar = self._avatar()
        if self._forbidden_at(avatar.x, avatar.y) is not None:
            self.lose()
            return
        goal = self._goal()
        if avatar.x == goal.x and avatar.y == goal.y:
            self.next_level()
            return
        if self._steps_used >= self._step_budget:
            self.lose()
            return

    # -- engine hooks ---------------------------------------------------

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 5), dtype=np.int16)
        avatar = self._avatar()
        state[0, 0] = avatar.x
        state[0, 1] = avatar.y
        state[0, 2] = self._steps_used
        state[0, 3] = 1 if self._teleport_pending is not None else 0
        state[0, 4] = 1 if self._float_selected else 0
        return state

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()
