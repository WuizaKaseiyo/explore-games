"""Wavefront-Ring-Expand.

Click an empty cell to emit a Chebyshev-distance wave. ACTION5 advances all
active waves by one radius; switches touched by the current ring toggle. Later
levels limit reach, add echo lenses that re-emit waves when struck, and add
one-shot switches that ignore later hits.
"""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
FLOOR = 12
WALL = 5
EMITTER = 15
WAVE = 11
SW_OFF = 13
SW_ON = 14
SW_TARGET = 8
ONE_SHOT = 6
ECHO = 9
HUD_FILL = 9
HUD_EMPTY = 5


class BottomHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps <= 0:
            return frame
        ratio = max(0.0, min(1.0, self.game.steps_left / self.game.max_steps))
        filled = int(round(frame.shape[1] * ratio))
        y = frame.shape[0] - 1
        for x in range(frame.shape[1]):
            frame[y, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


class Gg16(NovaBaseGame):
    GRID = 12
    CELL = 5
    OX = 2
    OY = 2
    W = 64
    H = 64

    def __init__(self):
        self.hud = BottomHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.switches = []
        self.walls = set()
        self.waves = []
        self.echoes = {}
        self.emitter = (1, 1)
        self.reach = 4
        self.witness = []
        self.max_steps = 0
        self.steps_left = 0
        super().__init__("gg16", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[5, 6])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        self.walls = set()
        self.waves = []
        self.echoes = {}
        self.emitter = (1, 1)
        lvl = level.get_data("Level")
        if lvl == 1:
            self.reach = 3
            self.switches = [
                {"pos": (3, 3), "state": False, "target": True, "single": False, "hits": 0},
                {"pos": (7, 3), "state": False, "target": True, "single": False, "hits": 0},
                {"pos": (7, 7), "state": False, "target": True, "single": False, "hits": 0},
            ]
            self.witness = [("emit", (5, 5)), "tick", "tick"]
        elif lvl == 2:
            self.reach = 1
            self.walls = {(5, y) for y in range(1, 8)} | {(x, 8) for x in range(4, 11) if x not in (8, 10)}
            self.echoes = {(9, 7): False}
            self.switches = [
                {"pos": (2, 2), "state": False, "target": True, "single": False, "hits": 0},
                {"pos": (4, 2), "state": False, "target": True, "single": False, "hits": 0},
                {"pos": (8, 8), "state": False, "target": True, "single": False, "hits": 0},
                {"pos": (10, 8), "state": False, "target": True, "single": False, "hits": 0},
            ]
            self.witness = [("emit", (3, 3)), "tick", ("emit", (9, 6)), "tick", "tick"]
        else:
            self.reach = 1
            self.walls = {(5, y) for y in range(2, 10) if y != 6} | {(x, 5) for x in range(1, 9) if x != 3}
            self.echoes = {(8, 3): False, (8, 8): False, (2, 8): False}
            self.switches = [
                {"pos": (2, 2), "state": False, "target": True, "single": True, "hits": 0},
                {"pos": (4, 2), "state": False, "target": True, "single": False, "hits": 0},
                {"pos": (8, 2), "state": False, "target": True, "single": True, "hits": 0},
                {"pos": (9, 7), "state": False, "target": True, "single": True, "hits": 0},
                {"pos": (2, 9), "state": False, "target": True, "single": True, "hits": 0},
                {"pos": (7, 9), "state": False, "target": True, "single": False, "hits": 0},
            ]
            self.witness = [("emit", (3, 3)), "tick", ("emit", (8, 4)), "tick", "tick", ("emit", (8, 7)), "tick", "tick", ("emit", (2, 7)), "tick", "tick"]
        self.max_steps = len(self.witness) + 3
        self.steps_left = self.max_steps
        self._sync()

    def _grid_at(self, gx, gy):
        if not (self.OX <= gx < self.OX + self.GRID * self.CELL and self.OY <= gy < self.OY + self.GRID * self.CELL):
            return None
        return ((gx - self.OX) // self.CELL, (gy - self.OY) // self.CELL)

    def _cell_pos(self, x, y):
        return self.OX + x * self.CELL, self.OY + y * self.CELL

    def _ring_cells(self, source, radius):
        sx, sy = source
        cells = set()
        for y in range(sy - radius, sy + radius + 1):
            for x in range(sx - radius, sx + radius + 1):
                if 0 <= x < self.GRID and 0 <= y < self.GRID and max(abs(x - sx), abs(y - sy)) == radius and (x, y) not in self.walls:
                    cells.add((x, y))
        return cells

    def _emit(self, pos):
        if pos in self.walls or pos in self.echoes or any(s["pos"] == pos for s in self.switches):
            return False
        self.emitter = pos
        self.waves.append({"source": pos, "radius": 0})
        self.steps_left -= 1
        return True

    def _tick(self):
        hit_cells = set()
        new_waves = []
        for wave in self.waves:
            wave["radius"] += 1
            hit_cells |= self._ring_cells(wave["source"], wave["radius"])
            if wave["radius"] < self.reach:
                new_waves.append(wave)
        self.waves = new_waves
        for sw in self.switches:
            if sw["pos"] in hit_cells:
                if not sw["single"] or sw["hits"] == 0:
                    sw["state"] = not sw["state"]
                sw["hits"] += 1
        for pos, used in list(self.echoes.items()):
            if not used and pos in hit_cells:
                self.echoes[pos] = True
                new_waves.append({"source": pos, "radius": 0})
        self.steps_left -= 1

    def _check_win(self):
        return all(sw["state"] == sw["target"] for sw in self.switches)

    def _floor_pixels(self):
        px = [[FLOOR] * self.CELL for _ in range(self.CELL)]
        px[2][2] = 10
        return px

    def _switch_pixels(self, sw):
        color = SW_ON if sw["state"] else SW_OFF
        px = [[-1] * self.CELL for _ in range(self.CELL)]
        for i in range(self.CELL):
            px[0][i] = px[4][i] = px[i][0] = px[i][4] = SW_TARGET
        for y in range(1, 4):
            for x in range(1, 4):
                px[y][x] = color
        if sw["single"]:
            px[2][2] = ONE_SHOT
        return px

    def _sync(self):
        sprites = [Sprite([[BG] * self.W for _ in range(self.H)], "bg", layer=-2).set_position(0, 0)]
        wave_cells = set()
        for wave in self.waves:
            if wave["radius"] > 0:
                wave_cells |= self._ring_cells(wave["source"], wave["radius"])
        for y in range(self.GRID):
            for x in range(self.GRID):
                px, py = self._cell_pos(x, y)
                color = WALL if (x, y) in self.walls else WAVE if (x, y) in wave_cells else None
                if color is None:
                    sprites.append(Sprite(self._floor_pixels(), f"floor_{x}_{y}", layer=0).set_position(px, py))
                else:
                    sprites.append(Sprite([[color] * self.CELL for _ in range(self.CELL)], f"cell_{x}_{y}", layer=1).set_position(px, py))
        for sw in self.switches:
            sprites.append(Sprite(self._switch_pixels(sw), f"switch_{sw['pos']}", layer=3).set_position(*self._cell_pos(*sw["pos"])))
        for pos, used in self.echoes.items():
            color = FLOOR if used else ECHO
            sprites.append(Sprite([[-1, color, -1, color, -1], [color, color, color, color, color], [-1, color, 5, color, -1], [color, color, color, color, color], [-1, color, -1, color, -1]], f"echo_{pos}", layer=2).set_position(*self._cell_pos(*pos)))
        ex, ey = self._cell_pos(*self.emitter)
        sprites.append(Sprite([[-1, EMITTER, -1, EMITTER, -1], [EMITTER, EMITTER, EMITTER, EMITTER, EMITTER], [-1, EMITTER, 5, EMITTER, -1], [EMITTER, EMITTER, EMITTER, EMITTER, EMITTER], [-1, EMITTER, -1, EMITTER, -1]], "emitter", layer=4).set_position(ex, ey))
        self.current_level._sprites = sprites

    def step(self):
        if self.steps_left > 0:
            if self.action.id == GameAction.ACTION5:
                self._tick()
            elif self.action.id == GameAction.ACTION6:
                grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
                cell = self._grid_at(*grid) if grid is not None else None
                if cell is not None:
                    self._emit(cell)
        self._sync()
        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        arr = np.zeros((self.GRID, self.GRID), dtype=np.int16)
        for sw in self.switches:
            x, y = sw["pos"]
            arr[y, x] = 2 if sw["state"] else 1
        return arr
