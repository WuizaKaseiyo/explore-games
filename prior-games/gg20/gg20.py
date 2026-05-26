"""Counterweight-Beam-Balance.

Side-view mobile puzzle.  Click a tray stone, then click a pan to place it.
ACTION5 ticks sliding stones; deeper levels add cascaded beams and lock pins.
"""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 13
WOOD = 5
ROPE = 11
PAN = 8
TARGET = 14
SELECT = 15
LOCK = 10
PANEL = 5
STONE = {1: 7, 2: 6, 3: 0}
BEAM_HALF = 9
PAN_DROP = 10
TILT_PIXELS = 2


class RightHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if not self.game.max_steps:
            return frame
        filled = int(round(frame.shape[0] * max(0, self.game.steps_left) / self.game.max_steps))
        x = frame.shape[1] - 1
        for y in range(frame.shape[0]):
            frame[y, x] = TARGET if y >= frame.shape[0] - filled else WOOD
        return frame


class Gg20(NovaBaseGame):
    W = 64
    H = 64

    def __init__(self):
        self.hud = RightHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.beams = []
        self.stones = []
        self.selected = None
        self.target = []
        self.witness = []
        self.max_steps = 0
        self.steps_left = 0
        self.tick_count = 0
        super().__init__("gg20", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[5, 6])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        lvl = level.get_data("Level")
        self.selected = None
        self.tick_count = 0
        if lvl == 1:
            self.beams = [self._beam(0, 31, 17)]
            self.stones = [self._stone(1), self._stone(2), self._stone(3), self._stone(1)]
            self.witness = [("stone", 0), ("pan", 0, "left"), ("stone", 1), ("pan", 0, "right")]
        elif lvl == 2:
            self.beams = [self._beam(0, 25, 10), self._beam(1, 42, 25), self._beam(2, 27, 40)]
            self.stones = [self._stone(w) for w in [1, 2, 3, 1, 2, 1, 3, 2]]
            self.witness = [
                ("stone", 2), ("pan", 0, "left"), ("stone", 1), ("pan", 0, "right"),
                ("stone", 0), ("pan", 1, "right"), ("stone", 3), ("pan", 1, "right"),
                ("stone", 4), ("pan", 2, "left"), ("stone", 5), ("pan", 2, "right"),
            ]
        else:
            self.beams = [self._beam(0, 20, 8), self._beam(1, 43, 21), self._beam(2, 20, 34), self._beam(3, 43, 44)]
            self.stones = [self._stone(w, sliding=(i == 4)) for i, w in enumerate([3, 2, 1, 2, 1, 3, 3, 2, 2, 1, 2, 3, 3])]
            self.witness = [
                ("stone", 0), ("pan", 0, "left"), ("stone", 1), ("pan", 0, "left"),
                ("stone", 6), ("pan", 0, "right"), ("stone", 9), ("pan", 0, "right"),
                ("stone", 5), ("pan", 1, "right"), ("stone", 3), ("pan", 1, "right"),
                ("stone", 11), ("pan", 1, "left"), ("stone", 2), ("pan", 1, "left"),
                ("stone", 4), ("pan", 2, "right"), "tick", ("stone", 12), ("pan", 2, "left"),
                ("stone", 8), ("pan", 3, "right"), ("stone", 10), ("pan", 3, "right"),
                ("stone", 7), ("pan", 3, "left"),
            ]
        self.target = self._simulate_target()
        self.max_steps = len(self.witness)
        self.steps_left = self.max_steps
        self._recompute()
        self._sync()

    def _beam(self, idx, x, y, lock=False):
        return {"id": idx, "x": x, "y": y, "tilt": 0, "locked": lock}

    def _stone(self, weight, sliding=False):
        return {"weight": weight, "sliding": sliding, "loc": "tray"}

    def _weights(self, beam, side):
        return sum(s["weight"] for s in self.stones if s["loc"] == (beam, side))

    def _intended_tilt(self, b):
        return max(-2, min(2, self._weights(b["id"], "right") - self._weights(b["id"], "left")))

    def _recompute(self):
        for b in self.beams:
            b["tilt"] = 0 if b["locked"] else self._intended_tilt(b)

    def _tick(self, consume=True):
        self._recompute()
        for s in self.stones:
            if not s["sliding"] or not isinstance(s["loc"], tuple):
                continue
            beam_id, side = s["loc"]
            b = self.beams[beam_id]
            tilt = self._intended_tilt(b)
            if tilt > 0:
                s["loc"] = (beam_id, "right")
            elif tilt < 0:
                s["loc"] = (beam_id, "left")
        self.tick_count += 1
        self._recompute()
        if consume:
            self.steps_left -= 1

    def _click_stone(self, idx, consume=True):
        if 0 <= idx < len(self.stones) and self.stones[idx]["loc"] == "tray":
            self.selected = idx
            if consume:
                self.steps_left -= 1
            return True
        return False

    def _click_pan(self, beam, side, consume=True):
        if self.selected is None:
            return False
        self.stones[self.selected]["loc"] = (beam, side)
        self.selected = None
        self._recompute()
        if consume:
            self.steps_left -= 1
        return True

    def _click_lock(self, beam, consume=True):
        if 0 <= beam < len(self.beams):
            self.beams[beam]["locked"] = not self.beams[beam]["locked"]
            self._recompute()
            if consume:
                self.steps_left -= 1
            return True
        return False

    def _simulate_target(self):
        saved_stones = [dict(s) for s in self.stones]
        saved_beams = [dict(b) for b in self.beams]
        saved_selected = self.selected
        for a in self.witness:
            if a == "tick":
                self._tick(False)
            elif a[0] == "stone":
                self._click_stone(a[1], False)
            elif a[0] == "pan":
                self._click_pan(a[1], a[2], False)
            elif a[0] == "lock":
                self._click_lock(a[1], False)
        out = [b["tilt"] for b in self.beams]
        self.stones = saved_stones
        self.beams = saved_beams
        self.selected = saved_selected
        return out

    def _pan_pos(self, beam, side):
        b = self.beams[beam]
        dx = -BEAM_HALF if side == "left" else BEAM_HALF
        drop = (-b["tilt"] if side == "left" else b["tilt"]) * TILT_PIXELS
        return b["x"] + dx, b["y"] + PAN_DROP + drop

    def _hit(self, x, y):
        for i, s in enumerate(self.stones):
            if s["loc"] == "tray":
                sx, sy = self._tray_pos(i)
                if sx <= x <= sx + 3 and sy <= y <= sy + 3:
                    return ("stone", i)
        for b in self.beams:
            if b["locked"] and abs(x - b["x"]) <= 2 and abs(y - b["y"]) <= 2:
                return ("lock", b["id"])
            for side in ("left", "right"):
                px, py = self._pan_pos(b["id"], side)
                if px - 3 <= x <= px + 3 and py <= y <= py + 4:
                    return ("pan", b["id"], side)
        return None

    def _check_win(self):
        return [self._intended_tilt(b) for b in self.beams] == self.target

    def _line(self, canvas, x0, y0, x1, y1, c):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(steps + 1):
            x = round(x0 + (x1 - x0) * i / steps)
            y = round(y0 + (y1 - y0) * i / steps)
            if 0 <= x < self.W and 0 <= y < self.H:
                canvas[y][x] = c

    def _tray_pos(self, idx):
        gap = 4 if len(self.stones) > 10 else 5
        return 4 + idx * gap, 58

    def _draw_weight(self, canvas, x, y, stone, selected=False):
        color = STONE[stone["weight"]]
        for yy in range(y, y + 4):
            for xx in range(x, x + 4):
                if 0 <= xx < self.W and 0 <= yy < self.H:
                    canvas[yy][xx] = color
        for k in range(stone["weight"]):
            px = x + 1 + (k % 2)
            py = y + 1 + (k // 2)
            canvas[py][px] = TARGET
        if stone["sliding"]:
            canvas[y][x + 3] = TARGET
            canvas[y + 1][x + 3] = TARGET
        if selected:
            for i in range(4):
                canvas[y][x + i] = canvas[y + 3][x + i] = SELECT
                canvas[y + i][x] = canvas[y + i][x + 3] = SELECT

    def _draw_pan_stone(self, canvas, x, y, stone):
        color = STONE[stone["weight"]]
        coords = [(0, 0)]
        if stone["weight"] >= 2:
            coords.append((1, 0))
        if stone["weight"] >= 3:
            coords.extend([(0, -1), (1, -1)])
        for dx, dy in coords:
            xx, yy = x + dx, y + dy
            if 0 <= xx < self.W and 0 <= yy < self.H:
                canvas[yy][xx] = color
        if stone["sliding"] and 0 <= x < self.W and 0 <= y - 2 < self.H:
            canvas[y - 2][x] = TARGET

    def _target_panel(self, canvas):
        for i, target in enumerate(self.target):
            y = 8 + i * 10
            for yy in range(y - 2, y + 5):
                for xx in range(54, 63):
                    canvas[yy][xx] = BG
            for xx in range(55, 62):
                canvas[y + 2][xx] = PANEL
            canvas[y + 1][58] = TARGET
            if target < 0:
                color, x0 = TARGET, 55
            elif target > 0:
                color, x0 = TARGET, 60
            else:
                color, x0 = TARGET, 58
            canvas[y][x0] = color
            canvas[y + 1][x0] = color
            if abs(target) == 2:
                canvas[y - 1][x0] = color
            if target == 0:
                canvas[y][57] = canvas[y][59] = PAN

    def _sync(self):
        canvas = [[BG for _ in range(self.W)] for _ in range(self.H)]
        for x in range(2, 52):
            canvas[2][x] = ROPE
            canvas[56][x] = ROPE
        for b in self.beams:
            lx, ly = b["x"] - BEAM_HALF, b["y"] - b["tilt"] * TILT_PIXELS
            rx, ry = b["x"] + BEAM_HALF, b["y"] + b["tilt"] * TILT_PIXELS
            self._line(canvas, lx, ly, rx, ry, WOOD)
            canvas[b["y"]][b["x"]] = LOCK if b["locked"] else TARGET
            for side, ex, ey in (("left", lx, ly), ("right", rx, ry)):
                px, py = self._pan_pos(b["id"], side)
                self._line(canvas, ex, ey, px, py, ROPE)
                for xx in range(px - 2, px + 3):
                    if 0 <= xx < self.W and 0 <= py + 3 < self.H:
                        canvas[py + 3][xx] = PAN
                for k, s in enumerate([s for s in self.stones if s["loc"] == (b["id"], side)]):
                    sx = px - 1 + (k % 2) * 2
                    sy = py + 2 - (k // 3)
                    self._draw_pan_stone(canvas, sx, sy, s)
        for i, s in enumerate(self.stones):
            if s["loc"] == "tray":
                sx, sy = self._tray_pos(i)
                self._draw_weight(canvas, sx, sy, s, self.selected == i)
        self._target_panel(canvas)
        self.current_level._sprites = [Sprite(canvas, "scene", layer=0).set_position(0, 0)]

    def step(self):
        if self.steps_left > 0:
            if self.action.id == GameAction.ACTION5:
                self._tick()
            elif self.action.id == GameAction.ACTION6:
                grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
                hit = self._hit(*grid) if grid is not None else None
                if hit:
                    if hit[0] == "stone":
                        self._click_stone(hit[1])
                    elif hit[0] == "pan":
                        self._click_pan(hit[1], hit[2])
                    elif hit[0] == "lock":
                        self._click_lock(hit[1])
        self._sync()
        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        return np.array([self.target + [b["tilt"] for b in self.beams]], dtype=np.int16)
