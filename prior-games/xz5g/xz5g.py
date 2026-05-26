"""Generated game xz5g."""

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
# 1. SPRITE BANK
# ---------------------------------------------------------------------

sprites = {
    "anchor_pin": Sprite(
        pixels=[
            [4, 4, 4, 4],
            [4, 14, 14, 4],
            [4, 14, 14, 4],
            [4, 4, 4, 4],
        ],
        name="anchor_pin",
        visible=True,
        collidable=False,
        tags=["anchor_pin", "visit_checkpoint"],
        layer=1,
    ),
    "avatar": Sprite(
        pixels=[
            [4, 9, 9, 9, 9, 4],
            [9, 0, 9, 9, 0, 9],
            [9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9],
            [9, 0, 9, 9, 0, 9],
            [4, 9, 9, 9, 9, 4],
        ],
        name="avatar",
        visible=True,
        collidable=True,
        tags=["rotatable", "avatar"],
        layer=3,
    ),
    "avatar_target": Sprite(
        pixels=[
            [4, 9, 9, 9, 9, 4],
            [9, -1, -1, -1, -1, 9],
            [9, -1, -1, -1, -1, 9],
            [9, -1, -1, -1, -1, 9],
            [9, -1, -1, -1, -1, 9],
            [4, 9, 9, 9, 9, 4],
        ],
        name="avatar_target",
        visible=True,
        collidable=False,
        tags=["target", "avatar_target"],
        layer=1,
    ),
    "companion": Sprite(
        pixels=[
            [4, 12, 12, 12, 12, 4],
            [12, 0, 12, 12, 0, 12],
            [12, 12, 12, 12, 12, 12],
            [12, 12, 12, 12, 12, 12],
            [12, 0, 12, 12, 0, 12],
            [4, 12, 12, 12, 12, 4],
        ],
        name="companion",
        visible=True,
        collidable=True,
        tags=["rotatable", "companion"],
        layer=3,
    ),
    "companion_target": Sprite(
        pixels=[
            [4, 12, 12, 12, 12, 4],
            [12, -1, -1, -1, -1, 12],
            [12, -1, -1, -1, -1, 12],
            [12, -1, -1, -1, -1, 12],
            [12, -1, -1, -1, -1, 12],
            [4, 12, 12, 12, 12, 4],
        ],
        name="companion_target",
        visible=True,
        collidable=False,
        tags=["target", "companion_target"],
        layer=1,
    ),
    "direction_indicator_ccw": Sprite(
        pixels=[
            [11, 13, 13, 13],
            [13, 13, 13, 13],
            [13, 13, 13, 13],
            [13, 13, 13, 13],
        ],
        name="direction_indicator_ccw",
        visible=True,
        collidable=False,
        tags=["direction_indicator", "dir_ccw"],
        layer=4,
    ),
    "direction_indicator_cw": Sprite(
        pixels=[
            [13, 13, 13, 11],
            [13, 13, 13, 13],
            [13, 13, 13, 13],
            [13, 13, 13, 13],
        ],
        name="direction_indicator_cw",
        visible=True,
        collidable=False,
        tags=["direction_indicator", "dir_cw"],
        layer=4,
    ),
    "pivot_marker": Sprite(
        pixels=[
            [-1, 7, -1],
            [7, 6, 7],
            [-1, 7, -1],
        ],
        name="pivot_marker",
        visible=True,
        collidable=False,
        tags=["pivot_marker"],
        layer=5,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------


def _level_1():
    pivot = sprites["pivot_marker"].clone().set_position(0, 0)
    pivot.set_interaction(InteractionMode.REMOVED)
    return Level(
        sprites=[
            sprites["avatar"].clone().set_position(12, 32),
            sprites["avatar_target"].clone().set_position(32, 12),
            pivot,
        ],
        grid_size=(64, 64),
        data={"step_budget": 25},
    )


def _level_2():
    pivot = sprites["pivot_marker"].clone().set_position(0, 0)
    pivot.set_interaction(InteractionMode.REMOVED)
    return Level(
        sprites=[
            sprites["avatar"].clone().set_position(8, 32),
            sprites["avatar_target"].clone().set_position(56, 32),
            sprites["companion"].clone().set_position(32, 8),
            sprites["companion_target"].clone().set_position(32, 56),
            pivot,
        ],
        grid_size=(64, 64),
        data={"step_budget": 30},
    )


def _level_3():
    pivot = sprites["pivot_marker"].clone().set_position(0, 0)
    pivot.set_interaction(InteractionMode.REMOVED)
    return Level(
        sprites=[
            sprites["avatar"].clone().set_position(12, 12),
            sprites["avatar_target"].clone().set_position(52, 52),
            sprites["companion"].clone().set_position(52, 12),
            sprites["companion_target"].clone().set_position(12, 52),
            pivot,
        ],
        grid_size=(64, 64),
        data={"step_budget": 40},
    )


levels = [_level_1(), _level_2(), _level_3()]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 1
PADDING_COLOR = 2
HUD_BAR_FILLED = 6
HUD_BAR_DRAINED = 4
GRID_SIZE = 64

ANCHOR_PIN_UNVISITED = np.array(
    [
        [4, 4, 4, 4],
        [4, 14, 14, 4],
        [4, 14, 14, 4],
        [4, 4, 4, 4],
    ],
    dtype=np.int16,
)

ANCHOR_PIN_VISITED = np.array(
    [
        [4, 4, 4, 4],
        [4, 11, 11, 4],
        [4, 11, 11, 4],
        [4, 4, 4, 4],
    ],
    dtype=np.int16,
)


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------


class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0):
        self.max_steps = max_steps
        self.current_steps = max_steps

    def configure(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_current(self, value: int) -> None:
        if self.max_steps == 0:
            self.current_steps = 0
        else:
            self.current_steps = max(0, min(value, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        ratio = self.current_steps / self.max_steps
        filled = int(round(GRID_SIZE * ratio))
        for x in range(GRID_SIZE):
            frame[GRID_SIZE - 1, x] = HUD_BAR_FILLED if x < filled else HUD_BAR_DRAINED
        return frame


# ---------------------------------------------------------------------
# 5. GAME CLASS
# ---------------------------------------------------------------------


class Xz5g(NovaBaseGame):
    def __init__(self) -> None:
        self._pivot = None
        self._direction = "CW"
        self._steps_left = 0
        self._visited_pins: set = set()
        self._step_hud = StepCounterHud(0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_hud],
        )
        super().__init__(
            game_id="xz5g",
            levels=levels,
            camera=camera,
            available_actions=[5, 6],
        )

    # ----- per-level setup ---------------------------------------------

    def on_set_level(self, level: Level) -> None:
        budget = level.get_data("step_budget") or 25
        self._steps_left = budget
        self._step_hud.configure(budget)
        self._pivot = None
        self._direction = "CW"
        self._visited_pins = set()

        # Hide the pivot_marker until first click.
        for marker in level.get_sprites_by_tag("pivot_marker"):
            marker.set_interaction(InteractionMode.REMOVED)

        # Restore default direction indicator state at L3.
        for s in level.get_sprites_by_tag("dir_cw"):
            s.set_interaction(InteractionMode.TANGIBLE)
        for s in level.get_sprites_by_tag("dir_ccw"):
            s.set_interaction(InteractionMode.REMOVED)

        # Reset anchor_pin pixels to unvisited state.
        for pin in level.get_sprites_by_tag("anchor_pin"):
            pin.pixels = ANCHOR_PIN_UNVISITED.copy()

    # ----- helpers ------------------------------------------------------

    def _click_hits_tag(self, gx: int, gy: int, tag: str) -> bool:
        for s in self.current_level.get_sprites_by_tag(tag):
            if s.interaction == InteractionMode.REMOVED:
                continue
            if s.x <= gx < s.x + s.width and s.y <= gy < s.y + s.height:
                return True
        return False

    def _pivot_marker_sprite(self):
        markers = self.current_level.get_sprites_by_tag("pivot_marker")
        return markers[0] if markers else None

    # ----- click handler ------------------------------------------------

    def _handle_click(self) -> None:
        data = self.action.data or {}
        x = data.get("x")
        y = data.get("y")
        if x is None or y is None:
            return
        coord = self.camera.display_to_grid(int(x), int(y))
        if coord is None:
            return
        gx, gy = coord

        # Rule 1: direction_indicator (L3 only) → toggle direction.
        if self._click_hits_tag(gx, gy, "direction_indicator"):
            self._toggle_direction()
            return

        # Rule 2: any rotatable / target / anchor_pin → no-op.
        for tag in ("rotatable", "target", "anchor_pin"):
            if self._click_hits_tag(gx, gy, tag):
                return

        # Rule 3: set pivot. The 3×3 "+" marker is positioned so its
        # centre pixel coincides with the pivot cell (gx, gy).
        self._pivot = (gx, gy)
        marker = self._pivot_marker_sprite()
        if marker is not None:
            hx = max(0, min(GRID_SIZE - marker.width, gx - 1))
            hy = max(0, min(GRID_SIZE - marker.height, gy - 1))
            marker.set_position(hx, hy)
            marker.set_interaction(InteractionMode.INTANGIBLE)

    def _toggle_direction(self) -> None:
        if self._direction == "CW":
            self._direction = "CCW"
            for s in self.current_level.get_sprites_by_tag("dir_cw"):
                s.set_interaction(InteractionMode.REMOVED)
            for s in self.current_level.get_sprites_by_tag("dir_ccw"):
                s.set_interaction(InteractionMode.TANGIBLE)
        else:
            self._direction = "CW"
            for s in self.current_level.get_sprites_by_tag("dir_ccw"):
                s.set_interaction(InteractionMode.REMOVED)
            for s in self.current_level.get_sprites_by_tag("dir_cw"):
                s.set_interaction(InteractionMode.TANGIBLE)

    # ----- rotation handler --------------------------------------------

    def _handle_rotate(self) -> None:
        if self._pivot is None:
            return
        px, py = self._pivot
        rotatables = list(self.current_level.get_sprites_by_tag("rotatable"))
        if not rotatables:
            return

        proposals = []
        for s in rotatables:
            x, y = s.x, s.y
            if self._direction == "CW":
                nx = px + py - y
                ny = py + x - px
            else:
                nx = px - py + y
                ny = px + py - x
            proposals.append((s, nx, ny))

        # Bounds check — any rotatable footprint must fit in the grid.
        for s, nx, ny in proposals:
            if nx < 0 or ny < 0 or nx + s.width > GRID_SIZE or ny + s.height > GRID_SIZE:
                return

        # Collision check — two rotatables targeting same cell, except clean
        # simultaneous swap (each lands on the other's pre-rotation cell).
        seen = {}
        for s, nx, ny in proposals:
            key = (nx, ny)
            if key in seen:
                # collision; allow only clean swap of two
                other_s, other_nx, other_ny = seen[key]
                # not a swap; reject
                return
            seen[key] = (s, nx, ny)

        # Apply.
        for s, nx, ny in proposals:
            s.set_position(nx, ny)
            if self._direction == "CW":
                s.rotate(90)
            else:
                s.rotate(270)

    # ----- visit-checkpoint update -------------------------------------

    def _update_visited_pins(self) -> None:
        rotatables = self.current_level.get_sprites_by_tag("rotatable")
        pins = self.current_level.get_sprites_by_tag("anchor_pin")
        for r in rotatables:
            for p in pins:
                if r.x == p.x and r.y == p.y:
                    if (p.x, p.y) not in self._visited_pins:
                        self._visited_pins.add((p.x, p.y))
                        p.pixels = ANCHOR_PIN_VISITED.copy()

    # ----- win predicate ------------------------------------------------

    def _check_win(self) -> bool:
        for target in self.current_level.get_sprites_by_tag("target"):
            match_tag = "avatar" if "avatar_target" in target.tags else "companion"
            matched = False
            for r in self.current_level.get_sprites_by_tag(match_tag):
                if r.x == target.x and r.y == target.y:
                    matched = True
                    break
            if not matched:
                return False
        for pin in self.current_level.get_sprites_by_tag("anchor_pin"):
            if (pin.x, pin.y) not in self._visited_pins:
                return False
        return True

    # ----- step ---------------------------------------------------------

    def step(self) -> None:
        aid = self.action.id
        if aid == GameAction.ACTION6:
            self._handle_click()
        elif aid == GameAction.ACTION5:
            self._handle_rotate()

        self._update_visited_pins()

        self._steps_left = max(0, self._steps_left - 1)
        self._step_hud.set_current(self._steps_left)

        if self._check_win():
            self.next_level()
            self.complete_action()
            return

        if self._steps_left <= 0:
            self.lose()
            self.complete_action()
            return

        self.complete_action()

    # ----- engine hooks -------------------------------------------------

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._steps_left
        state[0, 1] = 1 if self._direction == "CW" else 2
        state[0, 2] = self._pivot[0] if self._pivot is not None else -1
        state[0, 3] = self._pivot[1] if self._pivot is not None else -1
        state[1, 0] = len(self._visited_pins)
        return state

    def _get_valid_actions(self):
        return super()._get_valid_actions()
