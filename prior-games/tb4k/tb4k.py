"""tb4k — generated game."""

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

BACKGROUND_COLOR = 2
PADDING_COLOR = 3
GRID_CELLS = 16
PIXELS_PER_CELL = 2

# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "brick_lying_h": Sprite(
        pixels=[
            [4, 3, 3, 4],
            [3, 5, 5, 3],
        ],
        name="brick_lying_h",
        visible=True,
        collidable=True,
        tags=["brick"],
        layer=5,
    ),
    "brick_lying_v": Sprite(
        pixels=[
            [4, 3],
            [3, 5],
            [3, 5],
            [4, 3],
        ],
        name="brick_lying_v",
        visible=True,
        collidable=True,
        tags=["brick"],
        layer=5,
    ),
    "brick_standing": Sprite(
        pixels=[
            [4, 3],
            [3, 5],
        ],
        name="brick_standing",
        visible=True,
        collidable=True,
        tags=["brick"],
        layer=5,
    ),
    "goal_pad": Sprite(
        pixels=[
            [10, 9],
            [9, 10],
        ],
        name="goal_pad",
        visible=True,
        collidable=True,
        tags=["goal"],
        layer=2,
    ),
    "hole_tile": Sprite(
        pixels=[
            [13, 5],
            [5, 13],
        ],
        name="hole_tile",
        visible=True,
        collidable=True,
        tags=["hole"],
        layer=1,
    ),
    "life_pip": Sprite(
        pixels=[
            [13, 12],
            [12, 13],
        ],
        name="life_pip",
        visible=True,
        collidable=True,
        tags=["lives_hud"],
        layer=8,
    ),
}


def _placed(key: str, cx: int, cy: int) -> Sprite:
    return sprites[key].clone().set_position(cx * PIXELS_PER_CELL, cy * PIXELS_PER_CELL)


def _l3_holes() -> list[Sprite]:
    out = []
    for cx in (6, 7, 8, 9):
        for cy in range(1, GRID_CELLS):
            if cy != 3:
                out.append(_placed("hole_tile", cx, cy))
    return out


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
levels = [
    Level(
        sprites=[
            _placed("brick_standing", 3, 3),
            _placed("brick_lying_h", 3, 3),
            _placed("brick_lying_v", 3, 3),
            _placed("goal_pad", 11, 11),
        ],
        grid_size=(32, 32),
        data={"start": (3, 3), "goal": (11, 11), "step_budget": 40, "lives": 0},
    ),
    Level(
        sprites=[
            _placed("brick_standing", 2, 4),
            _placed("brick_lying_h", 2, 4),
            _placed("brick_lying_v", 2, 4),
            _placed("goal_pad", 14, 4),
            _placed("hole_tile", 7, 3),
            _placed("hole_tile", 8, 3),
            _placed("hole_tile", 9, 3),
            _placed("hole_tile", 8, 4),
            _placed("hole_tile", 7, 5),
            _placed("hole_tile", 8, 5),
            _placed("hole_tile", 9, 5),
            _placed("hole_tile", 10, 5),
            _placed("hole_tile", 11, 5),
            _placed("life_pip", 13, 0),
            _placed("life_pip", 14, 0),
            _placed("life_pip", 15, 0),
        ],
        grid_size=(32, 32),
        data={"start": (2, 4), "goal": (14, 4), "step_budget": 60, "lives": 3},
    ),
    Level(
        sprites=[
            _placed("brick_standing", 2, 5),
            _placed("brick_lying_h", 2, 5),
            _placed("brick_lying_v", 2, 5),
            _placed("goal_pad", 12, 1),
            *_l3_holes(),
            _placed("life_pip", 13, 0),
            _placed("life_pip", 14, 0),
            _placed("life_pip", 15, 0),
        ],
        grid_size=(32, 32),
        data={"start": (2, 5), "goal": (12, 1), "step_budget": 70, "lives": 3},
    ),
]


# ---------------------------------------------------------------------
# 3. HUD
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, initial_max: int) -> None:
        self.max_steps = max(1, initial_max)
        self.current_steps = self.max_steps

    def set_max(self, m: int) -> None:
        self.max_steps = max(1, m)
        self.current_steps = self.max_steps

    def set_current(self, c: int) -> None:
        self.current_steps = max(0, min(c, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        bar_width = 32
        x_offset = (64 - bar_width) // 2
        fraction = self.current_steps / self.max_steps
        filled = round(bar_width * fraction)
        filled = min(filled, bar_width)
        depleted = bar_width - filled
        for x in range(bar_width):
            if x < depleted:
                frame[0, x_offset + x] = 3
            else:
                frame[0, x_offset + x] = 1
        return frame


# ---------------------------------------------------------------------
# 4. THE GAME CLASS
# ---------------------------------------------------------------------
class Tb4k(NovaBaseGame):
    def __init__(self) -> None:
        self.step_counter_ui = StepCounterHud(initial_max=40)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_counter_ui],
        )
        self.brick_state: str = "standing"
        self.brick_cell: tuple[int, int] = (0, 0)
        self.start_cell: tuple[int, int] = (0, 0)
        self.goal_cell: tuple[int, int] = (0, 0)
        self.step_budget: int = 40
        self.lives_remaining: int = 0
        self.hole_cells: set[tuple[int, int]] = set()
        self._brick_standing: Sprite | None = None
        self._brick_lying_h: Sprite | None = None
        self._brick_lying_v: Sprite | None = None
        self._life_pips: list[Sprite] = []
        super().__init__(
            game_id="tb4k",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        self.start_cell = level.get_data("start") or (0, 0)
        self.goal_cell = level.get_data("goal") or (0, 0)
        self.step_budget = level.get_data("step_budget") or 40
        lives = level.get_data("lives")
        self.lives_remaining = lives if lives is not None else 0

        self.step_counter_ui.set_max(self.step_budget)

        self._brick_standing = None
        self._brick_lying_h = None
        self._brick_lying_v = None
        for b in level.get_sprites_by_tag("brick"):
            if b.name == "brick_standing":
                self._brick_standing = b
            elif b.name == "brick_lying_h":
                self._brick_lying_h = b
            elif b.name == "brick_lying_v":
                self._brick_lying_v = b

        self.hole_cells = set()
        for h in level.get_sprites_by_tag("hole"):
            self.hole_cells.add((h.x // PIXELS_PER_CELL, h.y // PIXELS_PER_CELL))

        self._life_pips = list(level.get_sprites_by_tag("lives_hud"))
        for i, pip in enumerate(self._life_pips):
            if i < self.lives_remaining:
                pip.set_interaction(InteractionMode.TANGIBLE)
            else:
                pip.set_interaction(InteractionMode.REMOVED)

        self._respawn_brick()

    def _respawn_brick(self) -> None:
        cx, cy = self.start_cell
        self.brick_state = "standing"
        self.brick_cell = (cx, cy)
        self._apply_brick()

    def _apply_brick(self) -> None:
        if self._brick_standing is None or self._brick_lying_h is None or self._brick_lying_v is None:
            return
        cx, cy = self.brick_cell
        self._brick_standing.set_interaction(InteractionMode.REMOVED)
        self._brick_lying_h.set_interaction(InteractionMode.REMOVED)
        self._brick_lying_v.set_interaction(InteractionMode.REMOVED)
        if self.brick_state == "standing":
            active = self._brick_standing
        elif self.brick_state == "lying_h":
            active = self._brick_lying_h
        else:
            active = self._brick_lying_v
        active.set_position(cx * PIXELS_PER_CELL, cy * PIXELS_PER_CELL)
        active.set_interaction(InteractionMode.TANGIBLE)

    def _occupied_cells(self, state: str, cell: tuple[int, int]) -> list[tuple[int, int]]:
        cx, cy = cell
        if state == "standing":
            return [(cx, cy)]
        if state == "lying_h":
            return [(cx, cy), (cx + 1, cy)]
        return [(cx, cy), (cx, cy + 1)]

    def _tumble(self, direction: str) -> tuple[str, tuple[int, int]]:
        cx, cy = self.brick_cell
        s = self.brick_state
        if direction == "E":
            if s == "standing":
                return ("lying_h", (cx, cy))
            if s == "lying_h":
                return ("standing", (cx + 2, cy))
            return ("lying_v", (cx + 1, cy))
        if direction == "W":
            if s == "standing":
                return ("lying_h", (cx - 1, cy))
            if s == "lying_h":
                return ("standing", (cx - 1, cy))
            return ("lying_v", (cx - 1, cy))
        if direction == "N":
            if s == "standing":
                return ("lying_v", (cx, cy - 1))
            if s == "lying_h":
                return ("lying_h", (cx, cy - 1))
            return ("standing", (cx, cy - 1))
        # direction == "S"
        if s == "standing":
            return ("lying_v", (cx, cy))
        if s == "lying_h":
            return ("lying_h", (cx, cy + 1))
        return ("standing", (cx, cy + 2))

    def _within_bounds(self, occupied: list[tuple[int, int]]) -> bool:
        for cx, cy in occupied:
            if not (0 <= cx < GRID_CELLS and 1 <= cy < GRID_CELLS):
                return False
        return True

    def _on_hole(self, occupied: list[tuple[int, int]]) -> bool:
        for cell in occupied:
            if cell in self.hole_cells:
                return True
        return False

    def _check_win(self) -> bool:
        return self.brick_state == "standing" and self.brick_cell == self.goal_cell

    def _hard_death(self) -> None:
        if self.lives_remaining > 0:
            self.lives_remaining -= 1
            if self.lives_remaining < len(self._life_pips):
                self._life_pips[self.lives_remaining].set_interaction(InteractionMode.REMOVED)
            if self.lives_remaining == 0:
                self.lose()
                return
            self._respawn_brick()
        else:
            self.lose()

    def step(self) -> None:
        remaining = max(0, self.step_budget - self._action_count)
        self.step_counter_ui.set_current(remaining)

        if self._action_count >= self.step_budget:
            self.lose()
            self.complete_action()
            return

        direction_map = {
            GameAction.ACTION1: "N",
            GameAction.ACTION2: "S",
            GameAction.ACTION3: "W",
            GameAction.ACTION4: "E",
        }
        direction = direction_map.get(self.action.id)
        if direction is None:
            self.complete_action()
            return

        new_state, new_cell = self._tumble(direction)
        new_occupied = self._occupied_cells(new_state, new_cell)

        if not self._within_bounds(new_occupied):
            self.complete_action()
            return

        self.brick_state = new_state
        self.brick_cell = new_cell
        self._apply_brick()

        if self._on_hole(new_occupied):
            self._hard_death()
            self.complete_action()
            return

        if self._check_win():
            self.next_level()

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state_id = {"standing": 0, "lying_h": 1, "lying_v": 2}[self.brick_state]
        cx, cy = self.brick_cell
        return np.array([[state_id, cx, cy, self.lives_remaining]], dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
