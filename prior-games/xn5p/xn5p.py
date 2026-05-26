"""xn5p — a generated NovaPlay environment."""

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
# 1. SPRITE BANK
# ---------------------------------------------------------------------

# Every gameplay sprite is 3x3, placed on a 3-cell stride. Lattice
# index (i, j) maps to grid (1 + 3*i, 1 + 3*j); the lattice spans
# i, j in 0..5, with the outer 1-cell rim of the 20x20 grid reserved
# for boundary walls.

_AVATAR_PIXELS = [
    [11, 11, 11],
    [11,  4, 11],
    [11, 11, 11],
]

_RED_PIXELS = [
    [8, 8, 8],
    [8, 0, 8],
    [8, 8, 8],
]

_BLUE_PIXELS = [
    [0, 9, 0],
    [9, 9, 9],
    [0, 9, 0],
]

_GREEN_PIXELS = [
    [14,  0, 14],
    [ 0, 14,  0],
    [14,  0, 14],
]

_WALL_STATIC_PIXELS = [
    [3, 3, 3],
    [3, 3, 3],
    [3, 3, 3],
]

_WALL_STAMP_PIXELS = [
    [4, 4, 4],
    [4, 3, 4],
    [4, 4, 4],
]


sprites = {
    "avatar": Sprite(
        pixels=_AVATAR_PIXELS,
        name="avatar",
        visible=True,
        collidable=False,
        tags=["avatar"],
        layer=3,
    ),
    "molecule_red": Sprite(
        pixels=_RED_PIXELS,
        name="molecule_red",
        visible=True,
        collidable=True,
        tags=["molecule", "molecule_red"],
        layer=2,
    ),
    "molecule_blue": Sprite(
        pixels=_BLUE_PIXELS,
        name="molecule_blue",
        visible=True,
        collidable=True,
        tags=["molecule", "molecule_blue"],
        layer=2,
    ),
    "molecule_green": Sprite(
        pixels=_GREEN_PIXELS,
        name="molecule_green",
        visible=True,
        collidable=True,
        tags=["molecule", "molecule_green"],
        layer=2,
    ),
    "wall_static": Sprite(
        pixels=_WALL_STATIC_PIXELS,
        name="wall_static",
        visible=True,
        collidable=True,
        tags=["wall", "wall_static"],
        layer=1,
    ),
    "wall_stamp": Sprite(
        pixels=_WALL_STAMP_PIXELS,
        name="wall_stamp",
        visible=True,
        collidable=True,
        tags=["wall", "wall_stamp"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

# Lattice helpers (used only at level-build time).
def _pos(i: int, j: int) -> tuple[int, int]:
    return (1 + 3 * i, 1 + 3 * j)


def _make_boundary_walls() -> list[Sprite]:
    """Outer rim of the 20x20 grid: 1-cell-thick wall band on all sides.
    The inner playable area is the 18x18 region [1..18, 1..18]."""
    cells: list[Sprite] = []
    # Top and bottom rows.
    for x in range(0, 20):
        cells.append(_one_pixel_wall(x, 0))
        cells.append(_one_pixel_wall(x, 19))
    # Left and right columns (excluding corners already placed).
    for y in range(1, 19):
        cells.append(_one_pixel_wall(0, y))
        cells.append(_one_pixel_wall(19, y))
    return cells


def _one_pixel_wall(x: int, y: int) -> Sprite:
    s = Sprite(
        pixels=[[3]],
        name="wall_rim",
        visible=True,
        collidable=True,
        tags=["wall", "wall_rim"],
        layer=1,
    )
    s.set_position(x, y)
    return s


def _static(i: int, j: int) -> Sprite:
    s = sprites["wall_static"].clone()
    x, y = _pos(i, j)
    s.set_position(x, y)
    return s


def _avatar(i: int, j: int) -> Sprite:
    s = sprites["avatar"].clone()
    x, y = _pos(i, j)
    s.set_position(x, y)
    return s


def _mol(name: str, i: int, j: int) -> Sprite:
    s = sprites[name].clone()
    x, y = _pos(i, j)
    s.set_position(x, y)
    return s


# ----- Level 1 -----
# Static walls in column i=2 except at row j=2 (the only channel between
# left half and right half). Avatar starts in the right half away from
# the channel so that a single stamp at the start cell does not win.
_l1_walls = [_static(2, j) for j in (0, 1, 3, 4, 5)]
_l1_sprites = (
    _make_boundary_walls()
    + _l1_walls
    + [
        _mol("molecule_red", 0, 2),
        _mol("molecule_blue", 5, 2),
        _avatar(5, 0),
    ]
)

# ----- Level 2 -----
# Two channels (col i=2 and i=3) at row j=2; obstacle red at (3, 2).
_l2_walls = (
    [_static(2, j) for j in (0, 1, 3, 4, 5)]
    + [_static(3, j) for j in (0, 1, 3, 4, 5)]
)
_l2_sprites = (
    _make_boundary_walls()
    + _l2_walls
    + [
        _mol("molecule_red", 0, 0),       # main red
        _mol("molecule_blue", 5, 5),      # main blue
        _mol("molecule_red", 3, 2),       # obstacle red (channel)
        _avatar(5, 0),
    ]
)

# ----- Level 3 -----
# Same two-channel topology + a vertical "alcove" at column i=3, rows 3..5
# accessible only via the channel at (3, 2). Green lives in the alcove.
_l3_walls = (
    [_static(2, j) for j in (0, 1, 3, 4, 5)]
    + [_static(3, j) for j in (0, 1)]      # col 3 closed top
    + [_static(4, j) for j in (3, 4, 5)]   # col 4 closed bottom (alcove ceiling)
)
_l3_sprites = (
    _make_boundary_walls()
    + _l3_walls
    + [
        _mol("molecule_red", 0, 0),
        _mol("molecule_blue", 5, 5),
        _mol("molecule_green", 3, 4),
        _mol("molecule_red", 3, 2),       # obstacle red
        _avatar(5, 0),
    ]
)


levels = [
    Level(sprites=_l1_sprites, grid_size=(20, 20), data={"step_budget": 30}),
    Level(sprites=_l2_sprites, grid_size=(20, 20), data={"step_budget": 60}),
    Level(
        sprites=_l3_sprites,
        grid_size=(20, 20),
        data={"step_budget": 100, "stamp_toggle": True},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 1
PADDING_COLOR = 2

HUD_FILL = 11   # remaining-steps colour (yellow)
HUD_EMPTY = 3   # consumed-steps colour (grey)

# Background-paint colour per molecule colour. Each painted lattice cell
# gets a 3x3 sprite of this palette index laid below the molecule sprite,
# rendering as a coloured backdrop that signals "this region is sealed
# with one colour".
PAINT_COLOR = {
    "red": 7,         # pink
    "blue": 10,       # light-blue
    "green": 14,      # green (molecule_green's white cross stays legible)
}

# How many lattice cells to paint per render tick during the reveal
# animation. With 11-15 cells per region typical, this finishes in
# 5-8 internal frames; the engine re-renders each step so the reveal
# feels like a wash, not a snap.
PAINT_CELLS_PER_TICK = 2


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    """Horizontal bar at the bottom row of the frame."""

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
            frame[frame.shape[0] - 1, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------

class Xn5p(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_ui = StepCounterHud(0)
        # Initialise per-level state BEFORE super().__init__() so the
        # set_level(0) call inside the parent constructor finds the
        # attributes already present (otherwise post-super assignment
        # would overwrite the on_set_level-populated values).
        self._step_budget = 0
        self._stamp_toggle_allowed = False
        self._paint_phase = -1
        self._paint_queue: list[tuple[tuple[int, int], str]] = []
        self._painted_cells: dict[tuple[int, int], str] = {}
        self._paint_sprites: dict[tuple[int, int], Sprite] = {}
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        super().__init__(
            game_id="xn5p",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        self._step_budget = level.get_data("step_budget") or 30
        self._step_counter_ui.reset(self._step_budget)
        self._stamp_toggle_allowed = bool(level.get_data("stamp_toggle"))
        # Painting state belongs to the current level only; new level
        # starts with an empty palette regardless of prior progression.
        self._paint_phase = -1
        self._paint_queue = []
        self._painted_cells = {}
        self._paint_sprites = {}

    # ---- helpers ----------------------------------------------------

    @staticmethod
    def _action_delta(aid) -> tuple[int, int]:
        if aid == GameAction.ACTION1:
            return 0, -3
        if aid == GameAction.ACTION2:
            return 0, 3
        if aid == GameAction.ACTION3:
            return -3, 0
        if aid == GameAction.ACTION4:
            return 3, 0
        return 0, 0

    def _avatar_sprite(self) -> Sprite | None:
        avatars = self.current_level.get_sprites_by_tag("avatar")
        return avatars[0] if avatars else None

    def _sprite_at_lattice(
        self, x: int, y: int, *, tags: tuple[str, ...] | None = None
    ) -> Sprite | None:
        """Return the first sprite whose top-left equals (x, y), optionally
        filtered by any of the supplied tags."""
        for s in self.current_level.get_sprites():
            if s.x != x or s.y != y:
                continue
            if tags is not None:
                s_tags = getattr(s, "tags", []) or []
                if not any(t in s_tags for t in tags):
                    continue
            return s
        return None

    @staticmethod
    def _within_inner(x: int, y: int) -> bool:
        # Inner playable area excludes the 1-cell rim. A 3x3 sprite
        # placed at top-left (x, y) requires 1 <= x <= 16, 1 <= y <= 16.
        return 1 <= x <= 16 and 1 <= y <= 16

    def _try_walk(self, dx: int, dy: int) -> None:
        avatar = self._avatar_sprite()
        if avatar is None:
            return
        nx, ny = avatar.x + dx, avatar.y + dy
        if not self._within_inner(nx, ny):
            return
        # If destination has a wall, reject.
        if self._sprite_at_lattice(nx, ny, tags=("wall",)) is not None:
            return
        # If destination has a molecule, attempt push.
        molecule = self._sprite_at_lattice(nx, ny, tags=("molecule",))
        if molecule is not None:
            mx, my = nx + dx, ny + dy
            if not self._within_inner(mx, my):
                return
            if self._sprite_at_lattice(mx, my, tags=("wall",)) is not None:
                return
            if self._sprite_at_lattice(mx, my, tags=("molecule",)) is not None:
                return
            molecule.set_position(mx, my)
        avatar.set_position(nx, ny)

    def _try_stamp(self) -> None:
        avatar = self._avatar_sprite()
        if avatar is None:
            return
        existing_stamp = self._sprite_at_lattice(
            avatar.x, avatar.y, tags=("wall_stamp",)
        )
        if existing_stamp is not None:
            if self._stamp_toggle_allowed:
                self.current_level.remove_sprite(existing_stamp)
            return
        # No stamp yet: create one at the avatar's cell.
        stamp = sprites["wall_stamp"].clone()
        stamp.set_position(avatar.x, avatar.y)
        self.current_level.add_sprite(stamp)

    # ---- partition + painting --------------------------------------

    def _compute_components(self) -> list[tuple[set[tuple[int, int]], str | None]]:
        """Return a list of (cells, colour-label) pairs for every connected
        component of open lattice cells. The colour-label is the molecule
        colour if exactly one is present, "mixed" if multiple, or None if
        the component has no molecules."""
        is_wall: dict[tuple[int, int], bool] = {}
        molecule_at: dict[tuple[int, int], str] = {}
        for s in self.current_level.get_sprites():
            tags = getattr(s, "tags", []) or []
            if "wall_rim" in tags:
                continue
            x, y = s.x, s.y
            if x < 1 or y < 1 or (x - 1) % 3 != 0 or (y - 1) % 3 != 0:
                continue
            i, j = (x - 1) // 3, (y - 1) // 3
            if not (0 <= i <= 5 and 0 <= j <= 5):
                continue
            if "wall" in tags:
                is_wall[(i, j)] = True
            elif "molecule_red" in tags:
                molecule_at[(i, j)] = "red"
            elif "molecule_blue" in tags:
                molecule_at[(i, j)] = "blue"
            elif "molecule_green" in tags:
                molecule_at[(i, j)] = "green"

        components: list[tuple[set[tuple[int, int]], str | None]] = []
        visited: set[tuple[int, int]] = set()
        for i0 in range(6):
            for j0 in range(6):
                start = (i0, j0)
                if start in visited or is_wall.get(start, False):
                    continue
                cells: set[tuple[int, int]] = set()
                colours: set[str] = set()
                stack = [start]
                while stack:
                    cell = stack.pop()
                    if cell in visited or is_wall.get(cell, False):
                        continue
                    visited.add(cell)
                    cells.add(cell)
                    if cell in molecule_at:
                        colours.add(molecule_at[cell])
                    ci, cj = cell
                    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ni, nj = ci + di, cj + dj
                        if 0 <= ni <= 5 and 0 <= nj <= 5:
                            stack.append((ni, nj))
                if len(colours) == 0:
                    label: str | None = None
                elif len(colours) == 1:
                    label = next(iter(colours))
                else:
                    label = "mixed"
                components.append((cells, label))
        return components

    def _check_win(self) -> bool:
        components = self._compute_components()
        any_molecule = False
        for _cells, label in components:
            if label is None:
                continue
            if label == "mixed":
                return False
            any_molecule = True
        return any_molecule

    def _avatar_lattice_cell(self) -> tuple[int, int] | None:
        avatar = self._avatar_sprite()
        if avatar is None:
            return None
        x, y = avatar.x, avatar.y
        if x < 1 or y < 1:
            return None
        if (x - 1) % 3 != 0 or (y - 1) % 3 != 0:
            return None
        i, j = (x - 1) // 3, (y - 1) // 3
        if not (0 <= i <= 5 and 0 <= j <= 5):
            return None
        return i, j

    def _avatar_in_painted_region(self) -> bool:
        cell = self._avatar_lattice_cell()
        return cell is not None and cell in self._painted_cells

    def _add_paint(self, cell: tuple[int, int], colour: str) -> None:
        i, j = cell
        x, y = 1 + 3 * i, 1 + 3 * j
        c = PAINT_COLOR[colour]
        sprite = Sprite(
            pixels=[[c, c, c], [c, c, c], [c, c, c]],
            name=f"paint_{colour}_{i}_{j}",
            visible=True,
            collidable=False,
            interaction=InteractionMode.INTANGIBLE,
            tags=["paint", f"paint_{colour}"],
            layer=0,
        )
        sprite.set_position(x, y)
        self.current_level.add_sprite(sprite)
        self._paint_sprites[cell] = sprite
        self._painted_cells[cell] = colour

    def _remove_paint(self, cell: tuple[int, int]) -> None:
        sprite = self._paint_sprites.pop(cell, None)
        if sprite is not None:
            self.current_level.remove_sprite(sprite)
        self._painted_cells.pop(cell, None)

    def _update_painting(self) -> None:
        """Reconcile the painted-cell set against the current component
        decomposition. Newly-monochromatic cells are queued for animated
        reveal; cells that have lost their monochromatic component
        (e.g. after an L3 toggle reconnects regions) lose paint instantly."""
        components = self._compute_components()
        desired: dict[tuple[int, int], str] = {}
        for cells, label in components:
            if label is None or label == "mixed":
                continue
            for cell in cells:
                desired[cell] = label

        # Remove paint from cells whose component no longer has the right
        # monochromatic label (immediate, no animation).
        for cell, colour in list(self._painted_cells.items()):
            if desired.get(cell) != colour:
                self._remove_paint(cell)

        # Queue paint reveals for newly-eligible cells.
        to_paint = sorted(
            (cell, colour) for cell, colour in desired.items()
            if cell not in self._painted_cells
        )
        if to_paint:
            self._paint_queue = to_paint
            if self._paint_phase < 0:
                self._paint_phase = 0

    # ---- step -------------------------------------------------------

    def _finalise_action(self) -> None:
        won = self._check_win()
        remaining = self._step_budget - self._action_count - 1
        self._step_counter_ui.set_current(remaining)
        if won:
            self.complete_action()
            self.next_level()
            return
        # Submerge-lose: avatar sits inside a painted (sealed) region but
        # the global predicate is still false. At L1/L2 stamps are
        # permanent so the avatar is genuinely trapped — no point
        # waiting for the budget to drain. At L3 the avatar can still
        # toggle a stamp on the painted region's boundary, so recovery
        # remains possible there.
        if (not self._stamp_toggle_allowed
                and self._avatar_in_painted_region()):
            self.lose()
            self.complete_action()
            return
        if remaining <= 0:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _advance_paint(self) -> None:
        for _ in range(PAINT_CELLS_PER_TICK):
            if not self._paint_queue:
                break
            cell, colour = self._paint_queue.pop(0)
            self._add_paint(cell, colour)
        if not self._paint_queue:
            self._paint_phase = -1
            self._finalise_action()
        else:
            self._paint_phase += 1

    def step(self) -> None:
        # Mid-animation render: advance the paint reveal one tick and
        # return WITHOUT calling complete_action, so the engine paints
        # the next intermediate frame on top of the same player action.
        if self._paint_phase >= 0:
            self._advance_paint()
            return

        if self.action.id == GameAction.ACTION5:
            self._try_stamp()
        else:
            dx, dy = self._action_delta(self.action.id)
            if dx != 0 or dy != 0:
                self._try_walk(dx, dy)

        # Reconcile paint state with the new component layout. If new
        # cells are queued for reveal, the animation takes over and
        # _finalise_action runs only when the queue is drained.
        self._update_painting()
        if self._paint_phase >= 0:
            return

        self._finalise_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._step_counter_ui.current
        state[0, 1] = 1 if self._stamp_toggle_allowed else 0
        avatar = self._avatar_sprite()
        if avatar is not None:
            state[1, 0] = avatar.x
            state[1, 1] = avatar.y
        return state
