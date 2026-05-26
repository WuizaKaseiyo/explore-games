"""Row-Flip-Mirror.

The player clicks edge buttons to reverse (mirror) a full row or column of
coloured tiles.  A framed target grid is shown beside the board.

Levels scale in grid size, anchor count, disabled buttons, and scramble depth:
  L1 — 3×3, no anchors, no disabled buttons, 2-step hand-authored scramble
  L2 — 5×5, 2 anchors, no disabled buttons, 9-step scramble
  L3 — 6×6, 3 anchors, 2 disabled buttons, 17-step scramble

Each level uses a unique colour palette for visual diversity.
"""

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite

# Nova palette constants
BG = 0
BUTTON_COLOR = 10      # light grey — active button
DISABLED_COLOR = 5     # dark grey — disabled button
ANCHOR_COLOR = 6       # magenta — anchor overlay
FRAME_COLOR = 5        # dark grey — target frame
TARGET_BACKDROP = 12   # pale grey/blue target paper
BOARD_BACKDROP = 13    # lavender board paper

# Per-level colour palettes (4–6 colours each, all valid Nova colours 1-14)
PALETTES = [
    [1, 2, 3, 7],                # L1: blue, red, green, orange
    [4, 8, 9, 3, 14],            # L2: yellow, cyan, maroon, green, grey
    [2, 7, 4, 9, 1, 8],          # L3: red, orange, yellow, maroon, blue, cyan
]


class StepHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps:
            filled = int(frame.shape[1] * self.game.steps_left / self.game.max_steps)
            for x in range(frame.shape[1]):
                frame[0, x] = 6 if x < filled else 1
        return frame


class Gg08(NovaBaseGame):
    """Row-Flip-Mirror game with scaling difficulty."""

    T = 3  # pixels per tile side

    def __init__(self):
        self.hud = StepHud(self)
        camera = Camera(background=BG, letter_box=BG, interfaces=[self.hud])
        levels = [
            Level(grid_size=(1, 1), sprites=[], data={"Level": 1}),
            Level(grid_size=(1, 1), sprites=[], data={"Level": 2}),
            Level(grid_size=(1, 1), sprites=[], data={"Level": 3}),
        ]
        self.N = 4
        self.tiles = np.zeros((4, 4), dtype=int)
        self.target = np.zeros((4, 4), dtype=int)
        self.anchors = set()
        self.disabled = set()
        self.palette = PALETTES[0]
        self.max_steps = 0
        self.steps_left = 0
        self.witness = []  # scramble sequence (for testing)
        super().__init__("gg08", levels, camera, available_actions=[6])

    # ------------------------------------------------------------------ #
    #  Layout helpers                                                      #
    # ------------------------------------------------------------------ #

    def _layout(self):
        """Compute layout constants based on current grid size N."""
        T = self.T
        board_px = self.N * T
        gap = 2
        target_px = self.N * T
        # +1 col for row buttons on left, +1 row for col buttons on top
        # board starts at x=T (after button column), y=T+1 (after HUD + button row)
        self.btn_col_y = 1                    # y of the column-button row (just below HUD)
        self.btn_row_x = 0                    # x of the row-button column
        self.board_x = T                      # board starts after button column
        self.board_y = T + 1                  # board starts after HUD row + button row
        self.target_x = self.board_x + board_px + gap  # target x (after gap)
        self.target_y = self.board_y          # target y (aligned with board)
        # frame around target: 1px border on all sides
        self.frame_x = self.target_x - 1
        self.frame_y = self.target_y - 1
        self.frame_w = target_px + 2
        self.frame_h = board_px + 2
        # camera dimensions
        cam_w = self.target_x + target_px + 1  # +1 for right frame border
        cam_h = self.board_y + board_px + 1     # +1 for bottom frame border
        return cam_w, cam_h

    # ------------------------------------------------------------------ #
    #  Level setup                                                         #
    # ------------------------------------------------------------------ #

    def on_set_level(self, level: Level) -> None:
        lvl = level.get_data("Level")
        if lvl == 1:
            self.N = 3
            self.palette = PALETTES[0]
            self.anchors = set()
            self.disabled = set()
            scramble_depth = 0
            self.max_steps = 6
        elif lvl == 2:
            self.N = 5
            self.palette = PALETTES[1]
            self.anchors = {(1, 1), (3, 3)}
            self.disabled = set()
            scramble_depth = 9
            self.max_steps = 24
        else:
            self.N = 6
            self.palette = PALETTES[2]
            self.anchors = {(1, 1), (4, 4), (2, 3)}
            self.disabled = {("row", 2), ("col", 1)}
            scramble_depth = 17
            self.max_steps = 44

        cam_w, cam_h = self._layout()
        self.camera.width = cam_w
        self.camera.height = cam_h
        self.current_level._grid_size = (cam_w, cam_h)

        if lvl == 1:
            # A small asymmetric target makes the first lesson readable: one
            # row reversal and one column reversal visibly repair the board.
            self.target = np.array([
                [1, 2, 3],
                [7, 1, 2],
                [3, 7, 1],
            ], dtype=int)
        else:
            n_colors = len(self.palette)
            self.target = np.array(
                [[self.palette[(r * 2 + c) % n_colors] for c in range(self.N)]
                 for r in range(self.N)], dtype=int
            )
        self.tiles = self.target.copy()

        if lvl == 1:
            self.witness = [("row", 0), ("col", 2)]
        else:
            # Generate scramble: pick random valid (axis, idx) pairs.
            rng = np.random.RandomState(42 + lvl)
            self.witness = []
            for _ in range(scramble_depth):
                while True:
                    axis = rng.choice(["row", "col"])
                    idx = int(rng.randint(0, self.N))
                    if (axis, idx) not in self.disabled and (not self.witness or self.witness[-1] != (axis, idx)):
                        break
                self.witness.append((axis, idx))

        # Apply scramble in reverse to create start state
        for axis, idx in reversed(self.witness):
            self._flip(axis, idx, consume=False)

        self.steps_left = self.max_steps
        self._sync()

    # ------------------------------------------------------------------ #
    #  Core mechanics                                                      #
    # ------------------------------------------------------------------ #

    def _flip(self, axis: str, idx: int, consume: bool = True) -> bool:
        """Reverse (mirror) a row or column, skipping anchors."""
        if (axis, idx) in self.disabled:
            return False
        if axis == "row":
            positions = [(idx, c) for c in range(self.N) if (c, idx) not in self.anchors]
        else:
            positions = [(r, idx) for r in range(self.N) if (idx, r) not in self.anchors]
        vals = [self.tiles[r, c] for r, c in positions][::-1]
        for (r, c), val in zip(positions, vals):
            self.tiles[r, c] = val
        if consume:
            self.steps_left -= 1
        return True

    def _button_at(self, gx: int, gy: int):
        """Return (axis, idx) if click is on a button, else None."""
        T = self.T
        # Row buttons: left column, within button area
        if gx < T and self.board_y <= gy < self.board_y + self.N * T:
            row_idx = (gy - self.board_y) // T
            if 0 <= row_idx < self.N:
                return ("row", row_idx)
        # Column buttons: top row, within button area
        if gy >= self.btn_col_y and gy < self.btn_col_y + T and self.board_x <= gx < self.board_x + self.N * T:
            col_idx = (gx - self.board_x) // T
            if 0 <= col_idx < self.N:
                return ("col", col_idx)
        return None

    # ------------------------------------------------------------------ #
    #  Rendering                                                           #
    # ------------------------------------------------------------------ #

    def _sync(self):
        sprites = []
        T = self.T
        board_w = self.N * T

        # Subtle paper backdrops keep the two grids readable without adding noise.
        sprites.append(
            Sprite([[BOARD_BACKDROP] * (board_w + 2) for _ in range(board_w + 2)], "board_backdrop", layer=0)
            .set_position(self.board_x - 1, self.board_y - 1)
        )
        sprites.append(
            Sprite([[TARGET_BACKDROP] * (board_w + 2) for _ in range(board_w + 2)], "target_backdrop", layer=0)
            .set_position(self.frame_x, self.frame_y)
        )

        # --- Row buttons (left column) ---
        for r in range(self.N):
            is_dis = ("row", r) in self.disabled
            col = DISABLED_COLOR if is_dis else BUTTON_COLOR
            # Draw T×T button block
            px = [[col] * T for _ in range(T)]
            if is_dis:
                # X mark on disabled
                px[0][0] = BG
                px[0][T-1] = BG
                px[T-1][0] = BG
                px[T-1][T-1] = BG
            else:
                # Arrow indicator: right-pointing triangle
                px[0][T-1] = BG
                px[T-1][T-1] = BG
            sprites.append(
                Sprite(pixels=px, name=f"row_btn_{r}", layer=2)
                .set_position(self.btn_row_x, self.board_y + r * T)
            )

        # --- Column buttons (top row) ---
        for c in range(self.N):
            is_dis = ("col", c) in self.disabled
            col = DISABLED_COLOR if is_dis else BUTTON_COLOR
            px = [[col] * T for _ in range(T)]
            if is_dis:
                px[0][0] = BG
                px[0][T-1] = BG
                px[T-1][0] = BG
                px[T-1][T-1] = BG
            else:
                # Arrow indicator: down-pointing triangle
                px[T-1][0] = BG
                px[T-1][T-1] = BG
            sprites.append(
                Sprite(pixels=px, name=f"col_btn_{c}", layer=2)
                .set_position(self.board_x + c * T, self.btn_col_y)
            )

        # --- Board tiles ---
        for r in range(self.N):
            for c in range(self.N):
                color = int(self.tiles[r, c])
                px = [[BOARD_BACKDROP] * T for _ in range(T)]
                if color != BG:
                    px[1][1] = color
                    px[1][2] = color
                    px[2][1] = color
                    px[2][2] = color
                # Anchor overlay
                if (c, r) in self.anchors:
                    for i in range(T):
                        px[0][i] = ANCHOR_COLOR
                        px[i][0] = ANCHOR_COLOR
                        px[i][T-1] = ANCHOR_COLOR
                        px[T-1][i] = ANCHOR_COLOR
                sprites.append(
                    Sprite(pixels=px, name=f"tile_{c}_{r}", layer=1)
                    .set_position(self.board_x + c * T, self.board_y + r * T)
                )

        # --- Target frame ---
        frame_px = [[FRAME_COLOR] * self.frame_w for _ in range(self.frame_h)]
        # Hollow out the interior
        for fy in range(1, self.frame_h - 1):
            for fx in range(1, self.frame_w - 1):
                frame_px[fy][fx] = TARGET_BACKDROP
        sprites.append(
            Sprite(pixels=frame_px, name="target_frame", layer=0)
            .set_position(self.frame_x, self.frame_y)
        )

        # --- Target tiles ---
        for r in range(self.N):
            for c in range(self.N):
                color = int(self.target[r, c])
                px = [[TARGET_BACKDROP] * T for _ in range(T)]
                if color != BG:
                    px[1][1] = color
                    px[1][2] = color
                    px[2][1] = color
                    px[2][2] = color
                sprites.append(
                    Sprite(pixels=px, name=f"tgt_{c}_{r}", layer=1)
                    .set_position(self.target_x + c * T, self.target_y + r * T)
                )

        self.current_level._sprites = sprites

    # ------------------------------------------------------------------ #
    #  Game loop                                                           #
    # ------------------------------------------------------------------ #

    def step(self) -> None:
        if self.action.id == GameAction.ACTION6:
            grid = self.camera.display_to_grid(
                self.action.data.get("x", -1),
                self.action.data.get("y", -1),
            )
            if grid is not None:
                button = self._button_at(*grid)
                if button is not None:
                    self._flip(*button)
        self._sync()
        if np.array_equal(self.tiles, self.target):
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return self.tiles.astype(np.int16)
