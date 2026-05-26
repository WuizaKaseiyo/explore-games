"""."""

from __future__ import annotations

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
    "ingredient_block": Sprite(
        pixels=[[8, 8, 8, 8, 8, 8]] * 6,
        name="ingredient_block",
        tags=["ingredient"],
        layer=2,
    ),
    "selected_ring": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, -1, -1, -1, -1, -1, -1, 0],
            [0, -1, -1, -1, -1, -1, -1, 0],
            [0, -1, -1, -1, -1, -1, -1, 0],
            [0, -1, -1, -1, -1, -1, -1, 0],
            [0, -1, -1, -1, -1, -1, -1, 0],
            [0, -1, -1, -1, -1, -1, -1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
        name="selected_ring",
        collidable=False,
        interaction=InteractionMode.REMOVED,
        tags=["selected_ring"],
        layer=4,
    ),
    "intermediate_pip": Sprite(
        pixels=[[0]],
        name="intermediate_pip",
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["intermediate_pip"],
        layer=3,
    ),
    "slot_frame": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="slot_frame",
        collidable=True,
        tags=["slot_frame"],
        layer=1,
    ),
    "slot_fill": Sprite(
        pixels=[[0, 0, 0, 0, 0, 0]] * 6,
        name="slot_fill",
        collidable=False,
        interaction=InteractionMode.REMOVED,
        tags=["slot_fill"],
        layer=2,
    ),
    "target_frame": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="target_frame",
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target_frame"],
        layer=1,
    ),
    "target_fill": Sprite(
        pixels=[[0, 0, 0, 0, 0, 0, 0, 0]] * 8,
        name="target_fill",
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target_fill"],
        layer=2,
    ),
    "divider_strip": Sprite(
        pixels=[[4]] * 48,
        name="divider_strip",
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["decor"],
        layer=1,
    ),
    "rule_patch": Sprite(
        pixels=[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        name="rule_patch",
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["mix_rule"],
        layer=1,
    ),
    "rule_gap": Sprite(
        pixels=[[4], [4], [4]],
        name="rule_gap",
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["mix_rule"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
# Layout constants (cells in the 64×64 grid).
SLOT_POSITIONS = [(2, 22), (12, 22), (22, 22)]   # slot1, slot2, slot3 (top-left corners of 8×8 frames)
RESULT_POSITION = (12, 36)
TARGET_POSITION = (50, 48)                        # 10×10 target frame top-left (bottom-right with margin)
DIVIDER_POSITION = (31, 2)
PALETTE_X = 50                                   # x of primary palette column
PRIMARY_BASE_Y = 4
PRIMARY_STRIDE = 10                              # 6 (block) + 4 spacing = 10
INTERMEDIATE_BASE_Y = 4                          # second column for intermediates
INTERMEDIATE_X = 38
INTERMEDIATE_STRIDE = 10

# Palette colour values (per skills/global/color-legend.md)
MAGENTA = 6
PINK = 7
RED = 8
BLUE = 9
LIGHT_BLUE = 10
YELLOW = 11
ORANGE = 12
MAROON = 13
GREEN = 14
PURPLE = 15


def _make_slot_frame(idx: int) -> Sprite:
    sx, sy = SLOT_POSITIONS[idx]
    return sprites["slot_frame"].clone(new_name=f"slot_frame_{idx}").set_position(sx, sy)


def _make_result_frame() -> Sprite:
    return sprites["slot_frame"].clone(new_name="result_frame").set_position(*RESULT_POSITION)


def _make_divider() -> Sprite:
    return sprites["divider_strip"].clone(new_name="divider").set_position(*DIVIDER_POSITION)


def _make_target_frame() -> Sprite:
    return sprites["target_frame"].clone(new_name="target_frame").set_position(*TARGET_POSITION)


def _make_rule_strip(level, x: int, y: int, colours: list[int]) -> None:
    """Place a sequence of 3×3 colour patches separated by 1-pixel gaps at (x, y)."""
    cursor_x = x
    for i, c in enumerate(colours):
        patch = sprites["rule_patch"].clone()
        patch.pixels = np.full((3, 3), c, dtype=np.int16)
        patch.set_position(cursor_x, y)
        level.add_sprite(patch)
        cursor_x += 3
        if i != len(colours) - 1:
            gap = sprites["rule_gap"].clone().set_position(cursor_x, y)
            level.add_sprite(gap)
            cursor_x += 1


# Each level is built dynamically in on_set_level using level.data; the
# top-level Level objects below seed only the immutable geometry sprites
# (divider, slot frames, target frame, result frame). The dynamic content
# (ingredients, target fill, mix-rule strips, intermediate slot fills) is
# spawned per-level inside on_set_level via add_sprite.

def _bare_level(*, level_index: int) -> Level:
    geom = [
        _make_divider(),
        _make_slot_frame(0),
        _make_slot_frame(1),
        _make_slot_frame(2),
        _make_result_frame(),
        _make_target_frame(),
    ]
    return Level(
        sprites=geom,
        grid_size=(64, 64),
        data={"level_index": level_index},
    )


levels = [
    _bare_level(level_index=1),
    _bare_level(level_index=2),
    _bare_level(level_index=3),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 2          # light-grey playfield
PADDING_COLOR = 3             # grey letter-box (no scaling, but harmless)
STEP_BAR_ROW = 0
STEP_BAR_LEFT = 8
STEP_BAR_WIDTH = 48
STEP_BAR_FILL = 0
STEP_BAR_BG = 4

L1_PRIMARIES = [MAGENTA, LIGHT_BLUE]
L1_PAIR_RECIPES = [(MAGENTA, LIGHT_BLUE, PURPLE)]
L1_TRIPLE_RECIPES: list[tuple[int, int, int, int]] = []
L1_TARGET = PURPLE
L1_BUDGET = 30
L1_SLOT3_VISIBLE = False

L2_PRIMARIES = [MAGENTA, LIGHT_BLUE, PINK]
L2_PAIR_RECIPES = [
    (MAGENTA, LIGHT_BLUE, PURPLE),
    (PURPLE, PINK, MAROON),
]
L2_TRIPLE_RECIPES: list[tuple[int, int, int, int]] = []
L2_TARGET = MAROON
L2_BUDGET = 50
L2_SLOT3_VISIBLE = False

L3_PRIMARIES = [MAGENTA, LIGHT_BLUE, PINK, YELLOW]
L3_PAIR_RECIPES = [
    (MAGENTA, LIGHT_BLUE, PURPLE),
]
L3_TRIPLE_RECIPES = [
    (PURPLE, PINK, YELLOW, BLUE),         # produces target
    (MAGENTA, LIGHT_BLUE, YELLOW, GREEN),  # decoy triple
]
L3_TARGET = BLUE
L3_BUDGET = 60
L3_SLOT3_VISIBLE = True


def _level_config(idx: int) -> dict:
    if idx == 1:
        return dict(
            primaries=L1_PRIMARIES,
            pair_recipes=L1_PAIR_RECIPES,
            triple_recipes=L1_TRIPLE_RECIPES,
            target=L1_TARGET,
            budget=L1_BUDGET,
            slot3_visible=L1_SLOT3_VISIBLE,
        )
    if idx == 2:
        return dict(
            primaries=L2_PRIMARIES,
            pair_recipes=L2_PAIR_RECIPES,
            triple_recipes=L2_TRIPLE_RECIPES,
            target=L2_TARGET,
            budget=L2_BUDGET,
            slot3_visible=L2_SLOT3_VISIBLE,
        )
    return dict(
        primaries=L3_PRIMARIES,
        pair_recipes=L3_PAIR_RECIPES,
        triple_recipes=L3_TRIPLE_RECIPES,
        target=L3_TARGET,
        budget=L3_BUDGET,
        slot3_visible=L3_SLOT3_VISIBLE,
    )


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
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
# 5. INGREDIENT HANDLES
# ---------------------------------------------------------------------
class IngredientHandle:
    """Bundles an ingredient block, its selection ring, and its (optional) intermediate pip."""

    def __init__(
        self,
        block: Sprite,
        ring: Sprite,
        pip: Sprite | None,
        color: int,
        kind: str,
        uses: int,
    ) -> None:
        self.block = block
        self.ring = ring
        self.pip = pip
        self.color = color
        self.kind = kind  # "primary" or "intermediate"
        self.uses = uses

    def occupies(self, gx: int, gy: int) -> bool:
        bx, by = int(self.block.x), int(self.block.y)
        bw, bh = int(self.block.width), int(self.block.height)
        return bx <= gx < bx + bw and by <= gy < by + bh

    def remove_from_palette(self) -> None:
        self.block.set_interaction(InteractionMode.REMOVED)
        self.ring.set_interaction(InteractionMode.REMOVED)
        if self.pip is not None:
            self.pip.set_interaction(InteractionMode.REMOVED)


# ---------------------------------------------------------------------
# 6. THE GAME CLASS
# ---------------------------------------------------------------------
class Hr8q(NovaBaseGame):
    def __init__(self) -> None:
        self.step_bar = StepBarHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_bar],
        )
        # Per-level mutable state
        self.ingredients: list[IngredientHandle] = []
        self.slot_colors: list[int | None] = [None, None, None]
        self.slot_fills: list[Sprite | None] = [None, None, None]
        self.slot_frames: list[Sprite] = [None, None, None]  # type: ignore[list-item]
        self.target_color: int | None = None
        self.target_queue: list[int] = []
        self.target_fill_sprite: Sprite | None = None
        self.target_frame_sprite: Sprite | None = None
        self.result_frame_sprite: Sprite | None = None
        self.result_fill_sprite: Sprite | None = None
        self.pair_table: dict[frozenset[int], int] = {}
        self.triple_table: dict[frozenset[int], int] = {}
        self.steps_used: int = 0
        self.max_steps: int = 0
        self.slot3_visible: bool = False
        self.current_result_color: int | None = None
        super().__init__(
            game_id="hr8q",
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

        # Reset per-level state
        self.ingredients = []
        self.slot_colors = [None, None, None]
        self.slot_fills = [None, None, None]
        self.slot_frames = [None, None, None]
        self.target_queue = [int(cfg["target"])]
        self.target_color = self.target_queue[0]
        self.pair_table = {
            frozenset((a, b)): r for (a, b, r) in cfg["pair_recipes"]
        }
        self.triple_table = {
            frozenset((a, b, c)): r for (a, b, c, r) in cfg["triple_recipes"]
        }
        self.steps_used = 0
        self.max_steps = int(cfg["budget"])
        self.step_bar.reset(self.max_steps)
        self.slot3_visible = bool(cfg["slot3_visible"])
        self.current_result_color = None

        # Wire pre-placed slot frames by name
        for i in range(3):
            found = level.get_sprites_by_name(f"slot_frame_{i}")
            self.slot_frames[i] = found[0] if found else None  # type: ignore[assignment]
        rfound = level.get_sprites_by_name("result_frame")
        self.result_frame_sprite = rfound[0] if rfound else None
        tfound = level.get_sprites_by_name("target_frame")
        self.target_frame_sprite = tfound[0] if tfound else None

        # Slot3 visibility
        if self.slot_frames[2] is not None:
            if self.slot3_visible:
                self.slot_frames[2].set_interaction(InteractionMode.TANGIBLE)
            else:
                self.slot_frames[2].set_interaction(InteractionMode.REMOVED)

        # Place slot_fill placeholders (initially REMOVED)
        for i in range(3):
            sf = sprites["slot_fill"].clone(new_name=f"slot_fill_{i}")
            sx, sy = SLOT_POSITIONS[i]
            sf.set_position(sx + 1, sy + 1)
            sf.set_interaction(InteractionMode.REMOVED)
            level.add_sprite(sf)
            self.slot_fills[i] = sf

        # Result fill placeholder
        rf = sprites["slot_fill"].clone(new_name="result_fill")
        rf.set_position(RESULT_POSITION[0] + 1, RESULT_POSITION[1] + 1)
        rf.set_interaction(InteractionMode.REMOVED)
        level.add_sprite(rf)
        self.result_fill_sprite = rf

        # Target fill (the inner colour of the target chip)
        tf = sprites["target_fill"].clone(new_name="target_fill")
        tf.set_position(TARGET_POSITION[0] + 1, TARGET_POSITION[1] + 1)
        tf.pixels = np.full((8, 8), self.target_color, dtype=np.int16)
        tf.set_interaction(InteractionMode.INTANGIBLE)
        level.add_sprite(tf)
        self.target_fill_sprite = tf

        # Primary ingredients
        primaries = list(cfg["primaries"])
        for i, color in enumerate(primaries):
            self._spawn_ingredient(level, color, kind="primary", slot_index=i)

        # Mix-table HUD strips at the bottom
        y = 51
        for (a, b, r) in cfg["pair_recipes"]:
            _make_rule_strip(level, x=2, y=y, colours=[a, b, r])
            y += 4
        for (a, b, c, r) in cfg["triple_recipes"]:
            _make_rule_strip(level, x=2, y=y, colours=[a, b, c, r])
            y += 4

    # -----------------------------------------------------------------
    # Ingredient helpers
    # -----------------------------------------------------------------
    def _palette_position(self, slot_index: int, kind: str) -> tuple[int, int]:
        if kind == "primary":
            return (PALETTE_X, PRIMARY_BASE_Y + slot_index * PRIMARY_STRIDE)
        return (INTERMEDIATE_X, INTERMEDIATE_BASE_Y + slot_index * INTERMEDIATE_STRIDE)

    def _spawn_ingredient(
        self,
        level: Level,
        color: int,
        kind: str,
        slot_index: int,
    ) -> IngredientHandle:
        bx, by = self._palette_position(slot_index, kind)
        block = sprites["ingredient_block"].clone(new_name=f"ing_block_{kind}_{slot_index}")
        block.pixels = np.full((6, 6), color, dtype=np.int16)
        block.set_position(bx, by)
        level.add_sprite(block)

        ring = sprites["selected_ring"].clone(new_name=f"sel_ring_{kind}_{slot_index}")
        ring.set_position(bx - 1, by - 1)
        ring.set_interaction(InteractionMode.REMOVED)
        level.add_sprite(ring)

        pip = None
        if kind == "intermediate":
            pip = sprites["intermediate_pip"].clone(new_name=f"pip_{kind}_{slot_index}")
            pip.set_position(bx + 2, by + 7)
            pip.set_interaction(InteractionMode.INTANGIBLE)
            level.add_sprite(pip)

        uses = 1 if kind == "intermediate" else 10**9  # primaries: effectively infinite
        h = IngredientHandle(block=block, ring=ring, pip=pip, color=color, kind=kind, uses=uses)
        self.ingredients.append(h)
        return h

    def _next_intermediate_slot(self) -> int:
        used = sum(1 for h in self.ingredients if h.kind == "intermediate")
        return used

    # -----------------------------------------------------------------
    # Slot helpers
    # -----------------------------------------------------------------
    def _slot_count(self) -> int:
        return 3 if self.slot3_visible else 2

    def _slots_used(self) -> int:
        return sum(1 for c in self.slot_colors[: self._slot_count()] if c is not None)

    def _empty_slot_index(self) -> int | None:
        for i in range(self._slot_count()):
            if self.slot_colors[i] is None:
                return i
        return None

    def _fill_slot(self, slot_index: int, color: int) -> None:
        self.slot_colors[slot_index] = color
        sf = self.slot_fills[slot_index]
        if sf is not None:
            sf.pixels = np.full((6, 6), color, dtype=np.int16)
            sf.set_interaction(InteractionMode.TANGIBLE)
        self._refresh_selection_rings()
        self._recompute_result()

    def _clear_slot(self, slot_index: int) -> None:
        self.slot_colors[slot_index] = None
        sf = self.slot_fills[slot_index]
        if sf is not None:
            sf.set_interaction(InteractionMode.REMOVED)
        self._refresh_selection_rings()
        self._recompute_result()

    def _clear_all_slots(self) -> None:
        for i in range(3):
            self.slot_colors[i] = None
            sf = self.slot_fills[i]
            if sf is not None:
                sf.set_interaction(InteractionMode.REMOVED)
        self._refresh_selection_rings()
        self._recompute_result()

    def _refresh_selection_rings(self) -> None:
        active_colors = {c for c in self.slot_colors if c is not None}
        for h in self.ingredients:
            if h.uses <= 0:
                h.ring.set_interaction(InteractionMode.REMOVED)
                continue
            if h.color in active_colors:
                h.ring.set_interaction(InteractionMode.INTANGIBLE)
            else:
                h.ring.set_interaction(InteractionMode.REMOVED)

    def _recompute_result(self) -> None:
        used = [c for c in self.slot_colors[: self._slot_count()] if c is not None]
        result: int | None = None
        if len(used) == 2 and not self.slot3_visible:
            result = self.pair_table.get(frozenset(used))
        elif len(used) == 2 and self.slot3_visible and self.slot_colors[2] is None:
            result = self.pair_table.get(frozenset(used))
        elif len(used) == 3:
            result = self.triple_table.get(frozenset(used))
        self.current_result_color = result
        rf = self.result_fill_sprite
        if rf is None:
            return
        if result is None:
            rf.set_interaction(InteractionMode.REMOVED)
        else:
            rf.pixels = np.full((6, 6), result, dtype=np.int16)
            rf.set_interaction(InteractionMode.TANGIBLE)

    # -----------------------------------------------------------------
    # Click + commit handlers
    # -----------------------------------------------------------------
    def _ingredient_at(self, gx: int, gy: int) -> IngredientHandle | None:
        for h in self.ingredients:
            if h.uses <= 0:
                continue
            if h.occupies(gx, gy):
                return h
        return None

    def _slot_index_at(self, gx: int, gy: int) -> int | None:
        for i in range(self._slot_count()):
            sx, sy = SLOT_POSITIONS[i]
            if sx <= gx < sx + 8 and sy <= gy < sy + 8:
                return i
        return None

    def _handle_click(self, gx: int, gy: int) -> None:
        h = self._ingredient_at(gx, gy)
        if h is not None:
            empty = self._empty_slot_index()
            if empty is not None:
                self._fill_slot(empty, h.color)
            return
        s = self._slot_index_at(gx, gy)
        if s is not None and self.slot_colors[s] is not None:
            self._clear_slot(s)
            return
        # Anywhere else: no-op.

    def _consume_slot_intermediates(self) -> None:
        """Remove from the palette any intermediates whose colour was in a slot at commit time."""
        slot_set = {c for c in self.slot_colors if c is not None}
        if not slot_set:
            return
        for h in self.ingredients:
            if h.kind == "intermediate" and h.uses > 0 and h.color in slot_set:
                h.uses = 0
                h.remove_from_palette()

    def _distil_intermediate(self, color: int) -> None:
        existing = next(
            (h for h in self.ingredients if h.kind == "intermediate" and h.color == color and h.uses > 0),
            None,
        )
        if existing is not None:
            return  # already in the palette; do not duplicate
        slot = self._next_intermediate_slot()
        self._spawn_ingredient(self.current_level, color, kind="intermediate", slot_index=slot)

    def _handle_commit(self) -> None:
        used_count = self._slots_used()
        if used_count < 2:
            return  # no-op; step still consumed by caller
        slot_colors = [c for c in self.slot_colors[: self._slot_count()] if c is not None]
        if used_count == 2:
            result = self.pair_table.get(frozenset(slot_colors))
        else:  # used_count == 3
            result = self.triple_table.get(frozenset(slot_colors))

        if result is None:
            # Failed commit: slots clear; intermediates in slots are consumed.
            self._consume_slot_intermediates()
            self._clear_all_slots()
            return

        if self.target_queue and result == self.target_queue[0]:
            # Successful target match.
            self._consume_slot_intermediates()
            self.target_queue.pop(0)
            self._clear_all_slots()
            self._update_target_chip()
            return

        # Mismatch but valid recipe: distil intermediate.
        self._consume_slot_intermediates()
        self._clear_all_slots()
        self._distil_intermediate(result)

    def _update_target_chip(self) -> None:
        if self.target_queue:
            self.target_color = self.target_queue[0]
            tf = self.target_fill_sprite
            if tf is not None:
                tf.pixels = np.full((8, 8), self.target_color, dtype=np.int16)
                tf.set_interaction(InteractionMode.INTANGIBLE)
        else:
            self.target_color = None
            if self.target_fill_sprite is not None:
                self.target_fill_sprite.set_interaction(InteractionMode.REMOVED)
            if self.target_frame_sprite is not None:
                self.target_frame_sprite.set_interaction(InteractionMode.REMOVED)

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

        self.steps_used += 1
        self.step_bar.set_used(self.steps_used)

        if not self.target_queue:
            self.next_level()
            self.complete_action()
            return
        if self.steps_used >= self.max_steps:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        n = max(1, len(self.ingredients))
        out = np.full((4, n), -1, dtype=np.int16)
        for i, h in enumerate(self.ingredients):
            out[0, i] = h.color
            out[1, i] = h.uses if h.uses < 10**8 else 99
            out[2, i] = 1 if h.kind == "intermediate" else 0
            out[3, i] = 1 if (h.color in {c for c in self.slot_colors if c is not None}) else 0
        return out

    def _get_valid_actions(self) -> list[ActionInput]:
        actions: list[ActionInput] = [ActionInput(id=GameAction.ACTION5)]
        for h in self.ingredients:
            if h.uses <= 0:
                continue
            cx = int(h.block.x) + 3
            cy = int(h.block.y) + 3
            actions.append(ActionInput(id=GameAction.ACTION6, data={"x": cx, "y": cy}))
        for i in range(self._slot_count()):
            if self.slot_colors[i] is not None:
                sx, sy = SLOT_POSITIONS[i]
                actions.append(ActionInput(id=GameAction.ACTION6, data={"x": sx + 3, "y": sy + 3}))
        return actions
