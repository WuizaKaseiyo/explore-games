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

sprites = {
    "wax_sprite": Sprite(
        pixels=[
            [12],
        ],
        name="wax_sprite",
        visible=True,
        collidable=False,
        tags=["wax_pickup"],
    ),
    "lantern_sprite": Sprite(
        pixels=[
            [11],
        ],
        name="lantern_sprite",
        visible=True,
        collidable=False,
        tags=["lantern"],
        layer=2,
    ),
    "filter_yellow_sprite": Sprite(
        pixels=[
            [11],
        ],
        name="filter_yellow_sprite",
        visible=True,
        collidable=False,
        tags=["filter", "filter_yellow"],
    ),
    "filter_red_sprite": Sprite(
        pixels=[
            [8],
        ],
        name="filter_red_sprite",
        visible=True,
        collidable=False,
        tags=["filter", "filter_red"],
    ),
    "target_yellow_sprite": Sprite(
        pixels=[
            [1, 1, 1],
            [1, -1, 1],
            [1, 1, 1],
        ],
        name="target_yellow_sprite",
        visible=True,
        collidable=True,
        blocking=BlockingMode.BOUNDING_BOX,
        tags=["target", "target_yellow"],
        layer=1,
    ),
    "target_yellow_thick_sprite": Sprite(
        pixels=[
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ],
        name="target_yellow_thick_sprite",
        visible=True,
        collidable=True,
        blocking=BlockingMode.BOUNDING_BOX,
        tags=["target", "target_yellow"],
        layer=1,
    ),
    "target_red_sprite": Sprite(
        pixels=[
            [8, 8, 8],
            [8, -1, 8],
            [8, 8, 8],
        ],
        name="target_red_sprite",
        visible=True,
        collidable=False,
        tags=["target", "target_red"],
        layer=1,
    ),
}

levels = [
    # Level 1
    Level(
        sprites=[
            sprites["lantern_sprite"].clone().set_position(3, 3),
            sprites["target_yellow_sprite"].clone().set_position(2, 7),
            sprites["target_yellow_sprite"].clone().set_position(7, 5),
        ],
        grid_size=(12, 12),
        data={
            "step_budget": 20,
            "initial_facing": 0,
            "initial_range": 4,
        },
    ),
    # Level 2
    Level(
        sprites=[
            sprites["lantern_sprite"].clone().set_position(3, 7),
            sprites["wax_sprite"].clone().set_position(10, 7),
            sprites["target_yellow_thick_sprite"].clone().set_position(2, 0),
            sprites["target_yellow_thick_sprite"].clone().set_position(2, 9),
        ],
        grid_size=(14, 14),
        data={
            "step_budget": 29,
            "initial_facing": 0,
            "initial_range": 2,
        },
    ),
    # Level 3
    Level(
        sprites=[
            sprites["lantern_sprite"].clone().set_position(2, 2),
            sprites["wax_sprite"].clone().set_position(10, 7),
            sprites["filter_red_sprite"].clone().set_position(2, 8),
            sprites["target_yellow_sprite"].clone().set_position(7, 1),
            sprites["target_red_sprite"].clone().set_position(1, 10),
        ],
        grid_size=(14, 14),
        data={
            "step_budget": 36,
            "initial_facing": 1,
            "initial_range": 1,
        },
    ),
]

BACKGROUND_COLOR = 5
PADDING_COLOR = 4
WAX_BONUS = 2
LIT_FROM_YELLOW = 1  # light grey (cone illumination from a yellow lantern)
LIT_FROM_RED = 13    # maroon (cone illumination from a red lantern)


class StepCounterHud(RenderableUserDisplay):
    """."""

    def __init__(self, budget: int = 0):
        self._budget = budget
        self._current = budget

    def set_budget(self, budget: int) -> None:
        self._budget = budget
        self._current = budget

    def set_steps(self, current: int) -> None:
        self._current = max(0, min(current, self._budget))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self._budget == 0:
            return frame
        ratio = self._current / self._budget
        filled = round(64 * ratio)
        for x in range(64):
            if x < filled:
                frame[63, x] = 1
            else:
                frame[63, x] = 3
        return frame


class ConeOverlay(RenderableUserDisplay):
    """."""

    def __init__(self):
        self.lx = 0
        self.ly = 0
        self.facing = 0
        self.cone_range = 0
        self.cone_color = 11
        self.grid_w = 12
        self.grid_h = 12
        self.bg = BACKGROUND_COLOR
        self.active = False

    def configure(
        self,
        lx: int,
        ly: int,
        facing: int,
        cone_range: int,
        cone_color: int,
        grid_w: int,
        grid_h: int,
        bg: int,
    ) -> None:
        self.lx = lx
        self.ly = ly
        self.facing = facing
        self.cone_range = cone_range
        self.cone_color = cone_color
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.bg = bg
        self.active = True

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if not self.active:
            return frame
        scale_x = 64 // max(1, self.grid_w)
        scale_y = 64 // max(1, self.grid_h)
        scale = max(1, min(scale_x, scale_y))
        scaled_w = self.grid_w * scale
        scaled_h = self.grid_h * scale
        x_offset = (64 - scaled_w) // 2
        y_offset = (64 - scaled_h) // 2

        if self.cone_color == 8:
            lit = LIT_FROM_RED
        else:
            lit = LIT_FROM_YELLOW

        cells = _cone_cells(
            self.lx, self.ly, self.facing, self.cone_range, self.grid_w, self.grid_h
        )
        for gx, gy in cells:
            px0 = x_offset + gx * scale
            py0 = y_offset + gy * scale
            for dy in range(scale):
                for dx in range(scale):
                    py = py0 + dy
                    px = px0 + dx
                    if 0 <= py < 64 and 0 <= px < 64:
                        if frame[py, px] == self.bg:
                            frame[py, px] = lit
        return frame


class FlameRidge(RenderableUserDisplay):
    """Three thin red striations painted at the lantern's cell edge
    in the facing direction. Sub-cell resolution (works at the pixel
    level, like the cone overlay) — gives the lantern a directional
    "flame ridge" without enlarging its grid footprint."""

    def __init__(self):
        self.lx = 0
        self.ly = 0
        self.facing = 0
        self.grid_w = 12
        self.grid_h = 12
        self.active = False

    def configure(
        self, lx: int, ly: int, facing: int, grid_w: int, grid_h: int
    ) -> None:
        self.lx = lx
        self.ly = ly
        self.facing = facing
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.active = True

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if not self.active:
            return frame
        scale_x = 64 // max(1, self.grid_w)
        scale_y = 64 // max(1, self.grid_h)
        scale = max(1, min(scale_x, scale_y))
        if scale < 3:
            return frame  # not enough pixels for three striations
        scaled_w = self.grid_w * scale
        scaled_h = self.grid_h * scale
        x_offset = (64 - scaled_w) // 2
        y_offset = (64 - scaled_h) // 2

        cell_left = x_offset + self.lx * scale
        cell_top = y_offset + self.ly * scale
        cell_right = cell_left + scale
        cell_bottom = cell_top + scale

        # A single yellow ridge centred on the lantern's edge in the
        # facing direction. Width along the cell's perpendicular axis
        # = scale - 2, so there is exactly 1-pixel margin on each
        # side (symmetric on every grid scale: 3 wide on a 5-pixel
        # cell, 2 wide on a 4-pixel cell, 1 wide on a 3-pixel cell).
        # Length along the facing axis = 2 pixels (1 in the lantern
        # cell, 1 in the adjacent cell — straddles the boundary).
        yellow = 11
        ridge_w = scale - 2  # >=1 because we early-returned for scale<3
        perp_start_x = cell_left + 1
        perp_start_y = cell_top + 1

        if self.facing == 0:    # N — top edge
            for dx in range(ridge_w):
                for dy in (-1, 0):
                    py = cell_top + dy
                    px = perp_start_x + dx
                    if 0 <= py < 64 and 0 <= px < 64:
                        frame[py, px] = yellow
        elif self.facing == 1:  # E — right edge
            for dy in range(ridge_w):
                for dx in (-1, 0):
                    py = perp_start_y + dy
                    px = cell_right + dx
                    if 0 <= py < 64 and 0 <= px < 64:
                        frame[py, px] = yellow
        elif self.facing == 2:  # S — bottom edge
            for dx in range(ridge_w):
                for dy in (-1, 0):
                    py = cell_bottom + dy
                    px = perp_start_x + dx
                    if 0 <= py < 64 and 0 <= px < 64:
                        frame[py, px] = yellow
        else:                   # W — left edge
            for dy in range(ridge_w):
                for dx in (-1, 0):
                    py = perp_start_y + dy
                    px = cell_left + dx
                    if 0 <= py < 64 and 0 <= px < 64:
                        frame[py, px] = yellow
        return frame


def _cone_cells(lx: int, ly: int, facing: int, cone_range: int, gw: int, gh: int):
    """Yield (x, y) grid cells inside the cone, clipped to grid."""
    if facing == 0:
        xs = range(lx - 1, lx + 2)
        ys = range(ly - cone_range, ly)
    elif facing == 1:
        xs = range(lx + 1, lx + 1 + cone_range)
        ys = range(ly - 1, ly + 2)
    elif facing == 2:
        xs = range(lx - 1, lx + 2)
        ys = range(ly + 1, ly + 1 + cone_range)
    else:
        xs = range(lx - cone_range, lx)
        ys = range(ly - 1, ly + 2)
    out = []
    for x in xs:
        for y in ys:
            if 0 <= x < gw and 0 <= y < gh:
                out.append((x, y))
    return out


class Lq5x(NovaBaseGame):
    def __init__(self) -> None:
        self.lantern: Sprite | None = None
        self.facing: int = 0
        self.cone_range: int = 2
        self.cone_color: int = 11
        self.step_budget: int = 0
        self._steps_used: int = 0
        self.lit_targets: set[int] = set()
        self._step_hud = StepCounterHud(0)
        self._cone_overlay = ConeOverlay()
        self._flame_ridge = FlameRidge()
        # Order matters: cone paints lit-cells first, then flame-ridge
        # paints red striations on top (so they're visible even where
        # they overlap cone-painted pixels), then step_hud paints the
        # bottom-row energy bar last.
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._cone_overlay, self._flame_ridge, self._step_hud],
        )
        super().__init__(
            game_id="lq5x",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (12, 12)
        self.camera.width = gw
        self.camera.height = gh

        self.lit_targets = set()
        facing_data = level.get_data("initial_facing")
        self.facing = facing_data if facing_data is not None else 0
        range_data = level.get_data("initial_range")
        self.cone_range = range_data if range_data is not None else 2
        self.cone_color = 11
        budget_data = level.get_data("step_budget")
        self.step_budget = budget_data if budget_data is not None else 30
        self._steps_used = 0
        self._step_hud.set_budget(self.step_budget)

        lanterns = level.get_sprites_by_tag("lantern")
        self.lantern = lanterns[0] if lanterns else None

        self._update_overlay()
        self._scan_filter_and_targets()

    def _grid(self) -> tuple[int, int]:
        if self.current_level is None or self.current_level.grid_size is None:
            return (12, 12)
        return self.current_level.grid_size

    def _update_overlay(self) -> None:
        if self.lantern is None:
            return
        gw, gh = self._grid()
        self._cone_overlay.configure(
            self.lantern.x,
            self.lantern.y,
            self.facing,
            self.cone_range,
            self.cone_color,
            gw,
            gh,
            BACKGROUND_COLOR,
        )
        self._flame_ridge.configure(
            self.lantern.x,
            self.lantern.y,
            self.facing,
            gw,
            gh,
        )

    def _scan_filter_and_targets(self) -> None:
        if self.lantern is None or self.current_level is None:
            return
        gw, gh = self._grid()
        cone_cells = set(
            _cone_cells(
                self.lantern.x,
                self.lantern.y,
                self.facing,
                self.cone_range,
                gw,
                gh,
            )
        )

        filters = self.current_level.get_sprites_by_tag("filter")
        candidates = []
        for f in filters:
            if f.interaction == InteractionMode.REMOVED:
                continue
            if (f.x, f.y) in cone_cells:
                candidates.append(f)
        if candidates:
            def _key(s: Sprite) -> tuple[int, int]:
                return (
                    abs(s.x - self.lantern.x) + abs(s.y - self.lantern.y),
                    filters.index(s),
                )

            candidates.sort(key=_key)
            chosen = candidates[0]
            if "filter_red" in chosen.tags:
                self.cone_color = 8
            elif "filter_yellow" in chosen.tags:
                self.cone_color = 11
            self._update_overlay()

        targets = self.current_level.get_sprites_by_tag("target")
        for t in targets:
            cx = t.x + t.width // 2
            cy = t.y + t.height // 2
            if (cx, cy) not in cone_cells:
                continue
            target_color = None
            if "target_yellow" in t.tags:
                target_color = 11
            elif "target_red" in t.tags:
                target_color = 8
            if target_color is None:
                continue
            if self.cone_color == target_color:
                if id(t) not in self.lit_targets:
                    fill = 1 if "target_yellow" in t.tags else 8
                    t.pixels[t.height // 2, t.width // 2] = fill
                self.lit_targets.add(id(t))

    def _is_won(self) -> bool:
        if self.current_level is None:
            return False
        targets = self.current_level.get_sprites_by_tag("target")
        if not targets:
            return False
        return all(id(t) in self.lit_targets for t in targets)

    def _blocked(self, x: int, y: int) -> bool:
        if self.current_level is None:
            return False
        for s in self.current_level.get_sprites():
            if not s.is_collidable or s.interaction == InteractionMode.REMOVED:
                continue
            if s.blocking == BlockingMode.BOUNDING_BOX:
                if s.x <= x < s.x + s.width and s.y <= y < s.y + s.height:
                    return True
        return False

    def _consume_pickup_at_lantern(self) -> None:
        if self.lantern is None or self.current_level is None:
            return
        for p in self.current_level.get_sprites_by_tag("wax_pickup"):
            if p.interaction == InteractionMode.REMOVED:
                continue
            if p.x == self.lantern.x and p.y == self.lantern.y:
                p.set_interaction(InteractionMode.REMOVED)
                self.cone_range += WAX_BONUS

    def step(self) -> None:
        if self.lantern is None:
            self.complete_action()
            return

        gw, gh = self._grid()
        aid = self.action.id
        consumed_step = False
        if aid in (
            GameAction.ACTION1,
            GameAction.ACTION2,
            GameAction.ACTION3,
            GameAction.ACTION4,
        ):
            dx, dy = 0, 0
            if aid == GameAction.ACTION1:
                dy = -1
            elif aid == GameAction.ACTION2:
                dy = 1
            elif aid == GameAction.ACTION3:
                dx = -1
            elif aid == GameAction.ACTION4:
                dx = 1
            new_x = self.lantern.x + dx
            new_y = self.lantern.y + dy
            if 0 <= new_x < gw and 0 <= new_y < gh and not self._blocked(new_x, new_y):
                self.lantern.move(dx, dy)
                self._consume_pickup_at_lantern()
            consumed_step = True
        elif aid == GameAction.ACTION5:
            self.facing = (self.facing + 1) % 4
            consumed_step = True

        if consumed_step:
            self._steps_used += 1

        self._update_overlay()
        self._scan_filter_and_targets()
        self._step_hud.set_steps(max(0, self.step_budget - self._steps_used))
        if self._is_won():
            self.complete_action()
            self.next_level()
            return
        if self._steps_used >= self.step_budget:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((4, 4), dtype=np.int16)
        if self.lantern is not None:
            out[0, 0] = self.lantern.x
            out[0, 1] = self.lantern.y
        out[0, 2] = self.facing
        out[0, 3] = self.cone_range
        out[1, 0] = self.cone_color
        out[1, 1] = self.step_budget - self._steps_used
        out[1, 2] = len(self.lit_targets)
        return out

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()
