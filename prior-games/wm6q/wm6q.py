"""wm6q — generated game (3 levels)."""

from typing import Optional

import numpy as np

from novaengine import (
    NovaBaseGame,
    Camera,
    GameAction,
    Level,
    RenderableUserDisplay,
    Sprite,
)

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 2          # light grey
PADDING_COLOR = 4             # off-black

INNER_REGULAR = 1             # off-white inner area for regular tiles
INNER_LOCKED = 4              # off-black filled square for locked tiles
INNER_LINKED_RING = 15        # purple ring for linked tiles
INNER_LINKED_FILL = 1         # off-white interior of linked ring

STEP_BAR_ACTIVE = 11          # yellow
STEP_BAR_DEPLETED = 5         # black

EDGE_COLORS = (8, 9, 11, 14)  # red, blue, yellow, green — palette for tile edges

TILE_SIZE = 16                # 16×16 display pixels per tile
EDGE_BAND_WIDTH = 3           # 3 px-wide colour bands at each edge
GLYPH_OFFSET = 5              # inner glyph occupies rows/cols 5..10 (6×6)
GLYPH_END = 11

GRID_W = 64
GRID_H = 64


# ---------------------------------------------------------------------
# Tile painting helper
# ---------------------------------------------------------------------
def _paint_tile_pixels(
    base: tuple[int, int, int, int],
    rotation: int,
    glyph: str,
) -> np.ndarray:
    """Return a 16x16 list-of-lists pixel array for a tile.

    `base` is `(T0, R0, B0, L0)` — palette values for the tile's four edges
    when at rotation 0. `rotation` ∈ {0, 1, 2, 3} cycles the assignment 90°
    CW per step, per the convention documented in mechanic-spec §4.
    `glyph` ∈ {"regular", "locked", "linked"} controls the inner 10x10 area.
    """
    t0, r0, b0, l0 = base
    if rotation == 0:
        top, right, bottom, left = t0, r0, b0, l0
    elif rotation == 1:
        top, right, bottom, left = l0, t0, r0, b0
    elif rotation == 2:
        top, right, bottom, left = b0, l0, t0, r0
    else:  # rotation == 3
        top, right, bottom, left = r0, b0, l0, t0

    # Start with inner-area fill colour
    if glyph == "regular":
        inner = INNER_REGULAR
    elif glyph == "locked":
        inner = INNER_REGULAR  # background of inner area; lock glyph painted over
    else:  # "linked"
        inner = INNER_REGULAR

    pixels = np.full((TILE_SIZE, TILE_SIZE), inner, dtype=np.int16)

    # Top / bottom edge bands span the full width, taking precedence at corners.
    pixels[:EDGE_BAND_WIDTH, :] = top
    pixels[TILE_SIZE - EDGE_BAND_WIDTH:, :] = bottom
    # Left / right bands only fill the middle rows so the corner colours come
    # from top/bottom bands above.
    pixels[EDGE_BAND_WIDTH:TILE_SIZE - EDGE_BAND_WIDTH, :EDGE_BAND_WIDTH] = left
    pixels[EDGE_BAND_WIDTH:TILE_SIZE - EDGE_BAND_WIDTH, TILE_SIZE - EDGE_BAND_WIDTH:] = right

    if glyph == "locked":
        # 6x6 solid black square at rows 5..10, cols 5..10
        pixels[GLYPH_OFFSET:GLYPH_END, GLYPH_OFFSET:GLYPH_END] = INNER_LOCKED
    elif glyph == "linked":
        # 6x6 ring outline (purple) with off-white interior
        pixels[GLYPH_OFFSET:GLYPH_END, GLYPH_OFFSET:GLYPH_END] = INNER_LINKED_FILL
        pixels[GLYPH_OFFSET, GLYPH_OFFSET:GLYPH_END] = INNER_LINKED_RING
        pixels[GLYPH_END - 1, GLYPH_OFFSET:GLYPH_END] = INNER_LINKED_RING
        pixels[GLYPH_OFFSET:GLYPH_END, GLYPH_OFFSET] = INNER_LINKED_RING
        pixels[GLYPH_OFFSET:GLYPH_END, GLYPH_END - 1] = INNER_LINKED_RING

    return pixels


def _placeholder_tile_pixels() -> np.ndarray:
    """A neutral 16x16 placeholder for sprite construction (overwritten in
    `on_set_level`)."""
    return np.full((TILE_SIZE, TILE_SIZE), BACKGROUND_COLOR, dtype=np.int16)


# ---------------------------------------------------------------------
# Sprite factory
# ---------------------------------------------------------------------
def _make_tile_sprite(name: str, glyph: str) -> Sprite:
    extra_tags = []
    if glyph == "locked":
        extra_tags.append("locked")
    elif glyph == "linked":
        extra_tags.append("linked")
    else:
        extra_tags.append("regular")
    return Sprite(
        pixels=_placeholder_tile_pixels(),
        name=name,
        visible=True,
        collidable=True,
        tags=["tile", *extra_tags],
    )


# ---------------------------------------------------------------------
# Level data tables
# ---------------------------------------------------------------------
# Level 1: 2 regular tiles in a row
LEVEL_1_TILES = {
    # name: (col, row, base T0/R0/B0/L0, glyph, linked_partner)
    "l1_a": ((16, 24), (8, 9, 14, 11), "regular", None),
    "l1_b": ((32, 24), (8, 9, 14, 11), "regular", None),
}
LEVEL_1_INITIAL_R = {"l1_a": 0, "l1_b": 0}
LEVEL_1_BUDGET = 12

# Level 2: 2x2, lock at (0,0)
LEVEL_2_TILES = {
    "l2_00": ((16, 8),  (8, 9, 14, 11),  "locked",  None),
    "l2_10": ((32, 8),  (8, 9, 11, 14),  "regular", None),
    "l2_01": ((16, 24), (9, 14, 11, 8),  "regular", None),
    "l2_11": ((32, 24), (8, 9, 14, 11),  "regular", None),
}
LEVEL_2_INITIAL_R = {n: 0 for n in LEVEL_2_TILES}
LEVEL_2_BUDGET = 25

# Level 3: 3x3, lock at (1,1), linked pair at (0,0) and (2,2)
LEVEL_3_TILES = {
    "l3_00": ((8,  8),  (14, 8,  9,  11), "linked",  "l3_22"),
    "l3_10": ((24, 8),  (9,  8,  11, 14), "regular", None),
    "l3_20": ((40, 8),  (8,  14, 9,  11), "regular", None),
    "l3_01": ((8,  24), (11, 9,  8,  14), "regular", None),
    "l3_11": ((24, 24), (8,  9,  14, 11), "locked",  None),
    "l3_21": ((40, 24), (8,  11, 9,  14), "regular", None),
    "l3_02": ((8,  40), (8,  14, 11, 9),  "regular", None),
    "l3_12": ((24, 40), (9,  11, 8,  14), "regular", None),
    "l3_22": ((40, 40), (8,  9,  11, 14), "linked",  "l3_00"),
}
LEVEL_3_INITIAL_R = {n: 0 for n in LEVEL_3_TILES}
LEVEL_3_BUDGET = 50

# Compose level sprite lists.
level_1_sprites = [_make_tile_sprite(name, meta[2]) for name, meta in LEVEL_1_TILES.items()]
level_2_sprites = [_make_tile_sprite(name, meta[2]) for name, meta in LEVEL_2_TILES.items()]
level_3_sprites = [_make_tile_sprite(name, meta[2]) for name, meta in LEVEL_3_TILES.items()]


# ---------------------------------------------------------------------
# Level objects
# ---------------------------------------------------------------------
levels = [
    Level(
        sprites=level_1_sprites,
        grid_size=(GRID_W, GRID_H),
        data={
            "step_budget": LEVEL_1_BUDGET,
            "tile_table": LEVEL_1_TILES,
            "initial_r": LEVEL_1_INITIAL_R,
        },
    ),
    Level(
        sprites=level_2_sprites,
        grid_size=(GRID_W, GRID_H),
        data={
            "step_budget": LEVEL_2_BUDGET,
            "tile_table": LEVEL_2_TILES,
            "initial_r": LEVEL_2_INITIAL_R,
        },
    ),
    Level(
        sprites=level_3_sprites,
        grid_size=(GRID_W, GRID_H),
        data={
            "step_budget": LEVEL_3_BUDGET,
            "tile_table": LEVEL_3_TILES,
            "initial_r": LEVEL_3_INITIAL_R,
        },
    ),
]


# ---------------------------------------------------------------------
# HUD
# ---------------------------------------------------------------------
class StepBarHud(RenderableUserDisplay):
    """Single-row depleting bar at frame row 63."""

    def __init__(self) -> None:
        self._max = 1
        self._current = 0

    def set_state(self, max_steps: int, used: int) -> None:
        self._max = max(1, max_steps)
        self._current = max(0, max_steps - used)

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        ratio = self._current / self._max
        active_cells = int(round(ratio * GRID_W))
        active_cells = max(0, min(GRID_W, active_cells))
        for x in range(GRID_W):
            frame[GRID_H - 1, x] = STEP_BAR_ACTIVE if x < active_cells else STEP_BAR_DEPLETED
        return frame


# ---------------------------------------------------------------------
# Game
# ---------------------------------------------------------------------
class Wm6q(NovaBaseGame):
    def __init__(self) -> None:
        self._step_bar_hud = StepBarHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_bar_hud],
        )
        super().__init__(
            game_id="wm6q",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )
        self._tile_rotations: dict[str, int] = {}
        self._tile_meta: dict[str, dict] = {}
        self._steps_used: int = 0

    # -- per-level setup --------------------------------------------------
    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (GRID_W, GRID_H)
        self.camera.width = gw
        self.camera.height = gh

        tile_table = level.get_data("tile_table")
        initial_r = level.get_data("initial_r")
        budget = level.get_data("step_budget")

        self._tile_rotations = {}
        self._tile_meta = {}
        self._steps_used = 0

        # Position each tile sprite + paint pixels for initial rotation.
        for sprite in level.get_sprites_by_tag("tile"):
            name = sprite.name
            (px, py), base, glyph, linked_partner = tile_table[name]
            r0 = initial_r.get(name, 0)
            sprite.set_position(px, py)
            sprite.pixels = _paint_tile_pixels(base, r0, glyph)
            self._tile_rotations[name] = r0
            self._tile_meta[name] = {
                "pixel_origin": (px, py),
                "base": base,
                "glyph": glyph,
                "linked_partner": linked_partner,
            }

        self._step_bar_hud.set_state(budget, 0)

    # -- step dispatch ----------------------------------------------------
    def step(self) -> None:
        if self.action.id == GameAction.ACTION6:
            data = self.action.data or {}
            x = int(data.get("x", -1))
            y = int(data.get("y", -1))
            handled = self._handle_click(x, y)
            if handled:
                self._steps_used += 1
                self._update_hud_and_terminal()
        self.complete_action()

    # -- click resolution -------------------------------------------------
    def _handle_click(self, display_x: int, display_y: int) -> bool:
        """Return True if the click rotated some tile (i.e. counts as a step)."""
        target = self._tile_at_display(display_x, display_y)
        if target is None:
            return False
        meta = self._tile_meta[target]
        if meta["glyph"] == "locked":
            return False  # no rotation, no step charged
        # Rotate this tile + its linked partner if any.
        self._rotate_tile(target)
        partner = meta["linked_partner"]
        if partner is not None:
            self._rotate_tile(partner)
        return True

    def _tile_at_display(self, display_x: int, display_y: int) -> Optional[str]:
        gx, gy = self.camera.display_to_grid(display_x, display_y) or (-1, -1)
        for name, meta in self._tile_meta.items():
            ox, oy = meta["pixel_origin"]
            if ox <= gx < ox + TILE_SIZE and oy <= gy < oy + TILE_SIZE:
                return name
        return None

    def _rotate_tile(self, name: str) -> None:
        new_r = (self._tile_rotations[name] + 1) % 4
        self._tile_rotations[name] = new_r
        meta = self._tile_meta[name]
        sprite_list = self.current_level.get_sprites_by_name(name)
        if not sprite_list:
            return
        sprite = sprite_list[0]
        sprite.pixels = _paint_tile_pixels(meta["base"], new_r, meta["glyph"])

    # -- win / lose -------------------------------------------------------
    def _update_hud_and_terminal(self) -> None:
        budget = self.current_level.get_data("step_budget")
        self._step_bar_hud.set_state(budget, self._steps_used)
        if self._check_win():
            self.next_level()
            return
        if self._steps_used >= budget:
            self.lose()

    def _check_win(self) -> bool:
        """Every internal grid edge between adjacent tiles must carry the
        same colour on both sides."""
        # Build a (col, row) → name index. Each tile occupies a 16x16 block;
        # use its pixel_origin as the grid identity.
        by_origin = {}
        for name, meta in self._tile_meta.items():
            by_origin[meta["pixel_origin"]] = name
        # For each tile, check right and bottom neighbours (if any).
        for (ox, oy), name in by_origin.items():
            right_origin = (ox + TILE_SIZE, oy)
            bottom_origin = (ox, oy + TILE_SIZE)
            if right_origin in by_origin:
                right_name = by_origin[right_origin]
                if self._edge_color(name, "right") != self._edge_color(right_name, "left"):
                    return False
            if bottom_origin in by_origin:
                bottom_name = by_origin[bottom_origin]
                if self._edge_color(name, "bottom") != self._edge_color(bottom_name, "top"):
                    return False
        return True

    def _edge_color(self, name: str, side: str) -> int:
        meta = self._tile_meta[name]
        t0, r0, b0, l0 = meta["base"]
        rot = self._tile_rotations[name]
        if rot == 0:
            top, right, bottom, left = t0, r0, b0, l0
        elif rot == 1:
            top, right, bottom, left = l0, t0, r0, b0
        elif rot == 2:
            top, right, bottom, left = b0, l0, t0, r0
        else:
            top, right, bottom, left = r0, b0, l0, t0
        return {"top": top, "right": right, "bottom": bottom, "left": left}[side]

    # -- engine debug hook ------------------------------------------------
    def _get_hidden_state(self) -> np.ndarray:
        # Pack rotations of all tiles in current level into a 1D array.
        if not self._tile_rotations:
            return np.zeros((1, 1), dtype=np.int16)
        rotations = sorted(self._tile_rotations.items())
        arr = np.array([[r for _, r in rotations]], dtype=np.int16)
        return arr

    def _get_valid_actions(self):
        return super()._get_valid_actions()
