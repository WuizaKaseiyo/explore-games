"""."""

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

_WIND_PIXELS = [[10] if i % 2 == 0 else [1] for i in range(21)]


sprites = {
    "arc_dot": Sprite(
        pixels=[[15]],
        name="arc_dot",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["arc_dot"],
    ),
    "launcher_p1": Sprite(
        pixels=[
            [-1, 12, 12, 12, -1],
            [12,  3,  3,  3, 12],
            [12,  3,  3,  3, 12],
            [12, 15, 15, 15, 12],
            [-1, 12, 12, 12, -1],
        ],
        name="launcher_p1",
        visible=True,
        collidable=True,
        tags=["launcher", "launcher_p1"],
    ),
    "launcher_p2": Sprite(
        pixels=[
            [-1, 12, 12, 12, -1],
            [12,  3,  3,  3, 12],
            [12, 15, 15, 15, 12],
            [12, 15, 15, 15, 12],
            [-1, 12, 12, 12, -1],
        ],
        name="launcher_p2",
        visible=True,
        collidable=True,
        tags=["launcher", "launcher_p2"],
    ),
    "launcher_p3": Sprite(
        pixels=[
            [-1, 12, 12, 12, -1],
            [12, 15, 15, 15, 12],
            [12, 15, 15, 15, 12],
            [12, 15, 15, 15, 12],
            [-1, 12, 12, 12, -1],
        ],
        name="launcher_p3",
        visible=True,
        collidable=True,
        tags=["launcher", "launcher_p3"],
    ),
    "shield": Sprite(
        pixels=[
            [5, 5],
            [5, 5],
            [5, 5],
            [5, 5],
            [5, 5],
            [5, 5],
        ],
        name="shield",
        visible=True,
        collidable=True,
        tags=["shield", "block"],
    ),
    "target_ring": Sprite(
        pixels=[
            [7, 7, 7],
            [7, -1, 7],
            [7, 7, 7],
        ],
        name="target_ring",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target"],
    ),
    "wind_marker": Sprite(
        pixels=_WIND_PIXELS,
        name="wind_marker",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["wind"],
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS  (EXACTLY 3 entries; level 0 is the tutorial)
# ---------------------------------------------------------------------


def _l1_sprites():
    p1 = sprites["launcher_p1"].clone().set_position(2, 48)
    p2 = sprites["launcher_p2"].clone().set_position(2, 48)
    p2.set_interaction(InteractionMode.REMOVED)
    p3 = sprites["launcher_p3"].clone().set_position(2, 48)
    p3.set_interaction(InteractionMode.REMOVED)
    return [
        p1,
        p2,
        p3,
        sprites["target_ring"].clone().set_position(15, 49),
    ]


def _l2_sprites():
    p1 = sprites["launcher_p1"].clone().set_position(2, 48)
    p2 = sprites["launcher_p2"].clone().set_position(2, 48)
    p2.set_interaction(InteractionMode.REMOVED)
    p3 = sprites["launcher_p3"].clone().set_position(2, 48)
    p3.set_interaction(InteractionMode.REMOVED)
    return [
        p1,
        p2,
        p3,
        sprites["target_ring"].clone().set_position(27, 49),
        sprites["target_ring"].clone().set_position(49, 49),
    ]


def _l3_sprites():
    p1 = sprites["launcher_p1"].clone().set_position(2, 48)
    p2 = sprites["launcher_p2"].clone().set_position(2, 48)
    p2.set_interaction(InteractionMode.REMOVED)
    p3 = sprites["launcher_p3"].clone().set_position(2, 48)
    p3.set_interaction(InteractionMode.REMOVED)
    return [
        p1,
        p2,
        p3,
        sprites["shield"].clone().set_position(16, 44),
        sprites["wind_marker"].clone().set_position(36, 30),
        sprites["target_ring"].clone().set_position(49, 49),
    ]


levels = [
    Level(
        sprites=_l1_sprites(),
        grid_size=(64, 64),
        data={"step_budget": 12, "target_centres": [(16, 50)]},
    ),
    Level(
        sprites=_l2_sprites(),
        grid_size=(64, 64),
        data={"step_budget": 30, "target_centres": [(28, 50), (50, 50)]},
    ),
    Level(
        sprites=_l3_sprites(),
        grid_size=(64, 64),
        data={"step_budget": 50, "target_centres": [(50, 50)]},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 10  # light-blue sky
PADDING_COLOR = 4      # off-black
WIND_DRIFT = 1
LAUNCHER_HALF = 2      # 5×5 sprite; centre offset from top-left

# (apex, range) per power level
POWER_TABLE = {
    1: (3, 16),
    2: (8, 24),
    3: (15, 36),
}


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int):
        self.max_steps = max(1, int(max_steps))
        self.current = self.max_steps

    def set_max(self, max_steps: int) -> None:
        self.max_steps = max(1, int(max_steps))
        self.current = self.max_steps

    def set_current(self, current: int) -> None:
        self.current = max(0, min(int(current), self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        bar_width = 40
        offset = (frame.shape[1] - bar_width) // 2
        ratio = self.current / self.max_steps if self.max_steps else 0.0
        filled = int(round(bar_width * ratio))
        for x in range(bar_width):
            frame[0, offset + x] = 0 if x < filled else 4
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Cv5b(NovaBaseGame):
    def __init__(self) -> None:
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
        )
        self._step_counter_ui = StepCounterHud(max_steps=12)
        camera.replace_interface([self._step_counter_ui])
        super().__init__(
            game_id="cv5b",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )

    # ---- Per-level setup --------------------------------------------------
    def on_set_level(self, level: Level) -> None:
        self.power = 1
        self.target_centres = list(level.get_data("target_centres") or [])
        self.targets_remaining = list(level.get_sprites_by_tag("target"))
        self.shields = list(level.get_sprites_by_tag("shield"))
        self.wind_markers = list(level.get_sprites_by_tag("wind"))
        self.arc_dot_sprites = []
        budget = level.get_data("step_budget") or 30
        self._step_counter_ui.set_max(int(budget))
        self._step_counter_ui.set_current(int(budget))
        # Reset launchers: only launcher_p1 active, others removed
        for s in level.get_sprites_by_tag("launcher"):
            if s.name == "launcher_p1":
                s.set_interaction(InteractionMode.TANGIBLE)
            else:
                s.set_interaction(InteractionMode.REMOVED)

    # ---- Helpers ----------------------------------------------------------
    def _all_launchers(self) -> list[Sprite]:
        return self.current_level.get_sprites_by_tag("launcher")

    def _active_launcher(self) -> Sprite:
        name = f"launcher_p{self.power}"
        matches = self.current_level.get_sprites_by_name(name)
        if matches:
            return matches[0]
        return self._all_launchers()[0]

    def _launcher_origin(self) -> tuple[int, int]:
        active = self._active_launcher()
        return (active.x + LAUNCHER_HALF, active.y + LAUNCHER_HALF)

    def _can_walk_to(self, top_left_x: int, top_left_y: int) -> bool:
        if top_left_x < 0 or top_left_x + 4 > 63:
            return False
        if top_left_y < 0 or top_left_y + 4 > 63:
            return False
        for shield in self.shields:
            sx, sy = shield.x, shield.y
            sw = shield.pixels.shape[1]
            sh = shield.pixels.shape[0]
            if (
                top_left_x < sx + sw
                and top_left_x + 5 > sx
                and top_left_y < sy + sh
                and top_left_y + 5 > sy
            ):
                return False
        return True

    def _walk(self, dx: int, dy: int) -> None:
        active = self._active_launcher()
        nx = active.x + dx
        ny = active.y + dy
        if not self._can_walk_to(nx, ny):
            return
        for s in self._all_launchers():
            s.set_position(nx, ny)

    def _cycle_power(self) -> None:
        self.power = (self.power % 3) + 1
        for s in self._all_launchers():
            if s.name == f"launcher_p{self.power}":
                s.set_interaction(InteractionMode.TANGIBLE)
            else:
                s.set_interaction(InteractionMode.REMOVED)

    def _clear_arc_dots(self) -> None:
        for dot in self.arc_dot_sprites:
            try:
                self.current_level.remove_sprite(dot)
            except Exception:
                pass
        self.arc_dot_sprites = []

    def _compute_arc(
        self, lx: int, ly: int, cx: int, cy: int, apex: int
    ) -> list[tuple[int, int]]:
        cells: list[tuple[int, int]] = []
        last: tuple[int, int] | None = None
        n_steps = max(48, 2 * abs(cx - lx))
        if n_steps == 0:
            return [(lx, ly)]
        for i in range(n_steps + 1):
            s = i / n_steps
            x = int(round(lx + (cx - lx) * s))
            y_line = ly + (cy - ly) * s
            y_dip = apex * 4 * s * (1 - s)
            y = int(round(y_line - y_dip))
            cell = (x, y)
            if cell != last:
                cells.append(cell)
                last = cell
        return cells

    def _shield_block_index(self, cells: list[tuple[int, int]]) -> int | None:
        for idx, (x, y) in enumerate(cells):
            for shield in self.shields:
                sx, sy = shield.x, shield.y
                sw = shield.pixels.shape[1]
                sh = shield.pixels.shape[0]
                if sx <= x < sx + sw and sy <= y < sy + sh:
                    return idx
        return None

    def _wind_hit(self, cells: list[tuple[int, int]]) -> bool:
        for x, y in cells:
            for wind in self.wind_markers:
                wx, wy = wind.x, wind.y
                ww = wind.pixels.shape[1]
                wh = wind.pixels.shape[0]
                if wx <= x < wx + ww and wy <= y < wy + wh:
                    return True
        return False

    def _spawn_arc_dots(self, cells: list[tuple[int, int]]) -> None:
        active = self._active_launcher()
        lx0, ly0 = active.x, active.y
        for x, y in cells:
            if not (0 <= x < 64 and 0 <= y < 64):
                continue
            # Skip cells inside the launcher's 5×5 footprint so the trail
            # never overlays the orange cabin / purple charge bar.
            if lx0 <= x < lx0 + 5 and ly0 <= y < ly0 + 5:
                continue
            dot = sprites["arc_dot"].clone().set_position(x, y)
            self.current_level.add_sprite(dot)
            self.arc_dot_sprites.append(dot)

    def _resolve_landing(self, landing: tuple[int, int]) -> None:
        for target in list(self.targets_remaining):
            centre = (target.x + 1, target.y + 1)
            if landing == centre:
                try:
                    self.current_level.remove_sprite(target)
                except Exception:
                    pass
                self.targets_remaining.remove(target)
                break

    def _fire(self, click_x: int, click_y: int) -> None:
        if not (0 <= click_x < 64 and 0 <= click_y < 64):
            return
        lx, ly = self._launcher_origin()
        if click_x == lx and click_y == ly:
            return
        apex, max_range = POWER_TABLE[self.power]
        dx_to_click = click_x - lx
        if abs(dx_to_click) > max_range:
            # Out-of-range click: render a "fell short" trajectory that
            # arcs as far as the current charge can reach in the click's
            # direction, then stops short of the target. No hit is
            # registered. This gives the player visual feedback that the
            # shot is under-powered, instead of a silent no-op.
            direction = 1 if dx_to_click > 0 else -1
            clamp_x = lx + direction * max_range
            frac = max_range / abs(dx_to_click)
            clamp_y = ly + int(round((click_y - ly) * frac))
            short_cells = self._compute_arc(lx, ly, clamp_x, clamp_y, apex)
            block_idx = self._shield_block_index(short_cells)
            if block_idx is not None:
                short_cells = short_cells[: block_idx + 1]
            self._spawn_arc_dots(short_cells)
            return
        cells = self._compute_arc(lx, ly, click_x, click_y, apex)
        block_idx = self._shield_block_index(cells)
        if block_idx is not None:
            cells = cells[: block_idx + 1]
            self._spawn_arc_dots(cells)
            return
        if self._wind_hit(cells):
            last_x, last_y = cells[-1]
            cells[-1] = (last_x + WIND_DRIFT, last_y)
        self._spawn_arc_dots(cells)
        self._resolve_landing(cells[-1])

    # ---- Engine entry points ---------------------------------------------
    def step(self) -> None:
        self._step_counter_ui.set_current(
            self._step_counter_ui.max_steps - self._action_count
        )
        if self._action_count >= self._step_counter_ui.max_steps:
            self.lose()
            self.complete_action()
            return

        self._clear_arc_dots()

        action_id = self.action.id
        if action_id == GameAction.ACTION1:
            self._walk(0, -1)
        elif action_id == GameAction.ACTION2:
            self._walk(0, 1)
        elif action_id == GameAction.ACTION3:
            self._walk(-1, 0)
        elif action_id == GameAction.ACTION4:
            self._walk(1, 0)
        elif action_id == GameAction.ACTION5:
            self._cycle_power()
        elif action_id == GameAction.ACTION6:
            cx = int(self.action.data.get("x", 0))
            cy = int(self.action.data.get("y", 0))
            grid = self.camera.display_to_grid(cx, cy)
            if grid is not None:
                gx, gy = grid
                self._fire(gx, gy)

        if not self.targets_remaining:
            self.next_level()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.array(
            [[self.power, len(self.targets_remaining)]], dtype=np.int16
        )
