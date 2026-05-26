"""Chromatic-Drip-Labyrinth."""

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
FLOOR_A = 11
FLOOR_B = 12
WALL = 5
STONE = 13
GLINT = 14
TARGET_RING = 10
MIXER_FRAME = 8
GATE_FRAME = 10
GATE_CORE = 14
HUD_FILL = 6
HUD_EMPTY = 1

COLORS = {"r": 2, "y": 4, "g": 3, "p": 9}
MIX = {
    ("r", "y"): "g",
    ("y", "r"): "g",
    ("g", "p"): "y",
    ("p", "g"): "y",
    ("y", "p"): "p",
    ("p", "y"): "p",
    ("r", "p"): "p",
    ("p", "r"): "p",
}


class StepHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps:
            filled = int(frame.shape[1] * self.game.steps_left / self.game.max_steps)
            for x in range(frame.shape[1]):
                frame[0, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


class Gg13(NovaBaseGame):
    GRID_W = 12
    GRID_H = 12
    CELL = 4
    WIDTH = GRID_W * CELL
    HEIGHT = 1 + GRID_H * CELL + 3
    DELTAS = {
        GameAction.ACTION1: (0, -1),
        GameAction.ACTION2: (0, 1),
        GameAction.ACTION3: (-1, 0),
        GameAction.ACTION4: (1, 0),
    }

    def __init__(self):
        self.hud = StepHud(self)
        levels = [Level(grid_size=(self.WIDTH, self.HEIGHT), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.pos = (1, 1)
        self.color = "r"
        self.paint = {}
        self.targets = {}
        self.mixers = {}
        self.gates = {}
        self.walls = set()
        self.witness = []
        self.max_steps = 0
        self.steps_left = 0
        super().__init__("gg13", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[1, 2, 3, 4])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.WIDTH
        self.camera.height = self.HEIGHT
        self.current_level._grid_size = (self.WIDTH, self.HEIGHT)
        lvl = level.get_data("Level")
        self.walls = {(x, 0) for x in range(self.GRID_W)} | {(x, self.GRID_H - 1) for x in range(self.GRID_W)}
        self.walls |= {(0, y) for y in range(self.GRID_H)} | {(self.GRID_W - 1, y) for y in range(self.GRID_H)}
        self.paint = {}
        self.gates = {}
        if lvl == 1:
            self.pos, self.color = (2, 6), "r"
            self.walls |= {(6, 6), (6, 7), (6, 8), (3, 4), (4, 4)}
            self.mixers = {(4, 6): "y"}
            self.gates = {(7, 5): "g"}
            self.targets = {(3, 6): "r", (4, 6): "g", (7, 5): "g", (8, 5): "g"}
            self.witness = [GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4]
        elif lvl == 2:
            self.pos, self.color = (2, 8), "r"
            self.walls |= {
                (7, 7), (7, 8), (7, 9), (3, 6), (4, 6), (5, 6),
                (9, 4), (9, 5), (2, 4), (8, 10), (9, 10),
            }
            self.mixers = {(4, 8): "y", (9, 8): "p"}
            self.gates = {(7, 6): "g", (9, 7): "y"}
            self.targets = {(3, 8): "r", (4, 8): "g", (6, 8): "g", (7, 6): "g", (9, 7): "y", (10, 7): "y"}
            self.witness = [
                GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION1, GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION4, GameAction.ACTION1, GameAction.ACTION4,
            ]
        else:
            self.pos, self.color = (2, 9), "r"
            self.walls |= {
                (3, 6), (4, 6), (5, 6), (5, 7), (5, 8),
                (7, 9), (8, 9), (9, 9), (10, 9),
                (2, 4), (3, 4), (6, 3), (6, 4), (6, 5),
            }
            self.mixers = {(4, 9): "y", (8, 7): "p", (8, 4): "p"}
            self.gates = {(6, 8): "g", (8, 7): "g", (9, 6): "y", (9, 4): "p"}
            self.targets = {
                (3, 9): "r", (4, 9): "g", (6, 8): "g", (8, 7): "y",
                (9, 6): "y", (9, 7): "y", (8, 4): "p", (9, 4): "p",
            }
            self.witness = [
                GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION1, GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION4,
                GameAction.ACTION1, GameAction.ACTION4, GameAction.ACTION2,
                GameAction.ACTION3, GameAction.ACTION3, GameAction.ACTION1, GameAction.ACTION1,
                GameAction.ACTION3, GameAction.ACTION3, GameAction.ACTION3, GameAction.ACTION1,
                GameAction.ACTION4, GameAction.ACTION4,
            ]
        self.paint[self.pos] = self.color
        self.max_steps = len(self.witness)
        self.steps_left = self.max_steps
        self._sync()

    def _cell_to_pixel(self, x, y):
        return x * self.CELL, 1 + y * self.CELL

    def _tile_pixels(self, x, y):
        a = FLOOR_A if (x + y) % 2 == 0 else FLOOR_B
        return [[a, a, a, a], [a, FLOOR_A, FLOOR_A, a], [a, FLOOR_A, FLOOR_A, a], [a, a, a, a]]

    def _wall_pixels(self):
        return [[WALL, STONE, WALL, WALL], [WALL, WALL, WALL, STONE], [STONE, WALL, WALL, WALL], [WALL, WALL, STONE, WALL]]

    def _paint_pixels(self, color_key):
        c = COLORS[color_key]
        return [[-1, c, c, -1], [c, c, c, c], [c, c, c, c], [-1, c, c, -1]]

    def _ring_pixels(self, color_key):
        c = COLORS[color_key]
        return [[TARGET_RING, c, c, TARGET_RING], [c, -1, -1, c], [c, -1, -1, c], [TARGET_RING, c, c, TARGET_RING]]

    def _mixer_pixels(self, color_key):
        c = COLORS[color_key]
        return [[-1, MIXER_FRAME, MIXER_FRAME, -1], [MIXER_FRAME, c, c, MIXER_FRAME], [MIXER_FRAME, c, c, MIXER_FRAME], [-1, MIXER_FRAME, MIXER_FRAME, -1]]

    def _gate_pixels(self, color_key, open_gate):
        c = COLORS[color_key]
        core = GATE_CORE if open_gate else WALL
        return [[GATE_FRAME, c, c, GATE_FRAME], [c, core, core, c], [c, core, core, c], [GATE_FRAME, c, c, GATE_FRAME]]

    def _droplet_pixels(self):
        c = COLORS[self.color]
        return [[-1, c, c, -1], [c, c, GLINT, c], [c, c, c, c], [-1, c, c, -1]]

    def _move(self, action):
        dx, dy = self.DELTAS[action]
        nxt = (self.pos[0] + dx, self.pos[1] + dy)
        gate_req = self.gates.get(nxt)
        if nxt not in self.walls and (gate_req is None or gate_req == self.color):
            self.pos = nxt
            if nxt in self.mixers:
                self.color = MIX.get((self.color, self.mixers.pop(nxt)), self.color)
            self.paint[self.pos] = self.color
        self.steps_left -= 1

    def _sync(self):
        sprites = [Sprite([[BG] * self.WIDTH for _ in range(self.HEIGHT)], "bg", layer=0).set_position(0, 0)]
        for y in range(self.GRID_H):
            for x in range(self.GRID_W):
                px, py = self._cell_to_pixel(x, y)
                pixels = self._wall_pixels() if (x, y) in self.walls else self._tile_pixels(x, y)
                sprites.append(Sprite(pixels, f"tile_{x}_{y}", layer=1).set_position(px, py))
        for (x, y), color_key in self.targets.items():
            px, py = self._cell_to_pixel(x, y)
            sprites.append(Sprite(self._ring_pixels(color_key), f"target_{x}_{y}", layer=4).set_position(px, py))
        for (x, y), color_key in self.gates.items():
            px, py = self._cell_to_pixel(x, y)
            sprites.append(Sprite(self._gate_pixels(color_key, color_key == self.color), f"gate_{x}_{y}", layer=5).set_position(px, py))
        for (x, y), color_key in self.paint.items():
            px, py = self._cell_to_pixel(x, y)
            sprites.append(Sprite(self._paint_pixels(color_key), f"paint_{x}_{y}", layer=3).set_position(px, py))
        for (x, y), color_key in self.mixers.items():
            px, py = self._cell_to_pixel(x, y)
            sprites.append(Sprite(self._mixer_pixels(color_key), f"mixer_{x}_{y}", layer=5).set_position(px, py))
        px, py = self._cell_to_pixel(*self.pos)
        sprites.append(Sprite(self._droplet_pixels(), "droplet", layer=6).set_position(px, py))
        self.current_level._sprites = sprites

    def _check_win(self):
        return all(self.paint.get(pos) == color for pos, color in self.targets.items())

    def step(self):
        if self.action.id in self.DELTAS and self.steps_left > 0:
            self._move(self.action.id)
        self._sync()
        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        arr = np.zeros((self.GRID_H, self.GRID_W), dtype=np.int16)
        for (x, y), color in self.paint.items():
            arr[y, x] = COLORS[color]
        return arr
