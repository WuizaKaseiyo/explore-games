"""bz3k."""

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
# CONSTANTS
# ---------------------------------------------------------------------

GRID = 64
BORDER = 4

BACKGROUND_COLOR = 0
PADDING_COLOR = 1

# Palette references
WALL_DARK = 4
WALL_TEXTURE = 3
PLAYER_BODY = 12
PLAYER_OUTLINE = 4
PLAYER_SPECK = 2
TARGET_RING = 11
TARGET_INNER = 0
HAZARD_OUTER = 13
HAZARD_INNER = 4
CAP_BORDER = 4
CAP_BODY = 11
FLIPPER_BG = 15
FLIPPER_PATTERN = 6
FLIPPER_BORDER = 4
WAKE_COLOR = 13

STEP_HUD_BG = 5
STEP_HUD_FG = 14

VEL_DOT_COLOR = 12

# Sprite size convention: gameplay sprites are 5x5; logical position
# is the sprite's center cell (top-left + (2, 2)).
SPRITE_SIZE = 5
LOGICAL_OFFSET = 2


# ---------------------------------------------------------------------
# SPRITE PIXEL PATTERNS
# ---------------------------------------------------------------------

PLAYER_PATTERN = [
    [-1,            PLAYER_OUTLINE, PLAYER_OUTLINE, PLAYER_OUTLINE, -1],
    [PLAYER_OUTLINE, PLAYER_SPECK,  PLAYER_BODY,    PLAYER_BODY,    PLAYER_OUTLINE],
    [PLAYER_OUTLINE, PLAYER_BODY,   PLAYER_BODY,    PLAYER_BODY,    PLAYER_OUTLINE],
    [PLAYER_OUTLINE, PLAYER_BODY,   PLAYER_BODY,    PLAYER_BODY,    PLAYER_OUTLINE],
    [-1,            PLAYER_OUTLINE, PLAYER_BODY,    PLAYER_OUTLINE, -1],
]

TARGET_PATTERN = [
    [TARGET_RING, TARGET_RING,  TARGET_RING,  TARGET_RING,  TARGET_RING],
    [TARGET_RING, TARGET_INNER, TARGET_INNER, TARGET_INNER, TARGET_RING],
    [TARGET_RING, TARGET_INNER, TARGET_RING,  TARGET_INNER, TARGET_RING],
    [TARGET_RING, TARGET_INNER, TARGET_INNER, TARGET_INNER, TARGET_RING],
    [TARGET_RING, TARGET_RING,  TARGET_RING,  TARGET_RING,  TARGET_RING],
]

HAZARD_PATTERN = [
    [HAZARD_OUTER, HAZARD_OUTER, HAZARD_INNER, HAZARD_OUTER, HAZARD_OUTER],
    [HAZARD_OUTER, HAZARD_INNER, HAZARD_OUTER, HAZARD_INNER, HAZARD_OUTER],
    [HAZARD_INNER, HAZARD_OUTER, HAZARD_OUTER, HAZARD_OUTER, HAZARD_INNER],
    [HAZARD_OUTER, HAZARD_INNER, HAZARD_OUTER, HAZARD_INNER, HAZARD_OUTER],
    [HAZARD_OUTER, HAZARD_OUTER, HAZARD_INNER, HAZARD_OUTER, HAZARD_OUTER],
]

CAP_BAND_PATTERN = [
    [CAP_BORDER, CAP_BORDER, CAP_BORDER, CAP_BORDER, CAP_BORDER],
    [CAP_BODY,   CAP_BODY,   CAP_BODY,   CAP_BODY,   CAP_BODY],
    [CAP_BODY,   CAP_BORDER, CAP_BODY,   CAP_BORDER, CAP_BODY],
    [CAP_BODY,   CAP_BODY,   CAP_BODY,   CAP_BODY,   CAP_BODY],
    [CAP_BORDER, CAP_BORDER, CAP_BORDER, CAP_BORDER, CAP_BORDER],
]

# Bowtie: two facing triangles meeting at center.
FLIPPER_PATTERN_PIXELS = [
    [FLIPPER_BORDER, FLIPPER_BORDER,  FLIPPER_BORDER,  FLIPPER_BORDER,  FLIPPER_BORDER],
    [FLIPPER_PATTERN, FLIPPER_BG,     FLIPPER_BG,      FLIPPER_BG,      FLIPPER_PATTERN],
    [FLIPPER_PATTERN, FLIPPER_PATTERN, FLIPPER_BG,     FLIPPER_PATTERN, FLIPPER_PATTERN],
    [FLIPPER_PATTERN, FLIPPER_BG,     FLIPPER_BG,      FLIPPER_BG,      FLIPPER_PATTERN],
    [FLIPPER_BORDER, FLIPPER_BORDER,  FLIPPER_BORDER,  FLIPPER_BORDER,  FLIPPER_BORDER],
]

WAKE_PATTERN = [[WAKE_COLOR]]


# ---------------------------------------------------------------------
# SPRITE BANK
# ---------------------------------------------------------------------

sprites = {
    "player": Sprite(
        pixels=PLAYER_PATTERN,
        name="player",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=3,
    ),
    "target": Sprite(
        pixels=TARGET_PATTERN,
        name="target",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target"],
        layer=1,
    ),
    "cap_band": Sprite(
        pixels=CAP_BAND_PATTERN,
        name="cap_band",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["cap_band"],
        layer=1,
    ),
    "flipper_plate": Sprite(
        pixels=FLIPPER_PATTERN_PIXELS,
        name="flipper_plate",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["flipper"],
        layer=1,
    ),
    "wake_pixel": Sprite(
        pixels=WAKE_PATTERN,
        name="wake_pixel",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["wake"],
        layer=0,
    ),
}


# ---------------------------------------------------------------------
# WALL FACTORY
# ---------------------------------------------------------------------

def _make_wall(width: int, height: int, name: str = "wall") -> Sprite:
    """Build a wall rectangle with a brick-texture pattern."""
    pixels = []
    for j in range(height):
        row = []
        for i in range(width):
            if (j % 4 == 3) or (i % 6 == 5 and j % 4 != 0):
                row.append(WALL_TEXTURE)
            else:
                row.append(WALL_DARK)
        pixels.append(row)
    return Sprite(
        pixels=pixels,
        name=name,
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    )


def _make_hazard_strip(width: int, height: int, name: str = "hazard") -> Sprite:
    """Build a hazard rectangle of given size by tiling the 5x5 pattern."""
    pixels = []
    for j in range(height):
        row = []
        for i in range(width):
            row.append(HAZARD_PATTERN[j % SPRITE_SIZE][i % SPRITE_SIZE])
        pixels.append(row)
    return Sprite(
        pixels=pixels,
        name=name,
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["hazard"],
        layer=2,
    )


# ---------------------------------------------------------------------
# LEVEL BUILDERS
# ---------------------------------------------------------------------

def _boundary_walls():
    """Four boundary wall sprites covering the 4-pixel-thick frame."""
    walls = []
    walls.append(_make_wall(GRID, BORDER, "wall_top").set_position(0, 0))
    walls.append(_make_wall(GRID, BORDER, "wall_bottom").set_position(0, GRID - BORDER))
    walls.append(_make_wall(BORDER, GRID - 2 * BORDER, "wall_left").set_position(0, BORDER))
    walls.append(_make_wall(BORDER, GRID - 2 * BORDER, "wall_right").set_position(GRID - BORDER, BORDER))
    return walls


def _build_level_1() -> Level:
    """Open arena, single target."""
    s = []
    s.extend(_boundary_walls())
    s.append(sprites["target"].clone().set_position(31, 30))
    s.append(sprites["player"].clone().set_position(6, 30))
    return Level(
        sprites=s,
        grid_size=(GRID, GRID),
        data={
            "step_budget": 30,
            "avatar_start_x": 6,
            "avatar_start_y": 30,
            "avatar_start_vx": 0,
            "avatar_start_vy": 0,
        },
    )


def _build_level_2() -> Level:
    """Internal wall column with single passage; avatar starts off-axis so it must turn."""
    s = []
    s.extend(_boundary_walls())
    # Internal wall column: 5 cells wide at x=[30..34], split by 5-row gap at y=[30..34].
    upper = _make_wall(SPRITE_SIZE, 26, "wall_internal_upper").set_position(30, BORDER)
    lower = _make_wall(SPRITE_SIZE, 25, "wall_internal_lower").set_position(30, 35)
    s.append(upper)
    s.append(lower)
    # Cap-band fills the gap (center (32, 32)).
    s.append(sprites["cap_band"].clone().set_position(30, 30))
    # Target near east wall, same y as the gap.
    s.append(sprites["target"].clone().set_position(55, 30))
    # Avatar starts south of the gap, so the player must turn (build vy) to line up
    # with the wall-column passage before drifting east through the cap-band.
    s.append(sprites["player"].clone().set_position(6, 42))
    return Level(
        sprites=s,
        grid_size=(GRID, GRID),
        data={
            "step_budget": 60,
            "avatar_start_x": 6,
            "avatar_start_y": 42,
            "avatar_start_vx": 0,
            "avatar_start_vy": 0,
        },
    )


def _build_level_3() -> Level:
    """Open arena with many sparse obstacle blocks. The avatar must drift east through the cap-band, detour vertically around a central blocker, then re-align onto the target."""
    s = []
    s.extend(_boundary_walls())
    # One central blocker sitting on the direct east path between cap and target.
    # Top-left (38, 28), 8x8 → bounding box x ∈ [38, 45], y ∈ [28, 35]; this overlaps
    # the avatar's natural y=30..34 row, so the player must shift vertically to pass.
    s.append(_make_wall(8, 8, "wall_central_blocker").set_position(38, 28))
    # Sparse decorative obstacle blocks scattered around the arena (same wall UI).
    # All are off the y=30..34 corridor so they shape the visual openness without
    # forming an additional barrier; the player can route past any of them.
    s.append(_make_wall(5, 5, "wall_obs_a").set_position(12, 10))
    s.append(_make_wall(5, 5, "wall_obs_b").set_position(26, 8))
    s.append(_make_wall(5, 5, "wall_obs_c").set_position(50, 12))
    s.append(_make_wall(5, 5, "wall_obs_d").set_position(12, 48))
    s.append(_make_wall(5, 5, "wall_obs_e").set_position(26, 50))
    s.append(_make_wall(5, 5, "wall_obs_f").set_position(50, 46))
    s.append(_make_wall(5, 5, "wall_obs_g").set_position(20, 18))
    s.append(_make_wall(5, 5, "wall_obs_h").set_position(20, 42))
    # Cap-band on the direct east path: center (28, 32) → top-left (26, 30).
    s.append(sprites["cap_band"].clone().set_position(26, 30))
    # Target at the right side, same row as the avatar's start.
    s.append(sprites["target"].clone().set_position(53, 30))
    # Avatar at the left side.
    s.append(sprites["player"].clone().set_position(6, 30))
    return Level(
        sprites=s,
        grid_size=(GRID, GRID),
        data={
            "step_budget": 60,
            "avatar_start_x": 6,
            "avatar_start_y": 30,
            "avatar_start_vx": 0,
            "avatar_start_vy": 0,
        },
    )


levels = [_build_level_1(), _build_level_2(), _build_level_3()]


# ---------------------------------------------------------------------
# HUD WIDGETS
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    """A horizontal depleting bar at the bottom row of the frame."""

    def __init__(self, max_steps: int) -> None:
        self.max_steps = max(1, max_steps)
        self.current = self.max_steps

    def set_current(self, current: int) -> None:
        self.current = max(0, min(current, self.max_steps))

    def set_max(self, max_steps: int) -> None:
        self.max_steps = max(1, max_steps)
        self.current = self.max_steps

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        ratio = self.current / self.max_steps
        filled = int(round(GRID * ratio))
        for x in range(GRID):
            frame[GRID - 1, x] = STEP_HUD_FG if x < filled else STEP_HUD_BG
        return frame


class VelocityDotHud(RenderableUserDisplay):
    """A 4x4 patch in the top-right corner showing (vx, vy) as a dot-cross."""

    def __init__(self) -> None:
        self.vx = 0
        self.vy = 0

    def set_velocity(self, vx: int, vy: int) -> None:
        self.vx = vx
        self.vy = vy

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        # Patch occupies rows 0..3, cols 60..63.
        cx = 61  # patch center col
        cy = 1   # patch center row
        # Clear the patch to background.
        for r in range(4):
            for c in range(4):
                frame[r, 60 + c] = BACKGROUND_COLOR
        # Anchor pixel at center.
        frame[cy, cx] = VEL_DOT_COLOR
        # Horizontal extent for vx.
        n_x = min(abs(self.vx), 2)
        for k in range(1, n_x + 1):
            col = cx + (k if self.vx > 0 else -k)
            if 60 <= col < 64:
                frame[cy, col] = VEL_DOT_COLOR
        # Vertical extent for vy.
        n_y = min(abs(self.vy), 2)
        for k in range(1, n_y + 1):
            row = cy + (k if self.vy > 0 else -k)
            if 0 <= row < 4:
                frame[row, cx] = VEL_DOT_COLOR
        return frame


# ---------------------------------------------------------------------
# THE GAME CLASS
# ---------------------------------------------------------------------

class Bz3k(NovaBaseGame):
    def __init__(self) -> None:
        self.step_hud = StepCounterHud(30)
        self.velocity_hud = VelocityDotHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_hud, self.velocity_hud],
        )
        # Per-game state.
        self.vx = 0
        self.vy = 0
        self.player_sprite: Sprite | None = None
        self.wake_sprites: list[Sprite] = []
        self.hazard_pending = False
        super().__init__(
            game_id="bz3k",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    # -----------------------------------------------------------------
    # Lifecycle hooks
    # -----------------------------------------------------------------

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (GRID, GRID)
        self.camera.width = gw
        self.camera.height = gh
        # Reset per-level state from level data.
        self.vx = level.get_data("avatar_start_vx") or 0
        self.vy = level.get_data("avatar_start_vy") or 0
        sx = level.get_data("avatar_start_x")
        sy = level.get_data("avatar_start_y")
        # Find player sprite for this level.
        players = level.get_sprites_by_tag("player")
        if players:
            self.player_sprite = players[0]
            if sx is not None and sy is not None:
                self.player_sprite.set_position(sx, sy)
        # Reset HUD.
        budget = level.get_data("step_budget") or 30
        self.step_hud.set_max(budget)
        self.step_hud.set_current(budget)
        self.velocity_hud.set_velocity(self.vx, self.vy)
        # Clear any prior wake sprites.
        self._clear_wake_sprites()
        self.hazard_pending = False

    # -----------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------

    def _avatar_center(self) -> tuple[int, int]:
        if self.player_sprite is None:
            return (0, 0)
        return (self.player_sprite.x + LOGICAL_OFFSET, self.player_sprite.y + LOGICAL_OFFSET)

    def _can_step_to(self, new_x: int, new_y: int) -> bool:
        """Return True iff the player sprite can occupy top-left (new_x, new_y) without wall overlap."""
        if self.player_sprite is None:
            return False
        # Bounds check.
        if new_x < 0 or new_y < 0:
            return False
        if new_x + SPRITE_SIZE > GRID or new_y + SPRITE_SIZE > GRID:
            return False
        # Wall collision via temporary placement + collides_with.
        old_x, old_y = self.player_sprite.x, self.player_sprite.y
        self.player_sprite.set_position(new_x, new_y)
        walls = self.current_level.get_sprites_by_tag("wall")
        blocked = any(self.player_sprite.collides_with(w) for w in walls)
        self.player_sprite.set_position(old_x, old_y)
        return not blocked

    def _check_trigger_at_center(self, gx: int, gy: int) -> str | None:
        """Return 'cap', 'flipper', 'hazard', or 'target' if the avatar's center cell coincides with such a sprite, else None."""
        # Single-cell sprite checks via center alignment.
        for tag, kind in (("cap_band", "cap"), ("flipper", "flipper"), ("target", "target")):
            for s in self.current_level.get_sprites_by_tag(tag):
                if s.x + LOGICAL_OFFSET == gx and s.y + LOGICAL_OFFSET == gy:
                    return kind
        # Hazard rectangle check (multi-cell).
        for s in self.current_level.get_sprites_by_tag("hazard"):
            arr = np.asarray(s.pixels)
            if arr.ndim != 2:
                continue
            sh, sw = arr.shape
            if s.x <= gx < s.x + sw and s.y <= gy < s.y + sh:
                px = int(arr[gy - s.y][gx - s.x])
                if px >= 0:
                    return "hazard"
        return None

    def _slide_axis(self, axis: str) -> None:
        """Slide the avatar one cell at a time along `axis` ('x' or 'y') by the matching velocity component."""
        if self.player_sprite is None:
            return
        v = self.vx if axis == "x" else self.vy
        if v == 0:
            return
        direction = 1 if v > 0 else -1
        steps = abs(v)
        for _ in range(steps):
            if axis == "x":
                new_x = self.player_sprite.x + direction
                new_y = self.player_sprite.y
            else:
                new_x = self.player_sprite.x
                new_y = self.player_sprite.y + direction
            if not self._can_step_to(new_x, new_y):
                # Wall collision: stop on this axis.
                if axis == "x":
                    self.vx = 0
                else:
                    self.vy = 0
                return
            self.player_sprite.set_position(new_x, new_y)
            cx, cy = self._avatar_center()
            trigger = self._check_trigger_at_center(cx, cy)
            if trigger == "cap":
                if axis == "x":
                    self.vx = 1 if self.vx > 0 else -1 if self.vx < 0 else 0
                else:
                    self.vy = 1 if self.vy > 0 else -1 if self.vy < 0 else 0
                return
            if trigger == "flipper":
                self.vx = -self.vx
                self.vy = -self.vy
                return
            if trigger == "hazard":
                self.hazard_pending = True
                return
            # Target trigger is checked at end-of-step, not here.

    def _rebuild_wake(self) -> None:
        """Remove any existing wake_pixel sprites and place new ones based on current velocity."""
        self._clear_wake_sprites()
        if self.player_sprite is None:
            return
        cx, cy = self._avatar_center()
        magnitude = abs(self.vx) + abs(self.vy)
        if magnitude == 0:
            return
        # Wake fans behind the avatar opposite to the velocity vector.
        # For each non-zero component, place |v| pixels in -direction along that axis.
        if self.vx != 0:
            step = -1 if self.vx > 0 else 1
            for k in range(1, abs(self.vx) + 1):
                wx = cx + step * (k + LOGICAL_OFFSET)
                wy = cy
                if 0 <= wx < GRID and 0 <= wy < GRID:
                    w = sprites["wake_pixel"].clone().set_position(wx, wy)
                    self.current_level.add_sprite(w)
                    self.wake_sprites.append(w)
        if self.vy != 0:
            step = -1 if self.vy > 0 else 1
            for k in range(1, abs(self.vy) + 1):
                wx = cx
                wy = cy + step * (k + LOGICAL_OFFSET)
                if 0 <= wx < GRID and 0 <= wy < GRID:
                    w = sprites["wake_pixel"].clone().set_position(wx, wy)
                    self.current_level.add_sprite(w)
                    self.wake_sprites.append(w)

    def _clear_wake_sprites(self) -> None:
        for w in self.wake_sprites:
            try:
                self.current_level.remove_sprite(w)
            except Exception:
                pass
        self.wake_sprites = []

    # -----------------------------------------------------------------
    # Step
    # -----------------------------------------------------------------

    def step(self) -> None:
        # Clear wake from previous turn before any motion.
        self._clear_wake_sprites()

        # Apply impulse.
        if self.action.id == GameAction.ACTION1:
            self.vy -= 1
        elif self.action.id == GameAction.ACTION2:
            self.vy += 1
        elif self.action.id == GameAction.ACTION3:
            self.vx -= 1
        elif self.action.id == GameAction.ACTION4:
            self.vx += 1

        # Slide horizontally then vertically.
        self.hazard_pending = False
        self._slide_axis("x")
        if not self.hazard_pending:
            self._slide_axis("y")

        # Rebuild wake to surface velocity.
        self._rebuild_wake()
        self.velocity_hud.set_velocity(self.vx, self.vy)

        # Update step counter HUD.
        budget = self.current_level.get_data("step_budget") or 0
        remaining = max(0, budget - (self._action_count + 1))
        self.step_hud.set_current(remaining)

        # Check hazard contact.
        if self.hazard_pending:
            self.lose()
            self.complete_action()
            return

        # Check target latch (speed-zero arrival).
        cx, cy = self._avatar_center()
        if self.vx == 0 and self.vy == 0:
            for t in self.current_level.get_sprites_by_tag("target"):
                if t.x + LOGICAL_OFFSET == cx and t.y + LOGICAL_OFFSET == cy:
                    self.next_level()
                    self.complete_action()
                    return

        # Check budget exhaustion.
        if (self._action_count + 1) >= budget:
            self.lose()
            self.complete_action()
            return

        self.complete_action()

    # -----------------------------------------------------------------
    # Required engine hooks
    # -----------------------------------------------------------------

    def _get_hidden_state(self) -> np.ndarray:
        # Expose (vx, vy) so the engine's graph-identity hashing distinguishes velocity states.
        return np.array([[self.vx, self.vy]], dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
