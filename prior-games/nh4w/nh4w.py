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
# Sprite bank
# ---------------------------------------------------------------------

def _make_floor() -> Sprite:
    rows = []
    rows.append([3] * 64)
    for _ in range(5):
        row = []
        for x in range(64):
            row.append(4 if x % 3 == 2 else 5)
        rows.append(row)
    for _ in range(7):
        rows.append([4] * 64)
    return Sprite(
        pixels=rows,
        name="floor",
        visible=True,
        collidable=False,
        tags=["floor"],
        layer=0,
    )


def _make_brick_wall(height: int) -> Sprite:
    rows = []
    pattern_a = [12, 8, 8, 12, 8, 8]
    pattern_b = [8, 8, 12, 8, 8, 12]
    for r in range(height):
        if r == 0 or r == height - 1 or r % 4 == 3:
            rows.append([12, 12, 12, 12, 12, 12])
        elif (r // 4) % 2 == 0:
            rows.append(pattern_a)
        else:
            rows.append(pattern_b)
    return Sprite(
        pixels=rows,
        name=f"wall_h{height}",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=1,
    )


def _make_stalactite(clearance: int) -> Sprite:
    height = 50 - clearance
    if height < 5:
        height = 5
    rows = []
    trunk = height - 5
    for _ in range(trunk):
        rows.append([3, 3, 3, 3, 3, 3, 3, 3])
    rows.append([3, 3, 3, 3, 3, 3, 3, 3])
    rows.append([-1, 3, 3, 3, 3, 3, 3, -1])
    rows.append([-1, 3, 3, 3, 3, 3, 3, -1])
    rows.append([-1, 13, 3, 3, 3, 3, 13, -1])
    rows.append([-1, 13, 13, 13, 13, 13, 13, -1])
    return Sprite(
        pixels=rows,
        name=f"ceiling_c{clearance}",
        visible=True,
        collidable=True,
        tags=["ceiling"],
        layer=1,
    )


def _make_target(palette: int, kind: str) -> Sprite:
    return Sprite(
        pixels=[
            [palette, palette, palette, palette],
            [palette, 4, 4, palette],
            [palette, 4, 4, palette],
            [palette, palette, palette, palette],
        ],
        name=f"target_{kind}",
        visible=True,
        collidable=False,
        tags=["target", kind],
        layer=0,
    )


sprites = {
    "floor": _make_floor(),
    "launcher": Sprite(
        pixels=[
            [-1, -1, 11, -1, -1],
            [-1, 11, 11, 11, -1],
            [9, 9, 9, 9, 9],
            [9, 3, 9, 3, 9],
            [5, 3, 3, 3, 5],
        ],
        name="launcher",
        visible=True,
        collidable=True,
        tags=["launcher"],
        layer=2,
    ),
    "projectile": Sprite(
        pixels=[
            [-1, 11, -1],
            [11, 11, 11],
            [-1, 11, -1],
        ],
        name="projectile",
        visible=True,
        collidable=False,
        tags=["projectile"],
        layer=5,
    ),
    "wall_h8": _make_brick_wall(8),
    "ceiling_c6": _make_stalactite(6),
    "ceiling_c13": _make_stalactite(13),
    "target_yellow": _make_target(11, "yellow"),
    "target_blue": _make_target(9, "blue"),
}


# ---------------------------------------------------------------------
# Levels
# ---------------------------------------------------------------------

levels = [
    Level(
        sprites=[
            sprites["floor"].clone().set_position(0, 51),
            sprites["launcher"].clone().set_position(4, 46),
            sprites["target_yellow"].clone().set_position(56, 51),
        ],
        grid_size=(64, 64),
        data={"step_budget": 15},
    ),
    Level(
        sprites=[
            sprites["floor"].clone().set_position(0, 51),
            sprites["launcher"].clone().set_position(4, 46),
            sprites["wall_h8"].clone().set_position(24, 43),
            sprites["target_yellow"].clone().set_position(60, 51),
        ],
        grid_size=(64, 64),
        data={"step_budget": 25},
    ),
    Level(
        sprites=[
            sprites["floor"].clone().set_position(0, 51),
            sprites["launcher"].clone().set_position(4, 46),
            sprites["wall_h8"].clone().set_position(24, 43),
            sprites["ceiling_c6"].clone().set_position(8, 0),
            sprites["ceiling_c13"].clone().set_position(32, 0),
            sprites["target_yellow"].clone().set_position(40, 51),
            sprites["target_blue"].clone().set_position(52, 51),
        ],
        grid_size=(64, 64),
        data={"step_budget": 35},
    ),
]


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 10
PADDING_COLOR = 4
WALK_STEP = 4
MAX_RANGE = 48
LAUNCH_ORIGIN_DY = 50  # y of the launch origin (one above floor surface 51)
FRAME_STEP = 2  # projectile advances this many px per animation frame
HUD_FILL = 14
HUD_EMPTY = 8


# ---------------------------------------------------------------------
# HUD widget
# ---------------------------------------------------------------------

class StepBarHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0):
        self.max_steps = max_steps
        self.remaining = max_steps

    def set_max(self, n: int) -> None:
        self.max_steps = n
        self.remaining = n

    def set_remaining(self, n: int) -> None:
        self.remaining = max(0, min(n, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        filled = round(64 * (self.remaining / self.max_steps))
        for x in range(64):
            frame[0, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


# ---------------------------------------------------------------------
# Game class
# ---------------------------------------------------------------------

class Nh4w(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_ui = StepBarHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        super().__init__(
            game_id="nh4w",
            levels=levels,
            camera=camera,
            available_actions=[3, 4, 6],
        )

    # -----------------------------------------------------------------
    # Per-level setup
    # -----------------------------------------------------------------

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        budget = level.get_data("step_budget") or 30
        self._step_max = budget
        self._step_remaining = budget
        self._step_counter_ui.set_max(budget)
        self._step_counter_ui.set_remaining(budget)

        self.launcher = level.get_sprites_by_tag("launcher")[0]
        self.walls = list(level.get_sprites_by_tag("wall"))
        self.ceilings = list(level.get_sprites_by_tag("ceiling"))
        self.targets = list(level.get_sprites_by_tag("target"))

        self.projectile = None
        self.flight_phase = -1
        self.flight_path = []
        self.flight_target_sprite = None
        self.flight_collision_index = None

    # -----------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------

    def _launcher_blocked(self, new_x: int) -> bool:
        if new_x < 0 or new_x + self.launcher.width > 64:
            return True
        proposed_x_range = (new_x, new_x + self.launcher.width - 1)
        proposed_y_range = (self.launcher.y, self.launcher.y + self.launcher.height - 1)
        for wall in self.walls:
            wall_x_range = (wall.x, wall.x + wall.width - 1)
            wall_y_range = (wall.y, wall.y + wall.height - 1)
            if (
                proposed_x_range[0] <= wall_x_range[1]
                and proposed_x_range[1] >= wall_x_range[0]
                and proposed_y_range[0] <= wall_y_range[1]
                and proposed_y_range[1] >= wall_y_range[0]
            ):
                return True
        return False

    def _walk(self, dx: int) -> None:
        new_x = self.launcher.x + dx
        if not self._launcher_blocked(new_x):
            self.launcher.set_position(new_x, self.launcher.y)

    def _bbox_overlaps(self, ax0, ay0, ax1, ay1, bx0, by0, bx1, by1) -> bool:
        return ax0 <= bx1 and ax1 >= bx0 and ay0 <= by1 and ay1 >= by0

    def _frame_collides(self, cx: int, cy: int) -> bool:
        proj_pixels = sprites["projectile"].pixels
        ph, pw = proj_pixels.shape
        for ly in range(ph):
            for lx in range(pw):
                if proj_pixels[ly][lx] < 0:
                    continue
                wx = cx - 1 + lx
                wy = cy - 1 + ly
                if wx < 0 or wx > 63 or wy < 0 or wy > 63:
                    continue
                for blocker in self.walls + self.ceilings:
                    bw = blocker.width
                    bh = blocker.height
                    bx_local = wx - blocker.x
                    by_local = wy - blocker.y
                    if bx_local < 0 or bx_local >= bw:
                        continue
                    if by_local < 0 or by_local >= bh:
                        continue
                    if blocker.pixels[by_local][bx_local] >= 0:
                        return True
        return False

    def _target_at(self, cx: int, cy: int):
        proj_x0, proj_x1 = cx - 1, cx + 1
        proj_y0, proj_y1 = cy - 1, cy + 1
        for target in self.targets:
            tx0 = target.x
            ty0 = target.y
            tx1 = target.x + target.width - 1
            ty1 = target.y + target.height - 1
            if self._bbox_overlaps(proj_x0, proj_y0, proj_x1, proj_y1, tx0, ty0, tx1, ty1):
                return target
        return None

    def _begin_flight(self, click_cx: int, click_cy: int) -> None:
        origin_x = self.launcher.x + 2
        origin_y = LAUNCH_ORIGIN_DY
        if click_cx == origin_x:
            return
        direction = 1 if click_cx > origin_x else -1
        requested = abs(click_cx - origin_x)
        horizontal = min(MAX_RANGE, requested)
        if horizontal <= 0:
            return
        peak = horizontal // 3
        target_x = origin_x + direction * horizontal

        path = []
        collision_index = None
        steps = horizontal // FRAME_STEP
        for i in range(steps + 1):
            offset = i * FRAME_STEP
            x = origin_x + direction * offset
            t = offset / horizontal
            alt = int(peak * 4 * t * (1 - t))
            y = origin_y - alt
            path.append((x, y))
            if collision_index is None and i > 0 and self._frame_collides(x, y):
                collision_index = i
                break

        landing_target = None
        if collision_index is None:
            last_x, last_y = path[-1]
            landing_target = self._target_at(last_x, last_y)

        self.flight_path = path
        self.flight_phase = 0
        self.flight_collision_index = collision_index
        self.flight_target_sprite = landing_target

        self.projectile = sprites["projectile"].clone()
        self.projectile.set_position(path[0][0] - 1, path[0][1] - 1)
        self.projectile.set_layer(5)
        self.current_level.add_sprite(self.projectile)

    def _resolve_flight(self) -> None:
        if self.projectile is not None:
            self.current_level.remove_sprite(self.projectile)
            self.projectile = None
        if self.flight_collision_index is None and self.flight_target_sprite is not None:
            self.current_level.remove_sprite(self.flight_target_sprite)
            if self.flight_target_sprite in self.targets:
                self.targets.remove(self.flight_target_sprite)
        self.flight_path = []
        self.flight_phase = -1
        self.flight_target_sprite = None
        self.flight_collision_index = None

    def _consume_action(self) -> None:
        self._step_remaining -= 1
        self._step_counter_ui.set_remaining(self._step_remaining)

    # -----------------------------------------------------------------
    # Engine entry points
    # -----------------------------------------------------------------

    def step(self) -> None:
        if self.flight_phase >= 0:
            self.flight_phase += 1
            terminate = False
            if self.flight_collision_index is not None and self.flight_phase >= self.flight_collision_index + 1:
                terminate = True
            elif self.flight_phase >= len(self.flight_path):
                terminate = True
            if terminate:
                self._resolve_flight()
                self._consume_action()
                if not self.targets:
                    self.complete_action()
                    self.next_level()
                    return
                if self._step_remaining <= 0:
                    self.lose()
                self.complete_action()
                return
            cx, cy = self.flight_path[self.flight_phase]
            if self.projectile is not None:
                self.projectile.set_position(cx - 1, cy - 1)
            return

        if self.action.id == GameAction.ACTION3:
            self._walk(-WALK_STEP)
            self._consume_action()
            if self._step_remaining <= 0 and self.targets:
                self.lose()
            self.complete_action()
            return
        if self.action.id == GameAction.ACTION4:
            self._walk(WALK_STEP)
            self._consume_action()
            if self._step_remaining <= 0 and self.targets:
                self.lose()
            self.complete_action()
            return
        if self.action.id == GameAction.ACTION6:
            cx_disp = int(self.action.data.get("x", 0))
            cy_disp = int(self.action.data.get("y", 0))
            grid = self.camera.display_to_grid(cx_disp, cy_disp)
            if grid is not None:
                gx, gy = grid
                self._begin_flight(gx, gy)
                if self.flight_phase >= 0:
                    return
            self._consume_action()
            if self._step_remaining <= 0 and self.targets:
                self.lose()
            self.complete_action()
            return

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((2, 2), dtype=np.int16)
        state[0, 0] = self._step_remaining
        state[0, 1] = self.flight_phase
        state[1, 0] = self.launcher.x if self.launcher is not None else 0
        state[1, 1] = len(self.targets)
        return state

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()
