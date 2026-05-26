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


# ==============================================================
# 1. SPRITE BANK
# ==============================================================

_carrier_base_pixels = [
    [-1,  5,  5,  5,  5, -1],
    [ 5,  4,  4,  4,  4,  5],
    [ 5,  4,  1,  1,  4,  5],
    [ 5,  4,  1,  1,  4,  5],
    [ 5,  4,  4,  4,  4,  5],
    [-1,  5,  5,  5,  5, -1],
]


def _pad_pixels(c):
    return [
        [-1,  2,  2,  2,  2, -1],
        [ 2,  c,  c,  c,  c,  2],
        [ 2,  c,  1,  1,  c,  2],
        [ 2,  c,  1,  1,  c,  2],
        [ 2,  c,  c,  c,  c,  2],
        [-1,  2,  2,  2,  2, -1],
    ]


def _slot_pixels(c):
    return [
        [-1,  c,  c,  c,  c, -1],
        [ c,  c,  4,  4,  c,  c],
        [ c,  4,  4,  4,  4,  c],
        [ c,  4,  4,  4,  4,  c],
        [ c,  c,  4,  4,  c,  c],
        [-1,  c,  c,  c,  c, -1],
    ]


def _door_pixels(c):
    return [
        [ c,  c,  c,  c,  c,  c],
        [ c,  5,  c,  c,  5,  c],
        [ c,  c,  5,  5,  c,  c],
        [ c,  c,  5,  5,  c,  c],
        [ c,  5,  c,  c,  5,  c],
        [ c,  c,  c,  c,  c,  c],
    ]


sprites = {
    "carrier": Sprite(
        pixels=_carrier_base_pixels,
        name="carrier",
        visible=True,
        collidable=True,
        tags=["carrier"],
        layer=2,
    ),
    "door_green": Sprite(
        pixels=_door_pixels(14),
        name="door_green",
        visible=True,
        collidable=True,
        tags=["door", "demands_green"],
        layer=1,
    ),
    "door_magenta": Sprite(
        pixels=_door_pixels(6),
        name="door_magenta",
        visible=True,
        collidable=True,
        tags=["door", "demands_magenta"],
        layer=1,
    ),
    "door_purple": Sprite(
        pixels=_door_pixels(15),
        name="door_purple",
        visible=True,
        collidable=True,
        tags=["door", "demands_purple"],
        layer=1,
    ),
    "pad_lightblue": Sprite(
        pixels=_pad_pixels(10),
        name="pad_lightblue",
        visible=True,
        collidable=False,
        tags=["pad", "pigment_lightblue"],
        layer=0,
    ),
    "pad_orange": Sprite(
        pixels=_pad_pixels(12),
        name="pad_orange",
        visible=True,
        collidable=False,
        tags=["pad", "pigment_orange"],
        layer=0,
    ),
    "pad_pink": Sprite(
        pixels=_pad_pixels(7),
        name="pad_pink",
        visible=True,
        collidable=False,
        tags=["pad", "pigment_pink"],
        layer=0,
    ),
    "slot_black": Sprite(
        pixels=_slot_pixels(5),
        name="slot_black",
        visible=True,
        collidable=False,
        tags=["slot", "demands_black"],
        layer=0,
    ),
    "slot_consumed": Sprite(
        pixels=[
            [-1,  2,  2,  2,  2, -1],
            [ 2,  2,  4,  4,  2,  2],
            [ 2,  4,  4,  4,  4,  2],
            [ 2,  4,  4,  4,  4,  2],
            [ 2,  2,  4,  4,  2,  2],
            [-1,  2,  2,  2,  2, -1],
        ],
        name="slot_consumed",
        visible=True,
        collidable=False,
        tags=["consumed"],
        layer=0,
    ),
    "slot_green": Sprite(
        pixels=_slot_pixels(14),
        name="slot_green",
        visible=True,
        collidable=False,
        tags=["slot", "demands_green"],
        layer=0,
    ),
    "slot_lightblue": Sprite(
        pixels=_slot_pixels(10),
        name="slot_lightblue",
        visible=True,
        collidable=False,
        tags=["slot", "demands_lightblue"],
        layer=0,
    ),
    "slot_magenta": Sprite(
        pixels=_slot_pixels(6),
        name="slot_magenta",
        visible=True,
        collidable=False,
        tags=["slot", "demands_magenta"],
        layer=0,
    ),
    "slot_orange": Sprite(
        pixels=_slot_pixels(12),
        name="slot_orange",
        visible=True,
        collidable=False,
        tags=["slot", "demands_orange"],
        layer=0,
    ),
    "slot_pink": Sprite(
        pixels=_slot_pixels(7),
        name="slot_pink",
        visible=True,
        collidable=False,
        tags=["slot", "demands_pink"],
        layer=0,
    ),
    "slot_purple": Sprite(
        pixels=_slot_pixels(15),
        name="slot_purple",
        visible=True,
        collidable=False,
        tags=["slot", "demands_purple"],
        layer=0,
    ),
    "wall_block": Sprite(
        pixels=[[3] * 8 for _ in range(8)],
        name="wall_block",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    ),
}


# ==============================================================
# 2. CONSTANTS
# ==============================================================

BACKGROUND_COLOR = 1
PADDING_COLOR = 2
STEP_SIZE = 8
SPRITE_INSET = 1

PIGMENT_ORANGE = 1
PIGMENT_PINK = 2
PIGMENT_LIGHTBLUE = 4

MIXING_TABLE = {
    0: 1,
    1: 12,
    2: 7,
    4: 10,
    3: 14,
    5: 15,
    6: 6,
    7: 5,
}

SLOT_DEMANDS = {
    "demands_orange":    1,
    "demands_pink":      2,
    "demands_lightblue": 4,
    "demands_green":     3,
    "demands_purple":    5,
    "demands_magenta":   6,
    "demands_black":     7,
}

DOOR_DEMANDS = {
    "demands_green":   3,
    "demands_purple":  5,
    "demands_magenta": 6,
}

PAD_PIGMENTS = {
    "pigment_orange":    1,
    "pigment_pink":      2,
    "pigment_lightblue": 4,
}


# ==============================================================
# 3. LEVELS
# ==============================================================

def _border_walls():
    walls = []
    for ix in range(8):
        walls.append(
            sprites["wall_block"].clone().set_position(ix * STEP_SIZE, 0)
        )
        walls.append(
            sprites["wall_block"].clone().set_position(ix * STEP_SIZE, 7 * STEP_SIZE)
        )
    for iy in range(1, 7):
        walls.append(
            sprites["wall_block"].clone().set_position(0, iy * STEP_SIZE)
        )
        walls.append(
            sprites["wall_block"].clone().set_position(7 * STEP_SIZE, iy * STEP_SIZE)
        )
    return walls


def _at(name, ix, iy):
    return sprites[name].clone().set_position(
        ix * STEP_SIZE + SPRITE_INSET,
        iy * STEP_SIZE + SPRITE_INSET,
    )


_level1_sprites = _border_walls() + [
    _at("carrier", 1, 1),
    _at("pad_orange", 3, 3),
    _at("slot_orange", 6, 5),
]

_level2_sprites = _border_walls() + [
    _at("carrier", 1, 1),
    _at("pad_orange", 2, 3),
    _at("pad_pink", 5, 3),
    _at("slot_pink", 1, 5),
    _at("slot_green", 5, 5),
]


_level3_walls = _border_walls()
for _ix in [1, 2, 3, 5, 6]:
    _level3_walls.append(
        sprites["wall_block"].clone().set_position(_ix * STEP_SIZE, 4 * STEP_SIZE)
    )

_level3_sprites = _level3_walls + [
    _at("carrier", 1, 1),
    _at("pad_orange", 1, 3),
    _at("pad_pink", 5, 3),
    _at("door_green", 4, 4),
    _at("slot_green", 3, 5),
    _at("pad_lightblue", 6, 5),
    _at("slot_pink", 1, 6),
    _at("pad_pink", 3, 6),
    _at("slot_lightblue", 4, 6),
    _at("slot_magenta", 5, 6),
]


levels = [
    Level(sprites=_level1_sprites, grid_size=(64, 64), data={"step_budget": 30}),
    Level(sprites=_level2_sprites, grid_size=(64, 64), data={"step_budget": 45}),
    Level(sprites=_level3_sprites, grid_size=(64, 64), data={"step_budget": 70}),
]


# ==============================================================
# 4. HUD WIDGET
# ==============================================================

class StepCounterHud(RenderableUserDisplay):
    def __init__(self):
        self._budget = 1
        self._remaining = 1

    def set_state(self, budget, remaining):
        self._budget = max(1, budget)
        self._remaining = max(0, min(remaining, self._budget))

    def render_interface(self, frame):
        ratio = self._remaining / self._budget
        bar_len = round(64 * ratio)
        for x in range(64):
            frame[0, x] = 4 if x < bar_len else 2
        return frame


class MixingLegendHud(RenderableUserDisplay):
    """Renders 0..3 8x8 formula blocks in the bottom 8 rows of the
    frame. Each block stacks the two input pigment swatches as 4x4
    quadrants on the left (top input, bottom input) with the resulting
    mixed colour as a 4x8 column on the right — communicating the
    mixing rules visually without symbols, letters, or arrow glyphs.

    The active entry list is set per-level by the game class so that
    only the formulas the current level actually requires are shown.
    """

    LEGEND_TOP_Y = 56
    LEGEND_BLOCK = 8

    def __init__(self):
        self._entries = []  # list of (input1_color, input2_color, result_color)

    def set_entries(self, entries):
        self._entries = list(entries)

    def render_interface(self, frame):
        if not self._entries:
            return frame
        n = len(self._entries)
        gap = 12
        total_w = n * self.LEGEND_BLOCK + (n - 1) * gap
        left_margin = (64 - total_w) // 2
        for y in range(self.LEGEND_TOP_Y, 64):
            for x in range(64):
                frame[y, x] = 2
        for entry_idx, (c1, c2, result) in enumerate(self._entries):
            x0 = left_margin + entry_idx * (self.LEGEND_BLOCK + gap)
            y0 = self.LEGEND_TOP_Y
            for y in range(y0, y0 + 4):
                for x in range(x0, x0 + 4):
                    frame[y, x] = c1
            for y in range(y0 + 4, y0 + 8):
                for x in range(x0, x0 + 4):
                    frame[y, x] = c2
            for y in range(y0, y0 + 8):
                for x in range(x0 + 4, x0 + 8):
                    frame[y, x] = result
        return frame


# Map a 2-pigment subset mask to its formula entry (input1, input2, result).
_FORMULA_FOR_MASK = {
    3: (12, 7, 14),    # {orange, pink}      -> green   (palette 14)
    5: (12, 10, 15),   # {orange, lightblue} -> purple  (palette 15)
    6: (7, 10, 6),     # {pink, lightblue}   -> magenta (palette 6)
}


# ==============================================================
# 5. THE GAME CLASS
# ==============================================================

class Fw8c(NovaBaseGame):
    def __init__(self):
        self._step_hud = StepCounterHud()
        self._legend_hud = MixingLegendHud()
        self._pigment_set = 0
        self._budget = 0
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_hud, self._legend_hud],
        )
        super().__init__(
            game_id="fw8c",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    def on_set_level(self, level: Level) -> None:
        self._pigment_set = 0
        self._budget = level.get_data("step_budget") or 30
        self._step_hud.set_state(self._budget, self._budget)
        carrier = self._get_carrier()
        if carrier is not None:
            self._retint_carrier(carrier)
        self._update_doors()
        self._update_legend(level)

    def _update_legend(self, level: Level) -> None:
        needed_masks = set()
        for slot in level.get_sprites_by_tag("slot"):
            for tag in slot.tags:
                mask = SLOT_DEMANDS.get(tag)
                if mask is not None and bin(mask).count("1") >= 2 and mask in _FORMULA_FOR_MASK:
                    needed_masks.add(mask)
        for door in level.get_sprites_by_tag("door"):
            for tag in door.tags:
                mask = DOOR_DEMANDS.get(tag)
                if mask is not None and mask in _FORMULA_FOR_MASK:
                    needed_masks.add(mask)
        entries = [_FORMULA_FOR_MASK[m] for m in sorted(needed_masks)]
        self._legend_hud.set_entries(entries)

    def _get_carrier(self):
        cs = self.current_level.get_sprites_by_tag("carrier")
        return cs[0] if cs else None

    def _retint_carrier(self, carrier):
        target = MIXING_TABLE[self._pigment_set]
        base = np.array(_carrier_base_pixels, dtype=carrier.pixels.dtype)
        fresh = base.copy()
        fresh[fresh == 1] = target
        carrier.pixels = fresh

    def _update_doors(self):
        for door in self.current_level.get_sprites_by_tag("door"):
            demand = None
            for tag in door.tags:
                if tag in DOOR_DEMANDS:
                    demand = DOOR_DEMANDS[tag]
                    break
            if demand is None:
                continue
            if self._pigment_set == demand:
                door.set_interaction(InteractionMode.REMOVED)
            else:
                door.set_interaction(InteractionMode.TANGIBLE)

    def _is_blocked(self, dest_px, dest_py):
        # Check center of the destination cell against walls and tangible doors.
        for wall in self.current_level.get_sprites_by_tag("wall"):
            if (wall.x <= dest_px < wall.x + wall.width and
                    wall.y <= dest_py < wall.y + wall.height):
                return True
        for door in self.current_level.get_sprites_by_tag("door"):
            if door.interaction != InteractionMode.TANGIBLE:
                continue
            if (door.x <= dest_px < door.x + door.width and
                    door.y <= dest_py < door.y + door.height):
                return True
        return False

    def _move_carrier(self, dx_cells, dy_cells):
        carrier = self._get_carrier()
        if carrier is None:
            return
        self._update_doors()
        new_x = carrier.x + dx_cells * STEP_SIZE
        new_y = carrier.y + dy_cells * STEP_SIZE
        if new_x < SPRITE_INSET or new_y < SPRITE_INSET:
            return
        if new_x > 7 * STEP_SIZE or new_y > 7 * STEP_SIZE:
            return
        check_px = new_x + STEP_SIZE // 2 - SPRITE_INSET
        check_py = new_y + STEP_SIZE // 2 - SPRITE_INSET
        if self._is_blocked(check_px, check_py):
            return
        carrier.set_position(new_x, new_y)
        for pad in self.current_level.get_sprites_by_tag("pad"):
            if pad.x == new_x and pad.y == new_y:
                for tag in pad.tags:
                    if tag in PAD_PIGMENTS:
                        self._pigment_set |= PAD_PIGMENTS[tag]
                        break
        self._retint_carrier(carrier)
        for slot in list(self.current_level.get_sprites_by_tag("slot")):
            if slot.interaction == InteractionMode.REMOVED:
                continue
            if slot.x == new_x and slot.y == new_y:
                demand = None
                for tag in slot.tags:
                    if tag in SLOT_DEMANDS:
                        demand = SLOT_DEMANDS[tag]
                        break
                if demand is not None and demand == self._pigment_set:
                    consumed = sprites["slot_consumed"].clone().set_position(slot.x, slot.y)
                    self.current_level.add_sprite(consumed)
                    slot.set_interaction(InteractionMode.REMOVED)
                    self._pigment_set = 0
                    self._retint_carrier(carrier)
        self._update_doors()

    def _check_win(self):
        for slot in self.current_level.get_sprites_by_tag("slot"):
            if slot.interaction != InteractionMode.REMOVED:
                return False
        return True

    def step(self) -> None:
        if self._action_count >= self._budget:
            self.lose()
            self.complete_action()
            return
        if self.action.id in (
            GameAction.ACTION1,
            GameAction.ACTION2,
            GameAction.ACTION3,
            GameAction.ACTION4,
        ):
            dx, dy = 0, 0
            if self.action.id == GameAction.ACTION1:
                dy = -1
            elif self.action.id == GameAction.ACTION2:
                dy = 1
            elif self.action.id == GameAction.ACTION3:
                dx = -1
            elif self.action.id == GameAction.ACTION4:
                dx = 1
            self._move_carrier(dx, dy)
        remaining_after = self._budget - (self._action_count + 1)
        self._step_hud.set_state(self._budget, max(0, remaining_after))
        if self._check_win():
            self.next_level()
            self.complete_action()
            return
        if remaining_after <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((1, 4), dtype=np.int16)
        out[0, 0] = self._pigment_set
        out[0, 1] = max(0, self._budget - self._action_count)
        return out

    def _get_valid_actions(self):
        return super()._get_valid_actions()
