"""rt9k generated game source."""

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

# Palette assignments (per spec § 3, see also skills/global/color-legend.md):
#   1  off-white  — playfield background
#   3  grey       — wall inner highlight, goal_plain outer ring
#   5  black      — wall outer + filter outer + sprite cores
#   6  magenta    — tone 0
#   11 yellow     — tone 1, goal_yellow outer ring
#   14 green      — tone 2 + step-counter HUD fill

sprites = {
    "avatar": Sprite(
        pixels=[
            [-1, 6, 6, -1],
            [6, 5, 5, 6],
            [6, 5, 5, 6],
            [-1, 6, 6, -1],
        ],
        name="avatar",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=2,
    ),
    "wall_solid": Sprite(
        pixels=[
            [5, 5, 5, 5],
            [5, 3, 3, 5],
            [5, 3, 3, 5],
            [5, 5, 5, 5],
        ],
        name="wall_solid",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=1,
    ),
    "filter_magenta": Sprite(
        pixels=[
            [5, 5, 5, 5],
            [5, 6, 6, 5],
            [5, 6, 6, 5],
            [5, 5, 5, 5],
        ],
        name="filter_magenta",
        visible=True,
        collidable=True,
        tags=["filter", "filter_magenta"],
        layer=1,
    ),
    "filter_yellow": Sprite(
        pixels=[
            [5, 5, 5, 5],
            [5, 11, 11, 5],
            [5, 11, 11, 5],
            [5, 5, 5, 5],
        ],
        name="filter_yellow",
        visible=True,
        collidable=True,
        tags=["filter", "filter_yellow"],
        layer=1,
    ),
    "filter_green": Sprite(
        pixels=[
            [5, 5, 5, 5],
            [5, 14, 14, 5],
            [5, 14, 14, 5],
            [5, 5, 5, 5],
        ],
        name="filter_green",
        visible=True,
        collidable=True,
        tags=["filter", "filter_green"],
        layer=1,
    ),
    "goal_plain": Sprite(
        pixels=[
            [3, 3, 3, 3],
            [3, 5, 5, 3],
            [3, 5, 5, 3],
            [3, 3, 3, 3],
        ],
        name="goal_plain",
        visible=True,
        collidable=False,
        tags=["goal", "goal_any"],
        layer=0,
    ),
    "goal_yellow": Sprite(
        pixels=[
            [11, 11, 11, 11],
            [11, 5, 5, 11],
            [11, 5, 5, 11],
            [11, 11, 11, 11],
        ],
        name="goal_yellow",
        visible=True,
        collidable=False,
        tags=["goal", "goal_yellow"],
        layer=0,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS — exactly 3 entries (per skills/design-constraints/composition-and-tutorial.md)
# ---------------------------------------------------------------------


def _level_1_sprites():
    """Tutorial: avatar + single full-height solid wall + plain goal."""
    placed = []
    # Avatar at logical (4, 7) → pixel (16, 28).
    placed.append(sprites["avatar"].clone().set_position(16, 28))
    # Solid wall: logical col 8 → pixel x=32, every row 0..14 → pixel y=0,4,...,56.
    for row in range(15):
        placed.append(sprites["wall_solid"].clone().set_position(32, row * 4))
    # Plain goal at logical (11, 7) → pixel (44, 28).
    placed.append(sprites["goal_plain"].clone().set_position(44, 28))
    return placed


def _level_2_sprites():
    """Adds tone-cycle (implicit on wrap) and a green filter column."""
    placed = []
    # Avatar at logical (1, 1) → pixel (4, 4).
    placed.append(sprites["avatar"].clone().set_position(4, 4))
    # Solid mid-wall column 8 (full height).
    for row in range(15):
        placed.append(sprites["wall_solid"].clone().set_position(32, row * 4))
    # Green filter column 14 (full height).
    for row in range(15):
        placed.append(sprites["filter_green"].clone().set_position(56, row * 4))
    # Plain goal at logical (13, 13) → pixel (52, 52).
    placed.append(sprites["goal_plain"].clone().set_position(52, 52))
    return placed


def _level_3_sprites():
    """Adds yellow filter row + tone-keyed goal."""
    placed = []
    # Avatar at logical (1, 7) → pixel (4, 28).
    placed.append(sprites["avatar"].clone().set_position(4, 28))
    # Solid mid-wall column 8 (full height).
    for row in range(15):
        placed.append(sprites["wall_solid"].clone().set_position(32, row * 4))
    # Green filter column 14 (full height).
    for row in range(15):
        placed.append(sprites["filter_green"].clone().set_position(56, row * 4))
    # Yellow filter row 14 (cols 9..13 → pixel x=36..52 step 4). Col 14 is
    # left to the green filter column to avoid an ambiguous overlap cell at
    # (56, 56) where two `filter` sprites would otherwise coincide; the
    # witness exercises yellow filter at (52, 56) = col 13.
    for col in range(9, 14):
        placed.append(sprites["filter_yellow"].clone().set_position(col * 4, 56))
    # Tone-keyed goal at logical (13, 7) → pixel (52, 28).
    placed.append(sprites["goal_yellow"].clone().set_position(52, 28))
    return placed


levels = [
    Level(
        sprites=_level_1_sprites(),
        grid_size=(64, 60),
        data={"step_budget": 30},
    ),
    Level(
        sprites=_level_2_sprites(),
        grid_size=(64, 60),
        data={"step_budget": 50},
    ),
    Level(
        sprites=_level_3_sprites(),
        grid_size=(64, 60),
        data={"step_budget": 70},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 1
PADDING_COLOR = 1
STRIDE = 4
GRID_W = 64
GRID_H = 60

TONE_MAGENTA = 0
TONE_YELLOW = 1
TONE_GREEN = 2

# Tone index → palette colour used in visible sprites.
TONE_TO_PALETTE = {
    TONE_MAGENTA: 6,
    TONE_YELLOW: 11,
    TONE_GREEN: 14,
}

# Tone index → tag suffix for filter sprites.
TONE_TO_TAG = {
    TONE_MAGENTA: "filter_magenta",
    TONE_YELLOW: "filter_yellow",
    TONE_GREEN: "filter_green",
}

HUD_FILL_COLOUR = 14
HUD_EMPTY_COLOUR = 5


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
        filled_pixels = round(64 * ratio)
        for hud_row in range(60, 64):
            for x in range(64):
                if x < filled_pixels:
                    frame[hud_row, x] = HUD_FILL_COLOUR
                else:
                    frame[hud_row, x] = HUD_EMPTY_COLOUR
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------


class Rt9k(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_hud = StepCounterHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_hud],
        )
        super().__init__(
            game_id="rt9k",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )
        self._tone = TONE_MAGENTA
        self._step_budget = 0
        self._steps_remaining = 0

    # -- per-level setup ------------------------------------------------

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (GRID_W, GRID_H)
        self.camera.width = gw
        self.camera.height = gh

        self._step_budget = level.get_data("step_budget") or 30
        self._steps_remaining = self._step_budget
        self._step_counter_hud.configure(self._step_budget)

        # Reset avatar tint to magenta.
        avatar = self._avatar()
        old_tone_color = self._current_avatar_tint(avatar)
        if old_tone_color != TONE_TO_PALETTE[TONE_MAGENTA]:
            avatar.color_remap(old_tone_color, TONE_TO_PALETTE[TONE_MAGENTA])
        self._tone = TONE_MAGENTA

    # -- helpers --------------------------------------------------------

    def _avatar(self) -> Sprite:
        return self.current_level.get_sprites_by_tag("player")[0]

    def _current_avatar_tint(self, avatar: Sprite) -> int:
        # The avatar's body uses one of the three tone palette values;
        # corner/centre cells are -1 / palette 5. Find the tint pixel.
        pixels = avatar.pixels
        for tone_idx in (TONE_MAGENTA, TONE_YELLOW, TONE_GREEN):
            color = TONE_TO_PALETTE[tone_idx]
            if np.any(pixels == color):
                return color
        return TONE_TO_PALETTE[TONE_MAGENTA]

    def _set_tone(self, new_tone: int) -> None:
        avatar = self._avatar()
        old_color = TONE_TO_PALETTE[self._tone]
        new_color = TONE_TO_PALETTE[new_tone]
        if old_color != new_color:
            avatar.color_remap(old_color, new_color)
        self._tone = new_tone

    def _wall_at(self, x: int, y: int) -> Sprite | None:
        for s in self.current_level.get_sprites_by_tag("wall"):
            if s.x == x and s.y == y:
                return s
        return None

    def _filter_at(self, x: int, y: int) -> Sprite | None:
        for s in self.current_level.get_sprites_by_tag("filter"):
            if s.x == x and s.y == y:
                return s
        return None

    def _filter_tone(self, sprite: Sprite) -> int | None:
        for tone_idx, tag in TONE_TO_TAG.items():
            if tag in sprite.tags:
                return tone_idx
        return None

    def _goal_at(self, x: int, y: int) -> Sprite | None:
        for s in self.current_level.get_sprites_by_tag("goal"):
            if s.x == x and s.y == y:
                return s
        return None

    def _goal_tone(self, sprite: Sprite) -> int | None:
        if "goal_yellow" in sprite.tags:
            return TONE_YELLOW
        # goal_any has no tone requirement.
        return None

    # -- step dispatch --------------------------------------------------

    def step(self) -> None:
        action_id = self.action.id

        if action_id == GameAction.ACTION1:
            self._attempt_move(0, -STRIDE)
        elif action_id == GameAction.ACTION2:
            self._attempt_move(0, STRIDE)
        elif action_id == GameAction.ACTION3:
            self._attempt_move(-STRIDE, 0)
        elif action_id == GameAction.ACTION4:
            self._attempt_move(STRIDE, 0)
        # Any other id falls through and just consumes a step below.

        # Every action drains exactly one step from the budget,
        # whether the move succeeded, was blocked, or was unrecognised.
        self._steps_remaining = max(0, self._steps_remaining - 1)
        self._step_counter_hud.set_remaining(self._steps_remaining)

        # Win / lose evaluation after the move resolves.
        if self._check_win():
            self.next_level()
            self.complete_action()
            return

        if self._steps_remaining == 0:
            self.lose()

        self.complete_action()

    # -- core movement + wrap + filter rule -----------------------------

    def _attempt_move(self, dx: int, dy: int) -> None:
        avatar = self._avatar()
        cur_x, cur_y = avatar.x, avatar.y
        new_x = cur_x + dx
        new_y = cur_y + dy

        # Wrap detection: if the intended cell is off the playfield in
        # the direction of motion, re-enter from the opposite edge AND
        # advance the tone in the corresponding direction.
        wrapped = False
        tone_delta = 0
        if dx < 0 and new_x < 0:
            new_x = GRID_W - STRIDE
            tone_delta = -1
            wrapped = True
        elif dx > 0 and new_x >= GRID_W:
            new_x = 0
            tone_delta = +1
            wrapped = True
        elif dy < 0 and new_y < 0:
            new_y = GRID_H - STRIDE
            tone_delta = -1
            wrapped = True
        elif dy > 0 and new_y >= GRID_H:
            new_y = 0
            tone_delta = +1
            wrapped = True

        # Compute the tone the avatar would have AFTER any wrap.
        post_tone = (self._tone + tone_delta) % 3 if wrapped else self._tone

        # Reject moves into solid walls.
        if self._wall_at(new_x, new_y) is not None:
            return

        # Reject moves into a filter that does not match the post-wrap tone.
        filter_sprite = self._filter_at(new_x, new_y)
        if filter_sprite is not None:
            wall_tone = self._filter_tone(filter_sprite)
            if wall_tone is not None and wall_tone != post_tone:
                return

        # Commit move; if a wrap happened, also commit the tone change.
        avatar.set_position(new_x, new_y)
        if wrapped:
            self._set_tone(post_tone)

    # -- predicates -----------------------------------------------------

    def _check_win(self) -> bool:
        avatar = self._avatar()
        goal = self._goal_at(avatar.x, avatar.y)
        if goal is None:
            return False
        required_tone = self._goal_tone(goal)
        if required_tone is None:
            return True
        return self._tone == required_tone

    # -- engine hooks ---------------------------------------------------

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 2), dtype=np.int16)
        state[0, 0] = self._tone
        state[0, 1] = self._steps_remaining
        return state

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()
