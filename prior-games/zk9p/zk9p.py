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

def _make_floor(size: int) -> list[list[int]]:
    pixels = [[4 for _ in range(size)] for _ in range(size)]
    for y in range(size):
        for x in range(size):
            if (x * 3 + y * 5) % 7 == 0:
                pixels[y][x] = 3
    return pixels


sprites = {
    "avatar": Sprite(
        pixels=[[6]],
        name="avatar",
        visible=True,
        collidable=True,
        tags=["avatar"],
        layer=3,
    ),
    "floor_14": Sprite(
        pixels=_make_floor(14),
        name="floor_14",
        visible=True,
        collidable=False,
        tags=["floor"],
        layer=-1,
    ),
    "floor_16": Sprite(
        pixels=_make_floor(16),
        name="floor_16",
        visible=True,
        collidable=False,
        tags=["floor"],
        layer=-1,
    ),
    "floor_18": Sprite(
        pixels=_make_floor(18),
        name="floor_18",
        visible=True,
        collidable=False,
        tags=["floor"],
        layer=-1,
    ),
    "pursuer_cyan": Sprite(
        pixels=[[10]],
        name="pursuer_cyan",
        visible=True,
        collidable=True,
        tags=["pursuer", "pursuer_orthogonal"],
        layer=2,
    ),
    "pursuer_green": Sprite(
        pixels=[[14]],
        name="pursuer_green",
        visible=True,
        collidable=True,
        tags=["pursuer", "pursuer_phase"],
        layer=2,
    ),
    "pursuer_red": Sprite(
        pixels=[[8]],
        name="pursuer_red",
        visible=True,
        collidable=True,
        tags=["pursuer", "pursuer_manhattan"],
        layer=2,
    ),
    "pursuer_yellow": Sprite(
        pixels=[[11]],
        name="pursuer_yellow",
        visible=True,
        collidable=True,
        tags=["pursuer", "pursuer_manhattan"],
        layer=2,
    ),
    "wall": Sprite(
        pixels=[[2]],
        name="wall",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

def _level_1_sprites() -> list[Sprite]:
    return [
        sprites["floor_14"].clone().set_position(0, 0),
        sprites["avatar"].clone().set_position(7, 10),
        sprites["pursuer_red"].clone().set_position(5, 3),
        sprites["pursuer_yellow"].clone().set_position(9, 3),
    ]


def _level_2_sprites() -> list[Sprite]:
    placed: list[Sprite] = [
        sprites["floor_16"].clone().set_position(0, 0),
        sprites["avatar"].clone().set_position(8, 13),
        sprites["pursuer_red"].clone().set_position(3, 2),
        sprites["pursuer_yellow"].clone().set_position(13, 2),
        sprites["pursuer_cyan"].clone().set_position(8, 2),
    ]
    for y in range(4, 9):
        placed.append(sprites["wall"].clone().set_position(8, y))
    for y in range(10, 12):
        placed.append(sprites["wall"].clone().set_position(8, y))
    return placed


def _level_3_sprites() -> list[Sprite]:
    placed: list[Sprite] = [
        sprites["floor_18"].clone().set_position(0, 0),
        sprites["avatar"].clone().set_position(9, 14),
        sprites["pursuer_red"].clone().set_position(3, 2),
        sprites["pursuer_yellow"].clone().set_position(15, 2),
        sprites["pursuer_cyan"].clone().set_position(9, 2),
        sprites["pursuer_green"].clone().set_position(9, 9),
    ]
    for x in range(2, 8):
        placed.append(sprites["wall"].clone().set_position(x, 8))
    for x in range(10, 16):
        placed.append(sprites["wall"].clone().set_position(x, 8))
    for y in range(10, 15):
        placed.append(sprites["wall"].clone().set_position(4, y))
    return placed


levels = [
    Level(
        sprites=_level_1_sprites(),
        grid_size=(14, 14),
        data={"step_budget": 60},
    ),
    Level(
        sprites=_level_2_sprites(),
        grid_size=(16, 16),
        data={"step_budget": 80},
    ),
    Level(
        sprites=_level_3_sprites(),
        grid_size=(18, 18),
        data={"step_budget": 100},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 4
PADDING_COLOR = 5

PURSUER_TAG = "pursuer"
PURSUER_MANHATTAN_TAG = "pursuer_manhattan"
PURSUER_ORTHOGONAL_TAG = "pursuer_orthogonal"
PURSUER_PHASE_TAG = "pursuer_phase"
WALL_TAG = "wall"
AVATAR_TAG = "avatar"

L3_INDEX = 2  # zero-based

HUD_BAR_FILL = 7
HUD_BAR_EMPTY = 3

INITIAL_LIVES = 3
LIFE_PIP_FILL = 6
LIFE_PIP_EMPTY = 3

# Animation phase counts (engine ticks each phase holds for).
CHASE_TOTAL_FRAMES = 3
MERGE_TOTAL_FRAMES = 3
ANIM_FLASH_COLOR = 0  # palette 0 = white

PURSUER_COLORS = {
    "pursuer_red": 8,
    "pursuer_yellow": 11,
    "pursuer_cyan": 10,
    "pursuer_green": 14,
}


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    def __init__(self, budget: int) -> None:
        self.budget = budget
        self.remaining = budget

    def set_budget(self, budget: int) -> None:
        self.budget = budget
        self.remaining = budget

    def set_remaining(self, value: int) -> None:
        self.remaining = max(0, min(value, self.budget))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.budget <= 0:
            return frame
        ratio = self.remaining / self.budget
        filled = round(64 * ratio)
        for x in range(64):
            frame[63, x] = HUD_BAR_FILL if x < filled else HUD_BAR_EMPTY
        return frame


class LivesHud(RenderableUserDisplay):
    def __init__(self, max_lives: int) -> None:
        self.max_lives = max_lives
        self.lives = max_lives

    def set_lives(self, value: int) -> None:
        self.lives = max(0, min(value, self.max_lives))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        # Three pips at row 0, each 3 cells wide with 1-cell gap, starting at col 1.
        for i in range(self.max_lives):
            color = LIFE_PIP_FILL if i < self.lives else LIFE_PIP_EMPTY
            x_start = 1 + i * 4
            for x in range(x_start, x_start + 3):
                frame[0, x] = color
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------

class Zk9p(NovaBaseGame):
    def __init__(self) -> None:
        self._step_hud = StepCounterHud(60)
        self._lives_hud = LivesHud(INITIAL_LIVES)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_hud, self._lives_hud],
        )
        self._step_budget = 60
        self._step_units_used = 0
        self._tick = 0
        self._lives = INITIAL_LIVES
        self._anim_phase = "idle"
        self._anim_frame = 0
        self._chase_targets: dict[Sprite, tuple[int, int]] = {}
        self._merging_groups: list[list[Sprite]] = []
        super().__init__(
            game_id="zk9p",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    # -- per-level setup --

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        budget = level.get_data("step_budget") or 60
        self._step_budget = budget
        self._step_units_used = 0
        self._tick = 0
        self._anim_phase = "idle"
        self._anim_frame = 0
        self._chase_targets = {}
        self._merging_groups = []
        self._step_hud.set_budget(budget)
        self._lives_hud.set_lives(self._lives)
        self._update_phase_interaction()

    # -- death + respawn --

    def _respawn_current_level(self) -> None:
        """Restore the current level to its pristine state and re-init."""
        idx = self._current_level_index
        self._levels[idx] = self._clean_levels[idx].clone()
        self.on_set_level(self.current_level)

    def _die(self) -> None:
        """Decrement lives; respawn if any remain, else lose the game."""
        self._lives -= 1
        self._lives_hud.set_lives(self._lives)
        self._anim_phase = "idle"
        self._anim_frame = 0
        self._chase_targets = {}
        self._merging_groups = []
        if self._lives <= 0:
            self.lose()
            return
        self._respawn_current_level()

    # -- helpers --

    def _level_index(self) -> int:
        return self._current_level_index

    def _walls(self) -> set[tuple[int, int]]:
        return {(s.x, s.y) for s in self.current_level.get_sprites_by_tag(WALL_TAG)}

    def _avatar(self) -> Sprite:
        return self.current_level.get_sprites_by_tag(AVATAR_TAG)[0]

    def _live_pursuers(self) -> list[Sprite]:
        return [
            s
            for s in self.current_level.get_sprites_by_tag(PURSUER_TAG)
            if s.interaction != InteractionMode.REMOVED
        ]

    def _phase_intangible_at(self, tick: int) -> bool:
        return tick % 2 == 1

    def _update_phase_interaction(self) -> None:
        intangible_now = self._phase_intangible_at(self._tick)
        for p in self.current_level.get_sprites_by_tag(PURSUER_TAG):
            if p.interaction == InteractionMode.REMOVED:
                continue
            if PURSUER_PHASE_TAG in p.tags:
                if intangible_now:
                    p.set_interaction(InteractionMode.INTANGIBLE)
                else:
                    p.set_interaction(InteractionMode.TANGIBLE)

    # -- avatar movement --

    def _move_avatar(self, dx: int, dy: int) -> None:
        avatar = self._avatar()
        gw, gh = self.current_level.grid_size or (64, 64)
        new_x = avatar.x + dx
        new_y = avatar.y + dy
        if not (0 <= new_x < gw and 0 <= new_y < gh):
            return
        if (new_x, new_y) in self._walls():
            return
        avatar.set_position(new_x, new_y)

    # -- pursuer chase --

    def _chase_step(self, pursuer: Sprite) -> tuple[int, int]:
        avatar = self._avatar()
        dx_total = avatar.x - pursuer.x
        dy_total = avatar.y - pursuer.y
        if dx_total == 0 and dy_total == 0:
            return (0, 0)
        if PURSUER_ORTHOGONAL_TAG in pursuer.tags:
            return self._orthogonal_step(dx_total, dy_total)
        return self._manhattan_step(dx_total, dy_total)

    def _manhattan_step(self, dx_total: int, dy_total: int) -> tuple[int, int]:
        if dx_total != 0 and abs(dx_total) >= abs(dy_total):
            return (1 if dx_total > 0 else -1, 0)
        if dy_total != 0:
            return (0, 1 if dy_total > 0 else -1)
        return (0, 0)

    def _orthogonal_step(self, dx_total: int, dy_total: int) -> tuple[int, int]:
        if dx_total != 0 and dy_total != 0:
            if abs(dx_total) < abs(dy_total):
                return (1 if dx_total > 0 else -1, 0)
            if abs(dy_total) < abs(dx_total):
                return (0, 1 if dy_total > 0 else -1)
            return (0, 1 if dy_total > 0 else -1)
        if dx_total != 0:
            return (1 if dx_total > 0 else -1, 0)
        return (0, 1 if dy_total > 0 else -1)

    def _plan_chase_targets(self) -> None:
        """Compute every live pursuer's intended next-cell. Stored in
        `self._chase_targets` so the chase animation can render the pursuer
        at its OLD position for several frames before snapping to NEW."""
        gw, gh = self.current_level.grid_size or (64, 64)
        walls = self._walls()
        self._chase_targets = {}
        for p in self._live_pursuers():
            dx, dy = self._chase_step(p)
            new_x = p.x + dx
            new_y = p.y + dy
            if not (0 <= new_x < gw and 0 <= new_y < gh):
                self._chase_targets[p] = (p.x, p.y)
                continue
            if (new_x, new_y) in walls:
                self._chase_targets[p] = (p.x, p.y)
                continue
            self._chase_targets[p] = (new_x, new_y)

    def _flash_pursuers(self, pursuers) -> None:
        for p in pursuers:
            if p.interaction == InteractionMode.REMOVED:
                continue
            p.color_remap(None, ANIM_FLASH_COLOR)

    def _restore_pursuer_color(self, pursuer: Sprite) -> None:
        orig = PURSUER_COLORS.get(pursuer.name)
        if orig is not None:
            pursuer.color_remap(None, orig)

    def _apply_chase_targets(self) -> None:
        for p, (nx, ny) in self._chase_targets.items():
            if p.interaction == InteractionMode.REMOVED:
                continue
            p.set_position(nx, ny)
            self._restore_pursuer_color(p)

    def _detect_merge_groups(self) -> list[list[Sprite]]:
        cell_to_pursuers: dict[tuple[int, int], list[Sprite]] = {}
        for p in self._live_pursuers():
            cell_to_pursuers.setdefault((p.x, p.y), []).append(p)
        return [group for group in cell_to_pursuers.values() if len(group) >= 2]

    def _commit_merges(self) -> None:
        for group in self._merging_groups:
            for p in group:
                p.set_interaction(InteractionMode.REMOVED)
        self._merging_groups = []
        self._update_phase_interaction()

    # -- end-of-action checks --

    def _check_caught(self) -> bool:
        avatar = self._avatar()
        for p in self.current_level.get_sprites_by_tag(PURSUER_TAG):
            if p.interaction != InteractionMode.TANGIBLE:
                continue
            if p.x == avatar.x and p.y == avatar.y:
                return True
        return False

    def _check_won(self) -> bool:
        for p in self.current_level.get_sprites_by_tag(PURSUER_TAG):
            if p.interaction != InteractionMode.REMOVED:
                return False
        return True

    def _consume_step(self, units: int) -> None:
        self._step_units_used += units
        self._step_hud.set_remaining(self._step_budget - self._step_units_used)

    # -- main step (multi-frame animation phase machine) --

    def step(self) -> None:
        if self._anim_phase == "chase":
            self._tick_chase_animation()
            return
        if self._anim_phase == "merge":
            self._tick_merge_animation()
            return
        # idle: process new player action
        self._begin_new_action()

    def _begin_new_action(self) -> None:
        action_id = self.action.id
        is_l3 = self._level_index() == L3_INDEX
        is_movement = action_id in (
            GameAction.ACTION1,
            GameAction.ACTION2,
            GameAction.ACTION3,
            GameAction.ACTION4,
        )
        is_l3_skip = action_id == GameAction.ACTION5 and is_l3
        is_noop_skip = action_id == GameAction.ACTION5 and not is_l3

        if is_noop_skip:
            # ACTION5 in L1/L2 is a 1-unit no-op; no animation needed.
            self._consume_step(1)
            self._maybe_terminate_or_complete()
            return

        if not (is_movement or is_l3_skip):
            self.complete_action()
            return

        # Tick advance + green parity update.
        self._tick += 1
        self._update_phase_interaction()

        # Avatar move (ACTION5 in L3 keeps the avatar stationary).
        if action_id == GameAction.ACTION1:
            self._move_avatar(0, -1)
        elif action_id == GameAction.ACTION2:
            self._move_avatar(0, 1)
        elif action_id == GameAction.ACTION3:
            self._move_avatar(-1, 0)
        elif action_id == GameAction.ACTION4:
            self._move_avatar(1, 0)

        # Step counter cost.
        units = 2 if is_l3_skip else 1
        self._consume_step(units)

        # Plan pursuer targets and start chase animation. Pursuers stay
        # at their OLD cells visually for the duration of the chase phase
        # so the player can read which pursuer reacted to which avatar
        # position. Their colours are flashed white during the phase.
        self._plan_chase_targets()
        self._flash_pursuers(self._chase_targets.keys())
        self._anim_phase = "chase"
        self._anim_frame = 0

    def _tick_chase_animation(self) -> None:
        # Each frame holds the flashed-pursuers-at-old-position visual.
        # The snap-to-new + colour-restore happens on the last frame so
        # the animation totals CHASE_TOTAL_FRAMES engine ticks (frame 0
        # is rendered by `_begin_new_action`'s initial flash).
        self._anim_frame += 1
        if self._anim_frame < CHASE_TOTAL_FRAMES - 1:
            return

        # Snap to new positions and restore colours.
        self._apply_chase_targets()

        # Caught check fires before merges resolve so a pursuer landing on
        # the avatar always ends the level (the merge animation, if any,
        # is skipped so the death is unambiguous).
        if self._check_caught():
            self._die()
            self.complete_action()
            return

        # Detect merges. If any cell now has 2+ pursuers, transition to
        # the merge animation phase; otherwise terminate the action.
        self._merging_groups = self._detect_merge_groups()
        if self._merging_groups:
            # Brighten the merging pursuers right away so the merge frame
            # 0 already reads as "these are about to vanish".
            merging_sprites = [p for grp in self._merging_groups for p in grp]
            self._flash_pursuers(merging_sprites)
            self._anim_phase = "merge"
            self._anim_frame = 0
            return

        self._anim_phase = "idle"
        self._maybe_terminate_or_complete()

    def _tick_merge_animation(self) -> None:
        # Hold the flashed-merging-pursuers visual for several frames so
        # the player can read which pursuers collided, then commit the
        # removal on the final frame.
        self._anim_frame += 1
        if self._anim_frame < MERGE_TOTAL_FRAMES - 1:
            return
        self._commit_merges()
        self._anim_phase = "idle"
        self._maybe_terminate_or_complete()

    def _maybe_terminate_or_complete(self) -> None:
        if self._check_won():
            self.next_level()
            self.complete_action()
            return
        if self._step_units_used >= self._step_budget:
            self._die()
            self.complete_action()
            return
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((4, 4), dtype=np.int16)
        out[0, 0] = self._step_budget - self._step_units_used
        out[0, 1] = sum(
            1
            for p in self.current_level.get_sprites_by_tag(PURSUER_TAG)
            if p.interaction != InteractionMode.REMOVED
        )
        out[0, 2] = self._tick
        return out
