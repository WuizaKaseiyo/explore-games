"""."""

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
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "socket": Sprite(
        pixels=[
            [14, 14, 14, 14, 14],
            [14, -1, -1, -1, 14],
            [14, -1, -1, -1, 14],
            [14, -1, -1, -1, 14],
            [14, 14, 14, 14, 14],
        ],
        name="socket",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["socket"],
        layer=1,
    ),
    "lock_mark": Sprite(
        pixels=[
            [5, -1, 5],
            [-1, -1, -1],
            [5, -1, 5],
        ],
        name="lock_mark",
        visible=True,
        collidable=False,
        interaction=InteractionMode.REMOVED,
        tags=["lock_mark"],
        layer=4,
    ),
    "tip": Sprite(
        pixels=[
            [8, 8, 8],
            [8, 8, 8],
            [8, 8, 8],
        ],
        name="tip",
        visible=True,
        collidable=True,
        tags=["tip", "sys_click"],
        layer=3,
    ),
    "hub": Sprite(
        pixels=[
            [3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3],
        ],
        name="hub",
        visible=True,
        collidable=False,
        tags=["hub"],
        layer=2,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
SLOT_CENTERS = [
    (32, 10),  # 0  top
    (47, 17),  # 1
    (54, 32),  # 2  right
    (47, 47),  # 3
    (32, 54),  # 4  bottom
    (17, 47),  # 5
    (10, 32),  # 6  left
    (17, 17),  # 7
]


def _tip_at(slot_idx, color):
    cx, cy = SLOT_CENTERS[slot_idx]
    return (
        sprites["tip"]
        .clone()
        .color_remap(None, color)
        .set_position(cx - 1, cy - 1)
    )


def _socket_at(slot_idx, color):
    cx, cy = SLOT_CENTERS[slot_idx]
    return (
        sprites["socket"]
        .clone()
        .color_remap(None, color)
        .set_position(cx - 2, cy - 2)
    )


def _hub():
    return sprites["hub"].clone().set_position(30, 30)


levels = [
    # Level 1
    Level(
        sprites=[
            _hub(),
            _tip_at(0, 12),
            _tip_at(2, 14),
            _tip_at(4, 15),
            _socket_at(2, 12),
            _socket_at(4, 14),
            _socket_at(6, 15),
        ],
        grid_size=(64, 64),
        data={
            "StepCounter": 16,
        },
    ),
    # Level 2
    Level(
        sprites=[
            _hub(),
            _tip_at(0, 12),
            _tip_at(3, 14),
            _tip_at(6, 15),
            _socket_at(1, 12),
            _socket_at(4, 14),
            _socket_at(6, 15),
        ],
        grid_size=(64, 64),
        data={
            "StepCounter": 18,
        },
    ),
    # Level 3
    Level(
        sprites=[
            _hub(),
            _tip_at(0, 12),
            _tip_at(1, 14),
            _tip_at(2, 15),
            _tip_at(5, 6),
            _tip_at(7, 11),
            _socket_at(0, 11),
            _socket_at(2, 12),
            _socket_at(3, 14),
            _socket_at(5, 6),
            _socket_at(6, 15),
        ],
        grid_size=(64, 64),
        data={
            "StepCounter": 32,
        },
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 2
PADDING_COLOR = 3
BAR_LEFT = 8
BAR_WIDTH = 48
BAR_ROW = 63
BAR_FILL_COLOR = 12
BAR_BG_COLOR = 3


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepBarHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def reset(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_current(self, val: int) -> None:
        self.current_steps = max(0, min(val, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.current_steps / self.max_steps
        filled = round(BAR_WIDTH * ratio)
        for x in range(BAR_WIDTH):
            frame[BAR_ROW, BAR_LEFT + x] = (
                BAR_FILL_COLOR if x < filled else BAR_BG_COLOR
            )
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Qz73(NovaBaseGame):
    def __init__(self) -> None:
        self.step_bar = StepBarHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_bar],
        )
        self.tips: list[Sprite] = []
        self.sockets: list[Sprite] = []
        self.tip_slot: dict[Sprite, int] = {}
        self.tip_locked: dict[Sprite, bool] = {}
        self.lock_marks: dict[Sprite, Sprite] = {}
        self.socket_slot: dict[Sprite, int] = {}
        self.socket_color: dict[Sprite, int] = {}
        self.max_steps = 0
        self.steps_used = 0
        super().__init__(
            game_id="qz73",
            levels=levels,
            camera=camera,
            available_actions=[5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        self.max_steps = level.get_data("StepCounter") or 32
        self.step_bar.reset(self.max_steps)
        self.steps_used = 0
        self.tips = list(level.get_sprites_by_tag("tip"))
        self.sockets = list(level.get_sprites_by_tag("socket"))
        self.tip_slot = {}
        self.tip_locked = {}
        self.lock_marks = {}
        self.socket_slot = {}
        self.socket_color = {}
        for tip in self.tips:
            self.tip_slot[tip] = self._slot_for_tip(tip)
            self.tip_locked[tip] = False
            mark = sprites["lock_mark"].clone()
            cx, cy = SLOT_CENTERS[self.tip_slot[tip]]
            mark.set_position(cx - 1, cy - 1)
            mark.set_interaction(InteractionMode.REMOVED)
            level.add_sprite(mark)
            self.lock_marks[tip] = mark
        for socket in self.sockets:
            self.socket_slot[socket] = self._slot_for_socket(socket)
            self.socket_color[socket] = int(socket.pixels[0, 0])

    def _slot_for_tip(self, sprite: Sprite) -> int:
        for idx, (cx, cy) in enumerate(SLOT_CENTERS):
            if sprite.x == cx - 1 and sprite.y == cy - 1:
                return idx
        return 0

    def _slot_for_socket(self, sprite: Sprite) -> int:
        for idx, (cx, cy) in enumerate(SLOT_CENTERS):
            if sprite.x == cx - 2 and sprite.y == cy - 2:
                return idx
        return 0

    def _set_tip_position(self, tip: Sprite, slot_idx: int) -> None:
        cx, cy = SLOT_CENTERS[slot_idx]
        tip.set_position(cx - 1, cy - 1)
        mark = self.lock_marks.get(tip)
        if mark is not None:
            mark.set_position(cx - 1, cy - 1)

    def _rotate_unlocked(self) -> None:
        locked_slots = {
            self.tip_slot[t] for t in self.tips if self.tip_locked[t]
        }
        # Two-pass: compute new positions, then commit atomically.
        proposed: dict[Sprite, int] = {}
        for tip in self.tips:
            if self.tip_locked[tip]:
                continue
            cur = self.tip_slot[tip]
            new = cur
            for offset in range(1, len(SLOT_CENTERS) + 1):
                cand = (cur + offset) % len(SLOT_CENTERS)
                if cand not in locked_slots:
                    new = cand
                    break
            proposed[tip] = new
        for tip, new_slot in proposed.items():
            self.tip_slot[tip] = new_slot
            self._set_tip_position(tip, new_slot)

    def _toggle_lock(self, tip: Sprite) -> None:
        new_state = not self.tip_locked[tip]
        self.tip_locked[tip] = new_state
        mark = self.lock_marks[tip]
        mark.set_interaction(
            InteractionMode.INTANGIBLE if new_state else InteractionMode.REMOVED
        )

    def _check_win(self) -> bool:
        for socket in self.sockets:
            sk_slot = self.socket_slot[socket]
            sk_color = self.socket_color[socket]
            matched = False
            for tip in self.tips:
                if self.tip_slot[tip] == sk_slot:
                    tip_color = int(tip.pixels[1, 1])
                    if tip_color == sk_color:
                        matched = True
                    break
            if not matched:
                return False
        return True

    def _refresh_bar(self) -> None:
        self.step_bar.set_current(self.max_steps - self.steps_used)

    def step(self) -> None:
        self._refresh_bar()
        if self.steps_used >= self.max_steps:
            self.lose()
            self.complete_action()
            return

        if self.action.id == GameAction.ACTION5:
            self._rotate_unlocked()
            self.steps_used += 1
            self._refresh_bar()
            if self._check_win():
                self.next_level()
                self.complete_action()
                return
            if self.steps_used >= self.max_steps:
                self.lose()
            self.complete_action()
            return

        if self.action.id == GameAction.ACTION6:
            data = self.action.data or {}
            ax = int(data.get("x", -1))
            ay = int(data.get("y", -1))
            grid_pt = self.camera.display_to_grid(ax, ay)
            if grid_pt is None:
                self.complete_action()
                return
            gx, gy = grid_pt
            target = self.current_level.get_sprite_at(gx, gy, "tip")
            if target is not None and target in self.tips:
                self._toggle_lock(target)
                self.steps_used += 1
                self._refresh_bar()
                if self._check_win():
                    self.next_level()
                    self.complete_action()
                    return
                if self.steps_used >= self.max_steps:
                    self.lose()
            self.complete_action()
            return

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        n = max(1, len(self.tips))
        out = np.full((2, n), -1, dtype=np.int16)
        for i, tip in enumerate(self.tips):
            out[0, i] = self.tip_slot[tip]
            out[1, i] = 1 if self.tip_locked[tip] else 0
        return out

    def _get_valid_actions(self) -> list[ActionInput]:
        actions: list[ActionInput] = [ActionInput(id=GameAction.ACTION5)]
        for tip in self.tips:
            cx, cy = SLOT_CENTERS[self.tip_slot[tip]]
            actions.append(
                ActionInput(
                    id=GameAction.ACTION6,
                    data={"x": cx, "y": cy},
                )
            )
        return actions
