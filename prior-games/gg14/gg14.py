"""Kiln-Mosaic-Stamp.

Click stamp handles to select a coloured stencil, then click the clay board to
place that stencil with its origin at the clicked cell. Empty clay takes the
stamp colour; differently coloured clay fuses into a third colour. Later
levels include a scraper stamp that clears selected cells before the final
colour is pressed. The target mosaic on the right shows the exact required
fused pattern.
"""

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
KILN = 12
CLAY = 11
FRAME = 5
STAMP_BODY = 13
SCRAPER = 10
HUD_FILL = 7
HUD_EMPTY = 5

RED = 2
BLUE = 1
GREEN = 3
YELLOW = 4
ORANGE = 7
PURPLE = 6
CYAN = 8
MAROON = 9
WHITE = 14

MIX = {
    frozenset((RED, BLUE)): PURPLE,
    frozenset((RED, YELLOW)): ORANGE,
    frozenset((RED, GREEN)): WHITE,
    frozenset((BLUE, GREEN)): CYAN,
    frozenset((BLUE, YELLOW)): CYAN,
    frozenset((GREEN, YELLOW)): SCRAPER,
    frozenset((PURPLE, YELLOW)): MAROON,
    frozenset((CYAN, RED)): WHITE,
    frozenset((ORANGE, BLUE)): MAROON,
}


class StepHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps <= 0:
            return frame
        filled = int(round(frame.shape[1] * self.game.steps_left / self.game.max_steps))
        for x in range(frame.shape[1]):
            frame[0, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


class Gg14(NovaBaseGame):
    WIDTH = 64
    HEIGHT = 48
    CELL = 4
    BOARD_X = 3
    BOARD_Y = 5
    TARGET_X = 36
    TARGET_Y = 5
    BUTTON_Y = 35

    def __init__(self):
        self.hud = StepHud(self)
        levels = [Level(grid_size=(self.WIDTH, self.HEIGHT), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.n = 4
        self.board = np.zeros((4, 4), dtype=int)
        self.target = np.zeros((4, 4), dtype=int)
        self.stamps = []
        self.witness = []
        self.selected_stamp = 0
        self.last_stamp = None
        self.last_cells = set()
        self.max_steps = 0
        self.steps_left = 0
        super().__init__("gg14", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[6])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.WIDTH
        self.camera.height = self.HEIGHT
        self.current_level._grid_size = (self.WIDTH, self.HEIGHT)
        lvl = level.get_data("Level")
        if lvl == 1:
            self.n = 4
            self.stamps = [
                self._stamp([(0, 0), (1, 0), (0, 1)], RED, 5, "corner_red"),
                self._stamp([(0, 0), (0, 1), (0, 2)], BLUE, 17, "line_blue"),
                self._stamp([(0, 0), (1, 0)], YELLOW, 29, "dash_yellow"),
            ]
            self.witness = [(0, (0, 0)), (1, (3, 0)), (0, (1, 2)), (2, (2, 3))]
        elif lvl == 2:
            self.n = 5
            self.stamps = [
                self._stamp([(0, 0), (1, 0), (1, 1)], RED, 4, "bend_red"),
                self._stamp([(0, 0), (1, 0), (2, 0)], BLUE, 14, "bar_blue"),
                self._stamp([(0, 0), (0, 1), (1, 1)], GREEN, 24, "hook_green"),
                self._stamp([(0, 0), (1, 0), (0, 1)], YELLOW, 34, "corner_yellow"),
            ]
            self.witness = [(0, (0, 0)), (1, (1, 0)), (2, (3, 1)), (0, (1, 2)), (3, (2, 3)), (1, (0, 4))]
        else:
            self.n = 6
            self.stamps = [
                self._stamp([(0, 0), (1, 0), (1, 1), (2, 1)], RED, 3, "step_red"),
                self._stamp([(0, 0), (0, 1), (0, 2), (0, 3)], BLUE, 13, "rail_blue"),
                self._stamp([(0, 0), (1, 0), (2, 0), (3, 0)], YELLOW, 23, "rail_yellow"),
                self._stamp([(0, 0), (0, 1), (1, 1), (1, 2)], GREEN, 33, "hook_green"),
                self._stamp([(0, 0), (1, 0), (0, 1)], SCRAPER, 43, "scrape", mode="clear"),
                self._stamp([(0, 0), (1, 0), (0, 1), (1, 1)], ORANGE, 53, "seal_orange"),
            ]
            self.witness = [(0, (0, 0)), (1, (4, 0)), (2, (1, 3)), (3, (3, 2)), (0, (2, 1)), (4, (3, 3)), (5, (3, 3)), (1, (0, 2))]
        self.board = np.zeros((self.n, self.n), dtype=int)
        self.target = self._simulate(self.witness)
        self.board = np.zeros((self.n, self.n), dtype=int)
        self.max_steps = len(self.witness)
        self.steps_left = self.max_steps
        self.selected_stamp = 0
        self.last_stamp = None
        self.last_cells = set()
        self._sync()

    def _stamp(self, cells, color, x, name, mode="paint"):
        return {"cells": cells, "color": color, "button": (x, self.BUTTON_Y), "name": name, "mode": mode}

    def _fuse(self, old, new):
        if old == 0 or old == new:
            return new
        return MIX.get(frozenset((int(old), int(new))), new)

    def _apply_stamp(self, idx, origin=(0, 0), consume=True):
        stamp = self.stamps[idx]
        ox, oy = origin
        touched = set()
        for x, y in stamp["cells"]:
            bx, by = ox + x, oy + y
            if 0 <= bx < self.n and 0 <= by < self.n:
                touched.add((bx, by))
                if stamp["mode"] == "clear":
                    self.board[by, bx] = 0
                else:
                    self.board[by, bx] = self._fuse(self.board[by, bx], stamp["color"])
        self.last_stamp = idx
        self.last_cells = touched
        if consume:
            self.steps_left -= 1

    def _simulate(self, sequence):
        saved = self.board.copy()
        saved_last = (self.last_stamp, set(self.last_cells))
        self.board = np.zeros((self.n, self.n), dtype=int)
        for idx, origin in sequence:
            self._apply_stamp(idx, origin, consume=False)
        result = self.board.copy()
        self.board = saved
        self.last_stamp, self.last_cells = saved_last
        return result

    def _stamp_at(self, gx, gy):
        for i, stamp in enumerate(self.stamps):
            bx, by = stamp["button"]
            if bx <= gx < bx + 7 and by <= gy < by + 7:
                return i
        return None

    def _board_cell_at(self, gx, gy):
        if not (self.BOARD_X <= gx < self.BOARD_X + self.n * self.CELL):
            return None
        if not (self.BOARD_Y <= gy < self.BOARD_Y + self.n * self.CELL):
            return None
        return ((gx - self.BOARD_X) // self.CELL, (gy - self.BOARD_Y) // self.CELL)

    def _cell_to_pixel(self, origin_x, origin_y, x, y):
        return origin_x + x * self.CELL, origin_y + y * self.CELL

    def _tile_pixels(self, color, active=False):
        fill = CLAY if color == 0 else int(color)
        edge = WHITE if active else FRAME
        return [
            [edge, edge, edge, edge],
            [edge, fill, fill, edge],
            [edge, fill, fill, edge],
            [edge, edge, edge, edge],
        ]

    def _button_pixels(self, stamp, active):
        color = stamp["color"]
        body = SCRAPER if stamp["mode"] == "clear" else STAMP_BODY
        edge = WHITE if active else FRAME
        px = [[edge] * 7 for _ in range(7)]
        for y in range(1, 6):
            for x in range(1, 6):
                px[y][x] = body
        for x, y in stamp["cells"]:
            sx = 1 + min(4, max(0, x))
            sy = 1 + min(4, max(0, y))
            px[sy][sx] = BG if stamp["mode"] == "clear" else color
        return px

    def _panel_pixels(self, w, h, color):
        px = [[FRAME] * w for _ in range(h)]
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                px[y][x] = color
        return px

    def _sync(self):
        sprites = [Sprite([[KILN] * self.WIDTH for _ in range(self.HEIGHT)], "kiln", layer=0).set_position(0, 0)]
        panel_size = self.n * self.CELL + 2
        sprites.append(Sprite(self._panel_pixels(panel_size, panel_size, CLAY), "board_panel", layer=1).set_position(self.BOARD_X - 1, self.BOARD_Y - 1))
        sprites.append(Sprite(self._panel_pixels(panel_size, panel_size, CLAY), "target_panel", layer=1).set_position(self.TARGET_X - 1, self.TARGET_Y - 1))

        active_cells = set(self.last_cells)

        for y in range(self.n):
            for x in range(self.n):
                px, py = self._cell_to_pixel(self.BOARD_X, self.BOARD_Y, x, y)
                sprites.append(Sprite(self._tile_pixels(self.board[y, x], (x, y) in active_cells), f"board_{x}_{y}", layer=2).set_position(px, py))
                tx, ty = self._cell_to_pixel(self.TARGET_X, self.TARGET_Y, x, y)
                sprites.append(Sprite(self._tile_pixels(self.target[y, x]), f"target_{x}_{y}", layer=2).set_position(tx, ty))

        for i, stamp in enumerate(self.stamps):
            bx, by = stamp["button"]
            sprites.append(Sprite(self._button_pixels(stamp, i == self.selected_stamp), f"stamp_{stamp['name']}", layer=4).set_position(bx, by))

        self.current_level._sprites = sprites

    def step(self):
        if self.action.id == GameAction.ACTION6 and self.steps_left > 0:
            grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
            if grid is not None:
                idx = self._stamp_at(*grid)
                cell = self._board_cell_at(*grid)
                if idx is not None:
                    self.selected_stamp = idx
                elif cell is not None:
                    self._apply_stamp(self.selected_stamp, cell)
        self._sync()
        if np.array_equal(self.board, self.target):
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        return np.stack([self.board, self.target]).astype(np.int16)
