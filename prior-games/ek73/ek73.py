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
# 1. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 2  # light-grey playfield
PADDING_COLOR = 4  # off-black letter-box (matches walls so border merges)
CELL_STRIDE = 4  # 4 pixels per logical cell; 16x16 logical grid on a 64x64 frame
GRID_LOGICAL = 16  # 16 logical cells per side
K_DECAY = 3  # wake decays after K turns


# ---------------------------------------------------------------------
# 2. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "player": Sprite(
        pixels=[
            [-1, 11,  4, -1],
            [11, 11, 11, 11],
            [-1, 11, -1, -1],
            [-1, 11, -1, -1],
        ],
        name="player",
        visible=True,
        collidable=True,
        tags=["player"],
        layer=5,
    ),
    "collectible": Sprite(
        pixels=[
            [-1, 12, -1, -1],
            [12,  1, 12, -1],
            [-1, 12, -1, -1],
            [-1, -1, -1, -1],
        ],
        name="collectible",
        visible=True,
        collidable=True,
        tags=["collectible"],
        layer=2,
    ),
    "wall": Sprite(
        pixels=[
            [4, 4, 5, 5],
            [4, 4, 5, 5],
            [5, 5, 4, 4],
            [5, 5, 4, 4],
        ],
        name="wall",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    ),
    "wake_age1": Sprite(
        pixels=[
            [6, 6, 6, 6],
            [6, 1, 1, 6],
            [6, 1, 1, 6],
            [6, 6, 6, 6],
        ],
        name="wake_age1",
        visible=True,
        collidable=True,
        tags=["wake"],
        layer=1,
    ),
    "wake_age2": Sprite(
        pixels=[
            [ 6,  6,  6,  6],
            [ 6, -1, -1,  6],
            [ 6, -1, -1,  6],
            [ 6,  6,  6,  6],
        ],
        name="wake_age2",
        visible=True,
        collidable=True,
        tags=["wake"],
        layer=1,
    ),
    "wake_age3": Sprite(
        pixels=[
            [ 6, -1, -1,  6],
            [-1, -1, -1, -1],
            [-1, -1, -1, -1],
            [ 6, -1, -1,  6],
        ],
        name="wake_age3",
        visible=True,
        collidable=True,
        tags=["wake"],
        layer=1,
    ),
    "clearer_pad": Sprite(
        pixels=[
            [14, -1, 14, -1],
            [-1,  0, -1, 14],
            [14, -1,  0, -1],
            [-1, 14, -1, 14],
        ],
        name="clearer_pad",
        visible=True,
        collidable=True,
        tags=["clearer"],
        layer=1,
    ),
    "warp_pad_a": Sprite(
        pixels=[
            [10, 10, 10, 10],
            [10,  9,  9, 10],
            [10,  9,  9, 10],
            [10, 10, 10, 10],
        ],
        name="warp_pad_a",
        visible=True,
        collidable=True,
        tags=["warp"],
        layer=1,
    ),
    "warp_pad_b": Sprite(
        pixels=[
            [10, 10, 10, 10],
            [10,  9,  9, 10],
            [10,  9,  9, 10],
            [10, 10, 10, 10],
        ],
        name="warp_pad_b",
        visible=True,
        collidable=True,
        tags=["warp"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 3. WALKABLE-CELL HELPERS (logical coordinates)
# ---------------------------------------------------------------------

def _to_pixel(lx: int, ly: int) -> tuple[int, int]:
    return (lx * CELL_STRIDE, ly * CELL_STRIDE)


def _l1_walkable() -> set[tuple[int, int]]:
    """Level 1: T-shape with 2-wide horizontal arm + 1-wide vertical arm.

    Horizontal arm: rows 3-4, columns 1-14 (28 cells).
    Vertical arm: column 3, rows 5-13 (9 cells).
    """
    cells: set[tuple[int, int]] = set()
    for c in range(1, 15):
        cells.add((c, 3))
        cells.add((c, 4))
    for r in range(5, 14):
        cells.add((3, r))
    return cells


def _l2_walkable() -> set[tuple[int, int]]:
    """Level 2: 2-wide horizontal corridor + 1-wide branch.

    Horizontal: rows 7-8, columns 1-14.
    Branch: column 8, rows 5-6.
    West row-5 stub: row 5, columns 2-8 (so collectible at (2, 5) reachable
    via the branch then west along row 5).
    """
    cells: set[tuple[int, int]] = set()
    for c in range(1, 15):
        cells.add((c, 7))
        cells.add((c, 8))
    for r in range(5, 7):
        cells.add((8, r))
    for c in range(2, 9):
        cells.add((c, 5))
    return cells


def _l3_walkable() -> set[tuple[int, int]]:
    """Level 3: T-junction with horizontal corridor + vertical branch + warp side-pads.

    Horizontal: row 8, columns 1-14.
    Vertical branch: column 8, rows 1-7.
    Warp-side pads: cells (1, 9) and (14, 9).
    """
    cells: set[tuple[int, int]] = set()
    for c in range(1, 15):
        cells.add((c, 8))
    for r in range(1, 8):
        cells.add((8, r))
    cells.add((1, 9))
    cells.add((14, 9))
    return cells


def _build_walls(walkable: set[tuple[int, int]]) -> list[Sprite]:
    """Place a wall sprite at every non-walkable cell in the 16x16 logical grid."""
    walls: list[Sprite] = []
    for c in range(GRID_LOGICAL):
        for r in range(GRID_LOGICAL):
            if (c, r) in walkable:
                continue
            wall = sprites["wall"].clone()
            wall.set_position(*_to_pixel(c, r))
            walls.append(wall)
    return walls


# ---------------------------------------------------------------------
# 4. LEVELS
# ---------------------------------------------------------------------

def _build_level_1() -> Level:
    walkable = _l1_walkable()
    placed: list[Sprite] = []
    placed.extend(_build_walls(walkable))
    # avatar at (3, 3)
    p = sprites["player"].clone()
    p.set_position(*_to_pixel(3, 3))
    placed.append(p)
    # collectibles at (12, 3) and (3, 13)
    c1 = sprites["collectible"].clone()
    c1.set_position(*_to_pixel(12, 3))
    placed.append(c1)
    c2 = sprites["collectible"].clone()
    c2.set_position(*_to_pixel(3, 13))
    placed.append(c2)
    return Level(
        sprites=placed,
        grid_size=(64, 64),
        data={"step_budget": 60, "level_num": 1},
    )


def _build_level_2() -> Level:
    walkable = _l2_walkable()
    placed: list[Sprite] = []
    placed.extend(_build_walls(walkable))
    # avatar at (2, 8)
    p = sprites["player"].clone()
    p.set_position(*_to_pixel(2, 8))
    placed.append(p)
    # clearer at (8, 5)
    cp = sprites["clearer_pad"].clone()
    cp.set_position(*_to_pixel(8, 5))
    placed.append(cp)
    # collectibles at (14, 8) and (2, 5)
    c1 = sprites["collectible"].clone()
    c1.set_position(*_to_pixel(14, 8))
    placed.append(c1)
    c2 = sprites["collectible"].clone()
    c2.set_position(*_to_pixel(2, 5))
    placed.append(c2)
    return Level(
        sprites=placed,
        grid_size=(64, 64),
        data={"step_budget": 50, "level_num": 2},
    )


def _build_level_3() -> Level:
    walkable = _l3_walkable()
    placed: list[Sprite] = []
    placed.extend(_build_walls(walkable))
    # avatar at (8, 8)
    p = sprites["player"].clone()
    p.set_position(*_to_pixel(8, 8))
    placed.append(p)
    # clearer at (8, 1) — co-located with collectible at (8, 1)
    cp = sprites["clearer_pad"].clone()
    cp.set_position(*_to_pixel(8, 1))
    placed.append(cp)
    # collectibles at (8, 1), (1, 8), (14, 8)
    for cellx, celly in [(8, 1), (1, 8), (14, 8)]:
        c = sprites["collectible"].clone()
        c.set_position(*_to_pixel(cellx, celly))
        placed.append(c)
    # warp pad pair: A at (1, 9), B at (14, 9)
    wa = sprites["warp_pad_a"].clone()
    wa.set_position(*_to_pixel(1, 9))
    placed.append(wa)
    wb = sprites["warp_pad_b"].clone()
    wb.set_position(*_to_pixel(14, 9))
    placed.append(wb)
    return Level(
        sprites=placed,
        grid_size=(64, 64),
        data={"step_budget": 80, "level_num": 3},
    )


levels = [_build_level_1(), _build_level_2(), _build_level_3()]


# ---------------------------------------------------------------------
# 5. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    """A horizontal bar at row 63: depleting from left to right as steps consumed."""

    def __init__(self) -> None:
        self.max_steps = 0
        self.current_steps = 0

    def reset(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_current(self, current: int) -> None:
        self.current_steps = max(0, min(current, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.current_steps / self.max_steps
        fill = int(round(64 * ratio))
        for x in range(64):
            frame[63, x] = 5 if x < fill else 2
        return frame


# ---------------------------------------------------------------------
# 6. THE GAME
# ---------------------------------------------------------------------

def _walkable_set_for(level_num: int) -> set[tuple[int, int]]:
    if level_num == 1:
        return _l1_walkable()
    if level_num == 2:
        return _l2_walkable()
    return _l3_walkable()


_WAKE_AGE_NAMES = {1: "wake_age1", 2: "wake_age2", 3: "wake_age3"}


class Ek73(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_ui = StepCounterHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        # Per-level state (initialised in on_set_level)
        self._walkable: set[tuple[int, int]] = set()
        self._wake: dict[tuple[int, int], int] = {}
        self._wake_sprites: dict[tuple[int, int], Sprite] = {}
        self._step_budget = 0
        super().__init__(
            game_id="ek73",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    # -- setup ----------------------------------------------------------
    def on_set_level(self, level: Level) -> None:
        level_num = level.get_data("level_num") or 1
        self._walkable = _walkable_set_for(level_num)
        self._wake = {}
        self._wake_sprites = {}
        self._step_budget = level.get_data("step_budget") or 60
        self._step_counter_ui.reset(self._step_budget)

    # -- helpers --------------------------------------------------------
    def _player(self) -> Sprite:
        return self.current_level.get_sprites_by_tag("player")[0]

    def _player_cell(self) -> tuple[int, int]:
        p = self._player()
        return (p.x // CELL_STRIDE, p.y // CELL_STRIDE)

    def _is_walkable(self, lx: int, ly: int) -> bool:
        if lx < 0 or lx >= GRID_LOGICAL or ly < 0 or ly >= GRID_LOGICAL:
            return False
        return (lx, ly) in self._walkable

    def _wake_at(self, lx: int, ly: int) -> bool:
        return (lx, ly) in self._wake

    def _direction_for(self, action_id: int) -> tuple[int, int]:
        if action_id == GameAction.ACTION1.value:
            return (0, -1)
        if action_id == GameAction.ACTION2.value:
            return (0, 1)
        if action_id == GameAction.ACTION3.value:
            return (-1, 0)
        if action_id == GameAction.ACTION4.value:
            return (1, 0)
        return (0, 0)

    # -- pad effects ----------------------------------------------------
    def _trigger_pad_at(self, lx: int, ly: int) -> tuple[int, int] | None:
        """Apply pad effects at the given cell. Returns the (possibly teleported)
        new player cell — or None if no teleport happened.
        """
        # Clearer pad: wipe all wake.
        for sprite in self.current_level.get_sprites_by_tag("clearer"):
            if sprite.interaction == InteractionMode.REMOVED:
                continue
            if (sprite.x // CELL_STRIDE, sprite.y // CELL_STRIDE) == (lx, ly):
                self._clear_all_wake()
                sprite.set_interaction(InteractionMode.REMOVED)
                break
        # Collectible: consume.
        for sprite in self.current_level.get_sprites_by_tag("collectible"):
            if sprite.interaction == InteractionMode.REMOVED:
                continue
            if (sprite.x // CELL_STRIDE, sprite.y // CELL_STRIDE) == (lx, ly):
                sprite.set_interaction(InteractionMode.REMOVED)
                break
        # Warp pad: teleport to the paired pad's position. Both pads consumed.
        for sprite in self.current_level.get_sprites_by_tag("warp"):
            if sprite.interaction == InteractionMode.REMOVED:
                continue
            if (sprite.x // CELL_STRIDE, sprite.y // CELL_STRIDE) == (lx, ly):
                # Find the partner (the OTHER warp pad still tangible).
                partner = None
                for other in self.current_level.get_sprites_by_tag("warp"):
                    if other is sprite or other.interaction == InteractionMode.REMOVED:
                        continue
                    partner = other
                    break
                if partner is None:
                    return None
                tx, ty = (partner.x // CELL_STRIDE, partner.y // CELL_STRIDE)
                self._player().set_position(*_to_pixel(tx, ty))
                sprite.set_interaction(InteractionMode.REMOVED)
                partner.set_interaction(InteractionMode.REMOVED)
                # Consume any collectible at the destination too (rare but possible).
                for c in self.current_level.get_sprites_by_tag("collectible"):
                    if c.interaction == InteractionMode.REMOVED:
                        continue
                    if (c.x // CELL_STRIDE, c.y // CELL_STRIDE) == (tx, ty):
                        c.set_interaction(InteractionMode.REMOVED)
                        break
                return (tx, ty)
        return None

    # -- wake bookkeeping -----------------------------------------------
    def _age_all_wake(self) -> None:
        new_wake: dict[tuple[int, int], int] = {}
        for cell, age in self._wake.items():
            if age + 1 > K_DECAY:
                # decay: remove the sprite below
                spr = self._wake_sprites.pop(cell, None)
                if spr is not None:
                    spr.set_interaction(InteractionMode.REMOVED)
                continue
            new_wake[cell] = age + 1
        self._wake = new_wake
        self._refresh_wake_sprite_visuals()

    def _add_wake(self, lx: int, ly: int) -> None:
        self._wake[(lx, ly)] = 1
        self._spawn_wake_sprite(lx, ly, 1)

    def _clear_all_wake(self) -> None:
        for cell, spr in list(self._wake_sprites.items()):
            spr.set_interaction(InteractionMode.REMOVED)
        self._wake = {}
        self._wake_sprites = {}

    def _spawn_wake_sprite(self, lx: int, ly: int, age: int) -> None:
        kind = sprites[_WAKE_AGE_NAMES[age]]
        spr = kind.clone()
        spr.set_position(*_to_pixel(lx, ly))
        # Attach to the level so it renders.
        self.current_level.add_sprite(spr) if hasattr(self.current_level, "add_sprite") else None
        # If the engine doesn't expose add_sprite, fall back: levels expose `_sprites` list.
        if not hasattr(self.current_level, "add_sprite"):
            try:
                self.current_level._sprites.append(spr)  # type: ignore[attr-defined]
            except Exception:
                pass
        self._wake_sprites[(lx, ly)] = spr

    def _refresh_wake_sprite_visuals(self) -> None:
        """Re-spawn sprites at the right age tier so visuals match self._wake."""
        for cell, age in self._wake.items():
            spr = self._wake_sprites.get(cell)
            target_name = _WAKE_AGE_NAMES[age]
            if spr is None:
                self._spawn_wake_sprite(*cell, age=age)
                continue
            # If the sprite kind doesn't match this age tier, swap it.
            if spr.name != target_name:
                spr.set_interaction(InteractionMode.REMOVED)
                self._spawn_wake_sprite(*cell, age=age)

    # -- soft-lock detector ---------------------------------------------
    def _is_soft_locked(self) -> bool:
        # Win predicate already satisfied → not soft-locked.
        if self._win_predicate():
            return False
        lx, ly = self._player_cell()
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = lx + dx, ly + dy
            # Off-grid and walls block movement non-lethally.
            if not self._is_walkable(nx, ny):
                continue
            # An adjacent wake cell still blocks (lethal); but that's a lethal
            # trap — equivalent to "the only valid moves all lose".
            # We treat lethal-only neighbours as soft-locked too: the player
            # can't make ANY non-losing move.
            if self._wake_at(nx, ny):
                continue
            return False
        return True

    # -- win/lose -------------------------------------------------------
    def _win_predicate(self) -> bool:
        for c in self.current_level.get_sprites_by_tag("collectible"):
            if c.interaction != InteractionMode.REMOVED:
                return False
        return True

    # -- step -----------------------------------------------------------
    def step(self) -> None:
        # Step counter HUD.
        remaining = self._step_budget - self._action_count
        self._step_counter_ui.set_current(remaining)
        if self._action_count >= self._step_budget:
            self.lose()
            self.complete_action()
            return

        action_id = self.action.id.value if hasattr(self.action.id, "value") else int(self.action.id)
        dx, dy = self._direction_for(action_id)
        if (dx, dy) == (0, 0):
            self.complete_action()
            return

        lx, ly = self._player_cell()
        nx, ny = lx + dx, ly + dy

        # Wall / off-grid: reject move (no-op, step counter still ticks).
        if not self._is_walkable(nx, ny):
            self.complete_action()
            return

        # Wake at destination: lose.
        if self._wake_at(nx, ny):
            self.lose()
            self.complete_action()
            return

        # Successful move.
        self._player().set_position(*_to_pixel(nx, ny))

        # Age existing wake first.
        self._age_all_wake()

        # Add wake at the originally-vacated cell. Don't add wake on the
        # destination cell. (If teleported below, this is the pre-teleport cell.)
        self._add_wake(lx, ly)

        # Pad effects at destination (clearer / collectible / warp). Clearer
        # fires AFTER the wake-add so it wipes the just-added wake too.
        teleport_dest = self._trigger_pad_at(nx, ny)

        # Win check.
        if self._win_predicate():
            self.next_level()
            self.complete_action()
            return

        # Soft-lock check.
        if self._is_soft_locked():
            self.lose()
            self.complete_action()
            return

        self.complete_action()

    # -- engine hooks ---------------------------------------------------
    def _get_hidden_state(self) -> np.ndarray:
        # Expose the wake count as a tiny debug signal.
        out = np.zeros((4, 4), dtype=np.int16)
        out[0, 0] = self._step_counter_ui.current_steps
        out[0, 1] = len(self._wake)
        return out
