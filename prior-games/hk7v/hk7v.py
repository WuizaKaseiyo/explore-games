"""hk7v — generated game."""

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

_WALL_PIXELS = [
    [4, 5, 4] if i % 2 == 0 else [4, 4, 4]
    for i in range(36)
]

sprites = {
    "beam": Sprite(
        pixels=[[3] * 64],
        name="beam",
        tags=["beam"],
        collidable=False,
        layer=1,
    ),
    "block_blue": Sprite(
        pixels=[
            [9, 9, 9, 9, 9],
            [9, 10, 9, 10, 9],
            [9, 9, 9, 9, 9],
            [9, 10, 9, 10, 9],
            [9, 9, 9, 9, 9],
        ],
        name="block_blue",
        tags=["block", "blue"],
        layer=3,
    ),
    "block_red": Sprite(
        pixels=[
            [8, 8, 8, 8, 8],
            [8, 13, 8, 13, 8],
            [8, 8, 8, 8, 8],
            [8, 13, 8, 13, 8],
            [8, 8, 8, 8, 8],
        ],
        name="block_red",
        tags=["block", "red"],
        layer=3,
    ),
    "block_yellow": Sprite(
        pixels=[
            [11, 11, 11, 11, 11],
            [11, 12, 11, 12, 11],
            [11, 11, 11, 11, 11],
            [11, 12, 11, 12, 11],
            [11, 11, 11, 11, 11],
        ],
        name="block_yellow",
        tags=["block", "yellow"],
        layer=3,
    ),
    "floor": Sprite(
        pixels=[[2] * 64],
        name="floor",
        tags=["floor"],
        collidable=False,
        layer=0,
    ),
    "hook": Sprite(
        pixels=[
            [-1, -1, 4, -1, -1],
            [3, 3, 3, 3, 3],
            [3, 4, -1, 4, 3],
            [3, 4, -1, 4, 3],
        ],
        name="hook",
        tags=["hook"],
        collidable=False,
        layer=4,
    ),
    "rope": Sprite(
        pixels=[[4]],
        name="rope",
        tags=["rope"],
        collidable=False,
        layer=4,
    ),
    "target_blue": Sprite(
        pixels=[[9, 9, -1, 9, -1, 9, 9]],
        name="target_blue",
        tags=["target", "blue"],
        collidable=False,
        layer=0,
    ),
    "target_red": Sprite(
        pixels=[[8, 8, -1, 8, -1, 8, 8]],
        name="target_red",
        tags=["target", "red"],
        collidable=False,
        layer=0,
    ),
    "target_yellow": Sprite(
        pixels=[[11, 11, -1, 11, -1, 11, 11]],
        name="target_yellow",
        tags=["target", "yellow"],
        collidable=False,
        layer=0,
    ),
    "trolley": Sprite(
        pixels=[
            [3, 3, 3, 3, 3],
            [3, 14, 14, 14, 3],
            [3, 15, 15, 15, 3],
            [-1, -1, 4, -1, -1],
        ],
        name="trolley",
        tags=["trolley"],
        collidable=False,
        layer=4,
    ),
    "wall": Sprite(
        pixels=_WALL_PIXELS,
        name="wall",
        tags=["wall"],
        layer=2,
    ),
}

# ---------------------------------------------------------------------
# 2. LEVELS  (3 entries)
# ---------------------------------------------------------------------
levels = [
    Level(
        sprites=[
            sprites["beam"].clone().set_position(0, 3),
            sprites["floor"].clone().set_position(0, 58),
            sprites["target_red"].clone().set_position(43, 57),
            sprites["block_red"].clone().set_position(14, 53),
            sprites["trolley"].clone().set_position(0, 4),
            sprites["hook"].clone().set_position(0, 8),
            sprites["rope"].clone().set_position(2, 8),
        ],
        grid_size=(64, 64),
        data={"step_budget": 150},
    ),
    Level(
        sprites=[
            sprites["beam"].clone().set_position(0, 3),
            sprites["floor"].clone().set_position(0, 58),
            sprites["wall"].clone().set_position(30, 20),
            sprites["target_red"].clone().set_position(43, 57),
            sprites["target_blue"].clone().set_position(57, 57),
            sprites["block_red"].clone().set_position(4, 53),
            sprites["block_blue"].clone().set_position(52, 53),
            sprites["trolley"].clone().set_position(0, 4),
            sprites["hook"].clone().set_position(0, 8),
            sprites["rope"].clone().set_position(2, 8),
        ],
        grid_size=(64, 64),
        data={"step_budget": 250},
    ),
    Level(
        sprites=[
            sprites["beam"].clone().set_position(0, 3),
            sprites["floor"].clone().set_position(0, 58),
            sprites["wall"].clone().set_position(30, 20),
            sprites["target_yellow"].clone().set_position(43, 57),
            sprites["target_blue"].clone().set_position(23, 57),
            sprites["target_red"].clone().set_position(57, 57),
            sprites["block_red"].clone().set_position(4, 53),
            sprites["block_blue"].clone().set_position(4, 48),
            sprites["block_yellow"].clone().set_position(4, 43),
            sprites["trolley"].clone().set_position(0, 4),
            sprites["hook"].clone().set_position(0, 8),
            sprites["rope"].clone().set_position(2, 8),
        ],
        grid_size=(64, 64),
        data={"step_budget": 500},
    ),
]

# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 10
PADDING_COLOR = 10
FLOOR_Y = 58
TROLLEY_Y = 4
TROLLEY_HEIGHT = 4

# Hook visual states. Open jaws = no cargo (gap between the claw arms);
# closed jaws = cargo gripped (gap filled with claw colour).
HOOK_PIXELS_OPEN = [
    [-1, -1, 4, -1, -1],
    [3, 3, 3, 3, 3],
    [3, 4, -1, 4, 3],
    [3, 4, -1, 4, 3],
]
HOOK_PIXELS_CLOSED = [
    [-1, -1, 4, -1, -1],
    [3, 3, 3, 3, 3],
    [3, 4, 11, 4, 3],
    [3, 4, 11, 4, 3],
]


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, budget: int) -> None:
        self.budget = budget
        self.current = budget

    def set_budget(self, budget: int) -> None:
        self.budget = budget
        self.current = budget

    def set_current(self, current: int) -> None:
        self.current = max(0, min(current, self.budget))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.budget <= 0:
            return frame
        bar_width = 32
        x_offset = (64 - bar_width) // 2
        ratio = self.current / self.budget
        filled = round(bar_width * ratio)
        filled = max(0, min(filled, bar_width))
        empty = bar_width - filled
        for x in range(bar_width):
            if x < empty:
                frame[63, x_offset + x] = 0
            else:
                frame[63, x_offset + x] = 4
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Hk7v(NovaBaseGame):
    def __init__(self) -> None:
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
        )
        self._step_counter_ui = StepCounterHud(150)
        camera.replace_interface([self._step_counter_ui])
        self.trolley = None
        self.hook = None
        self.rope = None
        self.carrying = None
        self.walls = []
        self.blocks = []
        self.targets = []
        super().__init__(
            game_id="hk7v",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    # -----------------------------------------------------------------
    # LEVEL SETUP
    # -----------------------------------------------------------------
    def on_set_level(self, level: Level) -> None:
        all_sprites = level.get_sprites()
        self.trolley = next(s for s in all_sprites if "trolley" in (s.tags or []))
        self.hook = next(s for s in all_sprites if "hook" in (s.tags or []))
        self.rope = next(s for s in all_sprites if "rope" in (s.tags or []))
        self.walls = [s for s in all_sprites if "wall" in (s.tags or [])]
        self.blocks = [s for s in all_sprites if "block" in (s.tags or [])]
        self.targets = [s for s in all_sprites if "target" in (s.tags or [])]
        self.carrying = None
        self._set_hook_visual(closed=False)
        budget = level.get_data("step_budget") or 150
        self._step_counter_ui.set_budget(budget)
        self._update_rope()

    # -----------------------------------------------------------------
    # STEP
    # -----------------------------------------------------------------
    def step(self) -> None:
        budget = self._step_counter_ui.budget
        self._step_counter_ui.set_current(budget - self._action_count)
        if self._action_count >= budget:
            self.lose()
            self.complete_action()
            return
        if self.action.id == GameAction.ACTION1:
            self._raise_hook()
        elif self.action.id == GameAction.ACTION2:
            self._lower_hook()
        elif self.action.id == GameAction.ACTION3:
            self._move_trolley(-1)
        elif self.action.id == GameAction.ACTION4:
            self._move_trolley(+1)
        elif self.action.id == GameAction.ACTION5:
            self._toggle_grab()
        self._update_rope()
        if self._check_win():
            self.next_level()
        self.complete_action()

    # -----------------------------------------------------------------
    # MOVEMENT HELPERS
    # -----------------------------------------------------------------
    def _raise_hook(self) -> None:
        new_y = self.hook.y - 1
        if new_y < self.trolley.y + self.trolley.height:
            return
        if self._cells_blocked(self.hook.x, new_y, self.hook.width, self.hook.height,
                               exclude={self.carrying} if self.carrying else set()):
            return
        if self.carrying is not None:
            new_block_y = self.carrying.y - 1
            if self._cells_blocked(self.carrying.x, new_block_y,
                                   self.carrying.width, self.carrying.height,
                                   exclude={self.carrying, self.hook}):
                return
            self.carrying.set_position(self.carrying.x, new_block_y)
        self.hook.set_position(self.hook.x, new_y)

    def _lower_hook(self) -> None:
        new_y = self.hook.y + 1
        if new_y + self.hook.height > FLOOR_Y:
            return
        if self._cells_blocked(self.hook.x, new_y, self.hook.width, self.hook.height,
                               exclude={self.carrying} if self.carrying else set()):
            return
        if self.carrying is not None:
            new_block_y = self.carrying.y + 1
            if new_block_y + self.carrying.height > FLOOR_Y:
                return
            if self._cells_blocked(self.carrying.x, new_block_y,
                                   self.carrying.width, self.carrying.height,
                                   exclude={self.carrying, self.hook}):
                return
            self.carrying.set_position(self.carrying.x, new_block_y)
        self.hook.set_position(self.hook.x, new_y)

    def _move_trolley(self, dx: int) -> None:
        new_x = self.trolley.x + dx
        if new_x < 0 or new_x + self.trolley.width > 64:
            return
        new_rope_x = new_x + 2
        rope_top = self.trolley.y + self.trolley.height
        rope_bottom = self.hook.y - 1
        if rope_bottom >= rope_top:
            for y in range(rope_top, rope_bottom + 1):
                if self._wall_at_cell(new_rope_x, y):
                    return
        if self._cells_blocked(new_x, self.hook.y, self.hook.width, self.hook.height,
                               exclude={self.carrying} if self.carrying else set()):
            return
        if self.carrying is not None:
            if self._cells_blocked(new_x, self.carrying.y,
                                   self.carrying.width, self.carrying.height,
                                   exclude={self.carrying, self.hook}):
                return
            self.carrying.set_position(new_x, self.carrying.y)
        self.trolley.set_position(new_x, self.trolley.y)
        self.hook.set_position(new_x, self.hook.y)

    def _toggle_grab(self) -> None:
        if self.carrying is not None:
            block = self.carrying
            self.carrying = None
            self._set_hook_visual(closed=False)
            self._fall(block)
        else:
            target_y = self.hook.y + self.hook.height
            for block in self.blocks:
                if block.x == self.hook.x and block.y == target_y:
                    self.carrying = block
                    self._set_hook_visual(closed=True)
                    return

    def _set_hook_visual(self, closed: bool) -> None:
        pixels = HOOK_PIXELS_CLOSED if closed else HOOK_PIXELS_OPEN
        self.hook.pixels = np.array(pixels, dtype=np.int16)

    def _fall(self, block) -> None:
        while block.y + block.height < FLOOR_Y:
            new_y = block.y + 1
            if new_y + block.height > FLOOR_Y:
                break
            if self._cells_blocked(block.x, new_y, block.width, block.height,
                                   exclude={block, self.hook}):
                break
            block.set_position(block.x, new_y)

    # -----------------------------------------------------------------
    # GEOMETRY
    # -----------------------------------------------------------------
    def _cells_blocked(self, x: int, y: int, w: int, h: int, exclude) -> bool:
        for sprite in self.walls + self.blocks:
            if sprite in exclude:
                continue
            if self._rect_overlap(x, y, w, h,
                                  sprite.x, sprite.y, sprite.width, sprite.height):
                return True
        return False

    @staticmethod
    def _rect_overlap(ax, ay, aw, ah, bx, by, bw, bh) -> bool:
        if ax + aw <= bx or bx + bw <= ax:
            return False
        if ay + ah <= by or by + bh <= ay:
            return False
        return True

    def _wall_at_cell(self, x: int, y: int) -> bool:
        for wall in self.walls:
            if wall.x <= x < wall.x + wall.width and wall.y <= y < wall.y + wall.height:
                return True
        return False

    # -----------------------------------------------------------------
    # ROPE RENDERING
    # -----------------------------------------------------------------
    def _update_rope(self) -> None:
        if self.rope is None or self.trolley is None or self.hook is None:
            return
        rope_length = self.hook.y - (self.trolley.y + self.trolley.height)
        if rope_length <= 0:
            self.rope.set_interaction(InteractionMode.REMOVED)
        else:
            self.rope.pixels = np.full((rope_length, 1), 4, dtype=np.int16)
            self.rope.set_position(self.trolley.x + 2,
                                   self.trolley.y + self.trolley.height)
            self.rope.set_interaction(InteractionMode.TANGIBLE)

    # -----------------------------------------------------------------
    # WIN
    # -----------------------------------------------------------------
    def _check_win(self) -> bool:
        for target in self.targets:
            tags = target.tags or []
            color_tag = next((t for t in tags if t != "target"), None)
            if color_tag is None:
                continue
            same_color_block = next(
                (b for b in self.blocks if color_tag in (b.tags or [])), None
            )
            if same_color_block is None:
                return False
            if same_color_block.x != target.x + 1:
                return False
            if same_color_block.y != FLOOR_Y - same_color_block.height:
                return False
        return True

    # -----------------------------------------------------------------
    # OPTIONAL DEBUG STATE
    # -----------------------------------------------------------------
    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._step_counter_ui.current
        state[0, 1] = 1 if self.carrying is not None else 0
        if self.trolley is not None:
            state[1, 0] = self.trolley.x
        if self.hook is not None:
            state[1, 1] = self.hook.y
        return state
