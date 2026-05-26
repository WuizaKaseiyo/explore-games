"""Museum-Heist-Net.

Maze security game. Thieves run through dark museum corridors. Cameras reveal
nearby corridors, traps, and thieves; guards run backward from the exit; traps
must be manually triggered when thieves are close.
"""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


# ---- Dark museum palette ----
BG = 0
FLOOR = 0           # Unlit floor
LIT = 7             # Lit floor (marble)
WALL = 11           # Dark wall
CASE = 9            # Display case
ARTIFACT = 4        # Gold artifacts
EXIT = 2            # Exit door
THIEF = 5           # Thief highlight
THIEF_DARK = 1      # Thief shadow
MASTER = 2          # Master thief
MASTER_DARK = 8     # Master thief shadow
CAMERA = 14         # Security camera
GUARD = 12          # Security guard
TRAP = 10           # Trap ready
RANGE = 6           # Camera range indicator
COIN = 4            # Coin / health
FLASH = 15          # Flash highlight
BAD = 2             # Warning / damage
SHADOW = 1          # Deep shadow for unlit walls
VAULT = 3           # Vault / safe accent


# Bounties for defeating each thief type
THIEF_STATS = {
    "pickpocket": {"hp": 2, "size": 1, "bounty": 2},
    "burglar":   {"hp": 4, "size": 2, "bounty": 3},
    "safecracker":{"hp": 8, "size": 3, "bounty": 5},
    "master":    {"hp":11, "size": 4, "bounty": 7},
}


LEVELS = [
    {
        "coins": 11,            # camera (6) + guard (5) = 11 exactly
        "waypoints": [
            (3, 50), (12, 50), (12, 42), (20, 42), (20, 33), (32, 33),
            (32, 42), (44, 42), (44, 25), (32, 25), (32, 16), (20, 16),
            (20, 25), (8, 25), (8, 16), (44, 16), (52, 16), (52, 8), (60, 8)
        ],
        "wave": ["pickpocket", "pickpocket", "burglar"],
        "spawn_gap": 4,
        "camera_slots": [(10, 45), (16, 30), (36, 38), (36, 20)],
        "active_cameras": [(10, 45)],       # covers first thieves
        "traps": [22, 48],
        "show_traps": True,
        "solution": [
            ("camera", 1),
            ("guard",),
        ] + [("wait",)] * 8 + [
            ("trap", 0),
        ] + [("wait",)] * 8 + [
            ("trap", 1),
        ] + [("wait",)] * 20,
    },
    {
        "coins": 18,
        "waypoints": [
            (2, 54), (10, 54), (10, 46), (22, 46), (22, 54), (34, 54),
            (34, 38), (22, 38), (10, 38), (10, 22), (22, 22), (34, 22),
            (34, 38), (46, 38), (46, 14), (34, 14), (22, 14), (10, 14),
            (10, 6), (46, 6), (58, 6)
        ],
        "wave": ["pickpocket", "burglar", "safecracker", "burglar", "master"],
        "spawn_gap": 4,
        "camera_slots": [(6, 48), (28, 46), (16, 30), (40, 30), (28, 18)],
        "active_cameras": [(6, 48)],
        "traps": [20, 52],
        "show_traps": False,
        "solution": [
            ("camera", 1), ("camera", 2),
        ] + [("wait",)] * 18 + [
            ("trap", 0),
        ] + [("wait",)] * 15 + [
            ("guard",),
        ] + [("wait",)] * 8 + [
            ("trap", 1),
        ] + [("wait",)] * 25,
    },
    {
        "coins": 16,
        "waypoints": [
            (2, 56), (14, 56), (14, 44), (26, 44), (26, 56), (38, 56),
            (38, 44), (50, 44), (50, 32), (38, 32), (26, 32), (14, 32),
            (14, 20), (26, 20), (38, 20), (50, 20), (50, 8), (38, 8),
            (26, 8), (14, 8), (14, 4), (62, 4)
        ],
        "wave": ["pickpocket"] * 3 + ["burglar"] * 2 + ["safecracker"] * 3 + ["master"],
        "spawn_gap": 3,
        "camera_slots": [(8, 50), (20, 44), (44, 38), (32, 26), (20, 14)],
        "active_cameras": [(8, 50)],
        "traps": [16, 42, 74],
        "show_traps": False,
        "solution": [
            ("camera", 1),
        ] + [("wait",)] * 15 + [
            ("trap", 0),
        ] + [("wait",)] * 12 + [
            ("trap", 1),
        ] + [("wait",)] * 18 + [
            ("trap", 2),
        ] + [("wait",)] * 8 + [
            ("guard",),
        ] + [("wait",)] * 30,
    },
]


class BottomHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        for x in range(frame.shape[1]):
            frame[63, x] = COIN if x < min(63, self.game.coins * 2) else WALL
        return frame


class Gg24(NovaBaseGame):
    W = 64
    H = 64
    CAMERA_COST = 6
    TRAP_COST = 2
    GUARD_COST = 5
    CAMERA_RADIUS = 10
    TRAP_RADIUS_INDEX = 4
    TRAP_DAMAGE = 5
    GUARD_HP = 5
    GUARD_DAMAGE = 1

    def __init__(self):
        self.hud = BottomHud(self)
        levels = [Level(grid_size=(self.W, self.H), sprites=[], data={**data, "Level": i + 1}) for i, data in enumerate(LEVELS)]
        self.path = []
        self.path_set = set()
        self.wave = []
        self.spawn_gap = 0
        self.spawn_timer = 0
        self.spawn_index = 0
        self.thieves = []
        self.guards = []
        self.camera_slots = []
        self.cameras = []
        self.traps = []
        self.show_traps = False
        self.effects = []
        self.coins = 0
        self.tick = 0
        self.solution = []
        self._pending_win = False        # instant win flag
        super().__init__("gg24", levels, Camera(background=BG, letter_box=BG, interfaces=[self.hud]), available_actions=[5, 6])

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.W
        self.camera.height = self.H
        self.current_level._grid_size = (self.W, self.H)
        self.path = self._make_path(level.get_data("waypoints"))
        self.path_set = set(self.path)
        self.wave = list(level.get_data("wave"))
        self.spawn_gap = level.get_data("spawn_gap")
        self.spawn_timer = 0
        self.spawn_index = 0
        self.thieves = []
        self.guards = []
        self.camera_slots = list(level.get_data("camera_slots"))
        self.cameras = list(level.get_data("active_cameras"))
        self.traps = [{"idx": idx, "cooldown": 0} for idx in level.get_data("traps")]
        self.show_traps = level.get_data("show_traps")
        self.effects = []
        self.coins = level.get_data("coins")
        self.tick = 0
        self.solution = list(level.get_data("solution"))
        self._pending_win = False
        self._spawn_next()
        self._sync()

    def _make_path(self, waypoints):
        path = []
        for a, b in zip(waypoints, waypoints[1:]):
            x0, y0 = a
            x1, y1 = b
            dx = abs(x1 - x0)
            dy = -abs(y1 - y0)
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            err = dx + dy
            x, y = x0, y0
            while True:
                if not path or path[-1] != (x, y):
                    path.append((x, y))
                if x == x1 and y == y1:
                    break
                e2 = 2 * err
                if e2 >= dy:
                    err += dy
                    x += sx
                if e2 <= dx:
                    err += dx
                    y += sy
        return path

    def _spawn_next(self):
        if self.spawn_index >= len(self.wave):
            return
        if any(thief["idx"] == 0 for thief in self.thieves):
            return
        kind = self.wave[self.spawn_index]
        stats = THIEF_STATS[kind]
        self.thieves.append({"idx": 0, "hp": stats["hp"], "max": stats["hp"], "kind": kind})
        self.spawn_index += 1
        self.spawn_timer = self.spawn_gap

    def _dist2(self, a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def _is_lit_point(self, point):
        return any(self._dist2(point, cam) <= self.CAMERA_RADIUS ** 2 for cam in self.cameras)

    def _is_lit_idx(self, idx):
        idx = max(0, min(len(self.path) - 1, idx))
        return self._is_lit_point(self.path[idx])

    def _slot_at(self, x, y):
        for i, slot in enumerate(self.camera_slots):
            if slot not in self.cameras and abs(x - slot[0]) + abs(y - slot[1]) <= 4:
                return i
        return None

    def _trap_at(self, x, y):
        for i, trap in enumerate(self.traps):
            if not self._trap_visible(trap):
                continue
            tx, ty = self.path[trap["idx"]]
            if abs(x - tx) + abs(y - ty) <= 4:
                return i
        return None

    def _trap_visible(self, trap):
        return self.show_traps or self._is_lit_idx(trap["idx"])

    def _buy_camera(self, slot_index):
        if self.coins < self.CAMERA_COST:
            return
        slot = self.camera_slots[slot_index]
        self.cameras.append(slot)
        self.coins -= self.CAMERA_COST

    def _buy_guard(self):
        if self.coins < self.GUARD_COST:
            return
        self.guards.append({"idx": len(self.path) - 1, "hp": self.GUARD_HP})
        self.coins -= self.GUARD_COST
        self.effects.append(("guard", self.path[-1]))

    def _trigger_trap(self, trap_index):
        if self.coins < self.TRAP_COST:
            return
        trap = self.traps[trap_index]
        if trap["cooldown"] > 0:
            return
        trap["cooldown"] = 8
        self.coins -= self.TRAP_COST
        center = trap["idx"]
        hit = False
        for thief in self.thieves:
            if abs(thief["idx"] - center) <= self.TRAP_RADIUS_INDEX:
                thief["hp"] -= self.TRAP_DAMAGE
                hit = True
        if hit:
            self.effects.append(("trap", self.path[center]))
        self._collect_captures()

    def _click(self, x, y):
        if 0 <= x <= 6 and 8 <= y <= 14:
            self._buy_guard()
            return
        trap = self._trap_at(x, y)
        if trap is not None:
            self._trigger_trap(trap)
            return
        slot = self._slot_at(x, y)
        if slot is not None:
            self._buy_camera(slot)

    def _collect_captures(self):
        """Remove dead thieves and award bounty. Set instant win if wave complete."""
        survivors = []
        for thief in self.thieves:
            if thief["hp"] <= 0:
                bounty = THIEF_STATS[thief["kind"]]["bounty"]
                self.coins += bounty
            else:
                survivors.append(thief)
        self.thieves = survivors
        # Immediately check if we've won after this kill
        self._try_instant_win()

    def _try_instant_win(self):
        """If the wave is fully spawned and no thieves remain, flag an instant win."""
        if self.spawn_index >= len(self.wave) and not self.thieves:
            self._pending_win = True

    def _advance_thieves(self):
        for thief in self.thieves:
            thief["idx"] += 1
            if thief["idx"] >= len(self.path) - 1:
                self.lose()
                return
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self._spawn_next()

    def _advance_guards(self):
        for guard in self.guards:
            if not any(abs(thief["idx"] - guard["idx"]) <= 1 for thief in self.thieves):
                guard["idx"] = max(0, guard["idx"] - 1)
        for guard in self.guards:
            targets = [thief for thief in self.thieves if abs(thief["idx"] - guard["idx"]) <= 1]
            if not targets:
                continue
            target = max(targets, key=lambda thief: thief["idx"])
            target["hp"] -= self.GUARD_DAMAGE
            guard["hp"] -= 1
            self.effects.append(("hit", self.path[target["idx"]]))
        self._collect_captures()
        self.guards = [guard for guard in self.guards if guard["hp"] > 0 and guard["idx"] > 0]

    def _advance_turn(self):
        self.effects = []
        for trap in self.traps:
            trap["cooldown"] = max(0, trap["cooldown"] - 1)
        if not self.thieves and self.spawn_index >= len(self.wave):
            self._pending_win = True   # catch cases where win wasn't already flagged
            return
        self._advance_thieves()
        if not getattr(self, "lost", False):
            self._advance_guards()
        self.tick += 1

    def _check_win(self):
        return self._pending_win

    # === Drawing helpers ===
    def _put(self, canvas, x, y, color):
        if 0 <= x < self.W and 0 <= y < self.H:
            canvas[y][x] = color

    def _rect(self, canvas, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._put(canvas, xx, yy, color)

    def _dot(self, canvas, x, y, color, r=1):
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                if abs(xx - x) + abs(yy - y) <= r + 1:
                    self._put(canvas, xx, yy, color)

    # ---- Museum visuals ----
    def _draw_background(self, canvas):
        for y in range(self.H):
            for x in range(self.W):
                if (x + y) % 31 == 0 or (x - y) % 23 == 0:
                    canvas[y][x] = SHADOW
                else:
                    canvas[y][x] = FLOOR

    def _draw_path(self, canvas):
        path_set = set(self.path)
        for (x, y) in self.path:
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in path_set and (abs(dx) == 2 or abs(dy) == 2):
                        self._put(canvas, nx, ny, WALL)
        for (x, y) in self.path:
            self._dot(canvas, x, y, FLOOR, 1)
            self._put(canvas, x, y, FLOOR)
        for i, (x, y) in enumerate(self.path):
            if self._is_lit_idx(i):
                self._dot(canvas, x, y, LIT, 1)
                self._put(canvas, x, y, LIT)
        sx, sy = self.path[0]
        ex, ey = self.path[-1]
        self._dot(canvas, sx, sy, EXIT, 3)
        self._rect(canvas, ex - 4, ey - 5, 9, 10, WALL)
        self._rect(canvas, ex - 2, ey - 2, 5, 5, EXIT)
        self._put(canvas, ex, ey, BG)

    def _draw_palette(self, canvas):
        self._rect(canvas, 0, 0, 7, 7, WALL)
        self._dot(canvas, 3, 3, CAMERA, 2)
        self._put(canvas, 3, 3, FLASH)
        self._rect(canvas, 0, 8, 7, 7, WALL)
        self._dot(canvas, 3, 11, GUARD, 2)
        self._put(canvas, 2, 10, FLASH)
        for x in range(min(63, self.coins)):
            self._put(canvas, x, 62, COIN)

    def _draw_camera_slot(self, canvas, slot, active):
        x, y = slot
        color = FLASH if active else CAMERA
        self._dot(canvas, x, y, CAMERA, 2)
        self._put(canvas, x, y, color)
        if active:
            for dx, dy in ((0, -4), (4, 0), (0, 4), (-4, 0)):
                self._put(canvas, x + dx, y + dy, RANGE)

    def _draw_trap(self, canvas, trap):
        if not self._trap_visible(trap):
            return
        x, y = self.path[trap["idx"]]
        self._rect(canvas, x - 2, y - 1, 5, 3, TRAP if trap["cooldown"] == 0 else WALL)
        self._put(canvas, x, y, FLASH if trap["cooldown"] == 0 else RANGE)

    def _draw_guard(self, canvas, guard):
        x, y = self.path[guard["idx"]]
        self._dot(canvas, x, y, GUARD, 2)
        self._put(canvas, x - 1, y, FLASH)
        self._put(canvas, x + 1, y, FLASH)
        for dx in range(min(5, guard["hp"])):
            self._put(canvas, x - 2 + dx, y - 4, COIN)

    def _draw_thief(self, canvas, thief):
        if not self._is_lit_idx(thief["idx"]):
            return
        x, y = self.path[thief["idx"]]
        size = THIEF_STATS[thief["kind"]]["size"]
        color = MASTER if thief["kind"] == "master" else THIEF
        dark = MASTER_DARK if thief["kind"] == "master" else THIEF_DARK
        self._dot(canvas, x, y, color, size)
        self._put(canvas, x - 1, y, dark)
        self._put(canvas, x + 1, y, dark)
        self._put(canvas, x, y - 1, FLASH)
        if thief["kind"] == "master":
            self._put(canvas, x - 3, y - 3, COIN)
            self._put(canvas, x + 3, y - 3, COIN)
        for dx in range(max(1, min(5, thief["hp"]))):
            self._put(canvas, x - 2 + dx, y - size - 1, BAD if thief["hp"] <= 2 else COIN)

    def _draw_effects(self, canvas):
        for effect in self.effects:
            kind, pos = effect
            x, y = pos
            if kind == "trap":
                for dx, dy in ((0, -2), (2, 0), (0, 2), (-2, 0)):
                    self._put(canvas, x + dx, y + dy, BAD)
            elif kind == "hit":
                self._put(canvas, x, y - 2, FLASH)
            else:
                self._put(canvas, x, y, GUARD)

    def _sync(self):
        canvas = [[BG for _ in range(self.W)] for _ in range(self.H)]
        self._draw_background(canvas)
        self._draw_path(canvas)
        self._draw_palette(canvas)
        for (px, py, prop) in [(12, 50, CASE), (50, 30, ARTIFACT), (28, 58, CASE),
                                (40, 10, CASE), (55, 50, ARTIFACT)]:
            self._rect(canvas, px-1, py-1, 3, 3, CASE)
            self._put(canvas, px, py, prop)
        for slot in self.camera_slots:
            self._draw_camera_slot(canvas, slot, slot in self.cameras)
        for trap in self.traps:
            self._draw_trap(canvas, trap)
        for guard in self.guards:
            self._draw_guard(canvas, guard)
        for thief in self.thieves:
            self._draw_thief(canvas, thief)
        self._draw_effects(canvas)
        self.current_level._sprites = [Sprite(canvas, "scene", layer=0).set_position(0, 0)]

    def step(self):
        if self._pending_win:
            # Instant win – skip the rest of the turn
            self.next_level()
            self.complete_action()
            return

        if self.action.id == GameAction.ACTION6:
            grid = self.camera.display_to_grid(self.action.data.get("x", -1), self.action.data.get("y", -1))
            if grid is not None:
                self._click(int(grid[0]), int(grid[1]))
            self._advance_turn()
        elif self.action.id == GameAction.ACTION5:
            self._advance_turn()

        self._sync()
        if self._check_win():
            self.next_level()
        elif not getattr(self, "lost", False) and any(thief["idx"] >= len(self.path) - 1 for thief in self.thieves):
            self.lose()
        self.complete_action()

    def _get_hidden_state(self):
        rows = [[self.coins, self.spawn_index, len(self.thieves), len(self.guards), len(self.cameras), self.tick]]
        rows.extend([[thief["idx"], thief["hp"], thief["max"], 1, 0, 0] for thief in self.thieves])
        rows.extend([[guard["idx"], guard["hp"], 0, 2, 0, 0] for guard in self.guards])
        rows.extend([[trap["idx"], trap["cooldown"], 0, 3, 0, 0] for trap in self.traps])
        return np.array(rows, dtype=np.int16)