"""Sheep-Pasture-Fence.

Fence-placement puzzle. Click grass squares to place or remove fences. Stones,
water, and fences block four-direction sheep movement. Win when the sheep is
enclosed in a pasture large enough for the level target without exceeding the
fence budget.
"""

from __future__ import annotations

from collections import deque

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


# ── Calm pasture palette ──
BG = 0
GRASS = 3
ENCLOSED = 10   # yellow enclosed pasture
WATER = 1
STONE = 4
STONE_LIGHT = 9
FENCE = 6
FENCE_POST = 12
SHEEP = 15
FACE = 0
ENERGY_DOT = 7
GOAL = 10


DIRS = ((0, -1), (0, 1), (-1, 0), (1, 0))


# ── Three non‑obvious, scattered obstacle puzzles (water never counted) ──
LEVELS = [
    {
        # 1 – The Diagonal Brook
        "sheep": (6, 6),
        "budget": 5,
        "energy": 15,
        "min_area": 20,          # reachable grass cells after optimal fencing
        "water": [
            # a wavy, diagonal‑ish stream cutting across
            (1,2),(2,2),(2,1),
            (3,3),(4,3),(5,3),
            (4,5),(5,5),(6,5),
            (7,6),(8,6),(9,6),(10,6),
            (9,8),(10,8),(11,8),(12,8),
            (12,10),(13,10),(14,10),(14,11),
            # a few separate puddles
            (4,10),(5,10),(6,10),
            (11,3),(12,3),(12,4),
            (2,13),(3,13),(4,13)   # bottom‑left corner obstruction
        ],
        "stones": [
            # scattered rocks
            (5,8),(6,8),(7,8),(8,8),
            (9,4),(10,4),(11,4),
            (3,7),(4,7),(4,8),
            (12,7),(13,7),(13,8),
            (7,12),(8,12),(9,12),
            (5,13),(6,13)
        ],
        # Winning fences (5 pieces): (8,4),(14,9),(6,14),(1,6),(2,9)
        "solution": [(8,4),(14,9),(6,14),(1,6),(2,9)]
    },
    {
        # 2 – The Speckled Flat
        "sheep": (7, 7),
        "budget": 8,
        "energy": 18,
        "min_area": 42,
        "water": [
            (1,3),(2,3),(3,3),(3,2),
            (12,1),(13,1),(14,1),(14,2),
            (2,11),(3,11),(4,11),(4,10),
            (13,13),(14,13),(14,14),
            (6,5),(7,5),(8,5),(5,6),
            (10,9),(11,9),(12,9),(9,10)
        ],
        "stones": [
            (5,4),(6,4),(7,4),(8,4),(9,4),
            (4,9),(5,9),(6,9),(7,9),(8,9),
            (9,12),(10,12),(11,12),(12,12),
            (3,6),(3,7),(3,8),
            (13,6),(13,7),(13,8)
        ],
        # Winning fences: (3,4),(11,2),(15,13),(2,14),(10,13),(5,14)
        "solution": [(3,4),(11,2),(15,13),(2,14),(10,13),(5,14)]
    },
    {
        # 3 – The Grand Winding Pasture
        "sheep": (8, 7),
        "budget": 8,
        "energy": 22,
        "min_area": 43,
        "water": [
            (0,2),(1,2),(1,3),(2,2),
            (3,0),(4,0),(5,0),(6,0),
            (14,4),(15,4),(15,5),
            (13,15),(14,15),(15,15),
            (3,12),(4,12),(5,12),(6,12),(7,12),
            (10,11),(11,11),(12,11),(13,11),
            (2,7),(2,8),(2,9),
            (13,3),(13,4),(13,5)
        ],
        "stones": [
            (7,5),(7,6),(7,7),(7,8),(7,9),
            (9,3),(10,3),(11,3),(12,3),
            (8,13),(9,13),(10,13),(11,13),
            (4,5),(4,6),(5,6),
            (11,8),(12,8),(12,9)
        ],
        # Winning fences: (1,4),(6,1),(15,6),(14,14),(7,14),(3,13),(2,10),(13,6)
        "solution": [(1,4),(6,1),(15,6),(14,14),(7,14),(3,13),(2,10),(13,6)]
    },
]


class BottomHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        used = len(self.game.fences)
        for i in range(self.game.fence_budget):
            color = FENCE if i >= used else FENCE_POST
            frame[63, i * 2] = color
            frame[63, i * 2 + 1] = color

        for i in range(self.game.energy):
            frame[63, 20 + i] = ENERGY_DOT

        target = min(22, max(1, self.game.min_area // 6))
        current = min(22, max(0, self.game.current_area // 6))
        for i in range(target):
            frame[63, 41 + i] = STONE
        for i in range(current):
            frame[63, 41 + i] = ENCLOSED if self.game.current_enclosed else GRASS
        return frame


class Gg26(NovaBaseGame):
    W = 64
    H = 64
    N = 16
    CELL = 4

    def __init__(self):
        self.hud = BottomHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[],
                        data={**data, "Level": i + 1})
                  for i, data in enumerate(LEVELS)]
        self.sheep = (0, 0)
        self.water = set()
        self.stones = set()
        self.fences = set()
        self.fence_budget = 0
        self.energy = 0
        self.min_area = 0
        self.current_area = 0
        self.current_enclosed = False
        self.enclosed_cells = set()
        self.animation_ticks = 0
        self.sheep_frame = 0
        super().__init__(
            "gg26",
            levels,
            Camera(background=BG, letter_box=BG, interfaces=[self.hud]),
            available_actions=[GameAction.ACTION6],
        )

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        self.sheep = tuple(level.get_data("sheep"))
        self.water = {tuple(c) for c in level.get_data("water")}
        self.stones = {tuple(c) for c in level.get_data("stones")}
        self.fences = set()
        self.fence_budget = level.get_data("budget")
        self.energy = level.get_data("energy")
        self.min_area = level.get_data("min_area")
        self.current_area = 0
        self.current_enclosed = False
        self.enclosed_cells = set()
        self.animation_ticks = 0
        self.sheep_frame = 0
        self._update_area()
        self._sync()

    def _in_bounds(self, cell):
        x, y = cell
        return 0 <= x < self.N and 0 <= y < self.N

    def _blocked(self, cell):
        return cell in self.water or cell in self.stones or cell in self.fences

    def _update_area(self):
        seen = {self.sheep}
        queue = deque([self.sheep])
        touches_edge = False
        while queue:
            x, y = queue.popleft()
            if x == 0 or y == 0 or x == self.N - 1 or y == self.N - 1:
                touches_edge = True
            for dx, dy in DIRS:
                nxt = (x + dx, y + dy)
                if self._in_bounds(nxt) and nxt not in seen and not self._blocked(nxt):
                    seen.add(nxt)
                    queue.append(nxt)
        self.current_area = len(seen)
        self.current_enclosed = not touches_edge
        self.enclosed_cells = seen if self.current_enclosed else set()

    def _cell_from_click(self, x, y):
        return (
            max(0, min(self.N - 1, int(x) // self.CELL)),
            max(0, min(self.N - 1, int(y) // self.CELL)),
        )

    def _toggle_fence(self, cell):
        if cell == self.sheep or cell in self.water or cell in self.stones:
            return False
        if cell in self.fences:
            self.fences.remove(cell)
            return True
        elif len(self.fences) < self.fence_budget:
            self.fences.add(cell)
            return True
        return False

    def _passes(self):
        return (
            self.current_enclosed
            and self.current_area >= self.min_area
            and len(self.fences) <= self.fence_budget
        )

    # ── Drawing helpers ──
    def _put(self, canvas, x, y, color):
        if 0 <= x < self.W and 0 <= y < self.H:
            canvas[y][x] = color

    def _rect(self, canvas, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._put(canvas, xx, yy, color)

    def _cell_px(self, cell):
        return cell[0] * self.CELL, cell[1] * self.CELL

    def _draw_grass(self, canvas, cell):
        x, y = self._cell_px(cell)
        if self.current_enclosed and cell in self.enclosed_cells:
            self._rect(canvas, x, y, 4, 4, ENCLOSED)
        else:
            self._rect(canvas, x, y, 4, 4, GRASS)

    def _draw_water(self, canvas, cell):
        x, y = self._cell_px(cell)
        self._rect(canvas, x, y, 4, 4, WATER)
        if (cell[0] + cell[1]) % 2 == 0:
            self._put(canvas, x + 1, y + 1, 8)
            self._put(canvas, x + 2, y + 2, 8)
        else:
            self._put(canvas, x + 2, y + 1, 8)
            self._put(canvas, x + 1, y + 2, 8)

    def _draw_stone(self, canvas, cell):
        x, y = self._cell_px(cell)
        self._rect(canvas, x, y, 4, 4, STONE)
        self._put(canvas, x + 1, y + 2, STONE_LIGHT)
        self._put(canvas, x + 2, y + 1, STONE_LIGHT)
        self._put(canvas, x + 3, y + 3, STONE_LIGHT)

    def _draw_fence(self, canvas, cell):
        x, y = self._cell_px(cell)
        self._rect(canvas, x, y, 4, 4, FENCE)
        self._put(canvas, x,     y,     FENCE_POST)
        self._put(canvas, x + 3, y,     FENCE_POST)
        self._put(canvas, x,     y + 3, FENCE_POST)
        self._put(canvas, x + 3, y + 3, FENCE_POST)
        self._put(canvas, x + 1, y,     FENCE)
        self._put(canvas, x + 1, y + 3, FENCE)

    def _draw_sheep(self, canvas):
        x, y = self._cell_px(self.sheep)
        self._rect(canvas, x + 1, y + 1, 2, 2, SHEEP)
        self._put(canvas, x,     y + 1, SHEEP)
        self._put(canvas, x + 3, y + 1, SHEEP)
        self._put(canvas, x + 1, y,     SHEEP)
        self._put(canvas, x + 2, y,     FACE)
        if self.sheep_frame % 4 < 2:
            self._put(canvas, x + 3, y, SHEEP)
        self._put(canvas, x,     y + 3, FACE)
        self._put(canvas, x + 2, y + 3, FACE)

    def _sync(self):
        canvas = [[BG for _ in range(self.W)] for _ in range(self.H)]
        for y in range(self.N):
            for x in range(self.N):
                self._draw_grass(canvas, (x, y))
        for cell in self.water:
            self._draw_water(canvas, cell)
        for cell in self.stones:
            self._draw_stone(canvas, cell)
        for cell in self.fences:
            self._draw_fence(canvas, cell)
        self._draw_sheep(canvas)
        self.current_level._sprites = [Sprite(canvas, "scene", layer=0).set_position(0, 0)]

    def step(self):
        if self.animation_ticks > 0:
            self.animation_ticks -= 1
            self.sheep_frame = (self.sheep_frame + 1) % 8
            self._sync()
            if self.animation_ticks == 0:
                self.next_level()
                self.complete_action()
            return

        self.sheep_frame = (self.sheep_frame + 1) % 8

        aid = self.action.id.value if hasattr(self.action.id, "value") else int(self.action.id)
        if aid == 6 and self.energy > 0:
            grid = self.camera.display_to_grid(
                self.action.data.get("x", -1),
                self.action.data.get("y", -1),
            )
            if grid is not None:
                cell = self._cell_from_click(grid[0], grid[1])
                if self._toggle_fence(cell):
                    self.energy -= 1
                self._update_area()

        self._sync()
        if self._passes():
            self.animation_ticks = 5
            return
        if self.energy <= 0 and not self.current_enclosed:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        rows = [
            [
                self.sheep[0],
                self.sheep[1],
                len(self.fences),
                self.fence_budget,
                self.energy,
                self.current_area,
                int(self.current_enclosed),
            ]
        ]
        rows.extend([[1, x, y, 0, 0, 0, 0] for x, y in sorted(self.fences)])
        rows.extend([[2, x, y, 0, 0, 0, 0] for x, y in sorted(self.water)])
        rows.extend([[3, x, y, 0, 0, 0, 0] for x, y in sorted(self.stones)])
        return np.array(rows, dtype=np.int16)