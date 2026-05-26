"""A small herding environment on a 16x16 logical board."""

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
# Geometry
# ---------------------------------------------------------------------
CELL = 4          # display pixels per logical cell
GRID = 16         # logical cells per side -> 64x64 display
SCARE_RADIUS = 4  # Manhattan range within which a creature reacts

BACKGROUND_COLOR = 1   # off-white field
PADDING_COLOR = 1

# palette ids
TEAL = 10
ORANGE = 12
MAGENTA = 6
SLATE = 2
GREY = 3
BLACK = 5
PURPLE = 15
AMBER = 11
DARK = 4

# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "shepherd": Sprite(
        pixels=[
            [TEAL, BLACK, BLACK, TEAL],
            [TEAL, TEAL, TEAL, TEAL],
            [TEAL, TEAL, TEAL, TEAL],
            [GREY, TEAL, TEAL, GREY],
        ],
        name="shepherd",
        visible=True,
        collidable=True,
        tags=["shepherd"],
        layer=3,
    ),
    "creature_timid": Sprite(
        pixels=[
            [-1, ORANGE, ORANGE, -1],
            [ORANGE, BLACK, BLACK, ORANGE],
            [ORANGE, ORANGE, ORANGE, ORANGE],
            [-1, ORANGE, ORANGE, -1],
        ],
        name="creature_timid",
        visible=True,
        collidable=True,
        tags=["creature", "straight"],
        layer=2,
    ),
    "creature_skittish": Sprite(
        pixels=[
            [-1, MAGENTA, MAGENTA, -1],
            [MAGENTA, BLACK, BLACK, MAGENTA],
            [MAGENTA, MAGENTA, MAGENTA, MAGENTA],
            [MAGENTA, -1, -1, MAGENTA],
        ],
        name="creature_skittish",
        visible=True,
        collidable=True,
        tags=["creature", "perp"],
        layer=2,
    ),
    "pen_amber": Sprite(
        pixels=[
            [ORANGE, ORANGE, ORANGE, ORANGE],
            [ORANGE, -1, -1, ORANGE],
            [ORANGE, -1, -1, ORANGE],
            [ORANGE, ORANGE, ORANGE, ORANGE],
        ],
        name="pen_amber",
        visible=True,
        collidable=False,
        tags=["pen", "pen_straight"],
        layer=0,
    ),
    "pen_magenta": Sprite(
        pixels=[
            [MAGENTA, MAGENTA, MAGENTA, MAGENTA],
            [MAGENTA, -1, -1, MAGENTA],
            [MAGENTA, -1, -1, MAGENTA],
            [MAGENTA, MAGENTA, MAGENTA, MAGENTA],
        ],
        name="pen_magenta",
        visible=True,
        collidable=False,
        tags=["pen", "pen_perp"],
        layer=0,
    ),
    "wall_unit": Sprite(
        pixels=[
            [SLATE, SLATE, GREY, GREY],
            [SLATE, GREY, GREY, GREY],
            [GREY, GREY, GREY, GREY],
            [GREY, GREY, GREY, GREY],
        ],
        name="wall_unit",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=1,
    ),
    "gate_closed": Sprite(
        pixels=[
            [PURPLE, PURPLE, PURPLE, PURPLE],
            [PURPLE, BLACK, BLACK, PURPLE],
            [PURPLE, BLACK, BLACK, PURPLE],
            [PURPLE, PURPLE, PURPLE, PURPLE],
        ],
        name="gate_closed",
        visible=True,
        collidable=True,
        tags=["gate", "gate_closed"],
        layer=1,
    ),
    "gate_open": Sprite(
        pixels=[
            [PURPLE, -1, -1, PURPLE],
            [PURPLE, -1, -1, PURPLE],
            [PURPLE, -1, -1, PURPLE],
            [PURPLE, -1, -1, PURPLE],
        ],
        name="gate_open",
        visible=True,
        collidable=False,
        tags=["gate", "gate_open"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# Level construction helpers
# ---------------------------------------------------------------------
def _px(cell):
    return cell * CELL


def _wall(cell_x, cell_y):
    return sprites["wall_unit"].clone(new_name=f"wall_{cell_x}_{cell_y}").set_position(_px(cell_x), _px(cell_y))


def _border_walls():
    placed = []
    for i in range(GRID):
        placed.append(_wall(0, i))
        placed.append(_wall(GRID - 1, i))
        if 0 < i < GRID - 1:
            placed.append(_wall(i, 0))
            placed.append(_wall(i, GRID - 1))
    return placed


def _shepherd(cx, cy):
    return sprites["shepherd"].clone(new_name="shepherd").set_position(_px(cx), _px(cy))


def _timid(cx, cy, idx):
    return sprites["creature_timid"].clone(new_name=f"timid_{idx}").set_position(_px(cx), _px(cy))


def _skittish(cx, cy, idx):
    return sprites["creature_skittish"].clone(new_name=f"skittish_{idx}").set_position(_px(cx), _px(cy))


def _pen_amber(cx, cy, idx):
    return sprites["pen_amber"].clone(new_name=f"pen_amber_{idx}").set_position(_px(cx), _px(cy))


def _pen_magenta(cx, cy, idx):
    return sprites["pen_magenta"].clone(new_name=f"pen_magenta_{idx}").set_position(_px(cx), _px(cy))


def _gate_pair(cx, cy):
    closed = sprites["gate_closed"].clone(new_name="gate_closed").set_position(_px(cx), _px(cy))
    opened = (
        sprites["gate_open"]
        .clone(new_name="gate_open")
        .set_position(_px(cx), _px(cy))
        .set_interaction(InteractionMode.REMOVED)
    )
    return [closed, opened]


# ---- Level 1 ---------------------------------------------------------
_l1 = _border_walls()
_l1 += [
    _pen_amber(14, 3, 0),
    _timid(10, 8, 0),
    _shepherd(7, 11),
]
level1 = Level(sprites=_l1, grid_size=(64, 64), data={"max_steps": 44})

# ---- Level 2 ---------------------------------------------------------
_l2 = _border_walls()
for x in range(1, GRID - 1):
    if x != 8:
        _l2.append(_wall(x, 8))
_l2 += _gate_pair(8, 8)
_l2 += [
    _pen_amber(8, 13, 0),
    _pen_amber(1, 4, 1),
    _timid(8, 5, 0),
    _timid(4, 4, 1),
    _shepherd(8, 2),
]
level2 = Level(sprites=_l2, grid_size=(64, 64), data={"max_steps": 80})

# ---- Level 3 ---------------------------------------------------------
_l3 = _border_walls()
for y in range(1, GRID - 1):
    if y != 8:
        _l3.append(_wall(8, y))
_l3 += _gate_pair(8, 8)
_l3 += [
    _pen_amber(12, 8, 0),
    _pen_magenta(1, 11, 0),
    _timid(4, 8, 0),
    _skittish(5, 11, 0),
    _shepherd(2, 8),
]
level3 = Level(sprites=_l3, grid_size=(64, 64), data={"max_steps": 90})

levels = [level1, level2, level3]


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0):
        self.max_steps = max_steps
        self.current = max_steps

    def configure(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current = max_steps

    def set_current(self, remaining: int) -> None:
        self.current = max(0, min(remaining, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        filled = round(64 * (self.current / self.max_steps))
        for x in range(64):
            frame[0, x] = AMBER if x < filled else DARK
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Hd7r(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = StepCounterHud(0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._hud],
        )
        self._steps_used = 0
        self.max_steps = 0
        super().__init__(
            game_id="hd7r",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 6],
        )

    # -- per-level setup ------------------------------------------------
    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        self._steps_used = 0
        self.max_steps = level.get_data("max_steps") or 60
        self._hud.configure(self.max_steps)

    # -- geometry queries ----------------------------------------------
    def _occupied_cell(self, sprite) -> tuple:
        return (sprite.x // CELL, sprite.y // CELL)

    def _blocked_cells(self) -> set:
        """Cells a creature or the shepherd cannot enter (walls + closed gates)."""
        blocked = set()
        for w in self.current_level.get_sprites_by_tag("wall"):
            blocked.add(self._occupied_cell(w))
        for g in self.current_level.get_sprites_by_tag("gate"):
            if "gate_closed" in g.tags and g.interaction != InteractionMode.REMOVED:
                blocked.add(self._occupied_cell(g))
        return blocked

    def _creature_cells(self, exclude=None) -> set:
        cells = set()
        for c in self.current_level.get_sprites_by_tag("creature"):
            if c is exclude:
                continue
            cells.add(self._occupied_cell(c))
        return cells

    # -- shepherd movement ---------------------------------------------
    def _move_shepherd(self, dcx: int, dcy: int) -> None:
        shep = self.current_level.get_sprites_by_tag("shepherd")[0]
        cx, cy = self._occupied_cell(shep)
        tx, ty = cx + dcx, cy + dcy
        if not (0 <= tx < GRID and 0 <= ty < GRID):
            return
        target = (tx, ty)
        if target in self._blocked_cells():
            return
        if target in self._creature_cells():
            return
        shep.set_position(_px(tx), _px(ty))

    # -- the flee response ---------------------------------------------
    def _resolve_flee(self) -> None:
        shep = self.current_level.get_sprites_by_tag("shepherd")[0]
        scx, scy = self._occupied_cell(shep)
        blocked = self._blocked_cells()
        creatures = list(self.current_level.get_sprites_by_tag("creature"))
        occupied = {self._occupied_cell(c) for c in creatures}
        for c in creatures:
            cx, cy = self._occupied_cell(c)
            dx = cx - scx
            dy = cy - scy
            if dx == 0 and dy == 0:
                continue
            if abs(dx) + abs(dy) > SCARE_RADIUS:
                continue
            if "perp" in c.tags:
                if abs(dx) >= abs(dy):
                    ax, ay = (1 if dx > 0 else -1), 0
                else:
                    ax, ay = 0, (1 if dy > 0 else -1)
                mvx, mvy = ay, -ax
            else:
                if abs(dx) >= abs(dy):
                    mvx, mvy = (1 if dx > 0 else -1), 0
                else:
                    mvx, mvy = 0, (1 if dy > 0 else -1)
            ntx, nty = cx + mvx, cy + mvy
            if not (0 <= ntx < GRID and 0 <= nty < GRID):
                continue
            tgt = (ntx, nty)
            if tgt in blocked:
                continue
            if tgt in (occupied - {(cx, cy)}):
                continue
            occupied.discard((cx, cy))
            occupied.add(tgt)
            c.set_position(_px(ntx), _px(nty))

    # -- gate toggle ----------------------------------------------------
    def _toggle_gate_at(self, gx: int, gy: int) -> bool:
        closed = None
        opened = None
        for g in self.current_level.get_sprites_by_tag("gate"):
            if self._occupied_cell(g) == (gx, gy):
                if "gate_closed" in g.tags:
                    closed = g
                elif "gate_open" in g.tags:
                    opened = g
        if closed is None or opened is None:
            return False
        if closed.interaction != InteractionMode.REMOVED:
            closed.set_interaction(InteractionMode.REMOVED)
            opened.set_interaction(InteractionMode.TANGIBLE)
        else:
            closed.set_interaction(InteractionMode.TANGIBLE)
            opened.set_interaction(InteractionMode.REMOVED)
        return True

    # -- win test -------------------------------------------------------
    def _check_win(self) -> bool:
        pens = self.current_level.get_sprites_by_tag("pen")
        for c in self.current_level.get_sprites_by_tag("creature"):
            ccell = self._occupied_cell(c)
            want = "pen_straight" if "straight" in c.tags else "pen_perp"
            matched = False
            for p in pens:
                if want in p.tags and self._occupied_cell(p) == ccell:
                    matched = True
                    break
            if not matched:
                return False
        return True

    # -- main step ------------------------------------------------------
    def step(self) -> None:
        moved = False
        if self.action.id in (
            GameAction.ACTION1,
            GameAction.ACTION2,
            GameAction.ACTION3,
            GameAction.ACTION4,
        ):
            if self.action.id == GameAction.ACTION1:
                self._move_shepherd(0, -1)
            elif self.action.id == GameAction.ACTION2:
                self._move_shepherd(0, 1)
            elif self.action.id == GameAction.ACTION3:
                self._move_shepherd(-1, 0)
            elif self.action.id == GameAction.ACTION4:
                self._move_shepherd(1, 0)
            self._resolve_flee()
            self._steps_used += 1
            moved = True
        elif self.action.id == GameAction.ACTION6:
            data = self.action.data or {}
            grid = self.camera.display_to_grid(int(data.get("x", 0)), int(data.get("y", 0)))
            if grid is not None:
                gx, gy = grid
                if self._toggle_gate_at(gx // CELL, gy // CELL):
                    self._steps_used += 1
                    moved = True

        if moved:
            self._hud.set_current(self.max_steps - self._steps_used)
            if self._check_win():
                self.next_level()
                self.complete_action()
                return
            if self._steps_used >= self.max_steps:
                self.lose()
                self.complete_action()
                return

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 1), dtype=np.int16)
        state[0, 0] = self.max_steps - self._steps_used
        return state

    def _get_valid_actions(self):
        return super()._get_valid_actions()
