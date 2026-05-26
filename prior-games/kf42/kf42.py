"""."""

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
sprites = {
    "floor": Sprite(
        pixels=[[5]],
        name="floor",
        visible=True,
        collidable=False,
        layer=0,
    ),
    "wall": Sprite(
        pixels=[[4]],
        name="wall",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=1,
    ),
    "target_pad": Sprite(
        pixels=[
            [-1, 8, -1],
            [8, -1, 8],
            [-1, 8, -1],
        ],
        name="target_pad",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target"],
        layer=2,
    ),
    "pawn": Sprite(
        pixels=[[8]],
        name="pawn",
        visible=True,
        collidable=True,
        blocking=BlockingMode.NOT_BLOCKED,
        tags=["pawn", "sys_click"],
        layer=4,
    ),
    "cycler_pad": Sprite(
        pixels=[
            [8, 8, 8],
            [8, 8, 8],
            [8, 8, 8],
        ],
        name="cycler_pad",
        visible=True,
        collidable=False,
        blocking=BlockingMode.NOT_BLOCKED,
        interaction=InteractionMode.INTANGIBLE,
        tags=["cycler"],
        layer=2,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
def _border_walls(w, h):
    out = []
    for x in range(w):
        out.append(sprites["wall"].clone().set_position(x, 0))
        out.append(sprites["wall"].clone().set_position(x, h - 1))
    for y in range(1, h - 1):
        out.append(sprites["wall"].clone().set_position(0, y))
        out.append(sprites["wall"].clone().set_position(w - 1, y))
    return out


def _level1_sprites():
    out = list(_border_walls(12, 12))
    out.append(
        sprites["target_pad"].clone().color_remap(None, 8).set_position(8, 5)
    )
    out.append(
        sprites["target_pad"].clone().color_remap(None, 9).set_position(7, 5)
    )
    out.append(
        sprites["pawn"].clone().color_remap(None, 8).set_position(2, 6)
    )
    out.append(
        sprites["pawn"].clone().color_remap(None, 9).set_position(3, 6)
    )
    return out


def _level2_sprites():
    out = list(_border_walls(14, 14))
    for ry in (4, 5, 6):
        out.append(sprites["wall"].clone().set_position(7, ry))
    out.append(
        sprites["cycler_pad"].clone().color_remap(None, 9).set_position(6, 8)
    )
    out.append(
        sprites["target_pad"].clone().color_remap(None, 8).set_position(10, 4)
    )
    out.append(
        sprites["target_pad"].clone().color_remap(None, 9).set_position(10, 8)
    )
    out.append(
        sprites["pawn"].clone().color_remap(None, 8).set_position(2, 7)
    )
    out.append(
        sprites["pawn"].clone().color_remap(None, 8).set_position(3, 7)
    )
    return out


def _level3_sprites():
    out = list(_border_walls(16, 16))
    for cx in (4, 5, 6, 9, 10, 11):
        out.append(sprites["wall"].clone().set_position(cx, 8))
    for ry in (5, 6, 10, 11, 12):
        out.append(sprites["wall"].clone().set_position(7, ry))
    out.append(
        sprites["cycler_pad"].clone().color_remap(None, 8).set_position(6, 4)
    )
    out.append(
        sprites["cycler_pad"].clone().color_remap(None, 9).set_position(6, 11)
    )
    out.append(
        sprites["target_pad"].clone().color_remap(None, 9).set_position(12, 4)
    )
    out.append(
        sprites["target_pad"].clone().color_remap(None, 8).set_position(12, 11)
    )
    out.append(
        sprites["pawn"].clone().color_remap(None, 8).set_position(2, 13)
    )
    out.append(
        sprites["pawn"].clone().color_remap(None, 8).set_position(2, 14)
    )
    return out


levels = [
    Level(
        sprites=_level1_sprites(),
        grid_size=(12, 12),
        data={"StepCounter": 30, "Tether": 4},
    ),
    Level(
        sprites=_level2_sprites(),
        grid_size=(14, 14),
        data={"StepCounter": 50, "Tether": 5},
    ),
    Level(
        sprites=_level3_sprites(),
        grid_size=(16, 16),
        data={"StepCounter": 80, "Tether": 7},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 5
PADDING_COLOR = 5
HUD_FILLED_COLOR = 6
HUD_EMPTY_COLOR = 0
SELECT_RING_COLOR = 11
ALPHABET = (8, 9, 11)


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class StepBarHud(RenderableUserDisplay):
    """."""

    def __init__(self) -> None:
        self.max_steps = 0
        self.current_steps = 0

    def reset(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_current(self, n: int) -> None:
        self.current_steps = max(0, min(n, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.current_steps / self.max_steps
        filled = int(round(64 * ratio))
        for x in range(64):
            frame[63, x] = HUD_FILLED_COLOR if x < filled else HUD_EMPTY_COLOR
        return frame


class ActiveMarkerHud(RenderableUserDisplay):
    """."""

    def __init__(self, game: "Kf42") -> None:
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        pawn = self.game.active_pawn
        if pawn is None:
            return frame
        gw, gh = self.game.current_level.grid_size or (64, 64)
        scale = max(1, min(64 // gw, 64 // gh))
        ox = (64 - gw * scale) // 2
        oy = (64 - gh * scale) // 2
        x0 = pawn.x * scale + ox
        y0 = pawn.y * scale + oy
        x1 = x0 + scale - 1
        y1 = y0 + scale - 1
        for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            if 0 <= cx < 64 and 0 <= cy < 64:
                frame[cy, cx] = SELECT_RING_COLOR
        return frame


# ---------------------------------------------------------------------
# 5. GAME CLASS
# ---------------------------------------------------------------------
class Kf42(NovaBaseGame):
    pawns: list[Sprite]
    active_pawn: Sprite | None
    tether_length: int
    target_pads: list[Sprite]
    cycler_pads: list[Sprite]
    max_steps: int
    step_bar: StepBarHud

    def __init__(self) -> None:
        self.pawns = []
        self.active_pawn = None
        self.tether_length = 0
        self.target_pads = []
        self.cycler_pads = []
        self.max_steps = 0
        self.step_bar = StepBarHud()
        self.active_marker = ActiveMarkerHud(self)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_bar, self.active_marker],
        )
        super().__init__(
            game_id="kf42",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        self.active_pawn = None
        self.tether_length = int(level.get_data("Tether") or 4)
        self.max_steps = int(level.get_data("StepCounter") or 30)
        self.step_bar.reset(self.max_steps)
        ps = level.get_sprites_by_tag("pawn")
        ps.sort(key=lambda s: (s.y, s.x))
        self.pawns = ps
        self.target_pads = level.get_sprites_by_tag("target")
        self.cycler_pads = level.get_sprites_by_tag("cycler")

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((2, 2), dtype=np.int16)
        if self.active_pawn is None or not self.pawns:
            out[0, 0] = -1
        else:
            try:
                out[0, 0] = self.pawns.index(self.active_pawn)
            except ValueError:
                out[0, 0] = -1
        out[0, 1] = self.step_bar.current_steps
        for i in range(min(2, len(self.pawns))):
            out[1, i] = int(self.pawns[i].pixels[0, 0])
        return out

    def _get_valid_actions(self) -> list[ActionInput]:
        out: list[ActionInput] = []
        gw, gh = self.current_level.grid_size or (64, 64)
        scale = max(1, min(64 // gw, 64 // gh))
        ox = (64 - gw * scale) // 2
        oy = (64 - gh * scale) // 2
        for pawn in self.pawns:
            cx = pawn.x * scale + ox + scale // 2
            cy = pawn.y * scale + oy + scale // 2
            out.append(
                ActionInput(
                    id=GameAction.ACTION6, data={"x": cx, "y": cy}
                )
            )
        if self.active_pawn is not None:
            for aid in (
                GameAction.ACTION1,
                GameAction.ACTION2,
                GameAction.ACTION3,
                GameAction.ACTION4,
            ):
                out.append(ActionInput(id=aid))
        return out

    def _wall_at(self, x: int, y: int) -> bool:
        gw, gh = self.current_level.grid_size or (64, 64)
        if x < 0 or y < 0 or x >= gw or y >= gh:
            return True
        return self.current_level.get_sprite_at(x, y, tag="wall") is not None

    def _apply_cycler(self, pawn: Sprite) -> None:
        pad = self.current_level.get_sprite_at(
            pawn.x, pawn.y, tag="cycler", ignore_collidable=True
        )
        if pad is None:
            return
        target_color = int(pad.pixels[0, 0])
        if pawn.pixels[0, 0] != target_color:
            pawn.color_remap(None, target_color)

    def _try_move_active(self, dx: int, dy: int) -> None:
        if self.active_pawn is None:
            return
        active = self.active_pawn
        other = self.pawns[1] if self.pawns[0] is active else self.pawns[0]
        new_x = active.x + dx
        new_y = active.y + dy
        if self._wall_at(new_x, new_y):
            return
        cheby_after = max(abs(new_x - other.x), abs(new_y - other.y))
        if cheby_after > self.tether_length:
            ddx = 0 if new_x == other.x else (1 if new_x > other.x else -1)
            ddy = 0 if new_y == other.y else (1 if new_y > other.y else -1)
            other_new_x = other.x + ddx
            other_new_y = other.y + ddy
            if self._wall_at(other_new_x, other_new_y):
                return
            other.set_position(other_new_x, other_new_y)
        active.set_position(new_x, new_y)
        self._apply_cycler(active)

    def _check_win(self) -> bool:
        if len(self.pawns) != 2 or len(self.target_pads) != 2:
            return False
        a, b = self.pawns
        for permutation in ((0, 1), (1, 0)):
            ok = True
            for pawn_index, pad_index in enumerate(permutation):
                p = self.pawns[pawn_index]
                pad = self.target_pads[pad_index]
                cx, cy = pad.x + 1, pad.y + 1
                if p.x != cx or p.y != cy:
                    ok = False
                    break
                pad_color = int(pad.pixels[0, 1])
                pawn_color = int(p.pixels[0, 0])
                if pawn_color != pad_color:
                    ok = False
                    break
            if ok:
                return True
        return False

    def step(self) -> None:
        remaining = self.max_steps - self._action_count
        self.step_bar.set_current(remaining)
        if self._action_count > self.max_steps:
            self.lose()
            self.complete_action()
            return
        aid = self.action.id
        if aid == GameAction.ACTION6:
            x = self.action.data.get("x", -1)
            y = self.action.data.get("y", -1)
            grid = self.camera.display_to_grid(int(x), int(y))
            if grid is not None:
                gx, gy = grid
                target = self.current_level.get_sprite_at(gx, gy, tag="pawn")
                if target is not None:
                    self.active_pawn = target
        elif aid == GameAction.ACTION1:
            self._try_move_active(0, -1)
        elif aid == GameAction.ACTION2:
            self._try_move_active(0, 1)
        elif aid == GameAction.ACTION3:
            self._try_move_active(-1, 0)
        elif aid == GameAction.ACTION4:
            self._try_move_active(1, 0)
        if self._check_win():
            self.next_level()
            self.complete_action()
            return
        if (self.max_steps - (self._action_count + 1)) <= 0:
            self.step_bar.set_current(0)
            self.lose()
        self.complete_action()
