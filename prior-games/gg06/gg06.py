"""Cluster-Rotate-Pivot: 6×6 grid of coloured tiles. Click a pivot to rotate
the 4 surrounding tiles 90° CW. Match the target arrangement to win."""

import numpy as np
from novaengine import (
    NovaBaseGame, Camera, GameAction, Level,
    Sprite, RenderableUserDisplay
)

# Colour palette (Nova standard 0-11)
BG_COLOR = 0          # black — background / empty
FLOOR_COLOR = 0       # black — empty tile
PIVOT_ACTIVE = 10     # light grey pivot dot
PIVOT_DISABLED = 13   # dark grey pivot dot (disabled)
LOCKED_BORDER = 0     # black border for locked tiles
MATCH_BORDER = 3      # green border for correctly-placed tiles


class StepBarHUD(RenderableUserDisplay):
    """Thin bar along the top showing remaining steps."""
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps > 0:
            ratio = self.game.current_steps / self.game.max_steps
            filled = int(round(frame.shape[1] * ratio))
            for x in range(frame.shape[1]):
                frame[-1, x] = 4 if x < filled else 5
        return frame


class Gg06(NovaBaseGame):
    """Cluster-Rotate-Pivot game.

    Layout: 6×6 logical tile grid.  Each tile is rendered as a 2×2 block
    of pixels (so the board is 12×12 px).  Pivots sit at the corners
    shared by four tiles — there are 5×5 = 25 pivot positions.  A 1-px
    dot is drawn for each pivot at pixel (2*px+1, 2*py+1).

    A small target preview is drawn to the right of the board.
    Total camera: 26×13 (12 board + 1 gap + 12 target + 1 pad).
    """

    TILE_PX = 3          # pixels per tile side
    BOARD_PX = 18        # 6 tiles × 3 px
    BUFFER_PX = 24       # 8 tiles × 3 px, includes one off-board ring
    BOARD_X = 2
    BOARD_Y = 2
    GAP = 3              # gap between board buffer and target preview
    CAM_W = 48           # off-board ring + target preview + padding
    CAM_H = 28           # off-board ring + bottom HUD

    def __init__(self) -> None:
        self.hud = StepBarHUD(self)
        camera = Camera(
            background=BG_COLOR,
            letter_box=BG_COLOR,
            interfaces=[self.hud],
        )
        levels = [
            Level(grid_size=(self.CAM_W, self.CAM_H), sprites=[], data={"Level": 1}),
            Level(grid_size=(self.CAM_W, self.CAM_H), sprites=[], data={"Level": 2}),
            Level(grid_size=(self.CAM_W, self.CAM_H), sprites=[], data={"Level": 3}),
        ]

        # State — initialised before super().__init__ because it calls
        # on_set_level which needs these fields.
        self.tiles = np.full((6, 6), FLOOR_COLOR, dtype=int)
        self.target = np.full((6, 6), FLOOR_COLOR, dtype=int)
        self.locked: set[tuple[int, int]] = set()
        self.disabled_pivots: set[tuple[int, int]] = set()
        self.outside_tiles: dict[tuple[int, int], int] = {}
        self.max_steps = 0
        self.current_steps = 0

        super().__init__(
            game_id="gg06",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    # ------------------------------------------------------------------ #
    #  Level setup                                                        #
    # ------------------------------------------------------------------ #

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.CAM_W
        self.camera.height = self.CAM_H
        self.current_level._grid_size = (self.CAM_W, self.CAM_H)
        lvl = level.get_data("Level")
        self.tiles.fill(FLOOR_COLOR)
        self.target.fill(FLOOR_COLOR)
        self.locked = set()
        self.disabled_pivots = set()
        self.outside_tiles = {}

        if lvl == 1:
            self._setup_level_1()
        elif lvl == 2:
            self._setup_level_2()
        elif lvl == 3:
            self._setup_level_3()

        self.current_steps = self.max_steps
        self._sync_sprites()

    # --- Level 1: pure rotation (M1 + M2) ---
    def _setup_level_1(self):
        self.max_steps = 45
        # 4-color checkerboard to prevent 180-degree symmetry and ensure visual separation
        colors = [[1, 2], [3, 7]]
        for r in range(4):
            for c in range(4):
                self.target[r, c] = colors[r % 2][c % 2]
        
        self.tiles[:] = self.target
        # Scramble with overlapping pivots to enforce ordering
        self._rotate_cw(0, 0)
        self._rotate_cw(1, 1)
        self._rotate_cw(2, 2)

    # --- Level 2: locked tiles (M1 + M2 + M3) ---
    def _setup_level_2(self):
        self.max_steps = 80
        self.locked = {(2, 2)}
        # 5x5 4-color checkerboard with center lock
        colors = [[1, 2], [3, 7]]
        for r in range(5):
            for c in range(5):
                if (c, r) == (2, 2):
                    self.target[r, c] = 0
                else:
                    self.target[r, c] = colors[r % 2][c % 2]
        
        self.tiles[:] = self.target
        # Scramble with overlapping pivots
        scramble_pivots = [(0, 0), (3, 0), (0, 3), (3, 3), (3, 1), (0, 1), (3, 2), (0, 2)]
        for p in scramble_pivots:
            self._rotate_cw(p[0], p[1])

    # --- Level 3: locked tiles + disabled pivots (M1 + M2 + M3 + M4) ---
    def _setup_level_3(self):
        self.max_steps = 150
        self.locked = {(2, 2), (2, 3), (3, 2), (3, 3)}
        self.disabled_pivots = {(1, 1), (1, 3), (3, 1), (3, 3)}
        
        # 6x6 4-color checkerboard
        colors = [[1, 2], [3, 7]]
        for r in range(6):
            for c in range(6):
                if (c, r) in self.locked:
                    self.target[r, c] = 0
                else:
                    self.target[r, c] = colors[r % 2][c % 2]

        self.tiles[:] = self.target
        # Complex scramble using allowed pivots twice to deeply mix the board
        allowed = []
        for py in range(5):
            for px in range(5):
                if (px, py) in self.disabled_pivots:
                    continue
                corners = [(px, py), (px+1, py), (px, py+1), (px+1, py+1)]
                if any((c, r) in self.locked for c, r in corners):
                    continue
                allowed.append((px, py))

        for p in allowed:
            self._rotate_cw(p[0], p[1])
            self._rotate_cw(p[0], p[1])

    # ------------------------------------------------------------------ #
    #  Pivot rotation helper (operates on self.tiles)                     #
    # ------------------------------------------------------------------ #

    def _rotate_cw(self, px: int, py: int) -> bool:
        """Rotate the 4 tiles around pivot (px, py) 90° CW.

        Pivot (px, py) connects tiles:
            (px, py)     (px+1, py)
            (px, py+1)   (px+1, py+1)

        CW permutation: TL←BL, TR←TL, BR←TR, BL←BR.
        Returns True if rotation was performed, False if blocked.
        """
        if (px, py) in self.disabled_pivots:
            return False
        if px < -1 or px > 5 or py < -1 or py > 5:
            return False

        # Check locked
        corners = [(px, py), (px+1, py), (px, py+1), (px+1, py+1)]
        if any((c, r) in self.locked for c, r in corners if 0 <= c < 6 and 0 <= r < 6):
            return False

        tl = self._get_tile(px, py)
        tr = self._get_tile(px+1, py)
        br = self._get_tile(px+1, py+1)
        bl = self._get_tile(px, py+1)

        self._set_tile(px, py, bl)       # TL ← BL
        self._set_tile(px+1, py, tl)     # TR ← TL
        self._set_tile(px+1, py+1, tr)   # BR ← TR
        self._set_tile(px, py+1, br)     # BL ← BR

        return True

    def _get_tile(self, c: int, r: int) -> int:
        if 0 <= c < 6 and 0 <= r < 6:
            return int(self.tiles[r, c])
        return self.outside_tiles.get((c, r), FLOOR_COLOR)

    def _set_tile(self, c: int, r: int, value: int) -> None:
        if 0 <= c < 6 and 0 <= r < 6:
            self.tiles[r, c] = value
        elif value == FLOOR_COLOR:
            self.outside_tiles.pop((c, r), None)
        else:
            self.outside_tiles[(c, r)] = value

    # ------------------------------------------------------------------ #
    #  Rendering                                                          #
    # ------------------------------------------------------------------ #

    def _sync_sprites(self):
        sprites = []
        T = self.TILE_PX

        def board_pos(c: int, r: int) -> tuple[int, int]:
            return self.BOARD_X + (c + 1) * T, self.BOARD_Y + (r + 1) * T

        # --- Draw board tiles plus the one-cell off-board rotation buffer ---
        for r in range(-1, 7):
            for c in range(-1, 7):
                color = self._get_tile(c, r)
                px = [[FLOOR_COLOR] * T for _ in range(T)]
                if color != FLOOR_COLOR:
                    px[1][1] = color
                    px[1][2] = color
                    px[2][1] = color
                    px[2][2] = color

                if 0 <= c < 6 and 0 <= r < 6 and (c, r) in self.locked:
                    # Locked: black immovable tile
                    for i in range(3):
                        px[0][i] = LOCKED_BORDER
                        px[i][0] = LOCKED_BORDER
                        px[i][2] = LOCKED_BORDER
                        px[2][i] = LOCKED_BORDER

                if not (0 <= c < 6 and 0 <= r < 6) and color == FLOOR_COLOR:
                    px[1][1] = PIVOT_DISABLED

                x, y = board_pos(c, r)
                sprites.append(
                    Sprite(pixels=px, name=f"tile_{c}_{r}", layer=0)
                    .set_position(x, y)
                )

        # --- Draw target preview ---
        ox = self.BOARD_X + self.BUFFER_PX + self.GAP  # x-offset for target
        oy = self.BOARD_Y + T
        
        # Add frame around target
        frame_color = 5  # dark grey
        frame_px = [[frame_color] * 20 for _ in range(20)]
        sprites.append(
            Sprite(pixels=frame_px, name="target_frame", layer=-1)
            .set_position(ox - 1, oy - 1)
        )
        
        for r in range(6):
            for c in range(6):
                color = self.target[r, c]
                px = [[FLOOR_COLOR] * T for _ in range(T)]
                if color != FLOOR_COLOR:
                    px[1][1] = color
                    px[1][2] = color
                    px[2][1] = color
                    px[2][2] = color
                sprites.append(
                    Sprite(pixels=px, name=f"tgt_{c}_{r}", layer=0)
                    .set_position(ox + c * T, oy + r * T)
                )

        # --- Draw pivot dots (1×1 sprites at the corners) ---
        for py in range(-1, 6):
            for px in range(-1, 6):
                is_disabled = (px, py) in self.disabled_pivots
                corners = [(px, py), (px+1, py), (px, py+1), (px+1, py+1)]
                has_locked = any((c, r) in self.locked for c, r in corners if 0 <= c < 6 and 0 <= r < 6)

                # Only draw disabled pivots; omit active indicators
                if is_disabled or has_locked:
                    c = PIVOT_DISABLED
                    sprites.append(
                        Sprite(pixels=[[c]], name=f"pivot_{px}_{py}", layer=1)
                        .set_position(self.BOARD_X + (px + 2) * T, self.BOARD_Y + (py + 2) * T)
                    )

        self.current_level._sprites = sprites

    # ------------------------------------------------------------------ #
    #  Hidden state (for graph builder)                                   #
    # ------------------------------------------------------------------ #

    def _get_hidden_state(self) -> np.ndarray:
        return self.tiles.copy().astype(np.int16)

    # ------------------------------------------------------------------ #
    #  Step                                                               #
    # ------------------------------------------------------------------ #

    def step(self) -> None:
        aid = self.action.id

        if aid == GameAction.ACTION6:
            gx = self.action.data.get("x", -1)
            gy = self.action.data.get("y", -1)

            # Map 64x64 frame coordinates back to CAM_W x CAM_H grid coordinates
            scale = min(64 // self.CAM_W, 64 // self.CAM_H)
            offset_x = (64 - self.CAM_W * scale) // 2
            offset_y = (64 - self.CAM_H * scale) // 2
            
            # play_pygame passes 64x64 coordinates. Map them:
            if offset_x <= gx < offset_x + self.CAM_W * scale and offset_y <= gy < offset_y + self.CAM_H * scale:
                grid_x = (gx - offset_x) // scale
                grid_y = (gy - offset_y) // scale
            else:
                grid_x, grid_y = -1, -1

            best = None
            best_dist = 999
            for cand_py in range(-1, 6):
                for cand_px in range(-1, 6):
                    dot_x = self.BOARD_X + (cand_px + 2) * self.TILE_PX
                    dot_y = self.BOARD_Y + (cand_py + 2) * self.TILE_PX
                    dist = abs(grid_x - dot_x) + abs(grid_y - dot_y)
                    if dist < best_dist:
                        best = (cand_px, cand_py)
                        best_dist = dist

            if best is not None and best_dist <= 3:
                if self._rotate_cw(*best):
                    self.current_steps -= 1

        self._sync_sprites()

        if np.array_equal(self.tiles, self.target):
            self.next_level()
        elif self.current_steps <= 0:
            self.lose()

        self.complete_action()
