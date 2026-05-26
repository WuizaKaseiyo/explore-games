"""Flashlight-Key-Maze.

Hidden-information maze.  Arrow keys move an avatar and set the flashlight
facing.  ACTION5 picks up a key on the current cell, or drops the oldest
carried key when the backpack is full/wrong.  Locked doors consume a matching
carried key when the player moves into them; the exit wins the level.
"""

from __future__ import annotations

from collections import Counter
import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
FOG = 5
MEMORY = 13
FLOOR = 11
LIGHT = 10
WALL = 7
WALL_LIT = 15
PLAYER = 8
EXIT = 14
HUD = 14
EMPTY_SLOT = 5
OPEN_DOOR = 11

N, E, S, W = 0, 1, 2, 3
DIRS = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
ACTION_DIR = {
    GameAction.ACTION1: N,
    GameAction.ACTION2: S,
    GameAction.ACTION3: W,
    GameAction.ACTION4: E,
}
KEY_COLORS = {"r": 12, "b": 9, "y": 10, "g": 14}
DOOR_TO_KEY = {"R": "r", "B": "b", "Y": "y", "G": "g"}


class TopHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if not self.game.max_steps:
            return frame
        filled = int(round(frame.shape[1] * max(0, self.game.steps_left) / self.game.max_steps))
        for x in range(frame.shape[1]):
            frame[0, x] = HUD if x < filled else EMPTY_SLOT
        return frame


class Gg21(NovaBaseGame):
    W = 64
    H = 64
    CELL = 4
    OX = 2
    OY = 3
    BW = 15
    BH = 15

    def __init__(self):
        self.hud = TopHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.walls = set()
        self.doors = {}
        self.open_doors = set()
        self.keys = {}
        self.exit = (13, 13)
        self.player = (1, 1)
        self.facing = E
        self.seen = set()
        self.lit = set()
        self.backpack = []
        self.capacity = 1
        self.light_range = 4
        self.max_steps = 0
        self.steps_left = 0
        super().__init__("gg21", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[1, 2, 3, 4, 5])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        lvl = level.get_data("Level")
        self.walls = self._border()
        self.doors = {}
        self.open_doors = set()
        self.keys = {}
        self.backpack = []
        self.seen = set()
        self.facing = E
        if lvl == 1:
            self.player = (1, 1)
            self.exit = (13, 13)
            self.capacity = 1
            self.light_range = 4
            self.max_steps = 80
            self._wall_v(5, 1, 11, gaps={10})
            self._wall_v(10, 3, 13, gaps={8})
            self._wall_h(4, 2, 9, gaps={4})
            self._wall_h(12, 3, 12, gaps={11})
            self.doors[(10, 8)] = "R"
            self.keys[(3, 10)] = "r"
        elif lvl == 2:
            self.player = (1, 1)
            self.exit = (13, 13)
            self.capacity = 1
            self.light_range = 4
            self.max_steps = 110
            self._wall_v(6, 1, 13, gaps={7})
            self._wall_v(11, 3, 13, gaps={12})
            self._wall_h(5, 2, 10, gaps={3, 8})
            self._wall_h(10, 7, 13, gaps={9})
            self._wall_h(2, 8, 13, gaps={10})
            self.doors[(6, 7)] = "R"
            self.doors[(11, 12)] = "B"
            self.keys[(2, 12)] = "r"
            self.keys[(10, 2)] = "b"
        else:
            self.player = (1, 1)
            self.exit = (13, 13)
            self.capacity = 2
            self.light_range = 5
            self.max_steps = 150
            self._wall_v(4, 1, 13, gaps={4})
            self._wall_v(8, 2, 13, gaps={9})
            self._wall_v(11, 1, 13, gaps={12})
            self._wall_h(7, 4, 11, gaps={6})
            self._wall_h(3, 8, 13, gaps={10})
            self._wall_h(11, 1, 10, gaps={5, 10})
            self.doors[(4, 4)] = "R"
            self.doors[(8, 9)] = "B"
            self.doors[(11, 12)] = "G"
            self.keys[(2, 10)] = "r"
            self.keys[(6, 3)] = "b"
            self.keys[(10, 10)] = "g"
            self.keys[(2, 2)] = "y"
        self.steps_left = self.max_steps
        self._refresh_light()
        self._sync()

    def _border(self):
        return {
            (x, y)
            for y in range(self.BH)
            for x in range(self.BW)
            if x == 0 or y == 0 or x == self.BW - 1 or y == self.BH - 1
        }

    def _wall_v(self, x, y0, y1, gaps=frozenset()):
        for y in range(y0, y1 + 1):
            if y not in gaps:
                self.walls.add((x, y))

    def _wall_h(self, y, x0, x1, gaps=frozenset()):
        for x in range(x0, x1 + 1):
            if x not in gaps:
                self.walls.add((x, y))

    def _cell_px(self, cell):
        x, y = cell
        return self.OX + x * self.CELL, self.OY + y * self.CELL

    def _refresh_light(self):
        lit = {self.player}
        px, py = self.player
        dx, dy = DIRS[self.facing]
        for dist in range(1, self.light_range + 1):
            for spread in range(-(dist // 2), dist // 2 + 1):
                if self.facing in (N, S):
                    cell = (px + spread, py + dy * dist)
                else:
                    cell = (px + dx * dist, py + spread)
                if not (0 <= cell[0] < self.BW and 0 <= cell[1] < self.BH):
                    continue
                lit.add(cell)
            front = (px + dx * dist, py + dy * dist)
            if front in self.walls or (front in self.doors and front not in self.open_doors):
                break
        self.lit = lit
        self.seen |= lit

    def _try_move(self, direction):
        self.facing = direction
        dx, dy = DIRS[direction]
        target = (self.player[0] + dx, self.player[1] + dy)
        if target in self.walls:
            self.steps_left -= 1
            self._refresh_light()
            return
        if target in self.doors and target not in self.open_doors:
            needed = DOOR_TO_KEY[self.doors[target]]
            if needed in self.backpack:
                self.backpack.remove(needed)
                self.open_doors.add(target)
                self.player = target
            self.steps_left -= 1
            self._refresh_light()
            return
        self.player = target
        self.steps_left -= 1
        self._refresh_light()

    def _use_pack(self):
        if self.player in self.keys and len(self.backpack) < self.capacity:
            self.backpack.append(self.keys.pop(self.player))
        elif self.player not in self.keys and self.backpack:
            self.keys[self.player] = self.backpack.pop(0)
        self.steps_left -= 1
        self._refresh_light()

    def _check_win(self):
        return self.player == self.exit

    def _put(self, canvas, x, y, color):
        if 0 <= x < self.W and 0 <= y < self.H:
            canvas[y][x] = color

    def _rect(self, canvas, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._put(canvas, xx, yy, color)

    def _draw_cell_base(self, canvas, cell):
        x0, y0 = self._cell_px(cell)
        if cell in self.lit:
            color = LIGHT
        elif cell in self.seen:
            color = MEMORY
        else:
            color = FOG if (cell[0] * 3 + cell[1]) % 5 else BG
        self._rect(canvas, x0, y0, self.CELL, self.CELL, color)

    def _draw_wall(self, canvas, cell, lit):
        x0, y0 = self._cell_px(cell)
        self._rect(canvas, x0, y0, self.CELL, self.CELL, WALL_LIT if lit else WALL)
        canvas[y0][x0] = BG
        canvas[y0 + 3][x0 + 3] = BG

    def _draw_key(self, canvas, cell, key):
        x0, y0 = self._cell_px(cell)
        color = KEY_COLORS[key]
        self._rect(canvas, x0 + 1, y0 + 1, 2, 2, color)
        canvas[y0 + 1][x0 + 3] = color
        canvas[y0 + 2][x0 + 3] = WALL

    def _draw_door(self, canvas, cell, door):
        x0, y0 = self._cell_px(cell)
        color = OPEN_DOOR if cell in self.open_doors else KEY_COLORS[DOOR_TO_KEY[door]]
        self._rect(canvas, x0, y0, self.CELL, self.CELL, color)
        canvas[y0 + 1][x0 + 1] = WALL
        canvas[y0 + 1][x0 + 2] = WALL
        if cell not in self.open_doors:
            canvas[y0 + 2][x0 + 1] = WALL

    def _draw_exit(self, canvas):
        if self.exit not in self.seen:
            return
        x0, y0 = self._cell_px(self.exit)
        self._rect(canvas, x0, y0, self.CELL, self.CELL, EXIT if self.exit in self.lit else MEMORY)
        canvas[y0 + 1][x0 + 1] = BG
        canvas[y0 + 2][x0 + 2] = BG

    def _draw_player(self, canvas):
        x0, y0 = self._cell_px(self.player)
        self._rect(canvas, x0 + 1, y0 + 1, 2, 2, PLAYER)
        tip = {
            N: (x0 + 1, y0),
            S: (x0 + 2, y0 + 3),
            W: (x0, y0 + 1),
            E: (x0 + 3, y0 + 2),
        }[self.facing]
        self._put(canvas, tip[0], tip[1], HUD)

    def _draw_backpack(self, canvas):
        for i in range(self.capacity):
            x = 3 + i * 5
            self._rect(canvas, x, 1, 4, 2, EMPTY_SLOT)
            if i < len(self.backpack):
                self._rect(canvas, x + 1, 1, 2, 2, KEY_COLORS[self.backpack[i]])
        x = 17
        for color, count in Counter(self.doors[p] for p in self.doors if p not in self.open_doors and p in self.seen).items():
            key = DOOR_TO_KEY[color]
            self._rect(canvas, x, 1, min(count, 3), 2, KEY_COLORS[key])
            x += 5

    def _sync(self):
        canvas = [[BG for _ in range(self.W)] for _ in range(self.H)]
        for y in range(self.BH):
            for x in range(self.BW):
                self._draw_cell_base(canvas, (x, y))
        for wall in self.walls:
            if wall in self.seen:
                self._draw_wall(canvas, wall, wall in self.lit)
        for cell, door in self.doors.items():
            if cell in self.seen:
                self._draw_door(canvas, cell, door)
        for cell, key in self.keys.items():
            if cell in self.seen:
                self._draw_key(canvas, cell, key)
        self._draw_exit(canvas)
        self._draw_player(canvas)
        self._draw_backpack(canvas)
        self.current_level._sprites = [Sprite(canvas, "scene", layer=0).set_position(0, 0)]

    def step(self):
        if self.steps_left > 0:
            if self.action.id in ACTION_DIR:
                self._try_move(ACTION_DIR[self.action.id])
            elif self.action.id == GameAction.ACTION5:
                self._use_pack()
        self._sync()
        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        arr = np.zeros((self.BH, self.BW), dtype=np.int16)
        for x, y in self.walls:
            arr[y, x] = 1
        for (x, y), door in self.doors.items():
            arr[y, x] = KEY_COLORS[DOOR_TO_KEY[door]] + (20 if (x, y) in self.open_doors else 0)
        for (x, y), key in self.keys.items():
            arr[y, x] = KEY_COLORS[key]
        arr[self.player[1], self.player[0]] = PLAYER
        return arr
