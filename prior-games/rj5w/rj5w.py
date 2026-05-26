"""NovaPlay generated game rj5w."""

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
# Sprite-pixel helpers
# ---------------------------------------------------------------------

LINE_LEN = 60  # length of fold-line cursor along its long axis


def _v_line_pixels():
    # 1-cell-wide column, alternating: 12, 12, -1, 12, 12, -1, ...
    return [[12 if i % 3 != 2 else -1] for i in range(LINE_LEN)]


def _h_line_pixels():
    # 1-cell-tall row, alternating: 12, 12, -1, 12, 12, -1, ...
    return [[12 if i % 3 != 2 else -1 for i in range(LINE_LEN)]]


# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------

sprites = {
    "fold_line_h": Sprite(
        pixels=_h_line_pixels(),
        name="fold_line_h",
        visible=True,
        collidable=False,
        tags=["fold_line", "fold_line_h"],
        interaction=InteractionMode.INTANGIBLE,
        layer=0,
    ),
    "fold_line_v": Sprite(
        pixels=_v_line_pixels(),
        name="fold_line_v",
        visible=True,
        collidable=False,
        tags=["fold_line", "fold_line_v"],
        interaction=InteractionMode.INTANGIBLE,
        layer=0,
    ),
    "pawn_green": Sprite(
        pixels=[
            [14, 14, 0, 14, 14],
            [14, 5, 14, 5, 14],
            [0, 14, 14, 14, 0],
            [14, 5, 14, 5, 14],
            [14, 14, 0, 14, 14],
        ],
        name="pawn_green",
        visible=True,
        collidable=True,
        tags=["pawn", "pawn_green"],
        layer=2,
    ),
    "pawn_purple": Sprite(
        pixels=[
            [15, 15, 0, 15, 15],
            [15, 5, 15, 5, 15],
            [0, 15, 15, 15, 0],
            [15, 5, 15, 5, 15],
            [15, 15, 0, 15, 15],
        ],
        name="pawn_purple",
        visible=True,
        collidable=True,
        tags=["pawn", "pawn_purple"],
        layer=2,
    ),
    "pawn_yellow": Sprite(
        pixels=[
            [11, 11, 0, 11, 11],
            [11, 5, 11, 5, 11],
            [0, 11, 11, 11, 0],
            [11, 5, 11, 5, 11],
            [11, 11, 0, 11, 11],
        ],
        name="pawn_yellow",
        visible=True,
        collidable=True,
        tags=["pawn", "pawn_yellow"],
        layer=2,
    ),
    "target_green": Sprite(
        pixels=[
            [14, 14, 14, 14, 14],
            [14, -1, -1, -1, 14],
            [14, -1, 5, -1, 14],
            [14, -1, -1, -1, 14],
            [14, 14, 14, 14, 14],
        ],
        name="target_green",
        visible=True,
        collidable=False,
        tags=["target", "target_green"],
        layer=1,
    ),
    "target_purple": Sprite(
        pixels=[
            [15, 15, 15, 15, 15],
            [15, -1, -1, -1, 15],
            [15, -1, 5, -1, 15],
            [15, -1, -1, -1, 15],
            [15, 15, 15, 15, 15],
        ],
        name="target_purple",
        visible=True,
        collidable=False,
        tags=["target", "target_purple"],
        layer=1,
    ),
    "target_yellow": Sprite(
        pixels=[
            [11, 11, 11, 11, 11],
            [11, -1, -1, -1, 11],
            [11, -1, 5, -1, 11],
            [11, -1, -1, -1, 11],
            [11, 11, 11, 11, 11],
        ],
        name="target_yellow",
        visible=True,
        collidable=False,
        tags=["target", "target_yellow"],
        layer=1,
    ),
    "target_green_l3": Sprite(
        pixels=[
            [14, 14,  5, 14, 14],
            [14, -1, -1, -1, 14],
            [ 5, -1,  5, -1,  5],
            [14, -1, -1, -1, 14],
            [14, 14,  5, 14, 14],
        ],
        name="target_green_l3",
        visible=True,
        collidable=False,
        tags=["target", "target_green"],
        layer=1,
    ),
    "target_purple_l3": Sprite(
        pixels=[
            [15, 15,  5, 15, 15],
            [15, -1, -1, -1, 15],
            [ 5, -1,  5, -1,  5],
            [15, -1, -1, -1, 15],
            [15, 15,  5, 15, 15],
        ],
        name="target_purple_l3",
        visible=True,
        collidable=False,
        tags=["target", "target_purple"],
        layer=1,
    ),
    "target_yellow_l3": Sprite(
        pixels=[
            [11, 11,  5, 11, 11],
            [11, -1, -1, -1, 11],
            [ 5, -1,  5, -1,  5],
            [11, -1, -1, -1, 11],
            [11, 11,  5, 11, 11],
        ],
        name="target_yellow_l3",
        visible=True,
        collidable=False,
        tags=["target", "target_yellow"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

levels = [
    Level(
        sprites=[
            sprites["pawn_green"].clone().set_position(8, 28),
            sprites["target_green"].clone().set_position(52, 28),
            sprites["fold_line_v"].clone().set_position(30, 2),
        ],
        grid_size=(64, 64),
        data={"step_budget": 25, "init_fv": 30, "init_fh": -1},
    ),
    Level(
        sprites=[
            sprites["pawn_green"].clone().set_position(8, 8),
            sprites["pawn_purple"].clone().set_position(8, 52),
            sprites["pawn_yellow"].clone().set_position(4, 4),
            sprites["target_green"].clone().set_position(52, 52),
            sprites["target_purple"].clone().set_position(52, 8),
            sprites["target_yellow"].clone().set_position(56, 56),
            sprites["fold_line_v"].clone().set_position(30, 2),
            sprites["fold_line_h"].clone().set_position(2, 30),
        ],
        grid_size=(64, 64),
        data={"step_budget": 100, "init_fv": 30, "init_fh": 30},
    ),
    Level(
        sprites=[
            sprites["pawn_green"].clone().set_position(8, 16),
            sprites["pawn_purple"].clone().set_position(16, 8),
            sprites["pawn_yellow"].clone().set_position(24, 28),
            sprites["target_green_l3"].clone().set_position(52, 16),
            sprites["target_purple_l3"].clone().set_position(16, 56),
            sprites["target_yellow_l3"].clone().set_position(36, 28),
            sprites["fold_line_v"].clone().set_position(28, 2),
            sprites["fold_line_h"].clone().set_position(2, 30),
        ],
        grid_size=(64, 64),
        data={"step_budget": 160, "init_fv": 28, "init_fh": 30},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 1
PADDING_COLOR = 1

ACTIVE_COLOR = 12
INACTIVE_COLOR = 3
LOCKED_COLOR = 3
HUD_FILLED = 6
HUD_EMPTY = 4

PAWN_BASE_COLOR = {
    "pawn_green": 14,
    "pawn_purple": 15,
    "pawn_yellow": 11,
}

PAWN_SIZE = 5  # pawns and targets are 5x5

GRID_MIN = 0
GRID_MAX = 64 - PAWN_SIZE  # max anchor x or y for a 5x5 pawn


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int) -> None:
        self.max_steps = max(0, max_steps)
        self.current_steps = self.max_steps

    def set_max(self, m: int) -> None:
        self.max_steps = max(0, m)
        self.current_steps = self.max_steps

    def set_current(self, c: int) -> None:
        self.current_steps = max(0, min(c, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.current_steps / self.max_steps
        filled = int(round(64 * ratio))
        for x in range(64):
            frame[63, x] = HUD_FILLED if x < filled else HUD_EMPTY
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------

class Rj5w(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_ui = StepCounterHud(0)
        self.active_axis = "V"
        self.fv = 32
        self.fh = -1
        self.step_budget = 0
        self.locked_pawns: set = set()
        self.pawn_to_target: dict = {}
        self.pawn_to_color: dict = {}
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        super().__init__(
            game_id="rj5w",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        self.active_axis = "V"
        self.fv = level.get_data("init_fv")
        if self.fv is None:
            self.fv = 32
        self.fh = level.get_data("init_fh")
        if self.fh is None:
            self.fh = -1
        self.step_budget = level.get_data("step_budget") or 50
        self._step_counter_ui.set_max(self.step_budget)
        self.locked_pawns = set()
        self.pawn_to_target = {}
        self.pawn_to_color = {}

        for pawn in level.get_sprites_by_tag("pawn"):
            for color_tag in ("pawn_green", "pawn_purple", "pawn_yellow"):
                if color_tag in pawn.tags:
                    color = color_tag.split("_", 1)[1]
                    target_list = level.get_sprites_by_tag(f"target_{color}")
                    if target_list:
                        self.pawn_to_target[id(pawn)] = target_list[0]
                        self.pawn_to_color[id(pawn)] = color
                    break

        for vl in level.get_sprites_by_tag("fold_line_v"):
            vl.set_position(self.fv, vl.y)
            self._set_line_color(vl, True)
        for hl in level.get_sprites_by_tag("fold_line_h"):
            hl.set_position(hl.x, self.fh)
            self._set_line_color(hl, False)

    # -----------------------------------------------------------------
    # helpers
    # -----------------------------------------------------------------

    def _set_line_color(self, line_sprite: Sprite, active: bool) -> None:
        target_color = ACTIVE_COLOR if active else INACTIVE_COLOR
        if (line_sprite.pixels == target_color).any():
            return
        if (line_sprite.pixels == ACTIVE_COLOR).any():
            line_sprite.color_remap(ACTIVE_COLOR, target_color)
        elif (line_sprite.pixels == INACTIVE_COLOR).any():
            line_sprite.color_remap(INACTIVE_COLOR, target_color)

    def _refresh_axis_colors(self) -> None:
        for vl in self.current_level.get_sprites_by_tag("fold_line_v"):
            self._set_line_color(vl, self.active_axis == "V")
        for hl in self.current_level.get_sprites_by_tag("fold_line_h"):
            self._set_line_color(hl, self.active_axis == "H")

    def _move_v(self, delta: int) -> None:
        new_fv = max(1, min(62, self.fv + delta))
        self.fv = new_fv
        for vl in self.current_level.get_sprites_by_tag("fold_line_v"):
            vl.set_position(self.fv, vl.y)

    def _move_h(self, delta: int) -> None:
        new_fh = max(1, min(62, self.fh + delta))
        self.fh = new_fh
        for hl in self.current_level.get_sprites_by_tag("fold_line_h"):
            hl.set_position(hl.x, self.fh)

    def _on_target(self, pawn: Sprite) -> bool:
        target = self.pawn_to_target.get(id(pawn))
        if target is None:
            return False
        return pawn.x == target.x and pawn.y == target.y

    def _dim_pawn(self, pawn: Sprite) -> None:
        for tag, base in PAWN_BASE_COLOR.items():
            if tag in pawn.tags:
                pawn.color_remap(base, LOCKED_COLOR)
                return

    def _commit_fold(self) -> None:
        # Box reflection: the whole 5x5 sprite mirrors through the fold-line,
        # so the new anchor is offset back from the reflected far corner.
        offset = PAWN_SIZE - 1
        pawns = self.current_level.get_sprites_by_tag("pawn")
        for pawn in pawns:
            if pawn in self.locked_pawns:
                continue
            old_x, old_y = pawn.x, pawn.y
            if self.active_axis == "V":
                new_x = 2 * self.fv - old_x - offset
                new_y = old_y
            else:
                new_x = old_x
                new_y = 2 * self.fh - old_y - offset
            if not (GRID_MIN <= new_x <= GRID_MAX and GRID_MIN <= new_y <= GRID_MAX):
                continue
            if new_x == old_x and new_y == old_y:
                continue
            pawn.set_position(new_x, new_y)
            if self._on_target(pawn):
                self.locked_pawns.add(pawn)
                self._dim_pawn(pawn)

    def _check_win(self) -> bool:
        pawns = self.current_level.get_sprites_by_tag("pawn")
        if not pawns:
            return False
        for pawn in pawns:
            if not self._on_target(pawn):
                return False
        return True

    # -----------------------------------------------------------------
    # step / valid actions / hidden state
    # -----------------------------------------------------------------

    def step(self) -> None:
        action_id = self.action.id
        if action_id == GameAction.RESET:
            self.complete_action()
            return
        self.step_budget -= 1
        self._step_counter_ui.set_current(self.step_budget)

        if action_id == GameAction.ACTION1:
            if self.active_axis == "H" and self.fh >= 0:
                self._move_h(-1)
        elif action_id == GameAction.ACTION2:
            if self.active_axis == "H" and self.fh >= 0:
                self._move_h(1)
        elif action_id == GameAction.ACTION3:
            if self.active_axis == "V":
                self._move_v(-1)
        elif action_id == GameAction.ACTION4:
            if self.active_axis == "V":
                self._move_v(1)
        elif action_id == GameAction.ACTION5:
            self._commit_fold()
            if self._check_win():
                self.next_level()
                self.complete_action()
                return
        elif action_id == GameAction.ACTION6:
            data = self.action.data or {}
            px = int(data.get("x", 0))
            py = int(data.get("y", 0))
            grid_xy = self.camera.display_to_grid(px, py)
            if grid_xy:
                gx, gy = grid_xy
                if gx == self.fv and self.fv >= 0:
                    if self.active_axis != "V":
                        self.active_axis = "V"
                        self._refresh_axis_colors()
                elif gy == self.fh and self.fh >= 0:
                    if self.active_axis != "H":
                        self.active_axis = "H"
                        self._refresh_axis_colors()

        if self.step_budget <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 4), dtype=np.int16)
        state[0, 0] = 0 if self.active_axis == "V" else 1
        state[0, 1] = self.fv
        state[0, 2] = self.fh
        state[0, 3] = len(self.locked_pawns)
        return state

    def _get_valid_actions(self) -> list:
        valid = []
        h_present = self.fh >= 0
        for a in self._available_actions:
            if a == 1 and self.active_axis == "H" and h_present:
                valid.append(ActionInput(id=GameAction.ACTION1))
            elif a == 2 and self.active_axis == "H" and h_present:
                valid.append(ActionInput(id=GameAction.ACTION2))
            elif a == 3 and self.active_axis == "V":
                valid.append(ActionInput(id=GameAction.ACTION3))
            elif a == 4 and self.active_axis == "V":
                valid.append(ActionInput(id=GameAction.ACTION4))
            elif a == 5:
                valid.append(ActionInput(id=GameAction.ACTION5))
            elif a == 6 and h_present:
                valid.append(ActionInput(id=GameAction.ACTION6))
        return valid
