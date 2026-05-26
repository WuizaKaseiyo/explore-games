"""qy7w — generated game (mechanic intentionally undocumented)."""

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

# Palette legend (for reference, not encoded in pixels):
#   3=grey, 4=off-black, 5=black, 7=pink, 8=red, 9=blue,
#   11=yellow, 14=green.

# Top caps — filled coloured 5x5 squares with off-black corners.
_TOP_CAP_TEMPLATE = lambda c: [
    [4, c, c, c, 4],
    [c, c, c, c, c],
    [c, c, c, c, c],
    [c, c, c, c, c],
    [4, c, c, c, 4],
]

# Bottom slots — hollow framed 5x5 squares.
_BOTTOM_SLOT_TEMPLATE = lambda c: [
    [c, c, c, c, c],
    [c, -1, -1, -1, c],
    [c, -1, -1, -1, c],
    [c, -1, -1, -1, c],
    [c, c, c, c, c],
]

# Binary crossing: 19 wide x 7 tall.
# Strand-col regions (local x 0..2 and 16..18) are transparent so the
# strand canvas shows through. Centre region (local x 3..15) is grey
# (palette 3). PASS variant has a small "+" centre marker. TWIST variant
# has an X spanning local (3, 0)..(15, 6) and (15, 0)..(3, 6).

_BIN_PASS_PIXELS = [
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 5, 5, 5, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1],
]

_BIN_TWIST_PIXELS = [
    [-1, -1, -1, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, -1, -1, -1],
    [-1, -1, -1, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 5, 3, 3, 3, 5, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 5, 3, 3, 3, 5, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, -1, -1, -1],
    [-1, -1, -1, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, -1, -1, -1],
]

# Long crossing: 35 wide x 7 tall.
# Strand cols at local x 0..2, 16..18, 32..34 — all transparent.
# Two grey regions x 3..15 and x 19..31. PASS has two centre markers.
# TWIST has X spanning x 3..31 (with col 1 strand passing through the
# X intersection at the centre via the transparent col 1 region).

_LONG_PASS_PIXELS = [
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 5, 5, 5, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 5, 5, 5, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1],
]

_LONG_TWIST_PIXELS = [
    [-1, -1, -1, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, -1, -1, -1, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, -1, -1, -1, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, -1, -1, -1],
    [-1, -1, -1, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, -1, -1, -1],
]

# Blocker: 7x7 coloured square crossed-out by a thick purple X.
# The coloured background identifies the rejected strand colour;
# the purple X reads as a "blocked / crossed-out" overlay.
_BLOCKER_TEMPLATE = lambda c: [
    [15,  c,  c,  c,  c,  c, 15],
    [15, 15,  c,  c,  c, 15, 15],
    [ c, 15, 15,  c, 15, 15,  c],
    [ c,  c, 15, 15, 15,  c,  c],
    [ c, 15, 15,  c, 15, 15,  c],
    [15, 15,  c,  c,  c, 15, 15],
    [15,  c,  c,  c,  c,  c, 15],
]

# Shift cell (green dye station): 6x6 abstract concentric pattern —
# green outer, black middle ring, green inner. Designed to be visually
# distinct from caps/slots/blockers and not resemble a face or symbol.
_SHIFT_GREEN_PIXELS = [
    [14, 14, 14, 14, 14, 14],
    [14,  5,  5,  5,  5, 14],
    [14,  5, 14, 14,  5, 14],
    [14,  5, 14, 14,  5, 14],
    [14,  5,  5,  5,  5, 14],
    [14, 14, 14, 14, 14, 14],
]


def _make_sprites():
    s = {}
    s["top_cap_red"] = Sprite(
        pixels=_TOP_CAP_TEMPLATE(8),
        name="top_cap_red",
        visible=True,
        collidable=False,
        tags=["start_cap", "colour_8"],
    )
    s["top_cap_blue"] = Sprite(
        pixels=_TOP_CAP_TEMPLATE(9),
        name="top_cap_blue",
        visible=True,
        collidable=False,
        tags=["start_cap", "colour_9"],
    )
    s["top_cap_yellow"] = Sprite(
        pixels=_TOP_CAP_TEMPLATE(11),
        name="top_cap_yellow",
        visible=True,
        collidable=False,
        tags=["start_cap", "colour_11"],
    )
    s["bottom_slot_red"] = Sprite(
        pixels=_BOTTOM_SLOT_TEMPLATE(8),
        name="bottom_slot_red",
        visible=True,
        collidable=False,
        tags=["end_slot", "colour_8"],
    )
    s["bottom_slot_blue"] = Sprite(
        pixels=_BOTTOM_SLOT_TEMPLATE(9),
        name="bottom_slot_blue",
        visible=True,
        collidable=False,
        tags=["end_slot", "colour_9"],
    )
    s["bottom_slot_yellow"] = Sprite(
        pixels=_BOTTOM_SLOT_TEMPLATE(11),
        name="bottom_slot_yellow",
        visible=True,
        collidable=False,
        tags=["end_slot", "colour_11"],
    )
    s["bottom_slot_green"] = Sprite(
        pixels=_BOTTOM_SLOT_TEMPLATE(14),
        name="bottom_slot_green",
        visible=True,
        collidable=False,
        tags=["end_slot", "colour_14"],
    )
    s["crossing_binary_pass"] = Sprite(
        pixels=_BIN_PASS_PIXELS,
        name="crossing_binary_pass",
        visible=True,
        collidable=False,
        tags=["crossing_visual", "type_binary", "state_pass"],
        layer=2,
    )
    s["crossing_binary_twist"] = Sprite(
        pixels=_BIN_TWIST_PIXELS,
        name="crossing_binary_twist",
        visible=True,
        collidable=False,
        tags=["crossing_visual", "type_binary", "state_twist"],
        layer=2,
    )
    s["crossing_long_pass"] = Sprite(
        pixels=_LONG_PASS_PIXELS,
        name="crossing_long_pass",
        visible=True,
        collidable=False,
        tags=["crossing_visual", "type_long", "state_pass"],
        layer=2,
    )
    s["crossing_long_twist"] = Sprite(
        pixels=_LONG_TWIST_PIXELS,
        name="crossing_long_twist",
        visible=True,
        collidable=False,
        tags=["crossing_visual", "type_long", "state_twist"],
        layer=2,
    )
    s["blocker_yellow"] = Sprite(
        pixels=_BLOCKER_TEMPLATE(11),
        name="blocker_yellow",
        visible=True,
        collidable=False,
        tags=["blocker", "colour_11"],
        layer=1,
    )
    s["blocker_blue"] = Sprite(
        pixels=_BLOCKER_TEMPLATE(9),
        name="blocker_blue",
        visible=True,
        collidable=False,
        tags=["blocker", "colour_9"],
        layer=1,
    )
    s["shift_green"] = Sprite(
        pixels=_SHIFT_GREEN_PIXELS,
        name="shift_green",
        visible=True,
        collidable=False,
        tags=["shift_cell", "colour_14"],
        layer=1,
    )
    # Strand canvas — placeholder pixels; rewritten in step().
    canvas_h = 49
    canvas_w = 64
    blank = [[-1] * canvas_w for _ in range(canvas_h)]
    s["strand_canvas"] = Sprite(
        pixels=blank,
        name="strand_canvas",
        visible=True,
        collidable=False,
        tags=["strand_canvas"],
        layer=0,
    )
    return s


sprites = _make_sprites()


# ---------------------------------------------------------------------
# 2. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 4
PADDING_COLOR = 4

# Strand column centres on screen.
COL_CENTRES = [17, 33, 49]
N_COLS = 3
STRAND_BAR_HALFWIDTH = 1  # 3-pixel-wide strand bar.

# Canvas extent in screen y.
CANVAS_TOP_Y = 8
CANVAS_BOTTOM_Y = 56  # exclusive; canvas rows are y in [8..56), height 48.
CANVAS_HEIGHT = CANVAS_BOTTOM_Y - CANVAS_TOP_Y + 1  # 49 (covers y=8..56 inclusive)

# Top-cap and bottom-slot y placement.
TOP_CAP_Y = 2
BOTTOM_SLOT_Y = 58

# Per-crossing-sprite dimensions for click-coord centre computation.
CROSSING_BINARY_W = 19
CROSSING_BINARY_H = 7
CROSSING_LONG_W = 35
CROSSING_LONG_H = 7


# ---------------------------------------------------------------------
# 3. LEVEL CONFIGURATIONS  (encoded as plain dicts; expanded into
#    Level(...) instances at module-import time).
# ---------------------------------------------------------------------

# Each level config has:
#   step_budget: int
#   start_caps: list of (col, palette_colour)
#   end_slots:  list of (col, palette_colour)
#   crossings:  list of (crossing_id, type ("binary"/"long"),
#                        column_pair, y_centre, initial_state)
#   blockers:   list of (col, y, colour)
#   shifts:     list of (col, y, new_colour)

_LEVEL_1_CFG = {
    "step_budget": 30,
    "start_caps": [(0, 8), (1, 9), (2, 11)],
    "end_slots":  [(0, 11), (1, 8), (2, 9)],
    "crossings": [
        ("C1", "binary", (0, 1), 16, "pass"),
        ("C2", "binary", (1, 2), 28, "pass"),
        ("C3", "binary", (0, 1), 40, "pass"),
    ],
    "blockers": [],
    "shifts":   [],
}

_LEVEL_2_CFG = {
    "step_budget": 24,
    "start_caps": [(0, 8), (1, 9), (2, 11)],
    "end_slots":  [(0, 11), (1, 8), (2, 9)],
    "crossings": [
        ("C1", "binary", (0, 1), 14, "pass"),
        ("C2", "long",   (0, 2), 22, "pass"),
        ("C3", "binary", (1, 2), 30, "pass"),
        ("C4", "binary", (0, 1), 46, "pass"),
    ],
    "blockers": [(1, 37, 11)],
    "shifts":   [],
}

_LEVEL_3_CFG = {
    "step_budget": 22,
    "start_caps": [(0, 8), (1, 9), (2, 11)],
    "end_slots":  [(0, 14), (1, 8), (2, 9)],
    "crossings": [
        ("C1", "binary", (0, 1), 14, "pass"),
        ("C2", "long",   (0, 2), 22, "pass"),
        ("C3", "binary", (1, 2), 30, "pass"),
        ("C4", "binary", (0, 1), 46, "pass"),
        ("C5", "binary", (1, 2), 53, "pass"),
    ],
    "blockers": [(1, 39, 11)],
    "shifts":   [(0, 38, 14)],
}

_LEVEL_CONFIGS = [_LEVEL_1_CFG, _LEVEL_2_CFG, _LEVEL_3_CFG]


def _slot_sprite_for_colour(c):
    return {8: "bottom_slot_red", 9: "bottom_slot_blue",
            11: "bottom_slot_yellow", 14: "bottom_slot_green"}[c]


def _cap_sprite_for_colour(c):
    return {8: "top_cap_red", 9: "top_cap_blue",
            11: "top_cap_yellow"}[c]


def _crossing_x_top_left(col_pair, ctype):
    # Crossing's top-left x: aligned so strand cols 0..2 of the bbox
    # land on the actual strand column on screen.
    if ctype == "binary":
        # Pair like (0, 1): leftmost col is min(pair). bbox starts at
        # x = COL_CENTRES[min] - 1 (so strand col bbox-local is 0..2).
        left_col = min(col_pair)
        return COL_CENTRES[left_col] - 1
    elif ctype == "long":
        # Always cols 0..2.
        return COL_CENTRES[0] - 1
    raise ValueError(ctype)


def _crossing_y_top_left(y_centre):
    return y_centre - 3  # 7 tall, centred.


def _build_level(cfg):
    placed = []

    # Top caps.
    for col, c in cfg["start_caps"]:
        cx = COL_CENTRES[col]
        sp = sprites[_cap_sprite_for_colour(c)].clone().set_position(cx - 2, TOP_CAP_Y)
        placed.append(sp)

    # Bottom slots.
    for col, c in cfg["end_slots"]:
        cx = COL_CENTRES[col]
        sp = sprites[_slot_sprite_for_colour(c)].clone().set_position(cx - 2, BOTTOM_SLOT_Y)
        placed.append(sp)

    # Strand canvas (placed at x=0, y=CANVAS_TOP_Y).
    placed.append(sprites["strand_canvas"].clone().set_position(0, CANVAS_TOP_Y))

    # Crossings: place BOTH PASS and TWIST variants at the same position.
    # The active variant has TANGIBLE; the inactive has REMOVED.
    # Per-crossing tags include the crossing_id so we can find the partner.
    for cid, ctype, col_pair, y_c, initial_state in cfg["crossings"]:
        x_tl = _crossing_x_top_left(col_pair, ctype)
        y_tl = _crossing_y_top_left(y_c)
        if ctype == "binary":
            pass_name = "crossing_binary_pass"
            twist_name = "crossing_binary_twist"
        else:
            pass_name = "crossing_long_pass"
            twist_name = "crossing_long_twist"

        # Per-crossing sprite tag carries cid + col_pair info, so we can
        # reconstruct routing from sprite tags at runtime.
        pair_tag = f"pair_{col_pair[0]}_{col_pair[1]}"
        cid_tag = f"cid_{cid}"

        pass_sp = sprites[pass_name].clone().set_position(x_tl, y_tl)
        for t in (cid_tag, pair_tag, f"yc_{y_c}"):
            pass_sp.tags.append(t)
        twist_sp = sprites[twist_name].clone().set_position(x_tl, y_tl)
        for t in (cid_tag, pair_tag, f"yc_{y_c}"):
            twist_sp.tags.append(t)

        if initial_state == "pass":
            pass_sp.set_interaction(InteractionMode.TANGIBLE)
            twist_sp.set_interaction(InteractionMode.REMOVED)
        else:
            pass_sp.set_interaction(InteractionMode.REMOVED)
            twist_sp.set_interaction(InteractionMode.TANGIBLE)
        placed.append(pass_sp)
        placed.append(twist_sp)

    # Blockers.
    for col, y, c in cfg["blockers"]:
        cx = COL_CENTRES[col]
        if c == 11:
            spname = "blocker_yellow"
        elif c == 9:
            spname = "blocker_blue"
        else:
            raise ValueError(f"unsupported blocker colour: {c}")
        sp = sprites[spname].clone().set_position(cx - 3, y - 3)
        sp.tags.append(f"blkcol_{col}")
        sp.tags.append(f"blky_{y}")
        placed.append(sp)

    # Shift cells.
    for col, y, c in cfg["shifts"]:
        cx = COL_CENTRES[col]
        if c == 14:
            spname = "shift_green"
        else:
            raise ValueError(f"unsupported shift colour: {c}")
        sp = sprites[spname].clone().set_position(cx - 3, y - 3)
        sp.tags.append(f"shfcol_{col}")
        sp.tags.append(f"shfy_{y}")
        placed.append(sp)

    level_data = {
        "step_budget": cfg["step_budget"],
        "start_caps": cfg["start_caps"],
        "end_slots":  cfg["end_slots"],
        "crossings":  cfg["crossings"],
        "blockers":   cfg["blockers"],
        "shifts":     cfg["shifts"],
    }
    return Level(sprites=placed, grid_size=(64, 64), data=level_data)


levels = [_build_level(cfg) for cfg in _LEVEL_CONFIGS]


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int):
        self.max_steps = max_steps
        self.current = max_steps

    def set_max(self, n: int) -> None:
        self.max_steps = n
        self.current = n

    def set_current(self, n: int) -> None:
        self.current = max(0, min(n, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.current / self.max_steps
        fill = round(64 * ratio)
        for x in range(64):
            frame[63, x] = 7 if x < fill else 4
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------

class Qy7w(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_ui = StepCounterHud(max_steps=30)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        super().__init__(
            game_id="qy7w",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )
        self.fail_pending: bool = False

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        budget = level.get_data("step_budget") or 30
        self._step_counter_ui.set_max(budget)
        self.fail_pending = False
        self._repaint_strands()

    # -- routing --------------------------------------------------------

    def _crossings_state(self):
        """Return a list of (cid, type, pair, y_centre, state) reflecting
        the current TANGIBLE variant of each crossing."""
        out = []
        seen = set()
        for sp in self.current_level.get_sprites_by_tag("crossing_visual"):
            if sp.interaction != InteractionMode.TANGIBLE:
                continue
            cid_tag = next((t for t in sp.tags if t.startswith("cid_")), None)
            if cid_tag is None or cid_tag in seen:
                continue
            seen.add(cid_tag)
            pair_tag = next((t for t in sp.tags if t.startswith("pair_")), None)
            yc_tag = next((t for t in sp.tags if t.startswith("yc_")), None)
            ctype = "binary" if "type_binary" in sp.tags else "long"
            state = "pass" if "state_pass" in sp.tags else "twist"
            pair_parts = pair_tag.split("_")
            pair = (int(pair_parts[1]), int(pair_parts[2]))
            yc = int(yc_tag.split("_")[1])
            out.append((cid_tag, ctype, pair, yc, state))
        # Sort by y-centre so crossings are processed top-to-bottom.
        out.sort(key=lambda t: t[3])
        return out

    def _level_data(self, key):
        return self.current_level.get_data(key)

    def _trace_strands(self):
        """Compute, for each strand identity, its (col, colour) at every
        screen y from CANVAS_TOP_Y to CANVAS_BOTTOM_Y. Returns:
            - strand_routes: list of dicts keyed by 'col' and 'colour' at each y.
            - blocker_hit: bool — True if any strand collided with a matching
              blocker during the trace.
            - bottom: list of (col, colour) at the canvas bottom row, indexed
              by strand identity 0..N_COLS-1.
        Strand identities are 0..N-1, matching the start_caps order.
        """
        start_caps = self._level_data("start_caps")
        crossings = self._crossings_state()
        blockers = self._level_data("blockers") or []
        shifts = self._level_data("shifts") or []

        # Strand state: list parallel to start_caps. Each entry is dict
        # {'col': current column index, 'colour': current colour}.
        strand_states = [
            {"col": col, "colour": colour}
            for (col, colour) in start_caps
        ]

        # Per-y-row routing log: list of dicts mapping col_idx -> strand_idx.
        # We don't strictly need this list; we just need to know which strand
        # is at which col at each y for canvas painting and constraint checks.
        canvas_paint = []  # list of (y, col_idx, colour) tuples to paint.
        blocker_hit = False

        for y in range(CANVAS_TOP_Y, CANVAS_BOTTOM_Y + 1):
            # Apply any crossing whose y_centre == y. (Crossings act at their
            # centre row.)
            for (_cid, ctype, pair, yc, state) in crossings:
                if yc != y or state != "twist":
                    continue
                if ctype == "binary":
                    a, b = pair
                    s_a = next((s for s in strand_states if s["col"] == a), None)
                    s_b = next((s for s in strand_states if s["col"] == b), None)
                    if s_a is not None and s_b is not None:
                        s_a["col"], s_b["col"] = b, a
                else:  # long
                    s_0 = next((s for s in strand_states if s["col"] == 0), None)
                    s_2 = next((s for s in strand_states if s["col"] == 2), None)
                    if s_0 is not None and s_2 is not None:
                        s_0["col"], s_2["col"] = 2, 0

            # Apply shift cells at this y.
            for (col, sy, new_colour) in shifts:
                if sy != y:
                    continue
                s = next((s for s in strand_states if s["col"] == col), None)
                if s is not None:
                    s["colour"] = new_colour

            # Check blockers at this y.
            for (col, by, blocker_colour) in blockers:
                if by != y:
                    continue
                s = next((s for s in strand_states if s["col"] == col), None)
                if s is not None and s["colour"] == blocker_colour:
                    blocker_hit = True

            # Record canvas paint instructions for this y.
            for s in strand_states:
                canvas_paint.append((y, s["col"], s["colour"]))

        bottom = [None] * len(strand_states)
        for s_idx, s in enumerate(strand_states):
            bottom[s_idx] = (s["col"], s["colour"])

        return canvas_paint, blocker_hit, bottom

    def _repaint_strands(self) -> None:
        canvas_paint, blocker_hit, bottom = self._trace_strands()
        canvas_sprites = self.current_level.get_sprites_by_tag("strand_canvas")
        if not canvas_sprites:
            return
        canvas = canvas_sprites[0]

        new_pixels = np.full((CANVAS_HEIGHT, 64), -1, dtype=np.int8)
        canvas_origin_y = canvas.y  # CANVAS_TOP_Y typically.

        for (y, col_idx, colour) in canvas_paint:
            cy = y - canvas_origin_y
            if cy < 0 or cy >= CANVAS_HEIGHT:
                continue
            cx_centre = COL_CENTRES[col_idx]
            for dx in range(-STRAND_BAR_HALFWIDTH, STRAND_BAR_HALFWIDTH + 1):
                x = cx_centre + dx
                if 0 <= x < 64:
                    new_pixels[cy, x] = colour
        canvas.pixels = new_pixels

        self.fail_pending = blocker_hit
        self._bottom_strands = bottom

    # -- click handling -------------------------------------------------

    def _toggle_crossing_at(self, gx: int, gy: int) -> bool:
        """If a crossing's TANGIBLE variant is at (gx, gy), swap states.
        Returns True if a toggle happened."""
        sp = self.current_level.get_sprite_at(gx, gy, "crossing_visual")
        if sp is None:
            return False
        cid_tag = next((t for t in sp.tags if t.startswith("cid_")), None)
        if cid_tag is None:
            return False
        # Find the partner sprite (same cid, different state).
        other_state_tag = "state_twist" if "state_pass" in sp.tags else "state_pass"
        partner = None
        for cand in self.current_level.get_sprites_by_tag(cid_tag):
            if cand is sp:
                continue
            if other_state_tag in cand.tags:
                partner = cand
                break
        if partner is None:
            return False
        sp.set_interaction(InteractionMode.REMOVED)
        partner.set_interaction(InteractionMode.TANGIBLE)
        return True

    # -- engine hooks ---------------------------------------------------

    def step(self) -> None:
        if self.action.id == GameAction.ACTION6:
            x = int(self.action.data.get("x", -1))
            y = int(self.action.data.get("y", -1))
            grid_xy = self.camera.display_to_grid(x, y)
            if grid_xy is not None:
                gx, gy = grid_xy
                self._toggle_crossing_at(gx, gy)

        self._repaint_strands()
        budget = self._level_data("step_budget") or 30
        self._step_counter_ui.set_current(budget - self._action_count)

        if self.fail_pending:
            self.lose()
            self.complete_action()
            return

        if self._action_count >= budget:
            self.lose()
            self.complete_action()
            return

        if self._check_win():
            self.next_level()

        self.complete_action()

    def _check_win(self) -> bool:
        end_slots = self._level_data("end_slots") or []
        if not hasattr(self, "_bottom_strands"):
            return False
        # Build a map: col -> (strand_idx, colour) at the bottom.
        bottom_by_col = {}
        for s_idx, (col, colour) in enumerate(self._bottom_strands):
            bottom_by_col[col] = (s_idx, colour)
        for (col, slot_colour) in end_slots:
            if col not in bottom_by_col:
                return False
            if bottom_by_col[col][1] != slot_colour:
                return False
        return True

    def _get_hidden_state(self) -> np.ndarray:
        budget = self._level_data("step_budget") or 30
        out = np.zeros((1, 1), dtype=np.int16)
        out[0, 0] = budget - self._action_count
        return out

    def _get_valid_actions(self) -> list[ActionInput]:
        actions = []
        seen_cid = set()
        for sp in self.current_level.get_sprites_by_tag("crossing_visual"):
            if sp.interaction != InteractionMode.TANGIBLE:
                continue
            cid_tag = next((t for t in sp.tags if t.startswith("cid_")), None)
            if cid_tag is None or cid_tag in seen_cid:
                continue
            seen_cid.add(cid_tag)
            # The crossing sprites have transparent strand-col regions in
            # the bbox (so the canvas underneath shows through). The bbox
            # centre may land on a transparent cell — pick a click target
            # known to be inside the visible grey region instead.
            if "type_long" in sp.tags:
                # Long crossing 35 wide: visible regions are local x 3..15
                # (between cols 0 and 1) and 19..31 (between cols 1 and 2).
                # Click at local x=9 (centre of left half).
                click_x = sp.x + 9
            else:
                # Binary crossing 19 wide: visible region is local x 3..15.
                # Click at local x=9 (centre).
                click_x = sp.x + 9
            click_y = sp.y + sp.height // 2
            actions.append(
                ActionInput(id=GameAction.ACTION6, data={"x": click_x, "y": click_y})
            )
        return actions
