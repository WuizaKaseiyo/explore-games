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
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "avatar": Sprite(
        pixels=[
            [10, 0],
            [0, 10],
        ],
        name="avatar",
        visible=True,
        collidable=True,
        tags=["avatar"],
        layer=3,
    ),
    "counter_switch": Sprite(
        pixels=[
            [6],
        ],
        name="counter_switch",
        visible=True,
        collidable=False,
        tags=["counter_switch"],
        layer=1,
    ),
    "rotor": Sprite(
        pixels=[
            [5, 5],
            [5, 3],
        ],
        name="rotor",
        visible=True,
        collidable=True,
        tags=["rotor"],
        layer=2,
    ),
    "target": Sprite(
        pixels=[
            [14],
        ],
        name="target",
        visible=True,
        collidable=False,
        tags=["target"],
        layer=2,
    ),
    "wall": Sprite(
        pixels=[
            [5],
        ],
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
levels = [
    Level(
        sprites=[
            sprites["rotor"].clone().set_position(5, 5),
            sprites["avatar"].clone().set_position(1, 1),
            sprites["target"].clone().set_position(10, 10),
        ],
        grid_size=(12, 12),
        data={"step_budget": 32, "avatar_start": (1, 1)},
    ),
    Level(
        sprites=[
            sprites["rotor"].clone().set_position(5, 5),
            sprites["avatar"].clone().set_position(1, 1),
            sprites["target"].clone().set_position(10, 10),
            sprites["wall"].clone().set_position(7, 0),
            sprites["wall"].clone().set_position(7, 1),
            sprites["wall"].clone().set_position(7, 2),
        ],
        grid_size=(12, 12),
        data={"step_budget": 36, "avatar_start": (1, 1)},
    ),
    Level(
        sprites=[
            sprites["rotor"].clone().set_position(5, 5),
            sprites["avatar"].clone().set_position(1, 1),
            sprites["target"].clone().set_position(1, 10),
            sprites["wall"].clone().set_position(2, 7),
            sprites["wall"].clone().set_position(2, 8),
            sprites["wall"].clone().set_position(2, 9),
            sprites["counter_switch"].clone().set_position(3, 1),
        ],
        grid_size=(12, 12),
        data={"step_budget": 36, "avatar_start": (1, 1)},
    ),
]

# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 4
PADDING_COLOR = 3

GRID_SIZE = 12
CAMERA_SCALE = 64 // GRID_SIZE  # = 5
FRAME_OFFSET = (64 - GRID_SIZE * CAMERA_SCALE) // 2  # = 2

LIT_TINT_NORMAL = 11
DIRECTION_MARKER_COLOR = 6
LIVES_PIP_FULL = 8
LIVES_PIP_EMPTY = 4

ROTOR_X_MIN, ROTOR_X_MAX = 5, 6
ROTOR_Y_MIN, ROTOR_Y_MAX = 5, 6

SECTOR_NW = 0
SECTOR_NE = 1
SECTOR_SE = 2
SECTOR_SW = 3

LIVES_PER_LEVEL = 3
AVATAR_SIZE = 2  # avatar is AVATAR_SIZE x AVATAR_SIZE

# Death-animation phase markers. Phase numbers are inclusive starts;
# the animation advances one phase per engine-step iteration while
# _death_anim_phase >= 0.
DEATH_PHASE_AVATAR_FLICKER_START = 0
DEATH_PHASE_AVATAR_FLICKER_END = 5   # phases 0..5 inclusive = 6 ticks
DEATH_PHASE_AVATAR_GONE = 6           # 1 tick — avatar fully hidden, no pip change yet
DEATH_PHASE_PIP_FLICKER_START = 7
DEATH_PHASE_PIP_FLICKER_END = 11      # phases 7..11 inclusive = 5 ticks; ends on EMPTY (11 is odd)
DEATH_PHASE_PIP_GONE = 12             # decrement lives this tick
DEATH_PHASE_RESPAWN = 13              # final tick — respawn or lose, complete action


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
def _sector_bounds(sector: int) -> tuple[range, range]:
    if sector == SECTOR_NW:
        return range(0, 6), range(0, 6)
    if sector == SECTOR_NE:
        return range(6, 12), range(0, 6)
    if sector == SECTOR_SE:
        return range(6, 12), range(6, 12)
    return range(0, 6), range(6, 12)


def _cell_in_sector(gx: int, gy: int, sector: int) -> bool:
    xr, yr = _sector_bounds(sector)
    return gx in xr and gy in yr


class WedgeOverlay(RenderableUserDisplay):
    def __init__(self, game: "Nz3v") -> None:
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        sector = self.game._rotor_angle
        xr, yr = _sector_bounds(sector)
        tint = LIT_TINT_NORMAL
        dot_offsets = [
            (0, 0),
            (CAMERA_SCALE - 1, 0),
            (0, CAMERA_SCALE - 1),
            (CAMERA_SCALE - 1, CAMERA_SCALE - 1),
            (CAMERA_SCALE // 2, CAMERA_SCALE // 2),
        ]
        for gy in yr:
            for gx in xr:
                if ROTOR_X_MIN <= gx <= ROTOR_X_MAX and ROTOR_Y_MIN <= gy <= ROTOR_Y_MAX:
                    continue
                cx0 = gx * CAMERA_SCALE + FRAME_OFFSET
                cy0 = gy * CAMERA_SCALE + FRAME_OFFSET
                for dx, dy in dot_offsets:
                    px = cx0 + dx
                    py = cy0 + dy
                    if 0 <= px < frame.shape[1] and 0 <= py < frame.shape[0]:
                        if frame[py, px] == BACKGROUND_COLOR:
                            frame[py, px] = tint
        return frame


class RotorDirectionMarker(RenderableUserDisplay):
    def __init__(self, game: "Nz3v") -> None:
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        notch_offsets = {
            SECTOR_NW: (-1, -1),
            SECTOR_NE: (1, -1),
            SECTOR_SE: (1, 1),
            SECTOR_SW: (-1, 1),
        }
        rotor_center_x = (ROTOR_X_MIN + ROTOR_X_MAX) / 2.0
        rotor_center_y = (ROTOR_Y_MIN + ROTOR_Y_MAX) / 2.0
        sector = self.game._rotor_angle
        nx, ny = notch_offsets[sector]
        notch_gx = rotor_center_x + nx * 0.5
        notch_gy = rotor_center_y + ny * 0.5
        notch_px = int(notch_gx * CAMERA_SCALE + FRAME_OFFSET + CAMERA_SCALE // 2)
        notch_py = int(notch_gy * CAMERA_SCALE + FRAME_OFFSET + CAMERA_SCALE // 2)
        if 0 <= notch_px < frame.shape[1] and 0 <= notch_py < frame.shape[0]:
            frame[notch_py, notch_px] = LIT_TINT_NORMAL
        next_sector = (sector + self.game._direction) % 4
        ddx, ddy = notch_offsets[next_sector]
        dir_gx = rotor_center_x + ddx * 0.5
        dir_gy = rotor_center_y + ddy * 0.5
        dir_px = int(dir_gx * CAMERA_SCALE + FRAME_OFFSET + CAMERA_SCALE // 2)
        dir_py = int(dir_gy * CAMERA_SCALE + FRAME_OFFSET + CAMERA_SCALE // 2)
        if 0 <= dir_px < frame.shape[1] and 0 <= dir_py < frame.shape[0]:
            frame[dir_py, dir_px] = DIRECTION_MARKER_COLOR
        return frame


class StepCounterHud(RenderableUserDisplay):
    def __init__(self, game: "Nz3v") -> None:
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        budget = self.game._step_budget
        taken = self.game._actions_taken
        remaining = max(0, budget - taken)
        if budget == 0:
            return frame
        width = frame.shape[1]
        filled = round(width * remaining / budget)
        filled = max(0, min(width, filled))
        for x in range(width):
            if x < filled:
                frame[63, x] = 1
            else:
                frame[63, x] = 4
        return frame


class LivesHud(RenderableUserDisplay):
    def __init__(self, game: "Nz3v") -> None:
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        pip_size = 3
        pip_gap = 2
        margin = 2
        phase = self.game._death_anim_phase
        lives = self.game._lives
        dying_idx = (
            lives - 1
            if DEATH_PHASE_PIP_FLICKER_START <= phase <= DEATH_PHASE_PIP_FLICKER_END
            else None
        )
        for i in range(LIVES_PER_LEVEL):
            if i == dying_idx:
                color = LIVES_PIP_FULL if (phase % 2 == 0) else LIVES_PIP_EMPTY
            elif i < lives:
                color = LIVES_PIP_FULL
            else:
                color = LIVES_PIP_EMPTY
            x0 = margin + i * (pip_size + pip_gap)
            y0 = margin
            for dy in range(pip_size):
                for dx in range(pip_size):
                    px = x0 + dx
                    py = y0 + dy
                    if 0 <= px < frame.shape[1] and 0 <= py < frame.shape[0]:
                        frame[py, px] = color
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Nz3v(NovaBaseGame):
    def __init__(self) -> None:
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
        )
        self._rotor_angle = 0
        self._direction = 1
        self._step_budget = 32
        self._actions_taken = 0
        self._lives = LIVES_PER_LEVEL
        self._avatar_start = (1, 1)
        self._spent_switches: set[tuple[int, int]] = set()
        self._death_anim_phase = -1
        super().__init__(
            game_id="nz3v",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )
        self._camera.replace_interface(
            [
                WedgeOverlay(self),
                RotorDirectionMarker(self),
                StepCounterHud(self),
                LivesHud(self),
            ]
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        self._rotor_angle = SECTOR_NW
        self._direction = 1
        self._actions_taken = 0
        self._lives = LIVES_PER_LEVEL
        self._spent_switches = set()
        self._death_anim_phase = -1
        budget = level.get_data("step_budget")
        self._step_budget = budget if budget is not None else 32
        avatar_start = level.get_data("avatar_start") or (1, 1)
        self._avatar_start = tuple(avatar_start)

    def _avatar(self) -> Sprite:
        return self.current_level.get_sprites_by_tag("avatar")[0]

    def _target(self) -> Sprite:
        return self.current_level.get_sprites_by_tag("target")[0]

    def _avatar_footprint(self, gx: int | None = None, gy: int | None = None) -> list[tuple[int, int]]:
        if gx is None or gy is None:
            avatar = self._avatar()
            gx, gy = avatar.x, avatar.y
        return [
            (gx + dx, gy + dy)
            for dx in range(AVATAR_SIZE)
            for dy in range(AVATAR_SIZE)
        ]

    def _is_cell_blocked(self, gx: int, gy: int) -> bool:
        if gx < 0 or gx >= GRID_SIZE or gy < 0 or gy >= GRID_SIZE:
            return True
        if ROTOR_X_MIN <= gx <= ROTOR_X_MAX and ROTOR_Y_MIN <= gy <= ROTOR_Y_MAX:
            return True
        for w in self.current_level.get_sprites_by_tag("wall"):
            if w.x == gx and w.y == gy:
                return True
        return False

    def _footprint_cells_blocked(self, footprint: list[tuple[int, int]]) -> bool:
        return any(self._is_cell_blocked(gx, gy) for gx, gy in footprint)

    def _footprint_any_in_lit_sector(self, footprint: list[tuple[int, int]]) -> bool:
        for gx, gy in footprint:
            if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
                if _cell_in_sector(gx, gy, self._rotor_angle):
                    return True
        return False

    def _footprint_contains_target(self, footprint: list[tuple[int, int]]) -> bool:
        target = self._target()
        for gx, gy in footprint:
            if gx == target.x and gy == target.y:
                return True
        return False

    def _check_counter_switch(self, footprint: list[tuple[int, int]]) -> None:
        for switch in self.current_level.get_sprites_by_tag("counter_switch"):
            for gx, gy in footprint:
                if gx == switch.x and gy == switch.y and (gx, gy) not in self._spent_switches:
                    self._spent_switches.add((gx, gy))
                    self._direction = -self._direction
                    switch.color_remap(6, 3)
                    return

    def _direction_delta(self, action_id: GameAction) -> tuple[int, int]:
        if action_id == GameAction.ACTION1:
            return 0, -1
        if action_id == GameAction.ACTION2:
            return 0, 1
        if action_id == GameAction.ACTION3:
            return -1, 0
        if action_id == GameAction.ACTION4:
            return 1, 0
        return 0, 0

    def _respawn_avatar(self) -> None:
        avatar = self._avatar()
        sx, sy = self._avatar_start
        avatar.set_position(sx, sy)
        avatar.set_visible(True)
        self._rotor_angle = SECTOR_NW
        self._direction = 1
        self._spent_switches = set()
        for switch in self.current_level.get_sprites_by_tag("counter_switch"):
            switch.color_remap(3, 6)

    def _start_death_animation(self) -> None:
        """Begin the death-animation sequence. Avatar flickers, then a life pip flickers and disappears, then respawn (or lose)."""
        self._death_anim_phase = DEATH_PHASE_AVATAR_FLICKER_START

    def _advance_death_animation(self) -> None:
        """Advance the death animation by one engine-step tick.

        Phases:
          0..5  avatar flicker (visible/invisible every tick)
          6     avatar fully hidden
          7..10 dying-pip flickers (LivesHud handles the rendering)
          11    decrement _lives; pip is now gone
          12    respawn (or lose if _lives <= 0); end animation
        """
        phase = self._death_anim_phase
        avatar = self._avatar()

        if phase <= DEATH_PHASE_AVATAR_FLICKER_END:
            avatar.set_visible(phase % 2 == 0)
        elif phase == DEATH_PHASE_AVATAR_GONE:
            avatar.set_visible(False)
        elif phase <= DEATH_PHASE_PIP_FLICKER_END:
            avatar.set_visible(False)
            if phase == DEATH_PHASE_PIP_FLICKER_END:
                # Decrement at the last flicker frame so frame 12+ shows the pip gone continuously.
                self._lives -= 1
                if self._lives <= 0:
                    self._death_anim_phase = -1
                    self.lose()
                    self.complete_action()
                    return
        elif phase == DEATH_PHASE_PIP_GONE:
            avatar.set_visible(False)
        else:  # DEATH_PHASE_RESPAWN
            self._death_anim_phase = -1
            self._respawn_avatar()
            self.complete_action()
            return

        self._death_anim_phase += 1

    def step(self) -> None:
        # If a death animation is in progress, advance one frame and return
        # without calling complete_action() until the animation finishes.
        # The novaengine loops perform_action -> step -> render until
        # complete_action() is called, so each loop iteration renders a frame
        # of the animation.
        if self._death_anim_phase >= 0:
            self._advance_death_animation()
            return

        action_id = self.action.id

        if action_id not in (
            GameAction.ACTION1,
            GameAction.ACTION2,
            GameAction.ACTION3,
            GameAction.ACTION4,
            GameAction.ACTION5,
        ):
            self.complete_action()
            return

        avatar = self._avatar()

        if action_id == GameAction.ACTION5:
            self._rotor_angle = (self._rotor_angle + self._direction) % 4
            footprint = self._avatar_footprint()
            self._actions_taken += 1
            if not self._footprint_any_in_lit_sector(footprint):
                self._start_death_animation()
                return
            if self._actions_taken >= self._step_budget:
                self.lose()
                self.complete_action()
                return
            self.complete_action()
            return

        dx, dy = self._direction_delta(action_id)
        new_x = avatar.x + dx
        new_y = avatar.y + dy
        new_footprint = self._avatar_footprint(new_x, new_y)

        if self._footprint_cells_blocked(new_footprint):
            self._actions_taken += 1
            if self._actions_taken >= self._step_budget:
                self.lose()
                self.complete_action()
                return
            self.complete_action()
            return

        avatar.set_position(new_x, new_y)
        self._check_counter_switch(new_footprint)
        self._actions_taken += 1

        if self._footprint_contains_target(new_footprint):
            self.next_level()
            self.complete_action()
            return

        if not self._footprint_any_in_lit_sector(new_footprint):
            self._start_death_animation()
            return

        if self._actions_taken >= self._step_budget:
            self.lose()
            self.complete_action()
            return

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._rotor_angle
        state[0, 1] = self._direction
        state[0, 2] = self._lives
        state[1, 0] = self._actions_taken
        return state
