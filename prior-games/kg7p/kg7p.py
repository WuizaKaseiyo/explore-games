"""Game kg7p."""

import math

import numpy as np
from novaengine import (
    ActionInput,
    NovaBaseGame,
    BlockingMode,
    Camera,
    GameAction,
    InteractionMode,
    Level,
    RenderableUserDisplay,
    Sprite,
)

# ---------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------
CELL_STRIDE = 4
GRID_CELLS = 16
GRID_PX = CELL_STRIDE * GRID_CELLS  # 64

BACKGROUND_COLOR = 4
PADDING_COLOR = 4

HUD_ROW = 63
HUD_BAR_LEN = 40
HUD_FILL_COLOR = 15
HUD_EMPTY_COLOR = 4

ROTATION_FOR_DIR = {
    (CELL_STRIDE, 0): 0,           # east
    (0, CELL_STRIDE): 90,          # south
    (-CELL_STRIDE, 0): 180,        # west
    (0, -CELL_STRIDE): 270,        # north
}
DIR_FOR_ROTATION = {v: k for k, v in ROTATION_FOR_DIR.items()}


# ---------------------------------------------------------------------
# Sprite bank
# ---------------------------------------------------------------------
sprites = {
    # Avatar — light-blue body, single black outline, two-pixel green
    # "emitter" pair on its east edge in default rotation. The emitter
    # rotates with the sprite, so it always faces the avatar's last walked
    # direction.
    "avatar": Sprite(
        pixels=[
            [ 5, 10, 10,  5],
            [10, 10, 10, 14],
            [10, 10, 10, 14],
            [ 5, 10, 10,  5],
        ],
        name="avatar",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=4,
    ),
    # Basic haulable block — yellow hollow square with off-black
    # interior pip cluster. No direction lock.
    "block_basic": Sprite(
        pixels=[
            [11, 11, 11, 11],
            [11,  4,  4, 11],
            [11,  4,  4, 11],
            [11, 11, 11, 11],
        ],
        name="block_basic",
        visible=True,
        collidable=True,
        tags=["block", "block_basic"],
        layer=3,
    ),
    # Direction-locked block — yellow body with a magenta EDGE STRIP on
    # the east face in default rotation 0. The strip rotates with the
    # sprite (np.rot90 CCW): rotation 0 ⇒ east, 90 ⇒ north, 180 ⇒ west,
    # 270 ⇒ south. The strip is the haul-direction marker (where the
    # block moves), and the avatar must approach from the opposite side.
    "block_dir": Sprite(
        pixels=[
            [11, 11, 11, 11],
            [11,  4,  4,  6],
            [11,  4,  4,  6],
            [11, 11, 11, 11],
        ],
        name="block_dir",
        visible=True,
        collidable=True,
        tags=["block", "block_dir"],
        layer=3,
    ),
    # Target for basic block — blue outline with orange interior.
    "target_basic": Sprite(
        pixels=[
            [ 9,  9,  9,  9],
            [ 9, 12, 12,  9],
            [ 9, 12, 12,  9],
            [ 9,  9,  9,  9],
        ],
        name="target_basic",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target", "target_basic"],
        layer=1,
    ),
    # Target for direction-locked block — blue outline with red interior.
    "target_dir": Sprite(
        pixels=[
            [ 9,  9,  9,  9],
            [ 9,  8,  8,  9],
            [ 9,  8,  8,  9],
            [ 9,  9,  9,  9],
        ],
        name="target_dir",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target", "target_dir"],
        layer=1,
    ),
    # Wall — solid grey with sparse off-black hatch pixels.
    "wall": Sprite(
        pixels=[
            [ 3,  3,  4,  3],
            [ 3,  3,  3,  3],
            [ 3,  4,  3,  3],
            [ 3,  3,  3,  4],
        ],
        name="wall",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=2,
    ),
    # Beam indicator — hollow green ring rendered at the cell in front
    # of the avatar while the beam is on. INTANGIBLE.
    "beam_indicator": Sprite(
        pixels=[
            [14, 14, 14, 14],
            [14, -1, -1, 14],
            [14, -1, -1, 14],
            [14, 14, 14, 14],
        ],
        name="beam_indicator",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["beam"],
        layer=5,
    ),
}


def _cell(cx, cy):
    """Cell coords -> pixel coords."""
    return cx * CELL_STRIDE, cy * CELL_STRIDE


def _place(name, cx, cy, rotation=0):
    sprite = sprites[name].clone()
    px, py = _cell(cx, cy)
    sprite.set_position(px, py)
    if rotation:
        sprite.set_rotation(rotation)
    return sprite


# ---------------------------------------------------------------------
# Levels
# ---------------------------------------------------------------------
# Level 1 — base dynamic system: walk + beam-couple-haul.
# Avatar at (3, 8), block at (8, 8), target at (12, 8). Open arena.
_level_1_sprites = [
    _place("avatar", 3, 8),
    _place("target_basic", 12, 8),
    _place("block_basic", 8, 8),
]

def _recolor_pixels(sprite, mapping):
    pix = sprite.pixels.copy()
    for src, dst in mapping.items():
        pix[pix == src] = dst
    sprite.pixels = pix
    return sprite

# Level 2 — adds release-and-re-couple via two cargo+target pairs.
# Avatar at (3, 8). Orange block at (8, 8) → target_orange at (3, 8).
# Yellow block at (8, 4) → target_yellow at (8, 12).
# The orange-first order is the witness; yellow-first hits a block-on-block
# collision because yellow's south path runs through (8, 8).
_block_orange_l2 = _place("block_basic", 8, 8)
_recolor_pixels(_block_orange_l2, {11: 12})            # yellow body -> orange
_target_orange_l2 = _place("target_basic", 3, 8)
_recolor_pixels(_target_orange_l2, {12: 12, 9: 9})     # keep default (blue outline + orange interior)
_block_yellow_l2 = _place("block_basic", 8, 4)         # default yellow body
_target_yellow_l2 = _place("target_basic", 8, 12)
_recolor_pixels(_target_yellow_l2, {12: 11, 9: 6})     # interior yellow, outline magenta — pair with yellow block

_level_2_sprites = [
    _place("avatar", 3, 8),
    _block_orange_l2,
    _target_orange_l2,
    _block_yellow_l2,
    _target_yellow_l2,
]

# Level 3 — adds direction-locked blocks. Avatar at (3, 3).
# block_C at (5, 5) with magenta stripe on north edge (haul direction = north,
# avatar approaches from south); achieved via rotation 90 (CCW: east-edge
# stripe rotates to north-edge).
# block_D at (3, 5) with magenta stripe on east edge (haul east, avatar
# approaches from west); default rotation 0.
# target_C at (5, 1); target_D at (8, 5).
_level_3_sprites = [
    _place("avatar", 3, 3),
    _place("block_dir", 5, 5, rotation=90),         # stripe north -> haul north (block_C)
    _place("block_dir", 3, 5, rotation=0),          # stripe east  -> haul east  (block_D)
    _place("target_dir", 5, 1),
    _place("target_dir", 8, 5),
]

levels = [
    Level(sprites=_level_1_sprites, grid_size=(GRID_PX, GRID_PX), data={"step_budget": 40}),
    Level(sprites=_level_2_sprites, grid_size=(GRID_PX, GRID_PX), data={"step_budget": 60}),
    Level(sprites=_level_3_sprites, grid_size=(GRID_PX, GRID_PX), data={"step_budget": 80}),
]


# ---------------------------------------------------------------------
# HUD
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    """Depleting step-bar centred on row 63."""

    def __init__(self, game: "Kg7p"):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        budget = max(self.game.level_budget, 1)
        remaining = max(self.game.level_budget - self.game._action_count, 0)
        frac = remaining / budget
        fill_px = max(0, min(HUD_BAR_LEN, math.ceil(HUD_BAR_LEN * frac)))
        left_margin = (GRID_PX - HUD_BAR_LEN) // 2
        for x in range(HUD_BAR_LEN):
            if x < fill_px:
                frame[HUD_ROW, left_margin + x] = HUD_FILL_COLOR
            else:
                frame[HUD_ROW, left_margin + x] = HUD_EMPTY_COLOR
        return frame


# ---------------------------------------------------------------------
# Game class
# ---------------------------------------------------------------------
class Kg7p(NovaBaseGame):
    def __init__(self) -> None:
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
        )
        # initialise these BEFORE super().__init__ in case the HUD is set up early
        self.avatar = None
        self.facing_dir = (CELL_STRIDE, 0)  # east at start
        self.beam_on = False
        self.coupled_block = None
        self.coupled_offset = (0, 0)
        self.beam_indicator_sprite = None
        self.level_budget = 40

        super().__init__(
            game_id="kg7p",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )
        self._step_counter_ui = StepCounterHud(self)
        self.camera.replace_interface([self._step_counter_ui])

    # ---------------- per-level state ----------------
    def on_set_level(self, level: Level) -> None:
        self.level_budget = level.get_data("step_budget") or 40
        self.beam_on = False
        self.coupled_block = None
        self.coupled_offset = (0, 0)
        self.beam_indicator_sprite = None
        avatars = level.get_sprites_by_name("avatar")
        if avatars:
            self.avatar = avatars[0]
            self.avatar.set_rotation(0)  # facing east at level start
            self.facing_dir = (CELL_STRIDE, 0)

    # ---------------- helpers ----------------
    def _in_bounds(self, x: int, y: int, w: int = CELL_STRIDE, h: int = CELL_STRIDE) -> bool:
        return 0 <= x and 0 <= y and x + w <= GRID_PX and y + h <= GRID_PX

    def _blockers_at(self, x: int, y: int, exclude=()) -> list:
        """Sprites that would block at (x, y) — walls and uncoupled blocks."""
        result = []
        for sprite in self.current_level.get_sprites():
            if sprite in exclude:
                continue
            if "wall" in sprite.tags or "block" in sprite.tags:
                # Check overlap
                if sprite.x == x and sprite.y == y:
                    if sprite.interaction != InteractionMode.REMOVED:
                        result.append(sprite)
        return result

    def _block_dir_allowed_haul(self, block: Sprite) -> tuple:
        """Direction the avatar must walk to haul this coupled directional block.
        Encoded by the block's rotation: the magenta stripe sits on the haul-side
        edge. np.rot90 is CCW, so rotation 0 = stripe east, 90 = stripe north,
        180 = stripe west, 270 = stripe south."""
        rot = block.rotation % 360
        if rot == 0:
            return (CELL_STRIDE, 0)         # stripe east -> haul east
        if rot == 90:
            return (0, -CELL_STRIDE)        # stripe north -> haul north
        if rot == 180:
            return (-CELL_STRIDE, 0)        # stripe west -> haul west
        if rot == 270:
            return (0, CELL_STRIDE)         # stripe south -> haul south
        return (CELL_STRIDE, 0)

    def _try_couple(self) -> None:
        """If beam is on and there is a block in the cell in front of the avatar,
        couple it (subject to direction-lock check)."""
        if not self.beam_on or self.coupled_block is not None or self.avatar is None:
            return
        dx, dy = self.facing_dir
        front_x = self.avatar.x + dx
        front_y = self.avatar.y + dy
        for sprite in self.current_level.get_sprites():
            if "block" in sprite.tags and sprite.x == front_x and sprite.y == front_y:
                if sprite.interaction == InteractionMode.REMOVED:
                    continue
                if "block_dir" in sprite.tags:
                    # direction-lock check: beam direction must match the block's
                    # allowed haul direction.
                    allowed = self._block_dir_allowed_haul(sprite)
                    if (dx, dy) != allowed:
                        continue
                self.coupled_block = sprite
                self.coupled_offset = (sprite.x - self.avatar.x, sprite.y - self.avatar.y)
                sprite.set_layer(4)
                return

    def _update_beam_indicator(self) -> None:
        """Spawn or move the beam_indicator to the cell in front of the avatar."""
        if not self.beam_on or self.avatar is None:
            return
        dx, dy = self.facing_dir
        front_x = self.avatar.x + dx
        front_y = self.avatar.y + dy
        if self.beam_indicator_sprite is None:
            self.beam_indicator_sprite = sprites["beam_indicator"].clone()
            self.current_level.add_sprite(self.beam_indicator_sprite)
        self.beam_indicator_sprite.set_position(front_x, front_y)

    def _remove_beam_indicator(self) -> None:
        if self.beam_indicator_sprite is not None:
            try:
                self.current_level.remove_sprite(self.beam_indicator_sprite)
            except Exception:
                pass
            self.beam_indicator_sprite = None

    def _check_win(self) -> bool:
        """Every block sits at the same (x, y) as a tag-matching target."""
        for sprite in self.current_level.get_sprites():
            if "block" not in sprite.tags or sprite.interaction == InteractionMode.REMOVED:
                continue
            target_tag = "target_dir" if "block_dir" in sprite.tags else "target_basic"
            matched = False
            for t in self.current_level.get_sprites_by_tag(target_tag):
                if t.x == sprite.x and t.y == sprite.y:
                    matched = True
                    break
            if not matched:
                return False
        return True

    # ---------------- step ----------------
    def step(self) -> None:
        # Lose check first
        if self._action_count >= self.level_budget:
            self.lose()
            self.complete_action()
            return

        if self.action.id == GameAction.ACTION5:
            # Toggle beam
            if self.beam_on:
                # release
                self.beam_on = False
                if self.coupled_block is not None:
                    self.coupled_block.set_layer(3)
                    self.coupled_block = None
                    self.coupled_offset = (0, 0)
                self._remove_beam_indicator()
            else:
                self.beam_on = True
                self._update_beam_indicator()
                self._try_couple()
            if self._check_win():
                self.next_level()
            self.complete_action()
            return

        # Walk actions
        direction = None
        if self.action.id == GameAction.ACTION1:
            direction = (0, -CELL_STRIDE)
        elif self.action.id == GameAction.ACTION2:
            direction = (0, CELL_STRIDE)
        elif self.action.id == GameAction.ACTION3:
            direction = (-CELL_STRIDE, 0)
        elif self.action.id == GameAction.ACTION4:
            direction = (CELL_STRIDE, 0)

        if direction is None:
            self.complete_action()
            return

        dx, dy = direction
        # Avatar always re-faces to the pressed direction even if move rejected.
        new_rotation = ROTATION_FOR_DIR[direction]
        if self.avatar is not None:
            self.avatar.set_rotation(new_rotation)
        self.facing_dir = direction

        # Update beam indicator to follow new facing, and attempt to couple
        # to any block in the new beam cell BEFORE the collision check —
        # otherwise turning to face a block would always be rejected as
        # "uncoupled block in destination" and the player could never couple.
        if self.beam_on:
            self._update_beam_indicator()
            if self.coupled_block is None:
                self._try_couple()

        # If coupled to a directional block, check that the walk matches its allowed haul direction.
        if self.coupled_block is not None and "block_dir" in self.coupled_block.tags:
            allowed = self._block_dir_allowed_haul(self.coupled_block)
            if direction != allowed:
                # Walk rejected by direction-lock. Avatar still rotates.
                if self.beam_on:
                    self._update_beam_indicator()
                self.complete_action()
                return

        # Compute avatar destination
        ax = self.avatar.x + dx
        ay = self.avatar.y + dy
        if not self._in_bounds(ax, ay):
            if self.beam_on:
                self._update_beam_indicator()
            self.complete_action()
            return

        # Excluded sprites from collision checks for the avatar
        avatar_exclude = [self.avatar]
        if self.coupled_block is not None:
            avatar_exclude.append(self.coupled_block)

        avatar_blockers = self._blockers_at(ax, ay, exclude=avatar_exclude)
        if avatar_blockers:
            if self.beam_on:
                self._update_beam_indicator()
            self.complete_action()
            return

        # If coupled, check block destination
        if self.coupled_block is not None:
            bx = self.coupled_block.x + dx
            by = self.coupled_block.y + dy
            if not self._in_bounds(bx, by):
                if self.beam_on:
                    self._update_beam_indicator()
                self.complete_action()
                return
            block_blockers = self._blockers_at(bx, by, exclude=[self.avatar, self.coupled_block])
            if block_blockers:
                if self.beam_on:
                    self._update_beam_indicator()
                self.complete_action()
                return

        # Commit: move avatar (and coupled block) together
        self.avatar.move(dx, dy)
        if self.coupled_block is not None:
            self.coupled_block.move(dx, dy)

        # Update beam, attempt couple if not already coupled
        if self.beam_on:
            self._update_beam_indicator()
            if self.coupled_block is None:
                self._try_couple()

        # Win check
        if self._check_win():
            self.next_level()

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self.level_budget - self._action_count
        state[0, 1] = 1 if self.beam_on else 0
        state[0, 2] = 1 if self.coupled_block is not None else 0
        return state

    def _get_valid_actions(self) -> list:
        return super()._get_valid_actions()
