"""Pendulum-Sync-Rail.

Side-view phase puzzle.  Click coloured pendulum bobs to shove their
phase forward; ACTION5 ticks the shared rail.  Later levels add rail
coupling, a heavy bob, and a one-way damper clip.
"""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 13
RAIL = 5
ROPE = 11
TARGET = 15
HUD = 8
EMPTY = 0
CLIP = 7
HEAVY = 0
PHASE_SEQ = [-2, -1, 0, 1, 2, 1, 0, -1]


class BottomHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps <= 0:
            return frame
        filled = int(round(frame.shape[1] * max(0, self.game.steps_left) / self.game.max_steps))
        y = frame.shape[0] - 1
        for x in range(frame.shape[1]):
            frame[y, x] = HUD if x < filled else EMPTY
        return frame


class Gg18(NovaBaseGame):
    W = 64
    H = 64

    def __init__(self):
        self.hud = BottomHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.pendulums = []
        self.couplings = []
        self.target = []
        self.tick_count = 0
        self.witness = []
        self.max_steps = 0
        self.steps_left = 0
        self.snap = False
        super().__init__("gg18", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[5, 6])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        lvl = level.get_data("Level")
        if lvl == 1:
            self.pendulums = [
                self._pend(13, 2, 12), self._pend(27, 5, 10), self._pend(41, 4, 14)
            ]
            self.couplings = []
            self.witness = [("push", 0), ("push", 2), ("push", 2), "tick", "tick"]
        elif lvl == 2:
            self.pendulums = [
                self._pend(10, 1, 12, segment=0), self._pend(23, 6, 10, segment=0),
                self._pend(38, 0, 14, segment=1), self._pend(51, 3, 9, segment=1),
            ]
            self.couplings = [(0, 1), (2, 3)]
            self.witness = [("push", 1), ("push", 1), "tick", ("push", 0), ("push", 3), "tick", "tick", ("push", 2), "tick"]
        else:
            self.pendulums = [
                self._pend(8, 3, 12, segment=0), self._pend(19, 7, 10, segment=0, clip=True),
                self._pend(30, 1, 14, segment=0, heavy=True), self._pend(43, 6, 9, segment=1),
                self._pend(55, 0, 6, segment=2),
            ]
            self.couplings = [(0, 1), (1, 2)]
            self.witness = [
                ("push", 2), ("push", 2), ("push", 1), ("push", 1), "tick",
                "tick", ("push", 2), ("push", 2), ("push", 0),
                "tick", ("push", 4), ("push", 4), "tick", "tick",
            ]
        self.target = self._simulate_target()
        self.max_steps = len(self.witness)
        self.steps_left = self.max_steps
        self.tick_count = 0
        self.snap = False
        self._sync()

    def _pend(self, x, idx, color, segment=0, heavy=False, clip=False):
        return {"x": x, "idx": idx, "color": color, "segment": segment, "heavy": heavy, "charge": 0, "clip": clip, "clipped": False, "armed": False}

    def _phase(self, p):
        return PHASE_SEQ[p["idx"] % len(PHASE_SEQ)]

    def _advance_idx(self, p, n=1):
        p["idx"] = (p["idx"] + n) % len(PHASE_SEQ)

    def _pull_toward(self, idx, target_phase):
        phase = self._phase(self.pendulums[idx])
        current_gap = abs(target_phase - phase)
        forward_idx = (self.pendulums[idx]["idx"] + 1) % len(PHASE_SEQ)
        forward_gap = abs(target_phase - PHASE_SEQ[forward_idx])
        if forward_gap < current_gap:
            self.pendulums[idx]["idx"] = forward_idx

    def _tick(self, consume=True):
        for p in self.pendulums:
            if not p["clipped"]:
                self._advance_idx(p)
        pulls = []
        for a, b in self.couplings:
            if self.pendulums[a]["clipped"] or self.pendulums[b]["clipped"]:
                continue
            pa, pb = self._phase(self.pendulums[a]), self._phase(self.pendulums[b])
            if abs(pa - pb) >= 2:
                pulls.append((a, pb))
                pulls.append((b, pa))
        for idx, phase in pulls:
            self._pull_toward(idx, phase)
        self.tick_count += 1
        if consume:
            self.steps_left -= 1

    def _push(self, idx, consume=True):
        if not (0 <= idx < len(self.pendulums)):
            return False
        p = self.pendulums[idx]
        if p["clip"] and p["armed"]:
            p["clipped"] = True
            p["armed"] = False
            if consume:
                self.steps_left -= 1
            return True
        if p["clip"] and not p["armed"] and self.current_level.get_data("Level") == 3:
            p["armed"] = True
            if consume:
                self.steps_left -= 1
            return True
        if p["heavy"]:
            p["charge"] += 1
            if p["charge"] >= 2:
                p["charge"] = 0
                self._advance_idx(p)
        else:
            self._advance_idx(p)
        if consume:
            self.steps_left -= 1
        return True

    def _simulate_target(self):
        saved = [dict(p) for p in self.pendulums]
        saved_tick = self.tick_count
        for action in self.witness:
            if action == "tick":
                self._tick(False)
            else:
                self._push(action[1], False)
        target = [self._phase(p) for p in self.pendulums]
        self.pendulums = saved
        self.tick_count = saved_tick
        return target

    def _bob_pos(self, p):
        phase = self._phase(p)
        return p["x"] + phase * 3, 39 + abs(phase)

    def _hit_pendulum(self, x, y):
        for i, p in enumerate(self.pendulums):
            bx, by = self._bob_pos(p)
            if bx - 2 <= x <= bx + 2 and by - 2 <= y <= by + 2:
                return i
        return None

    def _check_win(self):
        return [self._phase(p) for p in self.pendulums] == self.target

    def _line(self, canvas, x0, y0, x1, y1, color):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            if 0 <= x0 < self.W and 0 <= y0 < self.H:
                canvas[y0][x0] = color
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def _sync(self):
        canvas = [[BG for _ in range(self.W)] for _ in range(self.H)]
        for x in range(3, 61):
            canvas[12][x] = RAIL
            if x % 7 == 0:
                canvas[11][x] = RAIL
        for a, b in self.couplings:
            x = (self.pendulums[a]["x"] + self.pendulums[b]["x"]) // 2
            canvas[10][x] = TARGET
        for p in self.pendulums:
            bx, by = self._bob_pos(p)
            self._line(canvas, p["x"], 13, bx, by, ROPE)
            if p["clip"]:
                cy = (by + 13) // 2
                canvas[cy][(p["x"] + bx) // 2] = CLIP if not p["clipped"] else TARGET
            for yy in range(by - 1, by + 2):
                for xx in range(bx - 1, bx + 2):
                    if 0 <= xx < self.W and 0 <= yy < self.H:
                        canvas[yy][xx] = p["color"]
            if p["heavy"]:
                for xx, yy in ((bx - 2, by), (bx + 2, by), (bx, by - 2), (bx, by + 2)):
                    if 0 <= xx < self.W and 0 <= yy < self.H:
                        canvas[yy][xx] = HEAVY
            if p["armed"]:
                canvas[max(0, by - 3)][bx] = TARGET
        for i, target in enumerate(self.target):
            x0 = 8 + i * 11
            y0 = 53
            for k, phase in enumerate([-2, -1, 0, 1, 2]):
                canvas[y0][x0 + k] = ROPE
                if phase == target:
                    canvas[y0 - 1][x0 + k] = TARGET
            current = self._phase(self.pendulums[i])
            canvas[y0 + 1][x0 + current + 2] = self.pendulums[i]["color"]
        self.current_level._sprites = [Sprite(canvas, "scene", layer=0).set_position(0, 0)]

    def step(self):
        if self.steps_left > 0:
            if self.action.id == GameAction.ACTION5:
                self._tick()
            elif self.action.id == GameAction.ACTION6:
                grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
                if grid is not None:
                    hit = self._hit_pendulum(*grid)
                    if hit is not None:
                        self._push(hit)
        self._sync()
        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        return np.array([[self._phase(p) for p in self.pendulums]], dtype=np.int16)
