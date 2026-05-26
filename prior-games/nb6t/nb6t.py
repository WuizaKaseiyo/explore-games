"""nb6t."""

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
# Constants
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 0
PADDING_COLOR = 0

COLOR_BASE_FILL = 6
COLOR_BASE_RIM = 4
COLOR_SEGMENT_FILL = 9
COLOR_SEGMENT_RIM = 4
COLOR_HINGE_RIM = 4
COLOR_HINGE_INNER = 11
COLOR_ACTIVE_RING = 11
COLOR_TIP_FILL = 8
COLOR_TIP_RIM = 4
COLOR_TARGET_OUTER = 15
COLOR_TARGET_INNER = 0
COLOR_OBJECT_RED_FILL = 8
COLOR_OBJECT_RIM = 4
COLOR_DROP_RED_OUTER = 15
COLOR_DROP_RED_INNER = 8
COLOR_HUD_FILLED = 11
COLOR_HUD_EMPTY = 4

ANGLE_E = 0
ANGLE_N = 90
ANGLE_W = 180
ANGLE_S = 270
DIRECTION_VECTORS = {
    ANGLE_E: (1, 0),
    ANGLE_N: (0, -1),
    ANGLE_W: (-1, 0),
    ANGLE_S: (0, 1),
}

BASE_X = 16
BASE_Y = 32
N_SEGMENTS = 3
DEFAULT_LENGTH = 12
MIN_LENGTH = 1
MAX_LENGTH = 14
GRID_W = 64
GRID_H = 64
HUD_ROW = 63

SEGMENT_NAMES = ["segment_a", "segment_b", "segment_c"]
HINGE_NAMES = ["hinge_0", "hinge_1", "hinge_2"]


# ---------------------------------------------------------------------
# Pixel-array builders
# ---------------------------------------------------------------------
def _build_base_anchor_pixels():
    arr = np.full((5, 5), COLOR_BASE_FILL, dtype=np.int8)
    arr[0, :] = COLOR_BASE_RIM
    arr[-1, :] = COLOR_BASE_RIM
    arr[:, 0] = COLOR_BASE_RIM
    arr[:, -1] = COLOR_BASE_RIM
    return arr


def _build_hinge_pixels():
    arr = np.full((3, 3), -1, dtype=np.int8)
    arr[0, :] = COLOR_HINGE_RIM
    arr[-1, :] = COLOR_HINGE_RIM
    arr[:, 0] = COLOR_HINGE_RIM
    arr[:, -1] = COLOR_HINGE_RIM
    arr[1, 1] = COLOR_HINGE_INNER
    return arr


def _build_active_halo_pixels():
    arr = np.full((5, 5), -1, dtype=np.int8)
    arr[0, :] = COLOR_ACTIVE_RING
    arr[-1, :] = COLOR_ACTIVE_RING
    arr[:, 0] = COLOR_ACTIVE_RING
    arr[:, -1] = COLOR_ACTIVE_RING
    return arr


def _build_tip_marker_pixels():
    """C-shaped clamp opening to the right (default rotation 0)."""
    arr = np.full((3, 3), COLOR_TIP_FILL, dtype=np.int8)
    arr[1, 1] = -1
    arr[1, 2] = -1
    return arr


def _build_target_pad_pixels():
    arr = np.full((5, 5), COLOR_TARGET_INNER, dtype=np.int8)
    arr[0, :] = COLOR_TARGET_OUTER
    arr[-1, :] = COLOR_TARGET_OUTER
    arr[:, 0] = COLOR_TARGET_OUTER
    arr[:, -1] = COLOR_TARGET_OUTER
    return arr


def _build_object_red_pixels():
    """Plus-shaped 3x3 sprite, centered."""
    arr = np.full((3, 3), -1, dtype=np.int8)
    arr[0, 1] = COLOR_OBJECT_RED_FILL
    arr[1, 0] = COLOR_OBJECT_RED_FILL
    arr[1, 1] = COLOR_OBJECT_RED_FILL
    arr[1, 2] = COLOR_OBJECT_RED_FILL
    arr[2, 1] = COLOR_OBJECT_RED_FILL
    return arr


def _build_drop_zone_red_pixels():
    arr = np.full((5, 5), COLOR_DROP_RED_INNER, dtype=np.int8)
    arr[0, :] = COLOR_DROP_RED_OUTER
    arr[-1, :] = COLOR_DROP_RED_OUTER
    arr[:, 0] = COLOR_DROP_RED_OUTER
    arr[:, -1] = COLOR_DROP_RED_OUTER
    return arr


def _build_segment_pixels(theta, length):
    if theta in (ANGLE_E, ANGLE_W):
        h, w = 3, length
    else:
        h, w = length, 3
    arr = np.full((h, w), COLOR_SEGMENT_FILL, dtype=np.int8)
    arr[0, :] = COLOR_SEGMENT_RIM
    arr[-1, :] = COLOR_SEGMENT_RIM
    arr[:, 0] = COLOR_SEGMENT_RIM
    arr[:, -1] = COLOR_SEGMENT_RIM
    return arr


def _segment_top_left(theta, length, hinge_x, hinge_y):
    if theta == ANGLE_E:
        return (hinge_x, hinge_y - 1)
    if theta == ANGLE_W:
        return (hinge_x - length, hinge_y - 1)
    if theta == ANGLE_N:
        return (hinge_x - 1, hinge_y - length)
    if theta == ANGLE_S:
        return (hinge_x - 1, hinge_y)
    raise ValueError(theta)


# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "base_anchor": Sprite(
        pixels=_build_base_anchor_pixels().tolist(),
        name="base_anchor",
        visible=True,
        collidable=False,
        tags=["base"],
        layer=1,
    ),
    "segment_a": Sprite(
        pixels=_build_segment_pixels(ANGLE_E, DEFAULT_LENGTH).tolist(),
        name="segment_a",
        visible=True,
        collidable=False,
        tags=["segment"],
        layer=2,
    ),
    "segment_b": Sprite(
        pixels=_build_segment_pixels(ANGLE_E, DEFAULT_LENGTH).tolist(),
        name="segment_b",
        visible=True,
        collidable=False,
        tags=["segment"],
        layer=2,
    ),
    "segment_c": Sprite(
        pixels=_build_segment_pixels(ANGLE_E, DEFAULT_LENGTH).tolist(),
        name="segment_c",
        visible=True,
        collidable=False,
        tags=["segment"],
        layer=2,
    ),
    "hinge_0": Sprite(
        pixels=_build_hinge_pixels().tolist(),
        name="hinge_0",
        visible=True,
        collidable=False,
        tags=["hinge", "sys_click"],
        layer=3,
    ),
    "hinge_1": Sprite(
        pixels=_build_hinge_pixels().tolist(),
        name="hinge_1",
        visible=True,
        collidable=False,
        tags=["hinge", "sys_click"],
        layer=3,
    ),
    "hinge_2": Sprite(
        pixels=_build_hinge_pixels().tolist(),
        name="hinge_2",
        visible=True,
        collidable=False,
        tags=["hinge", "sys_click"],
        layer=3,
    ),
    "active_halo": Sprite(
        pixels=_build_active_halo_pixels().tolist(),
        name="active_halo",
        visible=True,
        collidable=False,
        tags=["active_halo"],
        layer=4,
    ),
    "tip_marker": Sprite(
        pixels=_build_tip_marker_pixels().tolist(),
        name="tip_marker",
        visible=True,
        collidable=False,
        tags=["tip", "sys_click"],
        layer=5,
        blocking=BlockingMode.BOUNDING_BOX,
    ),
    "tip_carry_halo": Sprite(
        pixels=_build_active_halo_pixels().tolist(),
        name="tip_carry_halo",
        visible=True,
        collidable=False,
        tags=["tip_carry_halo"],
        layer=4,
        interaction=InteractionMode.REMOVED,
    ),
    "target_pad": Sprite(
        pixels=_build_target_pad_pixels().tolist(),
        name="target_pad",
        visible=True,
        collidable=False,
        tags=["target"],
        layer=0,
    ),
    "object_red": Sprite(
        pixels=_build_object_red_pixels().tolist(),
        name="object_red",
        visible=True,
        collidable=False,
        tags=["object", "object_red", "sys_click"],
        layer=1,
    ),
    "drop_zone_red": Sprite(
        pixels=_build_drop_zone_red_pixels().tolist(),
        name="drop_zone_red",
        visible=True,
        collidable=False,
        tags=["drop_zone", "drop_zone_red"],
        layer=0,
    ),
}


def _level_chain_sprites():
    return [
        sprites["base_anchor"].clone().set_position(BASE_X - 2, BASE_Y - 2),
        sprites["segment_a"].clone(),
        sprites["segment_b"].clone(),
        sprites["segment_c"].clone(),
        sprites["hinge_0"].clone(),
        sprites["hinge_1"].clone(),
        sprites["hinge_2"].clone(),
        sprites["active_halo"].clone(),
        sprites["tip_marker"].clone(),
    ]


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
levels = [
    Level(
        sprites=_level_chain_sprites() + [
            sprites["target_pad"].clone().set_position(2, 6),
        ],
        grid_size=(GRID_W, GRID_H),
        data={
            "step_budget": 40,
            "target_center": (4, 8),
            "level_actions": [3, 4, 5, 6],
            "has_carry": False,
        },
    ),
    Level(
        sprites=_level_chain_sprites() + [
            sprites["target_pad"].clone().set_position(6, 6),
        ],
        grid_size=(GRID_W, GRID_H),
        data={
            "step_budget": 100,
            "target_center": (8, 8),
            "level_actions": [1, 2, 3, 4, 5, 6],
            "has_carry": False,
        },
    ),
    Level(
        sprites=_level_chain_sprites() + [
            sprites["tip_carry_halo"].clone(),
            sprites["object_red"].clone().set_position(7, 7),
            sprites["drop_zone_red"].clone().set_position(30, 18),
        ],
        grid_size=(GRID_W, GRID_H),
        data={
            "step_budget": 100,
            "object_red_center": (8, 8),
            "drop_zone_red_center": (32, 20),
            "level_actions": [1, 2, 3, 4, 5, 6],
            "has_carry": True,
        },
    ),
]


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int) -> None:
        self._max_steps = max(1, max_steps)
        self.current_steps = self._max_steps

    def set_max(self, max_steps: int) -> None:
        self._max_steps = max(1, max_steps)
        self.current_steps = self._max_steps

    def set_current(self, current: int) -> None:
        self.current_steps = max(0, min(current, self._max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        ratio = self.current_steps / self._max_steps
        filled_cells = int(round(GRID_W * ratio))
        filled_cells = max(0, min(filled_cells, GRID_W))
        for x in range(GRID_W):
            if x < filled_cells:
                frame[HUD_ROW, x] = COLOR_HUD_FILLED
            else:
                frame[HUD_ROW, x] = COLOR_HUD_EMPTY
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Nb6t(NovaBaseGame):
    def __init__(self) -> None:
        camera = Camera(background=BACKGROUND_COLOR, letter_box=PADDING_COLOR)
        self._step_counter_ui = StepCounterHud(max_steps=DEFAULT_LENGTH)
        camera.replace_interface([self._step_counter_ui])
        self._pose = [(ANGLE_E, DEFAULT_LENGTH)] * N_SEGMENTS
        self._active_hinge = 0
        self._carrying = None
        self._level_actions = [1, 2, 3, 4, 5, 6]
        self._has_carry = False
        super().__init__(
            game_id="nb6t",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )

    # ----- per-level state setup -----
    def on_set_level(self, level: Level) -> None:
        self._pose = [(ANGLE_E, DEFAULT_LENGTH)] * N_SEGMENTS
        self._active_hinge = 0
        self._carrying = None
        budget = level.get_data("step_budget") or DEFAULT_LENGTH
        self._step_counter_ui.set_max(budget)
        self._level_actions = list(level.get_data("level_actions") or [1, 2, 3, 4, 5, 6])
        self._has_carry = bool(level.get_data("has_carry"))
        self._render_chain()

    # ----- forward kinematics -----
    def _hinge_positions(self):
        positions = [(BASE_X, BASE_Y)]
        for theta, length in self._pose:
            dx, dy = DIRECTION_VECTORS[theta]
            prev = positions[-1]
            positions.append((prev[0] + length * dx, prev[1] + length * dy))
        return positions

    def _pose_in_bounds(self, pose):
        positions = [(BASE_X, BASE_Y)]
        for theta, length in pose:
            dx, dy = DIRECTION_VECTORS[theta]
            prev = positions[-1]
            for k in range(1, length + 1):
                cx = prev[0] + k * dx
                cy = prev[1] + k * dy
                if dx != 0:
                    if not (0 <= cx < GRID_W and 1 <= cy < GRID_H - 1):
                        return False
                else:
                    if not (1 <= cx < GRID_W - 1 and 0 <= cy < GRID_H):
                        return False
            positions.append((prev[0] + length * dx, prev[1] + length * dy))
            new_pos = positions[-1]
            if not (0 <= new_pos[0] < GRID_W and 0 <= new_pos[1] < GRID_H):
                return False
        return True

    def _tip_cell(self):
        return self._hinge_positions()[N_SEGMENTS]

    # ----- chain rendering -----
    def _render_chain(self) -> None:
        positions = self._hinge_positions()
        for i in range(N_SEGMENTS):
            theta, length = self._pose[i]
            seg = self.current_level.get_sprites_by_name(SEGMENT_NAMES[i])[0]
            seg.pixels = _build_segment_pixels(theta, length)
            tx, ty = _segment_top_left(theta, length, positions[i][0], positions[i][1])
            seg.set_position(tx, ty)
        for i in range(N_SEGMENTS):
            hinge = self.current_level.get_sprites_by_name(HINGE_NAMES[i])[0]
            hx, hy = positions[i]
            hinge.set_position(hx - 1, hy - 1)
        tip = self.current_level.get_sprites_by_name("tip_marker")[0]
        tx, ty = positions[N_SEGMENTS]
        tip.set_position(tx - 1, ty - 1)
        seg_last_theta = self._pose[N_SEGMENTS - 1][0]
        tip.set_rotation((360 - seg_last_theta) % 360)
        halo = self.current_level.get_sprites_by_name("active_halo")[0]
        ax, ay = positions[self._active_hinge]
        halo.set_position(ax - 2, ay - 2)
        if self._has_carry:
            carry_halos = self.current_level.get_sprites_by_name("tip_carry_halo")
            if carry_halos:
                carry_halo = carry_halos[0]
                if self._carrying is not None:
                    carry_halo.set_interaction(InteractionMode.INTANGIBLE)
                    carry_halo.set_position(tx - 2, ty - 2)
                else:
                    carry_halo.set_interaction(InteractionMode.REMOVED)
        if self._carrying is not None:
            self._carrying.set_position(tx - 1, ty - 1)

    # ----- mutation primitives -----
    def _attempt_rotate(self, delta: int) -> bool:
        theta, length = self._pose[self._active_hinge]
        new_theta = (theta + delta) % 360
        new_pose = list(self._pose)
        new_pose[self._active_hinge] = (new_theta, length)
        if not self._pose_in_bounds(new_pose):
            return False
        self._pose = new_pose
        return True

    def _attempt_length(self, delta: int) -> bool:
        theta, length = self._pose[self._active_hinge]
        new_length = length + delta
        if new_length < MIN_LENGTH or new_length > MAX_LENGTH:
            return False
        new_pose = list(self._pose)
        new_pose[self._active_hinge] = (theta, new_length)
        if not self._pose_in_bounds(new_pose):
            return False
        self._pose = new_pose
        return True

    # ----- click dispatch -----
    def _handle_click(self) -> None:
        click_x = int(self.action.data.get("x", -1))
        click_y = int(self.action.data.get("y", -1))
        if click_x < 0 or click_y < 0:
            return
        gxy = self.camera.display_to_grid(click_x, click_y)
        if gxy is None:
            return
        gx, gy = gxy
        clicked = self.current_level.get_sprite_at(gx, gy, tag="sys_click", ignore_collidable=True)
        if clicked is None:
            return
        if clicked.name.startswith("hinge_"):
            try:
                idx = int(clicked.name.split("_")[1])
                if 0 <= idx < N_SEGMENTS:
                    self._active_hinge = idx
            except (ValueError, IndexError):
                pass

    # ----- pickup detection -----
    def _check_pickup(self) -> None:
        if not self._has_carry or self._carrying is not None:
            return
        tip_x, tip_y = self._tip_cell()
        for obj in self.current_level.get_sprites_by_tag("object"):
            if obj.interaction == InteractionMode.REMOVED:
                continue
            obj_cx = obj.x + 1
            obj_cy = obj.y + 1
            if max(abs(tip_x - obj_cx), abs(tip_y - obj_cy)) <= 2:
                self._carrying = obj
                obj.set_interaction(InteractionMode.REMOVED)
                return

    # ----- auto-drop on target -----
    def _check_carry_drop(self) -> bool:
        if not self._has_carry or self._carrying is None:
            return False
        drop_center = self.current_level.get_data("drop_zone_red_center")
        if drop_center is None:
            return False
        tip_x, tip_y = self._tip_cell()
        if max(abs(tip_x - drop_center[0]), abs(tip_y - drop_center[1])) <= 2:
            self._carrying.set_position(drop_center[0] - 1, drop_center[1] - 1)
            self._carrying.set_interaction(InteractionMode.TANGIBLE)
            self._carrying = None
            self.next_level()
            return True
        return False

    # ----- HUD update -----
    def _update_hud(self) -> None:
        budget = self.current_level.get_data("step_budget") or DEFAULT_LENGTH
        self._step_counter_ui.set_current(budget - self._action_count)

    # ----- win/lose -----
    def _check_win(self) -> bool:
        if self._has_carry:
            return False
        target_center = self.current_level.get_data("target_center")
        if target_center is not None:
            tip_x, tip_y = self._tip_cell()
            if tip_x == target_center[0] and tip_y == target_center[1]:
                self.next_level()
                return True
        return False

    def _check_lose(self) -> bool:
        budget = self.current_level.get_data("step_budget") or DEFAULT_LENGTH
        if self._action_count >= budget:
            self.lose()
            return True
        return False

    # ----- main step dispatch -----
    def step(self) -> None:
        if self.action.id == GameAction.ACTION1:
            if 1 in self._level_actions:
                self._attempt_length(+1)
        elif self.action.id == GameAction.ACTION2:
            if 2 in self._level_actions:
                self._attempt_length(-1)
        elif self.action.id == GameAction.ACTION3:
            if 3 in self._level_actions:
                self._attempt_rotate(+90)
        elif self.action.id == GameAction.ACTION4:
            if 4 in self._level_actions:
                self._attempt_rotate(-90)
        elif self.action.id == GameAction.ACTION5:
            if 5 in self._level_actions:
                self._active_hinge = (self._active_hinge + 1) % N_SEGMENTS
        elif self.action.id == GameAction.ACTION6:
            if 6 in self._level_actions:
                self._handle_click()
        self._check_pickup()
        won = self._check_carry_drop()
        self._render_chain()
        self._update_hud()
        if won or self._check_win():
            self.complete_action()
            return
        self._check_lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._action_count
        state[0, 1] = self._active_hinge
        state[0, 2] = 1 if self._carrying is not None else 0
        for i in range(N_SEGMENTS):
            theta, length = self._pose[i]
            state[1 + i, 0] = theta
            state[1 + i, 1] = length
        return state

    def _get_valid_actions(self):
        return [ActionInput(id=GameAction.from_id(a)) for a in self._level_actions]
