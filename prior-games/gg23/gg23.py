"""Braid-Strand-Weave.

Textile topology puzzle. ACTION6 cycles crossings between straight,
left-over, and right-over. Active crossings swap adjacent strand lanes, so the
bottom tapestry depends on braid topology. Later levels add dye transfer.
"""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
WEFT = 5
SHADOW = 8
HILITE = 15
FRAME = 7
LOCK = 10

DYE_COLOR = {
    1: 12,
    2: 9,
    3: 13,
    4: 14,
    5: 10,
    6: 11,
    7: 15,
    8: 6,
    9: 3,
    10: 4,
    11: 15,
    12: 10,
    13: 15,
    14: 15,
    15: 15,
}


class BottomHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if not self.game.max_steps:
            return frame

        filled = int(
            round(
                frame.shape[1]
                * max(0, self.game.steps_left)
                / self.game.max_steps
            )
        )
        y = frame.shape[0] - 1

        for x in range(frame.shape[1]):
            frame[y, x] = HILITE if x < filled else SHADOW

        return frame


LEVELS = [
    {
        "slot_x": [12, 28, 44],
        "bits": [1, 2, 8],
        "crossings": [(16, 0), (31, 1), (46, 0)],
        "solution": [1, 2, 0],
        "rule": "order",
        "max_steps": 9,
    },
    {
        "slot_x": [8, 22, 36, 50],
        "bits": [1, 2, 4, 8],
        "crossings": [(13, 1), (23, 0), (33, 2), (45, 1)],
        "solution": [2, 1, 1, 2],
        "rule": "dye",
        "max_steps": 15,
    },
    {
        "slot_x": [8, 22, 36, 50],
        "bits": [1, 2, 4, 8],
        "crossings": [(12, 0), (20, 2), (28, 1), (36, 0), (44, 2), (52, 1)],
        "solution": [1, 2, 1, 1, 2, 2],
        "rule": "dye",
        "max_steps": 12,
    },
]


class Gg23(NovaBaseGame):
    W = 64
    H = 64
    TOP = 6
    BOTTOM = 58
    GAP = 4

    def __init__(self):
        self.hud = BottomHud(self)

        levels = [
            Level(
                grid_size=(self.W, self.H),
                sprites=[],
                data={**data, "Level": i + 1},
            )
            for i, data in enumerate(LEVELS)
        ]

        self.slot_x = []
        self.bits = []
        self.crossings = []
        self.states = []
        self.solution = []
        self.target_order = []
        self.target_dyes = {}
        self.target_states = []
        self.max_steps = 0
        self.steps_left = 0
        self.failed = False

        super().__init__(
            "gg23",
            levels,
            Camera(background=BG, letter_box=BG, interfaces=[self.hud]),
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)

        self.slot_x = list(level.get_data("slot_x"))
        self.bits = list(level.get_data("bits"))
        self.crossings = list(level.get_data("crossings"))
        self.states = [0 for _ in self.crossings]
        self.solution = list(level.get_data("solution"))
        self.target_states = (
            list(self.solution)
            if level.get_data("rule") == "state"
            else []
        )

        self.max_steps = level.get_data("max_steps")
        self.steps_left = self.max_steps
        self.failed = False

        self.target_order, self.target_dyes = self._evaluate(self.solution)
        self._sync()

    def _evaluate(self, states=None):
        states = self.states if states is None else states

        order = list(range(len(self.bits)))
        dyes = {sid: self.bits[sid] for sid in order}

        for idx, state in enumerate(states):
            lane = self.crossings[idx][1]

            if state == 0:
                continue

            left = order[lane]
            right = order[lane + 1]

            top = left if state == 1 else right
            under = right if state == 1 else left

            if self.current_level.get_data("rule") == "dye":
                dyes[under] |= self.bits[top]

            order[lane], order[lane + 1] = order[lane + 1], order[lane]

        return order, dyes

    def _check_win(self):
        order, dyes = self._evaluate()
        rule = self.current_level.get_data("rule")

        if order != self.target_order:
            return False

        if rule == "state" and self.states != self.target_states:
            return False

        if rule == "dye":
            if any(dyes[sid] != self.target_dyes[sid] for sid in dyes):
                return False

        return True

    def _put(self, canvas, x, y, color):
        if 0 <= x < self.W and 0 <= y < self.H:
            canvas[y][x] = color

    def _rect(self, canvas, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._put(canvas, xx, yy, color)

    def _dot(self, canvas, x, y, color, radius=1):
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if abs(dx) + abs(dy) <= radius + 1:
                    self._put(canvas, x + dx, y + dy, color)

    def _line(self, canvas, x0, y0, x1, y1, color, radius=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0

        while True:
            self._dot(canvas, x, y, color, radius)

            if x == x1 and y == y1:
                break

            e2 = 2 * err

            if e2 >= dy:
                err += dy
                x += sx

            if e2 <= dx:
                err += dx
                y += sy

    def _strand_color(self, sid, dyes=None):
        bit = self.bits[sid] if dyes is None else dyes[sid]
        return DYE_COLOR.get(bit, HILITE)

    def _draw_ribbon(self, canvas, sid, x0, y0, x1, y1, dyes=None, top=True):
        color = self._strand_color(sid, dyes)

        self._line(canvas, x0 + 1, y0 + 1, x1 + 1, y1 + 1, SHADOW, 2)
        self._line(canvas, x0, y0, x1, y1, color, 2)

        if top:
            self._line(canvas, x0, y0, x1, y1, HILITE, 0)

    def _draw_target_chip(self, canvas, bit, x, y):
        color = DYE_COLOR.get(bit, HILITE)

        self._rect(canvas, x - 3, y - 2, 7, 5, FRAME)
        self._rect(canvas, x - 2, y - 1, 5, 3, color)
        self._put(canvas, x, y, HILITE)

    def _draw_crossing_lock(self, canvas, x1, x2, y, state, target=None):
        cx = (x1 + x2) // 2
        self._rect(canvas, cx - 3, y - 3, 7, 7, FRAME)

        color = HILITE if target is not None and state == target else LOCK

        if state == 1:
            self._line(canvas, cx - 2, y - 1, cx + 2, y + 1, color, 0)
        elif state == 2:
            self._line(canvas, cx + 2, y - 1, cx - 2, y + 1, color, 0)
        else:
            self._line(canvas, cx - 2, y, cx + 2, y, color, 0)

    def _draw_scene(self):
        canvas = [[BG for _ in range(self.W)] for _ in range(self.H)]

        for y in range(0, self.H, 4):
            for x in range(0, self.W, 4):
                canvas[y][x] = WEFT

        for y in range(3, self.H, 8):
            self._line(canvas, 2, y, self.W - 3, y, WEFT, 0)

        order = list(range(len(self.bits)))
        _, dyes = self._evaluate()
        live_dyes = {sid: self.bits[sid] for sid in range(len(self.bits))}
        last_y = self.TOP

        for idx, (y, lane) in enumerate(self.crossings):
            state = self.states[idx]
            top_y = y - self.GAP
            bot_y = y + self.GAP

            for pos, sid in enumerate(order):
                x = self.slot_x[pos]
                self._draw_ribbon(canvas, sid, x, last_y, x, top_y, live_dyes)

            x1 = self.slot_x[lane]
            x2 = self.slot_x[lane + 1]

            for pos, sid in enumerate(order):
                if pos not in (lane, lane + 1):
                    x = self.slot_x[pos]
                    self._draw_ribbon(canvas, sid, x, top_y, x, bot_y, live_dyes)

            left = order[lane]
            right = order[lane + 1]

            if state == 0:
                self._draw_ribbon(canvas, left, x1, top_y, x1, bot_y, live_dyes)
                self._draw_ribbon(canvas, right, x2, top_y, x2, bot_y, live_dyes)
            else:
                top_sid = left if state == 1 else right
                under_sid = right if state == 1 else left

                under_from = (x2, top_y) if under_sid == right else (x1, top_y)
                under_to = (x1, bot_y) if under_sid == right else (x2, bot_y)
                top_from = (x1, top_y) if top_sid == left else (x2, top_y)
                top_to = (x2, bot_y) if top_sid == left else (x1, bot_y)

                self._draw_ribbon(
                    canvas,
                    under_sid,
                    *under_from,
                    *under_to,
                    live_dyes,
                    top=False,
                )
                self._draw_ribbon(
                    canvas,
                    top_sid,
                    *top_from,
                    *top_to,
                    live_dyes,
                    top=True,
                )

                if self.current_level.get_data("rule") == "dye":
                    live_dyes[under_sid] |= self.bits[top_sid]

                order[lane], order[lane + 1] = order[lane + 1], order[lane]

            target = (
                self.solution[idx]
                if self.current_level.get_data("rule") == "state"
                else None
            )
            self._draw_crossing_lock(canvas, x1, x2, y, state, target)

            last_y = bot_y

        for pos, sid in enumerate(order):
            x = self.slot_x[pos]
            self._draw_ribbon(canvas, sid, x, last_y, x, self.BOTTOM, live_dyes)

        for pos, bit in enumerate(self.bits):
            x = self.slot_x[pos]
            self._rect(canvas, x - 5, self.TOP - 5, 11, 5, FRAME)
            self._rect(canvas, x - 4, self.TOP - 4, 9, 3, DYE_COLOR[bit])
            self._put(canvas, x, self.TOP - 3, HILITE)

        for pos, sid in enumerate(self.target_order):
            x = self.slot_x[pos]
            y = self.BOTTOM + 1
            self._draw_target_chip(canvas, self.target_dyes[sid], x, y)

        self.current_level._sprites = [
            Sprite(canvas, "scene", layer=0).set_position(0, 0)
        ]

    def _sync(self):
        self._draw_scene()

    def _crossing_at(self, gx, gy):
        for idx, (y, lane) in enumerate(self.crossings):
            x1 = self.slot_x[lane]
            x2 = self.slot_x[lane + 1]
            cx = (x1 + x2) // 2

            if abs(gx - cx) <= 5 and abs(gy - y) <= 5:
                return idx

        return None

    def _click(self, gx, gy):
        idx = self._crossing_at(gx, gy)

        if idx is not None:
            self.states[idx] = (self.states[idx] + 1) % 3
            self.steps_left -= 1

    def step(self):
        if self.steps_left > 0 and not self.failed:
            if self.action.id == GameAction.ACTION6:
                grid = self.camera.display_to_grid(
                    self.action.data.get("x", -1),
                    self.action.data.get("y", -1),
                )

                if grid is not None:
                    self._click(*grid)

        self._sync()

        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()

        self.complete_action()

    def _get_hidden_state(self):
        order, dyes = self._evaluate()

        rows = [[self.steps_left, *self.states[:6]]]
        rows.append(order + [0] * (6 - len(order)))
        rows.append(
            [dyes[sid] for sid in range(len(self.bits))]
            + [0] * (6 - len(self.bits))
        )

        return np.array(rows, dtype=np.int16)