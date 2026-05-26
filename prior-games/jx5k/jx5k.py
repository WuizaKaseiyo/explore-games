"""Generated game jx5k."""

from typing import List, Optional, Tuple

import numpy as np
from novaengine import (
    ActionInput,
    NovaBaseGame,
    BlockingMode,
    Camera,
    GameAction,
    InteractionMode,
    Level,
    RenderableUserDisplay,
    Sprite,
)


# ---------------------------------------------------------------------
# 1. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 1
PADDING_COLOR = 2

NODE_BORDER = 4
NODE_BLUE = 9
NODE_RED = 8
NODE_YELLOW = 11

HALO_COLOR = 12
PIP_EMPTY_COLOR = 3
PIP_FILLED_COLOR = 12
EDGE_COLOR = 15
HUD_FILL_COLOR = 14
HUD_BG_COLOR = 1

REJECT_FLASH_FRAMES = 6


# ---------------------------------------------------------------------
# 2. SPRITE PIXEL TEMPLATES
# ---------------------------------------------------------------------
def _make_node_pixels(color: int) -> List[List[int]]:
    """5x5 node sprite: a coloured circle with a checker-pattern interior."""
    c = color
    b = NODE_BORDER
    return [
        [-1, c, c, c, -1],
        [c, b, c, b, c],
        [c, c, b, c, c],
        [c, b, c, b, c],
        [-1, c, c, c, -1],
    ]


NODE_PIXELS_BLUE = _make_node_pixels(NODE_BLUE)
NODE_PIXELS_RED = _make_node_pixels(NODE_RED)
NODE_PIXELS_YELLOW = _make_node_pixels(NODE_YELLOW)


def _make_halo_pixels() -> List[List[int]]:
    """7x7 halo: orange ring with transparent interior."""
    rows = []
    rows.append([HALO_COLOR] * 7)
    for _ in range(5):
        rows.append([HALO_COLOR] + [-1] * 5 + [HALO_COLOR])
    rows.append([HALO_COLOR] * 7)
    return rows


HALO_PIXELS = _make_halo_pixels()


# ---------------------------------------------------------------------
# 3. LINE / BRESENHAM HELPERS
# ---------------------------------------------------------------------
def _bresenham(x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
    """Cells visited by a line from (x0, y0) to (x1, y1), inclusive both ends."""
    cells: List[Tuple[int, int]] = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        cells.append((x, y))
        if x == x1 and y == y1:
            return cells
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def _line_cells_for_strand(
    x0: int, y0: int, x1: int, y1: int, k: int
) -> List[Tuple[int, int]]:
    """Bresenham cells for an edge strand. k=0 is the centre line; k=1 is shifted by 1 perpendicular for a parallel double-edge variant."""
    base = _bresenham(x0, y0, x1, y1)
    if k == 0:
        return base
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) >= abs(dy):
        return [(x, y + 1) for x, y in base]
    return [(x + 1, y) for x, y in base]


def _strand_sprite_pixels(
    cells: List[Tuple[int, int]],
) -> Tuple[List[List[int]], int, int]:
    """Build pixel array + top-left grid position for a sprite covering `cells`."""
    if not cells:
        return [[-1]], 0, 0
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    w = xmax - xmin + 1
    h = ymax - ymin + 1
    pixels = [[-1] * w for _ in range(h)]
    for x, y in cells:
        pixels[y - ymin][x - xmin] = EDGE_COLOR
    return pixels, xmin, ymin


# ---------------------------------------------------------------------
# 4. LAYOUTS — declarative per-level descriptors
# ---------------------------------------------------------------------
LAYOUT_L1 = {
    "nodes": [
        ("n_nw", 8, 8, NODE_BLUE),
        ("n_ne", 24, 8, NODE_BLUE),
        ("n_se", 24, 24, NODE_BLUE),
        ("n_sw", 8, 24, NODE_BLUE),
    ],
    "target_degrees": {"n_nw": 2, "n_ne": 2, "n_se": 2, "n_sw": 2},
    "max_multiplicity": 1,
    "step_budget": 30,
    "level_palette": [NODE_BLUE],
}

LAYOUT_L2 = {
    "nodes": [
        ("n0", 5, 16, NODE_RED),
        ("n1", 16, 5, NODE_BLUE),
        ("n2", 27, 16, NODE_RED),
        ("n3", 16, 27, NODE_BLUE),
        ("n4", 16, 16, NODE_RED),
    ],
    "target_degrees": {"n0": 3, "n1": 3, "n2": 3, "n3": 3, "n4": 4},
    "max_multiplicity": 1,
    "step_budget": 50,
    "level_palette": [NODE_BLUE, NODE_RED],
}

LAYOUT_L3 = {
    "nodes": [
        ("n0", 8, 16, NODE_RED),
        ("n1", 16, 8, NODE_BLUE),
        ("n2", 24, 16, NODE_RED),
        ("n3", 16, 24, NODE_BLUE),
    ],
    "target_degrees": {"n0": 4, "n1": 2, "n2": 4, "n3": 2},
    "max_multiplicity": 2,
    "step_budget": 50,
    "level_palette": [NODE_BLUE, NODE_RED],
}


# ---------------------------------------------------------------------
# 5. PIP POSITIONS — clockwise around the node centre at radius ~4
# ---------------------------------------------------------------------
def _pip_positions(cx: int, cy: int, count: int) -> List[Tuple[int, int]]:
    candidates = [
        (cx, cy - 4),       # N
        (cx + 3, cy - 3),   # NE
        (cx + 4, cy),       # E
        (cx + 3, cy + 3),   # SE
        (cx, cy + 4),       # S
        (cx - 3, cy + 3),   # SW
        (cx - 4, cy),       # W
        (cx - 3, cy - 3),   # NW
    ]
    return candidates[:count]


# ---------------------------------------------------------------------
# 6. LEVEL BUILDERS — instantiate Level from layout dict
# ---------------------------------------------------------------------
def _build_level(layout: dict) -> Level:
    sprites: List[Sprite] = []

    nodes = layout["nodes"]
    target_degrees = layout["target_degrees"]
    max_mult = layout["max_multiplicity"]

    # 6a. Node colour variants — pre-place all 3 per node, only the starting colour TANGIBLE.
    for name, cx, cy, start_color in nodes:
        for variant_color, variant_pixels, variant_tag in (
            (NODE_BLUE, NODE_PIXELS_BLUE, "colour_blue"),
            (NODE_RED, NODE_PIXELS_RED, "colour_red"),
            (NODE_YELLOW, NODE_PIXELS_YELLOW, "colour_yellow"),
        ):
            interaction = (
                InteractionMode.TANGIBLE
                if variant_color == start_color
                else InteractionMode.REMOVED
            )
            s = Sprite(
                pixels=variant_pixels,
                name=f"{name}__{variant_tag}",
                x=cx - 2,
                y=cy - 2,
                tags=["node", variant_tag, f"node_{name}"],
                interaction=interaction,
                blocking=BlockingMode.PIXEL_PERFECT,
            )
            sprites.append(s)

    # 6b. Pip slots per node — empty + filled variants at the same cell.
    for name, cx, cy, _ in nodes:
        target = target_degrees[name]
        for idx, (px, py) in enumerate(_pip_positions(cx, cy, target)):
            empty = Sprite(
                pixels=[[PIP_EMPTY_COLOR]],
                name=f"pip_empty__{name}_{idx}",
                x=px,
                y=py,
                tags=[
                    "pip_empty",
                    f"pip_node_{name}",
                    f"pip_idx_{idx}",
                ],
                interaction=InteractionMode.TANGIBLE,
                blocking=BlockingMode.NOT_BLOCKED,
                layer=2,
            )
            filled = Sprite(
                pixels=[[PIP_FILLED_COLOR]],
                name=f"pip_filled__{name}_{idx}",
                x=px,
                y=py,
                tags=[
                    "pip_filled",
                    f"pip_node_{name}",
                    f"pip_idx_{idx}",
                ],
                interaction=InteractionMode.REMOVED,
                blocking=BlockingMode.NOT_BLOCKED,
                layer=2,
            )
            sprites.append(empty)
            sprites.append(filled)

    # 6c. Halo (one per level, REMOVED initially).
    halo = Sprite(
        pixels=HALO_PIXELS,
        name="halo",
        x=0,
        y=0,
        tags=["halo"],
        interaction=InteractionMode.REMOVED,
        blocking=BlockingMode.NOT_BLOCKED,
        layer=3,
    )
    sprites.append(halo)

    # 6d. Edge strand sprites — one per pair × multiplicity.
    # Sort names alphabetically so that sprite names match what
    # `_attempt_edge` and `_get_edge_strand` look up (which use
    # `tuple(sorted([name_a, name_b]))`).
    pos = {name: (cx, cy) for name, cx, cy, _ in nodes}
    names = sorted(n[0] for n in nodes)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            ni, nj = names[i], names[j]
            xi, yi = pos[ni]
            xj, yj = pos[nj]
            for k in range(max_mult):
                cells = _line_cells_for_strand(xi, yi, xj, yj, k)
                pixels, xmin, ymin = _strand_sprite_pixels(cells)
                strand = Sprite(
                    pixels=pixels,
                    name=f"edge__{ni}__{nj}__{k}",
                    x=xmin,
                    y=ymin,
                    tags=[
                        "edge",
                        f"pair_{ni}_{nj}",
                    ],
                    interaction=InteractionMode.REMOVED,
                    blocking=BlockingMode.NOT_BLOCKED,
                    layer=1,
                )
                sprites.append(strand)

    return Level(
        sprites=sprites,
        grid_size=(32, 32),
        data={
            "max_edge_multiplicity": max_mult,
            "target_degrees": dict(target_degrees),
            "step_budget": layout["step_budget"],
            "level_palette": list(layout["level_palette"]),
            "node_starting_colors": {
                name: color for name, _, _, color in nodes
            },
            "node_positions": {
                name: (cx, cy) for name, cx, cy, _ in nodes
            },
        },
    )


levels = [_build_level(LAYOUT_L1), _build_level(LAYOUT_L2), _build_level(LAYOUT_L3)]


# ---------------------------------------------------------------------
# 7. HUD WIDGET — depleting step counter at the bottom row
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self) -> None:
        super().__init__()
        self.max = 30
        self.current = 30

    def set_max(self, value: int) -> None:
        self.max = max(1, int(value))
        self.current = self.max

    def set_current(self, value: int) -> None:
        self.current = max(0, int(value))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max <= 0:
            return frame
        width_pixels = max(0, int(64 * self.current / self.max))
        frame[63, :] = HUD_BG_COLOR
        if width_pixels > 0:
            frame[63, :width_pixels] = HUD_FILL_COLOR
        return frame


# ---------------------------------------------------------------------
# 8. THE GAME CLASS
# ---------------------------------------------------------------------
class Jx5k(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_hud = StepCounterHud()
        camera = Camera(
            width=32,
            height=32,
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_hud],
        )
        super().__init__(
            game_id="jx5k",
            levels=levels,
            camera=camera,
            available_actions=[5, 6],
        )

    # ---- engine hooks ----

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        self._max_edge_multiplicity = level.get_data("max_edge_multiplicity")
        self._target_degrees = dict(level.get_data("target_degrees"))
        self._step_remaining = int(level.get_data("step_budget"))
        self._level_palette = list(level.get_data("level_palette"))
        self._node_color = dict(level.get_data("node_starting_colors"))
        self._node_positions = dict(level.get_data("node_positions"))
        self._selected_node: Optional[str] = None
        self._reject_flash_phase = 0
        self._edge_state: dict = {}

        self._step_counter_hud.set_max(self._step_remaining)
        self._step_counter_hud.set_current(self._step_remaining)

        # Reset all pips and edges to baseline (engine clones each level fresh, so no need
        # to walk and reset; this is a defensive no-op for the initial load).

    def step(self) -> None:
        if self._step_remaining <= 0:
            self.lose()
            self.complete_action()
            return

        self._step_remaining -= 1
        self._step_counter_hud.set_current(self._step_remaining)

        if self._reject_flash_phase > 0:
            self._reject_flash_phase -= 1

        action_id = self.action.id
        if action_id == GameAction.ACTION5:
            self._handle_action5()
        elif action_id == GameAction.ACTION6:
            self._handle_action6()

        if self._check_win():
            self.next_level()
            self.complete_action()
            return

        if self._step_remaining <= 0 and not self._check_win():
            self.lose()
            self.complete_action()
            return

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.array([[self._reject_flash_phase]], dtype=np.int16)

    def _get_valid_actions(self) -> List[ActionInput]:
        # L1 (index 0): only ACTION6. L2/L3: ACTION5 + ACTION6.
        if self._current_level_index == 0:
            return [ActionInput(id=GameAction.ACTION6, data={"x": 0, "y": 0})]
        return [
            ActionInput(id=GameAction.ACTION5, data={}),
            ActionInput(id=GameAction.ACTION6, data={"x": 0, "y": 0}),
        ]

    # ---- action handlers ----

    def _handle_action5(self) -> None:
        if self._selected_node is None:
            return
        name = self._selected_node
        current = self._node_color[name]
        palette = self._level_palette
        if current not in palette or len(palette) <= 1:
            self._deselect()
            return
        idx = palette.index(current)
        new_color = palette[(idx + 1) % len(palette)]
        self._set_node_color(name, new_color)
        self._deselect()

    def _handle_action6(self) -> None:
        x = int(self.action.data.get("x", 0))
        y = int(self.action.data.get("y", 0))
        grid = self.camera.display_to_grid(x, y)
        if grid is None:
            self._deselect()
            return
        gx, gy = grid

        clicked_node = self._find_node_at(gx, gy)
        if clicked_node is not None:
            if self._selected_node is None:
                self._select(clicked_node)
            elif self._selected_node == clicked_node:
                self._deselect()
            else:
                self._attempt_edge(self._selected_node, clicked_node)
            return

        clicked_pair = self._find_edge_at(gx, gy)
        if clicked_pair is not None and self._max_edge_multiplicity >= 2:
            self._set_edge_state(clicked_pair, 0)
            self._deselect()
            return

        # Empty cell or non-actionable click
        self._deselect()

    # ---- selection ----

    def _select(self, name: str) -> None:
        self._selected_node = name
        halo = self._get_halo()
        if halo is None:
            return
        cx, cy = self._node_positions[name]
        halo.set_position(cx - 3, cy - 3)
        halo.set_interaction(InteractionMode.TANGIBLE)

    def _deselect(self) -> None:
        self._selected_node = None
        halo = self._get_halo()
        if halo is not None:
            halo.set_interaction(InteractionMode.REMOVED)

    # ---- edge management ----

    def _attempt_edge(self, name_a: str, name_b: str) -> None:
        pair = tuple(sorted([name_a, name_b]))
        if self._node_color[name_a] != self._node_color[name_b]:
            self._reject_flash_phase = REJECT_FLASH_FRAMES
            self._deselect()
            return
        if self._line_passes_through_other_node(name_a, name_b):
            self._reject_flash_phase = REJECT_FLASH_FRAMES
            self._deselect()
            return

        max_mult = self._max_edge_multiplicity
        current = self._edge_state.get(pair, 0)
        next_state = (current + 1) % (max_mult + 1)
        delta = next_state - current
        if delta > 0:
            # Adding edge(s) — reject if either endpoint would exceed its target degree.
            for endpoint in pair:
                if self._compute_node_degree(endpoint) + delta > self._target_degrees[endpoint]:
                    self._reject_flash_phase = REJECT_FLASH_FRAMES
                    self._deselect()
                    return
        self._set_edge_state(pair, next_state)
        self._deselect()

    def _set_edge_state(self, pair: tuple, new_state: int) -> None:
        self._edge_state[pair] = new_state
        ni, nj = pair
        for k in range(self._max_edge_multiplicity):
            strand = self._get_edge_strand(ni, nj, k)
            if strand is None:
                continue
            if k < new_state:
                strand.set_interaction(InteractionMode.TANGIBLE)
            else:
                strand.set_interaction(InteractionMode.REMOVED)
        self._refresh_pips(ni)
        self._refresh_pips(nj)

    def _refresh_pips(self, name: str) -> None:
        degree = self._compute_node_degree(name)
        target = self._target_degrees[name]
        for idx in range(target):
            empty = self._get_pip(name, idx, "empty")
            filled = self._get_pip(name, idx, "filled")
            if empty is None or filled is None:
                continue
            if idx < degree:
                empty.set_interaction(InteractionMode.REMOVED)
                filled.set_interaction(InteractionMode.TANGIBLE)
            else:
                empty.set_interaction(InteractionMode.TANGIBLE)
                filled.set_interaction(InteractionMode.REMOVED)

    def _set_node_color(self, name: str, new_color: int) -> None:
        old_color = self._node_color[name]
        if old_color == new_color:
            return
        self._node_color[name] = new_color
        old_variant = self._get_node_variant(name, old_color)
        new_variant = self._get_node_variant(name, new_color)
        if old_variant is not None:
            old_variant.set_interaction(InteractionMode.REMOVED)
        if new_variant is not None:
            new_variant.set_interaction(InteractionMode.TANGIBLE)

    # ---- predicates ----

    def _compute_node_degree(self, name: str) -> int:
        deg = 0
        for (i, j), mult in self._edge_state.items():
            if name == i or name == j:
                deg += mult
        return deg

    def _check_win(self) -> bool:
        for name, target in self._target_degrees.items():
            if self._compute_node_degree(name) != target:
                return False
        return True

    def _line_passes_through_other_node(self, name_a: str, name_b: str) -> bool:
        xa, ya = self._node_positions[name_a]
        xb, yb = self._node_positions[name_b]
        cells = _bresenham(xa, ya, xb, yb)
        if len(cells) <= 2:
            return False
        interior = cells[1:-1]
        for other_name, (cx, cy) in self._node_positions.items():
            if other_name in (name_a, name_b):
                continue
            sprite = self._get_node_variant(other_name, self._node_color[other_name])
            if sprite is None:
                continue
            sx, sy = sprite.x, sprite.y
            sw, sh = sprite.width, sprite.height
            for ix, iy in interior:
                if sx <= ix < sx + sw and sy <= iy < sy + sh:
                    return True
        return False

    # ---- sprite lookups ----

    def _find_node_at(self, gx: int, gy: int) -> Optional[str]:
        for sprite in self.current_level.get_sprites_by_tag("node"):
            if sprite.interaction != InteractionMode.TANGIBLE:
                continue
            sx, sy = sprite.x, sprite.y
            sw, sh = sprite.width, sprite.height
            if sx <= gx < sx + sw and sy <= gy < sy + sh:
                return sprite.name.split("__")[0]
        return None

    def _find_edge_at(self, gx: int, gy: int) -> Optional[tuple]:
        for sprite in self.current_level.get_sprites_by_tag("edge"):
            if sprite.interaction != InteractionMode.TANGIBLE:
                continue
            sx, sy = sprite.x, sprite.y
            sw, sh = sprite.width, sprite.height
            if not (sx <= gx < sx + sw and sy <= gy < sy + sh):
                continue
            local_x = gx - sx
            local_y = gy - sy
            if 0 <= local_y < sprite.pixels.shape[0] and 0 <= local_x < sprite.pixels.shape[1]:
                if int(sprite.pixels[local_y, local_x]) == EDGE_COLOR:
                    parts = sprite.name.split("__")
                    if len(parts) >= 4:
                        return (parts[1], parts[2])
        return None

    def _get_halo(self) -> Optional[Sprite]:
        sprites = self.current_level.get_sprites_by_tag("halo")
        return sprites[0] if sprites else None

    def _get_node_variant(self, name: str, color: int) -> Optional[Sprite]:
        tag_map = {
            NODE_BLUE: "colour_blue",
            NODE_RED: "colour_red",
            NODE_YELLOW: "colour_yellow",
        }
        tag = tag_map.get(color)
        if tag is None:
            return None
        for sprite in self.current_level.get_sprites_by_tag(f"node_{name}"):
            if tag in sprite.tags:
                return sprite
        return None

    def _get_edge_strand(self, ni: str, nj: str, k: int) -> Optional[Sprite]:
        target_name = f"edge__{ni}__{nj}__{k}"
        for sprite in self.current_level.get_sprites_by_tag(f"pair_{ni}_{nj}"):
            if sprite.name == target_name:
                return sprite
        return None

    def _get_pip(self, name: str, idx: int, kind: str) -> Optional[Sprite]:
        target_name = f"pip_{kind}__{name}_{idx}"
        for sprite in self.current_level.get_sprites_by_tag(f"pip_node_{name}"):
            if sprite.name == target_name:
                return sprite
        return None
