"""Gear-Mesh-Spin.

The player clicks gears to rotate their marker tooth one step clockwise.
Meshed neighbours counter-rotate (alternating CW/CCW) and the effect
propagates through the mesh graph.  ACTION5 toggles a lock on the most
recently clicked gear; locked gears block propagation.

Levels scale in gear count, branching, and lock dependency:
  L1 — 3 linear gears, target reachable by pure mesh rotations
  L2 — 5 gears (Y-branch), target generated through a lock/unlock sequence
  L3 — 7 gears (complex mesh), target requires repeated isolation with locks

Each level uses a unique colour palette for visual diversity.
Gears are rendered as 3×3 cross shapes (not solid blocks) for a cog effect.
"""

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite

BG = 0
FLOOR = 11
TOOTH = 14         # bright white — marker tooth
SOCKET = 5         # dark grey — target socket
LOCK_COLOR = 6     # magenta — lock indicator
FRAME_COLOR = 5    # dark grey
HUD_FILL = 4
HUD_EDGE = 7
HUD_EMPTY = 5

# Per-level gear palettes (visual diversity)
GEAR_PALETTES = [
    [2, 4, 7],                   # L1: red, yellow, orange
    [1, 3, 8, 9, 2],             # L2: blue, green, cyan, maroon, red
    [4, 7, 1, 9, 3, 8, 2],       # L3: yellow, orange, blue, maroon, green, cyan, red
]

# 8 cardinal + intercardinal directions (used for tooth/socket rendering)
DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


class StepHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps:
            ratio = max(0.0, min(1.0, self.game.steps_left / self.game.max_steps))
            filled = int(round(frame.shape[0] * ratio))
            bar_x = frame.shape[1] - 1
            for y in range(frame.shape[0]):
                frame[y, bar_x] = HUD_FILL if y >= frame.shape[0] - filled else HUD_EMPTY
            if frame.shape[1] > 1:
                for y in range(frame.shape[0]):
                    frame[y, bar_x - 1] = HUD_EDGE
        return frame


class Gg09(NovaBaseGame):
    """Gear-Mesh-Spin game with scaling difficulty."""

    def __init__(self):
        self.hud = StepHud(self)
        levels = [
            Level(grid_size=(1, 1), sprites=[], data={"Level": i})
            for i in (1, 2, 3)
        ]
        self.positions = []
        self.mesh = {}
        self.notches = []
        self.targets = []
        self.locked = set()
        self.last_clicked = None
        self.palette = GEAR_PALETTES[0]
        self.max_steps = 0
        self.steps_left = 0
        self.witness = []
        super().__init__(
            "gg09", levels,
            Camera(background=BG, letter_box=BG, interfaces=[self.hud]),
            available_actions=[5, 6],
        )

    # ------------------------------------------------------------------ #
    #  Level setup                                                         #
    # ------------------------------------------------------------------ #

    def on_set_level(self, level: Level) -> None:
        lvl = level.get_data("Level")
        self.locked = set()
        self.last_clicked = None

        if lvl == 1:
            # 3 linear gears
            self.positions = [(2, 4), (6, 4), (10, 4)]
            self.mesh = {0: [1], 1: [0, 2], 2: [1]}
            self.notches = [0, 0, 0]
            self.palette = GEAR_PALETTES[0]
            self.witness = [0, 1, 0, 2, 1, 2, 0, 1, 2, 0]
            self.max_steps = 16
        elif lvl == 2:
            # 5 gears in Y-branch:  0-1-2 with 3 below 1 and 4 below 2
            self.positions = [(1, 3), (5, 3), (9, 3), (5, 7), (9, 7)]
            self.mesh = {
                0: [1], 1: [0, 2, 3], 2: [1, 4],
                3: [1, 4], 4: [2, 3],
            }
            self.notches = [0, 0, 0, 0, 0]
            self.palette = GEAR_PALETTES[1]
            self.witness = [1, "lock", 0, 0, 3, 4, "unlock", 2, 2, 1, 3, 0]
            self.max_steps = 22
        else:
            # 7 gears in a complex mesh
            # Layout:  0   1   2
            #            3   4
            #          5   6
            self.positions = [
                (1, 2), (5, 2), (9, 2),
                (3, 5), (7, 5),
                (1, 8), (5, 8),
            ]
            self.mesh = {
                0: [1, 3], 1: [0, 2, 3, 4], 2: [1, 4],
                3: [0, 1, 5, 6], 4: [1, 2, 6],
                5: [3, 6], 6: [3, 4, 5],
            }
            self.notches = [0, 0, 0, 0, 0, 0, 0]
            self.palette = GEAR_PALETTES[2]
            self.witness = [1, "lock", 6, 6, 2, 4, "unlock", 3, "lock", 0, 5, 2, "unlock", 4, 1, 6]
            self.max_steps = 28

        # Compute camera size based on gear positions
        max_x = max(x for x, y in self.positions) + 3
        max_y = max(y for x, y in self.positions) + 3 + 1  # +1 for HUD
        cam_w = max(max_x + 1, 14)
        cam_h = max(max_y + 1, 12)
        self.camera.width = cam_w
        self.camera.height = cam_h
        self.current_level._grid_size = (cam_w, cam_h)

        self.targets = self._simulate_witness(self.notches[:], self.witness)
        self.steps_left = self.max_steps
        self._sync()

    def _simulate_witness(self, start_notches, witness):
        """Run witness click sequence and return final notch positions."""
        saved = (self.notches[:], self.locked.copy(), self.last_clicked, self.steps_left)
        self.notches = start_notches[:]
        self.locked = set()
        self.last_clicked = None
        self.steps_left = 999

        for item in witness:
            if item in ("lock", "unlock"):
                self._toggle_lock()
            else:
                self._click_gear(item)

        result = self.notches[:]
        self.notches, self.locked, self.last_clicked, self.steps_left = saved
        return result

    # ------------------------------------------------------------------ #
    #  Core mechanics                                                      #
    # ------------------------------------------------------------------ #

    def _gear_at(self, gx, gy):
        """Find which gear index a grid click hits, or None."""
        for i, (x, y) in enumerate(self.positions):
            if x <= gx <= x + 2 and y <= gy <= y + 2:
                return i
        return None

    def _click_gear(self, idx):
        """Rotate a gear and propagate through the mesh."""
        if idx in self.locked:
            self.last_clicked = idx
            return False
        seen = {idx}
        frontier = [(idx, 0)]
        while frontier:
            cur, depth = frontier.pop(0)
            if cur in self.locked:
                continue
            delta = 1 if depth % 2 == 0 else -1
            self.notches[cur] = (self.notches[cur] + delta) % 8
            for nxt in self.mesh.get(cur, []):
                if nxt not in seen and nxt not in self.locked:
                    seen.add(nxt)
                    frontier.append((nxt, depth + 1))
        self.last_clicked = idx
        self.steps_left -= 1
        return True

    def _toggle_lock(self):
        """Toggle lock on the last-clicked gear."""
        if self.last_clicked is None:
            return False
        if self.last_clicked in self.locked:
            self.locked.remove(self.last_clicked)
        else:
            self.locked.add(self.last_clicked)
        self.steps_left -= 1
        return True

    # ------------------------------------------------------------------ #
    #  Rendering                                                           #
    # ------------------------------------------------------------------ #

    def _sync(self):
        sprites = []

        for i, (x, y) in enumerate(self.positions):
            col = self.palette[i % len(self.palette)]

            # Draw gear as a cross shape (3×3 with corners empty)
            #  .X.
            #  XXX
            #  .X.
            cross = [
                [BG,  col, BG],
                [col, col, col],
                [BG,  col, BG],
            ]
            sprites.append(
                Sprite(pixels=cross, name=f"gear_{i}", layer=1)
                .set_position(x, y + 1)  # +1 for HUD
            )

            # Draw tooth (current notch position) — on the 3×3 body
            dx, dy = DIRS[self.notches[i]]
            tx, ty = x + 1 + dx, y + 1 + 1 + dy  # +1 for center, +1 for HUD
            sprites.append(
                Sprite(pixels=[[TOOTH]], name=f"tooth_{i}", layer=3)
                .set_position(tx, ty)
            )

            # Draw socket (target notch position) — as a dot outside the gear
            sdx, sdy = DIRS[self.targets[i]]
            # Place socket 2 steps from center (just outside the 3×3 body)
            # but clamp to valid range
            sx, sy = x + 1 + sdx * 2, y + 1 + 1 + sdy * 2
            if 0 <= sx < self.camera.width and 0 <= sy < self.camera.height:
                sprites.append(
                    Sprite(pixels=[[SOCKET]], name=f"socket_{i}", layer=0)
                    .set_position(sx, sy)
                )

            # Lock indicator
            if i in self.locked:
                sprites.append(
                    Sprite(pixels=[[LOCK_COLOR]], name=f"lock_{i}", layer=4)
                    .set_position(x + 1, y + 1 + 1)  # center of gear
                )

        self.current_level._sprites = sprites

    # ------------------------------------------------------------------ #
    #  Game loop                                                           #
    # ------------------------------------------------------------------ #

    def step(self):
        if self.action.id == GameAction.ACTION6:
            grid = self.camera.display_to_grid(
                self.action.data.get("x", -1),
                self.action.data.get("y", -1),
            )
            if grid is not None:
                gx, gy = grid
                # Adjust for HUD offset
                idx = self._gear_at(gx, gy - 1)
                if idx is not None:
                    self._click_gear(idx)
        elif self.action.id == GameAction.ACTION5:
            self._toggle_lock()
        self._sync()
        if self.notches == self.targets:
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        return np.array([self.notches, self.targets], dtype=np.int16)
