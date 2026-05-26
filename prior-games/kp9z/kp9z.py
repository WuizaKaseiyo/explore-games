"""NovaPlay game kp9z."""

from __future__ import annotations

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


# ---------------------------------------------------------------------
# Palette constants
# ---------------------------------------------------------------------
PALETTE_BACKDROP = 2
PALETTE_FRAME = 4
PALETTE_SOURCE = 6
PALETTE_CURRENT_PIP = 11
PALETTE_REDIRECTOR = 12
PALETTE_TARGET = 13
PALETTE_TARGET_PIP = 14

PALETTE_HUD_FILL = 14
PALETTE_HUD_EMPTY = 4


# ---------------------------------------------------------------------
# Cell-sprite layout constants (12x12 sprite per conceptual cell)
# ---------------------------------------------------------------------
CELL_SIZE = 12
GRID_SIZE = (64, 64)

# Two well-separated dots — 1 vs 2 reads at a glance.
TARGET_DOT_SLOTS = [(2, 2), (2, 8)]


# ---------------------------------------------------------------------
# Orientation helpers
# ---------------------------------------------------------------------
ORIENTATION_DELTAS = {
    "north": (-1, 0),
    "south": (1, 0),
    "east": (0, 1),
    "west": (0, -1),
}

ORIENTATION_CW = {
    "north": "east",
    "east": "south",
    "south": "west",
    "west": "north",
}


# ---------------------------------------------------------------------
# Cell-pixel factory
# ---------------------------------------------------------------------
def _frame_color_for(cell_type: str) -> int:
    if cell_type == "source":
        return PALETTE_SOURCE
    if cell_type == "target":
        return PALETTE_TARGET
    if cell_type == "redirector":
        return PALETTE_REDIRECTOR
    return PALETTE_FRAME


def _build_cell_pixels(
    cell_type: str,
    target_count: int = 0,
    orientation: str = "south",
    current_count: int = 0,
) -> np.ndarray:
    p = np.full((CELL_SIZE, CELL_SIZE), PALETTE_BACKDROP, dtype=np.int32)
    fc = _frame_color_for(cell_type)
    p[0:2, :] = fc
    p[10:12, :] = fc
    p[:, 0:2] = fc
    p[:, 10:12] = fc

    if cell_type == "target":
        for i in range(min(target_count, len(TARGET_DOT_SLOTS))):
            sr, sc = TARGET_DOT_SLOTS[i]
            p[sr : sr + 2, sc : sc + 2] = PALETTE_TARGET_PIP

    if cell_type == "redirector":
        p[5:7, 5:7] = PALETTE_REDIRECTOR
        if orientation == "north":
            p[2:5, 5:7] = PALETTE_REDIRECTOR
        elif orientation == "south":
            p[7:10, 5:7] = PALETTE_REDIRECTOR
        elif orientation == "east":
            p[5:7, 7:10] = PALETTE_REDIRECTOR
        elif orientation == "west":
            p[5:7, 2:5] = PALETTE_REDIRECTOR
    else:
        # Vertical fill bar inside the inner area (rows 4..9 = 6 rows of fill).
        # 2 rows per grain; cap visible at 3 (4 is transient mid-topple).
        fill_levels = min(max(current_count, 0), 3)
        if fill_levels > 0:
            top_row = 10 - fill_levels * 2
            p[top_row:10, 2:10] = PALETTE_CURRENT_PIP

    return p


def _make_cell_sprite(
    name: str,
    cell_type: str,
    target_count: int = 0,
    orientation: str = "south",
) -> Sprite:
    pixels = _build_cell_pixels(cell_type, target_count, orientation)
    tags = ["cell", cell_type]
    if cell_type == "target":
        tags.append(f"target_{target_count}")
    if cell_type == "redirector":
        tags.append(f"redir_{orientation}")
    return Sprite(
        pixels=pixels.tolist(),
        name=name,
        visible=True,
        collidable=True,
        tags=tags,
        layer=0,
        interaction=InteractionMode.TANGIBLE,
    )


# ---------------------------------------------------------------------
# Level layouts
# ---------------------------------------------------------------------
L1_LAYOUT: dict[tuple[int, int], dict] = {
    (1, 1): {"type": "source"},
    (0, 1): {"type": "target", "target_count": 1},
    (1, 0): {"type": "target", "target_count": 1},
    (2, 1): {"type": "target", "target_count": 1},
    (1, 2): {"type": "target", "target_count": 1},
}

L2_LAYOUT: dict[tuple[int, int], dict] = {
    (2, 2): {"type": "source"},
    (1, 2): {"type": "target", "target_count": 2},
    (2, 1): {"type": "target", "target_count": 2},
    (2, 3): {"type": "target", "target_count": 2},
    (3, 2): {"type": "target", "target_count": 2},
}

L3_LAYOUT: dict[tuple[int, int], dict] = {
    (2, 2): {"type": "source"},
    (1, 2): {"type": "redirector", "orientation": "south"},
    (2, 3): {"type": "redirector", "orientation": "south"},
    (0, 2): {"type": "target", "target_count": 1},
    (2, 4): {"type": "target", "target_count": 1},
}


def _build_level(
    name: str,
    layout: dict[tuple[int, int], dict],
    board_size: int,
    anchor: tuple[int, int],
    step_budget: int,
) -> Level:
    placed_sprites: list[Sprite] = []
    full_layout: dict[tuple[int, int], dict] = {}
    for r in range(board_size):
        for c in range(board_size):
            info = layout.get((r, c), {"type": "regular"})
            full_layout[(r, c)] = info
            cell_type = info["type"]
            target_count = info.get("target_count", 0)
            orientation = info.get("orientation", "south")
            sp_name = f"{name}_cell_{r}_{c}"
            sprite = _make_cell_sprite(
                sp_name, cell_type, target_count, orientation
            )
            ax, ay = anchor
            sprite.set_position(ax + CELL_SIZE * c, ay + CELL_SIZE * r)
            placed_sprites.append(sprite)
    return Level(
        name=name,
        sprites=placed_sprites,
        grid_size=GRID_SIZE,
        data={
            "step_budget": step_budget,
            "anchor": anchor,
            "board_size": board_size,
            "layout": full_layout,
        },
    )


levels: list[Level] = [
    _build_level("l1", L1_LAYOUT, 4, (8, 8), 8),
    _build_level("l2", L2_LAYOUT, 5, (2, 2), 16),
    _build_level("l3", L3_LAYOUT, 5, (2, 2), 28),
]


# ---------------------------------------------------------------------
# HUD
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self) -> None:
        super().__init__()
        self.max_steps = 1
        self.current_steps = 1

    def set_steps(self, current: int, maximum: int) -> None:
        self.max_steps = max(1, maximum)
        self.current_steps = max(0, min(current, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        ratio = self.current_steps / self.max_steps if self.max_steps else 0.0
        bar_width = max(0, min(64, int(round(64 * ratio))))
        frame[63, :bar_width] = PALETTE_HUD_FILL
        frame[63, bar_width:] = PALETTE_HUD_EMPTY
        return frame


# ---------------------------------------------------------------------
# Game
# ---------------------------------------------------------------------
class Kp9z(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = StepCounterHud()
        self.steps_left: int = 0
        self.max_steps: int = 0
        self.anchor: tuple[int, int] = (0, 0)
        self.board_size: int = 0
        self.cell_types: dict[tuple[int, int], str] = {}
        self.target_counts: dict[tuple[int, int], int] = {}
        self.grain_counts: dict[tuple[int, int], int] = {}
        self.redirector_orientations: dict[tuple[int, int], str] = {}
        self.cell_sprites: dict[tuple[int, int], Sprite] = {}
        camera = Camera(
            background=PALETTE_BACKDROP,
            letter_box=PALETTE_FRAME,
            interfaces=[self._hud],
        )
        super().__init__(
            game_id="kp9z",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        anchor = level.get_data("anchor") or (0, 0)
        board_size = level.get_data("board_size") or 4
        step_budget = level.get_data("step_budget") or 8
        layout = level.get_data("layout") or {}

        self.anchor = tuple(anchor)
        self.board_size = int(board_size)
        self.max_steps = int(step_budget)
        self.steps_left = self.max_steps
        self._hud.set_steps(self.steps_left, self.max_steps)

        self.cell_types = {}
        self.target_counts = {}
        self.grain_counts = {}
        self.redirector_orientations = {}
        self.cell_sprites = {}

        for r in range(self.board_size):
            for c in range(self.board_size):
                info = layout.get((r, c), {"type": "regular"})
                self.cell_types[(r, c)] = info["type"]
                self.target_counts[(r, c)] = int(info.get("target_count", 0))
                self.grain_counts[(r, c)] = 0
                if info["type"] == "redirector":
                    self.redirector_orientations[(r, c)] = info.get(
                        "orientation", "south"
                    )

        for sprite in level.get_sprites():
            if not sprite.tags or "cell" not in sprite.tags:
                continue
            parts = sprite.name.split("_")
            try:
                r = int(parts[-2])
                c = int(parts[-1])
            except (ValueError, IndexError):
                continue
            self.cell_sprites[(r, c)] = sprite

        self._refresh_cell_pixels()

    # -- cascade helpers -----------------------------------------------

    def _deliver_grain(self, r: int, c: int) -> None:
        if (r, c) not in self.grain_counts:
            return
        self.grain_counts[(r, c)] += 1

    def _resolve_cascade(self) -> None:
        max_iterations = max(1, self.board_size * self.board_size * 8)
        for _ in range(max_iterations):
            progressed = False
            for (r, c), grains in list(self.grain_counts.items()):
                cell_type = self.cell_types[(r, c)]
                if cell_type == "redirector":
                    if grains >= 1:
                        self.grain_counts[(r, c)] = 0
                        orientation = self.redirector_orientations[(r, c)]
                        dr, dc = ORIENTATION_DELTAS[orientation]
                        self._deliver_grain(r + dr, c + dc)
                        progressed = True
                else:
                    if grains >= 4:
                        self.grain_counts[(r, c)] = grains - 4
                        self._deliver_grain(r - 1, c)
                        self._deliver_grain(r + 1, c)
                        self._deliver_grain(r, c - 1)
                        self._deliver_grain(r, c + 1)
                        progressed = True
            if not progressed:
                break

    # -- visual refresh -----------------------------------------------

    def _refresh_cell_pixels(self) -> None:
        for (r, c), sprite in self.cell_sprites.items():
            cell_type = self.cell_types[(r, c)]
            target_count = self.target_counts[(r, c)]
            grains = self.grain_counts[(r, c)]
            orientation = self.redirector_orientations.get((r, c), "south")
            arr = _build_cell_pixels(
                cell_type, target_count, orientation, grains
            )
            sprite.pixels = arr

    # -- win/lose -----------------------------------------------------

    def _check_win(self) -> bool:
        for (r, c), grains in self.grain_counts.items():
            if self.cell_types[(r, c)] != "target":
                continue
            if grains != self.target_counts[(r, c)]:
                return False
        return True

    def _check_overshoot(self) -> bool:
        for (r, c), grains in self.grain_counts.items():
            if self.cell_types[(r, c)] != "target":
                continue
            if grains > self.target_counts[(r, c)]:
                return True
        return False

    # -- step ---------------------------------------------------------

    def step(self) -> None:
        if self.action.id == GameAction.ACTION6:
            data = self.action.data or {}
            cx = int(data.get("x", 0))
            cy = int(data.get("y", 0))
            grid = self.camera.display_to_grid(cx, cy)
            if grid is not None:
                gx, gy = grid
                ax, ay = self.anchor
                col = (gx - ax) // CELL_SIZE
                row = (gy - ay) // CELL_SIZE
                if 0 <= row < self.board_size and 0 <= col < self.board_size:
                    cell_type = self.cell_types.get((row, col))
                    if cell_type == "source":
                        self.grain_counts[(row, col)] += 1
                        self._resolve_cascade()
                    elif cell_type == "redirector":
                        prev = self.redirector_orientations[(row, col)]
                        self.redirector_orientations[(row, col)] = ORIENTATION_CW[prev]

        self._refresh_cell_pixels()

        self.steps_left = max(0, self.steps_left - 1)
        self._hud.set_steps(self.steps_left, self.max_steps)

        if self._check_win():
            if self._current_level_index == len(self._levels) - 1:
                self.win()
            else:
                self.next_level()
        elif self._check_overshoot() or self.steps_left <= 0:
            self.lose()

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        size = max(1, self.board_size)
        arr = np.zeros((size, size), dtype=np.int16)
        for (r, c), grains in self.grain_counts.items():
            if 0 <= r < size and 0 <= c < size:
                arr[r, c] = grains
        return arr
