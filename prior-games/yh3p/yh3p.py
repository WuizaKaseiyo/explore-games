"""yh3p — generated game (single-file source)."""

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
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "bloom": Sprite(
        pixels=[
            [12, 12, 12, 12],
            [12,  7,  6, 12],
            [12,  6,  7, 12],
            [12, 12, 12, 12],
        ],
        name="bloom",
        visible=True,
        collidable=True,
        tags=["bloom", "vine"],
        layer=1,
    ),
    "bud_closed": Sprite(
        pixels=[
            [12, 12, 12, 12],
            [12,  6,  6, 12],
            [12,  6,  6, 12],
            [12, 12, 12, 12],
        ],
        name="bud_closed",
        visible=True,
        collidable=True,
        tags=["bud_closed"],
        layer=1,
    ),
    "bud_notched": Sprite(
        pixels=[
            [-1, 12, 12, -1],
            [12,  6,  6, 12],
            [12,  6,  6, 12],
            [-1, 11, 11, -1],
        ],
        name="bud_notched",
        visible=True,
        collidable=True,
        tags=["bud_notched"],
        layer=1,
    ),
    "root": Sprite(
        pixels=[
            [13,  8,  8, 13],
            [ 8, 14, 14,  8],
            [ 8, 14, 14,  8],
            [13,  8,  8, 13],
        ],
        name="root",
        visible=True,
        collidable=True,
        tags=["root", "vine"],
        layer=1,
    ),
    "stalk": Sprite(
        pixels=[
            [-1, 14, 14, -1],
            [14, 13, 13, 14],
            [14, 13, 13, 14],
            [-1, 14, 14, -1],
        ],
        name="stalk",
        visible=True,
        collidable=True,
        tags=["stalk", "vine"],
        layer=1,
    ),
    "tip_active": Sprite(
        pixels=[
            [-1, 11, 11, -1],
            [11, 11, 11, 11],
            [11,  8,  8, 11],
            [14, 11, 11, 14],
        ],
        name="tip_active",
        visible=True,
        collidable=False,
        blocking=BlockingMode.NOT_BLOCKED,
        tags=["tip"],
        layer=3,
    ),
    "tip_dormant": Sprite(
        pixels=[
            [-1,  0,  0, -1],
            [ 0,  3,  3,  0],
            [ 0,  3,  3,  0],
            [-1,  0,  0, -1],
        ],
        name="tip_dormant",
        visible=True,
        collidable=False,
        blocking=BlockingMode.NOT_BLOCKED,
        tags=["tip"],
        layer=3,
    ),
    "wall": Sprite(
        pixels=[
            [ 4,  3,  3,  4],
            [ 3,  4,  4,  3],
            [ 3,  4,  4,  3],
            [ 4,  3,  3,  4],
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
CELL = 4  # display pixels per logical grid cell


def _at(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _wall_col(cx: int, cy_start: int, cy_end: int) -> list[Sprite]:
    return [
        sprites["wall"].clone().set_position(*_at(cx, cy))
        for cy in range(cy_start, cy_end + 1)
    ]


def _wall_row(cy: int, cx_start: int, cx_end: int) -> list[Sprite]:
    return [
        sprites["wall"].clone().set_position(*_at(cx, cy))
        for cx in range(cx_start, cx_end + 1)
    ]


def _tip_pair(cx: int, cy: int) -> list[Sprite]:
    return [
        sprites["tip_active"].clone().set_position(*_at(cx, cy)),
        sprites["tip_dormant"].clone().set_position(*_at(cx, cy)),
    ]


levels = [
    # Level 1 — single straight corridor.
    Level(
        sprites=[
            sprites["root"].clone().set_position(*_at(3, 7)),
            sprites["bud_closed"].clone().set_position(*_at(15, 7)),
            *_tip_pair(3, 7),
        ],
        grid_size=(64, 64),
        data={"step_budget": 24},
    ),
    # Level 2 — sealed wall column with a single bottom-row gap;
    # two targets in opposite regions.
    Level(
        sprites=[
            sprites["root"].clone().set_position(*_at(4, 8)),
            sprites["bud_closed"].clone().set_position(*_at(4, 2)),
            sprites["bud_closed"].clone().set_position(*_at(12, 8)),
            *_wall_col(8, 0, 14),
            *_tip_pair(4, 8),
        ],
        grid_size=(64, 64),
        data={"step_budget": 50},
    ),
    # Level 3 — L-shaped walls partition the playfield into four
    # quadrants connected by single-cell gaps; three notched
    # targets each demand a specific arrival direction.
    Level(
        sprites=[
            sprites["root"].clone().set_position(*_at(4, 4)),
            sprites["bud_notched"].clone().set_position(*_at(12, 4)).set_rotation(180),
            sprites["bud_notched"].clone().set_position(*_at(4, 12)).set_rotation(270),
            sprites["bud_notched"].clone().set_position(*_at(12, 12)).set_rotation(0),
            *_wall_col(8, 0, 6),
            *_wall_row(8, 0, 6),
            *_tip_pair(4, 4),
        ],
        grid_size=(64, 64),
        data={"step_budget": 100},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 2
PADDING_COLOR = 5

DIRECTION_MAP = {
    GameAction.ACTION1: ("UP", 0, -CELL),
    GameAction.ACTION2: ("DOWN", 0, CELL),
    GameAction.ACTION3: ("LEFT", -CELL, 0),
    GameAction.ACTION4: ("RIGHT", CELL, 0),
}
ROTATION_MAP = {"UP": 0, "RIGHT": 90, "DOWN": 180, "LEFT": 270}
BUD_ROT_TO_INTAKE_FACING = {0: "UP", 90: "RIGHT", 180: "DOWN", 270: "LEFT"}


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class StepBarHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0):
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_max(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def consume(self) -> None:
        if self.current_steps > 0:
            self.current_steps -= 1

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        ratio = self.current_steps / self.max_steps
        filled = round(64 * ratio)
        for x in range(64):
            frame[0, x] = 7 if x < filled else 3
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Yh3p(NovaBaseGame):
    def __init__(self) -> None:
        self._active_tip_cell: tuple[int, int] = (0, 0)
        self._tip_facing: str | None = None
        self._vine_cells: set[tuple[int, int]] = set()
        self._tip_blocked_on_notched: bool = False
        self._tip_active_sprite: Sprite | None = None
        self._tip_dormant_sprite: Sprite | None = None
        self._step_bar = StepBarHud(0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_bar],
        )
        super().__init__(
            game_id="yh3p",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        budget = level.get_data("step_budget") or 50
        self._step_bar.set_max(budget)
        roots = level.get_sprites_by_tag("root")
        if not roots:
            return
        root = roots[0]
        self._active_tip_cell = (root.x, root.y)
        self._tip_facing = None
        self._vine_cells = {(root.x, root.y)}
        self._tip_blocked_on_notched = False
        self._tip_active_sprite = None
        self._tip_dormant_sprite = None
        for t in level.get_sprites_by_tag("tip"):
            if t.name == "tip_active":
                self._tip_active_sprite = t
            elif t.name == "tip_dormant":
                self._tip_dormant_sprite = t
        self._refresh_tip_visual()

    def _refresh_tip_visual(self) -> None:
        if self._tip_active_sprite is None or self._tip_dormant_sprite is None:
            return
        ax, ay = self._active_tip_cell
        self._tip_active_sprite.set_position(ax, ay)
        self._tip_dormant_sprite.set_position(ax, ay)
        if self._tip_facing is None:
            self._tip_active_sprite.set_interaction(InteractionMode.REMOVED)
            self._tip_dormant_sprite.set_interaction(InteractionMode.TANGIBLE)
        else:
            self._tip_active_sprite.set_interaction(InteractionMode.TANGIBLE)
            self._tip_active_sprite.set_rotation(ROTATION_MAP[self._tip_facing])
            self._tip_dormant_sprite.set_interaction(InteractionMode.REMOVED)

    def _wall_at(self, x: int, y: int) -> bool:
        for s in self.current_level.get_sprites_by_tag("wall"):
            if s.x == x and s.y == y:
                return True
        return False

    def _bud_at(self, x: int, y: int, tag: str) -> Sprite | None:
        for s in self.current_level.get_sprites_by_tag(tag):
            if s.x == x and s.y == y:
                return s
        return None

    def _handle_extend(self, direction: str, dx: int, dy: int) -> None:
        if self._tip_blocked_on_notched:
            return
        cur_x, cur_y = self._active_tip_cell
        new_x, new_y = cur_x + dx, cur_y + dy
        if not (0 <= new_x <= 60 and 0 <= new_y <= 60):
            return
        if (new_x, new_y) in self._vine_cells:
            return
        if self._wall_at(new_x, new_y):
            return
        bud_closed = self._bud_at(new_x, new_y, "bud_closed")
        bud_notched = self._bud_at(new_x, new_y, "bud_notched")
        if bud_closed is not None:
            self.current_level.remove_sprite(bud_closed)
            new_bloom = sprites["bloom"].clone().set_position(new_x, new_y)
            self.current_level.add_sprite(new_bloom)
            self._vine_cells.add((new_x, new_y))
            self._active_tip_cell = (new_x, new_y)
            self._tip_facing = direction
            self._tip_blocked_on_notched = False
        elif bud_notched is not None:
            self._active_tip_cell = (new_x, new_y)
            self._tip_facing = direction
            self._tip_blocked_on_notched = True
        else:
            new_stalk = sprites["stalk"].clone().set_position(new_x, new_y)
            self.current_level.add_sprite(new_stalk)
            self._vine_cells.add((new_x, new_y))
            self._active_tip_cell = (new_x, new_y)
            self._tip_facing = direction
            self._tip_blocked_on_notched = False
        self._refresh_tip_visual()

    def _handle_bloom(self) -> None:
        if self._tip_facing is None:
            return
        ax, ay = self._active_tip_cell
        bud_notched = self._bud_at(ax, ay, "bud_notched")
        if bud_notched is None:
            return
        intake_facing = BUD_ROT_TO_INTAKE_FACING.get(bud_notched.rotation)
        if intake_facing != self._tip_facing:
            return
        self.current_level.remove_sprite(bud_notched)
        new_bloom = sprites["bloom"].clone().set_position(ax, ay)
        self.current_level.add_sprite(new_bloom)
        self._vine_cells.add((ax, ay))
        self._tip_facing = None
        self._tip_blocked_on_notched = False
        self._refresh_tip_visual()

    def _handle_click(self) -> None:
        click_x = int(self.action.data.get("x", 0))
        click_y = int(self.action.data.get("y", 0))
        grid = self.camera.display_to_grid(click_x, click_y)
        if grid is None:
            return
        gx, gy = grid
        cx = (int(gx) // CELL) * CELL
        cy = (int(gy) // CELL) * CELL
        if (cx, cy) not in self._vine_cells:
            return
        self._active_tip_cell = (cx, cy)
        self._tip_facing = None
        self._tip_blocked_on_notched = False
        self._refresh_tip_visual()

    def step(self) -> None:
        if self.action.id == GameAction.RESET:
            self.complete_action()
            return
        self._step_bar.consume()
        if self.action.id in DIRECTION_MAP:
            direction, dx, dy = DIRECTION_MAP[self.action.id]
            self._handle_extend(direction, dx, dy)
        elif self.action.id == GameAction.ACTION5:
            self._handle_bloom()
        elif self.action.id == GameAction.ACTION6:
            self._handle_click()
        if self._check_win():
            self.next_level()
        elif self._step_bar.current_steps <= 0:
            self.lose()
        self.complete_action()

    def _check_win(self) -> bool:
        remaining = (
            self.current_level.get_sprites_by_tag("bud_closed")
            + self.current_level.get_sprites_by_tag("bud_notched")
        )
        return len(remaining) == 0

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 1), dtype=np.int16)
        state[0, 0] = self._step_bar.current_steps
        return state
