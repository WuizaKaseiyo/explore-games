"""Generated game rk7x."""

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
    # Wall: solid 4x4 black block tiling the negative space of the corridor.
    "wall_tile": Sprite(
        pixels=[
            [5, 5, 5, 5],
            [5, 5, 5, 5],
            [5, 5, 5, 5],
            [5, 5, 5, 5],
        ],
        name="wall_tile",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    ),
    # Courier "red" — yellow body with an orange tip on the east edge.
    # Rotation handles other directions.
    "courier_red": Sprite(
        pixels=[
            [-1, -1, -1, -1],
            [-1, 11, 11, 12],
            [-1, 11, 11, 12],
            [-1, -1, -1, -1],
        ],
        name="courier_red",
        visible=True,
        collidable=True,
        tags=["courier", "courier_red"],
        layer=5,
    ),
    # Courier "blue" — light-blue body with a dark-blue tip on the east edge.
    "courier_blue": Sprite(
        pixels=[
            [-1, -1, -1, -1],
            [-1, 10, 10, 9],
            [-1, 10, 10, 9],
            [-1, -1, -1, -1],
        ],
        name="courier_blue",
        visible=True,
        collidable=True,
        tags=["courier", "courier_blue"],
        layer=5,
    ),
    # Junction blade variants.  Each junction places TWO of these at the
    # same cell (one TANGIBLE, one REMOVED); clicking swaps which is
    # active.  The blade shape is chosen per-state from each junction's
    # `pass_<state>` dict so the rendered shape literally depicts which
    # two cardinal directions are currently connected:
    #   * straight bars (green) — pass-through (W↔E or N↔S),
    #   * L-shapes (magenta)   — turning corners (NW, NE, SW, SE).
    # The "junction_h" / "junction_v" slot tags are applied at placement
    # time (in `_build_level`), not in the sprite definitions.
    "junction_straight_h": Sprite(
        pixels=[
            [4, 4, 4, 4],
            [14, 14, 14, 14],
            [14, 14, 14, 14],
            [4, 4, 4, 4],
        ],
        name="junction_straight_h",
        visible=True,
        collidable=True,
        tags=["switch"],
        layer=2,
    ),
    "junction_straight_v": Sprite(
        pixels=[
            [4, 14, 14, 4],
            [4, 14, 14, 4],
            [4, 14, 14, 4],
            [4, 14, 14, 4],
        ],
        name="junction_straight_v",
        visible=True,
        collidable=True,
        tags=["switch"],
        layer=2,
    ),
    "junction_l_nw": Sprite(
        pixels=[
            [4, 14, 14, 4],
            [14, 14, 14, 4],
            [14, 14, 4, 4],
            [4, 4, 4, 4],
        ],
        name="junction_l_nw",
        visible=True,
        collidable=True,
        tags=["switch"],
        layer=2,
    ),
    "junction_l_ne": Sprite(
        pixels=[
            [4, 14, 14, 4],
            [4, 14, 14, 14],
            [4, 4, 14, 14],
            [4, 4, 4, 4],
        ],
        name="junction_l_ne",
        visible=True,
        collidable=True,
        tags=["switch"],
        layer=2,
    ),
    "junction_l_sw": Sprite(
        pixels=[
            [4, 4, 4, 4],
            [14, 14, 4, 4],
            [14, 14, 14, 4],
            [4, 14, 14, 4],
        ],
        name="junction_l_sw",
        visible=True,
        collidable=True,
        tags=["switch"],
        layer=2,
    ),
    "junction_l_se": Sprite(
        pixels=[
            [4, 4, 4, 4],
            [4, 4, 14, 14],
            [4, 14, 14, 14],
            [4, 14, 14, 4],
        ],
        name="junction_l_se",
        visible=True,
        collidable=True,
        tags=["switch"],
        layer=2,
    ),
    # Bend — fixed-routing terrain (no toggle).  Visual: small dot in centre.
    "bend": Sprite(
        pixels=[
            [-1, -1, -1, -1],
            [-1, 2, 2, -1],
            [-1, 2, 2, -1],
            [-1, -1, -1, -1],
        ],
        name="bend",
        visible=True,
        collidable=True,
        tags=["bend"],
        layer=2,
    ),
    # Stop "red" — hollow red ring (visit me).
    "stop_red": Sprite(
        pixels=[
            [8, 8, 8, 8],
            [8, -1, -1, 8],
            [8, -1, -1, 8],
            [8, 8, 8, 8],
        ],
        name="stop_red",
        visible=True,
        collidable=True,
        tags=["stop_red"],
        layer=3,
    ),
    # Stop "red" visited — solid red square (post-visit).
    "stop_red_visited": Sprite(
        pixels=[
            [8, 8, 8, 8],
            [8, 13, 13, 8],
            [8, 13, 13, 8],
            [8, 8, 8, 8],
        ],
        name="stop_red_visited",
        visible=True,
        collidable=True,
        tags=["stop_red_visited"],
        layer=3,
    ),
    # Stop "blue" — hollow light-blue ring.
    "stop_blue": Sprite(
        pixels=[
            [10, 10, 10, 10],
            [10, -1, -1, 10],
            [10, -1, -1, 10],
            [10, 10, 10, 10],
        ],
        name="stop_blue",
        visible=True,
        collidable=True,
        tags=["stop_blue"],
        layer=3,
    ),
    # Stop "blue" visited — light-blue ring with solid centre.
    "stop_blue_visited": Sprite(
        pixels=[
            [10, 10, 10, 10],
            [10, 9, 9, 10],
            [10, 9, 9, 10],
            [10, 10, 10, 10],
        ],
        name="stop_blue_visited",
        visible=True,
        collidable=True,
        tags=["stop_blue_visited"],
        layer=3,
    ),
    # Terminal "red" — concentric purple+maroon square.
    "terminal_red": Sprite(
        pixels=[
            [15, 15, 15, 15],
            [15, 13, 13, 15],
            [15, 13, 13, 15],
            [15, 15, 15, 15],
        ],
        name="terminal_red",
        visible=True,
        collidable=True,
        tags=["terminal_red"],
        layer=1,
    ),
    # Terminal "blue" — concentric purple+blue square.
    "terminal_blue": Sprite(
        pixels=[
            [15, 15, 15, 15],
            [15, 9, 9, 15],
            [15, 9, 9, 15],
            [15, 15, 15, 15],
        ],
        name="terminal_blue",
        visible=True,
        collidable=True,
        tags=["terminal_blue"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 2. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 3   # grey corridor floor
PADDING_COLOR = 5      # black letter-box (matches walls)
CELL = 4               # one logical cell = 4 grid units (= 4 display pixels)


# Direction vectors keyed by name.
DIRECTIONS = {
    "E": (CELL, 0),
    "W": (-CELL, 0),
    "N": (0, -CELL),
    "S": (0, CELL),
}


# Convert a logical (cx, cy) cell coord to grid coord (top-left of the 4x4 cell).
def cell_to_grid(cx: int, cy: int) -> tuple[int, int]:
    return cx * CELL, cy * CELL


# ---------------------------------------------------------------------
# 3. LEVEL HELPERS — build per-level sprite lists declaratively.
# ---------------------------------------------------------------------
# Each level is described by a dictionary with these keys:
#   "wall_cells"     : list of (cx, cy) cells that hold a wall sprite.
#                      The 16x16 cell grid is implicit; any cell NOT in
#                      the corridor and NOT a junction/stop/terminal
#                      should be a wall.
#   "couriers"       : list of (color, start_cx, start_cy, dir_name).
#   "junctions"      : list of dicts with keys
#                          {"id": int, "cell": (cx, cy),
#                           "default_state": "H" or "V",
#                           "pass_h": dict came_from -> exit,
#                           "pass_v": dict came_from -> exit}
#   "stops"          : list of (color, cx, cy).
#   "terminals"      : list of (color, cx, cy).
#   "step_budget"    : int.
#
# (color is "red" or "blue".)


def _infer_shape(pass_dict: dict[str, str]) -> str:
    """Pick a junction-blade shape from a routing dict.

    The shape sprite literally depicts which two cardinal directions the
    blade currently connects, taken from both the keys (came_from) and
    values (exit) of `pass_dict`.
    """
    dirs: set[str] = set()
    for came_from, exit_dir in pass_dict.items():
        dirs.add(came_from)
        dirs.add(exit_dir)
    if dirs == {"W", "E"}:
        return "straight_h"
    if dirs == {"N", "S"}:
        return "straight_v"
    if dirs == {"W", "N"}:
        return "l_nw"
    if dirs == {"E", "N"}:
        return "l_ne"
    if dirs == {"W", "S"}:
        return "l_sw"
    if dirs == {"E", "S"}:
        return "l_se"
    # Fallback: a junction whose state has more than two cardinal
    # connections (e.g., a 3-way that lets a courier come from any of
    # three directions).  Render as a straight horizontal bar — the
    # specific routing is still determined by `pass_dict`, only the
    # visual cue is approximate.
    return "straight_h"


def _build_level(layout: dict) -> Level:
    """Materialise a level from a layout dict into a Level instance."""
    placed: list[Sprite] = []

    # Walls.
    for cx, cy in layout["wall_cells"]:
        gx, gy = cell_to_grid(cx, cy)
        placed.append(sprites["wall_tile"].clone().set_position(gx, gy))

    # Bends: fixed-routing terrain that the courier follows passively.
    for b in layout.get("bends", []):
        cx, cy = b["cell"]
        gx, gy = cell_to_grid(cx, cy)
        placed.append(sprites["bend"].clone().set_position(gx, gy))

    # Junctions: place BOTH twin sprites at the same cell; default-state
    # twin is TANGIBLE, the other is REMOVED.  Each twin carries an ID
    # tag so step() can find its mate.  The blade SHAPE is inferred from
    # the routing dict for that state — a pass-through routing gives a
    # straight bar, a turning routing gives an L-shape that points to the
    # two connected directions.  The slot tags `junction_h` / `junction_v`
    # are applied at placement time (sprite kinds don't carry slot tags).
    for j in layout["junctions"]:
        cx, cy = j["cell"]
        gx, gy = cell_to_grid(cx, cy)
        h_sprite = sprites[
            f"junction_{_infer_shape(j['pass_h'])}"
        ].clone().set_position(gx, gy)
        v_sprite = sprites[
            f"junction_{_infer_shape(j['pass_v'])}"
        ].clone().set_position(gx, gy)
        h_sprite.tags.append("junction_h")
        v_sprite.tags.append("junction_v")
        h_sprite.tags.append(f"sw_{j['id']}")
        v_sprite.tags.append(f"sw_{j['id']}")
        if j["default_state"] == "H":
            v_sprite.set_interaction(InteractionMode.REMOVED)
        else:
            h_sprite.set_interaction(InteractionMode.REMOVED)
        placed.append(h_sprite)
        placed.append(v_sprite)

    # Stops: place visited twin at same cell as REMOVED, hollow stop TANGIBLE.
    for color, cx, cy in layout["stops"]:
        gx, gy = cell_to_grid(cx, cy)
        if color == "red":
            stop = sprites["stop_red"].clone().set_position(gx, gy)
            visited = (
                sprites["stop_red_visited"]
                .clone()
                .set_position(gx, gy)
            )
        else:
            stop = sprites["stop_blue"].clone().set_position(gx, gy)
            visited = (
                sprites["stop_blue_visited"]
                .clone()
                .set_position(gx, gy)
            )
        visited.set_interaction(InteractionMode.REMOVED)
        placed.append(stop)
        placed.append(visited)

    # Terminals.
    for color, cx, cy in layout["terminals"]:
        gx, gy = cell_to_grid(cx, cy)
        if color == "red":
            placed.append(
                sprites["terminal_red"].clone().set_position(gx, gy)
            )
        else:
            placed.append(
                sprites["terminal_blue"].clone().set_position(gx, gy)
            )

    # Couriers.  Courier sprites store start-direction; we apply rotation
    # to make the orange tip face the start direction.
    for color, cx, cy, dir_name in layout["couriers"]:
        gx, gy = cell_to_grid(cx, cy)
        if color == "red":
            sprite = sprites["courier_red"].clone().set_position(gx, gy)
        else:
            sprite = sprites["courier_blue"].clone().set_position(gx, gy)
        rotation = {"E": 0, "S": 90, "W": 180, "N": 270}[dir_name]
        if rotation:
            sprite.rotate(rotation)
        placed.append(sprite)

    junction_table = {
        (j["cell"][0] * CELL, j["cell"][1] * CELL): {
            "H": j["pass_h"],
            "V": j["pass_v"],
            "id": j["id"],
        }
        for j in layout["junctions"]
    }
    bend_table = {
        (b["cell"][0] * CELL, b["cell"][1] * CELL): b["pass"]
        for b in layout.get("bends", [])
    }
    courier_starts = [
        (color, dir_name) for color, _, _, dir_name in layout["couriers"]
    ]
    return Level(
        sprites=placed,
        grid_size=(64, 64),
        data={
            "step_budget": layout["step_budget"],
            "junctions": junction_table,
            "bends": bend_table,
            "courier_starts": courier_starts,
        },
    )


# ---------------------------------------------------------------------
# 4. LEVEL LAYOUTS
# ---------------------------------------------------------------------
# Cell coordinates are (cx, cy) on a 16x16 logical grid.
# Convention: H means "courier passes east-west through this junction",
# V means "courier passes between west-and-south through this junction".

def _l1_layout() -> dict:
    # L1 corridor (cells):
    #   horizontal arm: (1,7) (2,7) ... (8,7)
    #   vertical arm:   (8,8) (8,9) ... (8,14)
    #   stub-up arm:    (8,6) (8,5) (8,4) (8,3)  <- ends at wall (8,2)
    # Junction at (8,7).
    corridor = set()
    for cx in range(1, 9):
        corridor.add((cx, 7))
    for cy in range(8, 15):
        corridor.add((8, cy))
    for cy in range(3, 7):
        corridor.add((8, cy))
    walls = [(cx, cy) for cx in range(16) for cy in range(16)
             if (cx, cy) not in corridor]
    return {
        "wall_cells": walls,
        "couriers": [("red", 1, 7, "E")],
        "junctions": [
            {
                "id": 1,
                "cell": (8, 7),
                "default_state": "H",
                # H: courier coming from W exits N (up the stub-arm into wall).
                "pass_h": {"W": "N", "N": "W"},
                # V: courier coming from W exits S (down toward terminal).
                "pass_v": {"W": "S", "S": "W"},
            }
        ],
        "stops": [],
        "terminals": [("red", 8, 14)],
        "step_budget": 24,
    }


def _l2_layout() -> dict:
    # L2 corridor:
    #   main artery row: (1,7)..(14,7) with terminal at (14,7) and wall at (15,7)
    #   south detour 1 from junction (5,7):
    #       J1_in (5,7) → south arm (5,8)(5,9)(5,10) → bend (5,11) east
    #       → stop (6,11) → bend (7,11) north → north arm (7,10)(7,9)(7,8)
    #       → J1_out (7,7)
    #   south detour 2 from junction (10,7):
    #       J2_in (10,7) → south arm (10,8)(10,9)(10,10) → bend (10,11) east
    #       → stop (11,11) → bend (12,11) north → north arm (12,10)(12,9)(12,8)
    #       → J2_out (12,7)
    corridor = set()
    for cx in range(1, 15):
        corridor.add((cx, 7))
    for cy in range(8, 12):
        corridor.add((5, cy))
        corridor.add((7, cy))
    corridor.add((6, 11))
    for cy in range(8, 12):
        corridor.add((10, cy))
        corridor.add((12, cy))
    corridor.add((11, 11))

    walls = [(cx, cy) for cx in range(16) for cy in range(16)
             if (cx, cy) not in corridor]

    return {
        "wall_cells": walls,
        "couriers": [("red", 1, 7, "E")],
        "bends": [
            {"cell": (5, 11), "pass": {"N": "E", "W": "S"}},
            {"cell": (7, 11), "pass": {"W": "N", "S": "E"}},
            {"cell": (10, 11), "pass": {"N": "E", "W": "S"}},
            {"cell": (12, 11), "pass": {"W": "N", "S": "E"}},
        ],
        "junctions": [
            # J1_in at (5,7): default H (continue east); V (turn south).
            {
                "id": 1,
                "cell": (5, 7),
                "default_state": "H",
                "pass_h": {"W": "E", "E": "W"},
                "pass_v": {"W": "S", "S": "W"},
            },
            # J1_out at (7,7): default H (artery thru); V (north-arriving courier exits east).
            {
                "id": 2,
                "cell": (7, 7),
                "default_state": "H",
                "pass_h": {"W": "E", "E": "W"},
                "pass_v": {"S": "E", "E": "S"},
            },
            # J2_in at (10,7): default H; V (turn south).
            {
                "id": 3,
                "cell": (10, 7),
                "default_state": "H",
                "pass_h": {"W": "E", "E": "W"},
                "pass_v": {"W": "S", "S": "W"},
            },
            # J2_out at (12,7): default H; V (north-arriving courier exits east).
            {
                "id": 4,
                "cell": (12, 7),
                "default_state": "H",
                "pass_h": {"W": "E", "E": "W"},
                "pass_v": {"S": "E", "E": "S"},
            },
        ],
        "stops": [
            ("red", 6, 11),
            ("red", 11, 11),
        ],
        "terminals": [("red", 14, 7)],
        "step_budget": 60,
    }


def _l3_layout() -> dict:
    # L3: two disjoint zig-zag corridors that never share a cell.
    #   Red corridor: (1,1)..(8,1) east; (8,1) [J_R_top] south to (8,11);
    #                 (8,11) [J_R_bot] east to (13,11) terminal_red.
    #                 stop_red on the red corridor at (4,1).
    #   Blue corridor: (1,13)..(10,13) east; (10,13) [J_B_top] north to (10,3);
    #                  (10,3) [J_B_bot] east to (13,3) terminal_blue.
    #                  stop_blue on the blue corridor at (4,13).
    # The conflict-cell rule is implemented but the disjoint corridors
    # make it dormant for the witness path; the dual-courier mechanic
    # (clicks tick BOTH couriers simultaneously) is the L3 distinguisher.
    corridor = set()
    # Red corridor.
    for cx in range(1, 9):
        corridor.add((cx, 1))
    for cy in range(2, 12):
        corridor.add((8, cy))
    for cx in range(9, 14):
        corridor.add((cx, 11))
    # Blue corridor.
    for cx in range(1, 11):
        corridor.add((cx, 13))
    for cy in range(3, 13):
        corridor.add((10, cy))
    for cx in range(11, 14):
        corridor.add((cx, 3))

    walls = [(cx, cy) for cx in range(16) for cy in range(16)
             if (cx, cy) not in corridor]

    return {
        "wall_cells": walls,
        "couriers": [
            ("red", 1, 1, "E"),
            ("blue", 1, 13, "E"),
        ],
        "junctions": [
            # J_R_top at (8,1): H continues east into wall; V turns south.
            {
                "id": 1,
                "cell": (8, 1),
                "default_state": "H",
                "pass_h": {"W": "E", "E": "W"},
                "pass_v": {"W": "S", "S": "W"},
            },
            # J_R_bot at (8,11): default V (continue south into wall), H turns east.
            {
                "id": 2,
                "cell": (8, 11),
                "default_state": "V",
                "pass_h": {"N": "E", "E": "N"},
                "pass_v": {"N": "S", "S": "N"},
            },
            # J_B_top at (10,13): H continues east into wall; V turns north.
            {
                "id": 3,
                "cell": (10, 13),
                "default_state": "H",
                "pass_h": {"W": "E", "E": "W"},
                "pass_v": {"W": "N", "N": "W"},
            },
            # J_B_bot at (10,3): default V (continue north into wall), H turns east.
            {
                "id": 4,
                "cell": (10, 3),
                "default_state": "V",
                "pass_h": {"S": "E", "E": "S"},
                "pass_v": {"S": "N", "N": "S"},
            },
        ],
        "stops": [
            ("red", 4, 1),
            ("blue", 4, 13),
        ],
        "terminals": [
            ("red", 13, 11),
            ("blue", 13, 3),
        ],
        "step_budget": 96,
    }


levels = [
    _build_level(_l1_layout()),
    _build_level(_l2_layout()),
    _build_level(_l3_layout()),
]


# ---------------------------------------------------------------------
# 5. HUD WIDGETS
# ---------------------------------------------------------------------
class StepBarHud(RenderableUserDisplay):
    """A horizontal bar at the bottom of the frame showing remaining steps."""

    def __init__(self) -> None:
        self.budget = 1
        self.remaining = 1

    def update(self, remaining: int, budget: int) -> None:
        self.budget = max(1, budget)
        self.remaining = max(0, min(remaining, self.budget))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        bar_left = 16
        bar_right = 48
        bar_y = 63
        width = bar_right - bar_left
        ratio = self.remaining / self.budget
        filled = round(width * ratio)
        for i in range(width):
            frame[bar_y, bar_left + i] = 11 if i < filled else 4
        return frame


# ---------------------------------------------------------------------
# 6. THE GAME CLASS
# ---------------------------------------------------------------------
class Rk7x(NovaBaseGame):
    """."""

    def __init__(self) -> None:
        self._step_bar = StepBarHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_bar],
        )
        super().__init__(
            game_id="rk7x",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        self.camera.width = 64
        self.camera.height = 64
        self._budget = int(level.get_data("step_budget"))
        self._junction_tables = level.get_data("junctions") or {}
        self._bend_tables = level.get_data("bends") or {}
        self._step_bar.update(self._budget, self._budget)

        # Per-courier walking direction.
        self._directions: dict[Sprite, tuple[int, int]] = {}
        # Per-courier identity colour (used for stop matching).
        self._colors: dict[Sprite, str] = {}

        couriers = level.get_sprites_by_tag("courier")
        starts = level.get_data("courier_starts") or []
        # `starts` and `couriers` are in the same order they were added.
        # Pair them up positionally.
        for sprite, (color, dir_name) in zip(couriers, starts):
            self._directions[sprite] = DIRECTIONS[dir_name]
            self._colors[sprite] = color

        # Cache initial required-stop counts per colour for the win check.
        self._required_red = len(level.get_sprites_by_tag("stop_red"))
        self._required_blue = len(level.get_sprites_by_tag("stop_blue"))

    # -- helpers -------------------------------------------------------

    def _toggle_switch(self, gx: int, gy: int) -> None:
        """If (gx, gy) lands on a switch sprite, swap the H/V twin pair."""
        switch = self.current_level.get_sprite_at(gx, gy, tag="switch")
        if switch is None:
            return
        sw_tag = next(
            (t for t in switch.tags if t.startswith("sw_")),
            None,
        )
        if sw_tag is None:
            return
        pair = self.current_level.get_sprites_by_tag(sw_tag)
        # Each pair has exactly one TANGIBLE sprite; swap interaction modes.
        for member in pair:
            if member.interaction == InteractionMode.TANGIBLE:
                member.set_interaction(InteractionMode.REMOVED)
            else:
                member.set_interaction(InteractionMode.TANGIBLE)

    def _direction_came_from(self, dx: int, dy: int) -> str:
        if dx > 0:
            return "W"
        if dx < 0:
            return "E"
        if dy > 0:
            return "N"
        return "S"

    def _exit_to_direction(self, exit_dir: str) -> tuple[int, int]:
        return DIRECTIONS[exit_dir]

    def _direction_rotation(self, vec: tuple[int, int]) -> int:
        if vec == (CELL, 0):
            return 0
        if vec == (0, CELL):
            return 90
        if vec == (-CELL, 0):
            return 180
        return 270

    def _set_courier_facing(self, sprite: Sprite, vec: tuple[int, int]) -> None:
        # Reset rotation to 0 then apply the new rotation.  novaengine
        # `rotate` is incremental, so we must restore to canonical first.
        target = self._direction_rotation(vec)
        delta = (target - sprite.rotation) % 360
        if delta:
            sprite.rotate(delta)

    # -- step ----------------------------------------------------------

    def step(self) -> None:
        if self.action.id != GameAction.ACTION6:
            self.complete_action()
            return

        data = self.action.data or {}
        click_x = int(data.get("x", 0))
        click_y = int(data.get("y", 0))
        coords = self.camera.display_to_grid(click_x, click_y)
        if coords is not None:
            gx, gy = coords
            self._toggle_switch(gx, gy)

        # Advance every courier one logical cell.
        new_positions: dict[Sprite, tuple[int, int]] = {}
        for courier, vec in self._directions.items():
            dx, dy = vec
            new_x = courier.x + dx
            new_y = courier.y + dy
            new_positions[courier] = (new_x, new_y)

        # 1. Wall collision check.
        for courier, (nx, ny) in new_positions.items():
            wall = self.current_level.get_sprite_at(nx, ny, tag="wall")
            if wall is not None:
                self.lose()
                self.complete_action()
                return

        # 2. Apply moves; junctions update direction; stops get visited.
        for courier, (nx, ny) in new_positions.items():
            came_from = self._direction_came_from(*self._directions[courier])
            courier.set_position(nx, ny)

            # Switch / junction read.
            table = self._junction_tables.get((nx, ny))
            if table is not None:
                # Find which state is currently TANGIBLE for this junction.
                state_key = self._active_blade(nx, ny)
                exit_map = table.get(state_key, {})
                exit_dir = exit_map.get(came_from)
                if exit_dir is None:
                    # Came from a direction the current blade does not
                    # accept — treat as wall hit.
                    self.lose()
                    self.complete_action()
                    return
                new_vec = DIRECTIONS[exit_dir]
                self._directions[courier] = new_vec
                self._set_courier_facing(courier, new_vec)
            else:
                # Bend cell read (passive direction-change).
                bend_map = self._bend_tables.get((nx, ny))
                if bend_map is not None:
                    exit_dir = bend_map.get(came_from)
                    if exit_dir is None:
                        self.lose()
                        self.complete_action()
                        return
                    new_vec = DIRECTIONS[exit_dir]
                    self._directions[courier] = new_vec
                    self._set_courier_facing(courier, new_vec)

            # Stop visit (matched by colour).
            color = self._colors[courier]
            stop_tag = f"stop_{color}"
            visited_tag = f"stop_{color}_visited"
            stop = self.current_level.get_sprite_at(nx, ny, tag=stop_tag)
            if stop is not None:
                # Toggle stop ↔ visited twin at this cell.
                self._swap_stop(stop, visited_tag)

        # 3. Conflict-cell check (two couriers on the same cell).
        positions = [c for c in new_positions.values()]
        if len(positions) != len(set(positions)):
            self.lose()
            self.complete_action()
            return

        # 4. Update HUD remaining-bar.
        remaining = self._budget - (self._action_count + 1)
        self._step_bar.update(remaining, self._budget)

        # 5. Win check.
        if self._is_win():
            self.next_level()
            self.complete_action()
            return

        # 6. Step budget exhaustion.
        if self._action_count + 1 >= self._budget:
            self.lose()
            self.complete_action()
            return

        self.complete_action()

    def _active_blade(self, gx: int, gy: int) -> str:
        """Return 'H' or 'V' for the currently-tangible blade at (gx, gy)."""
        h = self.current_level.get_sprite_at(gx, gy, tag="junction_h")
        if h is not None:
            return "H"
        v = self.current_level.get_sprite_at(gx, gy, tag="junction_v")
        if v is not None:
            return "V"
        return "H"

    def _swap_stop(self, stop: Sprite, visited_tag: str) -> None:
        """Swap a hollow stop with its filled visited twin at the same cell."""
        x, y = stop.x, stop.y
        candidates = [
            s
            for s in self.current_level.get_sprites_by_tag(visited_tag)
            if s.x == x and s.y == y
        ]
        if not candidates:
            return
        twin = candidates[0]
        stop.set_interaction(InteractionMode.REMOVED)
        twin.set_interaction(InteractionMode.TANGIBLE)

    def _is_win(self) -> bool:
        # Every courier must be on its matching terminal.
        for courier in self._directions:
            color = self._colors[courier]
            terminal_tag = f"terminal_{color}"
            terms = self.current_level.get_sprites_by_tag(terminal_tag)
            on_terminal = any(t.x == courier.x and t.y == courier.y for t in terms)
            if not on_terminal:
                return False
        # Every required stop must be visited.
        if self.current_level.get_sprites_by_tag("stop_red"):
            unvisited_red = [
                s
                for s in self.current_level.get_sprites_by_tag("stop_red")
                if s.interaction == InteractionMode.TANGIBLE
            ]
            if unvisited_red:
                return False
        if self.current_level.get_sprites_by_tag("stop_blue"):
            unvisited_blue = [
                s
                for s in self.current_level.get_sprites_by_tag("stop_blue")
                if s.interaction == InteractionMode.TANGIBLE
            ]
            if unvisited_blue:
                return False
        return True

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((2, 4), dtype=np.int16)
        for i, courier in enumerate(list(self._directions)[:2]):
            dx, dy = self._directions[courier]
            out[i, 0] = courier.x
            out[i, 1] = courier.y
            out[i, 2] = dx
            out[i, 3] = dy
        return out

    def _get_valid_actions(self):
        return super()._get_valid_actions()
