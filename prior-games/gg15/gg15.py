"""Pulse-Wire-Relay.

Click wire cells to rotate endpoints, click source pads to inject coloured
pulses, and press ACTION5 to clock every pulse one wire cell forward. Relays
open gates only after a pulse of the required colour reaches them, so later
levels require routing, launch order, and timing rather than static connection.
"""

from __future__ import annotations

from collections import defaultdict
import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
FLOOR = 11
WIRE = 5
PULSE_TRAIL = 10
GATE_CLOSED = 13
GATE_OPEN = 14
RELAY = 6
HUD_FILL = 8
HUD_EMPTY = 5

N, E, S, W = 0, 1, 2, 3
DIRS = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
OPP = {N: S, E: W, S: N, W: E}


class LeftHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps <= 0:
            return frame
        ratio = max(0.0, min(1.0, self.game.steps_left / self.game.max_steps))
        filled = int(round(frame.shape[0] * ratio))
        for y in range(frame.shape[0]):
            frame[y, 0] = HUD_FILL if y >= frame.shape[0] - filled else HUD_EMPTY
        return frame


class Gg15(NovaBaseGame):
    GRID = 12
    CELL = 5
    OX = 2
    OY = 2
    W = 64
    H = 64

    def __init__(self):
        self.hud = LeftHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.wires = {}
        self.sources = []
        self.sinks = []
        self.relays = {}
        self.gates = {}
        self.open_gates = set()
        self.pulses = []
        self.hit_sinks = set()
        self.tick_count = 0
        self.witness = []
        self.max_steps = 0
        self.steps_left = 0
        super().__init__("gg15", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[5, 6])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        self.relays = {}
        self.gates = {}
        self.open_gates = set()
        self.pulses = []
        self.hit_sinks = set()
        self.tick_count = 0
        lvl = level.get_data("Level")
        if lvl == 1:
            target = {
                (2, 5): ("straight", 1), (3, 5): ("straight", 1), (4, 5): ("bend", 2),
                (4, 6): ("straight", 0), (4, 7): ("bend", 0), (5, 7): ("straight", 1), (6, 7): ("straight", 1),
            }
            self.sources = [((1, 5), E, 12)]
            self.sinks = [((7, 7), W, 12)]
            self.witness = [("rot", (4, 5)), ("rot", (4, 5)), ("rot", (4, 5)), ("rot", (4, 7)), ("src", (1, 5)), "tick", "tick", "tick", "tick", "tick", "tick"]
        elif lvl == 2:
            target = {
                (2, 5): ("straight", 1), (3, 5): ("straight", 1), (4, 5): ("straight", 1), (5, 5): ("cross", 0),
                (6, 5): ("straight", 1), (7, 5): ("straight", 1), (8, 5): ("straight", 1),
                (5, 2): ("straight", 0), (5, 3): ("straight", 0), (5, 4): ("straight", 0),
                (5, 6): ("straight", 0), (5, 7): ("straight", 0), (5, 8): ("straight", 0),
            }
            self.sources = [((1, 5), E, 12), ((5, 1), S, 9)]
            self.sinks = [((9, 5), W, 12), ((5, 9), N, 9)]
            self.relays = {(8, 5): {"color": 12, "opens": (5, 6), "lit": False}}
            self.gates = {(5, 6): 12}
            self.witness = [("rot", (2, 5)), ("rot", (3, 5)), ("rot", (5, 2)), ("rot", (5, 3)), ("src", (1, 5)), "tick", "tick", "tick", "tick", "tick", "tick", ("src", (5, 1)), "tick", "tick", "tick", "tick", "tick", "tick"]
        else:
            target = {
                (2, 4): ("diode", E), (3, 4): ("straight", 1), (4, 4): ("straight", 1), (5, 4): ("cross", 0),
                (6, 4): ("straight", 1), (7, 4): ("straight", 1), (8, 4): ("straight", 1),
                (5, 2): ("diode", S), (5, 3): ("straight", 0), (5, 5): ("straight", 0), (5, 6): ("straight", 0), (5, 7): ("straight", 0),
                (2, 9): ("diode", E), (3, 9): ("straight", 1), (4, 9): ("straight", 1), (5, 9): ("straight", 1), (6, 9): ("straight", 1),
            }
            self.sources = [((1, 4), E, 12), ((5, 1), S, 9), ((1, 9), E, 14)]
            self.sinks = [((9, 4), W, 12), ((5, 8), N, 9), ((7, 9), W, 14)]
            self.relays = {
                (8, 4): {"color": 12, "opens": (5, 5), "lit": False},
                (6, 9): {"color": 14, "opens": (5, 7), "lit": False},
            }
            self.gates = {(5, 5): 12, (5, 7): 14}
            self.witness = [
                ("rot", (2, 4)), ("rot", (5, 2)), ("rot", (2, 9)),
                ("src", (1, 4)), "tick", "tick", "tick", "tick", "tick", "tick", "tick", "tick",
                ("src", (1, 9)), "tick", "tick", "tick", "tick",
                ("src", (5, 1)), "tick", "tick", "tick", "tick", "tick",
            ]
        self._load_scrambled(target)
        self.max_steps = len(self.witness)
        self.steps_left = self.max_steps
        self._sync()

    def _load_scrambled(self, target):
        counts = defaultdict(int)
        for item in self.witness:
            if isinstance(item, tuple) and item[0] == "rot":
                counts[item[1]] += 1
        self.wires = {}
        for pos, (kind, orient) in target.items():
            period = 1 if kind == "cross" else 2 if kind == "straight" else 4
            self.wires[pos] = {"kind": kind, "orient": (orient - counts[pos]) % period}

    def _ends(self, wire):
        kind, orient = wire["kind"], wire["orient"]
        if kind == "straight":
            return {N, S} if orient % 2 == 0 else {E, W}
        if kind == "bend":
            return [{N, E}, {E, S}, {S, W}, {W, N}][orient % 4]
        if kind == "diode":
            return {orient % 4, OPP[orient % 4]}
        return {N, E, S, W}

    def _exits(self, wire, incoming):
        if wire["kind"] == "diode":
            direction = wire["orient"] % 4
            return {direction} if incoming == OPP[direction] else set()
        if wire["kind"] == "cross":
            return {N, S} if incoming in (N, S) else {E, W}
        return self._ends(wire)

    def _rotate(self, pos):
        if pos not in self.wires or self.wires[pos]["kind"] == "cross":
            return False
        period = 2 if self.wires[pos]["kind"] == "straight" else 4
        self.wires[pos]["orient"] = (self.wires[pos]["orient"] + 1) % period
        self.steps_left -= 1
        return True

    def _launch(self, source_pos):
        for pos, direction, color in self.sources:
            if pos != source_pos:
                continue
            dx, dy = DIRS[direction]
            first = (pos[0] + dx, pos[1] + dy)
            if self._can_enter(first, OPP[direction]):
                self.pulses.append({"pos": first, "from": OPP[direction], "color": color})
                self.steps_left -= 1
                return True
        return False

    def _can_enter(self, pos, incoming):
        if pos in self.gates and pos not in self.open_gates:
            return False
        return pos in self.wires and incoming in self._ends(self.wires[pos])

    def _mark_arrival(self, pos, color):
        if pos in self.relays and self.relays[pos]["color"] == color:
            self.relays[pos]["lit"] = True
            self.open_gates.add(self.relays[pos]["opens"])
        for sink_pos, side, sink_color in self.sinks:
            dx, dy = DIRS[side]
            if (sink_pos[0] + dx, sink_pos[1] + dy) == pos and color == sink_color:
                self.hit_sinks.add(sink_pos)

    def _tick(self):
        new_pulses = []
        for pulse in self.pulses:
            pos = pulse["pos"]
            color = pulse["color"]
            self._mark_arrival(pos, color)
            wire = self.wires.get(pos)
            if wire is None:
                continue
            for direction in self._exits(wire, pulse["from"]):
                if direction == pulse["from"]:
                    continue
                dx, dy = DIRS[direction]
                nxt = (pos[0] + dx, pos[1] + dy)
                incoming = OPP[direction]
                if self._can_enter(nxt, incoming):
                    self._mark_arrival(nxt, color)
                    new_pulses.append({"pos": nxt, "from": incoming, "color": color})
                else:
                    for sink_pos, side, sink_color in self.sinks:
                        if sink_pos == nxt and side == incoming and color == sink_color:
                            self.hit_sinks.add(sink_pos)
        self.pulses = new_pulses
        self.tick_count += 1
        self.steps_left -= 1

    def _check_win(self):
        return all(pos in self.hit_sinks for pos, _, _ in self.sinks)

    def _grid_at(self, gx, gy):
        if not (self.OX <= gx < self.OX + self.GRID * self.CELL and self.OY <= gy < self.OY + self.GRID * self.CELL):
            return None
        return ((gx - self.OX) // self.CELL, (gy - self.OY) // self.CELL)

    def _cell_pos(self, x, y):
        return self.OX + x * self.CELL, self.OY + y * self.CELL

    def _wire_pixels(self, wire):
        color = WIRE
        px = [[-1] * self.CELL for _ in range(self.CELL)]
        for d in self._ends(wire):
            if d == N:
                for y in range(3):
                    px[y][2] = color
            elif d == S:
                for y in range(2, 5):
                    px[y][2] = color
            elif d == E:
                for x in range(2, 5):
                    px[2][x] = color
            else:
                for x in range(3):
                    px[2][x] = color
        px[2][2] = RELAY if wire["kind"] == "diode" else color
        return px

    def _ring_pixels(self, color, filled=False):
        px = [[-1] * self.CELL for _ in range(self.CELL)]
        for i in range(self.CELL):
            px[0][i] = px[4][i] = px[i][0] = px[i][4] = color
        if filled:
            for y in range(1, 4):
                for x in range(1, 4):
                    px[y][x] = color
        return px

    def _sync(self):
        sprites = [Sprite([[BG] * self.W for _ in range(self.H)], "bg", layer=-2).set_position(0, 0)]
        for y in range(self.GRID):
            for x in range(self.GRID):
                sprites.append(Sprite([[FLOOR] * self.CELL for _ in range(self.CELL)], f"floor_{x}_{y}", layer=-1).set_position(*self._cell_pos(x, y)))
        for pos, wire in self.wires.items():
            sprites.append(Sprite(self._wire_pixels(wire), f"wire_{pos}", layer=1).set_position(*self._cell_pos(*pos)))
        for pos in self.gates:
            color = GATE_OPEN if pos in self.open_gates else GATE_CLOSED
            sprites.append(Sprite([[color, color, color], [color, BG, color], [color, color, color]], f"gate_{pos}", layer=3).set_position(self._cell_pos(*pos)[0] + 1, self._cell_pos(*pos)[1] + 1))
        for pos, relay in self.relays.items():
            color = relay["color"] if relay["lit"] else RELAY
            sprites.append(Sprite([[color]], f"relay_{pos}", layer=4).set_position(self._cell_pos(*pos)[0] + 2, self._cell_pos(*pos)[1] + 2))
        for pulse in self.pulses:
            sprites.append(Sprite([[pulse["color"], pulse["color"], pulse["color"]], [pulse["color"], BG, pulse["color"]], [pulse["color"], pulse["color"], pulse["color"]]], f"pulse_{pulse['pos']}", layer=5).set_position(self._cell_pos(*pulse["pos"])[0] + 1, self._cell_pos(*pulse["pos"])[1] + 1))
        for pos, _, color in self.sources:
            sprites.append(Sprite(self._ring_pixels(color, True), f"source_{pos}", layer=4).set_position(*self._cell_pos(*pos)))
        for pos, _, color in self.sinks:
            sprites.append(Sprite(self._ring_pixels(color, pos in self.hit_sinks), f"sink_{pos}", layer=4).set_position(*self._cell_pos(*pos)))
        self.current_level._sprites = sprites

    def step(self):
        if self.steps_left > 0:
            if self.action.id == GameAction.ACTION5:
                self._tick()
            elif self.action.id == GameAction.ACTION6:
                grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
                cell = self._grid_at(*grid) if grid is not None else None
                if cell is not None and not self._launch(cell):
                    self._rotate(cell)
        self._sync()
        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        arr = np.zeros((self.GRID, self.GRID), dtype=np.int16)
        for (x, y), wire in self.wires.items():
            arr[y, x] = wire["orient"] + 10
        for pulse in self.pulses:
            x, y = pulse["pos"]
            arr[y, x] = pulse["color"]
        return arr
