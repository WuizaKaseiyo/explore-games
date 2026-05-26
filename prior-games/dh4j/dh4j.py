"""Generated game source (dh4j)."""

from typing import Optional

import numpy as np
from novaengine import (
    ActionInput,
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

# Cell stride in pixels (each game cell renders as 8x8 pixels).
CELL = 8


def _floor_pip_1() -> list[list[int]]:
    """1-pip yellow floor — a single 2x2 yellow accent centered."""
    return [
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 11, 11, 1, 1, 5],
        [5, 1, 1, 11, 11, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
    ]


def _floor_pip_2() -> list[list[int]]:
    """2-pip yellow floor — two 2x2 yellow accents side-by-side."""
    return [
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 11, 11, 1, 1, 11, 11, 5],
        [5, 11, 11, 1, 1, 11, 11, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
    ]


def _floor_pip_3() -> list[list[int]]:
    """3-pip yellow floor — three vertical 1x2 yellow accents."""
    return [
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 11, 1, 11, 1, 11, 5],
        [5, 1, 11, 1, 11, 1, 11, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
    ]


def _pivot_pip_2() -> list[list[int]]:
    """2-pip yellow floor + one maroon BONUS pip in the top-right.

    The maroon pip is the persistent visual cue that this cell is a pivot;
    on consumption the maroon pip is removed and the cell renders as a plain
    `_floor_pip_2()` (or `_floor_pip_3()` if the switch toggled it).
    """
    return [
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 1, 1, 1, 13, 13, 1, 5],
        [5, 1, 1, 1, 13, 13, 1, 5],
        [5, 11, 11, 1, 1, 11, 11, 5],
        [5, 11, 11, 1, 1, 11, 11, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
    ]


def _pivot_pip_3() -> list[list[int]]:
    """3-pip yellow floor + one maroon BONUS pip in the top-right.

    Used when the switch has been toggled and a former pivot+pip-2 cell now
    visually carries 3 stride pips. Same bonus-pip cue as `_pivot_pip_2()`.
    """
    return [
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 1, 1, 1, 13, 13, 1, 5],
        [5, 1, 1, 1, 13, 13, 1, 5],
        [5, 1, 11, 1, 11, 1, 11, 5],
        [5, 1, 11, 1, 11, 1, 11, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
    ]


sprites: dict[str, Sprite] = {
    "avatar_normal": Sprite(
        pixels=[
            [-1, -1, 6, 6, 6, 6, -1, -1],
            [-1, 6, 6, 6, 6, 6, 6, -1],
            [6, 6, 6, 6, 6, 6, 6, 6],
            [6, 6, 6, 0, 0, 6, 6, 6],
            [6, 6, 6, 0, 0, 6, 6, 6],
            [6, 6, 6, 6, 6, 6, 6, 6],
            [-1, 6, 6, 6, 6, 6, 6, -1],
            [-1, -1, 6, 6, 6, 6, -1, -1],
        ],
        name="avatar_normal",
        visible=True,
        collidable=False,
        tags=["avatar"],
        layer=2,
    ),
    "floor_pip_1": Sprite(
        pixels=_floor_pip_1(),
        name="floor_pip_1",
        visible=True,
        collidable=False,
        tags=["floor", "pip_1"],
        layer=0,
    ),
    "floor_pip_2": Sprite(
        pixels=_floor_pip_2(),
        name="floor_pip_2",
        visible=True,
        collidable=False,
        tags=["floor", "pip_2"],
        layer=0,
    ),
    "floor_pip_3": Sprite(
        pixels=_floor_pip_3(),
        name="floor_pip_3",
        visible=True,
        collidable=False,
        tags=["floor", "pip_3"],
        layer=0,
    ),
    "wall_block": Sprite(
        pixels=[
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 4, 4, 4, 4, 4, 4, 5],
            [5, 4, 4, 4, 4, 4, 4, 5],
            [5, 4, 4, 4, 4, 4, 4, 5],
            [5, 4, 4, 4, 4, 4, 4, 5],
            [5, 4, 4, 4, 4, 4, 4, 5],
            [5, 4, 4, 4, 4, 4, 4, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
        ],
        name="wall_block",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    ),
    "goal_cell": Sprite(
        pixels=[
            [14, 14, 14, 14, 14, 14, 14, 14],
            [14, 14, 14, 14, 14, 14, 14, 14],
            [14, 14, 0, 0, 0, 0, 14, 14],
            [14, 14, 0, 14, 14, 0, 14, 14],
            [14, 14, 0, 14, 14, 0, 14, 14],
            [14, 14, 0, 0, 0, 0, 14, 14],
            [14, 14, 14, 14, 14, 14, 14, 14],
            [14, 14, 14, 14, 14, 14, 14, 14],
        ],
        name="goal_cell",
        visible=True,
        collidable=False,
        tags=["goal"],
        layer=1,
    ),
    # Switch — a raised "button" sprite visually distinct from any floor cell.
    # Concentric rings: orange outer, maroon mid, white core. Rounded corners
    # (-1 transparent at the 4 outer corners). Stepping on it swaps every
    # pip-2 and pip-3 floor sprite's pip count in place.
    "switch_button": Sprite(
        pixels=[
            [-1, 5, 5, 5, 5, 5, 5, -1],
            [5, 12, 12, 12, 12, 12, 12, 5],
            [5, 12, 13, 13, 13, 13, 12, 5],
            [5, 12, 13, 0, 0, 13, 12, 5],
            [5, 12, 13, 0, 0, 13, 12, 5],
            [5, 12, 13, 13, 13, 13, 12, 5],
            [5, 12, 12, 12, 12, 12, 12, 5],
            [-1, 5, 5, 5, 5, 5, 5, -1],
        ],
        name="switch_button",
        visible=True,
        collidable=False,
        tags=["switch"],
        layer=1,
    ),
    # Pivot composite — a 2-pip yellow floor that visibly carries one extra
    # maroon BONUS pip in the top-right corner. Landing on it transfers the
    # bonus pip to the avatar (rendered as a maroon corner dot). On the next
    # press the bonus is consumed and the pivot reverts to a plain pip floor.
    "pivot_pip_2": Sprite(
        pixels=_pivot_pip_2(),
        name="pivot_pip_2",
        visible=True,
        collidable=False,
        tags=["floor", "pip_2", "pivot"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS (exactly 3 entries)
# ---------------------------------------------------------------------

# Layout grammar:
#   '.' floor pip-1
#   '2' floor pip-2
#   '3' floor pip-3
#   'W' wall
#   'G' goal
#   'S' switch button
#   'P' pivot composite (pip-2 + bonus pip)
#   'A' avatar starting cell (treated as pip-1 floor underneath)
#
# Each layout is 8 cols x 7 rows of cells (cy 0..6).
LEVEL_1_LAYOUT = [
    ".......G",
    "........",
    "........",
    "WWWWWWWW",
    "A..3....",
    "........",
    "........",
]

LEVEL_2_LAYOUT = [
    ".......G",
    "........",
    "WWWWWWWW",
    "WWWWWWWW",
    "A..2.S..",
    "........",
    "........",
]

LEVEL_3_LAYOUT = [
    ".......G",
    "........",
    "WWWWWWWW",
    "WWWWWWWW",
    "WWWWWWWW",
    "A..P....",
    ".....S..",
]


def _build_level_sprites(layout: list[str]) -> list[Sprite]:
    """Translate a layout-string grid into a list of placed Sprite instances."""
    placed: list[Sprite] = []
    for cy, row in enumerate(layout):
        for cx, ch in enumerate(row):
            px, py = cx * CELL, cy * CELL
            if ch == "W":
                placed.append(sprites["wall_block"].clone().set_position(px, py))
            elif ch == "G":
                placed.append(sprites["goal_cell"].clone().set_position(px, py))
            elif ch == "S":
                placed.append(sprites["switch_button"].clone().set_position(px, py))
            elif ch == "P":
                placed.append(sprites["pivot_pip_2"].clone().set_position(px, py))
            elif ch == "2":
                placed.append(sprites["floor_pip_2"].clone().set_position(px, py))
            elif ch == "3":
                placed.append(sprites["floor_pip_3"].clone().set_position(px, py))
            else:
                # '.' or 'A' — pip-1 floor underneath.
                placed.append(sprites["floor_pip_1"].clone().set_position(px, py))
            if ch == "A":
                placed.append(sprites["avatar_normal"].clone().set_position(px, py))
    return placed


levels: list[Level] = [
    Level(
        sprites=_build_level_sprites(LEVEL_1_LAYOUT),
        grid_size=(64, 64),
        data={"step_budget": 30},
    ),
    Level(
        sprites=_build_level_sprites(LEVEL_2_LAYOUT),
        grid_size=(64, 64),
        data={"step_budget": 50},
    ),
    Level(
        sprites=_build_level_sprites(LEVEL_3_LAYOUT),
        grid_size=(64, 64),
        data={"step_budget": 80},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 1
PADDING_COLOR = 3
PLAYFIELD_COLS = 8
PLAYFIELD_ROWS = 7
STEP_COUNTER_ROW = 63
DEFAULT_STEP_BUDGET = 30

DIRECTION_MAP = {
    GameAction.ACTION1: (0, -1),
    GameAction.ACTION2: (0, 1),
    GameAction.ACTION3: (-1, 0),
    GameAction.ACTION4: (1, 0),
}


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------


class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0) -> None:
        self._max_steps = max_steps
        self._current = max_steps

    def set_max(self, max_steps: int) -> None:
        self._max_steps = max_steps
        self._current = max_steps

    def set_current(self, current: int) -> None:
        self._current = max(0, min(current, self._max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self._max_steps <= 0:
            return frame
        fill = round(64 * self._current / self._max_steps)
        for x in range(64):
            frame[STEP_COUNTER_ROW, x] = 11 if x < fill else 4
        return frame


# ---------------------------------------------------------------------
# 5. GAME CLASS
# ---------------------------------------------------------------------


class Dh4j(NovaBaseGame):
    def __init__(self) -> None:
        self._step_hud = StepCounterHud(0)
        self._pending_bonus = 0
        self._armed_pivot: Optional[Sprite] = None
        self._slide_remaining = 0
        self._slide_dx = 0
        self._slide_dy = 0
        self._max_steps = DEFAULT_STEP_BUDGET
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_hud],
        )
        super().__init__(
            game_id="dh4j",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    def on_set_level(self, level: Level) -> None:
        self._pending_bonus = 0
        self._armed_pivot = None
        self._slide_remaining = 0
        self._slide_dx = 0
        self._slide_dy = 0
        self._max_steps = level.get_data("step_budget") or DEFAULT_STEP_BUDGET
        self._step_hud.set_max(self._max_steps)
        self._step_hud.set_current(self._max_steps)

    # -- avatar / cell helpers -----------------------------------------

    def _get_avatar(self) -> Sprite:
        return self.current_level.get_sprites_by_tag("avatar")[0]

    def _set_avatar_pending_visual(self, pending: bool) -> None:
        """Paint or clear the maroon 2x2 bonus dot at the avatar's top-right corner.

        When `pending` is True, the avatar's top-right 2x2 patch becomes
        maroon (color 13) — visually matching the maroon bonus pip that lived
        on the pivot cell. When False, the patch reverts to the avatar's
        base magenta (color 6).
        """
        av = self._get_avatar()
        marker = 13 if pending else 6
        av.pixels[1, 5] = marker
        av.pixels[1, 6] = marker
        av.pixels[2, 5] = marker
        av.pixels[2, 6] = marker

    def _floor_at(self, px: int, py: int) -> Optional[Sprite]:
        for s in self.current_level.get_sprites_by_tag("floor"):
            if s.x == px and s.y == py:
                return s
        return None

    def _cell_at(self, px: int, py: int) -> Optional[Sprite]:
        for tag in ("switch", "goal"):
            for s in self.current_level.get_sprites_by_tag(tag):
                if s.x == px and s.y == py:
                    return s
        return self._floor_at(px, py)

    def _stride_for_cell(self, cell: Optional[Sprite]) -> int:
        if cell is None:
            return 1
        if "pip_3" in cell.tags:
            return 3
        if "pip_2" in cell.tags:
            return 2
        if "pip_1" in cell.tags:
            return 1
        return 1

    def _cell_in_bounds(self, cx: int, cy: int) -> bool:
        return 0 <= cx < PLAYFIELD_COLS and 0 <= cy < PLAYFIELD_ROWS

    def _is_wall_at_grid(self, cx: int, cy: int) -> bool:
        if not self._cell_in_bounds(cx, cy):
            return True  # off-grid acts as a wall
        px, py = cx * CELL, cy * CELL
        for s in self.current_level.get_sprites_by_tag("wall"):
            if s.x == px and s.y == py:
                return True
        return False

    # -- switch / pivot transitions ------------------------------------

    def _toggle_switch(self) -> None:
        """Swap every pip-2 and pip-3 floor cell in place.

        Pivot composites keep their bonus pip across the swap by switching
        to the matching `_pivot_pip_{2,3}` pattern. Plain floor cells use
        the `_floor_pip_{2,3}` pattern.
        """
        for s in self.current_level.get_sprites_by_tag("floor"):
            is_pivot = "pivot" in s.tags
            if "pip_2" in s.tags:
                new_pixels = _pivot_pip_3() if is_pivot else _floor_pip_3()
                s.pixels[:] = np.array(new_pixels, dtype=np.int8)
                s.tags.remove("pip_2")
                s.tags.append("pip_3")
            elif "pip_3" in s.tags:
                new_pixels = _pivot_pip_2() if is_pivot else _floor_pip_2()
                s.pixels[:] = np.array(new_pixels, dtype=np.int8)
                s.tags.remove("pip_3")
                s.tags.append("pip_2")

    def _arm_pivot(self, pivot_sprite: Sprite) -> None:
        self._pending_bonus = 1
        self._armed_pivot = pivot_sprite
        self._set_avatar_pending_visual(True)

    def _consume_pivot(self) -> None:
        """Remove the bonus-pip from the previously-armed pivot cell.

        The pivot cell reverts to a plain `floor_pip_2` or `floor_pip_3`
        (matching its current pip count) and loses the `pivot` tag.
        """
        if self._armed_pivot is None:
            return
        if "pip_3" in self._armed_pivot.tags:
            new_pixels = _floor_pip_3()
        else:
            new_pixels = _floor_pip_2()
        self._armed_pivot.pixels[:] = np.array(new_pixels, dtype=np.int8)
        if "pivot" in self._armed_pivot.tags:
            self._armed_pivot.tags.remove("pivot")
        self._armed_pivot = None

    # -- per-frame step ------------------------------------------------

    def step(self) -> None:
        # In the middle of a slide animation, advance one cell per frame.
        if self._slide_remaining > 0:
            self._advance_slide_one_cell()
            return

        # Budget check at the start of a new press.
        if self._action_count > self._max_steps:
            self.lose()
            self.complete_action()
            return

        aid = self.action.id
        if aid in DIRECTION_MAP:
            self._handle_press(aid)
            if self._slide_remaining == 0:
                # No-op press (or instant trivial result); the press still
                # counts toward the budget via _action_count.
                self._update_step_hud()
                self.complete_action()
            return

        self.complete_action()

    def _handle_press(self, aid: GameAction) -> None:
        avatar = self._get_avatar()
        dx_dir, dy_dir = DIRECTION_MAP[aid]
        cell = self._cell_at(avatar.x, avatar.y)
        base_stride = self._stride_for_cell(cell)
        effective_stride = base_stride + self._pending_bonus
        bonus_was_pending = self._pending_bonus > 0

        # Consume the bonus + the armed pivot at press initiation (per spec).
        if bonus_was_pending:
            self._pending_bonus = 0
            self._consume_pivot()
            self._set_avatar_pending_visual(False)

        if effective_stride <= 0:
            return

        cx = avatar.x // CELL
        cy = avatar.y // CELL
        dest_cx = cx + dx_dir * effective_stride
        dest_cy = cy + dy_dir * effective_stride

        if self._is_wall_at_grid(dest_cx, dest_cy):
            return  # no-op; press still counted by _action_count

        self._slide_dx = dx_dir
        self._slide_dy = dy_dir
        self._slide_remaining = effective_stride

    def _advance_slide_one_cell(self) -> None:
        avatar = self._get_avatar()
        avatar.set_position(
            avatar.x + self._slide_dx * CELL,
            avatar.y + self._slide_dy * CELL,
        )
        self._slide_remaining -= 1

        # Mid-slide goal-overlap check.
        if self._on_goal(avatar):
            self._slide_remaining = 0
            self._update_step_hud()
            self.next_level()
            self.complete_action()
            return

        if self._slide_remaining == 0:
            self._finalize_slide_landing()

    def _finalize_slide_landing(self) -> None:
        avatar = self._get_avatar()
        # Switch landing — toggle every pip-2 <-> pip-3 cell on the playfield.
        for s in self.current_level.get_sprites_by_tag("switch"):
            if s.x == avatar.x and s.y == avatar.y:
                self._toggle_switch()
                break
        # Pivot landing — arm the bonus (only fires if the cell still carries
        # the "pivot" tag; once consumed it is gone).
        for s in self.current_level.get_sprites_by_tag("pivot"):
            if s.x == avatar.x and s.y == avatar.y:
                self._arm_pivot(s)
                break
        # Goal landing safety net.
        if self._on_goal(avatar):
            self._update_step_hud()
            self.next_level()
            self.complete_action()
            return
        self._update_step_hud()
        self.complete_action()

    def _on_goal(self, avatar: Sprite) -> bool:
        for s in self.current_level.get_sprites_by_tag("goal"):
            if s.x == avatar.x and s.y == avatar.y:
                return True
        return False

    def _update_step_hud(self) -> None:
        self._step_hud.set_current(self._max_steps - self._action_count)

    # -- engine integration --------------------------------------------

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((2, 2), dtype=np.int16)
        state[0, 0] = self._max_steps - self._action_count
        state[1, 0] = self._pending_bonus
        state[1, 1] = self._slide_remaining
        return state

    def _get_valid_actions(self) -> list[ActionInput]:
        return [ActionInput(id=GameAction.from_id(a)) for a in self._available_actions]
