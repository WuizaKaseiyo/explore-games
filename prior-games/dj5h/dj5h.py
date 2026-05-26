"""dj5h."""

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
# 0. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 1   # off-white sky behind the playfield
PADDING_COLOR = 1
BEAM_GREY = 3
BEAM_DARK = 4
RIVET_YELLOW = 11
WHEEL_RING = 4
WHEEL_SPOKE = 11
WHEEL_HUB = 13
HALO_COLOR = 12
ROPE_COLOR = 4

FLOOR_BODY = 2
FLOOR_HIGHLIGHT = 1
FLOOR_SHADOW = 3

PIT_DARK = 5
PIT_HATCH = 4

WALL_BODY = 5
WALL_EDGE = 4
WALL_STRIPE = 13
WALL_RIVET = 3

PLATFORM_TOP = 13       # maroon top edge
PLATFORM_RED = 8
PLATFORM_BLUE = 9
PLATFORM_GREEN = 14
PLATFORM_PIP_RED = 1
PLATFORM_PIP_BLUE = 10
PLATFORM_PIP_GREEN = 1

AVATAR_HEAD = 1
AVATAR_BODY = 6
AVATAR_FEET = 4

PEG_RED_BODY = 8
PEG_BLUE_BODY = 9
PEG_GREEN_BODY = 14
PEG_RED_RIM = 13
PEG_BLUE_RIM = 10
PEG_GREEN_RIM = 1
PEG_OUTLINE = 4

SOCKET_RING = 13
SOCKET_CORNER = 3
SOCKET_CENTER = 4

GOAL_OUTER = 11
GOAL_MIDDLE = 4
GOAL_CENTER = 11

CABLE_COLOR = 12

HUD_FILL = 12
HUD_EMPTY = 4

# Geometry
GRID_W = 64
GRID_H = 64
WHEEL_SIZE = 5            # 5×5 spoked wheel
PLATFORM_W = 7
PLATFORM_H = 2
HIGH_Y = 14               # platform.y when HIGH
LOW_Y = 56                # platform.y when LOW (top row at row 56)
FLOOR_TOP = 56            # top row of floor tiles
AVATAR_W = 3
AVATAR_H = 3
WALK_STEP = 4             # pixels per arrow press

# avatar.y when standing on a surface whose top row is `top`:
#   avatar bottom row = top - 1, so avatar.y = top - AVATAR_H = top - 3.

LEFT_HIGH = "LEFT_HIGH"
LEFT_LOW = "LEFT_LOW"


def _flip(state: str) -> str:
    return LEFT_LOW if state == LEFT_HIGH else LEFT_HIGH


# ---------------------------------------------------------------------
# 1. SPRITE BANK (helpers + dict)
# ---------------------------------------------------------------------
def _beam_pixels() -> list:
    row0 = [BEAM_GREY] * GRID_W
    row1 = []
    for x in range(GRID_W):
        if x % 8 == 4:
            row1.append(RIVET_YELLOW)
        else:
            row1.append(BEAM_DARK)
    row2 = [BEAM_GREY] * GRID_W
    return [row0, row1, row2]


def _wheel_pixels() -> list:
    # 5×5 spoked wheel: outer ring palette 4, plus '+'-spokes palette 11, hub palette 13.
    p = [
        [WHEEL_RING, WHEEL_RING, WHEEL_SPOKE, WHEEL_RING, WHEEL_RING],
        [WHEEL_RING, WHEEL_RING, WHEEL_SPOKE, WHEEL_RING, WHEEL_RING],
        [WHEEL_SPOKE, WHEEL_SPOKE, WHEEL_HUB, WHEEL_SPOKE, WHEEL_SPOKE],
        [WHEEL_RING, WHEEL_RING, WHEEL_SPOKE, WHEEL_RING, WHEEL_RING],
        [WHEEL_RING, WHEEL_RING, WHEEL_SPOKE, WHEEL_RING, WHEEL_RING],
    ]
    return p


def _halo_pixels() -> list:
    # 7×7 ring border, transparent interior.
    p = []
    for r in range(7):
        row = []
        for c in range(7):
            if r == 0 or r == 6 or c == 0 or c == 6:
                row.append(HALO_COLOR)
            else:
                row.append(-1)
        p.append(row)
    return p


def _platform_pixels(body: int, pip: int) -> list:
    top = [PLATFORM_TOP] * PLATFORM_W
    bot = [body] * PLATFORM_W
    bot[1] = pip
    bot[3] = pip
    bot[5] = pip
    return [top, bot]


def _floor_pixels() -> list:
    # 4×4 floor tile.
    return [
        [FLOOR_HIGHLIGHT, FLOOR_BODY, FLOOR_HIGHLIGHT, FLOOR_SHADOW],
        [FLOOR_BODY, FLOOR_BODY, FLOOR_BODY, FLOOR_SHADOW],
        [FLOOR_BODY, FLOOR_BODY, FLOOR_BODY, FLOOR_SHADOW],
        [FLOOR_BODY, FLOOR_BODY, FLOOR_BODY, FLOOR_SHADOW],
    ]


def _wall_pixels() -> list:
    # 4×8 wall.
    rows = []
    for r in range(8):
        row = [WALL_EDGE, WALL_BODY, WALL_BODY, WALL_RIVET]
        if r % 3 == 0:
            row[1] = WALL_STRIPE
            row[2] = WALL_STRIPE
        rows.append(row)
    return rows


def _avatar_pixels(head: int) -> list:
    return [
        [-1, head, -1],
        [AVATAR_BODY, AVATAR_BODY, AVATAR_BODY],
        [AVATAR_FEET, -1, AVATAR_FEET],
    ]


def _peg_pixels(body: int, rim: int) -> list:
    return [
        [PEG_OUTLINE, rim, PEG_OUTLINE],
        [rim, body, rim],
        [PEG_OUTLINE, rim, PEG_OUTLINE],
    ]


def _peg_seated_pixels(body: int, rim: int) -> list:
    return [
        [PEG_OUTLINE, rim, PEG_OUTLINE],
        [rim, body, rim],
        [PEG_OUTLINE, PEG_OUTLINE, PEG_OUTLINE],
    ]


def _socket_pixels() -> list:
    return [
        [SOCKET_CORNER, SOCKET_RING, SOCKET_CORNER],
        [SOCKET_RING, SOCKET_CENTER, SOCKET_RING],
        [SOCKET_CORNER, SOCKET_RING, SOCKET_CORNER],
    ]


def _goal_pixels() -> list:
    return [
        [GOAL_OUTER, GOAL_OUTER, GOAL_OUTER],
        [GOAL_OUTER, GOAL_MIDDLE, GOAL_OUTER],
        [GOAL_OUTER, GOAL_OUTER, GOAL_OUTER],
    ]


def _rope_pixels(length: int) -> list:
    return [[ROPE_COLOR] for _ in range(length)]


def _cable_segment_pixels() -> list:
    return [[CABLE_COLOR]]


sprites = {
    "beam": Sprite(
        pixels=_beam_pixels(),
        name="beam",
        tags=["beam", "decor"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=0,
    ),
    "pulley_wheel": Sprite(
        pixels=_wheel_pixels(),
        name="pulley_wheel",
        tags=["pulley_wheel", "sys_click"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=4,
    ),
    "pulley_halo": Sprite(
        pixels=_halo_pixels(),
        name="pulley_halo",
        tags=["pulley_halo"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=3,
    ),
    "platform_red": Sprite(
        pixels=_platform_pixels(PLATFORM_RED, PLATFORM_PIP_RED),
        name="platform_red",
        tags=["platform", "platform_red"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=2,
    ),
    "platform_blue": Sprite(
        pixels=_platform_pixels(PLATFORM_BLUE, PLATFORM_PIP_BLUE),
        name="platform_blue",
        tags=["platform", "platform_blue"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=2,
    ),
    "platform_green": Sprite(
        pixels=_platform_pixels(PLATFORM_GREEN, PLATFORM_PIP_GREEN),
        name="platform_green",
        tags=["platform", "platform_green"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=2,
    ),
    "floor_block": Sprite(
        pixels=_floor_pixels(),
        name="floor_block",
        tags=["floor"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=1,
    ),
    "wall_block": Sprite(
        pixels=_wall_pixels(),
        name="wall_block",
        tags=["wall"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=2,
    ),
    "avatar": Sprite(
        pixels=_avatar_pixels(AVATAR_HEAD),
        name="avatar",
        tags=["avatar", "avatar_main"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=5,
    ),
    "avatar_carry_red": Sprite(
        pixels=_avatar_pixels(PEG_RED_BODY),
        name="avatar_carry_red",
        tags=["avatar", "avatar_carry"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=5,
    ),
    "avatar_carry_blue": Sprite(
        pixels=_avatar_pixels(PEG_BLUE_BODY),
        name="avatar_carry_blue",
        tags=["avatar", "avatar_carry"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=5,
    ),
    "avatar_carry_green": Sprite(
        pixels=_avatar_pixels(PEG_GREEN_BODY),
        name="avatar_carry_green",
        tags=["avatar", "avatar_carry"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=5,
    ),
    "peg_red": Sprite(
        pixels=_peg_pixels(PEG_RED_BODY, PEG_RED_RIM),
        name="peg_red",
        tags=["peg", "peg_red"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=4,
    ),
    "peg_blue": Sprite(
        pixels=_peg_pixels(PEG_BLUE_BODY, PEG_BLUE_RIM),
        name="peg_blue",
        tags=["peg", "peg_blue"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=4,
    ),
    "peg_green": Sprite(
        pixels=_peg_pixels(PEG_GREEN_BODY, PEG_GREEN_RIM),
        name="peg_green",
        tags=["peg", "peg_green"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=4,
    ),
    "peg_seated_red": Sprite(
        pixels=_peg_seated_pixels(PEG_RED_BODY, PEG_RED_RIM),
        name="peg_seated_red",
        tags=["peg_seated"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=4,
    ),
    "peg_seated_blue": Sprite(
        pixels=_peg_seated_pixels(PEG_BLUE_BODY, PEG_BLUE_RIM),
        name="peg_seated_blue",
        tags=["peg_seated"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=4,
    ),
    "peg_seated_green": Sprite(
        pixels=_peg_seated_pixels(PEG_GREEN_BODY, PEG_GREEN_RIM),
        name="peg_seated_green",
        tags=["peg_seated"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=4,
    ),
    "socket": Sprite(
        pixels=_socket_pixels(),
        name="socket",
        tags=["socket"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=2,
    ),
    "goal_marker": Sprite(
        pixels=_goal_pixels(),
        name="goal_marker",
        tags=["goal"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=2,
    ),
    "cable_segment": Sprite(
        pixels=_cable_segment_pixels(),
        name="cable_segment",
        tags=["cable"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=3,
    ),
    "rope_short": Sprite(
        pixels=_rope_pixels(2),
        name="rope_short",
        tags=["rope"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=2,
    ),
    "rope_long": Sprite(
        pixels=_rope_pixels(44),
        name="rope_long",
        tags=["rope"],
        blocking=BlockingMode.NOT_BLOCKED,
        layer=2,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVEL BUILDER HELPERS
# ---------------------------------------------------------------------
def _floor_strip(x_start: int, x_end_exclusive: int, y: int) -> list:
    out = []
    x = x_start
    while x < x_end_exclusive:
        out.append(sprites["floor_block"].clone(new_name=f"floor_{x}_{y}").set_position(x, y))
        x += 4
    return out


def _make_pulley(name: str, wheel_x: int, wheel_y: int,
                 left_color: str, right_color: str, initial_state: str) -> list:
    placed = []
    placed.append(
        sprites["pulley_wheel"].clone(new_name=f"{name}_wheel").set_position(wheel_x, wheel_y)
    )
    halo = sprites["pulley_halo"].clone(new_name=f"{name}_halo").set_position(wheel_x - 1, wheel_y - 1)
    halo.set_interaction(InteractionMode.REMOVED)
    placed.append(halo)
    # platforms
    if initial_state == LEFT_HIGH:
        left_y, right_y = HIGH_Y, LOW_Y
    else:
        left_y, right_y = LOW_Y, HIGH_Y
    # Platform centred on rope. Left rope at wheel.x; right rope at wheel.x+4.
    # PLATFORM_W=7 → platform_x = rope - 3.
    left_x = wheel_x - 3
    right_x = wheel_x + 1
    placed.append(
        sprites[f"platform_{left_color}"].clone(new_name=f"{name}_left").set_position(left_x, left_y)
    )
    placed.append(
        sprites[f"platform_{right_color}"].clone(new_name=f"{name}_right").set_position(right_x, right_y)
    )
    # ropes (decorative, repositioned at runtime)
    rope_left = sprites["rope_long"].clone(new_name=f"{name}_left_rope").set_position(wheel_x, wheel_y + WHEEL_SIZE)
    rope_right = sprites["rope_long"].clone(new_name=f"{name}_right_rope").set_position(wheel_x + 4, wheel_y + WHEEL_SIZE)
    placed.append(rope_left)
    placed.append(rope_right)
    return placed


def _make_avatars(start_x: int, start_y: int) -> list:
    avs = []
    avs.append(sprites["avatar"].clone(new_name="avatar").set_position(start_x, start_y))
    for color in ("red", "blue", "green"):
        ac = sprites[f"avatar_carry_{color}"].clone(new_name=f"avatar_carry_{color}").set_position(start_x, start_y)
        ac.set_interaction(InteractionMode.REMOVED)
        avs.append(ac)
    return avs


def _make_cable(pulley_a_wheel_x: int, pulley_b_wheel_x: int, beam_y: int) -> list:
    out = []
    x_start = min(pulley_a_wheel_x, pulley_b_wheel_x) + WHEEL_SIZE - 1
    x_end = max(pulley_a_wheel_x, pulley_b_wheel_x)
    y = beam_y - 1
    for i, x in enumerate(range(x_start, x_end)):
        seg = sprites["cable_segment"].clone(new_name=f"cable_{i}").set_position(x, y)
        out.append(seg)
    return out


# ---------------------------------------------------------------------
# 3. LEVEL DEFINITIONS
# ---------------------------------------------------------------------
def _level_1() -> Level:
    # Right-side ground is ELEVATED to the HIGH altitude (top row at row 14).
    # The avatar boards the LOW platform after a toggle, rides up with a second
    # toggle, and walks RIGHT off the platform onto the elevated ground to
    # reach the goal sitting on it.
    placed = []
    placed.append(sprites["beam"].clone(new_name="beam_l1").set_position(0, 4))
    placed.extend(_make_pulley("PA", wheel_x=28, wheel_y=5,
                                left_color="red", right_color="blue",
                                initial_state=LEFT_HIGH))
    # Left ground (low; cols 0-27, top row 56).
    placed.extend(_floor_strip(0, 28, FLOOR_TOP))
    # Elevated right ground (top row 14; cols 32-63).
    placed.extend(_floor_strip(32, 64, 14))
    # Goal sits on the elevated ground.
    placed.append(sprites["goal_marker"].clone(new_name="goal_l1").set_position(56, 11))
    placed.extend(_make_avatars(start_x=12, start_y=53))

    data = {
        "step_budget": 30,
        "pulleys": {
            "PA": {
                "wheel_x": 28, "wheel_y": 5,
                "left_x": 25, "right_x": 29,
                "state": LEFT_HIGH,
            },
        },
        "cable_pairs": [],
        "pegs": [],
        "sockets": [],
        "walls": [],
        "goal_pos": (56, 11),
        "avatar_start": (12, 53),
    }
    return Level(sprites=placed, grid_size=(GRID_W, GRID_H), data=data, name="L1")


def _level_2() -> Level:
    # Single-pulley layout. PA starts at LEFT_LOW (blue HIGH = no bridge);
    # the witness toggles PA so blue falls to LOW and bridges A → B.
    # Peg lives on B; socket lives on B; dropping peg removes a wall blocking C.
    placed = []
    placed.append(sprites["beam"].clone(new_name="beam_l2").set_position(0, 4))
    placed.extend(_make_pulley("PA", wheel_x=8, wheel_y=5,
                                left_color="red", right_color="blue",
                                initial_state=LEFT_LOW))
    # Floor A.
    placed.extend(_floor_strip(0, 8, FLOOR_TOP))
    # Floor B (cols 16-31).
    placed.extend(_floor_strip(16, 32, FLOOR_TOP))
    # Wall blocks col-range 32-35 from B → C.
    placed.append(sprites["wall_block"].clone(new_name="wall_l2").set_position(32, 48))
    # Hidden floor under and past the wall, revealed when wall is REMOVED.
    placed.extend(_floor_strip(32, 40, FLOOR_TOP))
    # Floor C-D (cols 40-63 contiguous).
    placed.extend(_floor_strip(40, 64, FLOOR_TOP))
    # Peg on B near its left edge (foot col 19 picks it up at x=18).
    placed.append(sprites["peg_red"].clone(new_name="peg_l2").set_position(18, 53))
    # Socket on B further right (foot col 27 drops the peg at x=26).
    placed.append(sprites["socket"].clone(new_name="socket_l2").set_position(25, 53))
    # Goal on the far right.
    placed.append(sprites["goal_marker"].clone(new_name="goal_l2").set_position(58, 53))
    placed.extend(_make_avatars(start_x=2, start_y=53))

    data = {
        "step_budget": 80,
        "pulleys": {
            "PA": {"wheel_x": 8, "wheel_y": 5, "left_x": 5, "right_x": 9, "state": LEFT_LOW},
        },
        "cable_pairs": [],
        "pegs": [{"name": "peg_l2", "color": "red", "x": 18, "y": 53}],
        "sockets": [
            {"name": "socket_l2", "color": "red", "anchor_pulley": None, "anchor_side": None,
             "removes_wall": "wall_l2", "x": 25, "y": 53}
        ],
        "walls": [{"name": "wall_l2", "x": 32, "y": 48}],
        "goal_pos": (58, 53),
        "avatar_start": (2, 53),
    }
    return Level(sprites=placed, grid_size=(GRID_W, GRID_H), data=data, name="L2")


def _level_3() -> Level:
    # Three pulleys. PA and PC are cable-coupled in opposite phase: a single
    # ACTION5 toggles BOTH simultaneously while preserving their inverted relation.
    # Witness: A → PA-blue → B (pickup peg) → back → drop on PA-blue socket
    # → wall removes → walk forward through B → PB → C → past wall → PC-red
    # → cable-toggle → PC-red rides UP carrying avatar to the goal at HIGH.
    placed = []
    placed.append(sprites["beam"].clone(new_name="beam_l3").set_position(0, 4))
    placed.extend(_make_pulley("PA", wheel_x=8, wheel_y=5,
                                left_color="red", right_color="blue",
                                initial_state=LEFT_HIGH))
    placed.extend(_make_pulley("PB", wheel_x=32, wheel_y=5,
                                left_color="green", right_color="blue",
                                initial_state=LEFT_HIGH))
    placed.extend(_make_pulley("PC", wheel_x=56, wheel_y=5,
                                left_color="red", right_color="blue",
                                initial_state=LEFT_LOW))
    placed.extend(_make_cable(8, 56, beam_y=4))
    # Floor islands.
    placed.extend(_floor_strip(0, 8, FLOOR_TOP))
    placed.extend(_floor_strip(16, 32, FLOOR_TOP))
    placed.extend(_floor_strip(40, 48, FLOOR_TOP))
    # Wall + hidden floor underneath.
    placed.append(sprites["wall_block"].clone(new_name="wall_l3").set_position(48, 48))
    placed.extend(_floor_strip(48, 56, FLOOR_TOP))
    # Peg on B near its left edge.
    placed.append(sprites["peg_blue"].clone(new_name="peg_l3").set_position(18, 53))
    # Socket sits on PA's RIGHT (blue) platform when blue is LOW (initial state).
    # The on_set_level re-anchor places the socket at row 53 in initial state.
    placed.append(sprites["socket"].clone(new_name="socket_l3").set_position(11, 53))
    # Goal at HIGH-side of PC-red (after cable-toggle PC-red rises with avatar).
    placed.append(sprites["goal_marker"].clone(new_name="goal_l3").set_position(57, 13))
    placed.extend(_make_avatars(start_x=2, start_y=53))

    data = {
        "step_budget": 150,
        "pulleys": {
            "PA": {"wheel_x": 8, "wheel_y": 5, "left_x": 5, "right_x": 9, "state": LEFT_HIGH},
            "PB": {"wheel_x": 32, "wheel_y": 5, "left_x": 29, "right_x": 33, "state": LEFT_HIGH},
            "PC": {"wheel_x": 56, "wheel_y": 5, "left_x": 53, "right_x": 57, "state": LEFT_LOW},
        },
        "cable_pairs": [("PA", "PC", "opposite")],
        "pegs": [{"name": "peg_l3", "color": "blue", "x": 18, "y": 53}],
        "sockets": [
            {"name": "socket_l3", "color": "blue", "anchor_pulley": "PA", "anchor_side": "right",
             "removes_wall": "wall_l3", "x": 11, "y": 53}
        ],
        "walls": [{"name": "wall_l3", "x": 48, "y": 48}],
        "goal_pos": (57, 13),
        "avatar_start": (2, 53),
    }
    return Level(sprites=placed, grid_size=(GRID_W, GRID_H), data=data, name="L3")


levels = [_level_1(), _level_2(), _level_3()]


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, game_ref):
        super().__init__()
        self._game = game_ref

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        budget = self._game.current_level.get_data("step_budget") or 100
        remaining = max(0, budget - self._game._action_count)
        ratio = remaining / budget
        fill_cells = int(GRID_W * ratio)
        for x in range(GRID_W):
            frame[GRID_H - 1, x] = HUD_FILL if x < fill_cells else HUD_EMPTY
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Dj5h(NovaBaseGame):
    def __init__(self) -> None:
        # Initialise attributes BEFORE super().__init__ because the parent's
        # constructor calls self.set_level(0) which calls self.on_set_level().
        self.active_pulley = None
        self.pulley_state = {}
        self.pulley_cfg = {}
        self.cable_pairs = []
        self.carrying = None
        self.seated_pegs = set()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
        )
        super().__init__(
            game_id="dj5h",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )
        self._hud = StepCounterHud(self)
        self.camera._interfaces.append(self._hud)

    # ---- per-level setup ----
    def on_set_level(self, level: Level) -> None:
        self.active_pulley = None
        self.pulley_cfg = dict(level.get_data("pulleys") or {})
        self.pulley_state = {pid: cfg["state"] for pid, cfg in self.pulley_cfg.items()}
        self.cable_pairs = list(level.get_data("cable_pairs") or [])
        self.carrying = None
        self.seated_pegs = set()
        self._sync_platforms_to_state(level)
        self._sync_halos(level)
        self._sync_avatar_variant(level)
        self._sync_socket_position(level)

    # ---- helpers ----
    def _level_sprite(self, name: str):
        sl = self.current_level.get_sprites_by_name(name)
        return sl[0] if sl else None

    def _platform_y(self, state: str, side: str) -> int:
        # state = LEFT_HIGH or LEFT_LOW; side = "left" or "right"
        if state == LEFT_HIGH:
            return HIGH_Y if side == "left" else LOW_Y
        else:
            return LOW_Y if side == "left" else HIGH_Y

    def _sync_platforms_to_state(self, level: Level) -> None:
        for pid, cfg in self.pulley_cfg.items():
            state = self.pulley_state[pid]
            ly = self._platform_y(state, "left")
            ry = self._platform_y(state, "right")
            ls = self._level_sprite(f"{pid}_left")
            rs = self._level_sprite(f"{pid}_right")
            if ls:
                ls.set_position(cfg["left_x"], ly)
            if rs:
                rs.set_position(cfg["right_x"], ry)
            self._update_rope(pid, cfg, ly, ry)

    def _update_rope(self, pid: str, cfg: dict, left_y: int, right_y: int) -> None:
        # Rope sprites are 1×44 vertical; we just reposition so they end at the platform top.
        rl = self._level_sprite(f"{pid}_left_rope")
        rr = self._level_sprite(f"{pid}_right_rope")
        wheel_bot = cfg["wheel_y"] + WHEEL_SIZE
        if rl:
            # rope's bottom should reach left_y; rope is 44 tall; set rope.y so rope.y + 44 == left_y
            rl.set_position(cfg["wheel_x"], left_y - 44)
        if rr:
            rr.set_position(cfg["wheel_x"] + 4, right_y - 44)
        _ = wheel_bot  # decorative; rope may visually overlap wheel below if positioned high

    def _sync_halos(self, level: Level) -> None:
        for pid in self.pulley_cfg:
            halo = self._level_sprite(f"{pid}_halo")
            if not halo:
                continue
            if self.active_pulley == pid:
                halo.set_interaction(InteractionMode.TANGIBLE)
            else:
                halo.set_interaction(InteractionMode.REMOVED)

    def _sync_avatar_variant(self, level: Level) -> None:
        main = self._level_sprite("avatar")
        if main is None:
            return
        ax, ay = main.x, main.y
        for color in ("red", "blue", "green"):
            ac = self._level_sprite(f"avatar_carry_{color}")
            if ac is None:
                continue
            ac.set_position(ax, ay)
            if self.carrying == color:
                ac.set_interaction(InteractionMode.TANGIBLE)
            else:
                ac.set_interaction(InteractionMode.REMOVED)
        if self.carrying is None:
            main.set_interaction(InteractionMode.TANGIBLE)
        else:
            main.set_interaction(InteractionMode.REMOVED)

    def _sync_socket_position(self, level: Level) -> None:
        # Re-anchor each socket to its bound platform (if anchored). Sockets with
        # `anchor_pulley=None` stay at their level-defined floor position.
        for sock_cfg in level.get_data("sockets") or []:
            sock = self._level_sprite(sock_cfg["name"])
            if sock is None:
                continue
            pid = sock_cfg.get("anchor_pulley")
            if pid is None:
                continue  # floor-anchored socket; do not reposition
            side = sock_cfg["anchor_side"]
            cfg = self.pulley_cfg[pid]
            state = self.pulley_state[pid]
            py = self._platform_y(state, side)
            base_x = cfg["left_x"] if side == "left" else cfg["right_x"]
            sock_x = base_x + (PLATFORM_W // 2) - 1
            sock_y = py - 3
            sock.set_position(sock_x, sock_y)

    # ---- click handling ----
    def _handle_click(self) -> None:
        data = self.action.data or {}
        x = int(data.get("x", -1))
        y = int(data.get("y", -1))
        if x < 0 or y < 0:
            return
        gx, gy = x, y  # camera 64×64, scale=1, no padding
        # Find any pulley wheel under this cell.
        for pid, cfg in self.pulley_cfg.items():
            wx, wy = cfg["wheel_x"], cfg["wheel_y"]
            if wx <= gx < wx + WHEEL_SIZE and wy <= gy < wy + WHEEL_SIZE:
                self.active_pulley = pid
                self._sync_halos(self.current_level)
                return
        # Click outside any wheel — no-op.

    # ---- toggle handling ----
    def _toggle_active_pulley(self) -> None:
        if self.active_pulley is None:
            return  # ACTION5 with no active pulley is a no-op
        primary = self.active_pulley
        # Find linked partner via cable_pairs.
        partner = None
        phase = "same"
        for a, b, p in self.cable_pairs:
            if a == primary:
                partner, phase = b, p
                break
            if b == primary:
                partner, phase = a, p
                break
        # Capture pre-toggle platform state for avatar-carry detection.
        pre_state = dict(self.pulley_state)
        # Apply primary toggle.
        self.pulley_state[primary] = _flip(self.pulley_state[primary])
        # Apply partner toggle.
        if partner is not None:
            if phase == "same":
                self.pulley_state[partner] = _flip(self.pulley_state[partner])
            else:  # opposite
                self.pulley_state[partner] = _flip(self.pulley_state[partner])
                # Note: same flip; opposite-phase coupling is encoded by INITIAL state choice
                # (PA and PC start in opposite states); a flip on one flips both, preserving
                # the opposite-phase invariant. Mechanically identical to "same" for the toggle
                # operation; the visual cross-over of the cable signals the inverted relation.
        # Reposition avatars if they were on a platform that moved.
        self._ride_platforms(pre_state, level=self.current_level)
        # Resync visuals.
        self._sync_platforms_to_state(self.current_level)
        self._sync_socket_position(self.current_level)
        self._sync_avatar_variant(self.current_level)

    def _ride_platforms(self, pre_state: dict, level: Level) -> None:
        avatar = self._level_sprite("avatar")
        if avatar is None:
            return
        ax = avatar.x
        ay = avatar.y
        foot_row = ay + AVATAR_H  # the row of the surface the avatar stands on
        # For each pulley, check whether the avatar's foot row matches that pulley's
        # pre-toggle platform-top row, then carry the avatar to the new row.
        for pid, cfg in self.pulley_cfg.items():
            if pre_state.get(pid) == self.pulley_state[pid]:
                continue  # this pulley did not toggle
            for side in ("left", "right"):
                pre_y = self._platform_y_from(pre_state[pid], side)
                new_y = self._platform_y(self.pulley_state[pid], side)
                base_x = cfg["left_x"] if side == "left" else cfg["right_x"]
                if (foot_row == pre_y and
                        base_x <= ax + 1 < base_x + PLATFORM_W):
                    new_ay = new_y - AVATAR_H
                    self._move_avatar(ax, new_ay)
                    return  # only one platform can carry per toggle

    def _platform_y_from(self, state: str, side: str) -> int:
        return self._platform_y(state, side)

    def _move_avatar(self, x: int, y: int) -> None:
        avatar = self._level_sprite("avatar")
        if avatar is not None:
            avatar.set_position(x, y)
        for color in ("red", "blue", "green"):
            ac = self._level_sprite(f"avatar_carry_{color}")
            if ac is not None:
                ac.set_position(x, y)

    # ---- movement ----
    def _try_move(self, dx: int, dy: int) -> None:
        avatar = self._level_sprite("avatar")
        if avatar is None:
            return
        nx = avatar.x + dx
        ny = avatar.y + dy
        if not self._is_walkable(nx, ny):
            return
        self._move_avatar(nx, ny)
        self._check_pickup()
        self._check_drop()

    def _is_walkable(self, x: int, y: int) -> bool:
        if x < 0 or y < 0 or x + AVATAR_W > GRID_W or y + AVATAR_H > GRID_H - 1:
            return False
        # Surface row (where avatar's feet land) is row y + AVATAR_H.
        surface_row = y + AVATAR_H
        # Check that the surface row contains a walkable pixel under the avatar's foot column.
        foot_col = x + 1   # centre column
        # Floor: any floor_block whose y == surface_row and whose x-range covers foot_col.
        for f in self.current_level.get_sprites_by_tag("floor"):
            if f.y == surface_row and f.x <= foot_col < f.x + f.width:
                if not self._wall_blocks(x, y):
                    return True
        # Platform: any platform whose y == surface_row and whose x-range covers foot_col.
        for p in self.current_level.get_sprites_by_tag("platform"):
            if p.y == surface_row and p.x <= foot_col < p.x + p.width:
                if not self._wall_blocks(x, y):
                    return True
        return False

    def _wall_blocks(self, x: int, y: int) -> bool:
        # Avatar body cells: cols x..x+2, rows y..y+2. Reject if any wall_block (TANGIBLE) overlaps.
        for w in self.current_level.get_sprites_by_tag("wall"):
            if w._interaction == InteractionMode.REMOVED:
                continue
            if (x < w.x + w.width and x + AVATAR_W > w.x and
                    y < w.y + w.height and y + AVATAR_H > w.y):
                return True
        return False

    def _check_pickup(self) -> None:
        if self.carrying is not None:
            return
        avatar = self._level_sprite("avatar")
        if avatar is None:
            return
        foot_col = avatar.x + 1
        foot_row = avatar.y + AVATAR_H - 1   # avatar occupies row up to y+AVATAR_H-1
        for peg in self.current_level.get_sprites_by_tag("peg"):
            if peg._interaction == InteractionMode.REMOVED:
                continue
            if (peg.x <= foot_col < peg.x + peg.width and
                    peg.y <= foot_row < peg.y + peg.height):
                # Pick it up.
                color = None
                for c in ("red", "blue", "green"):
                    if f"peg_{c}" in peg.tags:
                        color = c
                        break
                if color is None:
                    continue
                peg.set_interaction(InteractionMode.REMOVED)
                self.carrying = color
                self._sync_avatar_variant(self.current_level)
                return

    def _check_drop(self) -> None:
        if self.carrying is None:
            return
        avatar = self._level_sprite("avatar")
        if avatar is None:
            return
        foot_col = avatar.x + 1
        foot_row = avatar.y + AVATAR_H - 1
        for sock_cfg in self.current_level.get_data("sockets") or []:
            sock = self._level_sprite(sock_cfg["name"])
            if sock is None:
                continue
            if sock_cfg["color"] != self.carrying:
                continue
            if sock_cfg["name"] in self.seated_pegs:
                continue
            if (sock.x <= foot_col < sock.x + sock.width and
                    sock.y <= foot_row < sock.y + sock.height):
                # Seat the peg, remove the wall.
                self.seated_pegs.add(sock_cfg["name"])
                # Mark sock visually changed: turn its centre pixel to peg color.
                self.carrying = None
                wall_name = sock_cfg.get("removes_wall")
                if wall_name:
                    wall = self._level_sprite(wall_name)
                    if wall is not None:
                        wall.set_interaction(InteractionMode.REMOVED)
                # Recolour socket to indicate seating.
                color = sock_cfg["color"]
                body = {"red": PEG_RED_BODY, "blue": PEG_BLUE_BODY, "green": PEG_GREEN_BODY}[color]
                sock.color_remap(SOCKET_CENTER, body)
                self._sync_avatar_variant(self.current_level)
                return

    # ---- win/lose ----
    def _check_win(self) -> None:
        avatar = self._level_sprite("avatar")
        if avatar is None:
            return
        goal = self._level_sprite_by_tag("goal")
        if goal is None:
            return
        foot_col = avatar.x + 1
        foot_row = avatar.y + AVATAR_H - 1
        if (goal.x <= foot_col < goal.x + goal.width and
                goal.y <= foot_row < goal.y + goal.height):
            self.next_level()

    def _level_sprite_by_tag(self, tag: str):
        sl = self.current_level.get_sprites_by_tag(tag)
        return sl[0] if sl else None

    # ---- step dispatch ----
    def step(self) -> None:
        budget = self.current_level.get_data("step_budget") or 999
        if self._action_count > budget:
            self.lose()
            self.complete_action()
            return

        aid = self.action.id
        if aid == GameAction.ACTION1:
            self._try_move(0, -WALK_STEP)
        elif aid == GameAction.ACTION2:
            self._try_move(0, WALK_STEP)
        elif aid == GameAction.ACTION3:
            self._try_move(-WALK_STEP, 0)
        elif aid == GameAction.ACTION4:
            self._try_move(WALK_STEP, 0)
        elif aid == GameAction.ACTION5:
            self._toggle_active_pulley()
        elif aid == GameAction.ACTION6:
            self._handle_click()

        self._check_win()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        # Encode active pulley + state flags + carrying flag + seated count.
        out = np.zeros((4, 4), dtype=np.int8)
        ids = list(self.pulley_cfg.keys())
        for i, pid in enumerate(ids[:4]):
            out[0, i] = 1 if self.pulley_state.get(pid) == LEFT_HIGH else 2
            out[1, i] = 1 if self.active_pulley == pid else 0
        out[2, 0] = 1 if self.carrying is not None else 0
        out[2, 1] = len(self.seated_pegs)
        return out

    def _get_valid_actions(self):
        valid = super()._get_valid_actions()
        if self.active_pulley is None:
            valid = [v for v in valid if v.id != GameAction.ACTION5]
        return valid


# ---------------------------------------------------------------------
# 6. WITNESS SOLUTIONS (consumed by the smoke-test CHECK_WITNESS_WINS)
# ---------------------------------------------------------------------
def _act(n: int):
    return ActionInput(id=GameAction.from_id(n), data={})


def _click(x: int, y: int):
    return ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y})


WITNESS_L1 = [
    _click(30, 7),    # select PA
    _act(5),          # PA: LEFT_HIGH → LEFT_LOW; red platform falls to LOW (cols 25-31 row 56)
    _act(4),          # walk x=12 → 16
    _act(4),          # 16 → 20
    _act(4),          # 20 → 24
    _act(4),          # 24 → 28 (foot col 29 on PA-red LOW)
    _act(5),          # PA: LEFT_LOW → LEFT_HIGH; avatar rides red platform up; now at (28, 11) on red HIGH
    _act(4),          # 28 → 32 (foot col 33 onto elevated right ground at row 14)
    _act(4),          # 32 → 36
    _act(4),          # 36 → 40
    _act(4),          # 40 → 44
    _act(4),          # 44 → 48
    _act(4),          # 48 → 52
    _act(4),          # 52 → 56 (foot col 57 lands on goal at (56, 11))
]

WITNESS_L2 = [
    _click(10, 7),    # select PA (wheel cols 8-12 rows 5-9)
    _act(5),          # toggle PA: LEFT_LOW → LEFT_HIGH; blue falls to LOW (cols 9-15 row 56) — bridge A→B
    _act(4),          # walk x=2 → 6 (foot col 7 on A floor)
    _act(4),          # 6 → 10 (foot col 11 on PA-blue)
    _act(4),          # 10 → 14 (foot col 15 on PA-blue)
    _act(4),          # 14 → 18 (foot col 19 on B + peg pickup at (16, 53))
    _act(4),          # 18 → 22 (foot col 23 on B)
    _act(4),          # 22 → 26 (foot col 27 on B + drop at socket (24, 53)) — wall removes
    _act(4),          # 26 → 30 (foot col 31 on B)
    _act(4),          # 30 → 34 (foot col 35 — wall removed; on hidden floor)
    _act(4),          # 34 → 38 (foot col 39)
    _act(4),          # 38 → 42 (foot col 43 on C)
    _act(4),          # 42 → 46
    _act(4),          # 46 → 50
    _act(4),          # 50 → 54
    _act(4),          # 54 → 58 (foot col 59 on goal at (58, 53)) → win
]

WITNESS_L3 = [
    _act(4),          # x=2→6 on A
    _act(4),          # 6→10 on A (foot col 11 — would also overlap socket but carrying=None, no drop)
    _act(4),          # 10→14 on PA-blue (cols 9-15)
    _act(4),          # 14→18 on B (foot col 19 — pickup peg at (18, 53))
    _act(3),          # 18→14 on PA-blue
    _act(3),          # 14→10 on PA-blue (foot col 11 — drop peg on socket; wall removes)
    _act(4),          # 10→14 on PA-blue
    _act(4),          # 14→18 on B
    _act(4),          # 18→22 on B
    _act(4),          # 22→26 on B
    _act(4),          # 26→30 on B
    _act(4),          # 30→34 on PB-blue-clone (cols 33-39)
    _act(4),          # 34→38 on PB-blue-clone
    _act(4),          # 38→42 on C (cols 40-47)
    _act(4),          # 42→46 on C
    _act(4),          # 46→50 on hidden floor (wall removed; cols 48-55)
    _act(4),          # 50→54 on hidden floor
    _act(4),          # 54→58 on PC-red at LOW (cols 53-59)
    _click(58, 7),    # select PC (wheel cols 56-60)
    _act(5),          # cable-toggle: PC red rises HIGH (avatar carried up); PA flips simultaneously
                      # Avatar lands on goal at (57, 13)
]
