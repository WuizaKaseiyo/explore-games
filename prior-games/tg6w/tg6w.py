"""tg6w — a generated NovaPlay environment."""

import numpy as np
from novaengine import (
    NovaBaseGame,
    Camera,
    GameAction,
    Level,
    RenderableUserDisplay,
    Sprite,
)


# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------

# Every gameplay sprite is 3x3, placed on a 3-cell stride. Lattice
# index (i, j) maps to grid (3*i, 3*j); the lattice spans i, j in 0..6
# with the outer ring (lattice 0 and 6) reserved for boundary walls.

_WALL_SOLID_PIXELS = [
    [3, 3, 3],
    [3, 3, 3],
    [3, 3, 3],
]

_WALL_RIM_YELLOW_PIXELS = [
    [11, 11, 11],
    [11,  3, 11],
    [11, 11, 11],
]

_WALL_RIM_ORANGE_PIXELS = [
    [12, 12, 12],
    [12,  3, 12],
    [12, 12, 12],
]

_BLOCK_YELLOW_PIXELS = [
    [11, 11, 11],
    [11,  1, 11],
    [11, 11, 11],
]

_BLOCK_ORANGE_PIXELS = [
    [12, 12, 12],
    [12,  1, 12],
    [12, 12, 12],
]

_TARGET_YELLOW_PIXELS = [
    [11, 11, 11],
    [11, -1, 11],
    [11, 11, 11],
]

_TARGET_ORANGE_PIXELS = [
    [12, 12, 12],
    [12, -1, 12],
    [12, 12, 12],
]

# Red hazard wall: 5 rows x 2 cols. Left column is solid red; right column
# alternates red / dark-grey row-by-row, producing a serrated "zigzag"
# right edge. The dark-grey cells (palette 4) match the playfield
# background, so the recessed pixels read as bites taken out of the wall.
_WALL_HAZARD_PIXELS = [
    [8, 8],
    [8, 4],
    [8, 8],
    [8, 4],
    [8, 8],
]


sprites = {
    "wall_solid": Sprite(
        pixels=_WALL_SOLID_PIXELS,
        name="wall_solid",
        visible=True,
        collidable=True,
        tags=["wall", "wall_solid"],
        layer=1,
    ),
    "wall_rim_yellow": Sprite(
        pixels=_WALL_RIM_YELLOW_PIXELS,
        name="wall_rim_yellow",
        visible=True,
        collidable=True,
        tags=["wall", "wall_rim_yellow"],
        layer=1,
    ),
    "wall_rim_orange": Sprite(
        pixels=_WALL_RIM_ORANGE_PIXELS,
        name="wall_rim_orange",
        visible=True,
        collidable=True,
        tags=["wall", "wall_rim_orange"],
        layer=1,
    ),
    "block_yellow": Sprite(
        pixels=_BLOCK_YELLOW_PIXELS,
        name="block_yellow",
        visible=True,
        collidable=True,
        tags=["block", "block_yellow", "loose"],
        layer=3,
    ),
    "block_orange": Sprite(
        pixels=_BLOCK_ORANGE_PIXELS,
        name="block_orange",
        visible=True,
        collidable=True,
        tags=["block", "block_orange", "loose"],
        layer=3,
    ),
    "target_yellow": Sprite(
        pixels=_TARGET_YELLOW_PIXELS,
        name="target_yellow",
        visible=True,
        collidable=False,
        tags=["target", "target_yellow"],
        layer=0,
    ),
    "target_orange": Sprite(
        pixels=_TARGET_ORANGE_PIXELS,
        name="target_orange",
        visible=True,
        collidable=False,
        tags=["target", "target_orange"],
        layer=0,
    ),
    "wall_hazard": Sprite(
        pixels=_WALL_HAZARD_PIXELS,
        name="wall_hazard",
        visible=True,
        collidable=True,
        tags=["wall", "wall_hazard"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

# Lattice helpers (used only at level-build time).
def _pos(i: int, j: int) -> tuple[int, int]:
    return (3 * i, 3 * j)


def _place(name: str, i: int, j: int) -> Sprite:
    s = sprites[name].clone()
    x, y = _pos(i, j)
    s.set_position(x, y)
    return s


def _place_at(name: str, x: int, y: int) -> Sprite:
    """Place a sprite at exact base coords (used for thin walls that don't
    align to the 3-cell lattice)."""
    s = sprites[name].clone()
    s.set_position(x, y)
    return s


def _border_walls(n: int = 7) -> list[Sprite]:
    """Outer ring of `wall_solid` sprites for a lattice of size n x n
    (positions 0..n-1, with 0 and n-1 being the border rows/columns)."""
    cells: list[Sprite] = []
    seen: set[tuple[int, int]] = set()
    last = n - 1
    for i in range(n):
        for j in (0, last):
            if (i, j) not in seen:
                cells.append(_place("wall_solid", i, j))
                seen.add((i, j))
    for j in range(n):
        for i in (0, last):
            if (i, j) not in seen:
                cells.append(_place("wall_solid", i, j))
                seen.add((i, j))
    return cells


# ----- Level 1 -----
# Two yellow blocks at top-left and top-right interior; targets directly
# below at the bottom row. Single ACTION2 (DOWN) wins.
_l1_sprites = (
    _border_walls()
    + [
        _place("block_yellow", 1, 1),
        _place("block_yellow", 5, 1),
        _place("target_yellow", 1, 5),
        _place("target_yellow", 5, 5),
    ]
)


# ----- Level 2 -----
# Row-3 divider with one yellow-permeable cell at (3, 3) and one
# orange-permeable cell at (5, 3); other row-3 cells full-blocking.
# Stop-wall at (4, 5) lets the LEFT after DOWN nudge yellow alone.
_l2_sprites = (
    _border_walls()
    + [
        _place("wall_solid", 1, 3),
        _place("wall_solid", 2, 3),
        _place("wall_rim_yellow", 3, 3),
        _place("wall_solid", 4, 3),
        _place("wall_rim_orange", 5, 3),
        _place("wall_solid", 4, 5),
        _place("block_yellow", 3, 1),
        _place("block_orange", 5, 1),
        _place("target_yellow", 1, 5),
        _place("target_orange", 5, 5),
    ]
)


# ----- Level 3 -----
# Wider 9x9 lattice (27x27 base grid) to fit the full row-7 layout:
# yellow target (cols 9..11), 3-col grey wall (cols 12..14), 2-col red
# zigzag hazard wall (cols 15..16), 4-col empty gap (cols 17..20), and
# orange target (cols 21..23). Row 4 is the colour-permeable divider
# with yellow-rim at lattice (1, 4) and orange-rim at lattice (7, 4).
_l3_sprites = (
    _border_walls(9)
    + [
        _place("wall_rim_yellow", 1, 4),
        _place("wall_solid", 2, 4),
        _place("wall_solid", 3, 4),
        _place("wall_solid", 4, 4),
        _place("wall_solid", 5, 4),
        _place("wall_solid", 6, 4),
        _place("wall_rim_orange", 7, 4),
        # Row-7 obstacles between the two targets.
        _place("wall_solid", 4, 7),                 # 3-col grey wall at base (12, 21)
        _place_at("wall_hazard", 15, 19),           # 2-col x 5-row red zigzag
        # Blocks and targets.
        _place("block_yellow", 3, 1),
        _place("block_orange", 7, 1),
        _place("target_yellow", 3, 7),
        _place("target_orange", 7, 7),
    ]
)


levels = [
    Level(sprites=_l1_sprites, grid_size=(21, 21), data={"step_budget": 12}),
    Level(sprites=_l2_sprites, grid_size=(21, 21), data={"step_budget": 25}),
    Level(sprites=_l3_sprites, grid_size=(27, 27), data={"step_budget": 30}),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 4   # off-black backdrop
PADDING_COLOR = 4      # match bg

HUD_FILL = 11   # remaining-steps colour (yellow)
HUD_EMPTY = 4   # consumed-steps colour (matches bg)

LATTICE_STRIDE = 3

# Internal offset per cardinal-arrow press (in base-grid coords).
_DIR_DELTAS = {
    GameAction.ACTION1: (0, -LATTICE_STRIDE),
    GameAction.ACTION2: (0,  LATTICE_STRIDE),
    GameAction.ACTION3: (-LATTICE_STRIDE, 0),
    GameAction.ACTION4: ( LATTICE_STRIDE, 0),
}


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    """Horizontal bar at the top row of the frame; drains 1 cell per consumed action."""

    def __init__(self, max_steps: int = 0) -> None:
        self.max_steps = max_steps
        self.current = max_steps

    def reset(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current = max_steps

    def set_current(self, remaining: int) -> None:
        self.current = max(0, min(remaining, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        width = frame.shape[1]
        filled = int(round(width * self.current / self.max_steps))
        for x in range(width):
            frame[0, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------

class Tg6w(NovaBaseGame):
    def __init__(self) -> None:
        # Initialise per-level state BEFORE super().__init__() so that
        # the set_level(0) call inside NovaBaseGame.__init__ finds the
        # attributes already populated (avoids the post-super overwrite
        # bug seen in lv4k / xn5p).
        self._step_counter_ui = StepCounterHud(0)
        self._step_budget = 0
        self._steps_used = 0
        # Animation state: a list of frames; each frame is a list of
        # (block, new_x, new_y) tuples. When non-empty, step() pops one
        # frame per call without completing the action, until empty.
        self._anim_queue: list[list[tuple[Sprite, int, int]]] = []
        # Hazard event flag: set during slide simulation when any block's
        # destination cell is a `wall_hazard`. After the animation drains,
        # `step()` fires `lose()` instead of `_finalise_action()`.
        self._hazard_pending: bool = False
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        super().__init__(
            game_id="tg6w",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        self._step_budget = level.get_data("step_budget") or 30
        self._steps_used = 0
        self._step_counter_ui.reset(self._step_budget)
        self._anim_queue = []
        self._hazard_pending = False

    # ---- helpers ----------------------------------------------------

    def _wall_at(self, x: int, y: int) -> Sprite | None:
        for s in self.current_level.get_sprites_by_tag("wall"):
            if s.x == x and s.y == y:
                return s
        return None

    def _block_at(self, x: int, y: int) -> Sprite | None:
        for s in self.current_level.get_sprites_by_tag("block"):
            if s.x == x and s.y == y:
                return s
        return None

    @staticmethod
    def _block_can_pass(block: Sprite, wall: Sprite) -> bool:
        b_tags = getattr(block, "tags", []) or []
        w_tags = getattr(wall, "tags", []) or []
        if "wall_solid" in w_tags:
            return False
        if "wall_rim_yellow" in w_tags:
            return "block_yellow" in b_tags
        if "wall_rim_orange" in w_tags:
            return "block_orange" in b_tags
        return False

    def _block_colour(self, block: Sprite) -> str | None:
        b_tags = getattr(block, "tags", []) or []
        if "block_yellow" in b_tags:
            return "yellow"
        if "block_orange" in b_tags:
            return "orange"
        return None

    def _matching_target_cells(self, block: Sprite) -> set[tuple[int, int]]:
        """Return the set of grid coords occupied by same-coloured target
        sprites in the current level. Used by the slide simulator to snap a
        block to its target when it enters one."""
        colour = self._block_colour(block)
        if colour is None:
            return set()
        tag = f"target_{colour}"
        return {(t.x, t.y) for t in self.current_level.get_sprites_by_tag(tag)}

    @staticmethod
    def _bbox_overlap(ax: int, ay: int, aw: int, ah: int,
                      bx: int, by: int, bw: int, bh: int) -> bool:
        return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

    # ---- slide simulation ------------------------------------------

    def _compute_slide_animation(self, dx: int, dy: int) -> tuple[list[list[tuple[Sprite, int, int]]], bool]:
        """Simulate the slide tick-by-tick on a snapshot of block positions.

        Returns `(frames, hazard_triggered)`. Each frame is a list of
        `(block, new_x, new_y)` move tuples. `hazard_triggered` is True if
        any block's destination cell during the slide was a `wall_hazard`
        (the block enters the cell visually, then `lose()` fires once the
        animation drains).
        """
        STRIDE = LATTICE_STRIDE
        blocks = list(self.current_level.get_sprites_by_tag("block"))

        # Working state — we mutate copies, not the live sprites.
        block_pos: dict[int, tuple[int, int]] = {
            id(b): (b.x, b.y) for b in blocks
        }
        # Snapshot walls (positions are immutable for the duration of the slide).
        walls_at: dict[tuple[int, int], Sprite] = {
            (s.x, s.y): s for s in self.current_level.get_sprites_by_tag("wall")
        }
        # Hazard sprites — checked against the block's hypothetical bbox at
        # every 1-cell sub-step of the stride, so a block sliding past a
        # thin off-stride hazard dies even though its stride-aligned
        # destination cell wouldn't reveal the overlap.
        hazards = list(self.current_level.get_sprites_by_tag("wall_hazard"))
        # Per-block matching-colour target cells — sliding INTO one snaps
        # the block to that cell.
        target_cells: dict[int, set[tuple[int, int]]] = {
            id(b): self._matching_target_cells(b) for b in blocks
        }
        stopped: set[int] = set()
        hazard_triggered = False

        frames: list[list[tuple[Sprite, int, int]]] = []

        # Animation cap: at most ~20 ticks per slide (defensive bound).
        for _tick in range(64):
            # Order active blocks: those furthest in the slide direction go first.
            active = [b for b in blocks if id(b) not in stopped]
            if not active:
                break
            if dx > 0:
                active.sort(key=lambda b: -block_pos[id(b)][0])
            elif dx < 0:
                active.sort(key=lambda b: block_pos[id(b)][0])
            elif dy > 0:
                active.sort(key=lambda b: -block_pos[id(b)][1])
            else:
                active.sort(key=lambda b: block_pos[id(b)][1])

            tick_moves: list[tuple[Sprite, int, int]] = []
            for b in active:
                x, y = block_pos[id(b)]
                # Sub-step hazard scan: at each 1-cell offset along the
                # slide direction within this stride, check whether the
                # block's hypothetical 3x3 bbox overlaps any hazard sprite.
                # This catches off-stride hazards (zigzag walls between
                # lattice cells) that the stride-aligned destination check
                # would skip over.
                hazard_landing: tuple[int, int] | None = None
                for k in range(1, STRIDE + 1):
                    ix = x + dx * k
                    iy = y + dy * k
                    if any(
                        self._bbox_overlap(ix, iy, b.width, b.height,
                                           h.x, h.y, h.width, h.height)
                        for h in hazards
                    ):
                        hazard_landing = (ix, iy)
                        break
                if hazard_landing is not None:
                    block_pos[id(b)] = hazard_landing
                    tick_moves.append((b, hazard_landing[0], hazard_landing[1]))
                    stopped.add(id(b))
                    hazard_triggered = True
                    continue

                nx, ny = x + dx * STRIDE, y + dy * STRIDE
                # Border guard. Per-level grid bounds; max top-left for a
                # 3-wide / 3-tall sprite is grid_size - 3.
                gw, gh = self.current_level.grid_size or (64, 64)
                if nx < 0 or ny < 0 or nx > gw - 3 or ny > gh - 3:
                    stopped.add(id(b))
                    continue
                # Wall guard at stride-aligned destination.
                wall = walls_at.get((nx, ny))
                if wall is not None and not self._block_can_pass(b, wall):
                    stopped.add(id(b))
                    continue
                # Block-block collision.
                blocked_by_block = False
                for other in blocks:
                    if other is b:
                        continue
                    if block_pos[id(other)] == (nx, ny):
                        blocked_by_block = True
                        break
                if blocked_by_block:
                    stopped.add(id(b))
                    continue
                # Move.
                block_pos[id(b)] = (nx, ny)
                tick_moves.append((b, nx, ny))
                # Same-colour target snap: a block that enters its matching
                # target cell stops there (otherwise it would slide past,
                # since target sprites are non-collidable).
                if (nx, ny) in target_cells.get(id(b), set()):
                    stopped.add(id(b))

            if not tick_moves:
                break
            frames.append(tick_moves)

        return frames, hazard_triggered

    def _apply_frame(self, frame: list[tuple[Sprite, int, int]]) -> None:
        """Apply one animation frame to live sprites."""
        for block, nx, ny in frame:
            block.set_position(nx, ny)

    # ---- win / lose / dead-end ------------------------------------

    def _check_win(self) -> bool:
        blocks = self.current_level.get_sprites_by_tag("block")
        targets = self.current_level.get_sprites_by_tag("target")
        for block in blocks:
            colour = self._block_colour(block)
            if colour is None:
                return False
            tag = f"target_{colour}"
            on_target = False
            for t in targets:
                t_tags = getattr(t, "tags", []) or []
                if tag in t_tags and t.x == block.x and t.y == block.y:
                    on_target = True
                    break
            if not on_target:
                return False
        return True

    # ---- step entry -----------------------------------------------

    def _finalise_action(self) -> None:
        self._step_counter_ui.set_current(self._step_budget - self._steps_used)
        if self._check_win():
            self.complete_action()
            self.next_level()
            return
        if self._steps_used >= self._step_budget:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _resolve_after_animation(self) -> None:
        """Called once the animation queue drains. Fires lose() if a hazard
        was triggered during the slide; otherwise runs the standard
        win/budget finalisation."""
        self._steps_used += 1
        if self._hazard_pending:
            self._hazard_pending = False
            self._step_counter_ui.set_current(self._step_budget - self._steps_used)
            self.lose()
            self.complete_action()
            return
        self._finalise_action()

    def step(self) -> None:
        # Continuing an in-flight slide animation: advance one frame, render,
        # and return without complete_action so the engine re-renders the
        # next intermediate state on top of the same player action.
        if self._anim_queue:
            frame = self._anim_queue.pop(0)
            self._apply_frame(frame)
            if self._anim_queue:
                return
            self._resolve_after_animation()
            return

        # Fresh action: dispatch on action.id.
        delta = _DIR_DELTAS.get(self.action.id)
        if delta is None:
            # Unknown action — just complete (defensive).
            self.complete_action()
            return

        dx, dy = delta
        # Normalise to unit (-1, 0, 1) for the simulator's stride math.
        sdx = 0 if dx == 0 else (1 if dx > 0 else -1)
        sdy = 0 if dy == 0 else (1 if dy > 0 else -1)
        frames, hazard_triggered = self._compute_slide_animation(sdx, sdy)
        self._hazard_pending = hazard_triggered

        if not frames:
            # No block could move (e.g. UP at row 1 with top border). The
            # action is consumed and the step counter still ticks.
            self._resolve_after_animation()
            return

        # Play the first frame this engine tick; queue the rest for
        # subsequent step() calls within the same player action.
        self._anim_queue = list(frames)
        first = self._anim_queue.pop(0)
        self._apply_frame(first)
        if self._anim_queue:
            # More frames to play.
            return
        # Single-frame slide — resolve here.
        self._resolve_after_animation()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._step_counter_ui.current
        state[0, 1] = self._step_budget
        state[0, 2] = self._steps_used
        state[0, 3] = 1 if self._hazard_pending else 0
        return state
