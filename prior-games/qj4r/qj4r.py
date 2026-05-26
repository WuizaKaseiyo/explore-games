"""NovaPlay generated game qj4r."""

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
# Constants
# ---------------------------------------------------------------------

CELL_SIZE = 4
GRID_OFFSET = 16  # 8x8 logical cells * 4 px = 32 px; centered in 64-frame: (64-32)/2

BACKGROUND_COLOR = 3   # grey padding
PADDING_COLOR = 3
ACTIVE_LIGHT = 1       # off-white
ACTIVE_DARK = 2        # light-grey
BAR_FILL_COLOR = 13    # maroon
BAR_EMPTY_COLOR = 4    # off-black

ORANGE = 12
PURPLE = 15
WHITE = 0
MERGED_RIM = 13


# ---------------------------------------------------------------------
# Sprite bank
# ---------------------------------------------------------------------

sprites = {
    "active_floor": Sprite(
        pixels=[[-1] * 64 for _ in range(64)],
        name="active_floor",
        visible=True,
        collidable=False,
        tags=["active"],
        layer=0,
    ),
    "piece_orange": Sprite(
        pixels=[
            [-1, ORANGE, ORANGE, -1],
            [ORANGE, WHITE, ORANGE, ORANGE],
            [ORANGE, ORANGE, ORANGE, ORANGE],
            [-1, ORANGE, ORANGE, -1],
        ],
        name="piece_orange",
        visible=True,
        collidable=False,
        tags=["piece", "orange"],
        layer=2,
    ),
    "piece_orange_merged": Sprite(
        pixels=[
            [MERGED_RIM, ORANGE, ORANGE, MERGED_RIM],
            [ORANGE, WHITE, ORANGE, ORANGE],
            [ORANGE, ORANGE, WHITE, ORANGE],
            [MERGED_RIM, ORANGE, ORANGE, MERGED_RIM],
        ],
        name="piece_orange_merged",
        visible=True,
        collidable=False,
        tags=["piece", "orange", "merged"],
        layer=2,
    ),
    "piece_purple": Sprite(
        pixels=[
            [-1, PURPLE, PURPLE, -1],
            [PURPLE, WHITE, PURPLE, PURPLE],
            [PURPLE, PURPLE, PURPLE, PURPLE],
            [-1, PURPLE, PURPLE, -1],
        ],
        name="piece_purple",
        visible=True,
        collidable=False,
        tags=["piece", "purple"],
        layer=2,
    ),
    "target_orange": Sprite(
        pixels=[
            [ORANGE, ORANGE, ORANGE, ORANGE],
            [ORANGE, -1, -1, ORANGE],
            [ORANGE, -1, -1, ORANGE],
            [ORANGE, ORANGE, ORANGE, ORANGE],
        ],
        name="target_orange",
        visible=True,
        collidable=False,
        tags=["target", "orange"],
        layer=1,
    ),
    "target_purple": Sprite(
        pixels=[
            [PURPLE, PURPLE, PURPLE, PURPLE],
            [PURPLE, -1, -1, PURPLE],
            [PURPLE, -1, -1, PURPLE],
            [PURPLE, PURPLE, PURPLE, PURPLE],
        ],
        name="target_purple",
        visible=True,
        collidable=False,
        tags=["target", "purple"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# Levels (3, per design-constraints/composition-and-tutorial.md)
# ---------------------------------------------------------------------

def _at(sprite_key: str, cx: int, cy: int) -> Sprite:
    return sprites[sprite_key].clone().set_position(
        GRID_OFFSET + cx * CELL_SIZE, GRID_OFFSET + cy * CELL_SIZE
    )


def _floor_at_origin() -> Sprite:
    return sprites["active_floor"].clone().set_position(0, 0)


levels = [
    Level(
        sprites=[
            _floor_at_origin(),
            _at("piece_orange", 1, 1),
            _at("target_orange", 6, 6),
        ],
        grid_size=(64, 64),
        data={"step_budget": 10},
    ),
    Level(
        sprites=[
            _floor_at_origin(),
            _at("piece_orange", 1, 4),
            _at("piece_orange", 6, 4),
            _at("target_orange", 5, 4),
        ],
        grid_size=(64, 64),
        data={"step_budget": 14},
    ),
    Level(
        sprites=[
            _floor_at_origin(),
            _at("piece_orange", 1, 4),
            _at("piece_orange", 6, 4),
            _at("target_orange", 5, 4),
            _at("piece_purple", 2, 1),
            _at("target_purple", 5, 1),
        ],
        grid_size=(64, 64),
        data={"step_budget": 22},
    ),
]


# ---------------------------------------------------------------------
# HUD
# ---------------------------------------------------------------------

class StepBarHud(RenderableUserDisplay):
    def __init__(self, max_steps: int) -> None:
        self.max_steps = max(1, max_steps)
        self.current_steps = max_steps

    def reset(self, max_steps: int) -> None:
        self.max_steps = max(1, max_steps)
        self.current_steps = max_steps

    def set_remaining(self, n: int) -> None:
        self.current_steps = max(0, min(n, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        bar_width = 32
        x_offset = 16
        ratio = self.current_steps / self.max_steps if self.max_steps > 0 else 0
        filled = int(round(bar_width * ratio))
        for x in range(bar_width):
            frame[63, x_offset + x] = BAR_FILL_COLOR if x < filled else BAR_EMPTY_COLOR
        return frame


# ---------------------------------------------------------------------
# Game class
# ---------------------------------------------------------------------

class Qj4r(NovaBaseGame):
    def __init__(self) -> None:
        self._cell_size = CELL_SIZE
        self._grid_offset = GRID_OFFSET
        self.active_x_min = 0
        self.active_x_max = 7
        self.active_y_min = 0
        self.active_y_max = 7
        self._step_budget = 8
        # Animation state
        self._anim_phase = -1
        self._anim_total = 0
        self._anim_action_id = 0
        self._anim_paths: list[tuple] = []
        self._anim_kept_lo = 0
        self._anim_kept_hi = 0
        self._anim_axis = "x"
        self._step_bar = StepBarHud(max_steps=8)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_bar],
        )
        super().__init__(
            game_id="qj4r",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    def on_set_level(self, level: Level) -> None:
        self.active_x_min = 0
        self.active_x_max = 7
        self.active_y_min = 0
        self.active_y_max = 7
        self._anim_phase = -1
        self._anim_paths = []
        budget = level.get_data("step_budget") or 8
        self._step_budget = budget
        self._step_bar.reset(budget)
        self._rebuild_active_floor()

    # --- helpers -----------------------------------------------------

    def _to_logical(self, sprite: Sprite) -> tuple[int, int]:
        return ((sprite.x - self._grid_offset) // self._cell_size,
                (sprite.y - self._grid_offset) // self._cell_size)

    def _set_logical(self, sprite: Sprite, cx: int, cy: int) -> None:
        sprite.set_position(self._grid_offset + cx * self._cell_size,
                            self._grid_offset + cy * self._cell_size)

    def _floor_sprite(self) -> Sprite | None:
        for s in self.current_level.get_sprites_by_tag("active"):
            return s
        return None

    def _rebuild_active_floor(self) -> None:
        floor = self._floor_sprite()
        if floor is None:
            return
        cs = self._cell_size
        floor.pixels[:] = -1
        for cy in range(self.active_y_min, self.active_y_max + 1):
            for cx in range(self.active_x_min, self.active_x_max + 1):
                color = ACTIVE_LIGHT if (cx + cy) % 2 == 0 else ACTIVE_DARK
                px = self._grid_offset + cx * cs
                py = self._grid_offset + cy * cs
                floor.pixels[py:py + cs, px:px + cs] = color

    # --- fold mechanics ---------------------------------------------

    def _compute_fold(self, action_id: int):
        """Return (axis_label, reflect_fn, kept_lo, kept_hi) for the given action."""
        if action_id in (1, 2):
            lo, hi = self.active_y_min, self.active_y_max
            sum_axis = lo + hi
            if action_id == 1:
                # fold-top-onto-bottom: kept = bottom half (larger y)
                kept_lo = (lo + hi + 1) // 2 + ((lo + hi) % 2 != 0 and (lo + hi) > 0 and 0)
                kept_lo = (lo + hi) // 2 + 1 if (lo + hi) % 2 == 1 else (lo + hi) // 2 + 1
                # Simpler: kept_lo = ceil((lo+hi+1)/2), kept_hi = hi
                kept_lo = (lo + hi + 1) // 2 + (1 if (lo + hi + 1) % 2 != 0 else 0)
                kept_lo = ((lo + hi) // 2) + 1
                kept_hi = hi
                def reflect(cx, cy, kept_lo=kept_lo, sum_axis=sum_axis):
                    if cy < kept_lo:
                        return cx, sum_axis - cy
                    return cx, cy
                return ("y", reflect, kept_lo, kept_hi)
            else:
                # fold-bottom-onto-top: kept = top half (smaller y)
                kept_lo = lo
                kept_hi = (lo + hi) // 2
                def reflect(cx, cy, kept_hi=kept_hi, sum_axis=sum_axis):
                    if cy > kept_hi:
                        return cx, sum_axis - cy
                    return cx, cy
                return ("y", reflect, kept_lo, kept_hi)
        elif action_id in (3, 4):
            lo, hi = self.active_x_min, self.active_x_max
            sum_axis = lo + hi
            if action_id == 3:
                # fold-left-onto-right: kept = right half
                kept_lo = ((lo + hi) // 2) + 1
                kept_hi = hi
                def reflect(cx, cy, kept_lo=kept_lo, sum_axis=sum_axis):
                    if cx < kept_lo:
                        return sum_axis - cx, cy
                    return cx, cy
                return ("x", reflect, kept_lo, kept_hi)
            else:
                # fold-right-onto-left: kept = left half
                kept_lo = lo
                kept_hi = (lo + hi) // 2
                def reflect(cx, cy, kept_hi=kept_hi, sum_axis=sum_axis):
                    if cx > kept_hi:
                        return sum_axis - cx, cy
                    return cx, cy
                return ("x", reflect, kept_lo, kept_hi)
        return None

    def _start_fold_animation(self, action_id: int) -> bool:
        """Plan a fold animation. Returns True if animation began, False if action is a no-op."""
        fold = self._compute_fold(action_id)
        if fold is None:
            return False
        axis, reflect, kept_lo, kept_hi = fold
        if axis == "x" and self.active_x_min == self.active_x_max:
            return False
        if axis == "y" and self.active_y_min == self.active_y_max:
            return False
        # Record interpolation paths for sprites that move (pieces and decoys reflect; targets are anchored).
        self._anim_paths = []
        for sprite in self.current_level.get_sprites():
            if "active" in sprite.tags:
                continue
            if "target" in sprite.tags:
                continue
            if sprite.interaction == InteractionMode.REMOVED:
                continue
            cx0, cy0 = self._to_logical(sprite)
            new_cx, new_cy = reflect(cx0, cy0)
            if (cx0, cy0) == (new_cx, new_cy):
                continue
            px0 = self._grid_offset + cx0 * self._cell_size
            py0 = self._grid_offset + cy0 * self._cell_size
            px1 = self._grid_offset + new_cx * self._cell_size
            py1 = self._grid_offset + new_cy * self._cell_size
            self._anim_paths.append((sprite, px0, py0, px1, py1, new_cx, new_cy))
        self._anim_action_id = action_id
        self._anim_axis = axis
        self._anim_kept_lo = kept_lo
        self._anim_kept_hi = kept_hi
        self._anim_phase = 0
        self._anim_total = 3  # 3 in-flight midway frames; finalize on the 4th step() call
        self._render_animation_phase(self._anim_phase)
        return True

    def _render_animation_phase(self, phase: int) -> None:
        """Render an in-flight animation frame: pieces interpolated toward destinations."""
        t = (phase + 1) / (self._anim_total + 1)  # 0.25, 0.5, 0.75 for total=3
        for sprite, px0, py0, px1, py1, _, _ in self._anim_paths:
            ipx = int(round(px0 + t * (px1 - px0)))
            ipy = int(round(py0 + t * (py1 - py0)))
            sprite.set_position(ipx, ipy)
        self._render_animation_floor(t)

    def _render_animation_floor(self, t: float) -> None:
        """During animation, dim the half being folded out."""
        floor = self._floor_sprite()
        if floor is None:
            return
        cs = self._cell_size
        floor.pixels[:] = -1
        for cy in range(self.active_y_min, self.active_y_max + 1):
            for cx in range(self.active_x_min, self.active_x_max + 1):
                in_kept = self._cell_in_kept_half(cx, cy)
                if in_kept:
                    color = ACTIVE_LIGHT if (cx + cy) % 2 == 0 else ACTIVE_DARK
                else:
                    # Fade from normal to maroon as t→1
                    color = MERGED_RIM if t > 0.5 else (ACTIVE_DARK if (cx + cy) % 2 == 0 else BAR_FILL_COLOR)
                px = self._grid_offset + cx * cs
                py = self._grid_offset + cy * cs
                floor.pixels[py:py + cs, px:px + cs] = color

    def _cell_in_kept_half(self, cx: int, cy: int) -> bool:
        if self._anim_axis == "x":
            return self._anim_kept_lo <= cx <= self._anim_kept_hi
        return self._anim_kept_lo <= cy <= self._anim_kept_hi

    def _finalize_fold(self) -> None:
        """Apply the actual fold: snap reflective sprites to destinations, contract active region,
        anchor targets (and lose if any are now stranded outside kept half), apply M2/M3."""
        # Snap reflective sprites to their final cells.
        for sprite, _, _, _, _, new_cx, new_cy in self._anim_paths:
            self._set_logical(sprite, new_cx, new_cy)
        # Contract active region.
        if self._anim_axis == "x":
            self.active_x_min = self._anim_kept_lo
            self.active_x_max = self._anim_kept_hi
        else:
            self.active_y_min = self._anim_kept_lo
            self.active_y_max = self._anim_kept_hi
        # Anchored targets: if any target's cell is outside the new active region, it is destroyed.
        targets_destroyed = False
        for sprite in self.current_level.get_sprites_by_tag("target"):
            if sprite.interaction == InteractionMode.REMOVED:
                continue
            cx, cy = self._to_logical(sprite)
            in_active = (self.active_x_min <= cx <= self.active_x_max and
                         self.active_y_min <= cy <= self.active_y_max)
            if not in_active:
                sprite.set_interaction(InteractionMode.REMOVED)
                targets_destroyed = True
        # Apply transformation rules.
        self._apply_same_colour_merge()
        # Rebuild floor with normal colours and contracted region.
        self._rebuild_active_floor()
        # Reset animation state.
        self._anim_phase = -1
        self._anim_paths = []
        # If any target was destroyed and that colour still has pieces, the level is unwinnable.
        if targets_destroyed and self._is_unwinnable():
            # Lose flagged externally in step() based on _check_unwinnable result.
            pass

    def _is_unwinnable(self) -> bool:
        """A colour has more active pieces than active targets (or 0 targets with active pieces)."""
        for colour in ("orange", "purple"):
            pieces = [s for s in self.current_level.get_sprites_by_tag(colour)
                      if "piece" in s.tags and s.interaction != InteractionMode.REMOVED]
            targets = [s for s in self.current_level.get_sprites_by_tag(colour)
                       if "target" in s.tags and s.interaction != InteractionMode.REMOVED]
            if len(pieces) > len(targets):
                return True
        return False

    def _apply_same_colour_merge(self) -> None:
        for colour in ("orange", "purple"):
            cells: dict[tuple[int, int], list[Sprite]] = {}
            for s in self.current_level.get_sprites_by_tag(colour):
                if "piece" not in s.tags:
                    continue
                if s.interaction == InteractionMode.REMOVED:
                    continue
                cells.setdefault(self._to_logical(s), []).append(s)
            merged_key = f"piece_{colour}_merged"
            if merged_key not in sprites:
                continue
            for group in cells.values():
                if len(group) < 2:
                    continue
                survivor = group[0]
                survivor.pixels = sprites[merged_key].pixels.copy()
                if "merged" not in survivor.tags:
                    survivor.tags.append("merged")
                for other in group[1:]:
                    other.set_interaction(InteractionMode.REMOVED)

    # --- win / lose --------------------------------------------------

    def _check_win(self) -> bool:
        for colour in ("orange", "purple"):
            pieces = [s for s in self.current_level.get_sprites_by_tag(colour)
                      if "piece" in s.tags and s.interaction != InteractionMode.REMOVED]
            targets = [s for s in self.current_level.get_sprites_by_tag(colour)
                       if "target" in s.tags and s.interaction != InteractionMode.REMOVED]
            if len(pieces) == 0 and len(targets) == 0:
                continue
            if len(pieces) != len(targets):
                return False
            piece_cells = sorted(self._to_logical(p) for p in pieces)
            target_cells = sorted(self._to_logical(t) for t in targets)
            if piece_cells != target_cells:
                return False
        return True

    # --- step --------------------------------------------------------

    def step(self) -> None:
        # If a fold animation is in flight, advance it.
        if self._anim_phase >= 0:
            self._anim_phase += 1
            if self._anim_phase < self._anim_total:
                self._render_animation_phase(self._anim_phase)
                return  # continue animating; engine will call step() again
            # Final phase: snap to destination, anchor-check targets, apply transformations.
            self._finalize_fold()
            self._post_action_resolve()
            return

        # No animation in progress; start one if the action is a fold.
        action = self.action.id
        if action in (GameAction.ACTION1, GameAction.ACTION2,
                      GameAction.ACTION3, GameAction.ACTION4):
            started = self._start_fold_animation(action.value)
            if started:
                return  # animation will run over subsequent step() calls
        # No-op fold (e.g. region 1-cell wide on the chosen axis): resolve immediately.
        self._post_action_resolve()

    def _post_action_resolve(self) -> None:
        """Update HUD, run win/lose checks, and complete the action."""
        remaining = self._step_budget - self._action_count
        self._step_bar.set_remaining(remaining)
        if self._check_win():
            self.next_level()
            self.complete_action()
            return
        # Lose if any colour has more pieces than targets (a target was destroyed by a wrong fold)
        # or if the step budget is exhausted.
        if self._is_unwinnable() or self._action_count >= self._step_budget:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 5), dtype=np.int16)
        state[0, 0] = self.active_x_min
        state[0, 1] = self.active_x_max
        state[0, 2] = self.active_y_min
        state[0, 3] = self.active_y_max
        state[0, 4] = self._step_budget - self._action_count
        return state
