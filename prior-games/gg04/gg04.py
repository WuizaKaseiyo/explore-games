"""gg04."""

from __future__ import annotations

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
# Module constants
# ---------------------------------------------------------------------
FRAME_W = 64
FRAME_H = 64
CELL = 5
GRID_W = 12
GRID_H = 12
PLAYFIELD_PX = GRID_W * CELL          # 60
HUD_ROW_Y = PLAYFIELD_PX              # rows 60..63 reserved for HUD bar

# Palette
FLOOR_COLOR = 1                       # very light grey
FLOOR_ALT_COLOR = 11
WALL_COLOR = 5                        # black
WALL_HI_COLOR = 13
MIRROR_DIAG_COLOR = 4                 # dark grey diagonal
MIRROR_FRAME_COLOR = 13
EMITTER_BG = 5                        # black emitter housing
HUD_FILLED = 6                        # pink
HUD_EMPTY = 4                         # off-black

# Beam-stream colour palette (level data refers to these)
ORANGE = 12
BLUE = 9
YELLOW = 11
PURPLE = 15
GREEN = 14
RED = 8
CYAN = 10                             # used for "fake" beams that match no target

# Direction codes
N, E, S, W = 0, 1, 2, 3
DX = {N: 0, E: 1, S: 0, W: -1}
DY = {N: -1, E: 0, S: 1, W: 0}

# Single-sided reflection table. Mirrors and prisms have a reflective
# *front face* on the SW side of the cell and a *transparent back face*
# on the NE side. A beam approaching from W or S (moving E or N
# respectively into the cell) hits the front and reflects. A beam
# approaching from E or N (moving W or S into the cell) hits the back
# and passes through unchanged. Two beams can therefore share a single
# mirror cell — one reflecting off the front, the other transmitting
# through the back — without merging.
#
# Concretely: a key in REFLECT[orient] means "this incoming direction
# reflects to the mapped outgoing direction"; a missing key means the
# beam transmits (continues unchanged).
REFLECT = {
    "/":  {E: N, N: E},               # E↔N reflect; S, W transmit
    "\\": {E: S, N: W},               # E→S, N→W; S, W transmit
}

# Mix table — ordered pair-key -> output colour. Used for both filters
# and prisms. Symmetric: tuple-key is sorted.
MIX = {
    tuple(sorted([ORANGE, BLUE])):   PURPLE,
    tuple(sorted([ORANGE, YELLOW])): GREEN,
    tuple(sorted([PURPLE, YELLOW])): RED,
}


def mix(c1: int, c2: int) -> int:
    if c1 == c2:
        return c1
    return MIX.get(tuple(sorted([c1, c2])), c1)


# ---------------------------------------------------------------------
# Sprite-pixel builders
# ---------------------------------------------------------------------
def _floor_pixels(a: int = FLOOR_COLOR, b: int = FLOOR_ALT_COLOR, accent: int = 13) -> list[list[int]]:
    return [[a] * CELL for _ in range(CELL)]


def _wall_pixels(wall: int = WALL_COLOR, hi: int = WALL_HI_COLOR) -> list[list[int]]:
    return [
        [wall, hi, wall, wall, hi],
        [wall, wall, wall, hi, wall],
        [hi, wall, wall, wall, wall],
        [wall, hi, wall, wall, hi],
        [wall, wall, hi, wall, wall],
    ]


def _mirror_pixels(orient: str, base: int = FLOOR_COLOR, frame: int = MIRROR_FRAME_COLOR, diag: int = MIRROR_DIAG_COLOR) -> list[list[int]]:
    """5×5 framed optical mirror with a diagonal reflective face."""
    p = [[base] * CELL for _ in range(CELL)]
    for i in range(CELL):
        p[0][i] = frame
        p[CELL - 1][i] = frame
        p[i][0] = frame
        p[i][CELL - 1] = frame
    if orient == "/":
        # NE-SW diagonal: row=4,col=0 ; row=3,col=1 ; ... ; row=0,col=4
        for i in range(CELL):
            p[CELL - 1 - i][i] = diag
    else:  # "\\"
        # NW-SE diagonal: row=0,col=0 ; row=1,col=1 ; ... ; row=4,col=4
        for i in range(CELL):
            p[i][i] = diag
    return p


def _filter_pixels(filter_color: int, frame: int = WALL_COLOR) -> list[list[int]]:
    """5×5 filter tile with a lens core and dark frame."""
    p = [[-1, frame, frame, frame, -1],
         [frame, filter_color, filter_color, filter_color, frame],
         [frame, filter_color, 14, filter_color, frame],
         [frame, filter_color, filter_color, filter_color, frame],
         [-1, frame, frame, frame, -1]]
    return p


def _prism_pixels(filter_color: int, orient: str, frame: int = WALL_COLOR) -> list[list[int]]:
    """5×5 faceted prism cell tinted in filter colour."""
    p = [[filter_color] * CELL for _ in range(CELL)]
    for i in range(CELL):
        p[0][i] = frame
        p[CELL - 1][i] = frame
        p[i][0] = frame
        p[i][CELL - 1] = frame
    p[2][2] = 14
    if orient == "/":
        for i in range(CELL):
            p[CELL - 1 - i][i] = frame
    else:
        for i in range(CELL):
            p[i][i] = frame
    return p


def _target_ring_pixels(target_color: int, frame: int = 13) -> list[list[int]]:
    """5×5 hollow ring; transparent inside so beam shows through."""
    p = [[-1] * CELL for _ in range(CELL)]
    for i in range(CELL):
        p[0][i] = target_color
        p[CELL - 1][i] = target_color
        p[i][0] = target_color
        p[i][CELL - 1] = target_color
    p[0][0] = frame
    p[0][CELL - 1] = frame
    p[CELL - 1][0] = frame
    p[CELL - 1][CELL - 1] = frame
    return p


def _emitter_pixels(beam_color: int, direction: int, housing: int = EMITTER_BG, trim: int = 13) -> list[list[int]]:
    """5×5 emitter housing — solid dark with a beam-coloured tip on the
    side of the emitting direction."""
    p = [[housing] * CELL for _ in range(CELL)]
    for i in range(CELL):
        p[0][i] = trim
        p[CELL - 1][i] = trim
        p[i][0] = trim
        p[i][CELL - 1] = trim
    cx = cy = CELL // 2
    p[cy][cx] = beam_color
    if direction == E:
        for j in (cx, cx + 1, CELL - 1):
            p[cy][j] = beam_color
    elif direction == W:
        for j in (cx - 1, cx, 0):
            p[cy][j] = beam_color
    elif direction == N:
        for i in (cy - 1, cy, 0):
            p[i][cx] = beam_color
    elif direction == S:
        for i in (cy, cy + 1, CELL - 1):
            p[i][cx] = beam_color
    return p


def _beam_overlay_pixels(beam_color: int) -> list[list[int]]:
    """5×5 small cross at centre — transparent everywhere else."""
    p = [[-1] * CELL for _ in range(CELL)]
    cx = cy = CELL // 2
    p[cy][cx] = beam_color
    p[cy - 1][cx] = beam_color
    p[cy + 1][cx] = beam_color
    p[cy][cx - 1] = beam_color
    p[cy][cx + 1] = beam_color
    return p


# ---------------------------------------------------------------------
# HUD
# ---------------------------------------------------------------------
class StepBarHud(RenderableUserDisplay):
    def __init__(self, game: "Gg04") -> None:
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps <= 0:
            return frame
        ratio = max(0.0, min(1.0, self.game.steps_remaining / self.game.max_steps))
        filled = int(round(FRAME_W * ratio))
        for y in range(HUD_ROW_Y, FRAME_H):
            for x in range(FRAME_W):
                frame[y, x] = HUD_FILLED if x < filled else HUD_EMPTY
        return frame


# ---------------------------------------------------------------------
# Game class
# ---------------------------------------------------------------------
class Gg04(NovaBaseGame):
    def __init__(self) -> None:
        # Per-level state placeholders — declared BEFORE super().__init__()
        # because super().__init__ runs `set_level(0)` → `on_set_level()`
        # which writes to these attrs.
        # Emitters: list of (cx, cy, direction, beam_color). cx, cy lie
        # on a virtual rim cell just OUTSIDE the grid; the first iteration
        # of the tracer steps the beam to its first in-grid cell.
        self.emitters: list[tuple[int, int, int, int]] = []
        self.mirrors: dict[tuple[int, int], str] = {}          # rotatable
        self.filters: dict[tuple[int, int], int] = {}          # fixed
        self.prisms: dict[tuple[int, int], tuple[int, str]] = {}
        self.walls: set[tuple[int, int]] = set()
        self.targets: list[tuple[int, int, int]] = []          # (cx, cy, required_color)
        self.steps_used: int = 0
        self.max_steps: int = 0
        self.theme = {}

        self.hud = StepBarHud(self)
        camera = Camera(
            background=FLOOR_COLOR,
            letter_box=WALL_COLOR,
            interfaces=[self.hud],
        )
        levels = [
            Level(grid_size=(FRAME_W, FRAME_H), sprites=[], data={"Level": 1}),
            Level(grid_size=(FRAME_W, FRAME_H), sprites=[], data={"Level": 2}),
            Level(grid_size=(FRAME_W, FRAME_H), sprites=[], data={"Level": 3}),
        ]
        super().__init__(
            game_id="gg04",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    @property
    def steps_remaining(self) -> int:
        return max(0, self.max_steps - self.steps_used)

    # ----------------------------------------------------------
    # Level setup
    # ----------------------------------------------------------
    def on_set_level(self, level: Level) -> None:
        self.camera.width = FRAME_W
        self.camera.height = FRAME_H
        self.steps_used = 0
        self.emitters = []
        self.mirrors = {}
        self.filters = {}
        self.prisms = {}
        self.walls = set()
        self.targets = []
        self.theme = {
            "floor_a": FLOOR_COLOR,
            "floor_b": FLOOR_ALT_COLOR,
            "floor_accent": 13,
            "wall": WALL_COLOR,
            "wall_hi": WALL_HI_COLOR,
            "mirror_base": FLOOR_ALT_COLOR,
            "mirror_frame": 13,
            "mirror_diag": MIRROR_DIAG_COLOR,
            "emitter_bg": EMITTER_BG,
            "emitter_trim": 13,
            "optic_frame": WALL_COLOR,
            "target_frame": 13,
        }

        # Single-sided mirrors mean two beams can share a mirror cell
        # without merging: a beam approaching from W or S (moving E or N)
        # reflects; a beam approaching from N or E (moving S or W)
        # transmits straight through. The level designs below exploit
        # this by routing two real beams through a SHARED mirror at
        # different approach angles, plus (at L2/L3) a "fake" beam whose
        # colour matches no target — fake beams paint cells but cannot
        # satisfy any target check.
        #
        # Each level also keeps the decoy-mirror twist from the prior
        # version: at least one mirror is already in its winning-state
        # orientation. A "click every mirror" strategy flips it
        # OFF-true and breaks at least one beam's path.

        lvl = level.get_data("Level")
        if lvl == 1:
            self.theme.update({
                "floor_a": 11,
                "floor_b": 12,
                "floor_accent": 13,
                "mirror_base": 11,
                "mirror_frame": 5,
                "mirror_diag": 14,
                "emitter_bg": 5,
                "emitter_trim": 13,
                "target_frame": 5,
            })
            # Two real beams sharing one mirror:
            #   Orange west-rim row 3 (E-bound).
            #   Blue  south-rim col 5 (N-bound).
            # M_shared at (5, 3). Both beams hit it from their FRONT
            # face (E and N approaches), so both reflect.
            # Initial M_shared='\\' deflects orange E→S (off the witness
            # path) and blue N→W (off the witness path). Player flips
            # to '/' so orange E→N and blue N→E.
            # M_o for orange's continuation north→east at (5, 1).
            # M_b for blue's continuation east→south at (8, 3).
            # M_o initial '/' is already CORRECT (decoy). Only M_shared
            # and M_b need flipping. Click-everything would also flip
            # the decoy M_o, sending orange's N→W off-grid west.
            self.emitters.append((-1, 3, E, ORANGE))     # west rim row 3
            self.emitters.append((5, GRID_H, N, BLUE))   # south rim col 5
            self.mirrors[(5, 3)] = "\\"                  # M_shared — REQUIRED flip → '/'.
            self.mirrors[(5, 1)] = "/"                   # M_o      — DECOY (already correct).
            self.mirrors[(8, 3)] = "/"                   # M_b      — REQUIRED flip → '\\'.
            self.targets.append((8, 1, ORANGE))          # orange target
            self.targets.append((8, 5, BLUE))            # blue target
            self.max_steps = 14

        elif lvl == 2:
            self.theme.update({
                "floor_a": 1,
                "floor_b": 11,
                "floor_accent": 10,
                "wall": 13,
                "wall_hi": 5,
                "mirror_base": 11,
                "mirror_frame": 1,
                "mirror_diag": 5,
                "emitter_bg": 13,
                "emitter_trim": 5,
                "optic_frame": 5,
                "target_frame": 13,
            })
            # Adds a filter cell AND a fake beam.
            #   Orange west-rim row 2 (E-bound) → tinted by filter to PURPLE.
            #   Blue  south-rim col 5 (N-bound).
            #   Fake  north-rim col 9 (S-bound, CYAN) — its colour
            #         appears on no target, so it can paint any cell
            #         without satisfying or breaking it. S-bound beams
            #         transmit through every mirror (single-sided rule),
            #         so the fake travels straight south through the
            #         full column 9.
            self.emitters.append((-1, 2, E, ORANGE))
            self.emitters.append((5, GRID_H, N, BLUE))
            self.emitters.append((9, -1, S, CYAN))       # fake beam
            self.mirrors[(5, 2)] = "\\"                  # M_shared — REQUIRED flip → '/'.
            self.mirrors[(5, 1)] = "/"                   # M_o      — DECOY (already correct).
            self.mirrors[(8, 2)] = "/"                   # M_b      — REQUIRED flip → '\\'.
            self.filters[(7, 1)] = BLUE                  # ORANGE + BLUE = PURPLE.
            self.targets.append((10, 1, PURPLE))         # orange→purple target
            self.targets.append((8, 5, BLUE))            # blue target
            self.max_steps = 24

        else:  # lvl == 3
            self.theme.update({
                "floor_a": 5,
                "floor_b": 13,
                "floor_accent": 9,
                "wall": 0,
                "wall_hi": 12,
                "mirror_base": 13,
                "mirror_frame": 9,
                "mirror_diag": 14,
                "emitter_bg": 0,
                "emitter_trim": 9,
                "optic_frame": 0,
                "target_frame": 12,
            })
            # Adds a prism cell. Three real-or-fake beams plus a longer
            # orange path through prism + filter.
            #   Orange west-rim row 6 (E-bound).
            #   Blue  south-rim col 4 (N-bound).
            #   Fake  north-rim col 8 (S-bound, CYAN).
            #
            # Orange routing: (0..4, 6) east → reflect S→N at M_shared
            # (4, 6) [witness '/'] → (4, 5..3) → reflect N→E at M_o1
            # (4, 3) [witness '/'] → (5..7, 3) → prism BLUE-`\\` at
            # (7, 3) tints orange→PURPLE and deflects E→S → (7, 4..6)
            # → filter YELLOW at (7, 6) tints PURPLE→RED → (7, 7..8)
            # → target RED at (7, 8).
            #
            # Blue routing: (4, 11..7) north → reflect N→E at M_shared
            # → (5..8, 6) → reflect E→S at M_b (8, 6) [decoy already
            # `\\`] → (8, 7..8) → target BLUE at (8, 8).
            #
            # Fake routing: (8, 0..11) south, transmits through every
            # mirror it crosses. It happens to pass through (8, 8) — the
            # blue target — adding CYAN to that cell's colour set; the
            # win check only requires BLUE to be present, so the fake
            # cannot break the level.
            self.emitters.append((-1, 6, E, ORANGE))
            self.emitters.append((4, GRID_H, N, BLUE))
            self.emitters.append((8, -1, S, CYAN))       # fake beam
            self.mirrors[(4, 6)] = "\\"                  # M_shared — REQUIRED flip → '/'.
            self.mirrors[(4, 3)] = "\\"                  # M_o1     — REQUIRED flip → '/'.
            self.mirrors[(8, 6)] = "\\"                  # M_b      — DECOY (already correct).
            self.prisms[(7, 3)] = (BLUE, "\\")           # tint + reflect E→S.
            self.filters[(7, 6)] = YELLOW                # PURPLE + YELLOW = RED.
            self.targets.append((7, 8, RED))             # orange→purple→red target
            self.targets.append((8, 8, BLUE))            # blue target
            self.max_steps = 36

        self._sync_sprites()

    # ----------------------------------------------------------
    # Beam tracing
    # ----------------------------------------------------------
    def _trace_beam(self, emitter: tuple[int, int, int, int]) -> list[tuple[int, int, int]]:
        """Trace one beam from the given emitter.

        Mirrors and prisms are SINGLE-SIDED: a beam only reflects (and
        a prism only tints) when the incoming direction is in the
        REFLECT table for the given orientation. Otherwise the beam
        transmits — it passes straight through the cell, unchanged.
        Filters are direction-agnostic: every beam crossing a filter
        is tinted via the mix table, regardless of approach direction.
        """
        cx, cy, direction, color = emitter
        visited: list[tuple[int, int, int]] = []
        for _ in range(GRID_W * GRID_H * 3):  # safety cap against loops
            cx += DX[direction]
            cy += DY[direction]
            if cx < 0 or cx >= GRID_W or cy < 0 or cy >= GRID_H:
                break
            if (cx, cy) in self.walls:
                break
            visited.append((cx, cy, color))
            # Process cell-effects in priority: prism > mirror > filter > pass-through.
            if (cx, cy) in self.prisms:
                pcolor, porient = self.prisms[(cx, cy)]
                if direction in REFLECT[porient]:           # front face hit
                    color = mix(color, pcolor)
                    direction = REFLECT[porient][direction]
                # else: back face — transmit unchanged.
                continue
            if (cx, cy) in self.mirrors:
                morient = self.mirrors[(cx, cy)]
                if direction in REFLECT[morient]:           # front face hit
                    direction = REFLECT[morient][direction]
                # else: back face — transmit unchanged.
                continue
            if (cx, cy) in self.filters:
                color = mix(color, self.filters[(cx, cy)])
                continue
            # plain floor: continue straight
        return visited

    def _trace_all_beams(self) -> tuple[
        dict[tuple[int, int], set[int]],
        list[list[tuple[int, int, int]]],
    ]:
        """Trace every emitter; aggregate cell→colour-set and return
        per-emitter paths for rendering."""
        cell_colors: dict[tuple[int, int], set[int]] = {}
        paths: list[list[tuple[int, int, int]]] = []
        for emitter in self.emitters:
            path = self._trace_beam(emitter)
            paths.append(path)
            for (x, y, c) in path:
                cell_colors.setdefault((x, y), set()).add(c)
        return cell_colors, paths

    # ----------------------------------------------------------
    # Win predicate
    # ----------------------------------------------------------
    def _check_win(self) -> bool:
        cell_colors, _ = self._trace_all_beams()
        for (tx, ty, tc) in self.targets:
            if tc not in cell_colors.get((tx, ty), set()):
                return False
        return True

    # ----------------------------------------------------------
    # Rendering — rebuild sprite list each step
    # ----------------------------------------------------------
    def _sync_sprites(self) -> None:
        sprites: list[Sprite] = []

        # Floor / wall
        for cx in range(GRID_W):
            for cy in range(GRID_H):
                px, py = cx * CELL, cy * CELL
                if (cx, cy) in self.walls:
                    sprites.append(
                        Sprite(
                            pixels=_wall_pixels(self.theme["wall"], self.theme["wall_hi"]),
                            name=f"wall_{cx}_{cy}",
                            layer=0,
                        )
                        .set_position(px, py)
                    )
                else:
                    sprites.append(
                        Sprite(
                            pixels=_floor_pixels(
                                self.theme["floor_a"],
                                self.theme["floor_b"],
                                self.theme["floor_accent"],
                            ),
                            name=f"floor_{cx}_{cy}",
                            layer=0,
                        )
                        .set_position(px, py)
                    )

        # Filters
        for (cx, cy), fc in self.filters.items():
            sprites.append(
                Sprite(
                    pixels=_filter_pixels(fc, self.theme["optic_frame"]),
                    name=f"filter_{cx}_{cy}",
                    layer=2,
                )
                .set_position(cx * CELL, cy * CELL)
            )

        # Prisms
        for (cx, cy), (pc, po) in self.prisms.items():
            sprites.append(
                Sprite(
                    pixels=_prism_pixels(pc, po, self.theme["optic_frame"]),
                    name=f"prism_{cx}_{cy}",
                    layer=2,
                )
                .set_position(cx * CELL, cy * CELL)
            )

        # Mirrors
        for (cx, cy), orient in self.mirrors.items():
            sprites.append(
                Sprite(
                    pixels=_mirror_pixels(
                        orient,
                        self.theme["mirror_base"],
                        self.theme["mirror_frame"],
                        self.theme["mirror_diag"],
                    ),
                    name=f"mirror_{cx}_{cy}",
                    layer=2,
                )
                .set_position(cx * CELL, cy * CELL)
            )

        # Emitters — render each at its rim cell.
        for i, (ex, ey, edir, ecolor) in enumerate(self.emitters):
            if ex == -1 and edir == E:                 # west rim, beam east
                px, py = 0, ey * CELL
            elif ex == GRID_W and edir == W:           # east rim, beam west
                px, py = (GRID_W - 1) * CELL, ey * CELL
            elif ey == -1 and edir == S:               # north rim, beam south
                px, py = ex * CELL, 0
            elif ey == GRID_H and edir == N:           # south rim, beam north
                px, py = ex * CELL, (GRID_H - 1) * CELL
            else:
                continue                                # unsupported placement
            sprites.append(
                Sprite(
                    pixels=_emitter_pixels(
                        ecolor,
                        edir,
                        self.theme["emitter_bg"],
                        self.theme["emitter_trim"],
                    ),
                    name=f"emitter_{i}",
                    layer=3,
                )
                .set_position(px, py)
            )

        # Targets (rings)
        for (tx, ty, tc) in self.targets:
            sprites.append(
                Sprite(
                    pixels=_target_ring_pixels(tc, self.theme["target_frame"]),
                    name=f"target_{tx}_{ty}_{tc}",
                    layer=4,
                )
                .set_position(tx * CELL, ty * CELL)
            )

        # Beam overlays — drawn last so they show on top of floor /
        # filter / mirror / target. When two beams of different colours
        # cross the same cell, the LATER overlay wins visually; the win
        # predicate uses the per-cell colour set, so the visual collapse
        # never affects correctness.
        _, paths = self._trace_all_beams()
        beam_idx = 0
        seen_per_emitter: list[set[tuple[int, int]]] = [set() for _ in paths]
        for ei, path in enumerate(paths):
            for (cx, cy, c) in path:
                if (cx, cy) in seen_per_emitter[ei]:
                    continue
                seen_per_emitter[ei].add((cx, cy))
                sprites.append(
                    Sprite(
                        pixels=_beam_overlay_pixels(c),
                        name=f"beam_{ei}_{beam_idx}",
                        layer=5,
                    ).set_position(cx * CELL, cy * CELL)
                )
                beam_idx += 1

        self.current_level._sprites = sprites

    # ----------------------------------------------------------
    # Step dispatch
    # ----------------------------------------------------------
    def step(self) -> None:
        if self.action.id == GameAction.ACTION6:
            xd = int(self.action.data.get("x", -1))
            yd = int(self.action.data.get("y", -1))
            grid_pos = self.camera.display_to_grid(xd, yd)
            if grid_pos is not None:
                gx, gy = grid_pos
                if 0 <= gy < HUD_ROW_Y:
                    cx = gx // CELL
                    cy = gy // CELL
                    if (cx, cy) in self.mirrors:
                        # Toggle orientation
                        self.mirrors[(cx, cy)] = "\\" if self.mirrors[(cx, cy)] == "/" else "/"
                        self.steps_used += 1
                        self._sync_sprites()
        # Other action ids are ignored (only ACTION6 is in available_actions).

        if self._check_win():
            self.next_level()
        elif self.steps_used >= self.max_steps:
            self.lose()

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        # Encode mirror orientations as a small array for debug-visibility.
        rows: list[list[int]] = []
        for (cx, cy), orient in sorted(self.mirrors.items()):
            rows.append([cx, cy, 1 if orient == "/" else 0])
        if not rows:
            return np.zeros((1, 1), dtype=np.int16)
        return np.array(rows, dtype=np.int16)

    def _get_valid_actions(self) -> list[ActionInput]:
        # Pre-enumerate one click candidate at the centre pixel of every
        # mirror cell — the only cells whose click does work.
        actions: list[ActionInput] = []
        for (cx, cy) in self.mirrors:
            px = cx * CELL + CELL // 2
            py = cy * CELL + CELL // 2
            actions.append(ActionInput(id=GameAction.ACTION6, data={"x": int(px), "y": int(py)}))
        return actions
