"""Generated game source — schema follows code/universal-scaffold.md."""

from typing import Dict, List, Optional, Tuple

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
# 1. SPRITE BANK
# ---------------------------------------------------------------------

def _build_perimeter_pixels() -> List[List[int]]:
    """A 64x64 array whose outer 4-cell ring carries the brick pattern."""
    pixels = [[-1] * 64 for _ in range(64)]
    brick = [[3, 3, 3, 3], [3, 5, 5, 3], [3, 5, 5, 3], [3, 3, 3, 3]]
    for cell_x in range(16):
        for r in range(4):
            for c in range(4):
                pixels[r][cell_x * 4 + c] = brick[r][c]
                pixels[60 + r][cell_x * 4 + c] = brick[r][c]
    for cell_y in range(1, 15):
        for r in range(4):
            for c in range(4):
                pixels[cell_y * 4 + r][c] = brick[r][c]
                pixels[cell_y * 4 + r][60 + c] = brick[r][c]
    return pixels


sprites: Dict[str, Sprite] = {
    "anchor_pillar": Sprite(
        pixels=[
            [5, 3, 3, 5],
            [3, 1, 1, 3],
            [3, 1, 1, 3],
            [5, 3, 3, 5],
        ],
        name="anchor_pillar",
        visible=True,
        collidable=True,
        tags=["anchor", "blocker"],
        layer=1,
    ),
    "item_blue_bar": Sprite(
        pixels=[
            [-1, 9, 9, -1],
            [-1, 9, 9, -1],
            [-1, 9, 9, -1],
            [-1, 9, 9, -1],
        ],
        name="item_blue_bar",
        visible=True,
        collidable=True,
        blocking=BlockingMode.BOUNDING_BOX,
        tags=["item", "shape_bar"],
        layer=1,
    ),
    "item_orange_blob": Sprite(
        pixels=[
            [-1, 12, 12, -1],
            [12, 12, 12, 12],
            [12, 12, 12, 12],
            [-1, 12, 12, -1],
        ],
        name="item_orange_blob",
        visible=True,
        collidable=True,
        blocking=BlockingMode.BOUNDING_BOX,
        tags=["item", "shape_blob"],
        layer=1,
    ),
    "item_pink_ring": Sprite(
        pixels=[
            [-1, 7, 7, -1],
            [7, -1, -1, 7],
            [7, -1, -1, 7],
            [-1, 7, 7, -1],
        ],
        name="item_pink_ring",
        visible=True,
        collidable=True,
        blocking=BlockingMode.BOUNDING_BOX,
        tags=["item", "shape_ring"],
        layer=1,
    ),
    "item_yellow_checker": Sprite(
        pixels=[
            [11, -1, 11, -1],
            [-1, 11, -1, 11],
            [11, -1, 11, -1],
            [-1, 11, -1, 11],
        ],
        name="item_yellow_checker",
        visible=True,
        collidable=True,
        blocking=BlockingMode.BOUNDING_BOX,
        tags=["item", "shape_checker"],
        layer=1,
    ),
    "perimeter_walls": Sprite(
        pixels=_build_perimeter_pixels(),
        name="perimeter_walls",
        visible=True,
        collidable=True,
        tags=["wall", "blocker"],
        layer=0,
    ),
    "player": Sprite(
        pixels=[
            [13, 0, 0, 13],
            [13, 13, 13, 13],
            [13, 13, 13, 13],
            [13, 13, 13, 13],
        ],
        name="player",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=2,
    ),
    "preview_blue_bar": Sprite(
        pixels=[
            [-1, 9, 9, -1],
            [-1, 9, 9, -1],
            [-1, 9, 9, -1],
            [-1, 9, 9, -1],
        ],
        name="preview_blue_bar",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["preview"],
        layer=0,
    ),
    "preview_orange_blob": Sprite(
        pixels=[
            [-1, 12, 12, -1],
            [12, 12, 12, 12],
            [12, 12, 12, 12],
            [-1, 12, 12, -1],
        ],
        name="preview_orange_blob",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["preview"],
        layer=0,
    ),
    "preview_pink_ring": Sprite(
        pixels=[
            [-1, 7, 7, -1],
            [7, -1, -1, 7],
            [7, -1, -1, 7],
            [-1, 7, 7, -1],
        ],
        name="preview_pink_ring",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["preview"],
        layer=0,
    ),
    "preview_yellow_checker": Sprite(
        pixels=[
            [11, -1, 11, -1],
            [-1, 11, -1, 11],
            [11, -1, 11, -1],
            [-1, 11, -1, 11],
        ],
        name="preview_yellow_checker",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["preview"],
        layer=0,
    ),
    "sweeper": Sprite(
        pixels=[
            [-1, 2, 2, -1],
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [-1, 2, 2, -1],
        ],
        name="sweeper",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["sweeper"],
        layer=3,
    ),
    "wall": Sprite(
        pixels=[
            [3, 3, 3, 3],
            [3, 5, 5, 3],
            [3, 5, 5, 3],
            [3, 3, 3, 3],
        ],
        name="wall",
        visible=True,
        collidable=True,
        tags=["wall", "blocker"],
        layer=0,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

CELL = 4  # cell stride in pixels


def _at(cell_x: int, cell_y: int) -> Tuple[int, int]:
    return cell_x * CELL, cell_y * CELL


levels: List[Level] = [
    # ------ Level 1 ------
    Level(
        sprites=[
            sprites["perimeter_walls"].clone().set_position(0, 0),
            sprites["preview_blue_bar"].clone().set_position(*_at(5, 1)),
            sprites["preview_orange_blob"].clone().set_position(*_at(6, 1)),
            sprites["preview_yellow_checker"].clone().set_position(*_at(7, 1)),
            sprites["preview_pink_ring"].clone().set_position(*_at(8, 1)),
            sprites["item_pink_ring"].clone().set_position(*_at(5, 8)),
            sprites["item_yellow_checker"].clone().set_position(*_at(6, 8)),
            sprites["item_orange_blob"].clone().set_position(*_at(7, 8)),
            sprites["item_blue_bar"].clone().set_position(*_at(8, 8)),
            sprites["player"].clone().set_position(*_at(2, 8)).set_rotation(90),
        ],
        grid_size=(64, 64),
        data={
            "step_budget": 50,
            "targets": [
                (5, 8, "shape_bar", 9),
                (6, 8, "shape_blob", 12),
                (7, 8, "shape_checker", 11),
                (8, 8, "shape_ring", 7),
            ],
        },
    ),
    # ------ Level 2 ------
    # Row 8 partitioned by anchor at (5,8); both segments must be reversed.
    # Walls at (5,7) and (5,9) make cell (5,8) unreachable for the avatar —
    # forcing the anchor to be the ONLY sweep-stop mid-line. Without the
    # anchor, the only reachable permutation of these 4 items via sweep is
    # the full-row reversal, which does NOT equal the per-segment-reversed
    # target — so the level is strictly unwinnable without the anchor.
    Level(
        sprites=[
            sprites["perimeter_walls"].clone().set_position(0, 0),
            sprites["preview_yellow_checker"].clone().set_position(*_at(3, 1)),
            sprites["preview_pink_ring"].clone().set_position(*_at(4, 1)),
            sprites["preview_blue_bar"].clone().set_position(*_at(6, 1)),
            sprites["preview_orange_blob"].clone().set_position(*_at(7, 1)),
            sprites["item_pink_ring"].clone().set_position(*_at(3, 8)),
            sprites["item_yellow_checker"].clone().set_position(*_at(4, 8)),
            sprites["anchor_pillar"].clone().set_position(*_at(5, 8)),
            sprites["item_orange_blob"].clone().set_position(*_at(6, 8)),
            sprites["item_blue_bar"].clone().set_position(*_at(7, 8)),
            sprites["wall"].clone().set_position(*_at(5, 7)),
            sprites["wall"].clone().set_position(*_at(5, 9)),
            sprites["player"].clone().set_position(*_at(1, 8)).set_rotation(90),
        ],
        grid_size=(64, 64),
        data={
            "step_budget": 100,
            "targets": [
                (3, 8, "shape_checker", 11),
                (4, 8, "shape_ring", 7),
                (6, 8, "shape_bar", 9),
                (7, 8, "shape_blob", 12),
            ],
        },
    ),
    # ------ Level 3 ------
    # A 3-row × 5-column grid of items with a single anchor at its centre
    # (7,5). The grid itself geometrically protects the anchor cell — every
    # cell cardinally adjacent to (7,5) is an item, so the avatar can never
    # walk onto the anchor cell regardless of the anchor sprite's presence.
    # Therefore no extra access-blocking walls are needed at L3.
    #
    # The target permutation reverses columns 5, 6, 8, 9 (full-column
    # reverses, requiring vertical sweeps) AND reverses both anchor-row
    # segments on row 5 (requiring horizontal sweeps that exploit the
    # anchor partition). Column 7 and rows 4 / 6 are NOT reversed
    # independently — row 4 and row 6 items get their final positions via
    # the column sweeps; column 7 has the anchor at (7,5) but neither (7,4)
    # nor (7,6) needs to move.
    Level(
        sprites=[
            sprites["perimeter_walls"].clone().set_position(0, 0),
            # Target preview — same 3×5 layout, rendered three rows below
            # the playable grid so the player can match cell-by-cell.
            sprites["preview_yellow_checker"].clone().set_position(*_at(5, 11)),
            sprites["preview_orange_blob"].clone().set_position(*_at(6, 11)),
            sprites["preview_yellow_checker"].clone().set_position(*_at(7, 11)),
            sprites["preview_pink_ring"].clone().set_position(*_at(8, 11)),
            sprites["preview_orange_blob"].clone().set_position(*_at(9, 11)),
            sprites["preview_pink_ring"].clone().set_position(*_at(5, 12)),
            sprites["preview_orange_blob"].clone().set_position(*_at(6, 12)),
            # gap at (7,12) corresponding to anchor at (7,5).
            sprites["preview_yellow_checker"].clone().set_position(*_at(8, 12)),
            sprites["preview_blue_bar"].clone().set_position(*_at(9, 12)),
            sprites["preview_pink_ring"].clone().set_position(*_at(5, 13)),
            sprites["preview_blue_bar"].clone().set_position(*_at(6, 13)),
            sprites["preview_blue_bar"].clone().set_position(*_at(7, 13)),
            sprites["preview_orange_blob"].clone().set_position(*_at(8, 13)),
            sprites["preview_pink_ring"].clone().set_position(*_at(9, 13)),
            # Playable 3×5 grid — row 4.
            sprites["item_pink_ring"].clone().set_position(*_at(5, 4)),
            sprites["item_blue_bar"].clone().set_position(*_at(6, 4)),
            sprites["item_yellow_checker"].clone().set_position(*_at(7, 4)),
            sprites["item_orange_blob"].clone().set_position(*_at(8, 4)),
            sprites["item_pink_ring"].clone().set_position(*_at(9, 4)),
            # Playable grid — row 5 (with central anchor).
            sprites["item_orange_blob"].clone().set_position(*_at(5, 5)),
            sprites["item_pink_ring"].clone().set_position(*_at(6, 5)),
            sprites["anchor_pillar"].clone().set_position(*_at(7, 5)),
            sprites["item_blue_bar"].clone().set_position(*_at(8, 5)),
            sprites["item_yellow_checker"].clone().set_position(*_at(9, 5)),
            # Playable grid — row 6.
            sprites["item_yellow_checker"].clone().set_position(*_at(5, 6)),
            sprites["item_orange_blob"].clone().set_position(*_at(6, 6)),
            sprites["item_blue_bar"].clone().set_position(*_at(7, 6)),
            sprites["item_pink_ring"].clone().set_position(*_at(8, 6)),
            sprites["item_orange_blob"].clone().set_position(*_at(9, 6)),
            sprites["player"].clone().set_position(*_at(1, 5)).set_rotation(90),
        ],
        grid_size=(64, 64),
        data={
            "step_budget": 250,
            "targets": [
                # Row 4 (after full-column reverses of cols 5,6,8,9; col 7 untouched).
                (5, 4, "shape_checker", 11),
                (6, 4, "shape_blob", 12),
                (7, 4, "shape_checker", 11),
                (8, 4, "shape_ring", 7),
                (9, 4, "shape_blob", 12),
                # Row 5 (anchor at col 7; both segments partial-reversed by horizontal sweeps).
                (5, 5, "shape_ring", 7),
                (6, 5, "shape_blob", 12),
                (8, 5, "shape_checker", 11),
                (9, 5, "shape_bar", 9),
                # Row 6 (after full-column reverses; col 7 untouched).
                (5, 6, "shape_ring", 7),
                (6, 6, "shape_bar", 9),
                (7, 6, "shape_bar", 9),
                (8, 6, "shape_blob", 12),
                (9, 6, "shape_ring", 7),
            ],
        },
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 4
PADDING_COLOR = 4
HUD_FILL = 7
HUD_EMPTY = 4


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    """Horizontal step-counter bar at row 63 of the rendered frame."""

    def __init__(self) -> None:
        self.budget = 0
        self.current = 0

    def reset(self, budget: int) -> None:
        self.budget = max(0, int(budget))
        self.current = self.budget

    def dec(self, n: int = 1) -> None:
        self.current = max(0, self.current - n)

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.budget == 0:
            return frame
        fraction = self.current / self.budget
        filled = int(round(64 * fraction))
        if filled > 64:
            filled = 64
        for x in range(64):
            frame[63, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Rs8n(NovaBaseGame):
    step_counter_hud: StepCounterHud
    sweep_phase: str
    sweep_axis: Tuple[int, int]
    sweep_cursor: Tuple[int, int]
    sweep_pickups: List[Tuple[Sprite, Tuple[int, int]]]
    sweeper_sprite: Optional[Sprite]
    return_drop_map: Dict[Tuple[int, int], Sprite]

    def __init__(self) -> None:
        self.step_counter_hud = StepCounterHud()
        self.sweep_phase = "idle"
        self.sweep_axis = (0, 0)
        self.sweep_cursor = (0, 0)
        self.sweep_pickups = []
        self.sweeper_sprite = None
        self.return_drop_map = {}
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_counter_hud],
        )
        super().__init__(
            game_id="rs8n",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    # ---- per-level setup ----

    def on_set_level(self, level: Level) -> None:
        budget = level.get_data("step_budget") or 0
        self.step_counter_hud.reset(int(budget))
        self.sweep_phase = "idle"
        self.sweep_axis = (0, 0)
        self.sweep_cursor = (0, 0)
        self.sweep_pickups = []
        self.return_drop_map = {}
        if self.sweeper_sprite is not None:
            try:
                level.remove_sprite(self.sweeper_sprite)
            except Exception:
                pass
            self.sweeper_sprite = None

    # ---- helpers ----

    def _player(self) -> Optional[Sprite]:
        sprites_p = self.current_level.get_sprites_by_tag("player")
        return sprites_p[0] if sprites_p else None

    @staticmethod
    def _rotation_to_delta(rot: int) -> Tuple[int, int]:
        if rot == 0:
            return (0, -CELL)
        if rot == 90:
            return (CELL, 0)
        if rot == 180:
            return (0, CELL)
        if rot == 270:
            return (-CELL, 0)
        return (0, 0)

    @staticmethod
    def _delta_to_rotation(dx: int, dy: int) -> int:
        if dy < 0:
            return 0
        if dx > 0:
            return 90
        if dy > 0:
            return 180
        if dx < 0:
            return 270
        return 0

    def _walk_blocked(self, x: int, y: int) -> bool:
        if x < 0 or x >= 64 or y < 0 or y >= 64:
            return True
        if self.current_level.get_sprite_at(x, y, "blocker") is not None:
            return True
        if self.current_level.get_sprite_at(x, y, "item") is not None:
            return True
        return False

    def _face_and_walk(self, dx: int, dy: int) -> None:
        player = self._player()
        if player is None:
            return
        rot = self._delta_to_rotation(dx, dy)
        player.set_rotation(rot)
        target_x = player.x + dx
        target_y = player.y + dy
        if not self._walk_blocked(target_x, target_y):
            player.set_position(target_x, target_y)

    @staticmethod
    def _dominant_palette(item: Sprite) -> int:
        pixels = item.pixels
        flat = pixels[pixels >= 0]
        if flat.size == 0:
            return -1
        return int(flat.flat[0])

    def _check_win(self) -> bool:
        targets = self.current_level.get_data("targets")
        if not targets:
            return False
        for cell_x, cell_y, shape_tag, palette in targets:
            x, y = cell_x * CELL, cell_y * CELL
            item = self.current_level.get_sprite_at(x, y, "item")
            if item is None:
                return False
            if shape_tag not in item.tags:
                return False
            if self._dominant_palette(item) != palette:
                return False
        return True

    def _check_lose(self) -> bool:
        return self.step_counter_hud.current <= 0

    # ---- sweep state machine ----

    def _start_sweep(self) -> None:
        player = self._player()
        if player is None:
            return
        rot = player.rotation
        dx, dy = self._rotation_to_delta(rot)
        self.sweep_axis = (dx, dy)
        self.sweep_cursor = (player.x + dx, player.y + dy)
        self.sweep_pickups = []
        self.return_drop_map = {}
        self.sweeper_sprite = sprites["sweeper"].clone()
        self.sweeper_sprite.set_position(*self.sweep_cursor)
        self.current_level.add_sprite(self.sweeper_sprite)
        self.sweep_phase = "outgoing"

    def _tick_outgoing(self) -> None:
        cur = self.sweep_cursor
        cx, cy = cur
        # Off-grid or blocker -> begin return.
        off_grid = cx < 0 or cx >= 64 or cy < 0 or cy >= 64
        blocker = (
            None
            if off_grid
            else self.current_level.get_sprite_at(cx, cy, "blocker")
        )
        if off_grid or blocker is not None:
            self._begin_return()
            return
        # Pickup.
        item = self.current_level.get_sprite_at(cx, cy, "item")
        if item is not None:
            self.current_level.remove_sprite(item)
            self.sweep_pickups.append((item, cur))
        # Advance.
        nxt = (cx + self.sweep_axis[0], cy + self.sweep_axis[1])
        self.sweep_cursor = nxt
        if self.sweeper_sprite is not None:
            self.sweeper_sprite.set_position(*nxt)

    def _begin_return(self) -> None:
        # Step the cursor back to the last valid (non-blocker) cell.
        back = (
            self.sweep_cursor[0] - self.sweep_axis[0],
            self.sweep_cursor[1] - self.sweep_axis[1],
        )
        self.sweep_cursor = back
        if self.sweeper_sprite is not None:
            self.sweeper_sprite.set_position(*back)
        # Build the drop-at-cell map.
        n = len(self.sweep_pickups)
        self.return_drop_map = {}
        for i in range(n):
            item = self.sweep_pickups[i][0]
            target_cell = self.sweep_pickups[n - 1 - i][1]
            self.return_drop_map[target_cell] = item
        self.sweep_phase = "return"

    def _finalize_sweep(self) -> None:
        if self.sweeper_sprite is not None:
            try:
                self.current_level.remove_sprite(self.sweeper_sprite)
            except Exception:
                pass
            self.sweeper_sprite = None
        self.sweep_phase = "idle"
        self.sweep_pickups = []
        self.return_drop_map = {}

    def _tick_return(self) -> None:
        cur = self.sweep_cursor
        player = self._player()
        if player is None:
            self._finalize_sweep()
            self.complete_action()
            return
        # If sweeper has reached the player's cell, finish.
        if cur == (player.x, player.y):
            self._finalize_sweep()
            if self._check_win():
                self.next_level()
            elif self._check_lose():
                self.lose()
            self.complete_action()
            return
        # Drop scheduled item at this cell.
        if cur in self.return_drop_map:
            item = self.return_drop_map.pop(cur)
            item.set_position(*cur)
            self.current_level.add_sprite(item)
        # Step backward.
        nxt = (cur[0] - self.sweep_axis[0], cur[1] - self.sweep_axis[1])
        self.sweep_cursor = nxt
        if self.sweeper_sprite is not None:
            self.sweeper_sprite.set_position(*nxt)

    # ---- step ----

    def step(self) -> None:
        if self.sweep_phase == "outgoing":
            self._tick_outgoing()
            return
        if self.sweep_phase == "return":
            self._tick_return()
            return

        aid = self.action.id
        if aid == GameAction.ACTION1:
            self._face_and_walk(0, -CELL)
        elif aid == GameAction.ACTION2:
            self._face_and_walk(0, CELL)
        elif aid == GameAction.ACTION3:
            self._face_and_walk(-CELL, 0)
        elif aid == GameAction.ACTION4:
            self._face_and_walk(CELL, 0)
        elif aid == GameAction.ACTION5:
            self.step_counter_hud.dec(1)
            self._start_sweep()
            return  # animation begins; do not call complete_action

        self.step_counter_hud.dec(1)
        if self._check_win():
            self.next_level()
        elif self._check_lose():
            self.lose()
        self.complete_action()

    # ---- introspection ----

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 4), dtype=np.int16)
        state[0, 0] = self.step_counter_hud.current
        player = self._player()
        if player is not None:
            state[0, 1] = player.x
            state[0, 2] = player.y
            state[0, 3] = player.rotation
        return state

    def _get_valid_actions(self) -> List[ActionInput]:
        if self.sweep_phase != "idle":
            return []
        return super()._get_valid_actions()
