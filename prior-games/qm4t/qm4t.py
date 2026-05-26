"""qm4t."""

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
    "critter_green": Sprite(
        pixels=[
            [-1, 14, 14, 14, -1],
            [14, 14,  0, 14, 14],
            [14, 14, 14, 14, 14],
            [-1, 14, 14, 14, -1],
        ],
        name="critter_green",
        visible=True,
        collidable=True,
        tags=["critter", "critter_green"],
    ),
    "critter_yellow": Sprite(
        pixels=[
            [-1, 11, 11, 11, -1],
            [11, 11,  0, 11, 11],
            [11, 11, 11, 11, 11],
            [-1, 11, 11, 11, -1],
        ],
        name="critter_yellow",
        visible=True,
        collidable=True,
        tags=["critter", "critter_yellow"],
    ),
    "critter_maroon": Sprite(
        pixels=[
            [-1, 13, 13, 13, -1],
            [13, 13,  0, 13, 13],
            [13, 13, 13, 13, 13],
            [-1, 13, 13, 13, -1],
        ],
        name="critter_maroon",
        visible=True,
        collidable=True,
        tags=["critter", "critter_maroon"],
    ),
    "patroller_purple": Sprite(
        pixels=[
            [-1, -1, 15, -1, -1],
            [-1, 15, 15, 15, -1],
            [15, 15,  0, 15, 15],
            [-1, 15, 15, 15, -1],
            [-1, -1, 15, -1, -1],
        ],
        name="patroller_purple",
        visible=True,
        collidable=True,
        tags=["patroller"],
    ),
    "vertex_post": Sprite(
        pixels=[
            [6],
            [6],
            [6],
        ],
        name="vertex_post",
        visible=True,
        collidable=True,
        tags=["vertex_post"],
    ),
    "tally_dot_green": Sprite(
        pixels=[
            [14, 14, 14],
            [14,  0, 14],
            [14, 14, 14],
        ],
        name="tally_dot_green",
        visible=True,
        collidable=False,
        tags=["tally", "tally_green"],
        interaction=InteractionMode.INTANGIBLE,
    ),
    "tally_dot_yellow": Sprite(
        pixels=[
            [11, 11, 11],
            [11,  0, 11],
            [11, 11, 11],
        ],
        name="tally_dot_yellow",
        visible=True,
        collidable=False,
        tags=["tally", "tally_yellow"],
        interaction=InteractionMode.INTANGIBLE,
    ),
    "strike_marker": Sprite(
        pixels=[
            [8, 8, 8],
            [8, 8, 8],
            [8, 8, 8],
        ],
        name="strike_marker",
        visible=True,
        collidable=False,
        tags=["strike_hud"],
        interaction=InteractionMode.INTANGIBLE,
    ),
    "pen_overlay": Sprite(
        pixels=[[-1] * 64 for _ in range(64)],
        name="pen_overlay",
        visible=True,
        collidable=False,
        tags=["pen_overlay"],
        interaction=InteractionMode.INTANGIBLE,
        layer=5,
    ),
}

# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
levels = [
    # ---- Level 1: 3 greens, no maroons, no patrollers ----
    Level(
        sprites=[
            sprites["critter_green"].clone().set_position(20, 20),
            sprites["critter_green"].clone().set_position(40, 22),
            sprites["critter_green"].clone().set_position(30, 40),
            sprites["tally_dot_green"].clone().set_position(20, 0),
            sprites["tally_dot_green"].clone().set_position(28, 0),
            sprites["tally_dot_green"].clone().set_position(36, 0),
            sprites["pen_overlay"].clone().set_position(0, 0),
        ],
        grid_size=(64, 64),
        data={"step_budget": 30, "patroller_cycles": []},
    ),
    # ---- Level 2: 3 greens centre cluster, 4 maroons at corners ----
    Level(
        sprites=[
            sprites["critter_green"].clone().set_position(20, 20),
            sprites["critter_green"].clone().set_position(40, 25),
            sprites["critter_green"].clone().set_position(30, 45),
            sprites["critter_maroon"].clone().set_position(5, 5),
            sprites["critter_maroon"].clone().set_position(58, 5),
            sprites["critter_maroon"].clone().set_position(5, 58),
            sprites["critter_maroon"].clone().set_position(58, 58),
            sprites["tally_dot_green"].clone().set_position(20, 0),
            sprites["tally_dot_green"].clone().set_position(28, 0),
            sprites["tally_dot_green"].clone().set_position(36, 0),
            sprites["pen_overlay"].clone().set_position(0, 0),
        ],
        grid_size=(64, 64),
        data={"step_budget": 50, "patroller_cycles": []},
    ),
    # ---- Level 3: 3 greens, 2 yellows, 3 maroons, 3 patrollers ----
    Level(
        sprites=[
            sprites["critter_green"].clone().set_position(15, 15),
            sprites["critter_green"].clone().set_position(50, 18),
            sprites["critter_green"].clone().set_position(32, 50),
            sprites["critter_yellow"].clone().set_position(20, 32),
            sprites["critter_yellow"].clone().set_position(45, 32),
            sprites["critter_maroon"].clone().set_position(8, 32),
            sprites["critter_maroon"].clone().set_position(58, 32),
            sprites["critter_maroon"].clone().set_position(32, 4),
            sprites["patroller_purple"].clone().set_position(28, 28),
            sprites["patroller_purple"].clone().set_position(34, 28),
            sprites["patroller_purple"].clone().set_position(28, 34),
            sprites["tally_dot_green"].clone().set_position(15, 0),
            sprites["tally_dot_green"].clone().set_position(23, 0),
            sprites["tally_dot_green"].clone().set_position(31, 0),
            sprites["tally_dot_yellow"].clone().set_position(40, 0),
            sprites["tally_dot_yellow"].clone().set_position(48, 0),
            sprites["pen_overlay"].clone().set_position(0, 0),
        ],
        grid_size=(64, 64),
        data={
            "step_budget": 80,
            "patroller_cycles": [
                # Phases 0..3 inside the witness pen; phases 4..7 at the
                # four playfield corners (outside the witness pen).
                [(28, 28), (28, 30), (30, 30), (30, 28),
                 (4,  4),  (4,  8),  (8,  8),  (8,  4) ],
                [(34, 28), (34, 30), (36, 30), (36, 28),
                 (4,  55), (4,  59), (8,  59), (8,  55)],
                [(28, 34), (28, 36), (30, 36), (30, 34),
                 (55, 4),  (55, 8),  (59, 8),  (59, 4) ],
            ],
        },
    ),
]

# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 5
PADDING_COLOR = 5

PLAYFIELD_TOP = 4
PLAYFIELD_BOTTOM = 58
MAX_POSTS = 8
MAX_STRIKES = 3

PEN_BOUNDARY_COLOR = 1
PEN_INTERIOR_COLOR = 2

STRIKE_SLOT_POSITIONS = [(50, 60), (56, 60), (60, 60)]


# ---------------------------------------------------------------------
# 4. CONVEX HULL + POINT-IN-POLYGON HELPERS
# ---------------------------------------------------------------------
def _convex_hull(points):
    pts = sorted(set((int(x), int(y)) for x, y in points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _point_in_polygon(px, py, polygon):
    n = len(polygon)
    if n < 3:
        return False
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if (yi > py) != (yj > py):
            denom = (yj - yi)
            if denom != 0:
                x_intersect = (xj - xi) * (py - yi) / denom + xi
                if px < x_intersect:
                    inside = not inside
        j = i
    return inside


def _draw_segment(pixels, x0, y0, x1, y1, color):
    h, w = pixels.shape
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        if 0 <= y0 < h and 0 <= x0 < w:
            pixels[y0, x0] = color
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


# ---------------------------------------------------------------------
# 5. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0):
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_current(self, current: int) -> None:
        self.current_steps = max(0, min(current, self.max_steps))

    def reset_to(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        ratio = self.current_steps / self.max_steps
        filled = round(64 * ratio)
        for x in range(64):
            frame[63, x] = 14 if x < filled else 5
        return frame


# ---------------------------------------------------------------------
# 6. THE GAME CLASS
# ---------------------------------------------------------------------
class Qm4t(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_ui = StepCounterHud(max_steps=0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        super().__init__(
            game_id="qm4t",
            levels=levels,
            camera=camera,
            available_actions=[5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        budget = level.get_data("step_budget") or 30
        self._max_steps = budget
        self._step_counter_ui.reset_to(budget)
        self._strikes = 0
        self._patroller_phase = 0

        cycles = level.get_data("patroller_cycles") or []
        self._patroller_cycles = list(cycles)
        self._patroller_sprites = level.get_sprites_by_tag("patroller")

        self._refresh_pen_overlay()

    # ---- internal helpers ----
    def _get_post_positions(self):
        return [(p.x, p.y) for p in self.current_level.get_sprites_by_tag("vertex_post")]

    def _get_pen_overlay(self):
        overlays = self.current_level.get_sprites_by_tag("pen_overlay")
        return overlays[0] if overlays else None

    def _refresh_pen_overlay(self):
        overlay = self._get_pen_overlay()
        if overlay is None:
            return
        pixels = np.full((64, 64), -1, dtype=np.int8)
        posts = self._get_post_positions()
        if len(posts) >= 3:
            hull = _convex_hull(posts)
            if len(hull) >= 3:
                for y in range(PLAYFIELD_TOP, PLAYFIELD_BOTTOM + 1):
                    for x in range(64):
                        if _point_in_polygon(x + 0.5, y + 0.5, hull):
                            pixels[y, x] = PEN_INTERIOR_COLOR
                for i in range(len(hull)):
                    x0, y0 = hull[i]
                    x1, y1 = hull[(i + 1) % len(hull)]
                    _draw_segment(pixels, x0, y0, x1, y1, PEN_BOUNDARY_COLOR)
        overlay.pixels = pixels

    def _sprite_centre(self, sprite: Sprite):
        h, w = sprite.pixels.shape
        return (sprite.x + w / 2.0, sprite.y + h / 2.0)

    def _is_in_playfield(self, gx: int, gy: int) -> bool:
        return PLAYFIELD_TOP <= gy <= PLAYFIELD_BOTTOM and 0 <= gx < 64

    def _post_at(self, gx: int, gy: int):
        for post in self.current_level.get_sprites_by_tag("vertex_post"):
            if post.x == gx and post.y <= gy < post.y + post.pixels.shape[0]:
                return post
        return None

    def _cell_blocked_for_post(self, gx: int, gy: int) -> bool:
        # Check if the 1x3 vertex_post at (gx, gy) would overlap a critter,
        # patroller, tally dot, strike marker, or another post.
        for sprite in self.current_level.get_sprites():
            if sprite.name == "pen_overlay":
                continue
            if sprite.name == "vertex_post":
                continue
            sh, sw = sprite.pixels.shape
            sx0, sy0 = sprite.x, sprite.y
            sx1, sy1 = sx0 + sw, sy0 + sh
            # Vertex post occupies (gx, gy..gy+2). Test overlap.
            if sx0 <= gx < sx1 and sy0 <= gy + 2 and sy1 > gy:
                return True
        return False

    def _add_strike(self) -> None:
        self._strikes += 1
        if self._strikes <= MAX_STRIKES:
            slot = self._strikes - 1
            x, y = STRIKE_SLOT_POSITIONS[slot]
            marker = sprites["strike_marker"].clone().set_position(x, y)
            self.current_level.add_sprite(marker)

    def _commit_pen(self) -> None:
        posts = self._get_post_positions()
        if len(posts) < 3:
            return
        hull = _convex_hull(posts)
        if len(hull) < 3:
            return

        # 1. Identify all enclosed critters and patrollers.
        to_remove = []
        for sprite in list(self.current_level.get_sprites()):
            if "critter" not in sprite.tags and "patroller" not in sprite.tags:
                continue
            cx, cy = self._sprite_centre(sprite)
            if _point_in_polygon(cx, cy, hull):
                to_remove.append(sprite)

        # 2. Resolve each capture: matching colour → tally; non-matching → strike.
        tally_green = self.current_level.get_sprites_by_tag("tally_green")
        tally_yellow = self.current_level.get_sprites_by_tag("tally_yellow")
        for sprite in to_remove:
            self.current_level.remove_sprite(sprite)
            if "critter_green" in sprite.tags and tally_green:
                self.current_level.remove_sprite(tally_green.pop())
            elif "critter_yellow" in sprite.tags and tally_yellow:
                self.current_level.remove_sprite(tally_yellow.pop())
            elif "patroller" in sprite.tags:
                self._add_strike()
                # Patroller removal also drops it from the tracked list.
                if sprite in self._patroller_sprites:
                    idx = self._patroller_sprites.index(sprite)
                    self._patroller_sprites.pop(idx)
                    if idx < len(self._patroller_cycles):
                        self._patroller_cycles.pop(idx)
            else:
                # Captured a non-target critter (e.g. maroon) or a green/yellow
                # whose tally row is already empty (an over-capture).
                self._add_strike()

        # 3. Clear all posts.
        for post in list(self.current_level.get_sprites_by_tag("vertex_post")):
            self.current_level.remove_sprite(post)

    def _advance_patrollers(self) -> None:
        if not self._patroller_sprites:
            return
        self._patroller_phase = (self._patroller_phase + 1) % 8
        for sprite, cycle in zip(self._patroller_sprites, self._patroller_cycles):
            if not cycle:
                continue
            x, y = cycle[self._patroller_phase % len(cycle)]
            sprite.set_position(x, y)

    def _check_terminal(self) -> bool:
        if self._strikes >= MAX_STRIKES:
            self.lose()
            return True
        if self._step_counter_ui.current_steps <= 0:
            self.lose()
            return True
        if not self.current_level.get_sprites_by_tag("tally"):
            self.next_level()
            return True
        return False

    # ---- engine entrypoint ----
    def step(self) -> None:
        action_id = self.action.id

        if action_id == GameAction.ACTION6:
            click_x = int(self.action.data.get("x", 0))
            click_y = int(self.action.data.get("y", 0))
            grid = self.camera.display_to_grid(click_x, click_y)
            if grid is not None:
                gx, gy = grid
                existing_post = self._post_at(gx, gy)
                if existing_post is not None:
                    self.current_level.remove_sprite(existing_post)
                else:
                    if (
                        self._is_in_playfield(gx, gy)
                        and len(self._get_post_positions()) < MAX_POSTS
                        and not self._cell_blocked_for_post(gx, gy)
                    ):
                        new_post = sprites["vertex_post"].clone().set_position(gx, gy)
                        self.current_level.add_sprite(new_post)
        elif action_id == GameAction.ACTION5:
            self._commit_pen()

        # Advance patrollers AFTER any commit / placement so the new positions
        # influence the next frame's state visually.
        self._advance_patrollers()

        # Tick the step counter.
        self._step_counter_ui.set_current(self._step_counter_ui.current_steps - 1)

        # Recompute the pen overlay for the new state.
        self._refresh_pen_overlay()

        # Resolve terminal conditions.
        self._check_terminal()

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._step_counter_ui.current_steps
        state[0, 1] = self._strikes
        state[0, 2] = self._patroller_phase
        state[0, 3] = len(self._get_post_positions())
        return state
