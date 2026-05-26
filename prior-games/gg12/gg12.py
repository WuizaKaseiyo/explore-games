"""Constellation-Lens-Relay.

Clicking a star rotates its lens and every linked neighbouring lens one
quarter-turn. The goal panel on the right shows the required final orientation
for each coloured star. Tight budgets make random clicking fail quickly; the
player must reason about overlap between linked stars.
"""

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BG = 0
SKY = 11
LINK = 13
TARGET_LINK = 5
PANEL = 12
PANEL_DARK = 5
LENS = 14
PULSE = 10
HUD_FILL = 6
HUD_EMPTY = 1

STAR_COLORS = [2, 3, 1, 4, 7, 8]
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


class StepHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps:
            filled = int(frame.shape[1] * self.game.steps_left / self.game.max_steps)
            for x in range(frame.shape[1]):
                frame[0, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


class Gg12(NovaBaseGame):
    WIDTH = 60
    HEIGHT = 48
    PANEL_X = 43

    def __init__(self):
        self.hud = StepHud(self)
        levels = [Level(grid_size=(self.WIDTH, self.HEIGHT), sprites=[], data={"Level": i}) for i in (1, 2, 3)]
        self.nodes = []
        self.links = []
        self.phases = []
        self.targets = []
        self.witness = []
        self.last_click = None
        self.steps_left = 0
        self.max_steps = 0
        super().__init__(
            "gg12",
            levels,
            Camera(background=BG, letter_box=BG, interfaces=[self.hud]),
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.WIDTH
        self.camera.height = self.HEIGHT
        self.current_level._grid_size = (self.WIDTH, self.HEIGHT)
        lvl = level.get_data("Level")
        if lvl == 1:
            self.nodes = [(9, 14), (21, 14), (33, 14)]
            self.links = [(0, 1), (1, 2)]
            self.phases = [0, 1, 3]
            self.witness = [0, 2, 1]
            self.max_steps = 3
        elif lvl == 2:
            self.nodes = [(10, 10), (30, 10), (10, 30), (30, 30)]
            self.links = [(0, 1), (0, 2), (1, 3), (2, 3)]
            self.phases = [2, 0, 1, 3]
            self.witness = [1, 2, 0, 3, 1]
            self.max_steps = 5
        else:
            self.nodes = [(8, 8), (25, 8), (36, 20), (23, 34), (7, 28)]
            self.links = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 3)]
            self.phases = [1, 3, 0, 2, 1]
            self.witness = [4, 1, 3, 0, 2, 1, 4]
            self.max_steps = 7
        self.targets = self._simulate(self.phases, self.witness)
        self.steps_left = self.max_steps
        self.last_click = None
        self._sync()

    def _affected(self, idx):
        out = {idx}
        for a, b in self.links:
            if a == idx:
                out.add(b)
            elif b == idx:
                out.add(a)
        return out

    def _simulate(self, phases, clicks):
        result = list(phases)
        for idx in clicks:
            for node_idx in self._affected(idx):
                result[node_idx] = (result[node_idx] + 1) % 4
        return result

    def _node_at(self, gx, gy):
        for i, (x, y) in enumerate(self.nodes):
            if abs(gx - x) <= 3 and abs(gy - y) <= 3:
                return i
        return None

    def _click_node(self, idx):
        for node_idx in self._affected(idx):
            self.phases[node_idx] = (self.phases[node_idx] + 1) % 4
        self.last_click = idx
        self.steps_left -= 1

    def _line_cells(self, a, b):
        x0, y0 = self.nodes[a]
        x1, y1 = self.nodes[b]
        steps = max(abs(x1 - x0), abs(y1 - y0))
        cells = []
        for i in range(steps + 1):
            t = i / max(1, steps)
            x = int(round(x0 + (x1 - x0) * t))
            y = int(round(y0 + (y1 - y0) * t))
            if 0 <= x < self.PANEL_X - 1 and 1 <= y < self.HEIGHT:
                cells.append((x, y))
        return cells

    def _lens_pixels(self, color, phase, highlight=False):
        pixels = [[-1] * 7 for _ in range(7)]
        ring = PULSE if highlight else color
        for x, y in [(3, 0), (1, 1), (5, 1), (0, 3), (6, 3), (1, 5), (5, 5), (3, 6)]:
            pixels[y][x] = ring
        for y in range(2, 5):
            for x in range(2, 5):
                pixels[y][x] = color
        dx, dy = DIRS[phase]
        pixels[3 + dy][3 + dx] = LENS
        pixels[3 + dy * 2][3 + dx * 2] = LENS
        return pixels

    def _mini_lens_pixels(self, color, phase):
        pixels = [[PANEL_DARK] * 5 for _ in range(5)]
        for y in range(1, 4):
            for x in range(1, 4):
                pixels[y][x] = color
        dx, dy = DIRS[phase]
        pixels[2 + dy][2 + dx] = LENS
        return pixels

    def _sync(self):
        sprites = [
            Sprite([[SKY] * self.WIDTH for _ in range(self.HEIGHT)], "sky", layer=0).set_position(0, 0)
        ]

        for x in range(self.PANEL_X - 1, self.PANEL_X + 16):
            if 0 <= x < self.WIDTH:
                sprites.append(Sprite([[PANEL]], f"panel_bg_{x}", layer=1).set_position(x, 1))
                for y in range(2, self.HEIGHT):
                    sprites.append(Sprite([[PANEL]], f"panel_bg_{x}_{y}", layer=1).set_position(x, y))
        for y in range(1, self.HEIGHT):
            sprites.append(Sprite([[PANEL_DARK]], f"divider_{y}", layer=3).set_position(self.PANEL_X - 1, y))

        for edge in self.links:
            for x, y in self._line_cells(*edge):
                sprites.append(Sprite([[LINK]], f"link_{edge}_{x}_{y}", layer=2).set_position(x, y))

        affected = self._affected(self.last_click) if self.last_click is not None else set()
        for i, (x, y) in enumerate(self.nodes):
            color = STAR_COLORS[i % len(STAR_COLORS)]
            sprites.append(
                Sprite(self._lens_pixels(color, self.phases[i], i in affected), f"node_{i}", layer=5)
                .set_position(x - 3, y - 3)
            )

        panel_y = 5
        for i, target_phase in enumerate(self.targets):
            color = STAR_COLORS[i % len(STAR_COLORS)]
            y = panel_y + i * 8
            sprites.append(Sprite([[color, color], [color, color]], f"target_key_{i}", layer=4).set_position(self.PANEL_X + 2, y + 1))
            sprites.append(
                Sprite(self._mini_lens_pixels(color, target_phase), f"target_lens_{i}", layer=5)
                .set_position(self.PANEL_X + 7, y)
            )
            if self.phases[i] == target_phase:
                sprites.append(Sprite([[PULSE]], f"target_done_{i}", layer=6).set_position(self.PANEL_X + 13, y + 2))
        self.current_level._sprites = sprites

    def step(self):
        if self.action.id == GameAction.ACTION6:
            grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
            if grid is not None:
                idx = self._node_at(*grid)
                if idx is not None and self.steps_left > 0:
                    self._click_node(idx)
        self._sync()
        if self.phases == self.targets:
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        return np.array([self.phases, self.targets], dtype=np.int16)
