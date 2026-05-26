"""Fuse-Burn-Ignite.

Click ignition pads to start burning fuse fronts; ACTION5 advances time one
burn tick. Bombs record the tick they fire, and the level is won only if all
bombs fire within the required synchronisation window. Later levels add bridge
gates that block fire until clicked open; level 3 also adds scissor cells that
can be cut before ignition to force longer routes.
"""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
FLOOR = 11
FUSE = 12
BURNING = 4
BURNED = 5
PAD = 10
BOMB_RING = 15
SCISSOR = 8
CUT = 13
BRIDGE = 9
BRIDGE_OPEN = 10
HUD_FILL = 14
HUD_EMPTY = 5


class RightHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps <= 0:
            return frame
        ratio = max(0.0, min(1.0, self.game.steps_left / self.game.max_steps))
        filled = int(round(frame.shape[0] * ratio))
        x = frame.shape[1] - 1
        for y in range(frame.shape[0]):
            frame[y, x] = HUD_FILL if y >= frame.shape[0] - filled else HUD_EMPTY
        return frame


class Gg17(NovaBaseGame):
    GRID = 12
    CELL = 5
    OX = 2
    OY = 2
    W = 64
    H = 64

    def __init__(self):
        self.hud = RightHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.fuse = set()
        self.graph = {}
        self.pads = {}
        self.bombs = []
        self.scissors = set()
        self.cut = set()
        self.bridges = set()
        self.blocked = set()
        self.burned = {}
        self.burning = set()
        self.turn = 0
        self.tolerance = 0
        self.witness = []
        self.max_steps = 0
        self.steps_left = 0
        super().__init__("gg17", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[5, 6])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        self.fuse = set()
        self.graph = {}
        self.pads = {}
        self.bombs = []
        self.scissors = set()
        self.cut = set()
        self.bridges = set()
        self.blocked = set()
        self.burned = {}
        self.burning = set()
        self.turn = 0
        lvl = level.get_data("Level")
        if lvl == 1:
            self.tolerance = 0
            self._add_path([(3, 3), (4, 3), (5, 3)])
            self._add_path([(3, 8), (4, 8), (5, 8), (6, 8), (7, 8)])
            self.pads = {(2, 3): [(3, 3)], (2, 8): [(3, 8)]}
            self.bombs = [{"pos": (6, 3), "color": 12, "turn": None}, {"pos": (8, 8), "color": 9, "turn": None}]
            self.bridges = {(4, 8)}
            self.blocked = set(self.bridges)
            self.witness = [("bridge", (4, 8)), ("pad", (2, 8)), "tick", "tick", ("pad", (2, 3)), "tick", "tick", "tick"]
        elif lvl == 2:
            self.tolerance = 2
            self._add_path([(2, 5), (3, 5), (4, 5), (5, 4), (6, 3)])
            self._add_path([(4, 5), (5, 6), (6, 7)])
            self._add_path([(2, 9), (3, 9), (4, 9), (5, 9)])
            self._add_path([(8, 2), (8, 3), (8, 4), (8, 5)])
            self.pads = {(1, 5): [(2, 5)], (1, 9): [(2, 9)], (8, 1): [(8, 2)]}
            self.bombs = [
                {"pos": (7, 3), "color": 12, "turn": None}, {"pos": (7, 7), "color": 9, "turn": None},
                {"pos": (6, 9), "color": 14, "turn": None}, {"pos": (8, 6), "color": 15, "turn": None},
            ]
            self.bridges = {(4, 5), (8, 4), (4, 9)}
            self.blocked = set(self.bridges)
            self.witness = [("bridge", (4, 5)), ("bridge", (8, 4)), ("bridge", (4, 9)), ("pad", (1, 5)), "tick", ("pad", (8, 1)), ("pad", (1, 9)), "tick", "tick", "tick", "tick"]
        else:
            self.tolerance = 0
            self._add_path([(2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)])
            self._add_path([(4, 6), (5, 5), (6, 6)])
            self._add_path([(2, 10), (3, 10), (4, 10), (5, 10), (6, 10)])
            self._add_path([(9, 2), (9, 3), (9, 4), (9, 5), (9, 6)])
            self.pads = {(1, 6): [(2, 6)], (1, 10): [(2, 10)], (9, 1): [(9, 2)]}
            self.bombs = [
                {"pos": (8, 6), "color": 12, "turn": None},
                {"pos": (7, 10), "color": 15, "turn": None},
                {"pos": (9, 7), "color": 8, "turn": None},
            ]
            self.bridges = {(4, 6), (6, 6), (9, 4), (4, 10)}
            self.blocked = set(self.bridges)
            self.scissors = {(5, 5)}
            self.witness = [
                ("bridge", (4, 6)), ("bridge", (6, 6)), ("bridge", (9, 4)), ("bridge", (4, 10)), ("cut", (5, 5)),
                ("pad", (1, 6)), "tick", ("pad", (9, 1)), ("pad", (1, 10)),
                "tick", "tick", "tick", "tick", "tick",
            ]
        self.max_steps = len(self.witness)
        self.steps_left = self.max_steps
        self._sync()

    def _add_path(self, cells):
        for cell in cells:
            self.fuse.add(cell)
            self.graph.setdefault(cell, set())
        for a, b in zip(cells, cells[1:]):
            self.graph.setdefault(a, set()).add(b)
            self.graph.setdefault(b, set()).add(a)

    def _grid_at(self, gx, gy):
        if not (self.OX <= gx < self.OX + self.GRID * self.CELL and self.OY <= gy < self.OY + self.GRID * self.CELL):
            return None
        return ((gx - self.OX) // self.CELL, (gy - self.OY) // self.CELL)

    def _cell_pos(self, x, y):
        return self.OX + x * self.CELL, self.OY + y * self.CELL

    def _ignite_pad(self, pos):
        if pos not in self.pads:
            return False
        for cell in self.pads[pos]:
            if cell not in self.cut and cell not in self.burned:
                self.burning.add(cell)
        self.steps_left -= 1
        return True

    def _consume_miss(self, pos):
        if pos is not None:
            self.steps_left -= 1
            return True
        return False

    def _cut_cell(self, pos):
        if pos in self.scissors and pos not in self.burned:
            self.cut.add(pos)
            self.burning.discard(pos)
            self.steps_left -= 1
            return True
        return False

    def _open_bridge(self, pos):
        if pos in self.blocked and pos not in self.burned:
            self.blocked.remove(pos)
            self.steps_left -= 1
            return True
        return False

    def _tick(self):
        self.turn += 1
        frontier = {p for p in self.burning if p not in self.cut and p not in self.blocked}
        next_front = set()
        for p in frontier:
            self.burned[p] = self.turn
        for bomb in self.bombs:
            if bomb["turn"] is None and any(abs(bomb["pos"][0] - x) + abs(bomb["pos"][1] - y) == 1 for x, y in frontier):
                bomb["turn"] = self.turn
        for p in frontier:
            for nxt in self.graph.get(p, ()):
                if nxt not in self.cut and nxt not in self.blocked and nxt not in self.burned:
                    next_front.add(nxt)
        self.burning = next_front
        self.steps_left -= 1

    def _check_win(self):
        turns = [b["turn"] for b in self.bombs]
        if any(t is None for t in turns):
            return False
        return max(turns) - min(turns) <= self.tolerance

    def _tile_pixels(self, color):
        px = [[color] * self.CELL for _ in range(self.CELL)]
        if color == FLOOR:
            px[1][1] = 12
            px[3][3] = 12
        return px

    def _fuse_pixels(self, color, junction=False):
        px = [[-1] * self.CELL for _ in range(self.CELL)]
        for i in range(self.CELL):
            px[2][i] = color
            px[i][2] = color
        if junction:
            px[2][2] = PAD
        return px

    def _bomb_pixels(self, bomb):
        color = bomb["color"] if bomb["turn"] is not None else BOMB_RING
        px = [[-1] * self.CELL for _ in range(self.CELL)]
        for i in range(self.CELL):
            px[0][i] = px[4][i] = px[i][0] = px[i][4] = color
        if bomb["turn"] is not None:
            for y in range(1, 4):
                for x in range(1, 4):
                    px[y][x] = color
        return px

    def _sync(self):
        sprites = [Sprite([[BG] * self.W for _ in range(self.H)], "bg", layer=-2).set_position(0, 0)]
        for y in range(self.GRID):
            for x in range(self.GRID):
                sprites.append(Sprite(self._tile_pixels(FLOOR), f"floor_{x}_{y}", layer=-1).set_position(*self._cell_pos(x, y)))
        for p in self.fuse:
            color = CUT if p in self.cut else BURNING if p in self.burning else BURNED if p in self.burned else FUSE
            sprites.append(Sprite(self._fuse_pixels(color, len(self.graph.get(p, ())) >= 3), f"fuse_{p}", layer=1).set_position(*self._cell_pos(*p)))
        for p in self.scissors:
            if p not in self.cut:
                sprites.append(Sprite([[SCISSOR]], f"scissor_{p}", layer=3).set_position(self._cell_pos(*p)[0] + 2, self._cell_pos(*p)[1] + 2))
        for p in self.bridges:
            color = BRIDGE if p in self.blocked else BRIDGE_OPEN
            sprites.append(Sprite([[color, color, color], [color, BG, color], [color, color, color]], f"bridge_{p}", layer=3).set_position(self._cell_pos(*p)[0] + 1, self._cell_pos(*p)[1] + 1))
        for p in self.pads:
            sprites.append(Sprite([[-1, PAD, -1, PAD, -1], [PAD, PAD, PAD, PAD, PAD], [-1, PAD, FUSE, PAD, -1], [PAD, PAD, PAD, PAD, PAD], [-1, PAD, -1, PAD, -1]], f"pad_{p}", layer=3).set_position(*self._cell_pos(*p)))
        for bomb in self.bombs:
            sprites.append(Sprite(self._bomb_pixels(bomb), f"bomb_{bomb['pos']}", layer=4).set_position(*self._cell_pos(*bomb["pos"])))
        for i, bomb in enumerate([b for b in self.bombs if b["turn"] is not None]):
            x = 4 + i * 3
            sprites.append(Sprite([[bomb["color"], bomb["color"]], [-1, bomb["color"]]], f"fire_mark_{i}", layer=5).set_position(x, 61))
        self.current_level._sprites = sprites

    def step(self):
        if self.steps_left > 0:
            if self.action.id == GameAction.ACTION5:
                self._tick()
            elif self.action.id == GameAction.ACTION6:
                grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
                cell = self._grid_at(*grid) if grid is not None else None
                if cell is not None and not self._cut_cell(cell) and not self._open_bridge(cell) and not self._ignite_pad(cell):
                    self._consume_miss(cell)
        self._sync()
        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        arr = np.zeros((self.GRID, self.GRID), dtype=np.int16)
        for x, y in self.fuse:
            arr[y, x] = 1
        for x, y in self.burning:
            arr[y, x] = 2
        return arr
