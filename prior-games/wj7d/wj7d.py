"""Generated game wj7d — for offline tooling."""

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
# Constants
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 2          # light-grey
PADDING_COLOR = 4             # off-black
CREASE_COLOR = 0              # white
CREASE_SELECTED_COLOR = 11    # yellow
HUD_FILLED = 14               # green
HUD_EMPTY = 4                 # off-black

GRID = 64
STAMP_SIZE = 6
HALO_SIZE = 8
ARROW_STEP = 4
CREASE_STEP = 4
CREASE_LENGTH = 56
CREASE_OFFSET = 4

SHADOW_TO_STAMP_COLOR = {7: 8, 10: 9}
SHADOW_TO_STAMP_TAG = {7: "stamp_red", 10: "stamp_blue"}


# ---------------------------------------------------------------------
# Sprite bank
# ---------------------------------------------------------------------

sprites = {
    "stamp_red_cross": Sprite(
        pixels=[
            [-1, -1,  8,  8, -1, -1],
            [-1, -1,  8,  8, -1, -1],
            [ 8,  8,  0,  0,  8,  8],
            [ 8,  8,  0,  0,  8,  8],
            [-1, -1,  8,  8, -1, -1],
            [-1, -1,  8,  8, -1, -1],
        ],
        name="stamp_red_cross",
        visible=True,
        collidable=True,
        tags=["stamp", "stamp_red"],
        layer=2,
    ),
    "stamp_blue_ring": Sprite(
        pixels=[
            [-1,  9,  9,  9,  9, -1],
            [ 9,  9, -1, -1,  9,  9],
            [ 9, -1, -1, -1, -1,  9],
            [ 9, -1, -1, -1, -1,  9],
            [ 9,  9, -1, -1,  9,  9],
            [-1,  9,  9,  9,  9, -1],
        ],
        name="stamp_blue_ring",
        visible=True,
        collidable=True,
        tags=["stamp", "stamp_blue"],
        layer=2,
    ),
    "shadow_red_cross": Sprite(
        pixels=[
            [-1, -1,  7,  7, -1, -1],
            [-1, -1,  7,  7, -1, -1],
            [ 7,  7, -1, -1,  7,  7],
            [ 7,  7, -1, -1,  7,  7],
            [-1, -1,  7,  7, -1, -1],
            [-1, -1,  7,  7, -1, -1],
        ],
        name="shadow_red_cross",
        visible=True,
        collidable=False,
        tags=["shadow", "shadow_red"],
        layer=0,
    ),
    "shadow_blue_ring": Sprite(
        pixels=[
            [-1, 10, 10, 10, 10, -1],
            [10, 10, -1, -1, 10, 10],
            [10, -1, -1, -1, -1, 10],
            [10, -1, -1, -1, -1, 10],
            [10, 10, -1, -1, 10, 10],
            [-1, 10, 10, 10, 10, -1],
        ],
        name="shadow_blue_ring",
        visible=True,
        collidable=False,
        tags=["shadow", "shadow_blue"],
        layer=0,
    ),
    "crease_h": Sprite(
        pixels=[[CREASE_COLOR] * CREASE_LENGTH],
        name="crease_h",
        visible=True,
        collidable=False,
        tags=["crease", "crease_h"],
        layer=1,
    ),
    "crease_v": Sprite(
        pixels=[[CREASE_COLOR] for _ in range(CREASE_LENGTH)],
        name="crease_v",
        visible=True,
        collidable=False,
        tags=["crease", "crease_v"],
        layer=1,
    ),
    "selection_halo": Sprite(
        pixels=[
            [15, 15, 15, 15, 15, 15, 15, 15],
            [15, -1, -1, -1, -1, -1, -1, 15],
            [15, -1, -1, -1, -1, -1, -1, 15],
            [15, -1, -1, -1, -1, -1, -1, 15],
            [15, -1, -1, -1, -1, -1, -1, 15],
            [15, -1, -1, -1, -1, -1, -1, 15],
            [15, -1, -1, -1, -1, -1, -1, 15],
            [15, 15, 15, 15, 15, 15, 15, 15],
        ],
        name="selection_halo",
        visible=True,
        collidable=False,
        tags=["halo"],
        layer=5,
    ),
}


# ---------------------------------------------------------------------
# Levels
# ---------------------------------------------------------------------

levels = [
    Level(
        sprites=[
            sprites["stamp_red_cross"].clone().set_position(8, 8),
            sprites["shadow_red_cross"].clone().set_position(24, 45),
            sprites["crease_h"].clone().set_position(CREASE_OFFSET, 31),
            sprites["crease_v"].clone().set_position(31, CREASE_OFFSET),
            sprites["selection_halo"].clone().set_position(7, 7),
        ],
        grid_size=(GRID, GRID),
        data={
            "step_budget": 30,
            "crease_movable": False,
            "crease_orient": "H",
            "crease_pos": 31,
            "auto_select_stamp": "stamp_red_cross",
        },
    ),
    Level(
        sprites=[
            sprites["stamp_red_cross"].clone().set_position(8, 4),
            sprites["stamp_blue_ring"].clone().set_position(24, 24),
            sprites["shadow_red_cross"].clone().set_position(24, 37),
            sprites["shadow_blue_ring"].clone().set_position(16, 41),
            sprites["crease_h"].clone().set_position(CREASE_OFFSET, 31),
            sprites["crease_v"].clone().set_position(31, CREASE_OFFSET),
            sprites["selection_halo"].clone().set_position(0, 0),
        ],
        grid_size=(GRID, GRID),
        data={
            "step_budget": 50,
            "crease_movable": False,
            "crease_orient": "H",
            "crease_pos": 31,
            "auto_select_stamp": None,
        },
    ),
    Level(
        sprites=[
            sprites["stamp_red_cross"].clone().set_position(16, 12),
            sprites["stamp_blue_ring"].clone().set_position(40, 8),
            sprites["shadow_red_cross"].clone().set_position(45, 16),
            sprites["shadow_blue_ring"].clone().set_position(40, 41),
            sprites["crease_h"].clone().set_position(CREASE_OFFSET, 31),
            sprites["crease_v"].clone().set_position(31, CREASE_OFFSET),
            sprites["selection_halo"].clone().set_position(0, 0),
        ],
        grid_size=(GRID, GRID),
        data={
            "step_budget": 60,
            "crease_movable": True,
            "crease_orient": "H",
            "crease_pos": 31,
            "auto_select_stamp": None,
        },
    ),
]


# ---------------------------------------------------------------------
# HUD widgets
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 30):
        self.max_steps = max_steps
        self.current = max_steps

    def configure(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current = max_steps

    def set_current(self, n: int) -> None:
        if self.max_steps == 0:
            return
        self.current = max(0, min(n, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        bar_width = CREASE_LENGTH
        x_offset = CREASE_OFFSET
        ratio = self.current / self.max_steps
        filled = round(bar_width * ratio)
        filled = min(max(filled, 0), bar_width)
        for x in range(bar_width):
            if x < filled:
                frame[0, x_offset + x] = HUD_FILLED
            else:
                frame[0, x_offset + x] = HUD_EMPTY
        return frame


class CoveredCellsOverlay(RenderableUserDisplay):
    def __init__(self, game: "Wj7d") -> None:
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        for (x, y), color in self.game.cells_covered.items():
            if 0 <= x < GRID and 0 <= y < GRID:
                frame[y, x] = color
        return frame


# ---------------------------------------------------------------------
# Game class
# ---------------------------------------------------------------------

class Wj7d(NovaBaseGame):
    def __init__(self) -> None:
        camera = Camera(background=BACKGROUND_COLOR, letter_box=PADDING_COLOR)
        self.hud = StepCounterHud(max_steps=30)
        self.cells_covered: dict[tuple[int, int], int] = {}
        self.overlay = CoveredCellsOverlay(self)
        self.selected_stamp: Sprite | None = None
        self.crease_selected: bool = False
        self.crease_orient: str = "H"
        self.crease_pos: int = 31
        self.crease_movable: bool = False
        super().__init__(
            game_id="wj7d",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )
        self.camera.replace_interface([self.overlay, self.hud])

    # -- per-level setup -------------------------------------------------

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (GRID, GRID)
        self.camera.width = gw
        self.camera.height = gh

        budget = level.get_data("step_budget") or 30
        self.hud.configure(budget)

        self.crease_movable = bool(level.get_data("crease_movable") or False)
        self.crease_orient = level.get_data("crease_orient") or "H"
        self.crease_pos = int(level.get_data("crease_pos") or 31)

        self.cells_covered = {}
        self.crease_selected = False
        self.selected_stamp = None

        for sprite in level.get_sprites():
            sprite.set_interaction(InteractionMode.TANGIBLE)
            if "crease" in (sprite.tags or []):
                self._paint_crease(sprite, CREASE_COLOR)

        self._activate_crease()

        auto_select = level.get_data("auto_select_stamp")
        if auto_select:
            matches = level.get_sprites_by_name(auto_select)
            if matches:
                self.selected_stamp = matches[0]

        self._update_halo()
        self._update_crease_color()

    # -- crease orientation / position ----------------------------------

    def _activate_crease(self) -> None:
        h_list = self.current_level.get_sprites_by_tag("crease_h")
        v_list = self.current_level.get_sprites_by_tag("crease_v")
        if self.crease_orient == "H":
            for sp in h_list:
                sp.set_position(CREASE_OFFSET, self.crease_pos)
                sp.set_interaction(InteractionMode.TANGIBLE)
            for sp in v_list:
                sp.set_interaction(InteractionMode.REMOVED)
        else:
            for sp in v_list:
                sp.set_position(self.crease_pos, CREASE_OFFSET)
                sp.set_interaction(InteractionMode.TANGIBLE)
            for sp in h_list:
                sp.set_interaction(InteractionMode.REMOVED)

    def _paint_crease(self, sprite: Sprite, color: int) -> None:
        if hasattr(sprite, "pixels"):
            sprite.pixels = np.full(sprite.pixels.shape, color, dtype=sprite.pixels.dtype)

    def _update_crease_color(self) -> None:
        target = CREASE_SELECTED_COLOR if self.crease_selected else CREASE_COLOR
        for sp in self.current_level.get_sprites_by_tag("crease"):
            if sp.interaction == InteractionMode.REMOVED:
                continue
            self._paint_crease(sp, target)

    # -- halo -----------------------------------------------------------

    def _update_halo(self) -> None:
        halos = self.current_level.get_sprites_by_tag("halo")
        if not halos:
            return
        halo = halos[0]
        if self.selected_stamp is not None and self.selected_stamp.interaction != InteractionMode.REMOVED:
            hx = max(0, self.selected_stamp.x - 1)
            hy = max(0, self.selected_stamp.y - 1)
            halo.set_position(hx, hy)
            halo.set_interaction(InteractionMode.INTANGIBLE)
        else:
            halo.set_interaction(InteractionMode.REMOVED)

    # -- step dispatch --------------------------------------------------

    def step(self) -> None:
        self.hud.set_current(self.hud.current - 1)
        if self.hud.current <= 0:
            if not self._check_win():
                self.lose()
                self.complete_action()
                return

        action_id = self.action.id
        if action_id == GameAction.ACTION6:
            self._handle_click()
        elif action_id == GameAction.ACTION5:
            self._handle_fold()
        elif action_id in (
            GameAction.ACTION1,
            GameAction.ACTION2,
            GameAction.ACTION3,
            GameAction.ACTION4,
        ):
            self._handle_arrow(action_id)

        self._update_halo()
        self._update_crease_color()

        if self._check_win():
            self.next_level()
            self.complete_action()
            return
        if self._check_unwinnable():
            self.lose()
            self.complete_action()
            return

        self.complete_action()

    # -- arrow handling -------------------------------------------------

    def _handle_arrow(self, action_id: GameAction) -> None:
        dx = dy = 0
        if action_id == GameAction.ACTION1:
            dy = -ARROW_STEP
        elif action_id == GameAction.ACTION2:
            dy = ARROW_STEP
        elif action_id == GameAction.ACTION3:
            dx = -ARROW_STEP
        elif action_id == GameAction.ACTION4:
            dx = ARROW_STEP

        if self.selected_stamp is not None and self.selected_stamp.interaction != InteractionMode.REMOVED:
            self._try_move_stamp(self.selected_stamp, dx, dy)
            return

        if self.crease_selected and self.crease_movable:
            self._try_move_crease(dx, dy)

    def _try_move_stamp(self, stamp: Sprite, dx: int, dy: int) -> None:
        new_x = stamp.x + dx
        new_y = stamp.y + dy
        if new_x < 0 or new_x + STAMP_SIZE > GRID:
            return
        if new_y < 1 or new_y + STAMP_SIZE > GRID:
            return
        if self._move_crosses_crease(stamp, new_x, new_y):
            return
        if self._move_collides_with_other_stamp(stamp, new_x, new_y):
            return
        stamp.set_position(new_x, new_y)

    def _move_crosses_crease(self, stamp: Sprite, new_x: int, new_y: int) -> bool:
        if self.crease_orient == "H":
            R = self.crease_pos
            cur_above = (stamp.y + STAMP_SIZE - 1) < R
            cur_below = stamp.y > R
            new_above = (new_y + STAMP_SIZE - 1) < R
            new_below = new_y > R
            if cur_above and not new_above:
                return True
            if cur_below and not new_below:
                return True
            if not cur_above and not cur_below:
                return True
            return False
        else:
            C = self.crease_pos
            cur_left = (stamp.x + STAMP_SIZE - 1) < C
            cur_right = stamp.x > C
            new_left = (new_x + STAMP_SIZE - 1) < C
            new_right = new_x > C
            if cur_left and not new_left:
                return True
            if cur_right and not new_right:
                return True
            if not cur_left and not cur_right:
                return True
            return False

    def _move_collides_with_other_stamp(self, stamp: Sprite, new_x: int, new_y: int) -> bool:
        for other in self.current_level.get_sprites_by_tag("stamp"):
            if other is stamp:
                continue
            if other.interaction == InteractionMode.REMOVED:
                continue
            if not (
                new_x + STAMP_SIZE <= other.x
                or new_x >= other.x + STAMP_SIZE
                or new_y + STAMP_SIZE <= other.y
                or new_y >= other.y + STAMP_SIZE
            ):
                if self._pixels_overlap(stamp, new_x, new_y, other):
                    return True
        return False

    def _pixels_overlap(self, stamp: Sprite, new_x: int, new_y: int, other: Sprite) -> bool:
        sp = stamp.pixels
        op = other.pixels
        for dy in range(STAMP_SIZE):
            for dx in range(STAMP_SIZE):
                if sp[dy, dx] < 0:
                    continue
                ox = (new_x + dx) - other.x
                oy = (new_y + dy) - other.y
                if 0 <= ox < STAMP_SIZE and 0 <= oy < STAMP_SIZE:
                    if op[oy, ox] >= 0:
                        return True
        return False

    def _try_move_crease(self, dx: int, dy: int) -> None:
        if self.crease_orient == "H":
            if dx != 0:
                return
            new_pos = self.crease_pos + dy
        else:
            if dy != 0:
                return
            new_pos = self.crease_pos + dx
        if new_pos < 6 or new_pos > 58:
            return
        if not self._every_stamp_clear_of_crease(self.crease_orient, new_pos):
            return
        self.crease_pos = new_pos
        self._activate_crease()

    def _every_stamp_clear_of_crease(self, orient: str, pos: int) -> bool:
        for stamp in self.current_level.get_sprites_by_tag("stamp"):
            if stamp.interaction == InteractionMode.REMOVED:
                continue
            if orient == "H":
                top = stamp.y
                bot = stamp.y + STAMP_SIZE - 1
                if top <= pos <= bot:
                    return False
            else:
                left = stamp.x
                right = stamp.x + STAMP_SIZE - 1
                if left <= pos <= right:
                    return False
        return True

    # -- click handling -------------------------------------------------

    def _handle_click(self) -> None:
        if "x" not in self.action.data or "y" not in self.action.data:
            return
        px = int(self.action.data["x"])
        py = int(self.action.data["y"])
        grid_pos = self.camera.display_to_grid(px, py)
        if grid_pos is None:
            return
        gx, gy = grid_pos

        stamp_at = self._find_stamp_at(gx, gy)
        if stamp_at is not None:
            self.selected_stamp = stamp_at
            self.crease_selected = False
            return

        if self.crease_movable and self._is_crease_cell(gx, gy):
            if self.crease_selected:
                if self.crease_orient == "H":
                    self.crease_orient = "V"
                    self.crease_pos = gx
                else:
                    self.crease_orient = "H"
                    self.crease_pos = gy
                self._activate_crease()
            else:
                self.selected_stamp = None
                self.crease_selected = True
            return

        self.selected_stamp = None
        self.crease_selected = False

    def _find_stamp_at(self, gx: int, gy: int) -> Sprite | None:
        for stamp in self.current_level.get_sprites_by_tag("stamp"):
            if stamp.interaction == InteractionMode.REMOVED:
                continue
            if stamp.x <= gx < stamp.x + STAMP_SIZE and stamp.y <= gy < stamp.y + STAMP_SIZE:
                return stamp
        return None

    def _is_crease_cell(self, gx: int, gy: int) -> bool:
        if self.crease_orient == "H":
            return gy == self.crease_pos and CREASE_OFFSET <= gx < CREASE_OFFSET + CREASE_LENGTH
        return gx == self.crease_pos and CREASE_OFFSET <= gy < CREASE_OFFSET + CREASE_LENGTH

    # -- fold -----------------------------------------------------------

    def _handle_fold(self) -> None:
        stamp = self.selected_stamp
        if stamp is None or stamp.interaction == InteractionMode.REMOVED:
            return
        sp = stamp.pixels
        h, w = sp.shape
        for dy in range(h):
            for dx in range(w):
                color = int(sp[dy, dx])
                if color < 0:
                    continue
                wx = stamp.x + dx
                wy = stamp.y + dy
                if self.crease_orient == "H":
                    R = self.crease_pos
                    rx = wx
                    ry = 2 * R - wy
                else:
                    C = self.crease_pos
                    rx = 2 * C - wx
                    ry = wy
                if 0 <= rx < GRID and 0 <= ry < GRID:
                    self.cells_covered[(rx, ry)] = color
        stamp.set_interaction(InteractionMode.REMOVED)
        self.selected_stamp = None

    # -- win / lose -----------------------------------------------------

    def _iter_shadow_cells(self):
        for shadow in self.current_level.get_sprites_by_tag("shadow"):
            if shadow.interaction == InteractionMode.REMOVED:
                continue
            sp = shadow.pixels
            h, w = sp.shape
            for dy in range(h):
                for dx in range(w):
                    sc = int(sp[dy, dx])
                    if sc < 0:
                        continue
                    yield shadow, shadow.x + dx, shadow.y + dy, sc

    def _check_win(self) -> bool:
        for _shadow, wx, wy, shadow_color in self._iter_shadow_cells():
            expected = SHADOW_TO_STAMP_COLOR.get(shadow_color)
            if expected is None:
                continue
            if self.cells_covered.get((wx, wy)) != expected:
                return False
        return True

    def _check_unwinnable(self) -> bool:
        uncovered_colors: set[int] = set()
        for _shadow, wx, wy, shadow_color in self._iter_shadow_cells():
            expected = SHADOW_TO_STAMP_COLOR.get(shadow_color)
            if expected is None:
                continue
            if self.cells_covered.get((wx, wy)) != expected:
                uncovered_colors.add(shadow_color)
        for shadow_color in uncovered_colors:
            stamp_tag = SHADOW_TO_STAMP_TAG.get(shadow_color)
            if stamp_tag is None:
                continue
            remaining = [
                s
                for s in self.current_level.get_sprites_by_tag(stamp_tag)
                if s.interaction != InteractionMode.REMOVED
            ]
            if not remaining:
                return True
        return False

    # -- engine hooks ---------------------------------------------------

    def _get_hidden_state(self) -> np.ndarray:
        s = np.zeros((4, 4), dtype=np.int16)
        s[0, 0] = self.hud.current
        s[0, 1] = self.crease_pos
        s[0, 2] = 0 if self.crease_orient == "H" else 1
        s[0, 3] = 1 if self.crease_selected else 0
        s[1, 0] = len(self.cells_covered)
        if self.selected_stamp is not None and self.selected_stamp.interaction != InteractionMode.REMOVED:
            s[1, 1] = 1
            s[1, 2] = self.selected_stamp.x
            s[1, 3] = self.selected_stamp.y
        return s

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()
