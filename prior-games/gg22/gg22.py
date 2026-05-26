"""Conveyor-Switch-Sorter.

Clocked conveyor sorter. ACTION5 advances the belt and automatically feeds
staggered parcels onto a connected conveyor. ACTION6 toggles visible junction
switches or station modes; parcels themselves are moved only by the belt.
"""

from __future__ import annotations

from collections import Counter
import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
BELT = 5
BELT_DOT = 11
PANEL = 7
SELECT = 15
HUD = 14
BAD = 2
SWITCH = 8
STATION = 6
OUTLET = 13
COL = {"red": 12, "blue": 9, "gold": 10, "green": 14}
MARK_COL = {"stripe": 15, "circle": 11, "square": 7, "timer": 6}


class BottomHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if not self.game.max_steps:
            return frame
        filled = int(round(frame.shape[1] * max(0, self.game.steps_left) / self.game.max_steps))
        y = frame.shape[0] - 1
        for x in range(frame.shape[1]):
            frame[y, x] = HUD if x < filled else BELT
        return frame


class Gg22(NovaBaseGame):
    W = 64
    H = 64
    CELL = 4
    OX = 1
    OY = 4
    DEFAULT_START = (1, 5)

    def __init__(self):
        self.hud = BottomHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.tracks = set()
        self.nexts = {}
        self.switches = {}
        self.stations = {}
        self.outputs = {}
        self.queue = []
        self.flight = []
        self.scored = []
        self.target = []
        self.tick_count = 0
        self.failed = False
        self.max_steps = 0
        self.steps_left = 0
        super().__init__(
            "gg22",
            levels,
            Camera(background=BG, letter_box=BG, interfaces=[self.hud]),
            available_actions=[5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        self.tracks = set()
        self.nexts = {}
        self.switches = {}
        self.stations = {}
        self.outputs = {}
        self.flight = []
        self.scored = []
        self.tick_count = 0
        self.failed = False
        lvl = level.get_data("Level")
        self._build_track(lvl)
        if lvl == 1:
            self.queue = [self._parcel("red", (7, 1)), self._parcel("blue", (4, 1)), self._parcel("gold", (1, 1))]
            self.switches = {
                (12, 5): {"outs": [(11, 5), (12, 6)], "state": 1},
                (12, 7): {"outs": [(11, 7), (12, 8)], "state": 1},
            }
            self.stations = {
                (8, 5): self._station("stripe", "red"),
                (8, 7): self._station("circle", "blue"),
                (8, 9): self._station("square", "gold"),
            }
            self.outputs = {
                (2, 5): ("red", "stripe"),
                (2, 7): ("blue", "circle"),
                (2, 9): ("gold", "square"),
            }
            self.target = list(self.outputs.values())
            self.max_steps = 55
        elif lvl == 2:
            self.queue = [
                self._parcel("red", (4, 1)),
                self._parcel("blue", (7, 1)),
                self._parcel("red", (10, 1)),
                self._parcel("green", (13, 1)),
            ]
            self.switches = {
                (2, 4): {"outs": [(3, 4), (2, 5)], "state": 1},
                (2, 7): {"outs": [(3, 7), (2, 8)], "state": 1},
            }
            self.stations = {
                (8, 4): self._station("stripe", "red"),
                (8, 7): self._station("circle", "blue"),
                (8, 10): self._station("square", "green"),
            }
            self.outputs = {
                (13, 4): ("red", "stripe"),
                (13, 7): ("blue", "circle"),
                (13, 10): ("green", "square"),
            }
            self.target = [("red", "stripe"), ("blue", "circle"), ("red", "stripe"), ("green", "square")]
            self.max_steps = 70
        else:
            self.queue = [
                self._parcel("red", (4, 11)),
                self._parcel("blue", (7, 11)),
                self._parcel("gold", (10, 11)),
                self._parcel("red", (12, 11)),
            ]
            self.switches = {
                (2, 6): {"outs": [(2, 5), (3, 6)], "state": 1},
                (6, 6): {"outs": [(6, 5), (6, 7)], "state": 1},
            }
            self.stations = {
                (8, 3): self._station("stripe", "red"),
                (9, 4): self._station("mode", "blue", modes=[("circle", "blue"), ("timer", "gold")]),
                (9, 7): self._station("circle", "blue"),
            }
            self.outputs = {
                (13, 3): ("red", "stripe"),
                (13, 4): ("gold", "timer"),
                (13, 7): ("blue", "circle"),
            }
            self.target = [("red", "stripe"), ("blue", "circle"), ("gold", "timer"), ("red", "stripe")]
            self.max_steps = 85
        self.steps_left = self.max_steps
        self._sync()

    def _parcel(self, color, start=None):
        return {"color": color, "mark": None, "pos": None, "start": start or self.DEFAULT_START}

    def _station(self, kind, color, modes=None):
        return {"kind": kind, "color": color, "modes": modes or [], "state": 0}

    def _add_path(self, cells):
        for cell in cells:
            self.tracks.add(cell)
        for a, b in zip(cells, cells[1:]):
            self.nexts[a] = b

    def _build_track(self, level):
        if level == 1:
            self._build_track_l1()
        elif level == 2:
            self._build_track_l2()
        else:
            self._build_track_l3()

    def _build_track_l1(self):
        self._add_path([(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1)])
        self._add_path([(12, 1), (12, 2), (12, 3), (12, 4), (12, 5)])
        self._add_path([(11, 5), (10, 5), (9, 5), (8, 5), (7, 5), (6, 5), (5, 5), (4, 5), (3, 5), (2, 5)])
        self._add_path([(12, 6), (12, 7)])
        self._add_path([(11, 7), (10, 7), (9, 7), (8, 7), (7, 7), (6, 7), (5, 7), (4, 7), (3, 7), (2, 7)])
        self._add_path([(12, 8), (12, 9), (11, 9), (10, 9), (9, 9), (8, 9), (7, 9), (6, 9), (5, 9), (4, 9), (3, 9), (2, 9)])

    def _build_track_l2(self):
        self._add_path([(13, 1), (12, 1), (11, 1), (10, 1), (9, 1), (8, 1), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1)])
        self._add_path([(2, 1), (2, 2), (2, 3), (2, 4)])
        self._add_path([(3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4)])
        self._add_path([(2, 5), (2, 6), (2, 7)])
        self._add_path([(3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (12, 7), (13, 7)])
        self._add_path([(2, 8), (2, 9), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10)])

    def _build_track_l3(self):
        self._add_path([(13, 11), (12, 11), (11, 11), (10, 11), (9, 11), (8, 11), (7, 11), (6, 11), (5, 11), (4, 11), (3, 11), (2, 11)])
        self._add_path([(2, 11), (2, 10), (2, 9), (2, 8), (2, 7), (2, 6)])
        self._add_path([(2, 5), (2, 4), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3)])
        self._add_path([(3, 6), (4, 6), (5, 6), (6, 6)])
        self._add_path([(6, 5), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4)])
        self._add_path([(6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (12, 7), (13, 7)])

    def _cell_px(self, cell):
        return self.OX + cell[0] * self.CELL, self.OY + cell[1] * self.CELL

    def _hit_cell(self, x, y):
        if self.OX <= x < self.OX + 15 * self.CELL and self.OY <= y < self.OY + 12 * self.CELL:
            return (x - self.OX) // self.CELL, (y - self.OY) // self.CELL
        return None

    def _signature(self, parcel):
        return parcel["color"], parcel["mark"]

    def _occupied(self):
        return {parcel["pos"] for parcel in self.flight}

    def _next_cell(self, parcel):
        pos = parcel["pos"]
        if pos in self.outputs:
            return None
        if pos in self.switches:
            switch = self.switches[pos]
            return switch["outs"][switch["state"]]
        return self.nexts.get(pos)

    def _apply_station(self, parcel):
        station = self.stations.get(parcel["pos"])
        if station is None:
            return
        kind, color = station["kind"], station["color"]
        if kind == "mode":
            kind, color = station["modes"][station["state"]]
        if parcel["color"] == color:
            parcel["mark"] = kind

    def _score_parcel(self, parcel):
        expected = self.outputs[parcel["pos"]]
        if parcel["color"] != expected[0]:
            return
        self.scored.append(expected)

    def _tick(self):
        old_positions = self._occupied()
        planned = []
        for parcel in self.flight:
            nxt = self._next_cell(parcel)
            planned.append((parcel, nxt))
        targets = [nxt for _, nxt in planned if nxt is not None]
        if len(targets) != len(set(targets)):
            self.failed = True
        moving_from = {parcel["pos"] for parcel, nxt in planned if nxt is not None}
        for _, nxt in planned:
            if nxt is not None and nxt in old_positions and nxt not in moving_from:
                self.failed = True
        new_flight = []
        if not self.failed:
            for parcel, nxt in planned:
                if nxt is not None:
                    parcel["pos"] = nxt
                self._apply_station(parcel)
                if parcel["pos"] in self.outputs:
                    self._score_parcel(parcel)
                else:
                    new_flight.append(parcel)
        self.flight = new_flight
        if not self.failed and self.queue and self.queue[0]["start"] not in self._occupied():
            parcel = self.queue.pop(0)
            parcel["pos"] = parcel["start"]
            self._apply_station(parcel)
            self.flight.append(parcel)
        self.tick_count += 1
        self.steps_left -= 1

    def _toggle(self, cell):
        if cell in self.switches:
            self.switches[cell]["state"] = 1 - self.switches[cell]["state"]
            self.steps_left -= 1
        elif cell in self.stations and self.stations[cell]["kind"] == "mode":
            station = self.stations[cell]
            station["state"] = (station["state"] + 1) % len(station["modes"])
            for parcel in self.flight:
                if parcel["pos"] == cell:
                    self._apply_station(parcel)
            self.steps_left -= 1

    def _check_win(self):
        return (
            not self.failed
            and not self.queue
            and not self.flight
            and Counter(self.scored) == Counter(self.target)
        )

    def _check_delivery_loss(self):
        return (
            not self.failed
            and not self.queue
            and not self.flight
            and Counter(self.scored) != Counter(self.target)
        )

    def _put(self, canvas, x, y, color):
        if 0 <= x < self.W and 0 <= y < self.H:
            canvas[y][x] = color

    def _rect(self, canvas, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._put(canvas, xx, yy, color)

    def _draw_belt_cell(self, canvas, cell):
        x, y = self._cell_px(cell)
        self._rect(canvas, x, y, self.CELL, self.CELL, BELT)
        if (cell[0] + cell[1] + self.tick_count) % 2 == 0:
            self._put(canvas, x + 1, y + 1, BELT_DOT)
            self._put(canvas, x + 2, y + 2, BELT_DOT)

    def _draw_switch(self, canvas, cell):
        x, y = self._cell_px(cell)
        self._rect(canvas, x, y, self.CELL, self.CELL, SWITCH)
        self._draw_switch_indicator(canvas, cell)

    def _draw_switch_indicator(self, canvas, cell):
        x, y = self._cell_px(cell)
        switch = self.switches[cell]
        out = switch["outs"][switch["state"]]
        dx = out[0] - cell[0]
        dy = out[1] - cell[1]
        pts = [(1, 1), (2, 1), (1, 2), (2, 2)]
        if dx < 0:
            pts.extend([(0, 1), (0, 2)])
        elif dx > 0:
            pts.extend([(3, 1), (3, 2)])
        elif dy < 0:
            pts.extend([(1, 0), (2, 0)])
        elif dy > 0:
            pts.extend([(1, 3), (2, 3)])
        for dx, dy in pts:
            self._put(canvas, x + dx, y + dy, SELECT)
        self._put(canvas, x, y, SELECT)
        self._put(canvas, x + 3, y + 3, SELECT)

    def _draw_station(self, canvas, cell, station):
        x, y = self._cell_px(cell)
        self._rect(canvas, x, y, self.CELL, self.CELL, STATION)
        kind, color = station["kind"], station["color"]
        if kind == "mode":
            kind, color = station["modes"][station["state"]]
        color_id = COL[color]
        if kind == "stripe":
            for xx in range(x, x + self.CELL):
                self._put(canvas, xx, y + 1, color_id)
                self._put(canvas, xx, y + 3, color_id)
        elif kind == "circle":
            for dx, dy in ((1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)):
                self._put(canvas, x + dx, y + dy, color_id)
        elif kind == "square":
            self._rect(canvas, x + 1, y + 1, 2, 2, color_id)
        elif kind == "timer":
            for dx, dy in ((1, 0), (2, 0), (0, 1), (3, 1), (1, 3), (2, 3)):
                self._put(canvas, x + dx, y + dy, color_id)
            self._put(canvas, x + 2, y + 2, SELECT)

    def _draw_parcel(self, canvas, parcel):
        x, y = self._cell_px(parcel["pos"])
        color = COL[parcel["color"]]
        self._rect(canvas, x, y, self.CELL, self.CELL, color)
        if parcel["mark"] == "stripe":
            for xx in range(x, x + self.CELL):
                self._put(canvas, xx, y + 1, SELECT)
        elif parcel["mark"] == "circle":
            self._put(canvas, x + 1, y + 1, SELECT)
            self._put(canvas, x + 2, y + 1, SELECT)
        elif parcel["mark"] == "square":
            self._rect(canvas, x + 1, y + 1, 2, 2, SELECT)
        elif parcel["mark"] == "timer":
            self._put(canvas, x, y, SELECT)
            self._put(canvas, x + 3, y + 3, SELECT)

    def _draw_sig(self, canvas, sig, x, y, done=False):
        color, mark = sig
        self._rect(canvas, x, y, 4, 4, COL[color])
        if mark == "stripe":
            for xx in range(x, x + 4):
                self._put(canvas, xx, y + 1, SELECT)
        elif mark == "circle":
            self._put(canvas, x + 1, y + 1, SELECT)
            self._put(canvas, x + 2, y + 1, SELECT)
        elif mark == "square":
            self._rect(canvas, x + 1, y + 1, 2, 2, SELECT)
        elif mark == "timer":
            self._put(canvas, x, y, SELECT)
            self._put(canvas, x + 3, y + 3, SELECT)
        if done:
            self._put(canvas, x + 5, y + 1, HUD)

    def _draw_panel(self, canvas):
        for i, parcel in enumerate(self.queue[:5]):
            sx, sy = self._cell_px(parcel["start"])
            x = 2 + i * 5
            y = 53 + (i % 2) * 3
            self._draw_sig(canvas, (parcel["color"], parcel["mark"]), x, y)
            self._put(canvas, min(50, sx), y + 1, COL[parcel["color"]])
            self._put(canvas, min(50, sx + 1), y + 1, COL[parcel["color"]])

    def _sync(self):
        canvas = [[BG for _ in range(self.W)] for _ in range(self.H)]
        for cell in self.tracks:
            self._draw_belt_cell(canvas, cell)
        for cell, sig in self.outputs.items():
            x, y = self._cell_px(cell)
            self._rect(canvas, x, y, self.CELL, self.CELL, OUTLET)
            self._draw_sig(canvas, sig, x, y)
        for cell in self.switches:
            self._draw_switch(canvas, cell)
        for cell, station in self.stations.items():
            self._draw_station(canvas, cell, station)
        for parcel in self.flight:
            self._draw_parcel(canvas, parcel)
        for cell in self.switches:
            self._draw_switch_indicator(canvas, cell)
        self._draw_panel(canvas)
        self.current_level._sprites = [Sprite(canvas, "scene", layer=0).set_position(0, 0)]

    def step(self):
        if self.steps_left > 0 and not self.failed:
            if self.action.id == GameAction.ACTION5:
                self._tick()
            elif self.action.id == GameAction.ACTION6:
                grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
                if grid is not None:
                    self._toggle(self._hit_cell(*grid))
        self._sync()
        if self._check_win():
            self.next_level()
        elif self.failed or self._check_delivery_loss() or self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        rows = [[len(self.queue), len(self.flight), len(self.scored), self.tick_count]]
        rows.extend([[p["pos"][0], p["pos"][1], COL[p["color"]], 0 if p["mark"] is None else MARK_COL[p["mark"]]] for p in self.flight])
        return np.array(rows, dtype=np.int16)
