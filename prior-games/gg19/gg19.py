"""Marble-Drop-Switchyard.

Side-view marble-run with switch arms, friction rugs, mixer cups, and a
one-shot track lever.  ACTION6 launches tray marbles or edits switchyard
hardware; ACTION5 advances every in-flight marble one ramp node.
"""

from __future__ import annotations

from collections import Counter
import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 13
WOOD = 5
RAMP = 11
SWITCH = 8
RUG = 10
BAD = 2
HUD = 14
PANEL = 7
COLORS = {"red": 12, "blue": 9, "gold": 10, "purple": 6, "green": 14}


class LeftHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if not self.game.max_steps:
            return frame
        filled = int(round(frame.shape[0] * max(0, self.game.steps_left) / self.game.max_steps))
        for y in range(frame.shape[0]):
            frame[y, 0] = HUD if y >= frame.shape[0] - filled else WOOD
        return frame


class Gg19(NovaBaseGame):
    W = 64
    H = 64
    CELL = 4
    OX = 1
    OY = 4

    def __init__(self):
        self.hud = LeftHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.nodes = {}
        self.switches = {}
        self.cups = {}
        self.mixers = {}
        self.rug_slots = set()
        self.rugs = set()
        self.rugs_left = 0
        self.levers = {}
        self.wires = []
        self.tray = []
        self.flight = []
        self.scored = []
        self.target = []
        self.failed = False
        self.witness = []
        self.steps_left = 0
        self.max_steps = 0
        super().__init__("gg19", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[5, 6])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        self.nodes = {}
        self.switches = {}
        self.cups = {}
        self.mixers = {}
        self.rug_slots = set()
        self.rugs = set()
        self.rugs_left = 0
        self.levers = {}
        self.wires = []
        self.flight = []
        self.scored = []
        self.failed = False
        lvl = level.get_data("Level")
        if lvl == 1:
            self._path((7, 1), (7, 3), (6, 5), (4, 8), (3, 11))
            self._path((7, 3), (8, 5), (8, 7))
            self._path((8, 7), (6, 10), (6, 11))
            self._path((8, 7), (10, 10), (10, 11))
            self.switches = {(7, 3): 0, (8, 7): 0}
            self.cups = {(3, 11): "red", (6, 11): "blue", (10, 11): "gold"}
            self.tray = ["red", "blue", "gold"]
            self.target = ["red", "blue", "gold"]
            self.witness = [("launch", 0), "tick", "tick", "tick", "tick", ("flip", (7, 3)), ("launch", 0), "tick", "tick", "tick", "tick", "tick", ("flip", (8, 7)), ("launch", 0), "tick", "tick", "tick", "tick", "tick"]
        elif lvl == 2:
            self._path((6, 1), (6, 3), (6, 5), (5, 7), (4, 9), (3, 11))
            self._path((6, 3), (8, 5), (9, 7), (10, 9), (11, 11))
            self._path((6, 5), (7, 7), (7, 9), (7, 11))
            self.switches = {(6, 3): 0, (6, 5): 0}
            self.cups = {(3, 11): "red", (7, 11): "blue", (11, 11): "gold"}
            self.rug_slots = {(6, 4), (7, 6)}
            self.rugs_left = 1
            self.wires = [((6, 3), (6, 5), 0, "control")]
            self.tray = ["red", "blue", "gold"]
            self.target = ["red", "blue", "gold"]
            self.witness = [("rug", (6, 4)), ("launch", 0), "tick", "tick", "tick", "tick", "tick", ("flip", (6, 5)), ("launch", 0), "tick", "tick", "tick", "tick", "tick", ("flip", (6, 3)), ("launch", 0), "tick", "tick", "tick", "tick", "tick"]
        else:
            self._path((7, 1), (7, 3), (5, 5), (4, 7), (4, 9))
            self._path((7, 3), (9, 5), (10, 7), (10, 9))
            self._path((4, 9), (4, 11))
            self._path((10, 9), (10, 11))
            self._path((7, 3), (7, 6), (7, 9), (7, 11))
            self.switches = {(7, 3): 0}
            self.levers = {(13, 5): False}
            self.wires = [((13, 5), (7, 3), COLORS["gold"], "gold gate")]
            self.mixers = {(4, 11): ("red", "purple", []), (10, 11): ("blue", "green", [])}
            self.cups = {(7, 11): "gold"}
            self.tray = ["red", "red", "blue", "blue", "gold"]
            self.target = ["purple", "green", "gold"]
            self.witness = [("lever", (13, 5)), ("launch", 0), "tick", "tick", "tick", "tick", "tick", ("launch", 0), "tick", "tick", "tick", "tick", "tick", ("flip", (7, 3)), ("launch", 0), "tick", "tick", "tick", "tick", "tick", ("launch", 0), "tick", "tick", "tick", "tick", "tick", ("flip", (7, 3)), ("launch", 0), "tick", "tick", "tick", "tick"]
        self.max_steps = len(self.witness)
        self.steps_left = self.max_steps
        self._sync()

    def _path(self, *cells):
        for a, b in zip(cells, cells[1:]):
            self.nodes.setdefault(a, []).append(b)
            self.nodes.setdefault(b, [])

    def _cell_to_px(self, cell):
        return self.OX + cell[0] * self.CELL, self.OY + cell[1] * self.CELL

    def _grid_at(self, x, y):
        gx, gy = (x - self.OX) // self.CELL, (y - self.OY) // self.CELL
        if 0 <= gx < 16 and 0 <= gy < 13:
            return gx, gy
        return None

    def _launch(self, idx):
        if idx < 0 or idx >= len(self.tray):
            return False
        color = self.tray.pop(idx)
        self.flight.append({"pos": (7, 1) if self.current_level.get_data("Level") != 2 else (6, 1), "color": color, "speed": 0})
        self.steps_left -= 1
        return True

    def _flip(self, cell):
        if cell in self.switches:
            self.switches[cell] = 1 - self.switches[cell]
            self.steps_left -= 1
            return True
        return False

    def _place_rug(self, cell):
        if self.rugs_left and cell in self.rug_slots and cell not in self.rugs:
            self.rugs.add(cell)
            self.rugs_left -= 1
            self.steps_left -= 1
            return True
        return False

    def _lever(self, cell):
        if cell in self.levers and not self.levers[cell]:
            self.levers[cell] = True
            self.steps_left -= 1
            return True
        return False

    def _next_cell(self, marble):
        pos = marble["pos"]
        outs = self.nodes.get(pos, [])
        if not outs:
            return None
        if pos in self.switches and len(outs) > 1:
            if self.current_level.get_data("Level") == 2 and marble["speed"] and pos == (6, 5) and (6, 4) not in self.rugs:
                return outs[0]
            if self.current_level.get_data("Level") == 3 and pos == (7, 3) and marble["color"] == "gold" and any(self.levers.values()):
                return outs[-1]
            return outs[self.switches[pos] % len(outs)]
        return outs[0]

    def _tick(self):
        new = []
        for marble in self.flight:
            if marble["pos"] not in self.rugs:
                marble["speed"] = min(1, marble["speed"] + 1)
            else:
                marble["speed"] = 0
            nxt = self._next_cell(marble)
            if nxt is None:
                self.failed = True
                continue
            marble["pos"] = nxt
            if nxt in self.rugs:
                marble["speed"] = 0
            if nxt in self.cups:
                if self.cups[nxt] == marble["color"]:
                    self.scored.append(marble["color"])
                else:
                    self.failed = True
            elif nxt in self.mixers:
                need, made, held = self.mixers[nxt]
                if marble["color"] != need:
                    self.failed = True
                else:
                    held.append(marble["color"])
                    if len(held) == 2:
                        self.scored.append(made)
                        held.clear()
            else:
                new.append(marble)
        self.flight = new
        self.steps_left -= 1

    def _check_win(self):
        return not self.failed and not self.tray and not self.flight and Counter(self.scored) == Counter(self.target)

    def _draw_cell(self, canvas, cell, color):
        x0, y0 = self._cell_to_px(cell)
        for y in range(y0, y0 + self.CELL):
            for x in range(x0, x0 + self.CELL):
                if 0 <= x < self.W and 0 <= y < self.H:
                    canvas[y][x] = color

    def _center(self, cell):
        x, y = self._cell_to_px(cell)
        return x + 2, y + 2

    def _line(self, canvas, x0, y0, x1, y1, color, dotted=False):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(steps + 1):
            if dotted and i % 2:
                continue
            x = round(x0 + (x1 - x0) * i / steps)
            y = round(y0 + (y1 - y0) * i / steps)
            if 0 <= x < self.W and 0 <= y < self.H:
                canvas[y][x] = color
                if 0 <= y + 1 < self.H and not dotted:
                    canvas[y + 1][x] = color

    def _track_node(self, canvas, cell):
        x, y = self._center(cell)
        for dx, dy in ((0, 0), (1, 0), (0, 1)):
            if 0 <= x + dx < self.W and 0 <= y + dy < self.H:
                canvas[y + dy][x + dx] = RAMP

    def _switch_icon(self, canvas, cell, state):
        x, y = self._cell_to_px(cell)
        for i in range(4):
            canvas[y][x + i] = canvas[y + 3][x + i] = SWITCH
            canvas[y + i][x] = canvas[y + i][x + 3] = SWITCH
        outs = self.nodes.get(cell, [])
        for i, nxt in enumerate(outs[:2]):
            cx, cy = self._center(cell)
            ox, oy = self._center(nxt)
            midx, midy = (cx + ox) // 2, (cy + oy) // 2
            canvas[midy][midx] = 12 if i == 0 else 9
        if outs:
            chosen = outs[state % len(outs)]
            cx, cy = self._center(cell)
            dx = 1 if chosen[0] > cell[0] else -1 if chosen[0] < cell[0] else 0
            dy = 1 if chosen[1] > cell[1] else -1 if chosen[1] < cell[1] else 0
            canvas[cy + dy][cx + dx] = HUD
            canvas[cy][cx] = HUD

    def _cup_icon(self, canvas, cell, color_name):
        x, y = self._cell_to_px(cell)
        color = COLORS[color_name]
        for i in range(4):
            canvas[y + 3][x + i] = color
            canvas[y + i][x] = color
            canvas[y + i][x + 3] = color
        canvas[y][x + 1] = canvas[y][x + 2] = HUD
        canvas[y + 1][x + 1] = canvas[y + 1][x + 2] = BG

    def _mixer_icon(self, canvas, cell, need, made, held):
        x, y = self._cell_to_px(cell)
        for i in range(4):
            canvas[y][x + i] = canvas[y + 3][x + i] = COLORS[made]
            canvas[y + i][x] = canvas[y + i][x + 3] = COLORS[made]
        canvas[y + 1][x + 1] = COLORS[need]
        canvas[y + 1][x + 2] = COLORS[need]
        canvas[y + 2][x + 1] = COLORS[need] if held else BG
        canvas[y + 2][x + 2] = COLORS[made]

    def _target_panel(self, canvas):
        x0 = 57
        for y in range(6, 30):
            canvas[y][x0 - 1] = PANEL
        for i, color_name in enumerate(self.target):
            y = 7 + i * 6
            color = COLORS[color_name]
            for yy in range(y, y + 4):
                for xx in range(x0, x0 + 5):
                    if xx < self.W:
                        canvas[yy][xx] = PANEL
            for xx, yy in ((x0, y), (x0 + 3, y), (x0, y + 3), (x0 + 3, y + 3)):
                canvas[yy][xx] = color
            if i < len(self.scored):
                canvas[y + 1][x0 + 1] = color
                canvas[y + 1][x0 + 2] = color
                canvas[y + 2][x0 + 1] = HUD
                canvas[y + 2][x0 + 2] = HUD

    def _sync(self):
        canvas = [[BG for _ in range(self.W)] for _ in range(self.H)]
        for x in range(4, 55):
            canvas[3][x] = WOOD
        for cell, outs in self.nodes.items():
            for nxt in outs:
                x0, y0 = self._center(cell)
                x1, y1 = self._center(nxt)
                self._line(canvas, x0, y0, x1, y1, WOOD)
        for cell in self.nodes:
            if cell not in self.switches and cell not in self.cups and cell not in self.mixers:
                self._track_node(canvas, cell)
        for start, end, color, _label in self.wires:
            sx, sy = self._center(start)
            ex, ey = self._center(end)
            active = True
            if start in self.levers:
                active = self.levers[start]
            self._line(canvas, sx, sy, ex, ey, color if active else WOOD, dotted=not active)
        for cell, state in self.switches.items():
            self._switch_icon(canvas, cell, state)
        for cell in self.rug_slots:
            x, y = self._cell_to_px(cell)
            for i in range(4):
                canvas[y + i][x + (i % 2)] = 6
                canvas[y + i][x + 2 + (i % 2)] = 6
        for cell in self.rugs:
            self._draw_cell(canvas, cell, RUG)
        for cell, used in self.levers.items():
            self._draw_cell(canvas, cell, 14 if used else 6)
            x, y = self._cell_to_px(cell)
            canvas[y][x] = canvas[y + 3][x + 3] = COLORS["gold"]
            canvas[y + 1][x + 2] = BG if used else BAD
        for cell, color in self.cups.items():
            self._cup_icon(canvas, cell, color)
        for cell, (need, made, held) in self.mixers.items():
            self._mixer_icon(canvas, cell, need, made, held)
        if self.current_level.get_data("Level") == 3 and any(self.levers.values()):
            for cell in [(7, 3), (7, 6), (7, 9), (7, 11)]:
                x, y = self._cell_to_px(cell)
                canvas[y][x + 3] = COLORS["gold"]
        for i, color in enumerate(self.tray):
            self._draw_cell(canvas, (1 + i, 0), COLORS[color])
        for marble in self.flight:
            x, y = self._cell_to_px(marble["pos"])
            c = COLORS[marble["color"]]
            for yy in range(y + 1, y + 3):
                for xx in range(x + 1, x + 3):
                    canvas[yy][xx] = c
            if marble["speed"]:
                canvas[y][x + 2] = BAD
        for i, color in enumerate(self.scored):
            self._draw_cell(canvas, (13, 10 - i), COLORS[color])
        self._target_panel(canvas)
        self.current_level._sprites = [Sprite(canvas, "scene", layer=0).set_position(0, 0)]

    def step(self):
        if self.steps_left > 0 and not self.failed:
            if self.action.id == GameAction.ACTION5:
                self._tick()
            elif self.action.id == GameAction.ACTION6:
                grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
                cell = self._grid_at(*grid) if grid is not None else None
                if cell is not None:
                    tray_idx = cell[0] - 1 if cell[1] == 0 else -1
                    if not self._place_rug(cell) and not self._lever(cell) and not self._flip(cell) and tray_idx >= 0:
                        self._launch(tray_idx)
        self._sync()
        if self._check_win():
            self.next_level()
        elif self.failed or self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        return np.array([[len(self.tray), len(self.flight), len(self.scored)]], dtype=np.int16)
