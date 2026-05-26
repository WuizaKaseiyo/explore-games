"""kj82."""

from __future__ import annotations

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
# 1. SPRITE BANK
# ---------------------------------------------------------------------

PLANK_TOP_A = 12
PLANK_TOP_B = 13
PLANK_BOT_A = 13
PLANK_BOT_B = 12


def _plank_pixels(length: int) -> list[list[int]]:
    """Build a 2-row stripe pattern."""
    top = [PLANK_TOP_A if i % 2 == 0 else PLANK_TOP_B for i in range(length)]
    bot = [PLANK_BOT_A if i % 2 == 0 else PLANK_BOT_B for i in range(length)]
    return [top, bot]


sprites = {
    "anchor_fixture": Sprite(
        pixels=[
            [5, 5, 5],
            [5, 11, 5],
            [5, 5, 5],
        ],
        name="anchor_fixture",
        visible=True,
        collidable=True,
        tags=["anchor_fixture"],
        layer=3,
    ),
    "anchor_halo": Sprite(
        pixels=[
            [14, 14, 14],
            [14, -1, 14],
            [14, 14, 14],
        ],
        name="anchor_halo",
        visible=True,
        collidable=True,
        tags=["halo"],
        layer=5,
    ),
    "goal_tile": Sprite(
        pixels=[
            [6, 6, 6, 6],
            [6, 0, 0, 6],
            [6, 0, 0, 6],
            [6, 6, 6, 6],
        ],
        name="goal_tile",
        visible=True,
        collidable=True,
        tags=["goal"],
        layer=0,
    ),
    "pawn": Sprite(
        pixels=[
            [5, 8, 5],
            [8, 0, 8],
            [5, 8, 5],
        ],
        name="pawn",
        visible=True,
        collidable=True,
        tags=["pawn"],
        layer=4,
    ),
    "plank_l13": Sprite(
        pixels=_plank_pixels(13),
        name="plank_l13",
        visible=True,
        collidable=True,
        tags=["plank", "sys_click"],
        layer=1,
    ),
    "plank_l8": Sprite(
        pixels=_plank_pixels(8),
        name="plank_l8",
        visible=True,
        collidable=True,
        tags=["plank", "sys_click"],
        layer=1,
    ),
    "post_blocking": Sprite(
        pixels=[
            [5, 5, 5],
            [5, 4, 5],
            [5, 5, 5],
        ],
        name="post_blocking",
        visible=True,
        collidable=True,
        tags=["post", "post_blocking", "sys_click"],
        layer=2,
    ),
    "post_permeable": Sprite(
        pixels=[
            [4, 4, 4],
            [4, 0, 4],
            [4, 4, 4],
        ],
        name="post_permeable",
        visible=True,
        collidable=True,
        tags=["post", "post_permeable", "sys_click"],
        layer=2,
    ),
    "spring": Sprite(
        pixels=[
            [5, 14, 5],
            [14, 0, 14],
            [5, 14, 5],
        ],
        name="spring",
        visible=True,
        collidable=True,
        tags=["spring"],
        layer=2,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

# Level 1: one plank, one pawn, one goal. Grid 32×32.
def _build_level1() -> Level:
    plank = sprites["plank_l8"].clone().set_position(10, 10)
    fixture = sprites["anchor_fixture"].clone().set_position(9, 9)
    pawn = sprites["pawn"].clone().set_position(13, 10)
    goal = sprites["goal_tile"].clone().set_position(10, 17)
    halo = sprites["anchor_halo"].clone().set_position(9, 9)
    halo.set_interaction(InteractionMode.REMOVED)
    return Level(
        sprites=[plank, fixture, pawn, goal, halo],
        grid_size=(32, 32),
        data={
            "step_budget": 30,
            "planks": [
                {"name": "plank_main", "anchor": (10, 10), "length": 8, "fixture_idx": 1},
            ],
            "pawn_idx": 2,
            "goal_idx": 3,
            "halo_idx": 4,
            "posts": [],
            "springs": [],
        },
    )


# Level 2: two planks + one toggleable post. Grid 32×32.
def _build_level2() -> Level:
    plank_alpha = sprites["plank_l13"].clone().set_position(4, 6)
    fixture_alpha = sprites["anchor_fixture"].clone().set_position(3, 5)
    plank_beta = sprites["plank_l13"].clone().set_position(4, 18)
    fixture_beta = sprites["anchor_fixture"].clone().set_position(3, 17)
    pawn = sprites["pawn"].clone().set_position(8, 6)
    goal = sprites["goal_tile"].clone().set_position(16, 18)
    post_blocking = sprites["post_blocking"].clone().set_position(3, 11)
    post_permeable = sprites["post_permeable"].clone().set_position(3, 11)
    post_permeable.set_interaction(InteractionMode.REMOVED)
    halo = sprites["anchor_halo"].clone().set_position(3, 5)
    halo.set_interaction(InteractionMode.REMOVED)
    return Level(
        sprites=[
            plank_alpha,
            fixture_alpha,
            plank_beta,
            fixture_beta,
            pawn,
            goal,
            post_blocking,
            post_permeable,
            halo,
        ],
        grid_size=(32, 32),
        data={
            "step_budget": 50,
            "planks": [
                {"name": "plank_alpha", "anchor": (4, 6), "length": 13, "fixture_idx": 1},
                {"name": "plank_beta", "anchor": (4, 18), "length": 13, "fixture_idx": 3},
            ],
            "pawn_idx": 4,
            "goal_idx": 5,
            "halo_idx": 8,
            "posts": [
                {"center": (4, 12), "blocking_idx": 6, "permeable_idx": 7},
            ],
            "springs": [],
        },
    )


# Level 3: two planks + one post + one spring. Grid 32×32.
def _build_level3() -> Level:
    plank_gamma = sprites["plank_l13"].clone().set_position(4, 8)
    fixture_gamma = sprites["anchor_fixture"].clone().set_position(3, 7)
    plank_delta = sprites["plank_l8"].clone().set_position(4, 20)
    fixture_delta = sprites["anchor_fixture"].clone().set_position(3, 19)
    pawn = sprites["pawn"].clone().set_position(8, 8)
    goal = sprites["goal_tile"].clone().set_position(16, 20)
    post_blocking = sprites["post_blocking"].clone().set_position(3, 13)
    post_permeable = sprites["post_permeable"].clone().set_position(3, 13)
    post_permeable.set_interaction(InteractionMode.REMOVED)
    spring = sprites["spring"].clone().set_position(10, 19)
    halo = sprites["anchor_halo"].clone().set_position(3, 7)
    halo.set_interaction(InteractionMode.REMOVED)
    return Level(
        sprites=[
            plank_gamma,
            fixture_gamma,
            plank_delta,
            fixture_delta,
            pawn,
            goal,
            post_blocking,
            post_permeable,
            spring,
            halo,
        ],
        grid_size=(32, 32),
        data={
            "step_budget": 60,
            "planks": [
                {"name": "plank_gamma", "anchor": (4, 8), "length": 13, "fixture_idx": 1},
                {
                    "name": "plank_delta",
                    "anchor": (4, 20),
                    "length": 8,
                    "fixture_idx": 3,
                    "spring_idx": 8,
                    "spring_offset_east": (7, 0),
                },
            ],
            "pawn_idx": 4,
            "goal_idx": 5,
            "halo_idx": 9,
            "posts": [
                {"center": (4, 14), "blocking_idx": 6, "permeable_idx": 7},
            ],
            "springs": [
                {"plank_name": "plank_delta", "offset_east": (7, 0), "range": 5, "sprite_idx": 8},
            ],
        },
    )


levels = [_build_level1(), _build_level2(), _build_level3()]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 10
PADDING_COLOR = 1
PLANK_THICKNESS = 2


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    """Bottom-row depleting bar."""

    def __init__(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current = max_steps

    def set_current(self, remaining: int) -> None:
        self.current = max(0, min(remaining, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        bar_width = 32
        x_offset = (64 - bar_width) // 2
        ratio = self.current / self.max_steps
        filled = round(bar_width * ratio)
        for x in range(bar_width):
            col = x_offset + x
            if x < filled:
                frame[63, col] = 11
            else:
                frame[63, col] = 5
        return frame


# ---------------------------------------------------------------------
# 5. PLANK STATE TRACKER
# ---------------------------------------------------------------------
class _PlankState:
    """Mutable per-instance plank state (anchor, length, orientation)."""

    __slots__ = (
        "name",
        "sprite",
        "fixture",
        "anchor_x",
        "anchor_y",
        "length",
        "orientation",
        "spring",
        "spring_offset_east",
        "spring_range",
    )

    def __init__(
        self,
        name: str,
        sprite: Sprite,
        fixture: Sprite,
        anchor_x: int,
        anchor_y: int,
        length: int,
    ) -> None:
        self.name = name
        self.sprite = sprite
        self.fixture = fixture
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.length = length
        self.orientation = 0
        self.spring = None
        self.spring_offset_east = None
        self.spring_range = 0

    def cells(self) -> set[tuple[int, int]]:
        return _compute_plank_cells(
            self.anchor_x, self.anchor_y, self.length, PLANK_THICKNESS, self.orientation
        )

    def cells_at(self, orientation: int) -> set[tuple[int, int]]:
        return _compute_plank_cells(
            self.anchor_x, self.anchor_y, self.length, PLANK_THICKNESS, orientation
        )

    def spring_cell_at(self, orientation: int) -> tuple[int, int] | None:
        if self.spring_offset_east is None:
            return None
        dx, dy = self.spring_offset_east
        # Apply CW rotation k times.
        for _ in range(orientation):
            dx, dy = -dy, dx
        return (self.anchor_x + dx, self.anchor_y + dy)

    def direction_vec(self) -> tuple[int, int]:
        return [(1, 0), (0, 1), (-1, 0), (0, -1)][self.orientation]


def _compute_plank_cells(
    ax: int, ay: int, length: int, thickness: int, orientation: int
) -> set[tuple[int, int]]:
    cells: set[tuple[int, int]] = set()
    for i in range(length):
        for j in range(thickness):
            if orientation == 0:
                cells.add((ax + i, ay + j))
            elif orientation == 1:
                cells.add((ax - j, ay + i))
            elif orientation == 2:
                cells.add((ax - i, ay - j))
            else:
                cells.add((ax + j, ay - i))
    return cells


def _render_plank_pixels(orientation: int, length: int) -> np.ndarray:
    base = np.array(_plank_pixels(length), dtype=np.int16)
    if orientation == 0:
        return base
    if orientation == 1:
        return np.rot90(base, k=-1)
    if orientation == 2:
        return np.rot90(base, k=2)
    return np.rot90(base, k=1)


def _plank_sprite_position(
    ax: int, ay: int, length: int, thickness: int, orientation: int
) -> tuple[int, int]:
    if orientation == 0:
        return (ax, ay)
    if orientation == 1:
        return (ax - thickness + 1, ay)
    if orientation == 2:
        return (ax - length + 1, ay - thickness + 1)
    return (ax, ay - length + 1)


# ---------------------------------------------------------------------
# 6. THE GAME CLASS
# ---------------------------------------------------------------------
class Kj82(NovaBaseGame):
    def __init__(self) -> None:
        camera = Camera(background=BACKGROUND_COLOR, letter_box=PADDING_COLOR)
        self._step_counter_ui = StepCounterHud(max_steps=30)
        camera.replace_interface([self._step_counter_ui])
        super().__init__(
            game_id="kj82",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )
        self._planks: list[_PlankState] = []
        self._post_pairs: list[dict] = []
        self._springs: list[dict] = []
        self._pawn: Sprite | None = None
        self._goal: Sprite | None = None
        self._halo: Sprite | None = None
        self._active_plank: _PlankState | None = None
        self._max_steps: int = 0

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        sprites_in_level = level.get_sprites()
        plank_specs = level.get_data("planks") or []
        post_specs = level.get_data("posts") or []
        spring_specs = level.get_data("springs") or []
        pawn_idx = level.get_data("pawn_idx")
        goal_idx = level.get_data("goal_idx")
        halo_idx = level.get_data("halo_idx")
        self._max_steps = int(level.get_data("step_budget") or 0)

        self._step_counter_ui.max_steps = self._max_steps
        self._step_counter_ui.set_current(self._max_steps)

        self._pawn = sprites_in_level[pawn_idx] if pawn_idx is not None else None
        self._goal = sprites_in_level[goal_idx] if goal_idx is not None else None
        self._halo = sprites_in_level[halo_idx] if halo_idx is not None else None
        if self._halo is not None:
            self._halo.set_interaction(InteractionMode.REMOVED)

        self._planks = []
        for spec in plank_specs:
            ax, ay = spec["anchor"]
            length = int(spec["length"])
            plank_name = spec["name"]
            sprite_idx = next(
                i
                for i, s in enumerate(sprites_in_level)
                if "plank" in (s.tags or []) and s.x == ax and s.y == ay
            )
            plank_sprite = sprites_in_level[sprite_idx]
            fixture = sprites_in_level[spec["fixture_idx"]]
            state = _PlankState(plank_name, plank_sprite, fixture, ax, ay, length)
            if "spring_offset_east" in spec:
                state.spring_offset_east = tuple(spec["spring_offset_east"])
            self._planks.append(state)

        self._post_pairs = []
        for spec in post_specs:
            self._post_pairs.append(
                {
                    "center": tuple(spec["center"]),
                    "blocking": sprites_in_level[spec["blocking_idx"]],
                    "permeable": sprites_in_level[spec["permeable_idx"]],
                }
            )

        self._springs = []
        for spec in spring_specs:
            owner = next(p for p in self._planks if p.name == spec["plank_name"])
            owner.spring = sprites_in_level[spec["sprite_idx"]]
            owner.spring_offset_east = tuple(spec["offset_east"])
            owner.spring_range = int(spec["range"])
            self._springs.append(owner)

        self._active_plank = None

        # Render every plank to its current orientation (defaults to 0 = east).
        for plank in self._planks:
            self._refresh_plank_visual(plank)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _refresh_plank_visual(self, plank: _PlankState) -> None:
        new_pixels = _render_plank_pixels(plank.orientation, plank.length)
        plank.sprite.pixels = new_pixels
        sx, sy = _plank_sprite_position(
            plank.anchor_x, plank.anchor_y, plank.length, PLANK_THICKNESS, plank.orientation
        )
        plank.sprite.set_position(sx, sy)
        # Fixture stays centered on anchor.
        plank.fixture.set_position(plank.anchor_x - 1, plank.anchor_y - 1)
        # Spring (child) follows its plank.
        if plank.spring is not None:
            sc = plank.spring_cell_at(plank.orientation)
            if sc is not None:
                plank.spring.set_position(sc[0] - 1, sc[1] - 1)

    def _all_plank_cells(self) -> set[tuple[int, int]]:
        cells: set[tuple[int, int]] = set()
        for p in self._planks:
            cells |= p.cells()
        return cells

    def _is_post_blocking_at(self, gx: int, gy: int) -> bool:
        for pair in self._post_pairs:
            cx, cy = pair["center"]
            if abs(gx - cx) <= 1 and abs(gy - cy) <= 1:
                blocking = pair["blocking"]
                if (
                    hasattr(blocking, "_interaction")
                    and blocking._interaction == InteractionMode.TANGIBLE
                ) or self._sprite_active(blocking):
                    return True
        return False

    def _sprite_active(self, s: Sprite) -> bool:
        """Treat a sprite as 'active' if it's not REMOVED."""
        try:
            return s.interaction != InteractionMode.REMOVED
        except AttributeError:
            return True

    def _post_blocking_cells(self) -> set[tuple[int, int]]:
        cells: set[tuple[int, int]] = set()
        for pair in self._post_pairs:
            if not self._sprite_active(pair["blocking"]):
                continue
            cx, cy = pair["center"]
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    cells.add((cx + dx, cy + dy))
        return cells

    def _post_at(self, gx: int, gy: int) -> dict | None:
        for pair in self._post_pairs:
            cx, cy = pair["center"]
            if abs(gx - cx) <= 1 and abs(gy - cy) <= 1:
                return pair
        return None

    def _toggle_post(self, pair: dict) -> None:
        blocking = pair["blocking"]
        permeable = pair["permeable"]
        if self._sprite_active(blocking):
            blocking.set_interaction(InteractionMode.REMOVED)
            permeable.set_interaction(InteractionMode.TANGIBLE)
        else:
            blocking.set_interaction(InteractionMode.TANGIBLE)
            permeable.set_interaction(InteractionMode.REMOVED)

    def _plank_at(self, gx: int, gy: int) -> _PlankState | None:
        for p in self._planks:
            if (gx, gy) in p.cells():
                return p
        return None

    def _set_active_plank(self, plank: _PlankState | None) -> None:
        self._active_plank = plank
        if self._halo is None:
            return
        if plank is None:
            self._halo.set_interaction(InteractionMode.REMOVED)
        else:
            self._halo.set_interaction(InteractionMode.TANGIBLE)
            self._halo.set_position(plank.anchor_x - 1, plank.anchor_y - 1)

    def _grid_size(self) -> tuple[int, int]:
        size = self.current_level.grid_size or (64, 64)
        return size

    def _on_grid(self, x: int, y: int) -> bool:
        gw, gh = self._grid_size()
        return 0 <= x < gw and 0 <= y < gh

    def _try_pivot_active_plank(self) -> None:
        if self._active_plank is None:
            return
        plank = self._active_plank
        new_orient = (plank.orientation + 1) % 4
        new_cells = plank.cells_at(new_orient)
        gw, gh = self._grid_size()
        for cx, cy in new_cells:
            if not (0 <= cx < gw and 0 <= cy < gh):
                return
        blocking = self._post_blocking_cells()
        if new_cells & blocking:
            return
        # Compute pivot-carry for the pawn.
        if self._pawn is not None:
            pawn_cell = (self._pawn.x, self._pawn.y)
            if pawn_cell in plank.cells():
                ax, ay = plank.anchor_x, plank.anchor_y
                dx = pawn_cell[0] - ax
                dy = pawn_cell[1] - ay
                # 90° CW around (ax, ay): new offset = (-dy, dx)
                new_pawn_cell = (ax - dy, ay + dx)
                # Confirm new pawn cell on plank in new orientation.
                if new_pawn_cell in new_cells:
                    self._pawn.set_position(new_pawn_cell[0], new_pawn_cell[1])
        plank.orientation = new_orient
        self._refresh_plank_visual(plank)

    def _try_walk_pawn(self, dx: int, dy: int) -> None:
        if self._pawn is None:
            return
        nx, ny = self._pawn.x + dx, self._pawn.y + dy
        gw, gh = self._grid_size()
        if not (0 <= nx < gw and 0 <= ny < gh):
            return
        if (nx, ny) not in self._all_plank_cells():
            return
        # Pawn cannot walk onto cells covered by a post in the blocking state.
        for pair in self._post_pairs:
            if not self._sprite_active(pair["blocking"]):
                continue
            cx, cy = pair["center"]
            if abs(nx - cx) <= 1 and abs(ny - cy) <= 1:
                return
        self._pawn.set_position(nx, ny)

    def _maybe_fire_spring(self) -> None:
        if self._pawn is None:
            return
        for plank in self._springs:
            if plank.spring is None or plank.spring_offset_east is None:
                continue
            spring_cell = plank.spring_cell_at(plank.orientation)
            if spring_cell is None:
                continue
            if (self._pawn.x, self._pawn.y) != spring_cell:
                continue
            dx, dy = plank.direction_vec()
            r = plank.spring_range
            blocking = self._post_blocking_cells()
            for step in range(1, r + 1):
                cx = spring_cell[0] + dx * step
                cy = spring_cell[1] + dy * step
                if (cx, cy) in blocking:
                    return
            destx = spring_cell[0] + dx * r
            desty = spring_cell[1] + dy * r
            if not self._on_grid(destx, desty):
                return
            valid = (destx, desty) in self._all_plank_cells()
            if self._goal is not None and (destx, desty) == (self._goal.x, self._goal.y):
                valid = True
            if not valid:
                return
            self._pawn.set_position(destx, desty)
            return

    def _check_win(self) -> bool:
        if self._pawn is None or self._goal is None:
            return False
        return (self._pawn.x, self._pawn.y) == (self._goal.x, self._goal.y)

    # ------------------------------------------------------------------
    # Engine entry points
    # ------------------------------------------------------------------

    def step(self) -> None:
        if self._action_count >= self._max_steps and self._max_steps > 0:
            self.lose()
            self.complete_action()
            return

        action_id = self.action.id

        if action_id == GameAction.ACTION6:
            x = int(self.action.data["x"])
            y = int(self.action.data["y"])
            grid = self.camera.display_to_grid(x, y)
            if grid is not None:
                gx, gy = grid
                post_pair = self._post_at(gx, gy)
                if post_pair is not None:
                    self._toggle_post(post_pair)
                else:
                    plank = self._plank_at(gx, gy)
                    if plank is not None:
                        if plank is self._active_plank:
                            self._set_active_plank(None)
                        else:
                            self._set_active_plank(plank)
        elif action_id == GameAction.ACTION5:
            self._try_pivot_active_plank()
        elif action_id == GameAction.ACTION1:
            self._try_walk_pawn(0, -1)
        elif action_id == GameAction.ACTION2:
            self._try_walk_pawn(0, 1)
        elif action_id == GameAction.ACTION3:
            self._try_walk_pawn(-1, 0)
        elif action_id == GameAction.ACTION4:
            self._try_walk_pawn(1, 0)

        self._maybe_fire_spring()

        self._step_counter_ui.set_current(self._max_steps - self._action_count - 1)

        if self._check_win():
            self.next_level()

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((4, 4), dtype=np.int16)
        out[0, 0] = self._step_counter_ui.current
        out[0, 1] = 0 if self._active_plank is None else 1
        if self._active_plank is not None:
            out[0, 2] = self._active_plank.orientation
        return out

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()
