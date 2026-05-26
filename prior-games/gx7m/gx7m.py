"""Game gx7m."""

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


# ----------------------------------------------------------------------
# Sprite bank
# ----------------------------------------------------------------------

# A toothed-disc body, 6x6, with a coloured "notch" at the top tooth.
# The notch position rotates with the sprite (engine handles via
# np.rot90 inside sprite.rotate(deg)).
def _disc_body(notch: int) -> list[list[int]]:
    return [
        [-1,    4, notch, notch,    4, -1],
        [ 4,    3,    2,    2,    3,    4],
        [ 4,    2,    2,    2,    2,    4],
        [ 4,    2,    2,    2,    2,    4],
        [ 4,    3,    2,    2,    3,    4],
        [-1,    4,    4,    4,    4, -1],
    ]


# 10x10 hollow square frame with a 2-cell placeholder cluster at one
# of the 4 cardinal edges. The placeholder cluster is palette 0 so
# `color_remap(0, mark_colour)` at level setup recolours just the
# indent.
_FRAME_BLANK: list[list[int]] = [
    [ 3,  3,  3,  3,  3,  3,  3,  3,  3,  3],
    [ 3, -1, -1, -1, -1, -1, -1, -1, -1,  3],
    [ 3, -1, -1, -1, -1, -1, -1, -1, -1,  3],
    [ 3, -1, -1, -1, -1, -1, -1, -1, -1,  3],
    [ 3, -1, -1, -1, -1, -1, -1, -1, -1,  3],
    [ 3, -1, -1, -1, -1, -1, -1, -1, -1,  3],
    [ 3, -1, -1, -1, -1, -1, -1, -1, -1,  3],
    [ 3, -1, -1, -1, -1, -1, -1, -1, -1,  3],
    [ 3, -1, -1, -1, -1, -1, -1, -1, -1,  3],
    [ 3,  3,  3,  3,  3,  3,  3,  3,  3,  3],
]


def _frame_with_indent(direction: str) -> list[list[int]]:
    pixels = [row[:] for row in _FRAME_BLANK]
    if direction == "north":
        pixels[0][4] = 0
        pixels[0][5] = 0
    elif direction == "east":
        pixels[4][9] = 0
        pixels[5][9] = 0
    elif direction == "south":
        pixels[9][4] = 0
        pixels[9][5] = 0
    elif direction == "west":
        pixels[4][0] = 0
        pixels[5][0] = 0
    return pixels


sprites = {
    "clutch_green": Sprite(
        pixels=_disc_body(14),
        name="clutch_green",
        visible=True,
        collidable=True,
        tags=["disc", "clutch"],
    ),
    "disc_lblue": Sprite(
        pixels=_disc_body(10),
        name="disc_lblue",
        visible=True,
        collidable=True,
        tags=["disc"],
    ),
    "disc_orange": Sprite(
        pixels=_disc_body(12),
        name="disc_orange",
        visible=True,
        collidable=True,
        tags=["disc"],
    ),
    "disc_pink": Sprite(
        pixels=_disc_body(7),
        name="disc_pink",
        visible=True,
        collidable=True,
        tags=["disc"],
    ),
    "frame_east": Sprite(
        pixels=_frame_with_indent("east"),
        name="frame_east",
        visible=True,
        collidable=False,
        tags=["frame"],
        layer=-1,
    ),
    "frame_north": Sprite(
        pixels=_frame_with_indent("north"),
        name="frame_north",
        visible=True,
        collidable=False,
        tags=["frame"],
        layer=-1,
    ),
    "frame_south": Sprite(
        pixels=_frame_with_indent("south"),
        name="frame_south",
        visible=True,
        collidable=False,
        tags=["frame"],
        layer=-1,
    ),
    "frame_west": Sprite(
        pixels=_frame_with_indent("west"),
        name="frame_west",
        visible=True,
        collidable=False,
        tags=["frame"],
        layer=-1,
    ),
    "ratchet_magenta": Sprite(
        pixels=_disc_body(6),
        name="ratchet_magenta",
        visible=True,
        collidable=True,
        tags=["disc", "ratchet"],
    ),
    "ratchet_bolt": Sprite(
        pixels=[
            [3],
            [3],
            [11],
            [11],
            [11],
        ],
        name="ratchet_bolt",
        visible=True,
        collidable=True,
        tags=["ratchet_bolt"],
    ),
    "clutch_bolt": Sprite(
        pixels=[
            [3],
            [3],
            [15],
            [15],
            [15],
        ],
        name="clutch_bolt",
        visible=True,
        collidable=True,
        tags=["clutch_bolt"],
    ),
}


# ----------------------------------------------------------------------
# Levels
# ----------------------------------------------------------------------

# Each level lists, for each disc:
#   (sprite_name, top_left_x, top_left_y, frame_indent_dir, mark_colour)
# Discs are 6x6. Their frames are 10x10 placed centred around the disc.
# Cardinal mesh adjacency: two discs whose top-lefts are exactly 10
# cells apart along a single axis.

_LEVEL_1_DISCS = [
    ("disc_pink",   18, 29, "south",  7),
    ("disc_lblue",  28, 29, "south", 10),
    ("disc_orange", 38, 29, "south", 12),
]
_LEVEL_2_DISCS = [
    ("disc_pink",       18, 29, "south",  7),
    ("ratchet_magenta", 28, 29, "east",   6),
    ("disc_lblue",      38, 29, "west",  10),
]
_LEVEL_3_DISCS = [
    ("disc_pink",        8, 29, "south",  7),
    ("ratchet_magenta", 18, 29, "east",   6),
    ("disc_lblue",      28, 29, "east",  10),
    ("clutch_green",    38, 29, "east",  14),
    ("disc_orange",     48, 29, "south", 12),
]


def _build_level_sprites(
    disc_specs: list[tuple[str, int, int, str, int]],
) -> list[Sprite]:
    placed: list[Sprite] = []
    for name, x, y, indent_dir, mark in disc_specs:
        frame = (
            sprites[f"frame_{indent_dir}"]
            .clone()
            .set_position(x - 2, y - 2)
            .color_remap(0, mark)
        )
        placed.append(frame)
        disc = sprites[name].clone().set_position(x, y)
        placed.append(disc)
        # Auto-place a 5-cell vertical bolt above any ratchet or
        # clutch disc. The bolt floats above the collar's top frame.
        # In the engaged state (LOCKED for ratchets, ENGAGED for
        # clutches) the bolt's coloured rod sits at the bottom of its
        # 5-cell sprite, visually extending toward the disc. In the
        # disengaged state the rod retracts to the top of the sprite,
        # visually pulled away from the disc. Centred on the disc at
        # column x + 2 (the gear's vertical centreline).
        if "ratchet" in disc.tags:
            placed.append(
                sprites["ratchet_bolt"].clone().set_position(x + 2, y - 7)
            )
        elif "clutch" in disc.tags:
            placed.append(
                sprites["clutch_bolt"].clone().set_position(x + 2, y - 7)
            )
    return placed


levels = [
    Level(
        sprites=_build_level_sprites(_LEVEL_1_DISCS),
        grid_size=(64, 64),
        data={
            "Targets": [180, 180, 180],
            "InitialRotations": [0, 0, 0],
            "StepBudget": 20,
        },
    ),
    Level(
        sprites=_build_level_sprites(_LEVEL_2_DISCS),
        grid_size=(64, 64),
        data={
            "Targets": [180, 90, 270],
            "InitialRotations": [0, 0, 0],
            "StepBudget": 30,
        },
    ),
    Level(
        sprites=_build_level_sprites(_LEVEL_3_DISCS),
        grid_size=(64, 64),
        data={
            "Targets": [180, 90, 90, 90, 180],
            "InitialRotations": [0, 0, 0, 0, 0],
            "StepBudget": 50,
        },
    ),
]


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

BACKGROUND_COLOR = 5    # black playfield
PADDING_COLOR = 13      # maroon letter-box (not visible at 64x64)

DISC_PITCH = 10         # cell distance between mesh-adjacent discs

DIR_LOCKED = "LOCKED"
DIR_CW = "CW"
_DIR_CYCLE = {DIR_LOCKED: DIR_CW, DIR_CW: DIR_LOCKED}


# ----------------------------------------------------------------------
# HUD widget
# ----------------------------------------------------------------------


class StepCounterHud(RenderableUserDisplay):
    """Single-row depleting bar at frame row 0; drained per action."""

    def __init__(self, max_steps: int = 0) -> None:
        self.max_steps = max_steps
        self.current = max_steps

    def set_max(self, m: int) -> None:
        self.max_steps = m
        self.current = m

    def update(self, remaining: int) -> None:
        self.current = max(0, min(remaining, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        bar_width = 32
        x_offset = (frame.shape[1] - bar_width) // 2
        ratio = self.current / self.max_steps
        filled = round(bar_width * ratio)
        for x in range(bar_width):
            frame[0, x_offset + x] = 0 if x < filled else 4
        return frame


# ----------------------------------------------------------------------
# Game class
# ----------------------------------------------------------------------


class Gx7m(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_ui = StepCounterHud(0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        super().__init__(
            game_id="gx7m",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        self.disc_list: list[Sprite] = level.get_sprites_by_tag("disc")
        self.disc_list.sort(key=lambda d: (d.x, d.y))

        # Static cardinal-adjacency mesh-graph (independent of clutch state).
        self.static_mesh: dict[Sprite, list[Sprite]] = {}
        for d in self.disc_list:
            self.static_mesh[d] = []
            for e in self.disc_list:
                if e is d:
                    continue
                if (abs(d.x - e.x) == DISC_PITCH and d.y == e.y) or (
                    d.x == e.x and abs(d.y - e.y) == DISC_PITCH
                ):
                    self.static_mesh[d].append(e)

        # Ratchet directional state (per ratchet sprite).
        self.ratchet_dirs: dict[Sprite, str] = {
            d: DIR_LOCKED for d in self.disc_list if "ratchet" in d.tags
        }

        # Clutch engagement state (per clutch sprite).
        self.clutch_engaged: dict[Sprite, bool] = {
            d: True for d in self.disc_list if "clutch" in d.tags
        }

        # Bolt ownership: each bolt sits centred above its owning
        # disc's collar with top-left at (disc.x + 2, disc.y - 7).
        # The bolt both shows the current state (rod at top vs bottom
        # of its 5-cell sprite) AND serves as the click target for
        # cycling it.
        self.bolt_owner: dict[Sprite, Sprite] = {}
        for tag in ("ratchet_bolt", "clutch_bolt"):
            for bolt in level.get_sprites_by_tag(tag):
                self.bolt_owner[bolt] = self._owner_of_bolt(bolt)

        # Per-disc target rotation (degrees, multiple of 90).
        target_degs = level.get_data("Targets") or [0] * len(self.disc_list)
        self.disc_targets: dict[Sprite, int] = dict(zip(self.disc_list, target_degs))

        # Apply initial rotations (cloned sprites start at rotation 0).
        initial = level.get_data("InitialRotations") or [0] * len(self.disc_list)
        for d, init_deg in zip(self.disc_list, initial):
            if init_deg:
                d.rotate(init_deg)

        # Render every bolt's initial visual state.
        for bolt in level.get_sprites_by_tag("ratchet_bolt"):
            owner = self.bolt_owner.get(bolt)
            if owner is not None:
                self._render_ratchet_bolt(bolt, self.ratchet_dirs[owner])
        for bolt in level.get_sprites_by_tag("clutch_bolt"):
            owner = self.bolt_owner.get(bolt)
            if owner is not None:
                self._render_clutch_bolt(bolt, self.clutch_engaged[owner])

        self.step_budget = level.get_data("StepBudget") or 50
        self._step_counter_ui.set_max(self.step_budget)

    def _owner_of_bolt(self, bolt: Sprite) -> Sprite | None:
        for d in self.disc_list:
            if bolt.x == d.x + 2 and bolt.y == d.y - 7:
                return d
        return None

    def _render_ratchet_bolt(self, bolt: Sprite, direction: str) -> None:
        # The yellow rod occupies 3 of the 5 cells; its position
        # encodes state. LOCKED → rod at bottom (extends toward disc);
        # CW → rod at top (retracted from disc). The remaining 2 cells
        # are dim grey "track".
        if direction == DIR_LOCKED:
            bolt.pixels[0, 0] = 3
            bolt.pixels[1, 0] = 3
            bolt.pixels[2, 0] = 11
            bolt.pixels[3, 0] = 11
            bolt.pixels[4, 0] = 11
        else:
            bolt.pixels[0, 0] = 11
            bolt.pixels[1, 0] = 11
            bolt.pixels[2, 0] = 11
            bolt.pixels[3, 0] = 3
            bolt.pixels[4, 0] = 3

    def _render_clutch_bolt(self, bolt: Sprite, engaged: bool) -> None:
        # Same metaphor as the ratchet bolt, in purple.
        if engaged:
            bolt.pixels[0, 0] = 3
            bolt.pixels[1, 0] = 3
            bolt.pixels[2, 0] = 15
            bolt.pixels[3, 0] = 15
            bolt.pixels[4, 0] = 15
        else:
            bolt.pixels[0, 0] = 15
            bolt.pixels[1, 0] = 15
            bolt.pixels[2, 0] = 15
            bolt.pixels[3, 0] = 3
            bolt.pixels[4, 0] = 3

    def _live_neighbors(self, disc: Sprite) -> list[Sprite]:
        """Mesh-graph neighbours after applying current clutch states."""
        if "clutch" in disc.tags and not self.clutch_engaged.get(disc, True):
            return []
        out: list[Sprite] = []
        for n in self.static_mesh.get(disc, []):
            if "clutch" in n.tags and not self.clutch_engaged.get(n, True):
                continue
            out.append(n)
        return out

    def _cascade(self, source: Sprite) -> None:
        """BFS through the live mesh-graph; flip sign at each hop.
        Ratchet discs gate as a one-way mechanism: when LOCKED no
        rotation passes; when CW only a +90° (CW) arrival rotates the
        ratchet and propagates past it (a -90° arrival is blocked)."""
        visited: set[Sprite] = {source}
        queue: list[tuple[Sprite, int]] = [(source, +1)]
        while queue:
            disc, sign = queue.pop(0)
            if "ratchet" in disc.tags:
                direction = self.ratchet_dirs[disc]
                if direction == DIR_LOCKED or sign != +1:
                    continue
            disc.rotate(90 if sign == +1 else 270)
            for n in self._live_neighbors(disc):
                if n not in visited:
                    visited.add(n)
                    queue.append((n, -sign))

    def _check_win(self) -> bool:
        for d in self.disc_list:
            if d.rotation != self.disc_targets[d]:
                return False
        return True

    def _handle_click(self, gx: int, gy: int) -> None:
        bolt = self.current_level.get_sprite_at(gx, gy, "ratchet_bolt")
        if bolt is not None:
            owner = self.bolt_owner.get(bolt)
            if owner is not None and "ratchet" in owner.tags:
                new_dir = _DIR_CYCLE[self.ratchet_dirs[owner]]
                self.ratchet_dirs[owner] = new_dir
                self._render_ratchet_bolt(bolt, new_dir)
            return
        bolt = self.current_level.get_sprite_at(gx, gy, "clutch_bolt")
        if bolt is not None:
            owner = self.bolt_owner.get(bolt)
            if owner is not None and "clutch" in owner.tags:
                new_engaged = not self.clutch_engaged[owner]
                self.clutch_engaged[owner] = new_engaged
                self._render_clutch_bolt(bolt, new_engaged)
            return
        disc = self.current_level.get_sprite_at(gx, gy, "disc")
        if disc is not None:
            self._cascade(disc)

    def step(self) -> None:
        self._step_counter_ui.update(self.step_budget - self._action_count)
        if self._action_count >= self.step_budget:
            self.lose()
            self.complete_action()
            return
        if self.action.id == GameAction.ACTION6:
            ax = self.action.data.get("x", -1)
            ay = self.action.data.get("y", -1)
            grid_xy = self.camera.display_to_grid(int(ax), int(ay))
            if grid_xy:
                gx, gy = grid_xy
                self._handle_click(gx, gy)
            if self._check_win():
                self.next_level()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((4, 4), dtype=np.int16)
        out[0, 0] = self._step_counter_ui.current
        for i, d in enumerate(self.disc_list[:4]):
            out[1, i] = d.rotation
        ratchet_codes = {DIR_LOCKED: 0, DIR_CW: 1}
        ratchets = [d for d in self.disc_list if "ratchet" in d.tags]
        for i, r in enumerate(ratchets[:4]):
            out[2, i] = ratchet_codes[self.ratchet_dirs[r]]
        clutches = [d for d in self.disc_list if "clutch" in d.tags]
        for i, c in enumerate(clutches[:4]):
            out[3, i] = 1 if self.clutch_engaged[c] else 0
        return out

    def _get_valid_actions(self) -> list[ActionInput]:
        out: list[ActionInput] = []
        for x in range(0, 64, 4):
            for y in range(0, 64, 4):
                out.append(
                    ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y})
                )
        return out
