"""."""

from __future__ import annotations

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
sprites = {
    "bead": Sprite(
        pixels=[
            [-1, 8, 8, -1],
            [8, 8, 8, 8],
            [8, 8, 8, 8],
            [-1, 8, 8, -1],
        ],
        name="bead",
        tags=["bead"],
    ),
    "peg_plain": Sprite(
        pixels=[
            [-1, 8, -1],
            [8, 8, 8],
            [-1, 8, -1],
        ],
        name="peg_plain",
        tags=["peg", "peg-plain"],
    ),
    "peg_sticky": Sprite(
        pixels=[
            [-1, 8, -1],
            [8, 4, 8],
            [-1, 8, -1],
        ],
        name="peg_sticky",
        tags=["peg", "peg-sticky"],
    ),
    "peg_pair_a": Sprite(
        pixels=[
            [0, 8, -1],
            [8, 8, 8],
            [-1, 8, -1],
        ],
        name="peg_pair_a",
        tags=["peg", "peg-pair", "pair-A"],
    ),
    "peg_pair_b": Sprite(
        pixels=[
            [-1, 8, 0],
            [8, 8, 8],
            [-1, 8, -1],
        ],
        name="peg_pair_b",
        tags=["peg", "peg-pair", "pair-B"],
    ),
    "target_ref": Sprite(
        pixels=[[8]],
        name="target_ref",
        tags=["target-ref"],
    ),
    "path_marker": Sprite(
        pixels=[[2, 2], [2, 2]],
        name="path_marker",
        tags=["path-marker"],
    ),
}


# ---------------------------------------------------------------------
# Helpers for level construction
# ---------------------------------------------------------------------
def _bead(x: int, y: int, color: int) -> Sprite:
    s = sprites["bead"].clone().set_position(x, y)
    s.color_remap(8, color)
    return s


def _peg(kind: str, x: int, y: int, color: int) -> Sprite:
    if kind == "plain":
        s = sprites["peg_plain"].clone()
    elif kind == "sticky":
        s = sprites["peg_sticky"].clone()
    elif kind == "pair-A":
        s = sprites["peg_pair_a"].clone()
    elif kind == "pair-B":
        s = sprites["peg_pair_b"].clone()
    else:
        raise ValueError(kind)
    s.set_position(x, y)
    s.color_remap(8, color)
    return s


def _pmh(x: int, y: int, length: int) -> Sprite:
    s = sprites["path_marker"].clone().set_position(x, y)
    s.pixels = np.full((1, length), 2, dtype=np.int16)
    s.set_interaction(InteractionMode.INTANGIBLE)
    return s


def _pmv(x: int, y: int, length: int) -> Sprite:
    s = sprites["path_marker"].clone().set_position(x, y)
    s.pixels = np.full((length, 1), 2, dtype=np.int16)
    s.set_interaction(InteractionMode.INTANGIBLE)
    return s


def _trefstrip(x: int, y: int, colors: list) -> Sprite:
    s = sprites["target_ref"].clone().set_position(x, y)
    s.pixels = np.array([colors], dtype=np.int16)
    s.set_interaction(InteractionMode.INTANGIBLE)
    return s


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
_L1_CHAIN = [(12, 20), (24, 20), (36, 20), (36, 36), (24, 36), (12, 36)]
_L1_INITIAL = [14, 11, 6, 14, 11, 6]
_L1_TARGET = [6, 11, 11, 14, 11, 14]

_L2_CHAIN = [
    (6, 14), (18, 14), (30, 14), (42, 14),
    (42, 42), (30, 42), (18, 42), (6, 42),
]
_L2_INITIAL = [15, 14, 6, 11, 14, 6, 15, 11]
_L2_TARGET = [11, 14, 14, 6, 14, 14, 15, 15]

_L3_CHAIN = [
    (6, 10), (18, 10), (30, 10), (42, 10),
    (42, 30),
    (30, 30), (18, 30),
    (18, 50),
    (30, 50), (42, 50),
]
_L3_INITIAL = [15, 6, 14, 11, 11, 14, 14, 15, 6, 14]
_L3_TARGET = [11, 6, 14, 14, 11, 11, 15, 15, 14, 11]


levels = [
    # ---- Level 1 ---------------------------------------------------
    Level(
        sprites=[
            _bead(12, 20, 14),
            _bead(24, 20, 11),
            _bead(36, 20, 6),
            _bead(36, 36, 14),
            _bead(24, 36, 11),
            _bead(12, 36, 6),
            _peg("plain", 12, 14, 6),
            _peg("plain", 36, 14, 11),
            _peg("plain", 12, 42, 14),
            _pmh(16, 21, 8),
            _pmh(28, 21, 8),
            _pmv(37, 24, 12),
            _pmh(28, 37, 8),
            _pmh(16, 37, 8),
            _trefstrip(43, 60, [6, 11, 11, 14, 11, 14]),
        ],
        grid_size=(64, 64),
        data={
            "ChainPositions": _L1_CHAIN,
            "AbovePegs": {0: (12, 14), 2: (36, 14)},
            "BelowPegs": {5: (12, 42)},
            "PairPartners": {},
            "TargetSequence": _L1_TARGET,
            "StepCounter": 24,
        },
    ),
    # ---- Level 2 ---------------------------------------------------
    Level(
        sprites=[
            _bead(6, 14, 15),
            _bead(18, 14, 14),
            _bead(30, 14, 6),
            _bead(42, 14, 11),
            _bead(42, 42, 14),
            _bead(30, 42, 6),
            _bead(18, 42, 15),
            _bead(6, 42, 11),
            _peg("plain", 6, 8, 11),
            _peg("sticky", 30, 8, 14),
            _peg("plain", 42, 22, 6),
            _peg("sticky", 30, 50, 14),
            _peg("plain", 6, 50, 15),
            _pmh(10, 15, 8),
            _pmh(22, 15, 8),
            _pmh(34, 15, 8),
            _pmv(43, 18, 24),
            _pmh(34, 43, 8),
            _pmh(22, 43, 8),
            _pmh(10, 43, 8),
            _trefstrip(43, 60, [11, 14, 14, 6, 14, 14, 15, 15]),
        ],
        grid_size=(64, 64),
        data={
            "ChainPositions": _L2_CHAIN,
            "AbovePegs": {0: (6, 8), 2: (30, 8)},
            "BelowPegs": {3: (42, 22), 5: (30, 50), 7: (6, 50)},
            "PairPartners": {},
            "TargetSequence": _L2_TARGET,
            "StepCounter": 32,
        },
    ),
    # ---- Level 3 ---------------------------------------------------
    Level(
        sprites=[
            _bead(6, 10, 15),
            _bead(18, 10, 6),
            _bead(30, 10, 14),
            _bead(42, 10, 11),
            _bead(42, 30, 11),
            _bead(30, 30, 14),
            _bead(18, 30, 14),
            _bead(18, 50, 15),
            _bead(30, 50, 6),
            _bead(42, 50, 14),
            _peg("plain", 6, 4, 11),
            _peg("sticky", 42, 4, 14),
            _peg("pair-A", 30, 24, 11),
            _peg("pair-B", 18, 24, 15),
            _peg("plain", 30, 56, 14),
            _peg("sticky", 42, 56, 11),
            _peg("sticky", 18, 36, 14),
            _pmh(10, 11, 8),
            _pmh(22, 11, 8),
            _pmh(34, 11, 8),
            _pmv(43, 14, 16),
            _pmh(34, 31, 8),
            _pmh(22, 31, 8),
            _pmv(19, 34, 16),
            _pmh(22, 51, 8),
            _pmh(34, 51, 8),
            _trefstrip(38, 62, [11, 6, 14, 14, 11, 11, 15, 15, 14, 11]),
        ],
        grid_size=(64, 64),
        data={
            "ChainPositions": _L3_CHAIN,
            "AbovePegs": {0: (6, 4), 3: (42, 4), 5: (30, 24), 6: (18, 24)},
            "BelowPegs": {6: (18, 36), 8: (30, 56), 9: (42, 56)},
            "PairPartners": {(30, 24): (18, 24), (18, 24): (30, 24)},
            "TargetSequence": _L3_TARGET,
            "StepCounter": 60,
        },
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 4
PADDING_COLOR = 4


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class StepBarHud(RenderableUserDisplay):
    """."""

    def __init__(self, max_steps: int) -> None:
        self._max_steps = max_steps
        self._used = 0

    def set_max(self, m: int) -> None:
        self._max_steps = m if m > 0 else 1

    def set_used(self, u: int) -> None:
        self._used = u

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self._max_steps <= 0:
            return frame
        bar_width = 32
        x0 = (frame.shape[1] - bar_width) // 2
        used_clamped = min(self._used, self._max_steps)
        remaining = self._max_steps - used_clamped
        filled = round(bar_width * remaining / self._max_steps)
        for i in range(bar_width):
            frame[0, x0 + i] = 0 if i < filled else 4
        return frame


class CursorHud(RenderableUserDisplay):
    """."""

    def __init__(self, game: "Qb84") -> None:
        self._game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        chain = getattr(self._game, "_chain", None) or []
        idx = getattr(self._game, "_cursor_index", 0)
        if not chain or idx < 0 or idx >= len(chain):
            return frame
        bead = chain[idx]
        bx, by = int(bead.x), int(bead.y)
        bw, bh = int(bead.width), int(bead.height)
        max_y, max_x = frame.shape[0], frame.shape[1]
        for cx, cy in (
            (bx - 1, by - 1),
            (bx + bw, by - 1),
            (bx - 1, by + bh),
            (bx + bw, by + bh),
        ):
            if 0 <= cx < max_x and 0 <= cy < max_y:
                frame[cy, cx] = 0
        return frame


# ---------------------------------------------------------------------
# 5. GAME CLASS
# ---------------------------------------------------------------------
class Qb84(NovaBaseGame):
    def __init__(self) -> None:
        self._step_bar = StepBarHud(max_steps=24)
        self._cursor_hud = CursorHud(self)
        self._chain: list = []
        self._cursor_index: int = 0
        self._pegs_above: dict = {}
        self._pegs_below: dict = {}
        self._pair_partner: dict = {}
        self._bead_locked: dict = {}
        self._target_seq: list = []
        self._max_steps: int = 24
        self._steps_used: int = 0
        cam = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_bar, self._cursor_hud],
        )
        super().__init__(
            game_id="qb84",
            levels=levels,
            camera=cam,
            available_actions=[1, 2, 3, 4],
        )

    def on_set_level(self, level: Level) -> None:
        """."""
        self._cursor_index = 0
        self._steps_used = 0
        self._max_steps = int(level.get_data("StepCounter") or 24)
        self._step_bar.set_max(self._max_steps)
        self._step_bar.set_used(0)

        positions = level.get_data("ChainPositions") or []
        self._chain = []
        for pos in positions:
            cx, cy = int(pos[0]), int(pos[1])
            bead = self._find_sprite_near(level, cx, cy, "bead")
            if bead is not None:
                self._chain.append(bead)

        self._bead_locked = {bead: False for bead in self._chain}

        above_data = level.get_data("AbovePegs") or {}
        below_data = level.get_data("BelowPegs") or {}
        self._pegs_above = {}
        self._pegs_below = {}
        for idx, pos in dict(above_data).items():
            px, py = int(pos[0]), int(pos[1])
            peg = self._find_sprite_near(level, px, py, "peg")
            if peg is not None:
                self._pegs_above[int(idx)] = peg
        for idx, pos in dict(below_data).items():
            px, py = int(pos[0]), int(pos[1])
            peg = self._find_sprite_near(level, px, py, "peg")
            if peg is not None:
                self._pegs_below[int(idx)] = peg

        self._pair_partner = {}
        pair_data = level.get_data("PairPartners") or {}
        for a_pos, b_pos in dict(pair_data).items():
            ax, ay = int(a_pos[0]), int(a_pos[1])
            bx, by = int(b_pos[0]), int(b_pos[1])
            peg_a = self._find_sprite_near(level, ax, ay, "peg")
            peg_b = self._find_sprite_near(level, bx, by, "peg")
            if peg_a is not None and peg_b is not None:
                self._pair_partner[peg_a] = peg_b

        self._target_seq = list(level.get_data("TargetSequence") or [])

    def _find_sprite_near(self, level: Level, x: int, y: int, tag: str):
        s = level.get_sprite_at(x, y, tag)
        if s is not None:
            return s
        for dx in range(0, 4):
            for dy in range(0, 4):
                s = level.get_sprite_at(x + dx, y + dy, tag)
                if s is not None:
                    return s
        return None

    def _bead_color(self, bead) -> int:
        return int(bead.pixels[1, 1])

    def _peg_color(self, peg) -> int:
        return int(peg.pixels[1, 0])

    def _peg_kind(self, peg) -> str:
        if peg is None:
            return "none"
        tags = list(getattr(peg, "_tags", None) or [])
        if "pair-A" in tags:
            return "pair-A"
        if "pair-B" in tags:
            return "pair-B"
        if "peg-sticky" in tags:
            return "sticky"
        return "plain"

    def _set_color(self, sprite, new_color: int, prev_color: int) -> None:
        if prev_color != new_color:
            sprite.color_remap(prev_color, new_color)

    def _try_swap(self, bead, peg) -> bool:
        """."""
        if peg is None:
            return False
        if self._bead_locked.get(bead, False):
            return False
        kind = self._peg_kind(peg)
        bead_c = self._bead_color(bead)
        peg_c = self._peg_color(peg)
        partner_c_at_start = None
        if kind in ("pair-A", "pair-B"):
            partner = self._pair_partner.get(peg)
            if partner is not None:
                partner_c_at_start = self._peg_color(partner)
        self._set_color(bead, peg_c, bead_c)
        self._set_color(peg, bead_c, peg_c)
        if kind == "sticky":
            self._bead_locked[bead] = True
        if partner_c_at_start is not None:
            try:
                idx = self._chain.index(bead)
            except ValueError:
                idx = -1
            neighbour = None
            if idx >= 0:
                if idx + 1 < len(self._chain):
                    neighbour = self._chain[idx + 1]
                elif idx - 1 >= 0:
                    neighbour = self._chain[idx - 1]
            if neighbour is not None and not self._bead_locked.get(neighbour, False):
                ncolor = self._bead_color(neighbour)
                self._set_color(neighbour, partner_c_at_start, ncolor)
        return True

    def _check_win(self) -> bool:
        if not self._target_seq or not self._chain:
            return False
        if len(self._target_seq) != len(self._chain):
            return False
        for i, bead in enumerate(self._chain):
            if self._bead_color(bead) != self._target_seq[i]:
                return False
        return True

    def step(self) -> None:
        """."""
        action_id = self.action.id
        consumed = False
        if action_id == GameAction.ACTION3:
            self._cursor_index = max(0, self._cursor_index - 1)
            consumed = True
        elif action_id == GameAction.ACTION4:
            self._cursor_index = min(max(0, len(self._chain) - 1), self._cursor_index + 1)
            consumed = True
        elif action_id == GameAction.ACTION1:
            if self._chain and 0 <= self._cursor_index < len(self._chain):
                bead = self._chain[self._cursor_index]
                peg = self._pegs_above.get(self._cursor_index)
                consumed = self._try_swap(bead, peg)
        elif action_id == GameAction.ACTION2:
            if self._chain and 0 <= self._cursor_index < len(self._chain):
                bead = self._chain[self._cursor_index]
                peg = self._pegs_below.get(self._cursor_index)
                consumed = self._try_swap(bead, peg)
        if consumed:
            self._steps_used += 1
            self._step_bar.set_used(self._steps_used)
        if self._check_win():
            self.next_level()
            self.complete_action()
            return
        if self._steps_used >= self._max_steps:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        n = max(1, len(self._chain))
        arr = np.zeros((3, n), dtype=np.int16)
        for i, bead in enumerate(self._chain):
            arr[0, i] = self._bead_color(bead)
            arr[1, i] = 1 if self._bead_locked.get(bead, False) else 0
        arr[2, 0] = self._cursor_index
        if n >= 2:
            arr[2, 1] = self._steps_used
        if n >= 3:
            arr[2, 2] = self._max_steps
        return arr

    def _get_valid_actions(self):
        return super()._get_valid_actions()
