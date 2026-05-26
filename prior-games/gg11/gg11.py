"""Tide-Current-Drift (gg11).

Dungeon-explorer themed: each level hosts multiple coloured avatars
that must each find their own colour-matched cross-shaped exit. A
global current direction (N/S/W/E) drifts every non-anchored pawn one
cell per ACTION5 tick. Arrow keys ACTION1..4 SET the current
direction (no drift). ACTION6 click toggles a pawn's anchor.

Sticky exits are active on every level: a pawn that lands on its own
matching exit auto-anchors irreversibly and acts as a wall thereafter,
so delivery order matters. Step budgets are tight enough that
solving each pawn one-at-a-time (anchor / unanchor shuffles) runs
out of energy — the player must orchestrate cooperative drift
sequences that advance every pawn at once.

Visuals: 12×12 dungeon grid rendered at 3 pixels per cell. Pawns are
solid coloured 3×3 blocks; exits render as a hollow plus of four
coloured tiles around an empty centre, in matching pawn colour.
"""

import numpy as np
from novaengine import (
    NovaBaseGame,
    Camera,
    GameAction,
    Level,
    RenderableUserDisplay,
    Sprite,
)

# ---- Palette (Nova 0..15) ----
BG = 0
FLOOR = 5
WALL = 13
ANCHOR_MARK = 13
DIR_ACTIVE = 4
DIR_OFF = 13
HUD_FILL = 7
HUD_EMPTY = 0

# ---- Direction codes ----
DIR_N = (0, -1)
DIR_S = (0, 1)
DIR_W = (-1, 0)
DIR_E = (1, 0)

PAWN_COLORS = {
    "red":   2,
    "green": 3,
    "blue":  1,
}


class StepBarHUD(RenderableUserDisplay):
    """Step bar drawn on the top row of the frame."""

    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps <= 0:
            return frame
        ratio = max(0.0, min(1.0, self.game.steps_left / self.game.max_steps))
        filled = int(round(frame.shape[1] * ratio))
        for x in range(frame.shape[1]):
            frame[0, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


class Pawn:
    def __init__(self, name: str, pos: tuple[int, int], exit_pos: tuple[int, int]):
        self.name = name
        self.pos = pos
        self.exit_pos = exit_pos
        self.anchored = False
        self.sticky = False

    @property
    def color(self) -> int:
        return PAWN_COLORS[self.name]

    @property
    def is_locked(self) -> bool:
        return self.anchored or self.sticky


class Gg11(NovaBaseGame):
    GRID_W = 12
    GRID_H = 12
    CELL = 3                 # 3 pixels per logical cell
    GRID_PX_X0 = 0           # grid pixel offset (left)
    GRID_PX_Y0 = 1           # row 0 reserved for HUD
    GRID_PX_W = GRID_W * CELL
    GRID_PX_H = GRID_H * CELL
    STATUS_PX_Y = GRID_PX_Y0 + GRID_PX_H  # status row starts here
    CAM_W = GRID_W * CELL                 # 36
    CAM_H = GRID_PX_Y0 + GRID_PX_H + CELL  # 1 + 36 + 3 = 40

    def __init__(self) -> None:
        self.hud = StepBarHUD(self)
        camera = Camera(
            background=BG,
            letter_box=BG,
            interfaces=[self.hud],
        )
        levels = [
            Level(grid_size=(self.CAM_W, self.CAM_H), sprites=[], data={"Level": 1}),
            Level(grid_size=(self.CAM_W, self.CAM_H), sprites=[], data={"Level": 2}),
            Level(grid_size=(self.CAM_W, self.CAM_H), sprites=[], data={"Level": 3}),
        ]

        self.pawns: list[Pawn] = []
        self.walls: set[tuple[int, int]] = set()
        self.current_dir = DIR_E
        self.steps_left = 0
        self.max_steps = 0

        super().__init__(
            game_id="gg11",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )

    # ------------------------------------------------------------------ #
    #  Level setup                                                        #
    # ------------------------------------------------------------------ #
    def on_set_level(self, level: Level) -> None:
        lvl = level.get_data("Level")
        self.walls = set()
        self.current_dir = DIR_E
        if lvl == 1:
            self._setup_level_1()
        elif lvl == 2:
            self._setup_level_2()
        else:
            self._setup_level_3()
        self.steps_left = self.max_steps
        self._sync_sprites()

    def _setup_level_1(self) -> None:
        """Two paired chambers each with a single mid-row wall. The
        cooperative path is E (until both stall on their walls), one
        S, E (past both walls), one N — anchor-shuffles cost more
        than the budget allows because each pawn alone needs the
        same 4-direction detour."""
        self.pawns = [
            Pawn("red",   pos=(2, 2), exit_pos=(8, 2)),
            Pawn("green", pos=(2, 9), exit_pos=(8, 9)),
        ]
        self.walls = {(5, 2), (5, 9), (6, 1), (6, 8), (7, 3), (7, 10)}
        self.max_steps = 16

    def _setup_level_2(self) -> None:
        """Two avatars must swap diagonally between corners. Sticky
        exits create a deadlock if either pawn lands on its exit
        before the other has cleared the row, so the cooperative
        path lifts both pawns to a parallel inner corridor and
        delivers green to (1,10) FIRST while red waits at the west
        edge, then routes red east via the upper corridor."""
        self.pawns = [
            Pawn("red",   pos=(1, 1),  exit_pos=(10, 10)),
            Pawn("green", pos=(10, 1), exit_pos=(1, 10)),
        ]
        self.walls = {(5, 5), (6, 5), (5, 6), (6, 6), (8, 1), (8, 2)}
        self.max_steps = 42

    def _setup_level_3(self) -> None:
        """Three avatars in a tri-floor dungeon, each blocked at a
        different column on their row. The shared drift schedule
        (E to stall the slowest, S one row, E to ferry past every
        wall via the lower edge, N to align, W to land) tags all
        three exits in the same sequence."""
        self.pawns = [
            Pawn("red",   pos=(1, 2),  exit_pos=(10, 2)),
            Pawn("green", pos=(1, 6),  exit_pos=(10, 6)),
            Pawn("blue",  pos=(1, 10), exit_pos=(10, 10)),
        ]
        self.walls = {
            (5, 2), (7, 6), (3, 10),
            (6, 1), (6, 3),
            (8, 5), (8, 7),
            (4, 9), (4, 11),
            (5, 4),
        }
        self.max_steps = 22

    # ------------------------------------------------------------------ #
    #  Movement helpers                                                   #
    # ------------------------------------------------------------------ #
    def _in_bounds(self, pos) -> bool:
        x, y = pos
        return 0 <= x < self.GRID_W and 0 <= y < self.GRID_H

    def _occupied_by_pawn(self, pos, exclude: Pawn | None = None):
        for p in self.pawns:
            if p is exclude:
                continue
            if p.pos == pos:
                return p
        return None

    def _can_enter(self, pos, mover: Pawn) -> bool:
        if not self._in_bounds(pos):
            return False
        if pos in self.walls:
            return False
        if self._occupied_by_pawn(pos, exclude=mover) is not None:
            return False
        return True

    def _drift_tick(self) -> None:
        dx, dy = self.current_dir
        if dx > 0:
            order = sorted(self.pawns, key=lambda p: -p.pos[0])
        elif dx < 0:
            order = sorted(self.pawns, key=lambda p: p.pos[0])
        elif dy > 0:
            order = sorted(self.pawns, key=lambda p: -p.pos[1])
        else:
            order = sorted(self.pawns, key=lambda p: p.pos[1])

        for p in order:
            if p.is_locked:
                continue
            new_pos = (p.pos[0] + dx, p.pos[1] + dy)
            if self._can_enter(new_pos, mover=p):
                p.pos = new_pos
                if p.pos == p.exit_pos:
                    p.sticky = True

    # ------------------------------------------------------------------ #
    #  Click → pawn anchor toggle                                         #
    # ------------------------------------------------------------------ #
    def _map_click_to_cell(self, gx: int, gy: int):
        scale = min(64 // self.CAM_W, 64 // self.CAM_H)
        ox = (64 - self.CAM_W * scale) // 2
        oy = (64 - self.CAM_H * scale) // 2
        if not (ox <= gx < ox + self.CAM_W * scale and
                oy <= gy < oy + self.CAM_H * scale):
            return None
        cam_x = (gx - ox) // scale
        cam_y = (gy - oy) // scale
        # Subtract HUD offset, then divide by cell size.
        grid_y = cam_y - self.GRID_PX_Y0
        if grid_y < 0:
            return None
        cx = cam_x // self.CELL
        cy = grid_y // self.CELL
        if not (0 <= cx < self.GRID_W and 0 <= cy < self.GRID_H):
            return None
        return (cx, cy)

    def _click_anchor(self, gx: int, gy: int) -> bool:
        cell = self._map_click_to_cell(gx, gy)
        if cell is None:
            return False
        for p in self.pawns:
            if p.pos == cell and not p.sticky:
                p.anchored = not p.anchored
                return True
        return False

    # ------------------------------------------------------------------ #
    #  Sprite construction                                                #
    # ------------------------------------------------------------------ #
    def _floor_pixels(self):
        return [[FLOOR] * self.CELL for _ in range(self.CELL)]

    def _wall_pixels(self):
        return [[WALL] * self.CELL for _ in range(self.CELL)]

    def _exit_pixels(self, color: int):
        # 3×3 plus-shape with hollow centre and corners.
        return [
            [-1,    color, -1],
            [color, -1,    color],
            [-1,    color, -1],
        ]

    def _pawn_pixels(self, color: int, locked: bool):
        px = [[color] * self.CELL for _ in range(self.CELL)]
        if locked:
            px[1][1] = ANCHOR_MARK
        return px

    def _arrow_pixels(self, direction, active: bool):
        c = DIR_ACTIVE if active else DIR_OFF
        if direction == DIR_N:
            return [[-1, c, -1], [c, c, c], [-1, -1, -1]]
        if direction == DIR_S:
            return [[-1, -1, -1], [c, c, c], [-1, c, -1]]
        if direction == DIR_W:
            return [[-1, c, -1], [c, c, -1], [-1, c, -1]]
        if direction == DIR_E:
            return [[-1, c, -1], [-1, c, c], [-1, c, -1]]
        return [[c] * 3 for _ in range(3)]

    def _pip_pixels(self, color: int, locked: bool):
        px = [[color] * self.CELL for _ in range(self.CELL)]
        if locked:
            px[1][1] = ANCHOR_MARK
        return px

    def _cell_to_pixel(self, cx: int, cy: int) -> tuple[int, int]:
        return (self.GRID_PX_X0 + cx * self.CELL,
                self.GRID_PX_Y0 + cy * self.CELL)

    # ------------------------------------------------------------------ #
    #  Rendering                                                          #
    # ------------------------------------------------------------------ #
    def _sync_sprites(self) -> None:
        sprites = []

        for cy in range(self.GRID_H):
            for cx in range(self.GRID_W):
                px, py = self._cell_to_pixel(cx, cy)
                sprites.append(
                    Sprite(self._floor_pixels(), name=f"floor_{cx}_{cy}", layer=0)
                    .set_position(px, py)
                )

        for (wx, wy) in sorted(self.walls):
            px, py = self._cell_to_pixel(wx, wy)
            sprites.append(
                Sprite(self._wall_pixels(), name=f"wall_{wx}_{wy}", layer=2)
                .set_position(px, py)
            )

        for p in self.pawns:
            ex, ey = p.exit_pos
            px, py = self._cell_to_pixel(ex, ey)
            sprites.append(
                Sprite(self._exit_pixels(p.color),
                       name=f"exit_{p.name}", layer=3)
                .set_position(px, py)
            )

        for p in self.pawns:
            cx, cy = p.pos
            px, py = self._cell_to_pixel(cx, cy)
            sprites.append(
                Sprite(self._pawn_pixels(p.color, p.is_locked),
                       name=f"pawn_{p.name}", layer=5)
                .set_position(px, py)
            )

        # Status row: pawn anchor pips on the left, direction arrows on the right.
        for i, p in enumerate(self.pawns):
            sprites.append(
                Sprite(self._pip_pixels(p.color, p.is_locked),
                       name=f"pip_{i}", layer=4)
                .set_position(i * self.CELL, self.STATUS_PX_Y)
            )

        arrow_slots = [DIR_N, DIR_S, DIR_W, DIR_E]
        for j, d in enumerate(arrow_slots):
            slot_cell_x = 4 + j  # leave a 1-cell gap after the pips
            sprites.append(
                Sprite(self._arrow_pixels(d, d == self.current_dir),
                       name=f"arrow_{j}", layer=4)
                .set_position(slot_cell_x * self.CELL, self.STATUS_PX_Y)
            )

        self.current_level._sprites = sprites

    # ------------------------------------------------------------------ #
    #  Win                                                                #
    # ------------------------------------------------------------------ #
    def _check_win(self) -> bool:
        return all(p.pos == p.exit_pos for p in self.pawns)

    # ------------------------------------------------------------------ #
    #  Step                                                               #
    # ------------------------------------------------------------------ #
    def step(self) -> None:
        aid = self.action.id
        acted = False

        if aid == GameAction.ACTION1:
            self.current_dir = DIR_N
            acted = True
        elif aid == GameAction.ACTION2:
            self.current_dir = DIR_S
            acted = True
        elif aid == GameAction.ACTION3:
            self.current_dir = DIR_W
            acted = True
        elif aid == GameAction.ACTION4:
            self.current_dir = DIR_E
            acted = True
        elif aid == GameAction.ACTION5:
            self._drift_tick()
            acted = True
        elif aid == GameAction.ACTION6:
            gx = int(self.action.data.get("x", -1))
            gy = int(self.action.data.get("y", -1))
            if self._click_anchor(gx, gy):
                acted = True

        if acted:
            self.steps_left -= 1

        self._sync_sprites()

        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()

        self.complete_action()

    # ------------------------------------------------------------------ #
    #  Hidden state                                                       #
    # ------------------------------------------------------------------ #
    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((self.GRID_H, self.GRID_W), dtype=np.int16)
        for (x, y) in self.walls:
            out[y, x] = 1
        for i, p in enumerate(self.pawns):
            x, y = p.exit_pos
            out[y, x] = 10 + i
            x, y = p.pos
            out[y, x] = 20 + i + (100 if p.is_locked else 0)
        return out
