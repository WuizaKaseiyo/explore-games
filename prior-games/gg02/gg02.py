"""Orc-Path-Tower-Defense.

Simplified tower defense prototype. Orcs follow a predefined winding path to a
castle. ACTION6 clicks select/build arrow or mine towers; ACTION5 waits. Every
action advances combat by one step.
"""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 3
GRASS = 3
GRASS_DARK = 13
PATH = 9
PATH_EDGE = 8
WATER = 12
TREE = 10
TRUNK = 5
CASTLE = 7
CASTLE_HI = 15
SPAWN = 2
ORC = 10
ORC_DARK = 5
BOSS = 2
BOSS_DARK = 8
ARROW = 14
MINE = 11
RANGE = 6
HUD = 15
COIN = 4
BAD = 2
SELECT = 15


ORC_STATS = {
    "easy": {"hp": 2, "size": 1},
    "medium": {"hp": 4, "size": 2},
    "hard": {"hp": 8, "size": 3},
    "boss": {"hp": 11, "size": 4},
}

LEVELS = [
    {
        "coins": 10,
        "waypoints": [(2, 50), (11, 45), (18, 36), (29, 38), (37, 30), (47, 35), (58, 26)],
        "wave": ["easy", "easy", "medium"],
        "spawn_gap": 4,
        "solution": [("select", "arrow"), ("build", 34, 34)] + [("wait",)] * 58,
    },
    {
        "coins": 30,
        "waypoints": [(2, 12), (13, 18), (24, 13), (33, 22), (25, 33), (35, 43), (49, 39), (59, 52)],
        "wave": ["easy", "medium", "easy", "medium", "hard", "easy", "medium", "boss"],
        "spawn_gap": 3,
        "solution": [
            ("select", "arrow"), ("build", 27, 18),
            ("select", "mine"), ("build", 24, 33),
            ("select", "arrow"), ("build", 45, 39),
        ] + [("wait",)] * 86,
    },
    {
        "coins": 10,
        "waypoints": [(2, 56), (10, 45), (21, 49), (31, 39), (23, 28), (35, 19), (48, 25), (57, 14)],
        "wave": ["easy"] * 10 + ["medium"] * 4 + ["hard"] * 6 + ["medium"] * 4 + ["hard"] * 4 + ["boss"],
        "spawn_gap": 2,
        "solution": [
            ("select", "arrow"), ("build", 28, 36),
        ] + [("wait",)] * 50 + [
            ("select", "mine"), ("build", 24, 28),
        ] + [("wait",)] * 28 + [
            ("select", "arrow"), ("build", 39, 22),
        ] + [("wait",)] * 120,
    },
]


class BottomHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        for x in range(frame.shape[1]):
            frame[63, x] = HUD if x < min(63, self.game.coins * 2) else PATH_EDGE
        return frame


class Gg02(NovaBaseGame):
    W = 64
    H = 64
    ARROW_COST = 10
    MINE_COST = 10
    ARROW_RANGE = 4
    MINE_RANGE = 1
    ARROW_DAMAGE = 1
    MINE_DAMAGE = 4

    def __init__(self):
        self.hud = BottomHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={**data, "Level": i + 1}) for i, data in enumerate(LEVELS)]
        self.path = []
        self.path_set = set()
        self.wave = []
        self.spawn_gap = 0
        self.spawn_timer = 0
        self.spawn_index = 0
        self.orcs = []
        self.towers = []
        self.effects = []
        self.coins = 0
        self.selected = "arrow"
        self.tick = 0
        self.solution = []
        super().__init__("gg02", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[5, 6])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        self.path = self._make_path(level.get_data("waypoints"))
        self.path_set = set(self.path)
        self.wave = list(level.get_data("wave"))
        self.spawn_gap = level.get_data("spawn_gap")
        self.spawn_timer = 0
        self.spawn_index = 0
        self.orcs = []
        self.towers = []
        self.effects = []
        self.coins = level.get_data("coins")
        self.selected = "arrow"
        self.tick = 0
        self.solution = list(level.get_data("solution"))
        self._spawn_next()
        self._sync()

    def _make_path(self, waypoints):
        path = []
        for a, b in zip(waypoints, waypoints[1:]):
            x0, y0 = a
            x1, y1 = b
            dx = abs(x1 - x0)
            dy = -abs(y1 - y0)
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            err = dx + dy
            x, y = x0, y0
            while True:
                if not path or path[-1] != (x, y):
                    path.append((x, y))
                if x == x1 and y == y1:
                    break
                e2 = 2 * err
                if e2 >= dy:
                    err += dy
                    x += sx
                if e2 <= dx:
                    err += dx
                    y += sy
        return path

    def _spawn_next(self):
        if self.spawn_index >= len(self.wave):
            return
        if any(orc["idx"] == 0 for orc in self.orcs):
            return
        kind = self.wave[self.spawn_index]
        stats = ORC_STATS[kind]
        self.orcs.append({"idx": 0, "hp": stats["hp"], "max_hp": stats["hp"], "kind": kind})
        self.spawn_index += 1
        self.spawn_timer = self.spawn_gap

    def _occupied(self, x, y):
        if (x, y) in self.path_set:
            return True
        if any(tower["pos"] == (x, y) for tower in self.towers):
            return True
        return any(self.path[orc["idx"]] == (x, y) for orc in self.orcs)

    def _click_palette(self, x, y):
        if 0 <= x <= 6 and 0 <= y <= 6:
            self.selected = "arrow"
            return True
        if 0 <= x <= 6 and 8 <= y <= 14:
            self.selected = "mine"
            return True
        return False

    def _build(self, x, y):
        if self._click_palette(x, y):
            return
        cost = self.ARROW_COST if self.selected == "arrow" else self.MINE_COST
        if self.coins < cost or self._occupied(x, y):
            return
        self.towers.append({"kind": self.selected, "pos": (x, y)})
        self.coins -= cost

    def _dist2(self, a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def _mine_armed(self):
        return self.tick % 2 == 0

    def _attack(self):
        for tower in self.towers:
            pos = tower["pos"]
            if tower["kind"] == "arrow":
                in_range = [
                    orc for orc in self.orcs
                    if self._dist2(pos, self.path[orc["idx"]]) <= self.ARROW_RANGE ** 2
                ]
                if in_range:
                    target = max(in_range, key=lambda orc: orc["idx"])
                    self.effects.append(("arrow", pos, self.path[target["idx"]]))
                    target["hp"] -= self.ARROW_DAMAGE
            else:
                if not self._mine_armed():
                    continue
                hit = False
                for orc in self.orcs:
                    if self._dist2(pos, self.path[orc["idx"]]) <= self.MINE_RANGE ** 2:
                        orc["hp"] -= self.MINE_DAMAGE
                        hit = True
                if hit:
                    self.effects.append(("mine", pos))
        survivors = []
        for orc in self.orcs:
            if orc["hp"] <= 0:
                self.coins += 1
            else:
                survivors.append(orc)
        self.orcs = survivors

    def _advance_orcs(self):
        for orc in self.orcs:
            orc["idx"] += 1
            if orc["idx"] >= len(self.path) - 1:
                self.lose()
                return
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self._spawn_next()

    def _advance_turn(self):
        self.effects = []
        self._attack()
        if not self.orcs and self.spawn_index >= len(self.wave):
            return
        self._advance_orcs()
        self.tick += 1

    def _check_win(self):
        return self.spawn_index >= len(self.wave) and not self.orcs

    def _put(self, canvas, x, y, color):
        if 0 <= x < self.W and 0 <= y < self.H:
            canvas[y][x] = color

    def _rect(self, canvas, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._put(canvas, xx, yy, color)

    def _dot(self, canvas, x, y, color, r=1):
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                if abs(xx - x) + abs(yy - y) <= r + 1:
                    self._put(canvas, xx, yy, color)

    def _line(self, canvas, a, b, color):
        x0, y0 = a
        x1, y1 = b
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self._dot(canvas, x, y, color, 1)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def _draw_background(self, canvas):
        # Pixel-art pass can expand this into richer forest/pond/castle dressing.
        for y in range(self.H):
            for x in range(self.W):
                canvas[y][x] = GRASS_DARK if (x * 3 + y * 5) % 17 == 0 else GRASS
        for pond in ((50, 6, 6, 3), (9, 26, 5, 4), (47, 55, 7, 3)):
            cx, cy, rx, ry = pond
            for yy in range(cy - ry, cy + ry + 1):
                for xx in range(cx - rx, cx + rx + 1):
                    if ((xx - cx) ** 2) * ry <= (rx ** 2) * max(1, ry - abs(yy - cy)):
                        self._put(canvas, xx, yy, WATER)
            self._put(canvas, cx - rx + 2, cy - 1, HUD)
            self._put(canvas, cx + rx - 2, cy + 1, RANGE)
        for tx, ty in ((4, 6), (13, 8), (22, 57), (39, 7), (55, 43), (4, 37), (44, 48), (58, 5), (17, 22)):
            self._rect(canvas, tx - 1, ty + 1, 3, 4, TRUNK)
            self._dot(canvas, tx, ty, TREE, 3)
            self._dot(canvas, tx - 2, ty + 1, TREE, 2)
            self._put(canvas, tx - 1, ty - 1, HUD)

    def _draw_path(self, canvas):
        for a, b in zip(self.path, self.path[1:]):
            self._line(canvas, a, b, PATH_EDGE)
        for x, y in self.path:
            self._put(canvas, x, y, PATH)
            if (x + y) % 5 == 0:
                self._put(canvas, x, y, TRUNK)
        sx, sy = self.path[0]
        self._dot(canvas, sx, sy, SPAWN, 3)
        self._put(canvas, sx - 1, sy - 1, BG)
        self._put(canvas, sx + 1, sy - 1, BG)
        cx, cy = self.path[-1]
        self._draw_castle(canvas, cx, cy)

    def _draw_castle(self, canvas, x, y):
        # Future visual pass: expand this keep with flags, banners, and wall shadows.
        self._rect(canvas, x - 6, y - 5, 13, 10, CASTLE)
        self._rect(canvas, x - 3, y - 1, 7, 6, CASTLE_HI)
        self._rect(canvas, x - 7, y - 9, 4, 6, CASTLE)
        self._rect(canvas, x + 4, y - 9, 4, 6, CASTLE)
        for dx in (-5, -1, 3):
            self._put(canvas, x + dx, y - 6, CASTLE_HI)
        self._put(canvas, x - 5, y - 7, BG)
        self._put(canvas, x + 6, y - 7, BG)
        self._put(canvas, x, y + 4, BG)
        self._put(canvas, x + 1, y + 4, BG)

    def _draw_palette(self, canvas):
        self._rect(canvas, 0, 0, 7, 7, PATH_EDGE if self.selected == "arrow" else GRASS_DARK)
        self._rect(canvas, 0, 8, 7, 7, PATH_EDGE if self.selected == "mine" else GRASS_DARK)
        self._put(canvas, 3, 1, ARROW)
        self._line(canvas, (2, 5), (5, 2), ARROW)
        self._put(canvas, 1, 1, RANGE)
        self._put(canvas, 5, 5, RANGE)
        self._dot(canvas, 3, 11, MINE, 2)
        self._put(canvas, 3, 9, SELECT if self._mine_armed() else PATH_EDGE)
        for x in range(min(63, self.coins)):
            self._put(canvas, x, 62, COIN)

    def _draw_range(self, canvas, tower):
        x, y = tower["pos"]
        radius = self.ARROW_RANGE if tower["kind"] == "arrow" else self.MINE_RANGE
        if tower["kind"] == "arrow":
            inner = max(0, radius - 1) ** 2
            outer = radius ** 2
            for yy in range(y - radius, y + radius + 1):
                for xx in range(x - radius, x + radius + 1):
                    d2 = self._dist2((x, y), (xx, yy))
                    if inner < d2 <= outer and (xx + yy) % 4 == 0:
                        self._put(canvas, xx, yy, RANGE)
        else:
            color = MINE if self._mine_armed() else PATH_EDGE
            for yy in range(y - radius, y + radius + 1):
                for xx in range(x - radius, x + radius + 1):
                    if self._dist2((x, y), (xx, yy)) <= radius ** 2:
                        self._put(canvas, xx, yy, color)

    def _draw_tower(self, canvas, tower):
        x, y = tower["pos"]
        if tower["kind"] == "arrow":
            self._rect(canvas, x - 1, y - 1, 3, 3, TRUNK)
            self._put(canvas, x, y - 2, ARROW)
            self._put(canvas, x - 1, y - 2, ARROW)
            self._put(canvas, x + 1, y - 2, ARROW)
        else:
            self._dot(canvas, x, y, MINE, 2)
            self._put(canvas, x - 2, y, BAD)
            self._put(canvas, x + 2, y, BAD)
            self._put(canvas, x, y - 2, BAD)
            self._put(canvas, x, y, SELECT if self._mine_armed() else PATH_EDGE)

    def _draw_effects(self, canvas):
        for effect in self.effects:
            if effect[0] == "arrow":
                _, start, end = effect
                sx, sy = start
                ex, ey = end
                mx, my = (sx + ex) // 2, (sy + ey) // 2
                self._put(canvas, mx, my, HUD)
                self._put(canvas, ex, ey - 1, BAD)
            else:
                _, pos = effect
                x, y = pos
                for dx, dy in ((0, -2), (2, 0), (0, 2), (-2, 0)):
                    self._put(canvas, x + dx, y + dy, BAD)

    def _draw_orc(self, canvas, orc):
        x, y = self.path[orc["idx"]]
        size = ORC_STATS[orc["kind"]]["size"]
        color = BOSS if orc["kind"] == "boss" else ORC
        dark = BOSS_DARK if orc["kind"] == "boss" else ORC_DARK
        self._dot(canvas, x, y, color, size)
        self._put(canvas, x - 1, y, dark)
        self._put(canvas, x + 1, y, dark)
        if orc["kind"] == "boss":
            self._put(canvas, x - 3, y - 3, SELECT)
            self._put(canvas, x + 3, y - 3, SELECT)
            self._put(canvas, x, y + 2, dark)
        hp_width = max(1, min(7, orc["hp"]))
        for dx in range(hp_width):
            self._put(canvas, x - 2 + dx, y - size - 2, BAD if orc["hp"] <= 2 else COIN)

    def _sync(self):
        canvas = [[BG for _ in range(self.W)] for _ in range(self.H)]
        self._draw_background(canvas)
        self._draw_path(canvas)
        self._draw_palette(canvas)
        for tower in self.towers:
            self._draw_range(canvas, tower)
        for tower in self.towers:
            self._draw_tower(canvas, tower)
        for orc in self.orcs:
            self._draw_orc(canvas, orc)
        self._draw_effects(canvas)
        self.current_level._sprites = [Sprite(canvas, "scene", layer=0).set_position(0, 0)]

    def step(self):
        if self.action.id == GameAction.ACTION6:
            grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
            if grid is not None:
                self._build(int(grid[0]), int(grid[1]))
            self._advance_turn()
        elif self.action.id == GameAction.ACTION5:
            self._advance_turn()
        self._sync()
        if self._check_win():
            self.next_level()
        elif not getattr(self, "lost", False) and any(orc["idx"] >= len(self.path) - 1 for orc in self.orcs):
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        rows = [[self.coins, self.spawn_index, len(self.orcs), len(self.towers), self.tick]]
        rows.extend([[orc["idx"], orc["hp"], orc["max_hp"], 0, 0] for orc in self.orcs])
        rows.extend([[tower["pos"][0], tower["pos"][1], 1 if tower["kind"] == "arrow" else 2, 0, 0] for tower in self.towers])
        return np.array(rows, dtype=np.int16)
