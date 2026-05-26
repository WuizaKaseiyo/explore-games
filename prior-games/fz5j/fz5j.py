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
# Pixel constants
# ---------------------------------------------------------------------
CELL_PX = 4
GRID_CELLS = 16
MAX_LIVES = 3


# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------

def _wall_frame_pixels():
    rows = [[4] * 64]
    for _ in range(62):
        rows.append([4] + [-1] * 62 + [4])
    rows.append([4] * 64)
    return rows


def _avatar_pixels():
    return [
        [-1, -1, -1, -1],
        [-1, 14, 14, -1],
        [-1, 14, 14, -1],
        [-1, -1, -1, -1],
    ]


def _wall_block_pixels():
    return [
        [4, 4, 4, 4],
        [4, 4, 4, 4],
        [4, 4, 4, 4],
        [4, 4, 4, 4],
    ]


def _goal_pixels():
    return [
        [11, 11, 11, 11],
        [11, -1, -1, 11],
        [11, -1, -1, 11],
        [11, 11, 11, 11],
    ]


def _phase_open_pixels(frame_color):
    # Open = period-coloured frame around a hollow centre.  Transparent
    # interior pixels let the background show through, signalling "you
    # may pass."
    return [
        [frame_color, frame_color, frame_color, frame_color],
        [frame_color, -1, -1, frame_color],
        [frame_color, -1, -1, frame_color],
        [frame_color, frame_color, frame_color, frame_color],
    ]


def _phase_closed_pixels(frame_color):
    # Closed = period-coloured tile with a black cross painted across both
    # diagonals.  The frame colour is preserved on the off-diagonal cells
    # so the player can read the period; the black diagonals signal "do
    # not enter on this step."
    return [
        [5, frame_color, frame_color, 5],
        [frame_color, 5, 5, frame_color],
        [frame_color, 5, 5, frame_color],
        [5, frame_color, frame_color, 5],
    ]


sprites = {
    "avatar": Sprite(
        pixels=_avatar_pixels(),
        name="avatar",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=5,
    ),
    "goal": Sprite(
        pixels=_goal_pixels(),
        name="goal",
        visible=True,
        collidable=False,
        tags=["goal"],
        layer=2,
    ),
    "phase2_closed": Sprite(
        pixels=_phase_closed_pixels(10),
        name="phase2_closed",
        visible=True,
        collidable=True,
        tags=["phase_tile", "period_2", "closed_variant"],
        layer=1,
    ),
    "phase2_open": Sprite(
        pixels=_phase_open_pixels(10),
        name="phase2_open",
        visible=True,
        collidable=True,
        tags=["phase_tile", "period_2", "open_variant"],
        layer=1,
    ),
    "phase3_closed": Sprite(
        pixels=_phase_closed_pixels(6),
        name="phase3_closed",
        visible=True,
        collidable=True,
        tags=["phase_tile", "period_3", "closed_variant"],
        layer=1,
    ),
    "phase3_open": Sprite(
        pixels=_phase_open_pixels(6),
        name="phase3_open",
        visible=True,
        collidable=True,
        tags=["phase_tile", "period_3", "open_variant"],
        layer=1,
    ),
    "phase4_closed": Sprite(
        pixels=_phase_closed_pixels(12),
        name="phase4_closed",
        visible=True,
        collidable=True,
        tags=["phase_tile", "period_4", "closed_variant"],
        layer=1,
    ),
    "phase4_open": Sprite(
        pixels=_phase_open_pixels(12),
        name="phase4_open",
        visible=True,
        collidable=True,
        tags=["phase_tile", "period_4", "open_variant"],
        layer=1,
    ),
    "wall_block": Sprite(
        pixels=_wall_block_pixels(),
        name="wall_block",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=1,
    ),
    "wall_frame": Sprite(
        pixels=_wall_frame_pixels(),
        name="wall_frame",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

def _cell(x, y):
    return (x * CELL_PX, y * CELL_PX)


def _place_phase_pair(open_name, closed_name, x, y):
    px, py = _cell(x, y)
    return [
        sprites[open_name].clone().set_position(px, py),
        sprites[closed_name].clone().set_position(px, py),
    ]


def _level1_sprites():
    """Single horizontal corridor on row 5; two period-2 chokepoints
    require exactly one wall-bump wait between them."""
    out = [
        sprites["wall_frame"].clone().set_position(0, 0),
        sprites["avatar"].clone().set_position(*_cell(1, 5)),
        sprites["goal"].clone().set_position(*_cell(14, 5)),
    ]
    # Solid walls on every interior row except row 5.
    for row in (1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14):
        for col in range(1, 15):
            out.append(sprites["wall_block"].clone().set_position(*_cell(col, row)))
    out += _place_phase_pair("phase2_open", "phase2_closed", 5, 5)
    out += _place_phase_pair("phase2_open", "phase2_closed", 10, 5)
    return out


def _level2_sprites():
    """Vertical corridor on col 5; adds a period-3 chokepoint between
    two period-2 tiles.  Witness needs two waits."""
    out = [
        sprites["wall_frame"].clone().set_position(0, 0),
        sprites["avatar"].clone().set_position(*_cell(5, 1)),
        sprites["goal"].clone().set_position(*_cell(5, 14)),
    ]
    for col in (1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14):
        for row in range(1, 15):
            out.append(sprites["wall_block"].clone().set_position(*_cell(col, row)))
    out += _place_phase_pair("phase2_open", "phase2_closed", 5, 5)
    out += _place_phase_pair("phase3_open", "phase3_closed", 5, 9)
    out += _place_phase_pair("phase2_open", "phase2_closed", 5, 12)
    return out


def _level3_sprites():
    """L-shaped corridor: row 1 east to col 10, then south down col 10.
    Four chokepoints across periods 2/3/4, with the last two on
    adjacent cells (rows 12 and 13 of col 10) so their residues are
    locked one step apart."""
    out = [
        sprites["wall_frame"].clone().set_position(0, 0),
        sprites["avatar"].clone().set_position(*_cell(1, 1)),
        sprites["goal"].clone().set_position(*_cell(10, 14)),
    ]
    # Row-2 wall barrier: only col 10 is open.
    for col in range(1, 15):
        if col == 10:
            continue
        out.append(sprites["wall_block"].clone().set_position(*_cell(col, 2)))
    # Bracket walls flanking the col-10 corridor on both sides, rows 3..14.
    for row in range(3, 15):
        out.append(sprites["wall_block"].clone().set_position(*_cell(9, row)))
        out.append(sprites["wall_block"].clone().set_position(*_cell(11, row)))
    # Phase tiles.
    out += _place_phase_pair("phase2_open", "phase2_closed", 4, 1)
    out += _place_phase_pair("phase3_open", "phase3_closed", 8, 1)
    out += _place_phase_pair("phase4_open", "phase4_closed", 10, 5)
    out += _place_phase_pair("phase3_open", "phase3_closed", 10, 12)
    out += _place_phase_pair("phase3_open", "phase3_closed", 10, 13)
    return out


levels = [
    Level(
        sprites=_level1_sprites(),
        grid_size=(64, 64),
        data={
            "step_budget": 22,
            "level_start_cell": (1, 5),
            "phase_offsets": {
                (5, 5): 0,
                (10, 5): 0,
            },
        },
    ),
    Level(
        sprites=_level2_sprites(),
        grid_size=(64, 64),
        data={
            "step_budget": 30,
            "level_start_cell": (5, 1),
            "phase_offsets": {
                (5, 5): 0,
                (5, 9): 1,
                (5, 12): 1,
            },
        },
    ),
    Level(
        sprites=_level3_sprites(),
        grid_size=(64, 64),
        data={
            "step_budget": 40,
            "level_start_cell": (1, 1),
            "phase_offsets": {
                (4, 1): 0,
                (8, 1): 1,
                (10, 5): 2,
                (10, 12): 0,
                (10, 13): 1,
            },
        },
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 1
PADDING_COLOR = 4


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps=0):
        self.max_steps = max_steps
        self.current_steps = max_steps

    def reset(self, max_steps):
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_current(self, value):
        self.current_steps = max(0, min(value, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.current_steps / self.max_steps
        fill = round(64 * ratio)
        for x in range(64):
            frame[63, x] = 11 if x < fill else 4
        return frame


class LivesHud(RenderableUserDisplay):
    """Three pips along the top edge.  Lit pips are palette 8 (red) on a
    palette-4 backdrop; lost pips dim to palette 4 entirely.  Pips occupy
    columns 4..23 across pixel rows 0..3, painted on top of the perimeter
    wall."""

    PIP_X_STARTS = (4, 12, 20)
    PIP_BODY_OFFSETS = (
        (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2), (1, 3),
        (2, 0), (2, 1), (2, 2), (2, 3),
        (3, 1), (3, 2),
    )

    def __init__(self):
        self.current_lives = MAX_LIVES

    def set_current(self, value):
        self.current_lives = max(0, min(value, MAX_LIVES))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        for i, x_start in enumerate(self.PIP_X_STARTS):
            color = 8 if i < self.current_lives else 4
            for dy, dx in self.PIP_BODY_OFFSETS:
                frame[dy, x_start + dx] = color
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Fz5j(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_hud = StepCounterHud(0)
        self._lives_hud = LivesHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_hud, self._lives_hud],
        )
        self._step_counter = 0
        self._max_steps = 0
        self._lives = MAX_LIVES
        self._level_start_cell = (0, 0)
        self._phase_state = {}
        super().__init__(
            game_id="fz5j",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    # -----------------------------------------------------------------
    def on_set_level(self, level: Level) -> None:
        self._step_counter = 0
        self._max_steps = level.get_data("step_budget") or 30
        self._step_counter_hud.reset(self._max_steps)

        self._lives = MAX_LIVES
        self._lives_hud.set_current(self._lives)

        self._level_start_cell = level.get_data("level_start_cell") or (1, 1)
        offsets = level.get_data("phase_offsets") or {}

        self._phase_state = {}
        for cell, offset in offsets.items():
            cx, cy = cell
            px, py = _cell(cx, cy)
            open_sprite = self._sprite_with_tag_at(px, py, "open_variant")
            closed_sprite = self._sprite_with_tag_at(px, py, "closed_variant")
            period = self._sprite_period(open_sprite or closed_sprite)
            self._phase_state[cell] = {
                "period": period,
                "offset": offset,
                "open_sprite": open_sprite,
                "closed_sprite": closed_sprite,
            }
        self._refresh_phase_tiles()

    # -----------------------------------------------------------------
    def _sprite_with_tag_at(self, px, py, tag):
        for s in self.current_level.get_sprites_by_tag(tag):
            if s.x == px and s.y == py:
                return s
        return None

    @staticmethod
    def _sprite_period(sprite):
        if sprite is None:
            return 0
        for t in sprite.tags:
            if t.startswith("period_"):
                return int(t.split("_", 1)[1])
        return 0

    def _avatar(self):
        avs = self.current_level.get_sprites_by_tag("player")
        return avs[0] if avs else None

    def _goal_cell(self):
        gs = self.current_level.get_sprites_by_tag("goal")
        if not gs:
            return (-1, -1)
        return (gs[0].x // CELL_PX, gs[0].y // CELL_PX)

    def _avatar_cell(self):
        a = self._avatar()
        if a is None:
            return (0, 0)
        return (a.x // CELL_PX, a.y // CELL_PX)

    def _is_open(self, cell):
        st = self._phase_state.get(cell)
        if st is None:
            return True
        if st["period"] <= 0:
            return True
        return (self._step_counter % st["period"]) == st["offset"]

    def _refresh_phase_tiles(self):
        for cell, st in self._phase_state.items():
            currently_open = self._is_open(cell)
            if st["open_sprite"] is not None:
                st["open_sprite"].set_interaction(
                    InteractionMode.TANGIBLE if currently_open else InteractionMode.REMOVED
                )
            if st["closed_sprite"] is not None:
                st["closed_sprite"].set_interaction(
                    InteractionMode.REMOVED if currently_open else InteractionMode.TANGIBLE
                )

    def _wall_at(self, target_cell):
        cx, cy = target_cell
        if cx < 0 or cy < 0 or cx >= GRID_CELLS or cy >= GRID_CELLS:
            return True
        if cx == 0 or cy == 0 or cx == GRID_CELLS - 1 or cy == GRID_CELLS - 1:
            return True
        px, py = _cell(cx, cy)
        for s in self.current_level.get_sprites_by_tag("wall"):
            if s.name == "wall_frame":
                continue
            if s.x == px and s.y == py:
                return True
        return False

    def _classify_target(self, target_cell):
        """Returns one of: 'wall', 'phase_closed', 'goal', 'open'."""
        if self._wall_at(target_cell):
            return "wall"
        if target_cell in self._phase_state:
            return "open" if self._is_open(target_cell) else "phase_closed"
        if target_cell == self._goal_cell():
            return "goal"
        return "open"

    @staticmethod
    def _delta(action_id):
        if action_id == GameAction.ACTION1:
            return (0, -1)
        if action_id == GameAction.ACTION2:
            return (0, 1)
        if action_id == GameAction.ACTION3:
            return (-1, 0)
        if action_id == GameAction.ACTION4:
            return (1, 0)
        return (0, 0)

    def _respawn_avatar(self):
        avatar = self._avatar()
        if avatar is not None:
            avatar.set_position(*_cell(*self._level_start_cell))
        self._step_counter = 0
        self._step_counter_hud.set_current(self._max_steps)
        self._refresh_phase_tiles()

    # -----------------------------------------------------------------
    def step(self) -> None:
        action_id = self.action.id
        avatar = self._avatar()

        if avatar is not None and action_id in (
            GameAction.ACTION1,
            GameAction.ACTION2,
            GameAction.ACTION3,
            GameAction.ACTION4,
        ):
            dx, dy = self._delta(action_id)
            cur_cell = self._avatar_cell()
            target_cell = (cur_cell[0] + dx, cur_cell[1] + dy)

            self._step_counter += 1
            self._refresh_phase_tiles()

            kind = self._classify_target(target_cell)

            if kind == "wall":
                # Wall-bump: implicit wait.  No movement, no life lost,
                # counter still ticked.
                pass
            elif kind == "phase_closed":
                # Death.  Lose a life and respawn at level start.
                self._lives -= 1
                self._lives_hud.set_current(self._lives)
                if self._lives <= 0:
                    self.lose()
                    self.complete_action()
                    return
                self._respawn_avatar()
            elif kind == "goal":
                avatar.set_position(*_cell(*target_cell))
                self.next_level()
                self.complete_action()
                return
            else:
                avatar.set_position(*_cell(*target_cell))

        self._step_counter_hud.set_current(self._max_steps - self._step_counter)

        if self._step_counter >= self._max_steps:
            self.lose()
            self.complete_action()
            return

        self.complete_action()

    # -----------------------------------------------------------------
    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 4), dtype=np.int16)
        state[0, 0] = self._step_counter
        state[0, 1] = self._max_steps
        state[0, 2] = self._lives
        state[0, 3] = self._current_level_index
        return state
