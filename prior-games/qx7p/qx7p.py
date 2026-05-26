"""Generated game qx7p."""

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
# 1. PIXEL-PATTERN HELPERS
# ---------------------------------------------------------------------
COLUMN_BORDER_COLOR = 4
TARGET_BORDER_COLOR = 3
SEGMENTS_PER_COLUMN = 12
SEGMENT_HEIGHT = 3
COLUMN_WIDTH = 6
COLUMN_HEIGHT = SEGMENTS_PER_COLUMN * SEGMENT_HEIGHT


def _column_pixels(colours: list[int]) -> list[list[int]]:
    if len(colours) != SEGMENTS_PER_COLUMN:
        raise ValueError("column needs exactly 12 segment colours")
    rows: list[list[int]] = []
    for c in colours:
        for _ in range(SEGMENT_HEIGHT):
            rows.append([COLUMN_BORDER_COLOR, c, c, c, c, COLUMN_BORDER_COLOR])
    return rows


def _target_pixels(c: int) -> list[list[int]]:
    border_row = [TARGET_BORDER_COLOR] * 8
    rows: list[list[int]] = [border_row[:]]
    for _ in range(3):
        rows.append([TARGET_BORDER_COLOR, c, c, c, c, c, c, TARGET_BORDER_COLOR])
    rows.append(border_row[:])
    return rows


# ---------------------------------------------------------------------
# 2. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "col_l1_a": Sprite(
        pixels=_column_pixels([9, 12, 14, 11, 12, 8, 15, 14, 9, 14, 11, 12]),
        name="col_l1_a", visible=True, collidable=True, tags=["column"],
    ),
    "col_l1_b": Sprite(
        pixels=_column_pixels([11, 12, 14, 8, 15, 9, 14, 12, 8, 14, 12, 15]),
        name="col_l1_b", visible=True, collidable=True, tags=["column"],
    ),
    "col_l1_c": Sprite(
        pixels=_column_pixels([8, 14, 12, 8, 14, 11, 12, 9, 15, 12, 9, 14]),
        name="col_l1_c", visible=True, collidable=True, tags=["column"],
    ),

    "col_l2_a": Sprite(
        pixels=_column_pixels([12, 14, 8, 15, 11, 9, 12, 8, 15, 11, 14, 8]),
        name="col_l2_a", visible=True, collidable=True, tags=["column"],
    ),
    "col_l2_b": Sprite(
        pixels=_column_pixels([9, 15, 12, 14, 8, 11, 9, 14, 12, 8, 14, 12]),
        name="col_l2_b", visible=True, collidable=True, tags=["column"],
    ),
    "col_l2_c": Sprite(
        pixels=_column_pixels([11, 9, 12, 15, 11, 8, 14, 9, 11, 12, 8, 14]),
        name="col_l2_c", visible=True, collidable=True, tags=["column"],
    ),
    "col_l2_d": Sprite(
        pixels=_column_pixels([11, 12, 9, 15, 12, 14, 11, 8, 12, 14, 9, 15]),
        name="col_l2_d", visible=True, collidable=True, tags=["column"],
    ),

    # L3 columns are designed so the bound-pair sums match (both = 4):
    # pair 1 k_a+k_b = 3+1 = 4; pair 2 k_c+k_d = 4+0 = 4.
    # Solvable offset for sum-4 pair: 2*offset = 4 (mod 12) -> offset 2 or 8.
    # Scan-line cycle picks {6, 7, 8} so only offset 8 satisfies both pairs.
    "col_l3_a": Sprite(
        pixels=_column_pixels([9, 12, 14, 8, 11, 9, 15, 14, 9, 11, 8, 15]),
        name="col_l3_a", visible=True, collidable=True, tags=["column"],
    ),
    "col_l3_b": Sprite(
        pixels=_column_pixels([14, 12, 9, 11, 8, 15, 14, 9, 11, 12, 8, 15]),
        name="col_l3_b", visible=True, collidable=True, tags=["column"],
    ),
    "col_l3_c": Sprite(
        pixels=_column_pixels([8, 14, 12, 8, 11, 14, 9, 12, 15, 8, 14, 12]),
        name="col_l3_c", visible=True, collidable=True, tags=["column"],
    ),
    "col_l3_d": Sprite(
        pixels=_column_pixels([14, 9, 12, 8, 11, 15, 12, 14, 9, 11, 8, 15]),
        name="col_l3_d", visible=True, collidable=True, tags=["column"],
    ),
    "col_l3_e": Sprite(
        pixels=_column_pixels([12, 14, 8, 11, 9, 15, 12, 14, 8, 11, 12, 9]),
        name="col_l3_e", visible=True, collidable=True, tags=["column"],
    ),

    "target_red": Sprite(
        pixels=_target_pixels(8),
        name="target_red", visible=True, collidable=True, tags=["target"],
    ),
    "target_orange": Sprite(
        pixels=_target_pixels(12),
        name="target_orange", visible=True, collidable=True, tags=["target"],
    ),
    "target_yellow": Sprite(
        pixels=_target_pixels(11),
        name="target_yellow", visible=True, collidable=True, tags=["target"],
    ),
    "target_green": Sprite(
        pixels=_target_pixels(14),
        name="target_green", visible=True, collidable=True, tags=["target"],
    ),
    "target_purple": Sprite(
        pixels=_target_pixels(15),
        name="target_purple", visible=True, collidable=True, tags=["target"],
    ),

    "scan_line_bar": Sprite(
        pixels=[[0] * 64],
        name="scan_line_bar", visible=True, collidable=True, tags=["scan_line"],
        layer=2,
    ),
    "scan_line_marker": Sprite(
        pixels=[[11, 11, 11], [11, 11, 11], [11, 11, 11]],
        name="scan_line_marker", visible=True, collidable=True,
        tags=["scan_line_marker"], layer=3,
    ),

    "bound_pair_ribbon_l2": Sprite(
        pixels=[[12] * 15],
        name="bound_pair_ribbon_l2", visible=True, collidable=True,
        tags=["bound_pair"],
    ),
    "bound_pair_ribbon_l3_ab": Sprite(
        pixels=[[12] * 13],
        name="bound_pair_ribbon_l3_ab", visible=True, collidable=True,
        tags=["bound_pair"],
    ),
    "bound_pair_ribbon_l3_cd": Sprite(
        pixels=[[12] * 13],
        name="bound_pair_ribbon_l3_cd", visible=True, collidable=True,
        tags=["bound_pair"],
    ),
    "bound_pair_dot": Sprite(
        pixels=[[12, 12], [12, 12]],
        name="bound_pair_dot", visible=True, collidable=True,
        tags=["bound_pair_dot"],
    ),

    "active_highlight": Sprite(
        pixels=[[0] for _ in range(COLUMN_HEIGHT)],
        name="active_highlight", visible=True, collidable=True,
        tags=["active_highlight"], layer=4,
    ),
}


# ---------------------------------------------------------------------
# 3. LEVELS
# ---------------------------------------------------------------------
levels = [
    Level(
        sprites=[
            sprites["col_l1_a"].clone().set_position(16, 14),
            sprites["col_l1_b"].clone().set_position(32, 14),
            sprites["col_l1_c"].clone().set_position(48, 14),
            sprites["target_green"].clone().set_position(15, 2),
            sprites["target_yellow"].clone().set_position(31, 2),
            sprites["target_purple"].clone().set_position(47, 2),
            sprites["scan_line_bar"].clone().set_position(0, 30),
            sprites["scan_line_marker"].clone().set_position(0, 29),
            sprites["scan_line_marker"].clone().set_position(61, 29),
        ],
        grid_size=(64, 64),
        data={
            "scan_line_rows": [30],
            "step_budget": 40,
            "bound_pairs": [],
            "level_id": 1,
        },
    ),

    Level(
        sprites=[
            sprites["col_l2_a"].clone().set_position(12, 14),
            sprites["col_l2_b"].clone().set_position(26, 14),
            sprites["col_l2_c"].clone().set_position(40, 14),
            sprites["col_l2_d"].clone().set_position(54, 14),
            sprites["target_yellow"].clone().set_position(11, 2),
            sprites["target_purple"].clone().set_position(25, 2),
            sprites["target_green"].clone().set_position(39, 2),
            sprites["target_red"].clone().set_position(53, 2),
            sprites["scan_line_bar"].clone().set_position(0, 30),
            sprites["scan_line_marker"].clone().set_position(0, 29),
            sprites["scan_line_marker"].clone().set_position(61, 29),
            sprites["bound_pair_ribbon_l2"].clone().set_position(15, 10),
            sprites["bound_pair_dot"].clone().set_position(14, 10),
            sprites["bound_pair_dot"].clone().set_position(28, 10),
        ],
        grid_size=(64, 64),
        data={
            "scan_line_rows": [30],
            "step_budget": 70,
            "bound_pairs": [["col_l2_a", "col_l2_b"]],
            "level_id": 2,
        },
    ),

    Level(
        sprites=[
            sprites["col_l3_a"].clone().set_position(6, 14),
            sprites["col_l3_b"].clone().set_position(18, 14),
            sprites["col_l3_c"].clone().set_position(30, 14),
            sprites["col_l3_d"].clone().set_position(42, 14),
            sprites["col_l3_e"].clone().set_position(54, 14),
            sprites["target_red"].clone().set_position(5, 2),
            sprites["target_orange"].clone().set_position(17, 2),
            sprites["target_yellow"].clone().set_position(29, 2),
            sprites["target_green"].clone().set_position(41, 2),
            sprites["target_purple"].clone().set_position(53, 2),
            sprites["scan_line_bar"].clone().set_position(0, 33),
            sprites["scan_line_marker"].clone().set_position(0, 32),
            sprites["scan_line_marker"].clone().set_position(61, 32),
            sprites["bound_pair_ribbon_l3_ab"].clone().set_position(9, 10),
            sprites["bound_pair_dot"].clone().set_position(8, 10),
            sprites["bound_pair_dot"].clone().set_position(20, 10),
            sprites["bound_pair_ribbon_l3_cd"].clone().set_position(33, 10),
            sprites["bound_pair_dot"].clone().set_position(32, 10),
            sprites["bound_pair_dot"].clone().set_position(44, 10),
        ],
        grid_size=(64, 64),
        data={
            "scan_line_rows": [33, 36, 39],
            "step_budget": 100,
            "bound_pairs": [["col_l3_a", "col_l3_b"], ["col_l3_c", "col_l3_d"]],
            "level_id": 3,
        },
    ),
]

BACKGROUND_COLOR = 4
PADDING_COLOR = 4


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0) -> None:
        self.max_steps = max_steps
        self.current = max_steps

    def set_remaining(self, remaining: int) -> None:
        self.current = max(0, min(remaining, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.current / self.max_steps
        filled = round(64 * ratio)
        for x in range(64):
            frame[0, x] = 11 if x < filled else 4
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Qx7p(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_hud = StepCounterHud(max_steps=0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_hud],
        )
        self.active_column: Sprite | None = None
        self._active_highlight_left: Sprite | None = None
        self._active_highlight_right: Sprite | None = None
        self.column_positions: dict[str, int] = {}
        self.column_base_pixels: dict[str, np.ndarray] = {}
        self.bound_partner: dict[str, str] = {}
        self.scan_line_rows: list[int] = []
        self.scan_line_idx: int = 0
        self.steps_remaining: int = 0
        self._scan_line_sprite: Sprite | None = None
        super().__init__(
            game_id="qx7p",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        self.column_positions = {}
        self.column_base_pixels = {}
        for col_sprite in level.get_sprites_by_tag("column"):
            self.column_positions[col_sprite.name] = 0
            base = sprites[col_sprite.name].pixels.copy()
            self.column_base_pixels[col_sprite.name] = base
            col_sprite.pixels = base.copy()

        self.bound_partner = {}
        for pair in level.get_data("bound_pairs") or []:
            a, b = pair[0], pair[1]
            self.bound_partner[a] = b
            self.bound_partner[b] = a

        self.scan_line_rows = list(level.get_data("scan_line_rows") or [29])
        self.scan_line_idx = 0
        self._scan_line_sprite = None
        for s in level.get_sprites_by_tag("scan_line"):
            self._scan_line_sprite = s
            break
        self._apply_scan_line_position()

        budget = int(level.get_data("step_budget") or 40)
        self.steps_remaining = budget
        self._step_counter_hud.max_steps = budget
        self._step_counter_hud.set_remaining(budget)

        self.active_column = None
        self._active_highlight_left = None
        self._active_highlight_right = None

    def _apply_scan_line_position(self) -> None:
        if self._scan_line_sprite is None:
            return
        target_y = self.scan_line_rows[self.scan_line_idx]
        self._scan_line_sprite.set_position(0, target_y)
        for marker in self.current_level.get_sprites_by_tag("scan_line_marker"):
            marker.set_position(marker.x, target_y - 1)

    def _scan_line_offset_for(self, column: Sprite) -> int:
        target_y = self.scan_line_rows[self.scan_line_idx]
        return ((target_y - column.y) // SEGMENT_HEIGHT) % SEGMENTS_PER_COLUMN

    def _shift_column(self, column: Sprite, delta: int) -> None:
        new_pos = (self.column_positions[column.name] + delta) % SEGMENTS_PER_COLUMN
        self.column_positions[column.name] = new_pos
        base = self.column_base_pixels[column.name]
        column.pixels = np.roll(base, -SEGMENT_HEIGHT * new_pos, axis=0)

    def _apply_shift(self, column: Sprite, delta: int) -> None:
        self._shift_column(column, delta)
        partner_name = self.bound_partner.get(column.name)
        if partner_name is not None:
            partners = self.current_level.get_sprites_by_name(partner_name)
            if partners:
                self._shift_column(partners[0], -delta)

    def _set_active_column(self, column: Sprite | None) -> None:
        if self._active_highlight_left is not None:
            self.current_level.remove_sprite(self._active_highlight_left)
            self._active_highlight_left = None
        if self._active_highlight_right is not None:
            self.current_level.remove_sprite(self._active_highlight_right)
            self._active_highlight_right = None
        self.active_column = column
        if column is not None:
            left = sprites["active_highlight"].clone().set_position(column.x - 1, column.y)
            right = sprites["active_highlight"].clone().set_position(column.x + COLUMN_WIDTH, column.y)
            self.current_level.add_sprite(left)
            self.current_level.add_sprite(right)
            self._active_highlight_left = left
            self._active_highlight_right = right

    def _target_colour_for_column(self, column: Sprite) -> int | None:
        col_centre_x = column.x + COLUMN_WIDTH // 2
        best: Sprite | None = None
        best_dist = 1_000
        for tgt in self.current_level.get_sprites_by_tag("target"):
            tgt_w = tgt.pixels.shape[1]
            tgt_centre_x = tgt.x + tgt_w // 2
            d = abs(col_centre_x - tgt_centre_x)
            if d < best_dist:
                best_dist = d
                best = tgt
        if best is None:
            return None
        return int(best.pixels[2, 3])

    def _check_win(self) -> bool:
        for col in self.current_level.get_sprites_by_tag("column"):
            offset = self._scan_line_offset_for(col)
            seg = (self.column_positions[col.name] + offset) % SEGMENTS_PER_COLUMN
            base = self.column_base_pixels[col.name]
            visible_colour = int(base[seg * SEGMENT_HEIGHT, 2])
            target_colour = self._target_colour_for_column(col)
            if target_colour is None or visible_colour != target_colour:
                return False
        return True

    def step(self) -> None:
        action_id = self.action.id
        if action_id == GameAction.RESET:
            self.complete_action()
            return

        self.steps_remaining = max(0, self.steps_remaining - 1)
        self._step_counter_hud.set_remaining(self.steps_remaining)

        if action_id == GameAction.ACTION6:
            x = int(self.action.data.get("x", -1))
            y = int(self.action.data.get("y", -1))
            grid_xy = self.camera.display_to_grid(x, y)
            clicked: Sprite | None = None
            if grid_xy is not None:
                gx, gy = grid_xy
                hit = self.current_level.get_sprite_at(gx, gy, tag="column")
                if hit is not None:
                    clicked = hit
            self._set_active_column(clicked)
        elif action_id in (GameAction.ACTION1, GameAction.ACTION2):
            if self.active_column is not None:
                delta = 1 if action_id == GameAction.ACTION1 else -1
                self._apply_shift(self.active_column, delta)
        elif action_id == GameAction.ACTION5:
            if len(self.scan_line_rows) > 1:
                self.scan_line_idx = (self.scan_line_idx + 1) % len(self.scan_line_rows)
                self._apply_scan_line_position()

        if self._check_win():
            self.next_level()
            self.complete_action()
            return
        if self.steps_remaining <= 0:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        h = np.zeros((4, 4), dtype=np.int16)
        h[0, 0] = self.steps_remaining
        h[0, 1] = self.scan_line_idx
        i = 0
        for col in sorted(self.column_positions.keys()):
            if i >= 4:
                break
            h[1, i] = self.column_positions[col]
            i += 1
        return h

    def _get_valid_actions(self) -> list[ActionInput]:
        valid = super()._get_valid_actions()
        if len(self.scan_line_rows) <= 1:
            valid = [a for a in valid if a.id != GameAction.ACTION5]
        return valid
