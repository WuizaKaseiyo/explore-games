"""Generated game hb5n."""

import numpy as np
from novaengine import (
    ActionInput,
    NovaBaseGame,
    Camera,
    GameAction,
    InteractionMode,
    Level,
    RenderableUserDisplay,
    Sprite,
)

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------
CELL_PX = 4
GRID_PX = 64

BACKGROUND = 1
PADDING = 2

WALL_FILL = 5
WALL_INNER = 4

AVATAR_FRAME = 8
ANCHOR_CENTER = 12
BODY_CENTER = 13

PICKUP_FRAME = 14
PICKUP_CENTER = 11

TARGET_OUTLINE = 3

HUD_FILL = PICKUP_FRAME
HUD_EMPTY = WALL_INNER

# ---------------------------------------------------------------------
# Cell pixel patterns (each cell is 4x4 display pixels)
# ---------------------------------------------------------------------
ANCHOR_PATTERN = [
    [AVATAR_FRAME, AVATAR_FRAME, AVATAR_FRAME, AVATAR_FRAME],
    [AVATAR_FRAME, ANCHOR_CENTER, ANCHOR_CENTER, AVATAR_FRAME],
    [AVATAR_FRAME, ANCHOR_CENTER, ANCHOR_CENTER, AVATAR_FRAME],
    [AVATAR_FRAME, AVATAR_FRAME, AVATAR_FRAME, AVATAR_FRAME],
]

BODY_PATTERN = [
    [AVATAR_FRAME, AVATAR_FRAME, AVATAR_FRAME, AVATAR_FRAME],
    [AVATAR_FRAME, BODY_CENTER, BODY_CENTER, AVATAR_FRAME],
    [AVATAR_FRAME, BODY_CENTER, BODY_CENTER, AVATAR_FRAME],
    [AVATAR_FRAME, AVATAR_FRAME, AVATAR_FRAME, AVATAR_FRAME],
]

WALL_PATTERN = [
    [WALL_FILL, WALL_INNER, WALL_FILL, WALL_FILL],
    [WALL_FILL, WALL_INNER, WALL_FILL, WALL_FILL],
    [WALL_INNER, WALL_INNER, WALL_INNER, WALL_INNER],
    [WALL_FILL, WALL_FILL, WALL_INNER, WALL_FILL],
]

PICKUP_PATTERN = [
    [PICKUP_FRAME, PICKUP_FRAME, PICKUP_FRAME, PICKUP_FRAME],
    [PICKUP_FRAME, PICKUP_CENTER, PICKUP_CENTER, PICKUP_FRAME],
    [PICKUP_FRAME, PICKUP_CENTER, PICKUP_CENTER, PICKUP_FRAME],
    [PICKUP_FRAME, PICKUP_FRAME, PICKUP_FRAME, PICKUP_FRAME],
]

TARGET_PATTERN = [
    [TARGET_OUTLINE, TARGET_OUTLINE, TARGET_OUTLINE, TARGET_OUTLINE],
    [TARGET_OUTLINE, -1, -1, TARGET_OUTLINE],
    [TARGET_OUTLINE, -1, -1, TARGET_OUTLINE],
    [TARGET_OUTLINE, TARGET_OUTLINE, TARGET_OUTLINE, TARGET_OUTLINE],
]

# ---------------------------------------------------------------------
# Sprite bank
# ---------------------------------------------------------------------
sprites = {
    "anchor_cell": Sprite(
        pixels=ANCHOR_PATTERN,
        name="anchor_cell",
        tags=["avatar_anchor"],
        layer=2,
        collidable=False,
    ),
    "body_cell": Sprite(
        pixels=BODY_PATTERN,
        name="body_cell",
        tags=["avatar_body"],
        layer=2,
        collidable=False,
    ),
    "wall": Sprite(
        pixels=WALL_PATTERN,
        name="wall",
        tags=["wall"],
        layer=0,
        collidable=True,
    ),
    "pickup": Sprite(
        pixels=PICKUP_PATTERN,
        name="pickup",
        tags=["pickup"],
        layer=1,
        collidable=False,
    ),
    "target_cell": Sprite(
        pixels=TARGET_PATTERN,
        name="target_cell",
        tags=["target"],
        layer=0,
        collidable=False,
    ),
}


def _place(key: str, cx: int, cy: int) -> Sprite:
    return sprites[key].clone().set_position(cx * CELL_PX, cy * CELL_PX)


def _outer_ring() -> list[Sprite]:
    out: list[Sprite] = []
    for c in range(16):
        out.append(_place("wall", c, 0))
        out.append(_place("wall", c, 15))
    for r in range(1, 15):
        out.append(_place("wall", 0, r))
        out.append(_place("wall", 15, r))
    return out


# ---------------------------------------------------------------------
# Levels
# ---------------------------------------------------------------------

# L1: 3-cell L avatar at (2,2) → target L at rotation 270 at (12,12).
_l1: list[Sprite] = _outer_ring()
for (c, r) in [(12, 12), (12, 13), (13, 13)]:
    _l1.append(_place("target_cell", c, r))

# L2: 3-cell L avatar + 1 pickup → 4-cell L-tetromino at rotation 90.
_l2: list[Sprite] = _outer_ring()
for (c, r) in [(12, 12), (12, 11), (11, 11), (12, 13)]:
    _l2.append(_place("target_cell", c, r))
_l2.append(_place("pickup", 5, 4))

# L3: 3-cell L avatar + EXACTLY 3 of 5 pickups → 6-cell + shape at rotation 90.
_l3: list[Sprite] = _outer_ring()
for (c, r) in [(12, 12), (12, 11), (11, 11), (12, 13), (13, 12), (11, 12)]:
    _l3.append(_place("target_cell", c, r))
# 5 pickups; the witness uses p1, p2, p3. p4 and p5 are decoys.
for (c, r) in [(5, 3), (5, 5), (5, 7), (8, 4), (8, 6)]:
    _l3.append(_place("pickup", c, r))

levels = [
    Level(
        sprites=_l1,
        grid_size=(GRID_PX, GRID_PX),
        data={"level_id": 1, "step_budget": 50},
    ),
    Level(
        sprites=_l2,
        grid_size=(GRID_PX, GRID_PX),
        data={"level_id": 2, "step_budget": 60},
    ),
    Level(
        sprites=_l3,
        grid_size=(GRID_PX, GRID_PX),
        data={"level_id": 3, "step_budget": 100},
    ),
]


BACKGROUND_COLOR = BACKGROUND
PADDING_COLOR = PADDING


# ---------------------------------------------------------------------
# HUD widget
# ---------------------------------------------------------------------
class StepCounterOverlay(RenderableUserDisplay):
    def __init__(self) -> None:
        super().__init__()
        self.maximum: int = 0
        self.current: int = 0

    def set_state(self, current: int, maximum: int) -> None:
        self.maximum = maximum
        self.current = max(0, min(current, maximum))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.maximum <= 0:
            return frame
        filled = int(round(64 * self.current / self.maximum))
        frame[63, :] = HUD_EMPTY
        if filled > 0:
            frame[63, :filled] = HUD_FILL
        return frame


# ---------------------------------------------------------------------
# Rotation helper
# ---------------------------------------------------------------------
def _rotate_cw(rel: tuple[int, int], k: int) -> tuple[int, int]:
    x, y = rel
    for _ in range(k % 4):
        x, y = -y, x
    return (x, y)


def _rotate_ccw(rel: tuple[int, int], k: int) -> tuple[int, int]:
    """Inverse of _rotate_cw(rel, k)."""
    return _rotate_cw(rel, (4 - k) % 4)


# ---------------------------------------------------------------------
# The game class
# ---------------------------------------------------------------------
class Hb5n(NovaBaseGame):
    def __init__(self) -> None:
        # Initialise state BEFORE super().__init__() because the base
        # constructor immediately calls set_level(0), which calls
        # on_set_level, which mutates these attributes.
        self.avatar_anchor: tuple[int, int] = (0, 0)
        self.avatar_rotation: int = 0
        self.avatar_relative_cells: list[tuple[int, int]] = [(0, 0), (-1, 0), (-1, 1)]
        self.avatar_sprites: list[Sprite] = []
        self.wall_cells: set[tuple[int, int]] = set()
        self.target_cells: set[tuple[int, int]] = set()
        self.pickup_cells: set[tuple[int, int]] = set()
        self.step_budget: int = 0
        self.step_remaining: int = 0

        self._step_hud = StepCounterOverlay()
        camera = Camera(
            background=BACKGROUND,
            letter_box=PADDING,
            interfaces=[self._step_hud],
        )
        super().__init__(
            game_id="hb5n",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    # -----------------------------------------------------------------
    # Per-level setup
    # -----------------------------------------------------------------
    def on_set_level(self, level: Level) -> None:
        level_id = level.get_data("level_id")
        if level_id == 3:
            self.avatar_anchor = (3, 3)
        else:
            self.avatar_anchor = (2, 2)
        self.avatar_rotation = 0
        self.avatar_relative_cells = [(0, 0), (-1, 0), (-1, 1)]

        self.avatar_sprites = []
        ax, ay = self.avatar_anchor
        for i, (rx, ry) in enumerate(self.avatar_relative_cells):
            kind = "anchor_cell" if i == 0 else "body_cell"
            s = sprites[kind].clone().set_position(
                (ax + rx) * CELL_PX, (ay + ry) * CELL_PX
            )
            level.add_sprite(s)
            self.avatar_sprites.append(s)

        self.wall_cells = {
            (w.x // CELL_PX, w.y // CELL_PX)
            for w in level.get_sprites_by_tag("wall")
        }
        self.target_cells = {
            (t.x // CELL_PX, t.y // CELL_PX)
            for t in level.get_sprites_by_tag("target")
        }
        self.pickup_cells = {
            (p.x // CELL_PX, p.y // CELL_PX)
            for p in level.get_sprites_by_tag("pickup")
        }

        budget = level.get_data("step_budget") or 0
        self.step_budget = int(budget)
        self.step_remaining = self.step_budget
        self._step_hud.set_state(self.step_remaining, self.step_budget)

    # -----------------------------------------------------------------
    # Geometry helpers
    # -----------------------------------------------------------------
    def _absolute_cells_for(
        self,
        anchor: tuple[int, int],
        rotation: int,
        relative_cells: list[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        ax, ay = anchor
        out: list[tuple[int, int]] = []
        for rel in relative_cells:
            rx, ry = _rotate_cw(rel, rotation)
            out.append((ax + rx, ay + ry))
        return out

    def _absolute_cells(self) -> list[tuple[int, int]]:
        return self._absolute_cells_for(
            self.avatar_anchor, self.avatar_rotation, self.avatar_relative_cells
        )

    def _cells_valid(self, cells: list[tuple[int, int]]) -> bool:
        for cx, cy in cells:
            if cx < 1 or cx > 14 or cy < 1 or cy > 14:
                return False
            if (cx, cy) in self.wall_cells:
                return False
        return True

    def _redraw_avatar(self) -> None:
        for s, (cx, cy) in zip(self.avatar_sprites, self._absolute_cells()):
            s.set_position(cx * CELL_PX, cy * CELL_PX)

    # -----------------------------------------------------------------
    # Action handlers
    # -----------------------------------------------------------------
    def _try_translate(self, dx: int, dy: int) -> bool:
        new_anchor = (self.avatar_anchor[0] + dx, self.avatar_anchor[1] + dy)
        new_cells = self._absolute_cells_for(
            new_anchor, self.avatar_rotation, self.avatar_relative_cells
        )
        if self._cells_valid(new_cells):
            self.avatar_anchor = new_anchor
            self._redraw_avatar()
            return True
        return False

    def _try_rotate(self) -> bool:
        new_rotation = (self.avatar_rotation + 1) % 4
        new_cells = self._absolute_cells_for(
            self.avatar_anchor, new_rotation, self.avatar_relative_cells
        )
        if self._cells_valid(new_cells):
            self.avatar_rotation = new_rotation
            self._redraw_avatar()
            return True
        return False

    def _try_absorb_pickups(self) -> None:
        """Absorb every pickup that is orthogonally adjacent to any avatar
        cell. Each absorption adds a new body cell at the pickup's absolute
        position. The relative-cell entry is computed by inverse-rotating
        the pickup-to-anchor offset into the rotation-0 frame so subsequent
        rotations carry the new cell correctly. Cascades: after one
        absorption the new body cell may bring another pickup into
        adjacency, so the loop repeats until no further absorptions fire.
        Absorption is rejected if (a) the pickup's cell coincides with an
        existing avatar cell, or (b) the computed rotation-0 relative offset
        is already in the relative-cells list.
        """
        while True:
            absorbed_any = False
            avatar_cells = set(self._absolute_cells())
            for cell in list(self.pickup_cells):
                pcx, pcy = cell
                if (pcx, pcy) in avatar_cells:
                    continue
                adjacent = any(
                    abs(av[0] - pcx) + abs(av[1] - pcy) == 1
                    for av in avatar_cells
                )
                if not adjacent:
                    continue
                ax, ay = self.avatar_anchor
                display_rel = (pcx - ax, pcy - ay)
                rotation_0_rel = _rotate_ccw(display_rel, self.avatar_rotation)
                if rotation_0_rel in self.avatar_relative_cells:
                    continue
                # Absorb.
                for p in self.current_level.get_sprites_by_tag("pickup"):
                    if (p.x // CELL_PX, p.y // CELL_PX) == cell:
                        p.set_interaction(InteractionMode.REMOVED)
                        break
                self.pickup_cells.discard(cell)
                self.avatar_relative_cells.append(rotation_0_rel)
                s = sprites["body_cell"].clone().set_position(
                    pcx * CELL_PX, pcy * CELL_PX
                )
                self.current_level.add_sprite(s)
                self.avatar_sprites.append(s)
                absorbed_any = True
                break
            if not absorbed_any:
                break

    # -----------------------------------------------------------------
    # Engine entry points
    # -----------------------------------------------------------------
    def step(self) -> None:
        self.step_remaining -= 1
        action_id = self.action.id
        if action_id == GameAction.ACTION1:
            self._try_translate(0, -1)
        elif action_id == GameAction.ACTION2:
            self._try_translate(0, 1)
        elif action_id == GameAction.ACTION3:
            self._try_translate(-1, 0)
        elif action_id == GameAction.ACTION4:
            self._try_translate(1, 0)
        elif action_id == GameAction.ACTION5:
            self._try_rotate()

        self._step_hud.set_state(self.step_remaining, self.step_budget)

        self._try_absorb_pickups()

        if self._check_win():
            self.next_level()
            self.complete_action()
            return
        if self._check_lose():
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _check_win(self) -> bool:
        return set(self._absolute_cells()) == self.target_cells

    def _check_lose(self) -> bool:
        return self.step_remaining <= 0 and not self._check_win()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self.step_remaining
        state[0, 1] = self.avatar_rotation
        state[0, 2] = len(self.avatar_relative_cells)
        state[0, 3] = len(self.pickup_cells)
        return state

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()
