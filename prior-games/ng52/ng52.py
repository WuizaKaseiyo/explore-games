"""."""

from __future__ import annotations

from collections import Counter

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
    "object_template": Sprite(
        pixels=[[9]],
        name="object_template",
        collidable=True,
        tags=["object"],
        layer=3,
    ),
    "selection_ring": Sprite(
        pixels=[[0, 0], [0, 0]],
        name="selection_ring",
        collidable=False,
        interaction=InteractionMode.REMOVED,
        tags=["selection_ring"],
        layer=5,
    ),
    "bin_frame_template": Sprite(
        pixels=[[4]],
        name="bin_frame_template",
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["bin_frame"],
        layer=1,
    ),
    "signature_stick_template": Sprite(
        pixels=[[9]],
        name="signature_stick_template",
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["signature_stick"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
# Each level's content is built dynamically in on_set_level. Level
# objects below carry only the level index in `data` so we can
# dispatch on it.

levels = [
    Level(sprites=[], grid_size=(64, 64), data={"level_index": 1}),
    Level(sprites=[], grid_size=(64, 64), data={"level_index": 2}),
    Level(sprites=[], grid_size=(64, 64), data={"level_index": 3}),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 2
PADDING_COLOR = 3
STEP_BAR_ROW = 0
STEP_BAR_LEFT = 8
STEP_BAR_WIDTH = 48
STEP_BAR_FILL = 0
STEP_BAR_BG = 4

# Palette colour values
BLUE = 9
PURPLE = 15
YELLOW = 11
OFF_BLACK = 4

# Layout (per bin count)
BIN_SIG_Y_TOP = 3
BIN_SIG_AREA_HEIGHT = 7
HAND_Y_OFFSET = 1  # rows above the holding-area bottom for hand-held objects


def _bin_layout(n_bins: int) -> dict:
    if n_bins == 4:
        return dict(
            bin_x=[2, 17, 32, 47],
            bin_width=13,
            holding_y_top=12,
            holding_height=10,
            slot_size=5,
            slots_per_row=2,
            slots_per_col=2,
            pool_y_top=24,
        )
    return dict(
        bin_x=[2, 22, 42],
        bin_width=18,
        holding_y_top=12,
        holding_height=16,
        slot_size=8,
        slots_per_row=2,
        slots_per_col=2,
        pool_y_top=30,
    )


# ---------------------------------------------------------------------
# 4. HUD
# ---------------------------------------------------------------------
class StepBarHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self._max = 1
        self._used = 0

    def reset(self, max_steps: int) -> None:
        self._max = max(1, int(max_steps))
        self._used = 0

    def set_used(self, u: int) -> None:
        self._used = max(0, int(u))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        remaining = max(0, self._max - self._used)
        filled = round(STEP_BAR_WIDTH * remaining / self._max)
        for i in range(STEP_BAR_WIDTH):
            frame[STEP_BAR_ROW, STEP_BAR_LEFT + i] = STEP_BAR_FILL if i < filled else STEP_BAR_BG
        return frame


# ---------------------------------------------------------------------
# 5. DATA HANDLES
# ---------------------------------------------------------------------
class ObjectHandle:
    def __init__(self, sprite, multiset, pool_position, container):
        self.sprite = sprite
        self.multiset = multiset
        self.pool_position = pool_position
        self.container = container

    @property
    def x(self) -> int:
        return int(self.sprite.x)

    @property
    def y(self) -> int:
        return int(self.sprite.y)

    @property
    def width(self) -> int:
        return int(self.sprite.width)

    @property
    def height(self) -> int:
        return int(self.sprite.height)

    def occupies(self, gx: int, gy: int) -> bool:
        return self.x <= gx < self.x + self.width and self.y <= gy < self.y + self.height


class BinHandle:
    def __init__(self, index, signature_multiset, holding_rect, slot_size, slots_per_row):
        self.index = index
        self.signature_multiset = signature_multiset
        self.holding_rect = holding_rect
        self.slot_size = slot_size
        self.slots_per_row = slots_per_row
        self.placed = []

    def container_id(self) -> str:
        return f"bin_{self.index}"

    def next_slot_position(self) -> tuple[int, int]:
        x0, y0, x1, y1 = self.holding_rect
        idx = len(self.placed)
        col = idx % self.slots_per_row
        row = idx // self.slots_per_row
        return x0 + col * self.slot_size, y0 + row * self.slot_size


# ---------------------------------------------------------------------
# 6. LEVEL CONTENT BUILDERS
# ---------------------------------------------------------------------
# Object pixel templates: each is a small (≤3×3) np-array with -1 for transparent.
def _pix(rows: list[list[int]]) -> np.ndarray:
    return np.array(rows, dtype=np.int16)


# L1 single-colour shapes (counts 3, 5, 7).
SHAPE_3B = _pix([
    [BLUE, BLUE],
    [BLUE, -1],
])  # L-tromino, 3 cells
SHAPE_5B = _pix([
    [-1, BLUE, -1],
    [BLUE, BLUE, BLUE],
    [-1, BLUE, -1],
])  # plus, 5 cells
SHAPE_7B = _pix([
    [BLUE, BLUE, BLUE],
    [-1, BLUE, -1],
    [BLUE, BLUE, BLUE],
])  # H-shape, 7 cells

# L2 / L3 multi-colour shapes — irregular and (in the multi-colour
# variants) deliberately scattered: same-colour pixels are not always
# 4-connected, but the whole shape is.

# 6-blue (single-colour, irregular)
SHAPE_6B_A = _pix([
    [BLUE, BLUE, -1],
    [-1, BLUE, -1],
    [BLUE, BLUE, BLUE],
])
SHAPE_6B_B = _pix([
    [BLUE, -1, BLUE],
    [BLUE, BLUE, BLUE],
    [-1, BLUE, -1],
])
SHAPE_6B_C = _pix([
    [-1, BLUE, BLUE],
    [BLUE, BLUE, -1],
    [BLUE, BLUE, -1],
])

# 3-blue + 3-purple (scattered)
SHAPE_3B3P_A = _pix([
    [BLUE, PURPLE, BLUE],
    [-1, PURPLE, -1],
    [BLUE, PURPLE, -1],
])  # P backbone, 3 B at corners
SHAPE_3B3P_B = _pix([
    [PURPLE, BLUE, PURPLE],
    [-1, BLUE, -1],
    [PURPLE, BLUE, -1],
])  # B backbone, 3 P at corners
SHAPE_3B3P_C = _pix([
    [BLUE, PURPLE, -1],
    [-1, BLUE, PURPLE],
    [-1, PURPLE, BLUE],
])  # diagonal staircase

# 4-blue + 2-purple (scattered)
SHAPE_4B2P_A = _pix([
    [BLUE, PURPLE, BLUE],
    [BLUE, BLUE, -1],
    [-1, PURPLE, -1],
])
SHAPE_4B2P_B = _pix([
    [PURPLE, BLUE, PURPLE, BLUE],
    [-1, BLUE, BLUE, -1],
])  # wide and flat
SHAPE_4B2P_C = _pix([
    [BLUE, BLUE, PURPLE],
    [BLUE, -1, -1],
    [PURPLE, BLUE, -1],
])

# 4-blue + 2-yellow (scattered)
SHAPE_4B2Y_A = _pix([
    [BLUE, YELLOW, BLUE],
    [BLUE, BLUE, -1],
    [-1, YELLOW, -1],
])
SHAPE_4B2Y_B = _pix([
    [YELLOW, BLUE, YELLOW, BLUE],
    [-1, BLUE, BLUE, -1],
])

# 2-blue + 2-purple + 2-yellow (tri-colour)
SHAPE_2B2P2Y_A = _pix([
    [BLUE, PURPLE, YELLOW],
    [YELLOW, PURPLE, BLUE],
])  # 2x3 alternating
SHAPE_2B2P2Y_B = _pix([
    [YELLOW, BLUE, PURPLE],
    [PURPLE, YELLOW, BLUE],
])  # 2x3 different alternation

# L3 distractors: pixel multisets matching NO bin signature.
SHAPE_DISTRACTOR_5B = _pix([
    [-1, BLUE, BLUE],
    [BLUE, BLUE, -1],
    [BLUE, -1, -1],
])  # 5B in a Z; multiset {B:5}
SHAPE_DISTRACTOR_3B1P = _pix([
    [BLUE, PURPLE, BLUE],
    [BLUE, -1, -1],
])  # {B:3, P:1} — close to bin B (3B+3P) but missing 2 purples


def _multiset_of(pixels: np.ndarray) -> dict:
    cnt: Counter = Counter()
    for v in pixels.flatten().tolist():
        if v >= 0:
            cnt[int(v)] += 1
    return dict(cnt)


def _build_object(name: str, pixels: np.ndarray, x: int, y: int) -> Sprite:
    s = sprites["object_template"].clone(new_name=name)
    s.pixels = pixels.copy()
    s.set_position(x, y)
    return s


def _level_config(idx: int) -> dict:
    if idx == 1:
        # Bins: A=3B, B=5B, C=7B. Pool order intentionally not matching bin
        # order — the player must read each shape and match it themselves.
        return dict(
            bin_signatures=[
                [(BLUE, 3)],
                [(BLUE, 5)],
                [(BLUE, 7)],
            ],
            objects=[
                ("o_7b", SHAPE_7B, 6, 38),
                ("o_3b", SHAPE_3B, 28, 38),
                ("o_5b", SHAPE_5B, 44, 38),
            ],
            budget=40,
        )
    if idx == 2:
        # 6 objects, 2 per bin; every object classifies (no distractors).
        # Multi-colour objects are deliberately irregular with scattered
        # B and P pixels.
        return dict(
            bin_signatures=[
                [(BLUE, 6)],
                [(BLUE, 3), (PURPLE, 3)],
                [(BLUE, 4), (PURPLE, 2)],
            ],
            objects=[
                ("o_3b3p_a", SHAPE_3B3P_A,   2, 36),
                ("o_4b2p_b", SHAPE_4B2P_B,  14, 36),
                ("o_6b_a",   SHAPE_6B_A,    30, 36),
                ("o_3b3p_b", SHAPE_3B3P_B,  44, 36),
                ("o_4b2p_a", SHAPE_4B2P_A,  56, 36),
                ("o_6b_b",   SHAPE_6B_B,     2, 50),
            ],
            budget=80,
        )
    # L3: 4 bins using 3 colours; more matching objects + 2 distractors
    # that must be left in the pool.
    return dict(
        bin_signatures=[
            [(BLUE, 6)],
            [(BLUE, 3), (PURPLE, 3)],
            [(BLUE, 4), (YELLOW, 2)],
            [(BLUE, 2), (PURPLE, 2), (YELLOW, 2)],
        ],
        objects=[
            # row 1
            ("o_6b_a",      SHAPE_6B_A,      2, 28),
            ("o_3b3p_a",    SHAPE_3B3P_A,   14, 28),
            ("o_4b2y_a",    SHAPE_4B2Y_A,   26, 28),
            ("o_2b2p2y_a",  SHAPE_2B2P2Y_A, 38, 28),
            ("o_distractor_5b", SHAPE_DISTRACTOR_5B, 52, 28),
            # row 2
            ("o_6b_b",      SHAPE_6B_B,      2, 40),
            ("o_3b3p_b",    SHAPE_3B3P_B,   14, 40),
            ("o_4b2y_b",    SHAPE_4B2Y_B,   26, 40),
            ("o_2b2p2y_b",  SHAPE_2B2P2Y_B, 38, 40),
            ("o_distractor_3b1p", SHAPE_DISTRACTOR_3B1P, 52, 40),
            # row 3 — extra matching variants for "more objects"
            ("o_6b_c",      SHAPE_6B_C,      2, 52),
            ("o_3b3p_c",    SHAPE_3B3P_C,   14, 52),
        ],
        budget=120,
    )


# ---------------------------------------------------------------------
# 7. THE GAME CLASS
# ---------------------------------------------------------------------
class Ng52(NovaBaseGame):
    def __init__(self) -> None:
        self.step_bar = StepBarHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_bar],
        )
        self.objects: list[ObjectHandle] = []
        self.bins: list[BinHandle] = []
        self.selection: ObjectHandle | None = None
        self.selection_ring: Sprite | None = None
        self.steps_used: int = 0
        self.max_steps: int = 0
        super().__init__(
            game_id="ng52",
            levels=levels,
            camera=camera,
            available_actions=[5, 6],
        )

    # -----------------------------------------------------------------
    # Level setup
    # -----------------------------------------------------------------
    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        idx = int(level.get_data("level_index") or 1)
        cfg = _level_config(idx)

        # Reset state
        self.objects = []
        self.bins = []
        self.selection = None
        self.selection_ring = None
        self.steps_used = 0
        self.max_steps = int(cfg["budget"])
        self.step_bar.reset(self.max_steps)

        n_bins = len(cfg["bin_signatures"])
        self.layout = _bin_layout(n_bins)

        # Bins: frame, signature sticks
        for i, sig in enumerate(cfg["bin_signatures"]):
            bx0 = self.layout["bin_x"][i]
            bx1 = bx0 + self.layout["bin_width"]
            hy0 = self.layout["holding_y_top"]
            hy1 = hy0 + self.layout["holding_height"]
            holding_rect = (bx0 + 1, hy0, bx1 - 1, hy1)
            sig_multiset: dict = {}
            for color, length in sig:
                sig_multiset[color] = sig_multiset.get(color, 0) + length
            self.bins.append(BinHandle(
                index=i,
                signature_multiset=sig_multiset,
                holding_rect=holding_rect,
                slot_size=self.layout["slot_size"],
                slots_per_row=self.layout["slots_per_row"],
            ))

            # Bin frame: 4 thin border lines around the holding area.
            self._add_bin_frame(level, holding_rect, name_prefix=f"bin{i}")

            # Signature sticks: stack vertically above the holding area.
            stick_y = BIN_SIG_Y_TOP
            for color, length in sig:
                stick = sprites["signature_stick_template"].clone(new_name=f"stick_b{i}_c{color}_l{length}_y{stick_y}")
                stick.pixels = np.full((1, length), color, dtype=np.int16)
                stick.set_position(bx0 + 1, stick_y)
                level.add_sprite(stick)
                stick_y += 2

        # Objects
        for (name, pixels, ox, oy) in cfg["objects"]:
            sprite = _build_object(name, pixels, ox, oy)
            level.add_sprite(sprite)
            self.objects.append(ObjectHandle(
                sprite=sprite,
                multiset=_multiset_of(pixels),
                pool_position=(ox, oy),
                container="pool",
            ))

        # Selection ring (initially REMOVED)
        ring = sprites["selection_ring"].clone(new_name="sel_ring")
        ring.set_interaction(InteractionMode.REMOVED)
        level.add_sprite(ring)
        self.selection_ring = ring

    def _add_bin_frame(self, level: Level, rect: tuple[int, int, int, int], name_prefix: str) -> None:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        # top
        top = sprites["bin_frame_template"].clone(new_name=f"{name_prefix}_top")
        top.pixels = np.full((1, width), OFF_BLACK, dtype=np.int16)
        top.set_position(x0, y0 - 1)
        level.add_sprite(top)
        # bottom
        bot = sprites["bin_frame_template"].clone(new_name=f"{name_prefix}_bot")
        bot.pixels = np.full((1, width), OFF_BLACK, dtype=np.int16)
        bot.set_position(x0, y1)
        level.add_sprite(bot)
        # left
        left = sprites["bin_frame_template"].clone(new_name=f"{name_prefix}_left")
        left.pixels = np.full((height, 1), OFF_BLACK, dtype=np.int16)
        left.set_position(x0 - 1, y0)
        level.add_sprite(left)
        # right
        right = sprites["bin_frame_template"].clone(new_name=f"{name_prefix}_right")
        right.pixels = np.full((height, 1), OFF_BLACK, dtype=np.int16)
        right.set_position(x1, y0)
        level.add_sprite(right)

    # -----------------------------------------------------------------
    # Selection / placement helpers
    # -----------------------------------------------------------------
    def _refresh_selection_ring(self) -> None:
        ring = self.selection_ring
        if ring is None:
            return
        if self.selection is None:
            ring.set_interaction(InteractionMode.REMOVED)
            return
        obj = self.selection
        w = obj.width + 2
        h = obj.height + 2
        ring_pixels = np.full((h, w), -1, dtype=np.int16)
        ring_pixels[0, :] = 0
        ring_pixels[-1, :] = 0
        ring_pixels[:, 0] = 0
        ring_pixels[:, -1] = 0
        ring.pixels = ring_pixels
        ring.set_position(obj.x - 1, obj.y - 1)
        ring.set_interaction(InteractionMode.INTANGIBLE)

    def _select(self, obj: ObjectHandle | None) -> None:
        self.selection = obj
        self._refresh_selection_ring()

    def _object_at(self, gx: int, gy: int) -> ObjectHandle | None:
        for obj in self.objects:
            if obj.occupies(gx, gy):
                return obj
        return None

    def _bin_holding_at(self, gx: int, gy: int) -> BinHandle | None:
        for b in self.bins:
            x0, y0, x1, y1 = b.holding_rect
            if x0 <= gx < x1 and y0 <= gy < y1:
                return b
        return None

    def _place_in_bin(self, obj: ObjectHandle, b: BinHandle) -> None:
        slot_x, slot_y = b.next_slot_position()
        obj.sprite.set_position(slot_x, slot_y)
        obj.container = b.container_id()
        b.placed.append(obj)

    def _remove_from_container(self, obj: ObjectHandle) -> None:
        if obj.container.startswith("bin_"):
            i = int(obj.container.split("_")[1])
            b = self.bins[i]
            if obj in b.placed:
                b.placed.remove(obj)
                # Re-pack remaining objects into slot positions.
                for j, o2 in enumerate(b.placed):
                    col = j % b.slots_per_row
                    row = j // b.slots_per_row
                    bx0, by0, _, _ = b.holding_rect
                    o2.sprite.set_position(bx0 + col * b.slot_size, by0 + row * b.slot_size)
        obj.container = "pool"

    def _snap_back_to_pool(self) -> None:
        for obj in self.objects:
            if obj.container != "pool":
                if obj.container.startswith("bin_"):
                    i = int(obj.container.split("_")[1])
                    if obj in self.bins[i].placed:
                        self.bins[i].placed.remove(obj)
                obj.sprite.set_position(*obj.pool_position)
                obj.container = "pool"
        self._select(None)

    # -----------------------------------------------------------------
    # Action handlers
    # -----------------------------------------------------------------
    def _handle_click(self, gx: int, gy: int) -> None:
        obj = self._object_at(gx, gy)
        if obj is not None:
            if obj.container.startswith("bin_"):
                # Pick up from bin: remove from bin, restore the object
                # to its original pool position, and set it as the
                # selection so the next bin click re-places it.
                self._remove_from_container(obj)
                obj.sprite.set_position(*obj.pool_position)
                self._select(obj)
            else:
                # Pool object: select (or switch selection)
                if self.selection is obj:
                    self._select(None)
                else:
                    self._select(obj)
            return
        # Bin holding-area hit?
        b = self._bin_holding_at(gx, gy)
        if b is not None and self.selection is not None:
            self._place_in_bin(self.selection, b)
            self._select(None)
            return
        # Anywhere else: no-op.

    def _check_win(self) -> bool:
        # Each bin must contain at least one placed object, and EVERY
        # placed object's per-colour pixel multiset must equal the bin's
        # signature multiset exactly.
        for b in self.bins:
            if not b.placed:
                return False
            for o in b.placed:
                if o.multiset != b.signature_multiset:
                    return False
        # Every CLASSIFIABLE object (one whose multiset matches some
        # bin signature) must be placed in a bin. Distractor objects
        # whose multisets match no bin are allowed to remain in the
        # pool.
        bin_sigs = [b.signature_multiset for b in self.bins]
        for o in self.objects:
            if any(o.multiset == sig for sig in bin_sigs):
                if not o.container.startswith("bin_"):
                    return False
        return True

    def _handle_commit(self) -> None:
        if self._check_win():
            self.next_level()
        else:
            self._snap_back_to_pool()

    # -----------------------------------------------------------------
    # Engine hooks
    # -----------------------------------------------------------------
    def step(self) -> None:
        if self.steps_used >= self.max_steps:
            self.lose()
            self.complete_action()
            return

        aid = self.action.id
        if aid == GameAction.ACTION5:
            self._handle_commit()
        elif aid == GameAction.ACTION6:
            data = self.action.data or {}
            ax = int(data.get("x", -1))
            ay = int(data.get("y", -1))
            gp = self.camera.display_to_grid(ax, ay)
            if gp is not None:
                gx, gy = int(gp[0]), int(gp[1])
                self._handle_click(gx, gy)

        self._refresh_selection_ring()
        self.steps_used += 1
        self.step_bar.set_used(self.steps_used)

        if self.steps_used >= self.max_steps:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        n = max(1, len(self.objects))
        out = np.full((3, n), -1, dtype=np.int16)
        for i, o in enumerate(self.objects):
            if o.container == "pool":
                out[0, i] = 0
            elif o.container.startswith("bin_"):
                out[0, i] = 1 + int(o.container.split("_")[1])
            else:
                out[0, i] = 9  # hand
            out[1, i] = o.x
            out[2, i] = o.y
        return out

    def _get_valid_actions(self) -> list[ActionInput]:
        actions: list[ActionInput] = [ActionInput(id=GameAction.ACTION5)]
        for o in self.objects:
            actions.append(ActionInput(id=GameAction.ACTION6, data={"x": o.x + 1, "y": o.y + 1}))
        for b in self.bins:
            x0, y0, x1, y1 = b.holding_rect
            actions.append(ActionInput(id=GameAction.ACTION6, data={"x": (x0 + x1) // 2, "y": (y0 + y1) // 2}))
        return actions
