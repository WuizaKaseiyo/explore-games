"""Docking-Orbit-Control.

Space-traffic timing puzzle. ACTION5 advances every unheld spacecraft one lane
slot. ACTION6 either holds/releases the clicked spacecraft or toggles a
transfer beacon that diverts ships between lanes. Ships must reach their docks
without striking asteroids or raiders.
"""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
LANE = 5
HOLD = 7
HUD = 14
DOCK = 15
ASTEROID = 8
RAIDER = 2
GATE_OFF = 11
GATE_ON = 10
COL = [12, 9, 10, 14]


class BottomHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if not self.game.max_steps:
            return frame
        filled = int(round(frame.shape[1] * max(0, self.game.steps_left) / self.game.max_steps))
        for x in range(frame.shape[1]):
            frame[63, x] = HUD if x < filled else LANE
        return frame


LEVELS = [
    {
        "paths": [
            [(8, 10), (15, 7), (23, 9), (29, 16), (30, 25), (25, 33), (17, 37), (10, 43), (7, 52), (14, 58), (24, 56), (31, 49), (29, 41), (21, 39), (13, 31), (6, 21)],
            [(42, 7), (52, 9), (59, 17), (57, 27), (50, 33), (42, 36), (36, 43), (38, 52), (47, 58), (56, 54), (61, 45), (58, 36), (51, 31), (44, 27), (38, 20), (39, 12)],
        ],
        "ships": [(0, 0, 0, (0, 4)), (1, 2, 1, (1, 10))],
        "hazards": [((0, 8), "raider", 1, 1), ((1, 13), "asteroid", 2, 1), ((1, 15), "raider", 1, -1)],
        "gates": [],
        "solution": [("tick",), ("tick",), ("tick",), ("tick",), ("hold", 0), ("tick",), ("tick",), ("tick",), ("tick",)],
        "max_steps": 16,
    },
    {
        "paths": [
            [(5, 13), (12, 8), (22, 7), (31, 12), (34, 22), (30, 31), (20, 35), (10, 32), (4, 23), (7, 16)],
            [(38, 10), (48, 8), (58, 15), (60, 26), (53, 36), (42, 38), (34, 31), (33, 20)],
            [(9, 50), (17, 43), (28, 41), (40, 44), (54, 42), (61, 50), (55, 59), (42, 60), (29, 57), (17, 59)],
        ],
        "ships": [(0, 0, 0, (1, 4)), (2, 5, 1, (2, 2))],
        "hazards": [((0, 4), "asteroid", 1, 1), ((1, 6), "raider", 1, 1), ((2, 0), "raider", 1, 1), ((2, 3), "asteroid", 2, 1)],
        "gates": [((0, 3), (1, 0), False)],
        "solution": [("tick",), ("tick",), ("gate", 0), ("tick",), ("tick",), ("tick",), ("tick",), ("tick",)],
        "max_steps": 16,
    },
    {
        "paths": [
            [(5, 6), (14, 4), (25, 7), (31, 16), (29, 27), (20, 34), (9, 31), (3, 20)],
            [(39, 5), (51, 4), (60, 12), (61, 24), (53, 33), (41, 32), (34, 23), (34, 12)],
            [(6, 43), (15, 38), (27, 40), (33, 49), (29, 59), (16, 61), (5, 55), (3, 48)],
            [(39, 42), (51, 39), (61, 47), (59, 58), (47, 62), (36, 56), (34, 47)],
        ],
        "ships": [(0, 0, 0, (1, 4)), (2, 0, 1, (0, 6)), (3, 3, 2, (3, 3))],
        "hazards": [((1, 6), "raider", 1, 1), ((2, 4), "raider", 1, 1), ((3, 0), "asteroid", 1, 1), ((3, 2), "raider", 2, 1)],
        "gates": [((0, 2), (1, 0), False), ((2, 2), (0, 6), False)],
        "solution": [("gate", 0), ("gate", 1), ("tick",), ("hold", 0), ("tick",), ("hold", 1), ("hold", 0), ("tick",), ("tick",), ("tick",), ("tick",), ("tick",)],
        "max_steps": 24,
    },
]


class Gg25(NovaBaseGame):
    W = 64
    H = 64

    def __init__(self):
        self.hud = BottomHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={**data, "Level": i + 1}) for i, data in enumerate(LEVELS)]
        self.paths = []
        self.ships = []
        self.hazards = {}
        self.gates = []
        self.clock = 0
        self.solution = []
        self.max_steps = 0
        self.steps_left = 0
        super().__init__("gg25", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[5, 6])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        self.paths = [list(path) for path in level.get_data("paths")]
        self.ships = [
            {"lane": lane, "pos": pos, "color": color, "dock": dock, "held": False}
            for lane, pos, color, dock in level.get_data("ships")
        ]
        self.hazards = [
            {"loc": tuple(cell), "kind": kind, "period": period, "dir": direction}
            for cell, kind, period, direction in level.get_data("hazards")
        ]
        self.gates = [
            {"from": tuple(src), "to": tuple(dst), "active": active}
            for src, dst, active in level.get_data("gates")
        ]
        self.solution = list(level.get_data("solution"))
        self.max_steps = level.get_data("max_steps")
        self.steps_left = self.max_steps
        self.clock = 0
        self._sync()

    def _slot_count(self, lane):
        return len(self.paths[lane])

    def _point_for(self, loc):
        lane, pos = loc
        return self.paths[lane][pos % self._slot_count(lane)]

    def _advance_loc(self, loc):
        lane, pos = loc
        loc = (lane, (pos + 1) % self._slot_count(lane))
        for gate in self.gates:
            if gate["active"] and gate["from"] == loc:
                return gate["to"]
        return loc

    def _advance_hazard(self, hazard):
        if (self.clock + 1) % hazard["period"] != 0:
            return hazard["loc"]
        lane, pos = hazard["loc"]
        return (lane, (pos + hazard["dir"]) % self._slot_count(lane))

    def _tick(self):
        next_locs = []
        for ship in self.ships:
            loc = (ship["lane"], ship["pos"])
            if not ship["held"]:
                loc = self._advance_loc(loc)
            next_locs.append(loc)
        next_hazards = [self._advance_hazard(hazard) for hazard in self.hazards]
        if any(loc in next_hazards for loc in next_locs):
            self.steps_left -= 1
            self.lose()
            return
        if len(set(next_locs)) != len(next_locs):
            self.steps_left -= 1
            self.lose()
            return
        for ship, (lane, pos) in zip(self.ships, next_locs):
            ship["lane"] = lane
            ship["pos"] = pos
        for hazard, loc in zip(self.hazards, next_hazards):
            hazard["loc"] = loc
        self.clock += 1
        self.steps_left -= 1

    def _ship_at(self, x, y):
        for idx, ship in enumerate(self.ships):
            sx, sy = self._point_for((ship["lane"], ship["pos"]))
            if abs(x - sx) + abs(y - sy) <= 5:
                return idx
        return None

    def _gate_point(self, gate):
        ax, ay = self._point_for(gate["from"])
        bx, by = self._point_for(gate["to"])
        return (ax + bx) // 2, (ay + by) // 2

    def _gate_at(self, x, y):
        for idx, gate in enumerate(self.gates):
            gx, gy = self._gate_point(gate)
            if abs(x - gx) + abs(y - gy) <= 5:
                return idx
        return None

    def _toggle_control(self, x, y):
        gate = self._gate_at(x, y)
        if gate is not None:
            self.gates[gate]["active"] = not self.gates[gate]["active"]
            self.steps_left -= 1
            return
        ship = self._ship_at(x, y)
        if ship is not None:
            self.ships[ship]["held"] = not self.ships[ship]["held"]
            self.steps_left -= 1

    def _check_win(self):
        return all((ship["lane"], ship["pos"]) == ship["dock"] for ship in self.ships)

    def _put(self, canvas, x, y, color):
        if 0 <= x < self.W and 0 <= y < self.H:
            canvas[y][x] = color

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
            self._put(canvas, x, y, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def _draw_dock(self, canvas, loc, color):
        x, y = self._point_for(loc)
        for i in range(-3, 4):
            self._put(canvas, x + i, y - 3, color)
            self._put(canvas, x + i, y + 3, color)
            self._put(canvas, x - 3, y + i, color)
            self._put(canvas, x + 3, y + i, color)
        self._put(canvas, x, y, DOCK)

    def _draw_asteroid(self, canvas, x, y):
        for dx, dy in [(-2, 0), (-1, -2), (0, -1), (0, 0), (1, 1), (2, 0), (1, -1), (-1, 1)]:
            self._put(canvas, x + dx, y + dy, ASTEROID)
        self._put(canvas, x, y, HOLD)
        self._put(canvas, x + 2, y - 1, BG)

    def _draw_raider(self, canvas, x, y, loc, period, direction):
        nx, ny = self._point_for((loc[0], (loc[1] + direction) % self._slot_count(loc[0])))
        dx = 0 if nx == x else (1 if nx > x else -1)
        dy = 0 if ny == y else (1 if ny > y else -1)
        if dx == 0 and dy == 0:
            dx = 1
        px, py = -dy, dx
        self._put(canvas, x + dx * 3, y + dy * 3, DOCK)
        for scale in (0, 1):
            self._put(canvas, x - dx * scale, y - dy * scale, RAIDER)
        self._put(canvas, x + px * 2, y + py * 2, RAIDER)
        self._put(canvas, x - px * 2, y - py * 2, RAIDER)
        self._put(canvas, x - dx + px, y - dy + py, RAIDER)
        self._put(canvas, x - dx - px, y - dy - py, RAIDER)
        if period == 2:
            self._put(canvas, x, y, HOLD)

    def _draw_hazard(self, canvas, hazard):
        loc = hazard["loc"]
        x, y = self._point_for(loc)
        if hazard["kind"] == "raider":
            self._draw_raider(canvas, x, y, loc, hazard["period"], hazard["dir"])
        else:
            self._draw_asteroid(canvas, x, y)

    def _draw_ship(self, canvas, ship):
        loc = (ship["lane"], ship["pos"])
        x, y = self._point_for(loc)
        nx, ny = self._point_for(self._advance_loc(loc))
        dx = 0 if nx == x else (1 if nx > x else -1)
        dy = 0 if ny == y else (1 if ny > y else -1)
        color = COL[ship["color"] % len(COL)]
        self._dot(canvas, x, y, color, 2)
        self._put(canvas, x + dx * 3, y + dy * 3, DOCK)
        self._put(canvas, x - dx, y - dy, BG)
        if ship["held"]:
            self._dot(canvas, x, y, HOLD, 1)

    def _sync(self):
        canvas = [[BG for _ in range(self.W)] for _ in range(self.H)]
        for y in range(1, self.H, 7):
            for x in range((y // 7) % 6, self.W, 9):
                canvas[y][x] = LANE
        for lane, path in enumerate(self.paths):
            for pos, point in enumerate(path):
                self._line(canvas, point, path[(pos + 1) % len(path)], LANE)
            for pos in range(len(path)):
                x, y = self._point_for((lane, pos))
                self._dot(canvas, x, y, LANE, 0)
        for gate in self.gates:
            a = self._point_for(gate["from"])
            b = self._point_for(gate["to"])
            color = GATE_ON if gate["active"] else GATE_OFF
            self._line(canvas, a, b, color)
            gx, gy = self._gate_point(gate)
            self._dot(canvas, gx, gy, color, 2)
            self._put(canvas, gx, gy, DOCK if gate["active"] else BG)
        for ship in self.ships:
            self._draw_dock(canvas, ship["dock"], COL[ship["color"] % len(COL)])
        for hazard in self.hazards:
            self._draw_hazard(canvas, hazard)
        for ship in self.ships:
            self._draw_ship(canvas, ship)
        self.current_level._sprites = [Sprite(canvas, "scene", layer=0).set_position(0, 0)]

    def step(self):
        if self.steps_left > 0:
            if self.action.id == GameAction.ACTION5:
                self._tick()
            elif self.action.id == GameAction.ACTION6:
                grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
                if grid is not None:
                    self._toggle_control(*grid)
        self._sync()
        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        row = [self.steps_left]
        for ship in self.ships:
            row.extend([ship["lane"], ship["pos"], int(ship["held"])])
        row.extend([int(gate["active"]) for gate in self.gates])
        for hazard in self.hazards:
            row.extend([hazard["loc"][0], hazard["loc"][1]])
        return np.array([row], dtype=np.int16)
