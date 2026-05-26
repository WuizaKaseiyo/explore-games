"""Generated game mw8p (offline-pre-competition asset)."""

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
# CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 2  # light-grey
PADDING_COLOR = 2

CELL_STRIDE = 8         # pixels per logical cell
HALF_STRIDE = CELL_STRIDE // 2
GRID_CELLS = 8          # 8 logical cells per axis
SPRITE_SIZE = 6
SPRITE_OFFSET = 1       # 1-px margin inside the 8-px cell

HUD_FULL_COLOR = 14     # green
HUD_EMPTY_COLOR = 4
HUD_ROW = 63

# Animation phases per single A-action
PHASE_PLAN = 0          # entry: A moves, plan B's
PHASE_B_HALF = 1
PHASE_B_FULL = 2        # B's land + resolve B-on-A + plan C's
PHASE_C_HALF = 3
PHASE_C_FULL = 4        # C's land + resolve M2 + tick budget + complete_action


# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------

_PLAYER_PIXELS = [
    [-1,  4,  4,  4,  4, -1],
    [ 4, 10, 11, 10, 11,  4],
    [ 4, 10, 10, 10, 10,  4],
    [ 4, 10, 10, 10, 10,  4],
    [ 4, 10, 10, 10, 10,  4],
    [-1,  4,  4,  4,  4, -1],
]

_PURSUER_PIXELS = [
    [ 8, -1,  8, -1,  8, -1],
    [-1, 12, 12, 12, 12,  8],
    [ 8, 12,  4, 12,  4, 12],
    [12, 12, 12, 12, 12,  8],
    [-1, 12, 12, 12, 12,  8],
    [ 8, -1,  8, -1,  8, -1],
]

_MID_PIXELS = [
    [-1,  4, 14,  4, 14, -1],
    [ 4, 14, 14, 14, 14,  4],
    [14, 14,  7,  7, 14, 14],
    [14, 14,  7,  7, 14, 14],
    [ 4, 14, 14, 14, 14,  4],
    [-1,  4, 14,  4, 14, -1],
]

_WALL_PIXELS = [
    [ 4, 13, 13, 13, 13,  4],
    [13, 13, 13, 13, 13, 13],
    [13, 13,  4,  4, 13, 13],
    [13, 13,  4,  4, 13, 13],
    [13, 13, 13, 13, 13, 13],
    [ 4, 13, 13, 13, 13,  4],
]

_EXIT_PIXELS = [
    [15, 15, 15, 15, 15, 15],
    [15, 15, 15, 15, 15, 15],
    [15, 15,  0,  0, 15, 15],
    [15, 15,  0,  0, 15, 15],
    [15, 15, 15, 15, 15, 15],
    [15, 15, 15, 15, 15, 15],
]


def _cell_to_px(cx: int, cy: int) -> tuple[int, int]:
    return cx * CELL_STRIDE + SPRITE_OFFSET, cy * CELL_STRIDE + SPRITE_OFFSET


def _make_player(cx: int, cy: int) -> Sprite:
    px, py = _cell_to_px(cx, cy)
    return Sprite(pixels=_PLAYER_PIXELS, name="player", x=px, y=py,
                  tags=["player"], layer=3)


def _make_pursuer(cx: int, cy: int, idx: int) -> Sprite:
    px, py = _cell_to_px(cx, cy)
    return Sprite(pixels=_PURSUER_PIXELS, name=f"pursuer_{idx}", x=px, y=py,
                  tags=["pursuer"], layer=1)


def _make_mid(cx: int, cy: int, idx: int) -> Sprite:
    px, py = _cell_to_px(cx, cy)
    return Sprite(pixels=_MID_PIXELS, name=f"mid_{idx}", x=px, y=py,
                  tags=["mid"], layer=2)


def _make_wall(cx: int, cy: int, idx: int) -> Sprite:
    px, py = _cell_to_px(cx, cy)
    return Sprite(pixels=_WALL_PIXELS, name=f"wall_{idx}", x=px, y=py,
                  tags=["wall"], layer=0)


def _make_exit(cx: int, cy: int) -> Sprite:
    px, py = _cell_to_px(cx, cy)
    return Sprite(pixels=_EXIT_PIXELS, name="exit", x=px, y=py,
                  tags=["exit"], layer=0, collidable=False)


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

def _build_level_1() -> Level:
    sprites_list = [
        _make_player(0, 0),
        _make_pursuer(2, 1, 0),
        _make_exit(7, 7),
    ]
    return Level(
        sprites=sprites_list,
        grid_size=(64, 64),
        data={"max_steps": 25, "exit_cell": (7, 7)},
    )


def _build_level_2() -> Level:
    sprites_list = [
        _make_player(0, 0),
        _make_mid(4, 3, 0),
        _make_pursuer(4, 5, 0),
        _make_exit(7, 7),
    ]
    return Level(
        sprites=sprites_list,
        grid_size=(64, 64),
        data={"max_steps": 30, "exit_cell": (7, 7)},
    )


def _build_level_3() -> Level:
    sprites_list = [
        _make_player(0, 0),
        _make_mid(1, 0, 0),       # C1: A's only first-move (must eat)
        _make_mid(1, 7, 1),       # C2: intercepts B if A retreats westward
        _make_pursuer(4, 4, 0),
        _make_wall(0, 1, 0),      # forces A's first move onto C1
        _make_exit(7, 7),
    ]
    return Level(
        sprites=sprites_list,
        grid_size=(64, 64),
        data={"max_steps": 35, "exit_cell": (7, 7)},
    )


levels = [_build_level_1(), _build_level_2(), _build_level_3()]


# ---------------------------------------------------------------------
# 3. STEP COUNTER HUD
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 1) -> None:
        super().__init__()
        self._max = max_steps
        self._remaining = max_steps

    def reset(self, max_steps: int) -> None:
        self._max = max_steps
        self._remaining = max_steps

    def set_remaining(self, remaining: int) -> None:
        self._remaining = max(0, remaining)

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self._max <= 0:
            return frame
        fill_width = int(round(64 * self._remaining / self._max))
        fill_width = max(0, min(64, fill_width))
        frame[HUD_ROW, :fill_width] = HUD_FULL_COLOR
        frame[HUD_ROW, fill_width:] = HUD_EMPTY_COLOR
        return frame


# ---------------------------------------------------------------------
# 4. GAME CLASS
# ---------------------------------------------------------------------

class Mw8p(NovaBaseGame):
    def __init__(self) -> None:
        self._step_bar = StepCounterHud(max_steps=25)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_bar],
        )
        super().__init__(
            game_id="mw8p",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )
        self._steps_used = 0
        self._max_steps = 25
        self._exit_cell: tuple[int, int] = (0, 0)
        self._phase = PHASE_PLAN
        self._b_pending: list[tuple[Sprite, int, int]] = []
        self._c_pending: list[tuple[Sprite, int, int]] = []

    # ----- cell helpers -----

    @staticmethod
    def _sprite_cell(s: Sprite) -> tuple[int, int]:
        return (s.x - SPRITE_OFFSET) // CELL_STRIDE, (s.y - SPRITE_OFFSET) // CELL_STRIDE

    def _set_sprite_cell(self, s: Sprite, cx: int, cy: int) -> None:
        s.set_position(cx * CELL_STRIDE + SPRITE_OFFSET, cy * CELL_STRIDE + SPRITE_OFFSET)

    def _live_sprites(self) -> list[Sprite]:
        return [s for s in self.current_level.get_sprites()
                if s._interaction != InteractionMode.REMOVED]

    def _sprite_at_cell(self, cx: int, cy: int, skip: Sprite | None = None) -> Sprite | None:
        for s in self._live_sprites():
            if s is skip:
                continue
            if self._sprite_cell(s) == (cx, cy):
                return s
        return None

    def _player(self) -> Sprite:
        return self.current_level.get_sprites_by_tag("player")[0]

    def _live_pursuers(self) -> list[Sprite]:
        return [s for s in self.current_level.get_sprites_by_tag("pursuer")
                if s._interaction != InteractionMode.REMOVED]

    def _live_mids(self) -> list[Sprite]:
        return [s for s in self.current_level.get_sprites_by_tag("mid")
                if s._interaction != InteractionMode.REMOVED]

    # ----- lifecycle -----

    def on_set_level(self, level: Level) -> None:
        self._steps_used = 0
        self._max_steps = level.get_data("max_steps") or 25
        self._exit_cell = tuple(level.get_data("exit_cell") or (0, 0))
        self._step_bar.reset(self._max_steps)
        self._phase = PHASE_PLAN
        self._b_pending = []
        self._c_pending = []

    # ----- pursuit planning -----

    def _plan_step(self, mover_cell: tuple[int, int], target_cell: tuple[int, int],
                   reserved_cells: set[tuple[int, int]],
                   kill_target_tag: str | None = None) -> tuple[int, int]:
        """Return the (dx, dy) cardinal step the mover should take toward
        target_cell under Manhattan-dominant policy (tie → x), respecting
        walls, bounds, other reserved cells, and other creatures. Returns
        (0, 0) if the mover cannot move."""
        mcx, mcy = mover_cell
        tcx, tcy = target_cell
        ddx = tcx - mcx
        ddy = tcy - mcy
        if ddx == 0 and ddy == 0:
            return (0, 0)

        if abs(ddx) >= abs(ddy):
            primary = (1 if ddx > 0 else -1, 0)
            secondary = (0, 1 if ddy > 0 else -1) if ddy != 0 else None
        else:
            primary = (0, 1 if ddy > 0 else -1)
            secondary = (1 if ddx > 0 else -1, 0) if ddx != 0 else None

        for step in (primary, secondary):
            if step is None:
                continue
            sdx, sdy = step
            ncx, ncy = mcx + sdx, mcy + sdy
            if not (0 <= ncx < GRID_CELLS and 0 <= ncy < GRID_CELLS):
                continue
            if (ncx, ncy) in reserved_cells:
                continue
            occupant = self._sprite_at_cell(ncx, ncy)
            if occupant is None:
                return (sdx, sdy)
            tags = occupant._tags
            if kill_target_tag is not None and kill_target_tag in tags:
                return (sdx, sdy)
            if "player" in tags:
                return (sdx, sdy)  # pursuer entering player's cell — kills A
            # walls / other movers block
        return (0, 0)

    # ----- step -----

    def step(self) -> None:
        if self._phase == PHASE_PLAN:
            self._phase_plan()
        elif self._phase == PHASE_B_HALF:
            self._phase_b_half()
        elif self._phase == PHASE_B_FULL:
            self._phase_b_full()
        elif self._phase == PHASE_C_HALF:
            self._phase_c_half()
        elif self._phase == PHASE_C_FULL:
            self._phase_c_full()

    def _phase_plan(self) -> None:
        action_id = self.action.id
        if action_id == GameAction.ACTION1:
            dx, dy = 0, -1
        elif action_id == GameAction.ACTION2:
            dx, dy = 0, 1
        elif action_id == GameAction.ACTION3:
            dx, dy = -1, 0
        elif action_id == GameAction.ACTION4:
            dx, dy = 1, 0
        else:
            self.complete_action()
            return

        player = self._player()
        pcx, pcy = self._sprite_cell(player)
        ncx, ncy = pcx + dx, pcy + dy

        if 0 <= ncx < GRID_CELLS and 0 <= ncy < GRID_CELLS:
            target = self._sprite_at_cell(ncx, ncy, skip=player)
            if target is None:
                self._set_sprite_cell(player, ncx, ncy)
            else:
                tags = target._tags
                if "wall" in tags:
                    pass
                elif "exit" in tags:
                    self._set_sprite_cell(player, ncx, ncy)
                elif "mid" in tags:
                    target.set_interaction(InteractionMode.REMOVED)
                    self._set_sprite_cell(player, ncx, ncy)
                elif "pursuer" in tags:
                    self._set_sprite_cell(player, ncx, ncy)
                    self._consume_step()
                    self.lose()
                    self._phase = PHASE_PLAN
                    self.complete_action()
                    return

        if self._sprite_cell(player) == self._exit_cell:
            self._consume_step()
            self.next_level()
            self._phase = PHASE_PLAN
            self.complete_action()
            return

        # Plan B's: target = player's new cell; reserve cells incrementally
        self._b_pending = []
        reserved: set[tuple[int, int]] = set()
        player_cell = self._sprite_cell(player)
        for b in self._live_pursuers():
            bcx, bcy = self._sprite_cell(b)
            sdx, sdy = self._plan_step((bcx, bcy), player_cell, reserved)
            self._b_pending.append((b, sdx, sdy))
            if (sdx, sdy) != (0, 0):
                reserved.add((bcx + sdx, bcy + sdy))
        self._phase = PHASE_B_HALF

    def _phase_b_half(self) -> None:
        for b, dx, dy in self._b_pending:
            if (dx, dy) != (0, 0):
                b.move(dx * HALF_STRIDE, dy * HALF_STRIDE)
        self._phase = PHASE_B_FULL

    def _phase_b_full(self) -> None:
        for b, dx, dy in self._b_pending:
            if (dx, dy) != (0, 0):
                b.move(dx * HALF_STRIDE, dy * HALF_STRIDE)
        # Resolve B-on-A
        player = self._player()
        pcell = self._sprite_cell(player)
        for b in self._live_pursuers():
            if self._sprite_cell(b) == pcell:
                self._consume_step()
                self.lose()
                self._phase = PHASE_PLAN
                self.complete_action()
                return

        # Plan C's
        self._c_pending = []
        live_bs = self._live_pursuers()
        if not live_bs:
            # Skip C-phases entirely; finalize this action
            if self._consume_step():
                self.lose()
                self._phase = PHASE_PLAN
                self.complete_action()
                return
            self._phase = PHASE_PLAN
            self.complete_action()
            return

        reserved: set[tuple[int, int]] = set()
        for c in self._live_mids():
            ccx, ccy = self._sprite_cell(c)
            target = min(live_bs, key=lambda b: (
                abs(self._sprite_cell(b)[0] - ccx) + abs(self._sprite_cell(b)[1] - ccy),
                live_bs.index(b),
            ))
            tcell = self._sprite_cell(target)
            sdx, sdy = self._plan_step(
                (ccx, ccy), tcell, reserved, kill_target_tag="pursuer"
            )
            self._c_pending.append((c, sdx, sdy))
            if (sdx, sdy) != (0, 0):
                reserved.add((ccx + sdx, ccy + sdy))
        self._phase = PHASE_C_HALF

    def _phase_c_half(self) -> None:
        for c, dx, dy in self._c_pending:
            if (dx, dy) != (0, 0):
                c.move(dx * HALF_STRIDE, dy * HALF_STRIDE)
        self._phase = PHASE_C_FULL

    def _phase_c_full(self) -> None:
        for c, dx, dy in self._c_pending:
            if (dx, dy) != (0, 0):
                c.move(dx * HALF_STRIDE, dy * HALF_STRIDE)
        # Resolve C on B
        for c in self._live_mids():
            ccell = self._sprite_cell(c)
            for b in self._live_pursuers():
                if self._sprite_cell(b) == ccell:
                    b.set_interaction(InteractionMode.REMOVED)
                    break
        # Tick step counter
        if self._consume_step():
            self.lose()
            self._phase = PHASE_PLAN
            self.complete_action()
            return
        self._phase = PHASE_PLAN
        self.complete_action()

    def _consume_step(self) -> bool:
        self._steps_used += 1
        remaining = max(0, self._max_steps - self._steps_used)
        self._step_bar.set_remaining(remaining)
        return self._steps_used >= self._max_steps

    # ----- engine hooks -----

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
