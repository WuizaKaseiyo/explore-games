"""cy3k."""

import numpy as np
from novaengine import (
    NovaBaseGame,
    Camera,
    GameAction,
    InteractionMode,
    Level,
    RenderableUserDisplay,
    Sprite,
)


# Colour alphabet (4 colours that cycle in this order)
ALPHABET = [11, 14, 8, 15]   # yellow → green → red → purple → yellow
ALPHABET_NEXT = {c: ALPHABET[(i + 1) % 4] for i, c in enumerate(ALPHABET)}

CURSOR_PIXELS = [
    [4, 9, 4],
    [9, 0, 9],
    [4, 9, 4],
]
FIXED_MARKER_PIXELS = [
    [3, 4, 3],
    [4, 3, 4],
    [3, 4, 3],
]
TRANSPARENT_MARKER_PIXELS = [
    [-1, 10, -1],
    [10, -1, 10],
    [-1, 10, -1],
]

BACKGROUND_COLOR = 1
PADDING_COLOR = 2


def _mk_cell(x, y, color):
    s = Sprite(
        pixels=[[color]],
        name=f"cell_{x}_{y}",
        visible=True,
        collidable=False,
        tags=["cell"],
        interaction=InteractionMode.INTANGIBLE,
    )
    s.set_position(x, y)
    s.set_layer(0)
    return s


def _mk_cursor(x, y):
    s = Sprite(
        pixels=CURSOR_PIXELS,
        name="cursor",
        visible=True,
        collidable=False,
        tags=["cursor"],
        interaction=InteractionMode.INTANGIBLE,
    )
    s.set_position(x, y)
    s.set_layer(3)
    return s


def _mk_fixed(x, y):
    s = Sprite(
        pixels=FIXED_MARKER_PIXELS,
        name=f"fixed_{x}_{y}",
        visible=True,
        collidable=False,
        tags=["fixed"],
        interaction=InteractionMode.INTANGIBLE,
    )
    s.set_position(x, y)
    s.set_layer(2)
    return s


def _mk_transparent(x, y):
    s = Sprite(
        pixels=TRANSPARENT_MARKER_PIXELS,
        name=f"transparent_{x}_{y}",
        visible=True,
        collidable=False,
        tags=["transparent"],
        interaction=InteractionMode.INTANGIBLE,
    )
    s.set_position(x, y)
    s.set_layer(2)
    return s


# Initial layouts and target patterns per level

# L1: 6x6 grid, 4 quadrants (3x3 each)
def _build_l1_initial():
    """Returns dict (x, y) -> color."""
    cells = {}
    for x in range(6):
        for y in range(6):
            if x < 3 and y < 3:
                color = 11  # A=yellow
            elif x >= 3 and y < 3:
                color = 8   # C=red
            elif x < 3 and y >= 3:
                color = 15  # B=purple
            else:
                color = 14  # D=green
            cells[(x, y)] = color
    return cells


def _build_l1_target():
    cells = {}
    for x in range(6):
        for y in range(6):
            if x < 3 and y < 3:
                color = 14   # A→green (was yellow)
            elif x >= 3 and y < 3:
                color = 15   # C→purple (was red)
            elif x < 3 and y >= 3:
                color = 11   # B→yellow (was purple)
            else:
                color = 8    # D→red (was green)
            cells[(x, y)] = color
    return cells


def _build_l1():
    sprites = []
    init = _build_l1_initial()
    for (x, y), c in init.items():
        sprites.append(_mk_cell(x, y, c))
    sprites.append(_mk_cursor(0, 0))
    return Level(sprites=sprites, grid_size=(6, 6))


# L2: 6x6 with 2 fixed cells
def _build_l2_initial():
    return _build_l1_initial()  # same starting layout


def _build_l2_target():
    """L2 target: cycle clusters but leave fixed cells (0,0) and (5,5) at original."""
    target = _build_l1_target()
    # Override fixed cells — they should match initial, not the cycled version
    init = _build_l1_initial()
    target[(0, 0)] = init[(0, 0)]   # stays at original (yellow)
    target[(5, 5)] = init[(5, 5)]   # stays at original (green)
    return target


def _build_l2():
    sprites = []
    init = _build_l2_initial()
    for (x, y), c in init.items():
        sprites.append(_mk_cell(x, y, c))
    sprites.append(_mk_fixed(0, 0))
    sprites.append(_mk_fixed(5, 5))
    sprites.append(_mk_cursor(2, 1))
    return Level(sprites=sprites, grid_size=(6, 6))


# L3: 8x8 with 1 fixed + 1 transparent
def _build_l3_initial():
    cells = {}
    for x in range(8):
        for y in range(8):
            if x < 4 and y < 4:
                color = 11
            elif x >= 4 and y < 4:
                color = 8
            elif x < 4 and y >= 4:
                color = 15
            else:
                color = 14
            cells[(x, y)] = color
    return cells


def _build_l3_target():
    """L3 target: each cluster cycles by 1; fixed cell stays; transparent doesn't cycle."""
    init = _build_l3_initial()
    target = {}
    for (x, y), c in init.items():
        target[(x, y)] = ALPHABET_NEXT[c]
    # Fixed cell at (0, 0) stays
    target[(0, 0)] = init[(0, 0)]
    # Transparent at (3, 3): stays at original (transparent doesn't cycle)
    target[(3, 3)] = init[(3, 3)]
    return target


def _build_l3():
    sprites = []
    init = _build_l3_initial()
    for (x, y), c in init.items():
        sprites.append(_mk_cell(x, y, c))
    sprites.append(_mk_fixed(0, 0))
    sprites.append(_mk_transparent(3, 3))
    sprites.append(_mk_cursor(2, 2))
    return Level(sprites=sprites, grid_size=(8, 8))


levels = [_build_l1(), _build_l2(), _build_l3()]


# Targets per level (looked up by level index)
TARGETS = [_build_l1_target(), _build_l2_target(), _build_l3_target()]


class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps=50):
        super().__init__()
        self._max = max_steps
        self._used = 0

    def set_state(self, used, max_steps):
        self._used = used
        self._max = max_steps

    def render_interface(self, frame):
        if self._max <= 0:
            return frame
        bar_y, x_lo, x_hi = 63, 16, 48
        remaining = max(0, self._max - self._used)
        width = x_hi - x_lo
        filled = int(round(width * (remaining / self._max)))
        for i, x in enumerate(range(x_lo, x_hi)):
            frame[bar_y, x] = 9 if i < filled else 3
        return frame


class TargetHud(RenderableUserDisplay):
    """Render target pattern as small swatch grid in top-right corner."""

    def __init__(self):
        super().__init__()
        self._target = {}
        self._gw = 6
        self._gh = 6

    def set_state(self, target, gw, gh):
        self._target = target
        self._gw = gw
        self._gh = gh

    def render_interface(self, frame):
        # 4x4 swatch in top-right corner — show target pattern compressed
        # Place at rows 0..min(8, gh), cols 56..63 (8 wide)
        cell_size = max(1, 8 // max(self._gw, self._gh))
        x_off = 56
        y_off = 0
        for (x, y), c in self._target.items():
            for py in range(cell_size):
                for px in range(cell_size):
                    fy = y_off + y * cell_size + py
                    fx = x_off + x * cell_size + px
                    if 0 <= fy < 64 and 0 <= fx < 64:
                        frame[fy, fx] = c
        return frame


class Cy3k(NovaBaseGame):
    def __init__(self):
        self._step_hud = StepCounterHud(50)
        self._target_hud = TargetHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._target_hud, self._step_hud],
        )
        super().__init__(
            game_id="cy3k",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )
        self._steps_used = 0
        self._max_steps = 50

    def on_set_level(self, level):
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        idx = getattr(self, "_current_level_index", 0)
        self._max_steps = [50, 80, 120][idx]
        self._steps_used = 0
        self._step_hud.set_state(self._steps_used, self._max_steps)
        self._target_hud.set_state(TARGETS[idx], gw, gh)

    def _cursor(self):
        return self.current_level.get_sprites_by_tag("cursor")[0]

    def _cell_at(self, x, y):
        for c in self.current_level.get_sprites_by_tag("cell"):
            if c.x == x and c.y == y:
                return c
        return None

    def _is_fixed(self, x, y):
        for f in self.current_level.get_sprites_by_tag("fixed"):
            if f.x == x and f.y == y:
                return True
        return False

    def _is_transparent(self, x, y):
        for t in self.current_level.get_sprites_by_tag("transparent"):
            if t.x == x and t.y == y:
                return True
        return False

    def _color_at(self, x, y):
        cell = self._cell_at(x, y)
        if cell is None:
            return None
        return int(cell.pixels[0][0])

    def _set_color(self, x, y, c):
        cell = self._cell_at(x, y)
        if cell is None:
            return
        cell.pixels = np.array([[c]], dtype=np.int16)

    def _direction(self, action_id):
        if action_id == GameAction.ACTION1:
            return (0, -1)
        if action_id == GameAction.ACTION2:
            return (0, 1)
        if action_id == GameAction.ACTION3:
            return (-1, 0)
        if action_id == GameAction.ACTION4:
            return (1, 0)
        return (0, 0)

    def _compute_cluster(self, sx, sy):
        """BFS for 4-connected same-colour cluster, allowing transparent cells as bridges
        but excluding the transparent cells themselves from the result."""
        gw, gh = self.current_level.grid_size or (64, 64)
        start_color = self._color_at(sx, sy)
        if start_color is None or self._is_transparent(sx, sy):
            return set()
        cluster = set()
        bridge = set()  # transparent cells we've crossed
        stack = [(sx, sy)]
        while stack:
            x, y = stack.pop()
            if (x, y) in cluster or (x, y) in bridge:
                continue
            if x < 0 or x >= gw or y < 0 or y >= gh:
                continue
            if self._is_transparent(x, y):
                # bridge through but don't include
                bridge.add((x, y))
                # Continue exploring neighbors
                for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < gw and 0 <= ny < gh and (nx, ny) not in cluster and (nx, ny) not in bridge:
                        stack.append((nx, ny))
                continue
            if self._color_at(x, y) != start_color:
                continue
            cluster.add((x, y))
            for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]:
                stack.append((x + dx, y + dy))
        return cluster

    def _cycle_cluster_at_cursor(self):
        c = self._cursor()
        cur_color = self._color_at(c.x, c.y)
        if cur_color is None:
            return
        if cur_color not in ALPHABET_NEXT:
            return
        next_c = ALPHABET_NEXT[cur_color]
        cluster = self._compute_cluster(c.x, c.y)
        for (x, y) in cluster:
            if self._is_fixed(x, y):
                continue  # fixed cells don't cycle
            self._set_color(x, y, next_c)

    def _check_win(self):
        idx = getattr(self, "_current_level_index", 0)
        target = TARGETS[idx]
        for (x, y), c in target.items():
            if self._color_at(x, y) != c:
                return False
        return True

    def step(self):
        if self._steps_used >= self._max_steps:
            self.lose()
            self.complete_action()
            return

        if self.action.id in (GameAction.ACTION1, GameAction.ACTION2,
                              GameAction.ACTION3, GameAction.ACTION4):
            dx, dy = self._direction(self.action.id)
            cursor = self._cursor()
            gw, gh = self.current_level.grid_size or (64, 64)
            new_x = cursor.x + dx
            new_y = cursor.y + dy
            if 0 <= new_x < gw and 0 <= new_y < gh:
                cursor.set_position(new_x, new_y)
            self._steps_used += 1
            self._step_hud.set_state(self._steps_used, self._max_steps)
        elif self.action.id == GameAction.ACTION5:
            self._cycle_cluster_at_cursor()
            self._steps_used += 1
            self._step_hud.set_state(self._steps_used, self._max_steps)
            if self._check_win():
                self.next_level()
                self.complete_action()
                return

        self.complete_action()

    def _get_hidden_state(self):
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
