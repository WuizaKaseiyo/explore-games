"""Sandbar-River-Block.

Click to place spreading sand on riverbanks or river cells. The boat advances
one directed current node after every placement. At junctions the first open
current is chosen, so the player must dam wrong tributaries before the boat
arrives without letting spreading sand choke the useful route.
"""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
LAND = 11
LAND_DARK = 12
WATER = 1
WATER_EDGE = 10
SAND = 4
SAND_EDGE = 7
BOAT = 9
PORT = 3
BAD_PORT = 2
ROCK = 5
HUD_FILL = 6
HUD_EMPTY = 13


class StepHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps:
            ratio = max(0.0, min(1.0, self.game.steps_left / self.game.max_steps))
            filled = int(round(frame.shape[1] * ratio))
            for x in range(frame.shape[1]):
                frame[0, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


class Gg05(NovaBaseGame):
    W = 64
    H = 64

    def __init__(self) -> None:
        self.hud = StepHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.river = set()
        self.river_edge = set()
        self.nodes = set()
        self.rocks = set()
        self.flow = {}
        self.boat = (0, 0)
        self.port = (0, 0)
        self.bad_ports = set()
        self.sand = set()
        self.witness = []
        self.max_steps = 0
        self.steps_left = 0
        super().__init__("gg05", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[6])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        self.river = set()
        self.river_edge = set()
        self.nodes = set()
        self.rocks = set()
        self.flow = {}
        self.sand = set()
        self.bad_ports = set()

        lvl = level.get_data("Level")
        if lvl == 1:
            self.boat = (6, 32)
            self.port = (56, 32)
            main = [(6, 32), (14, 32), (22, 32), (30, 32), (38, 32), (46, 32), (56, 32)]
            north = [(30, 32), (30, 24), (30, 16), (24, 10)]
            self._add_path(main)
            self._add_path(north)
            self.flow[(30, 32)] = [(30, 24), (38, 32)]
            self.bad_ports = {(24, 10)}
            self.rocks = {(18, 25), (19, 25), (44, 38), (45, 38), (46, 39), (11, 45)}
            self.witness = [(54, 55), (9, 54), (30, 24), (58, 10), (5, 9), (45, 55)]
        elif lvl == 2:
            self.boat = (5, 12)
            self.port = (58, 44)
            main = [(5, 12), (13, 12), (21, 12), (29, 12), (37, 12), (37, 20),
                    (37, 28), (37, 36), (45, 36), (53, 36), (58, 44)]
            north = [(21, 12), (21, 4), (14, 4)]
            west = [(37, 28), (29, 28), (21, 28), (13, 34)]
            self._add_path(main)
            self._add_path(north)
            self._add_path(west)
            self.flow[(21, 12)] = [(21, 4), (29, 12)]
            self.flow[(37, 28)] = [(29, 28), (37, 36)]
            self.bad_ports = {(14, 4), (13, 34)}
            self.rocks = {(9, 22), (10, 23), (11, 23), (48, 15), (49, 15), (50, 16), (30, 48), (31, 49)}
            self.witness = [(56, 56), (21, 4), (6, 54), (57, 8), (9, 46), (29, 28), (57, 55), (6, 7), (49, 54), (15, 56)]
        else:
            self.boat = (5, 52)
            self.port = (58, 12)
            main = [(5, 52), (13, 52), (21, 52), (21, 44), (21, 36), (29, 36),
                    (37, 36), (37, 28), (37, 20), (45, 20), (53, 20), (58, 12)]
            left = [(21, 44), (13, 44), (8, 36)]
            south = [(37, 36), (45, 44), (54, 52)]
            north = [(45, 20), (45, 12), (36, 8)]
            self._add_path(main)
            self._add_path(left)
            self._add_path(south)
            self._add_path(north)
            self.flow[(21, 44)] = [(13, 44), (21, 36)]
            self.flow[(37, 36)] = [(45, 44), (37, 28)]
            self.flow[(45, 20)] = [(45, 12), (53, 20)]
            self.bad_ports = {(8, 36), (54, 52), (36, 8)}
            self.rocks = {(12, 20), (13, 21), (28, 48), (29, 49), (50, 33), (51, 34), (55, 6), (6, 7)}
            self.witness = [(58, 58), (6, 58), (13, 44), (31, 58), (5, 5), (45, 44),
                            (57, 58), (5, 24), (45, 12), (12, 58), (49, 58)]

        self._thicken_river()
        self.max_steps = len(self.witness)
        self.steps_left = self.max_steps
        self._sync_sprites()

    def _add_path(self, cells):
        for cell in cells:
            self.nodes.add(cell)
        for a, b in zip(cells, cells[1:]):
            self.flow.setdefault(a, []).append(b)
            for p in self._line(a, b):
                self.river.add(p)

    def _line(self, a, b):
        x1, y1 = a
        x2, y2 = b
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            return [a]
        out = []
        for i in range(steps + 1):
            x = round(x1 + dx * i / steps)
            y = round(y1 + dy * i / steps)
            if 0 <= x < self.W and 1 <= y < self.H:
                out.append((x, y))
        return out

    def _thicken_river(self):
        edge = set()
        for x, y in self.river:
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                p = (x + dx, y + dy)
                if 0 <= p[0] < self.W and 1 <= p[1] < self.H:
                    edge.add(p)
        self.river_edge = edge

    def _spread_sand(self):
        expanded = set(self.sand)
        for x, y in self.sand:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p = (x + dx, y + dy)
                if 0 <= p[0] < self.W and 1 <= p[1] < self.H and p not in self.rocks and p not in (self.boat, self.port):
                    expanded.add(p)
        self.sand = expanded

    def _sand_blocks(self, node):
        x, y = node
        return any(abs(x - sx) + abs(y - sy) <= 2 for sx, sy in self.sand)

    def _open_node(self, node):
        return node in self.nodes and not self._sand_blocks(node)

    def _advance_boat(self):
        choices = [p for p in self.flow.get(self.boat, []) if self._open_node(p)]
        if not choices:
            return False
        self.boat = choices[0]
        return True

    def _place_sand(self, cell):
        if not (0 <= cell[0] < self.W and 1 <= cell[1] < self.H):
            return False
        if cell in self.rocks or cell == self.boat or cell == self.port:
            return False
        self.sand.add(cell)
        self._advance_boat()
        self._spread_sand()
        self.steps_left -= 1
        return True

    def _terrain_color(self, x, y):
        p = (x, y)
        if p in self.rocks:
            return ROCK
        if p in self.river:
            return WATER
        if p in self.river_edge:
            return WATER_EDGE
        return LAND if (x // 4 + y // 4) % 2 == 0 else LAND_DARK

    def _sync_sprites(self):
        sprites = []
        for y in range(1, self.H):
            for x in range(self.W):
                sprites.append(Sprite([[self._terrain_color(x, y)]], f"terrain_{x}_{y}", layer=0).set_position(x, y))

        for p in self.bad_ports:
            sprites.append(Sprite(self._port_pixels(BAD_PORT), f"bad_port_{p}", layer=2).set_position(p[0] - 1, p[1] - 1))
        for p in self.sand:
            color = SAND if p in self.river_edge or p in self.river else SAND_EDGE
            sprites.append(Sprite([[color]], f"sand_{p}", layer=3).set_position(*p))

        sprites.append(Sprite(self._port_pixels(PORT), "port", layer=4).set_position(self.port[0] - 1, self.port[1] - 1))
        sprites.append(Sprite([[BOAT, BOAT, BOAT], [BOAT, 14, BOAT], [-1, BOAT, -1]], "boat", layer=5).set_position(self.boat[0] - 1, self.boat[1] - 1))
        self.current_level._sprites = sprites

    def _port_pixels(self, color):
        return [[color, color, color], [color, BG, color], [color, color, color]]

    def _check_win(self):
        return self.boat == self.port

    def step(self) -> None:
        if self.action.id == GameAction.ACTION6 and self.steps_left > 0:
            grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
            if grid is not None:
                self._place_sand(grid)
        self._sync_sprites()
        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        arr = np.zeros((self.H, self.W), dtype=np.int16)
        for x, y in self.river:
            arr[y, x] = 1
        for x, y in self.sand:
            arr[y, x] = 4
        arr[self.boat[1], self.boat[0]] = 9
        arr[self.port[1], self.port[0]] = 3
        return arr
