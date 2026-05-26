"""Generated game jd4q."""

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
    "avatar": Sprite(
        pixels=[
            [6, 6, 6, 6],
            [6, 7, 6, 6],
            [6, 6, 6, 6],
            [6, 6, 6, 6],
        ],
        name="avatar",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=2,
    ),
    "echo": Sprite(
        pixels=[
            [-1, 11, 11, -1],
            [11, 11, 11, 11],
            [11, 11, 11, 11],
            [-1, 11, 11, -1],
        ],
        name="echo",
        visible=True,
        collidable=False,
        tags=["echo", "sys_click"],
        layer=1,
    ),
    "echo_anchor": Sprite(
        pixels=[
            [ 8, 11, 11,  8],
            [11, 11, 11, 11],
            [11, 11, 11, 11],
            [ 8, 11, 11,  8],
        ],
        name="echo_anchor",
        visible=True,
        collidable=False,
        tags=["echo", "sys_click", "permanent_echo"],
        layer=1,
    ),
    "wall": Sprite(
        pixels=[
            [5, 5, 5, 5],
            [5, 5, 5, 5],
            [5, 5, 5, 5],
            [5, 5, 5, 5],
        ],
        name="wall",
        visible=True,
        collidable=True,
        tags=["wall"],
    ),
    "door_open": Sprite(
        pixels=[
            [3, 3, 3, 3],
            [3, 10, 10, 3],
            [3, 10, 10, 3],
            [3, 3, 3, 3],
        ],
        name="door_open",
        visible=True,
        collidable=False,
        tags=["closing_door"],
    ),
    "door_sealed": Sprite(
        pixels=[
            [3, 3, 3, 3],
            [3, 5, 5, 3],
            [3, 5, 5, 3],
            [3, 3, 3, 3],
        ],
        name="door_sealed",
        visible=True,
        collidable=True,
        tags=["wall"],
    ),
    "pickup_a": Sprite(
        pixels=[
            [-1, 14, 14, -1],
            [14,  0,  0, 14],
            [14,  0,  0, 14],
            [-1, 14, 14, -1],
        ],
        name="pickup_a",
        visible=True,
        collidable=False,
        tags=["pickup"],
    ),
    "pickup_b": Sprite(
        pixels=[
            [-1, 9, 9, -1],
            [ 9, 0, 0,  9],
            [ 9, 0, 0,  9],
            [-1, 9, 9, -1],
        ],
        name="pickup_b",
        visible=True,
        collidable=False,
        tags=["pickup"],
    ),
    "pickup_c": Sprite(
        pixels=[
            [-1, 12, 12, -1],
            [12,  0,  0, 12],
            [12,  0,  0, 12],
            [-1, 12, 12, -1],
        ],
        name="pickup_c",
        visible=True,
        collidable=False,
        tags=["pickup"],
    ),
    "goal": Sprite(
        pixels=[
            [15, 15, 15, 15],
            [15,  0,  0, 15],
            [15,  0,  0, 15],
            [15, 15, 15, 15],
        ],
        name="goal",
        visible=True,
        collidable=False,
        tags=["goal"],
    ),
    "eraser": Sprite(
        pixels=[
            [13,  6,  6, 13],
            [ 6,  6,  6,  6],
            [ 6,  6,  6,  6],
            [13,  6,  6, 13],
        ],
        name="eraser",
        visible=True,
        collidable=False,
        tags=["eraser"],
    ),
    "anchor_floor": Sprite(
        pixels=[
            [ 8,  0,  0,  8],
            [ 0,  8,  8,  0],
            [ 0,  8,  8,  0],
            [ 8,  0,  0,  8],
        ],
        name="anchor_floor",
        visible=True,
        collidable=False,
        tags=["anchor_floor"],
    ),
}


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 2
PADDING_COLOR = 5
CELL_STRIDE = 4
GRID_CELLS = 16
ECHO_LIFESPAN_DEFAULT = 12

HUD_REMAINING_COLOR = 4
HUD_SPENT_COLOR = 3


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.remaining = max_steps

    def set_max(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.remaining = max_steps

    def set_remaining(self, remaining: int) -> None:
        self.remaining = max(0, min(remaining, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        width = frame.shape[1]
        proportion = self.remaining / self.max_steps
        filled = round(width * proportion)
        filled = min(filled, width)
        for x in range(width):
            if x < filled:
                frame[0, x] = HUD_REMAINING_COLOR
            else:
                frame[0, x] = HUD_SPENT_COLOR
        return frame


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
def _cell_pixel(col: int, row: int) -> tuple[int, int]:
    return (col * CELL_STRIDE, row * CELL_STRIDE)


def _build_walls(passable_cells: set[tuple[int, int]]) -> list[Sprite]:
    walls = []
    for c in range(GRID_CELLS):
        for r in range(GRID_CELLS):
            if (c, r) in passable_cells:
                continue
            walls.append(sprites["wall"].clone().set_position(*_cell_pixel(c, r)))
    return walls


def _build_level_1() -> Level:
    """Tutorial: walk + echo-teleport + closing-doors all introduced at once
    in a tiny U-shaped layout. The player walks east into a closing-door
    corridor to the pickup; the doors seal behind. The goal is south of S,
    so the player must teleport back via clicking the visible echo at S."""
    floor_cells = {(2, 2), (3, 2), (4, 2)}                      # vestibule + east step
    floor_cells |= {(2, r) for r in range(3, 8)}                # south corridor to goal
    door_cells = {(c, 2) for c in range(5, 8)}                  # closing-door arm east
    pickup_cell = (8, 2)
    goal_cell = (2, 8)

    passable_cells = floor_cells | door_cells | {pickup_cell, goal_cell}

    door_sprites = [
        sprites["door_open"].clone().set_position(*_cell_pixel(c, r))
        for (c, r) in door_cells
    ]
    pickup_sprite = sprites["pickup_a"].clone().set_position(*_cell_pixel(*pickup_cell))
    goal_sprite = sprites["goal"].clone().set_position(*_cell_pixel(*goal_cell))
    avatar_inst = sprites["avatar"].clone().set_position(*_cell_pixel(2, 2))
    walls = _build_walls(passable_cells)

    return Level(
        sprites=walls + door_sprites + [pickup_sprite, goal_sprite, avatar_inst],
        grid_size=(64, 64),
        data={
            "step_budget": 30,
            "echoes_active": True,
            "echo_lifespan": 12,
            "required_pickups": ["pickup_a"],
        },
    )


def _build_level_2() -> Level:
    """Adds the eraser cell. The player has TWO pickups in two
    closing-door dead-end branches. The path to the goal passes through
    an eraser that wipes the entire trail; once the trail is wiped the
    only way back is to walk normally, so the eraser-branch must be
    chosen LAST after both other pickups have been collected via
    teleport-back from their dead-ends."""
    vestibule = {(2, 2), (3, 2), (2, 3), (3, 3)}
    south_leg = {(2, r) for r in range(4, 9)}
    east_leg = {(c, 8) for c in range(3, 9)}                     # ends at J=(8,8)

    branch_a_doors = {(8, r) for r in range(3, 8)}               # north of J
    pickup_a_cell = (8, 2)

    branch_b_doors = {(c, 8) for c in range(9, 13)}              # east of J
    pickup_b_cell = (13, 8)

    eraser_cell = (8, 9)
    goal_corridor = {(8, r) for r in range(10, 13)}
    goal_cell = (8, 13)

    floor_cells = vestibule | south_leg | east_leg | goal_corridor
    passable_cells = (
        floor_cells
        | branch_a_doors
        | branch_b_doors
        | {eraser_cell, pickup_a_cell, pickup_b_cell, goal_cell}
    )

    door_a_sprites = [
        sprites["door_open"].clone().set_position(*_cell_pixel(c, r))
        for (c, r) in branch_a_doors
    ]
    door_b_sprites = [
        sprites["door_open"].clone().set_position(*_cell_pixel(c, r))
        for (c, r) in branch_b_doors
    ]
    eraser_sprite = sprites["eraser"].clone().set_position(*_cell_pixel(*eraser_cell))
    pickup_a_sprite = sprites["pickup_a"].clone().set_position(*_cell_pixel(*pickup_a_cell))
    pickup_b_sprite = sprites["pickup_b"].clone().set_position(*_cell_pixel(*pickup_b_cell))
    goal_sprite = sprites["goal"].clone().set_position(*_cell_pixel(*goal_cell))
    avatar_inst = sprites["avatar"].clone().set_position(*_cell_pixel(2, 2))
    walls = _build_walls(passable_cells)

    return Level(
        sprites=(
            walls
            + door_a_sprites
            + door_b_sprites
            + [
                eraser_sprite,
                pickup_a_sprite,
                pickup_b_sprite,
                goal_sprite,
                avatar_inst,
            ]
        ),
        grid_size=(64, 64),
        data={
            "step_budget": 80,
            "echoes_active": True,
            "echo_lifespan": 12,
            "required_pickups": ["pickup_a", "pickup_b"],
        },
    )


def _build_level_3() -> Level:
    """Adds the anchor cell. The branch B corridor is long enough that
    by the time the avatar reaches its pickup, every regular echo has
    faded — the only teleport point that survives is the permanent
    echo deposited when walking over the anchor cell. The eraser is
    placed at the *entrance* to branch A, so committing to branch A
    wipes the anchor; the player who tries branch A before branch B
    finds themselves at branch A's pickup with no anchor to teleport
    back from, and branch B becomes unreachable. The witness order is
    therefore: drop anchor → branch B (using anchor for return) →
    drop anchor again → branch A (eraser wipes anchor here) → continue
    forward through branch A's tail to pickup_c then goal."""
    vestibule = {(2, 2), (3, 2), (2, 3), (3, 3)}
    east_leg_floor = {(5, 2), (6, 2), (7, 2)}
    anchor_cell = (4, 2)
    j_cell = (8, 2)

    branch_b_doors = {(c, 2) for c in range(9, 15)}              # 6 closing-doors east
    pickup_b_cell = (15, 2)

    eraser_cell = (8, 3)                                          # at branch A entrance
    branch_a_doors = {(8, r) for r in range(4, 9)}                # 5 closing-doors south
    pickup_a_cell = (8, 9)
    south_corridor = {(8, 10)}
    pickup_c_cell = (8, 11)
    goal_cell = (8, 12)

    floor_cells = vestibule | east_leg_floor | south_corridor
    passable_cells = (
        floor_cells
        | branch_a_doors
        | branch_b_doors
        | {
            anchor_cell,
            j_cell,
            eraser_cell,
            pickup_a_cell,
            pickup_b_cell,
            pickup_c_cell,
            goal_cell,
        }
    )

    door_a_sprites = [
        sprites["door_open"].clone().set_position(*_cell_pixel(c, r))
        for (c, r) in branch_a_doors
    ]
    door_b_sprites = [
        sprites["door_open"].clone().set_position(*_cell_pixel(c, r))
        for (c, r) in branch_b_doors
    ]
    anchor_sprite = sprites["anchor_floor"].clone().set_position(*_cell_pixel(*anchor_cell))
    eraser_sprite = sprites["eraser"].clone().set_position(*_cell_pixel(*eraser_cell))
    pickup_a_sprite = sprites["pickup_a"].clone().set_position(*_cell_pixel(*pickup_a_cell))
    pickup_b_sprite = sprites["pickup_b"].clone().set_position(*_cell_pixel(*pickup_b_cell))
    pickup_c_sprite = sprites["pickup_c"].clone().set_position(*_cell_pixel(*pickup_c_cell))
    goal_sprite = sprites["goal"].clone().set_position(*_cell_pixel(*goal_cell))
    avatar_inst = sprites["avatar"].clone().set_position(*_cell_pixel(2, 2))
    walls = _build_walls(passable_cells)

    return Level(
        sprites=(
            walls
            + door_a_sprites
            + door_b_sprites
            + [
                anchor_sprite,
                eraser_sprite,
                pickup_a_sprite,
                pickup_b_sprite,
                pickup_c_sprite,
                goal_sprite,
                avatar_inst,
            ]
        ),
        grid_size=(64, 64),
        data={
            "step_budget": 100,
            "echoes_active": True,
            "echo_lifespan": 6,
            "required_pickups": ["pickup_a", "pickup_b", "pickup_c"],
        },
    )


levels = [_build_level_1(), _build_level_2(), _build_level_3()]


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Jd4q(NovaBaseGame):
    def __init__(self) -> None:
        self.step_counter_ui = StepCounterHud(max_steps=30)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_counter_ui],
        )
        self.avatar: Sprite | None = None
        # Each entry: (sprite, age, cell_xy, permanent)
        self.echoes: list[tuple[Sprite, int, tuple[int, int], bool]] = []
        self.collected_pickups: set[str] = set()
        super().__init__(
            game_id="jd4q",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        budget = level.get_data("step_budget") or 0
        self.step_counter_ui.set_max(budget)

        self.echoes = []
        self.collected_pickups = set()

        players = level.get_sprites_by_tag("player")
        self.avatar = players[0] if players else None

    def step(self) -> None:
        budget = self.current_level.get_data("step_budget") or 0
        echoes_active = bool(self.current_level.get_data("echoes_active"))

        if self._action_count >= budget:
            self.lose()
            self.complete_action()
            return

        action_id = self.action.id
        if action_id in (
            GameAction.ACTION1,
            GameAction.ACTION2,
            GameAction.ACTION3,
            GameAction.ACTION4,
        ):
            self._handle_walk(action_id, echoes_active)
        elif action_id == GameAction.ACTION6 and echoes_active:
            data = self.action.data or {}
            cx = int(data.get("x", -1))
            cy = int(data.get("y", -1))
            self._handle_click(cx, cy)

        self._collect_pickup_under_avatar()

        if self._check_win():
            self.next_level()
            self.complete_action()
            return

        if echoes_active:
            self._age_and_prune_echoes()

        remaining = max(0, budget - (self._action_count + 1))
        self.step_counter_ui.set_remaining(remaining)

        self.complete_action()

    def _handle_walk(self, action_id, echoes_active: bool) -> None:
        if self.avatar is None:
            return
        deltas = {
            GameAction.ACTION1: (0, -CELL_STRIDE),
            GameAction.ACTION2: (0, CELL_STRIDE),
            GameAction.ACTION3: (-CELL_STRIDE, 0),
            GameAction.ACTION4: (CELL_STRIDE, 0),
        }
        dx, dy = deltas[action_id]
        new_x = self.avatar.x + dx
        new_y = self.avatar.y + dy
        if not self._inside_grid(new_x, new_y):
            return
        if self._cell_blocked(new_x, new_y):
            return
        prev_x, prev_y = self.avatar.x, self.avatar.y
        self.avatar.set_position(new_x, new_y)
        self._handle_egress(prev_x, prev_y, echoes_active)
        self._handle_ingress(new_x, new_y, echoes_active)

    def _inside_grid(self, x: int, y: int) -> bool:
        return 0 <= x <= 64 - CELL_STRIDE and 0 <= y <= 64 - CELL_STRIDE

    def _cell_blocked(self, x: int, y: int) -> bool:
        for wall in self.current_level.get_sprites_by_tag("wall"):
            if wall.x == x and wall.y == y:
                return True
        return False

    def _sprite_at_with_tag(self, x: int, y: int, tag: str) -> Sprite | None:
        for s in self.current_level.get_sprites_by_tag(tag):
            if s.x == x and s.y == y:
                return s
        return None

    def _handle_egress(self, prev_x: int, prev_y: int, echoes_active: bool) -> None:
        door = self._sprite_at_with_tag(prev_x, prev_y, "closing_door")
        if door is not None:
            self._seal_door(door)
            return

        if self._sprite_at_with_tag(prev_x, prev_y, "eraser") is not None:
            return

        if echoes_active:
            permanent = self._sprite_at_with_tag(prev_x, prev_y, "anchor_floor") is not None
            self._deposit_echo(prev_x, prev_y, permanent=permanent)

    def _handle_ingress(self, new_x: int, new_y: int, echoes_active: bool) -> None:
        if not echoes_active:
            return
        if self._sprite_at_with_tag(new_x, new_y, "eraser") is not None:
            self._wipe_echoes()

    def _seal_door(self, door: Sprite) -> None:
        x, y = door.x, door.y
        self.current_level.remove_sprite(door)
        sealed = sprites["door_sealed"].clone().set_position(x, y)
        self.current_level.add_sprite(sealed)

    def _wipe_echoes(self) -> None:
        for echo_sprite, _, _, _ in self.echoes:
            self.current_level.remove_sprite(echo_sprite)
        self.echoes = []

    def _deposit_echo(self, x: int, y: int, permanent: bool = False) -> None:
        for i, (sp, age, cell, perm) in enumerate(self.echoes):
            if cell == (x, y):
                self.echoes[i] = (sp, 0, cell, perm or permanent)
                return
        sprite_key = "echo_anchor" if permanent else "echo"
        echo_sprite = sprites[sprite_key].clone().set_position(x, y)
        self.current_level.add_sprite(echo_sprite)
        self.echoes.append((echo_sprite, 0, (x, y), permanent))

    def _age_and_prune_echoes(self) -> None:
        lifespan = self.current_level.get_data("echo_lifespan") or ECHO_LIFESPAN_DEFAULT
        survivors: list[tuple[Sprite, int, tuple[int, int], bool]] = []
        for echo_sprite, age, cell, permanent in self.echoes:
            if permanent:
                survivors.append((echo_sprite, age, cell, True))
                continue
            new_age = age + 1
            if new_age >= lifespan:
                self.current_level.remove_sprite(echo_sprite)
            else:
                survivors.append((echo_sprite, new_age, cell, False))
        self.echoes = survivors

    def _handle_click(self, click_x: int, click_y: int) -> None:
        if self.avatar is None:
            return
        grid = self.camera.display_to_grid(click_x, click_y)
        if grid is None:
            return
        gx, gy = grid
        cell_x = (gx // CELL_STRIDE) * CELL_STRIDE
        cell_y = (gy // CELL_STRIDE) * CELL_STRIDE
        for i, (echo_sprite, age, cell, perm) in enumerate(self.echoes):
            if cell == (cell_x, cell_y):
                self.avatar.set_position(cell_x, cell_y)
                for j in range(i, len(self.echoes)):
                    self.current_level.remove_sprite(self.echoes[j][0])
                self.echoes = self.echoes[:i]
                return

    def _collect_pickup_under_avatar(self) -> None:
        if self.avatar is None:
            return
        pickup = self._sprite_at_with_tag(self.avatar.x, self.avatar.y, "pickup")
        if pickup is None:
            return
        self.collected_pickups.add(pickup.name)
        self.current_level.remove_sprite(pickup)

    def _check_win(self) -> bool:
        if self.avatar is None:
            return False
        goal = self._sprite_at_with_tag(self.avatar.x, self.avatar.y, "goal")
        if goal is None:
            return False
        required = set(self.current_level.get_data("required_pickups") or [])
        return required.issubset(self.collected_pickups)

    def _get_hidden_state(self) -> np.ndarray:
        budget = self.current_level.get_data("step_budget") or 0
        remaining = max(0, budget - self._action_count)
        return np.array(
            [[remaining, len(self.echoes), len(self.collected_pickups)]],
            dtype=np.int16,
        )

    def _get_valid_actions(self) -> list[ActionInput]:
        actions: list[ActionInput] = [
            ActionInput(id=GameAction.ACTION1),
            ActionInput(id=GameAction.ACTION2),
            ActionInput(id=GameAction.ACTION3),
            ActionInput(id=GameAction.ACTION4),
        ]
        if bool(self.current_level.get_data("echoes_active")):
            for echo_sprite, _, (cx, cy), _ in self.echoes:
                px = cx + CELL_STRIDE // 2
                py = cy + CELL_STRIDE // 2
                actions.append(
                    ActionInput(id=GameAction.ACTION6, data={"x": px, "y": py})
                )
        return actions
