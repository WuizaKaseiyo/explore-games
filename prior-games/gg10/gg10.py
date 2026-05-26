"""Echo-Delay-Follower.

Move the orange lead pawn with arrow actions. The blue echo pawn replays the
lead's movement after a delay, so both targets must be reached on the same
turn. Larger scaled cells, afterimages, paired target pads, spikes, and a
delay dial make the timing relation readable.
"""

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
FLOOR_A = 11
FLOOR_B = 12
WALL = 5
WALL_HI = 13
SPIKE = 2
SPIKE_CORE = 9
LEAD = 7
FOLLOWER = 1
LEAD_TARGET = LEAD
FOLLOW_TARGET = FOLLOWER
TRAIL = 10
DIAL_ON = 6
DIAL_OFF = 13
HUD_FILL = 6
HUD_EMPTY = 1


class StepHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps:
            filled = int(frame.shape[1] * self.game.steps_left / self.game.max_steps)
            for x in range(frame.shape[1]):
                frame[0, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


class Gg10(NovaBaseGame):
    CELL = 3
    STATUS_H = 4
    DELTAS = {
        GameAction.ACTION1: (0, -1),
        GameAction.ACTION2: (0, 1),
        GameAction.ACTION3: (-1, 0),
        GameAction.ACTION4: (1, 0),
    }

    def __init__(self):
        self.hud = StepHud(self)
        levels = [Level(grid_size=(1, 1), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.grid_w = 15
        self.grid_h = 12
        self.cam_w = 45
        self.cam_h = 41
        self.lead = (0, 0)
        self.follower = (0, 0)
        self.lead_prev = None
        self.follower_prev = None
        self.lead_start = (0, 0)
        self.follower_start = (0, 0)
        self.lead_target = (0, 0)
        self.follower_target = (0, 0)
        self.delay = 2
        self.buffer = []
        self.walls = set()
        self.spikes = set()
        self.dial = False
        self.witness = []
        self.max_steps = 0
        self.steps_left = 0
        super().__init__("gg10", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[1, 2, 3, 4, 6])

    def _set_size(self, w, h):
        self.grid_w = w
        self.grid_h = h
        self.cam_w = w * self.CELL
        self.cam_h = 1 + h * self.CELL + self.STATUS_H
        self.camera.width = self.cam_w
        self.camera.height = self.cam_h
        self.current_level._grid_size = (self.cam_w, self.cam_h)

    def _border_walls(self, w, h):
        walls = {(x, 0) for x in range(w)} | {(x, h - 1) for x in range(w)}
        walls |= {(0, y) for y in range(h)} | {(w - 1, y) for y in range(h)}
        return walls

    def on_set_level(self, level: Level) -> None:
        lvl = level.get_data("Level")
        if lvl == 1:
            self._set_size(15, 12)
            self.walls = self._border_walls(15, 12) | {(7, y) for y in range(2, 10) if y != 5}
            self.spikes = set()
            self.lead_start = (2, 5)
            self.follower_start = (2, 8)
            self.delay = 2
            self.dial = False
            self.witness = [
                GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION1,
                GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4,
            ]
        elif lvl == 2:
            self._set_size(17, 14)
            self.walls = self._border_walls(17, 14)
            self.walls |= {(8, y) for y in range(2, 12) if y not in (3, 10)}
            self.walls |= {(x, 7) for x in range(4, 15) if x not in (10, 12)}
            self.spikes = set()
            self.lead_start = (2, 3)
            self.follower_start = (2, 10)
            self.delay = 2
            self.dial = False
            self.witness = [GameAction.ACTION4] * 10 + [GameAction.ACTION2] * 3 + [GameAction.ACTION3] * 2 + [GameAction.ACTION2]
        else:
            self._set_size(19, 16)
            self.walls = self._border_walls(19, 16)
            self.walls |= {(9, y) for y in range(2, 14) if y not in (4, 11)}
            self.walls |= {(14, y) for y in range(2, 14) if y not in (6, 11)}
            self.walls |= {(x, 8) for x in range(4, 16) if x not in (6, 12)}
            self.spikes = {(6, 11), (13, 6), (16, 11), (5, 5)}
            self.lead_start = (2, 4)
            self.follower_start = (2, 11)
            self.delay = 2
            self.dial = True
            self.witness = [
                GameAction.ACTION6,
                GameAction.ACTION2, GameAction.ACTION4, GameAction.ACTION2, GameAction.ACTION4, GameAction.ACTION2, GameAction.ACTION4,
                GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION2, GameAction.ACTION3,
                GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION3, GameAction.ACTION1, GameAction.ACTION2,
                GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION1, GameAction.ACTION1, GameAction.ACTION1, GameAction.ACTION1,
                GameAction.ACTION2, GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4,
            ]
        self.lead = self.lead_start
        self.follower = self.follower_start
        self.lead_prev = None
        self.follower_prev = None
        self.buffer = []
        self.max_steps = len(self.witness)
        self.lead_target, self.follower_target = self._simulate_walk(self.witness)
        self.lead = self.lead_start
        self.follower = self.follower_start
        self.lead_prev = None
        self.follower_prev = None
        self.buffer = []
        self.delay = 2
        self.steps_left = self.max_steps
        self._sync()

    def _blocked(self, pos):
        x, y = pos
        return x < 0 or y < 0 or x >= self.grid_w or y >= self.grid_h or pos in self.walls

    def _step_pos(self, pos, delta):
        nxt = (pos[0] + delta[0], pos[1] + delta[1])
        return pos if self._blocked(nxt) else nxt

    def _move(self, action):
        delta = self.DELTAS[action]
        self.lead_prev = self.lead
        self.follower_prev = self.follower
        self.lead = self._step_pos(self.lead, delta)
        self.buffer.append(delta)
        if len(self.buffer) > self.delay:
            self.follower = self._step_pos(self.follower, self.buffer.pop(0))
        if self.follower in self.spikes:
            self.follower = self.follower_start
            self.buffer = []
        self.steps_left -= 1

    def _cycle_delay(self):
        if not self.dial:
            return False
        self.delay = 1 if self.delay == 3 else self.delay + 1
        self.buffer = self.buffer[-self.delay:]
        self.steps_left -= 1
        return True

    def _simulate_walk(self, walk):
        saved = (self.lead, self.follower, self.lead_prev, self.follower_prev, list(self.buffer), self.delay, self.steps_left)
        self.lead = self.lead_start
        self.follower = self.follower_start
        self.lead_prev = None
        self.follower_prev = None
        self.buffer = []
        self.delay = 2
        self.steps_left = 999
        for action in walk:
            if action == GameAction.ACTION6:
                self._cycle_delay()
            else:
                self._move(action)
        result = (self.lead, self.follower)
        self.lead, self.follower, self.lead_prev, self.follower_prev, self.buffer, self.delay, self.steps_left = saved
        return result

    def _cell_to_pixel(self, x, y):
        return x * self.CELL, 1 + y * self.CELL

    def _floor_pixels(self, x, y):
        c = FLOOR_A if (x + y) % 2 == 0 else FLOOR_B
        return [[c, c, c], [c, FLOOR_A, c], [c, c, c]]

    def _wall_pixels(self):
        return [[WALL, WALL_HI, WALL], [WALL, WALL, WALL], [WALL_HI, WALL, WALL]]

    def _target_pixels(self, color):
        return [[color, -1, color], [-1, color, -1], [color, -1, color]]

    def _pawn_pixels(self, color):
        return [[-1, color, -1], [color, color, color], [-1, color, TRAIL]]

    def _trail_pixels(self):
        return [[-1, TRAIL, -1], [TRAIL, -1, TRAIL], [-1, TRAIL, -1]]

    def _spike_pixels(self):
        return [[-1, SPIKE, -1], [SPIKE, SPIKE_CORE, SPIKE], [-1, SPIKE, -1]]

    def _sync(self):
        sprites = [Sprite([[BG] * self.cam_w for _ in range(self.cam_h)], "bg", layer=0).set_position(0, 0)]
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                px, py = self._cell_to_pixel(x, y)
                pixels = self._wall_pixels() if (x, y) in self.walls else self._floor_pixels(x, y)
                sprites.append(Sprite(pixels, f"cell_{x}_{y}", layer=1).set_position(px, py))
        for x, y in self.spikes:
            px, py = self._cell_to_pixel(x, y)
            sprites.append(Sprite(self._spike_pixels(), f"spike_{x}_{y}", layer=3).set_position(px, py))
        for pos, color, name in [(self.lead_target, LEAD_TARGET, "lead_target"), (self.follower_target, FOLLOW_TARGET, "follower_target")]:
            px, py = self._cell_to_pixel(*pos)
            sprites.append(Sprite(self._target_pixels(color), name, layer=4).set_position(px, py))
        for pos in (self.lead_prev, self.follower_prev):
            if pos is not None:
                px, py = self._cell_to_pixel(*pos)
                sprites.append(Sprite(self._trail_pixels(), f"trail_{pos}", layer=5).set_position(px, py))
        fx, fy = self.follower
        px, py = self._cell_to_pixel(fx, fy)
        sprites.append(Sprite(self._pawn_pixels(FOLLOWER), "follower", layer=6).set_position(px, py))
        lx, ly = self.lead
        px, py = self._cell_to_pixel(lx, ly)
        sprites.append(Sprite(self._pawn_pixels(LEAD), "lead", layer=7).set_position(px, py))

        status_y = 1 + self.grid_h * self.CELL
        for i, delta in enumerate(self.buffer[-3:]):
            color = {(-1, 0): 3, (1, 0): 4, (0, -1): 7, (0, 1): 9}.get(delta, DIAL_OFF)
            sprites.append(Sprite([[color] * 3 for _ in range(3)], f"buffer_{i}", layer=4).set_position(2 + i * 4, status_y))
        if self.dial:
            for d in range(1, 4):
                color = DIAL_ON if d == self.delay else DIAL_OFF
                sprites.append(Sprite([[color] * 3 for _ in range(3)], f"dial_{d}", layer=4).set_position(self.cam_w - 14 + d * 4, status_y))
        self.current_level._sprites = sprites

    def step(self):
        if self.action.id in self.DELTAS and self.steps_left > 0:
            self._move(self.action.id)
        elif self.action.id == GameAction.ACTION6 and self.steps_left > 0:
            self._cycle_delay()
        self._sync()
        if self.lead == self.lead_target and self.follower == self.follower_target:
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        return np.array([[*self.lead, *self.follower, self.delay]], dtype=np.int16)
