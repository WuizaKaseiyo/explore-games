"""NovaPlay generated game lv4k."""

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

sprites = {
    "beam_segment": Sprite(
        pixels=[
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 3, 3, 3, 3, 3, 3, 1],
            [1, 3, 3, 3, 3, 3, 3, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ],
        name="beam_segment",
        visible=True,
        collidable=True,
        tags=["beam_slot"],
    ),
    "fulcrum_post": Sprite(
        pixels=[
            [-1, -1, 4, 4, 4, 4, -1, -1],
            [-1, 4, 4, 4, 4, 4, 4, -1],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 5, 5, 5, 5, 4, 4],
            [4, 4, 5, 5, 5, 5, 4, 4],
            [4, 4, 5, 5, 5, 5, 4, 4],
            [4, 4, 5, 5, 5, 5, 4, 4],
            [4, 4, 5, 5, 5, 5, 4, 4],
            [4, 4, 5, 5, 5, 5, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="fulcrum_post",
        visible=True,
        collidable=False,
        tags=["fulcrum"],
    ),
    "passenger": Sprite(
        pixels=[
            [-1, 12, 12, -1],
            [12, 5, 5, 12],
            [12, 5, 5, 12],
            [-1, 12, 12, -1],
        ],
        name="passenger",
        visible=True,
        collidable=False,
        tags=["passenger"],
        layer=2,
    ),
    "tray_slot_small": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4],
            [4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4],
            [4, 4, 4, 4, 4, 4],
        ],
        name="tray_slot_small",
        visible=True,
        collidable=False,
        tags=["tray_slot"],
    ),
    "tray_slot_wide": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="tray_slot_wide",
        visible=True,
        collidable=False,
        tags=["tray_slot"],
    ),
    "weight_blue": Sprite(
        pixels=[
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 5, 5, 5, 5, 5, 5, 9],
            [9, 5, 5, 5, 5, 5, 5, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
        ],
        name="weight_blue",
        visible=True,
        collidable=True,
        tags=["weight", "weight_mass2"],
        layer=1,
    ),
    "weight_orange": Sprite(
        pixels=[
            [12, 12, 12, 12],
            [12, 5, 5, 12],
            [12, 5, 5, 12],
            [12, 12, 12, 12],
        ],
        name="weight_orange",
        visible=True,
        collidable=True,
        tags=["weight", "weight_mass1"],
        layer=1,
    ),
}

# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

levels = [
    # L1: 4 placement slots at arms {-2, -1, +1, +2}; fulcrum-x = 32; tray = 2 mass-1 weights.
    Level(
        sprites=[
            sprites["beam_segment"].clone().set_position(16, 24),
            sprites["beam_segment"].clone().set_position(24, 24),
            sprites["beam_segment"].clone().set_position(40, 24),
            sprites["beam_segment"].clone().set_position(48, 24),
            sprites["fulcrum_post"].clone().set_position(32, 28),
            sprites["tray_slot_small"].clone().set_position(4, 44),
            sprites["tray_slot_small"].clone().set_position(16, 44),
            sprites["weight_orange"].clone().set_position(5, 45),
            sprites["weight_orange"].clone().set_position(17, 45),
        ],
        grid_size=(64, 64),
    ),
    # L2: 6 placement slots at arms {-3..-1, +1..+3}; fulcrum-x = 32; tray = 1 mass-2 + 2 mass-1.
    Level(
        sprites=[
            sprites["beam_segment"].clone().set_position(8, 24),
            sprites["beam_segment"].clone().set_position(16, 24),
            sprites["beam_segment"].clone().set_position(24, 24),
            sprites["beam_segment"].clone().set_position(40, 24),
            sprites["beam_segment"].clone().set_position(48, 24),
            sprites["beam_segment"].clone().set_position(56, 24),
            sprites["fulcrum_post"].clone().set_position(32, 28),
            sprites["tray_slot_wide"].clone().set_position(4, 44),
            sprites["tray_slot_small"].clone().set_position(18, 44),
            sprites["tray_slot_small"].clone().set_position(34, 44),
            sprites["weight_blue"].clone().set_position(5, 45),
            sprites["weight_orange"].clone().set_position(19, 45),
            sprites["weight_orange"].clone().set_position(35, 45),
        ],
        grid_size=(64, 64),
    ),
    # L3: 6 placement slots; tray = 3 mass-2 + 1 mass-1; passenger initially at arm +2.
    Level(
        sprites=[
            sprites["beam_segment"].clone().set_position(8, 24),
            sprites["beam_segment"].clone().set_position(16, 24),
            sprites["beam_segment"].clone().set_position(24, 24),
            sprites["beam_segment"].clone().set_position(40, 24),
            sprites["beam_segment"].clone().set_position(48, 24),
            sprites["beam_segment"].clone().set_position(56, 24),
            sprites["fulcrum_post"].clone().set_position(32, 28),
            sprites["tray_slot_small"].clone().set_position(4, 44),
            sprites["tray_slot_wide"].clone().set_position(12, 44),
            sprites["tray_slot_wide"].clone().set_position(24, 44),
            sprites["tray_slot_wide"].clone().set_position(36, 44),
            sprites["weight_orange"].clone().set_position(5, 45),
            sprites["weight_blue"].clone().set_position(13, 45),
            sprites["weight_blue"].clone().set_position(25, 45),
            sprites["weight_blue"].clone().set_position(37, 45),
            sprites["passenger"].clone().set_position(48, 20),
        ],
        grid_size=(64, 64),
    ),
]

# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 3
PADDING_COLOR = 4

BEAM_TOP_Y = 24
FULCRUM_X = 32
SLOT_WIDTH = 8

PALETTE_SELECTION_HIGHLIGHT = 11
PALETTE_WEIGHT_ORANGE = 12
PALETTE_WEIGHT_BLUE = 9
HUD_FILLED = 14
HUD_EMPTY = 4

EXPOSED_ARMS_BY_LEVEL = [
    [-2, -1, 1, 2],
    [-3, -2, -1, 1, 2, 3],
    [-3, -2, -1, 1, 2, 3],
]
STEP_BUDGETS = [12, 24, 36]
PASSENGER_MASS = 1
ANIM_FRAMES = 4

# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------


class StepCounterHud(RenderableUserDisplay):
    def __init__(self, budget: int) -> None:
        self.budget = budget
        self.remaining = budget

    def set_remaining(self, n: int) -> None:
        self.remaining = max(0, min(n, self.budget))

    def reset(self, budget: int) -> None:
        self.budget = budget
        self.remaining = budget

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.budget == 0:
            return frame
        filled = int(64 * self.remaining / self.budget)
        for x in range(64):
            frame[0, x] = HUD_FILLED if x < filled else HUD_EMPTY
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------


class Lv4k(NovaBaseGame):
    def __init__(self) -> None:
        self.step_hud = StepCounterHud(STEP_BUDGETS[0])
        # Initialise per-level state BEFORE super().__init__(), because the parent
        # class's __init__ calls set_level(0) which calls on_set_level, which
        # populates these attributes. If we initialise after super(), we'd
        # overwrite the just-populated state with empty defaults.
        self.selected_weight: Sprite | None = None
        self.placement: dict[int, Sprite] = {}
        self.tray_origin: dict[Sprite, tuple[int, int]] = {}
        self.passenger_arm: int | None = None
        self.passenger_sprite: Sprite | None = None
        self.beam_segments: dict[int, Sprite] = {}
        self.tray_weights: list[Sprite] = []
        self.exposed_arms: list[int] = []
        self.step_budget: int = 0
        # Passenger-slide animation state. -1 = idle.
        self._anim_phase: int = -1
        self._anim_start_xy: tuple[int, int] = (0, 0)
        self._anim_end_xy: tuple[int, int] = (0, 0)
        self._anim_target_arm: int | None = None
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_hud],
        )
        super().__init__(
            game_id="lv4k",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        self._levels[self._current_level_index] = self._clean_levels[
            self._current_level_index
        ].clone()
        level = self._levels[self._current_level_index]
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        idx = self._current_level_index
        self.exposed_arms = list(EXPOSED_ARMS_BY_LEVEL[idx])
        self.step_budget = STEP_BUDGETS[idx]
        self.step_hud.reset(self.step_budget)

        self.selected_weight = None
        self.placement = {}
        self.tray_origin = {}
        self.passenger_arm = None
        self.passenger_sprite = None
        self.beam_segments = {}
        self.tray_weights = []

        for s in level.get_sprites_by_tag("beam_slot"):
            arm = (s.x - FULCRUM_X) // SLOT_WIDTH
            self.beam_segments[arm] = s

        for s in level.get_sprites_by_tag("weight"):
            self.tray_weights.append(s)
            self.tray_origin[s] = (s.x, s.y)

        passenger_list = level.get_sprites_by_tag("passenger")
        if passenger_list:
            self.passenger_sprite = passenger_list[0]
            self.passenger_arm = (
                self.passenger_sprite.x - FULCRUM_X
            ) // SLOT_WIDTH

        self._update_visuals()

    def step(self) -> None:
        if self._anim_phase >= 0:
            self._tick_animation()
            return

        if self.action.id == GameAction.ACTION6:
            x = int(self.action.data.get("x", 0))
            y = int(self.action.data.get("y", 0))
            grid_xy = self.camera.display_to_grid(x, y)
            if grid_xy is not None:
                gx, gy = grid_xy
                self._handle_click(gx, gy)

        if self._anim_phase >= 0:
            # Click started a passenger animation; defer end-of-step
            # checks until the animation finishes.
            return

        self._finalize_step()

    def _finalize_step(self) -> None:
        self.step_hud.set_remaining(self.step_budget - self._action_count)
        if self._check_win():
            self.next_level()
            self.complete_action()
            return
        if self._action_count >= self.step_budget:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _tick_animation(self) -> None:
        self._anim_phase += 1
        sx, sy = self._anim_start_xy
        ex, ey = self._anim_end_xy
        t = self._anim_phase / ANIM_FRAMES
        cx = int(round(sx + (ex - sx) * t))
        cy = int(round(sy + (ey - sy) * t))
        if self.passenger_sprite is not None:
            self.passenger_sprite.set_position(cx, cy)
        if self._anim_phase >= ANIM_FRAMES:
            if self._anim_target_arm is not None:
                self.passenger_arm = self._anim_target_arm
            self._anim_phase = -1
            self._anim_target_arm = None
            self._update_visuals()
            self._finalize_step()

    def _handle_click(self, gx: int, gy: int) -> None:
        weight = self._find_tray_weight_at(gx, gy)
        if weight is not None:
            if self.selected_weight is weight:
                self._deselect()
            else:
                self._select_weight(weight)
            return

        # Lift a placed weight: hit-test against the underlying slot so the
        # full slot width is clickable, even when a centred mass-1 leaves
        # gaps on the slot's left/right edges.
        for arm, w in list(self.placement.items()):
            segment = self.beam_segments[arm]
            if self._beam_lane_contains(gx, gy, segment):
                self._lift_weight(arm)
                return

        if self.selected_weight is not None:
            for arm, segment in self.beam_segments.items():
                if arm in self.placement:
                    continue
                if arm not in self.exposed_arms:
                    continue
                if arm == self.passenger_arm:
                    # Passenger occupies this slot; can't share.
                    continue
                if self._beam_lane_contains(gx, gy, segment):
                    self._place_at(arm)
                    return

    def _bbox_contains(self, gx: int, gy: int, sprite: Sprite) -> bool:
        return (
            sprite.x <= gx < sprite.x + sprite.width
            and sprite.y <= gy < sprite.y + sprite.height
        )

    def _extended_bbox_contains(
        self, gx: int, gy: int, sprite: Sprite, padding: int = 1
    ) -> bool:
        return (
            sprite.x - padding <= gx < sprite.x + sprite.width + padding
            and sprite.y - padding <= gy < sprite.y + sprite.height + padding
        )

    def _beam_lane_contains(self, gx: int, gy: int, sprite: Sprite) -> bool:
        # Strict in x (prevents adjacent-slot ambiguity), tolerant in y so
        # that the click registers even when the beam is tilted by up to 3
        # cells from the neutral y position.
        y_pad = 3
        return (
            sprite.x <= gx < sprite.x + sprite.width
            and sprite.y - y_pad <= gy < sprite.y + sprite.height + y_pad
        )

    def _find_tray_weight_at(self, gx: int, gy: int) -> Sprite | None:
        placed = set(self.placement.values())
        for w in self.tray_weights:
            if w in placed:
                continue
            tray_x, tray_y = self.tray_origin[w]
            if w.x != tray_x or w.y != tray_y:
                continue
            if self._extended_bbox_contains(gx, gy, w):
                return w
        return None

    def _select_weight(self, weight: Sprite) -> None:
        self._deselect()
        if "weight_mass1" in weight.tags:
            weight.color_remap(PALETTE_WEIGHT_ORANGE, PALETTE_SELECTION_HIGHLIGHT)
        else:
            weight.color_remap(PALETTE_WEIGHT_BLUE, PALETTE_SELECTION_HIGHLIGHT)
        self.selected_weight = weight

    def _deselect(self) -> None:
        if self.selected_weight is None:
            return
        w = self.selected_weight
        if "weight_mass1" in w.tags:
            w.color_remap(PALETTE_SELECTION_HIGHLIGHT, PALETTE_WEIGHT_ORANGE)
        else:
            w.color_remap(PALETTE_SELECTION_HIGHLIGHT, PALETTE_WEIGHT_BLUE)
        self.selected_weight = None

    def _place_at(self, arm: int) -> None:
        weight = self.selected_weight
        if weight is None:
            return
        self._deselect()
        self.placement[arm] = weight
        self._update_visuals()
        self._maybe_displace_passenger()

    def _lift_weight(self, arm: int) -> None:
        weight = self.placement.pop(arm)
        tray_x, tray_y = self.tray_origin[weight]
        weight.set_position(tray_x, tray_y)
        self._update_visuals()
        self._maybe_displace_passenger()

    def _compute_torque(self) -> int:
        torque = 0
        for arm, weight in self.placement.items():
            mass = 2 if "weight_mass2" in weight.tags else 1
            torque += mass * arm
        if (
            self.passenger_arm is not None
            and self.passenger_arm in self.exposed_arms
        ):
            torque += PASSENGER_MASS * self.passenger_arm
        return torque

    def _compute_tilt_level(self, torque: int) -> int:
        # Any non-zero torque shows at least a level-1 tilt so the beam is
        # never visually "balanced" when the torque sum is not exactly zero.
        # |torque|>=4 escalates to level 2 (the M3 passenger-slide threshold).
        if torque == 0:
            return 0
        sign = 1 if torque > 0 else -1
        magnitude = 2 if abs(torque) >= 4 else 1
        return sign * magnitude

    def _y_offset_for_arm(self, arm: int, tilt_level: int) -> int:
        raw = arm * tilt_level
        if raw >= 0:
            return raw // 2
        return -((-raw) // 2)

    def _update_visuals(self) -> None:
        torque = self._compute_torque()
        tilt = self._compute_tilt_level(torque)
        for arm, segment in self.beam_segments.items():
            y_offset = self._y_offset_for_arm(arm, tilt)
            new_y = BEAM_TOP_Y + y_offset
            slot_x = FULCRUM_X + arm * SLOT_WIDTH
            segment.set_position(slot_x, new_y)
            if arm in self.placement:
                w = self.placement[arm]
                # Centre the weight horizontally on the slot. mass-2 (width 8)
                # fills the slot exactly (offset 0); mass-1 (width 4) is
                # nudged in by 2 cells so it sits in the middle of the slot.
                centre_offset = (segment.width - w.width) // 2
                w.set_position(slot_x + centre_offset, new_y - w.height)
            if (
                self.passenger_arm == arm
                and self.passenger_sprite is not None
                and arm in self.exposed_arms
            ):
                centre_offset = (segment.width - self.passenger_sprite.width) // 2
                self.passenger_sprite.set_position(
                    slot_x + centre_offset, new_y - self.passenger_sprite.height
                )

    def _maybe_displace_passenger(self) -> None:
        if self.passenger_arm is None or self.passenger_sprite is None:
            return
        if self._anim_phase >= 0:
            return
        torque = self._compute_torque()
        tilt = self._compute_tilt_level(torque)
        if abs(tilt) < 2:
            return
        direction = 1 if tilt > 0 else -1
        new_arm = self.passenger_arm + direction
        # Skip the fulcrum (no slot at arm 0).
        if new_arm == 0:
            new_arm += direction
        # Clamp at beam ends — passenger never falls off.
        if new_arm not in self.exposed_arms:
            return
        # Blocked by an already-placed weight.
        if new_arm in self.placement:
            return
        # Set up the linear-interpolation animation.
        end_segment = self.beam_segments.get(new_arm)
        if end_segment is None:
            return
        end_centre_offset = (
            end_segment.width - self.passenger_sprite.width
        ) // 2
        end_x = end_segment.x + end_centre_offset
        end_y = end_segment.y - self.passenger_sprite.height
        self._anim_start_xy = (
            self.passenger_sprite.x,
            self.passenger_sprite.y,
        )
        self._anim_end_xy = (end_x, end_y)
        self._anim_target_arm = new_arm
        self._anim_phase = 0

    def _check_win(self) -> bool:
        if any(w not in self.placement.values() for w in self.tray_weights):
            return False
        return self._compute_torque() == 0

    def _check_lose(self) -> bool:
        # The only loss condition is step exhaustion; that is checked in
        # `_finalize_step` against `self._action_count >= self.step_budget`.
        # Passenger position is now always in `exposed_arms` (clamped), so
        # there is no off-beam-loss to detect here.
        return False

    def _get_hidden_state(self) -> np.ndarray:
        return np.array([self.step_hud.remaining], dtype=np.int16)

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()
