"""kn58."""

from __future__ import annotations

import math
from typing import Iterable

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
# Module constants
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 2          # light-grey
PADDING_COLOR = 4             # off-black
WALL_COLOR = 5                # black
HUD_BAR_COLOR = 10            # light-blue
HUD_BG_COLOR = 4              # off-black
ORANGE = 12
PURPLE = 15
ANCHOR_RIM = 4
ANCHOR_INNER = 10
ANCHOR_CENTER = 0
ANTI_RIM = 8
ANTI_INNER = 4

# Logical-cell stride in frame pixels.
CELL = 4

# Frame size and HUD row.
FRAME_W = 64
FRAME_H = 64
HUD_ROW_Y = 60                # rows 60..63 reserved for HUD bar
PLAYFIELD_H = 60              # frame rows 0..59 are playable area


# ---------------------------------------------------------------------
# Sprite-bank pixel builders
# ---------------------------------------------------------------------
def _outer_frame_pixels() -> list[list[int]]:
    """A hollow 60x64 frame: 4-pixel-wide border on top/bottom/left/right; centre transparent."""
    rows: list[list[int]] = []
    for y in range(PLAYFIELD_H):
        row: list[int] = []
        for x in range(FRAME_W):
            if y < CELL or y >= PLAYFIELD_H - CELL or x < CELL or x >= FRAME_W - CELL:
                row.append(WALL_COLOR)
            else:
                row.append(-1)
        rows.append(row)
    return rows


def _l2_interior_wall_pixels() -> list[list[int]]:
    """Interior wall block for level 2.

    Covers logical (cx, cy) in 1..14 x 1..13 EXCEPT:
      - row 7 cols 1..14 (corridor)
      - col 7 rows 8..9 (pocket south of corridor)
    Sprite size: 14*CELL = 56 wide, 13*CELL = 52 tall.
    Place at frame pixel (1*CELL, 1*CELL) = (4, 4).
    """
    cells_w, cells_h = 14, 13
    rows: list[list[int]] = []
    for sy in range(cells_h * CELL):
        row: list[int] = []
        cy = (sy // CELL) + 1
        for sx in range(cells_w * CELL):
            cx = (sx // CELL) + 1
            is_corridor = cy == 7
            is_pocket = cx == 7 and cy in (8, 9)
            row.append(-1 if (is_corridor or is_pocket) else WALL_COLOR)
        rows.append(row)
    return rows


def _l3_interior_wall_pixels() -> list[list[int]]:
    """Horizontal wall strip for level 3 — covers row 8, cols 1..14, with a single gap at col 8.

    Sprite size: 14*CELL = 56 wide, CELL = 4 tall.
    Place at frame pixel (1*CELL, 8*CELL) = (4, 32).
    """
    cells_w = 14
    rows: list[list[int]] = []
    for sy in range(CELL):
        row: list[int] = []
        for sx in range(cells_w * CELL):
            cx = (sx // CELL) + 1
            row.append(-1 if cx == 8 else WALL_COLOR)
        rows.append(row)
    return rows


# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites: dict[str, Sprite] = {
    "anchor": Sprite(
        pixels=[
            [-1, ANCHOR_RIM, -1, -1],
            [ANCHOR_RIM, ANCHOR_INNER, ANCHOR_INNER, ANCHOR_RIM],
            [ANCHOR_RIM, ANCHOR_INNER, ANCHOR_CENTER, ANCHOR_INNER],
            [-1, ANCHOR_RIM, ANCHOR_INNER, ANCHOR_RIM],
        ],
        name="anchor",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["anchor"],
        layer=2,
    ),
    "anti_anchor": Sprite(
        pixels=[
            [ANTI_RIM, -1, ANTI_RIM, -1],
            [-1, ANTI_INNER, ANTI_INNER, ANTI_RIM],
            [ANTI_RIM, ANTI_INNER, ANTI_INNER, -1],
            [-1, ANTI_RIM, -1, ANTI_RIM],
        ],
        name="anti_anchor",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["anti_anchor"],
        layer=1,
    ),
    "frame_wall": Sprite(
        pixels=_outer_frame_pixels(),
        name="frame_wall",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    ),
    "interior_wall_l2": Sprite(
        pixels=_l2_interior_wall_pixels(),
        name="interior_wall_l2",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    ),
    "interior_wall_l3": Sprite(
        pixels=_l3_interior_wall_pixels(),
        name="interior_wall_l3",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    ),
    "obstacle_block": Sprite(
        pixels=[
            [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
            [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
            [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
            [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
        ],
        name="obstacle_block",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    ),
    "target_plain": Sprite(
        pixels=[
            [-1, -1, -1, -1],
            [-1,  0,  0, -1],
            [-1,  0,  0, -1],
            [-1, -1, -1, -1],
        ],
        name="target_plain",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target", "plain"],
        layer=1,
    ),
    "pawn_orange": Sprite(
        pixels=[
            [ORANGE, ORANGE, ORANGE, ORANGE],
            [ORANGE, 4, ORANGE, ORANGE],
            [ORANGE, ORANGE, 4, ORANGE],
            [ORANGE, ORANGE, ORANGE, ORANGE],
        ],
        name="pawn_orange",
        visible=True,
        collidable=True,
        tags=["pawn", "orange"],
        layer=3,
    ),
    "pawn_purple": Sprite(
        pixels=[
            [PURPLE, PURPLE, PURPLE, PURPLE],
            [PURPLE, 4, PURPLE, PURPLE],
            [PURPLE, PURPLE, 4, PURPLE],
            [PURPLE, PURPLE, PURPLE, PURPLE],
        ],
        name="pawn_purple",
        visible=True,
        collidable=True,
        tags=["pawn", "purple"],
        layer=3,
    ),
    "target_orange": Sprite(
        pixels=[
            [ORANGE, ORANGE, ORANGE, ORANGE],
            [ORANGE, 0, 0, ORANGE],
            [ORANGE, 0, 0, ORANGE],
            [ORANGE, ORANGE, ORANGE, ORANGE],
        ],
        name="target_orange",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target", "orange"],
        layer=1,
    ),
    "target_purple": Sprite(
        pixels=[
            [PURPLE, PURPLE, PURPLE, PURPLE],
            [PURPLE, 0, 0, PURPLE],
            [PURPLE, 0, 0, PURPLE],
            [PURPLE, PURPLE, PURPLE, PURPLE],
        ],
        name="target_purple",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target", "purple"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
def _at(cx: int, cy: int) -> tuple[int, int]:
    """Logical-cell origin in frame pixels."""
    return (cx * CELL, cy * CELL)


levels = [
    # ---- Level 1: tutorial — single pawn + single target on an open arena.
    Level(
        sprites=[
            sprites["frame_wall"].clone().set_position(0, 0),
            sprites["target_orange"].clone().set_position(*_at(11, 7)),
            sprites["pawn_orange"].clone().set_position(*_at(4, 7)),
        ],
        grid_size=(FRAME_W, FRAME_H),
        data={"step_budget": 30, "anti_anchor_range": 0},
    ),
    # ---- Level 2: corridor + south pocket, two pawns swap ends.
    Level(
        sprites=[
            sprites["frame_wall"].clone().set_position(0, 0),
            sprites["interior_wall_l2"].clone().set_position(*_at(1, 1)),
            sprites["target_purple"].clone().set_position(*_at(1, 7)),
            sprites["target_orange"].clone().set_position(*_at(14, 7)),
            sprites["pawn_orange"].clone().set_position(*_at(1, 7)),
            sprites["pawn_purple"].clone().set_position(*_at(14, 7)),
        ],
        grid_size=(FRAME_W, FRAME_H),
        data={"step_budget": 80, "anti_anchor_range": 0},
    ),
    # ---- Level 3: targets are unlockable (no sticking on land) and colour-agnostic. Targets
    # ---- sit immediately adjacent to the centre obstacle on different cardinal sides; the
    # ---- obstacle is load-bearing — the only way for a pawn pulled past target distance to
    # ---- stop on its target is to be blocked by the obstacle. Without the obstacle the
    # ---- player would need pixel-precise click counting; with it, anchor placements that
    # ---- pull pawns toward the obstacle naturally rectify them onto the targets.
    Level(
        sprites=[
            sprites["frame_wall"].clone().set_position(0, 0),
            sprites["target_plain"].clone().set_position(*_at(8, 2)),
            sprites["pawn_orange"].clone().set_position(*_at(8, 3)),
            sprites["target_plain"].clone().set_position(*_at(8, 9)),
            sprites["pawn_purple"].clone().set_position(*_at(8, 12)),
        ],
        grid_size=(FRAME_W, FRAME_H),
        data={"step_budget": 30, "targets_unlocked": True},
    ),
]


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    """Horizontal depleting bar painted on rows 60..63 of every frame."""

    def __init__(self, game: "Kn58") -> None:
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        budget = max(1, self.game.step_budget)
        remaining = max(0, self.game.step_budget - self.game.steps_taken)
        fraction = remaining / budget
        bar_width = math.ceil(FRAME_W * fraction)
        for x in range(FRAME_W):
            for y in range(HUD_ROW_Y, FRAME_H):
                frame[y, x] = HUD_BAR_COLOR if x < bar_width else HUD_BG_COLOR
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME
# ---------------------------------------------------------------------
class Kn58(NovaBaseGame):
    def __init__(self) -> None:
        self.step_budget = 30
        self.steps_taken = 0
        self.anchor_sprite: Sprite | None = None
        self.anti_anchor_sprite: Sprite | None = None
        self.anti_anchor_range = 0
        self.anti_anchor_strength = 1
        self.targets_unlocked = False
        self.stuck_pawns: set[int] = set()  # use sprite id() for hashable identity
        self._step_counter_ui = StepCounterHud(self)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        super().__init__(
            game_id="kn58",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    # ------- Per-level setup -------

    def on_set_level(self, level: Level) -> None:
        self.step_budget = int(level.get_data("step_budget") or 30)
        self.steps_taken = 0
        self.anchor_sprite = None
        self.stuck_pawns = set()
        self.anti_anchor_range = int(level.get_data("anti_anchor_range") or 0)
        self.anti_anchor_strength = int(level.get_data("anti_anchor_strength") or 1)
        self.targets_unlocked = bool(level.get_data("targets_unlocked"))
        anti_list = level.get_sprites_by_tag("anti_anchor")
        self.anti_anchor_sprite = anti_list[0] if anti_list else None
        self._check_matches()

    # ------- Step dispatch -------

    def step(self) -> None:
        if self.action.id != GameAction.ACTION6:
            self.complete_action()
            return

        click_x = int(self.action.data.get("x", -1))
        click_y = int(self.action.data.get("y", -1))
        grid_pos = self.camera.display_to_grid(click_x, click_y)
        if grid_pos is None:
            self.complete_action()
            return

        gx, gy = grid_pos
        # Snap to the logical-cell origin (multiples of CELL).
        cell_x = (gx // CELL) * CELL
        cell_y = (gy // CELL) * CELL

        # Reject clicks on the HUD strip.
        if cell_y >= HUD_ROW_Y:
            self.complete_action()
            return

        self._place_or_toggle_anchor(cell_x, cell_y)

        # Phase 1: anchor pull (if anchor present).
        if self.anchor_sprite is not None:
            self._do_pull_phase()

        # Phase 1.5: match check.
        self._check_matches()

        # Phase 2: anti-anchor repulsion.
        if self.anti_anchor_sprite is not None:
            self._do_repel_phase()

        # Phase 2.5: match check.
        self._check_matches()

        # Step counter / win / lose.
        self.steps_taken += 1

        if self._all_matched():
            self.complete_action()
            self.next_level()
            return

        if self.steps_taken >= self.step_budget:
            self.lose()

        self.complete_action()

    # ------- Anchor placement -------

    def _place_or_toggle_anchor(self, cell_x: int, cell_y: int) -> None:
        if self.anchor_sprite is not None:
            if self.anchor_sprite.x != cell_x or self.anchor_sprite.y != cell_y:
                self.anchor_sprite.set_position(cell_x, cell_y)
            return
        new_anchor = sprites["anchor"].clone().set_position(cell_x, cell_y)
        self.current_level.add_sprite(new_anchor)
        self.anchor_sprite = new_anchor

    # ------- Phase 1: pull -------

    def _do_pull_phase(self) -> None:
        ax = self.anchor_sprite.x
        ay = self.anchor_sprite.y
        moving, all_pawns = self._partition_pawns()
        desired: dict[int, tuple[int, int]] = {}
        for p in moving:
            desired[id(p)] = self._step_along(p, ax - p.x, ay - p.y)
        self._commit_moves(moving, all_pawns, desired)

    # ------- Phase 2: repel -------

    def _do_repel_phase(self) -> None:
        if self.anti_anchor_sprite is None or self.anti_anchor_range <= 0:
            return
        aax = self.anti_anchor_sprite.x
        aay = self.anti_anchor_sprite.y
        moving, _ = self._partition_pawns()
        # Determine which pawns enter the repel phase based on their *initial*
        # in-range status. Strength-N is implemented as N successive 1-cell
        # sub-ticks, with full simultaneous-conflict resolution between, and a
        # match-check between sub-ticks (so a pawn that lands on its target
        # mid-push sticks and is exempt from the remaining sub-ticks).
        target_ids = set()
        for p in moving:
            dx = p.x - aax
            dy = p.y - aay
            cell_dist = (abs(dx) + abs(dy)) // CELL
            if 0 < cell_dist <= self.anti_anchor_range:
                target_ids.add(id(p))
        for _ in range(max(1, self.anti_anchor_strength)):
            target_ids -= self.stuck_pawns
            if not target_ids:
                return
            self._do_repel_sub_tick(target_ids, aax, aay)
            self._check_matches()

    def _do_repel_sub_tick(self, target_ids: set[int], aax: int, aay: int) -> None:
        moving, all_pawns = self._partition_pawns()
        movers = [p for p in moving if id(p) in target_ids]
        if not movers:
            return
        desired: dict[int, tuple[int, int]] = {}
        for p in movers:
            dx = p.x - aax
            dy = p.y - aay
            if dx == 0 and dy == 0:
                desired[id(p)] = (p.x, p.y)
            else:
                desired[id(p)] = self._step_along(p, dx, dy)
        self._commit_moves(movers, all_pawns, desired)

    # ------- Manhattan-gradient single-step helper -------

    def _step_along(self, pawn: Sprite, dx_to: int, dy_to: int) -> tuple[int, int]:
        """One-cell step along the dominant axis; secondary-axis fallback if blocked.

        dx_to, dy_to are in frame pixels (positive sign = move toward).
        """
        if abs(dx_to) >= abs(dy_to):
            primary = (CELL * _sign(dx_to), 0)
            secondary = (0, CELL * _sign(dy_to))
        else:
            primary = (0, CELL * _sign(dy_to))
            secondary = (CELL * _sign(dx_to), 0)

        if primary != (0, 0):
            nx = pawn.x + primary[0]
            ny = pawn.y + primary[1]
            if self._cell_passable(nx, ny, exclude=pawn):
                return (nx, ny)
        if secondary != (0, 0):
            nx = pawn.x + secondary[0]
            ny = pawn.y + secondary[1]
            if self._cell_passable(nx, ny, exclude=pawn):
                return (nx, ny)
        return (pawn.x, pawn.y)

    def _cell_passable(self, x: int, y: int, exclude: Sprite | None) -> bool:
        """A cell is passable for a moving pawn if it has no wall and no stuck pawn.

        Moving pawns are NOT considered here — pawn-vs-pawn conflicts among
        movers are resolved in `_commit_moves` so that vacating-and-entering
        in the same tick is allowed.
        """
        if x < 0 or x + CELL > FRAME_W:
            return False
        if y < 0 or y + CELL > PLAYFIELD_H:
            return False
        # Walls.
        for wx in (x, x + CELL - 1):
            for wy in (y, y + CELL - 1):
                w = self.current_level.get_sprite_at(wx, wy, "wall")
                if w is not None:
                    return False
        # Stuck pawns block.
        for p in self.current_level.get_sprites_by_tag("pawn"):
            if id(p) in self.stuck_pawns and p is not exclude:
                if p.x == x and p.y == y:
                    return False
        return True

    # ------- Simultaneous-conflict resolution -------

    def _commit_moves(
        self,
        moving: list[Sprite],
        all_pawns: list[Sprite],
        desired: dict[int, tuple[int, int]],
    ) -> None:
        # Stuck pawns are static obstacles; their cells must never be a destination.
        static_positions = {(p.x, p.y) for p in all_pawns if id(p) in self.stuck_pawns}
        for p in moving:
            d = desired[id(p)]
            if d != (p.x, p.y) and d in static_positions:
                desired[id(p)] = (p.x, p.y)

        # Iterate to a fixpoint:
        # - a moving pawn whose destination is also another mover's destination → both stay.
        # - a moving pawn whose destination is occupied by another mover that is staying → stay.
        while True:
            changed = False

            dest_count: dict[tuple[int, int], int] = {}
            for p in moving:
                d = desired[id(p)]
                dest_count[d] = dest_count.get(d, 0) + 1
            for p in moving:
                d = desired[id(p)]
                if d != (p.x, p.y) and dest_count.get(d, 0) > 1:
                    desired[id(p)] = (p.x, p.y)
                    changed = True

            position_to_mover: dict[tuple[int, int], Sprite] = {(p.x, p.y): p for p in moving}
            for p in moving:
                d = desired[id(p)]
                if d == (p.x, p.y):
                    continue
                occupant = position_to_mover.get(d)
                if occupant is not None and occupant is not p:
                    if desired[id(occupant)] == (occupant.x, occupant.y):
                        desired[id(p)] = (p.x, p.y)
                        changed = True

            if not changed:
                break

        for p in moving:
            d = desired[id(p)]
            if d != (p.x, p.y):
                p.set_position(d[0], d[1])

    # ------- Match-check -------

    def _check_matches(self) -> None:
        # In targets_unlocked mode pawns never stick — the win check is a
        # transient "all on targets at this exact tick" predicate handled in
        # `_all_matched`. Skip the per-pawn sticking entirely.
        if self.targets_unlocked:
            return
        pawns = self.current_level.get_sprites_by_tag("pawn")
        targets = self.current_level.get_sprites_by_tag("target")
        for p in pawns:
            if id(p) in self.stuck_pawns:
                continue
            p_color = self._color_tag(p)
            for t in targets:
                if t.x == p.x and t.y == p.y and self._color_tag(t) == p_color:
                    self.stuck_pawns.add(id(p))
                    break

    def _all_matched(self) -> bool:
        pawns = self.current_level.get_sprites_by_tag("pawn")
        if not pawns:
            return False
        if self.targets_unlocked:
            target_positions = {
                (t.x, t.y) for t in self.current_level.get_sprites_by_tag("target")
            }
            return all((p.x, p.y) in target_positions for p in pawns)
        return all(id(p) in self.stuck_pawns for p in pawns)

    # ------- Bookkeeping -------

    def _partition_pawns(self) -> tuple[list[Sprite], list[Sprite]]:
        all_pawns = self.current_level.get_sprites_by_tag("pawn")
        moving = [p for p in all_pawns if id(p) not in self.stuck_pawns]
        return moving, all_pawns

    @staticmethod
    def _color_tag(sprite: Sprite) -> str | None:
        for tag in sprite.tags:
            if tag in ("orange", "purple"):
                return tag
        return None

    # ------- Standard hooks -------

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((4, 4), dtype=np.int16)
        out[0, 0] = max(0, self.step_budget - self.steps_taken)
        out[0, 1] = len(self.stuck_pawns)
        if self.anchor_sprite is not None:
            out[1, 0] = self.anchor_sprite.x
            out[1, 1] = self.anchor_sprite.y
        else:
            out[1, 0] = -1
            out[1, 1] = -1
        return out

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()


def _sign(n: int) -> int:
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0
