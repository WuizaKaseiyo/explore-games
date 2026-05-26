"""Generated game pn5d. Source is opaque to the player by §3.4."""

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
# Constants
# ---------------------------------------------------------------------
WALL_COLOR = 4
FILL_COLOR = 10
TARGET_COLOR = 8
CAP_COLOR = 12
OPEN_COLOR = 14
CLOSED_COLOR = 3
CURSOR_COLOR = 11
BACKGROUND_COLOR = 5
PADDING_COLOR = 5
HUD_BG = 3
HUD_FG = 4

VESSEL_W = 8
VESSEL_H = 14
INTERNAL_H = 12  # liquid range: 0..INTERNAL_H
VESSEL_TOP_Y = 8
VALVE_Y = 18
CURSOR_Y = 4

# ---------------------------------------------------------------------
# Sprite bank
# ---------------------------------------------------------------------
def _vessel_outline_pixels():
    rows = []
    rows.append([-1] * VESSEL_W)  # open top
    for _ in range(1, VESSEL_H - 1):
        row = [-1] * VESSEL_W
        row[0] = WALL_COLOR
        row[VESSEL_W - 1] = WALL_COLOR
        rows.append(row)
    rows.append([WALL_COLOR] * VESSEL_W)  # bottom wall
    return rows


sprites = {
    "liquid_fill": Sprite(
        pixels=[[-1] * (VESSEL_W - 2) for _ in range(INTERNAL_H)],
        name="liquid_fill",
        visible=True,
        collidable=False,
        tags=["fill"],
        layer=-1,
    ),
    "overflow_cap": Sprite(
        pixels=[[CAP_COLOR], [CAP_COLOR], [CAP_COLOR]],
        name="overflow_cap",
        visible=True,
        collidable=False,
        tags=["overflow"],
        layer=1,
    ),
    "pour_cursor": Sprite(
        pixels=[
            [CURSOR_COLOR, CURSOR_COLOR, CURSOR_COLOR],
            [CURSOR_COLOR, -1, CURSOR_COLOR],
            [CURSOR_COLOR, CURSOR_COLOR, CURSOR_COLOR],
        ],
        name="pour_cursor",
        visible=True,
        collidable=False,
        tags=["cursor"],
        layer=2,
    ),
    "target_mark": Sprite(
        pixels=[[TARGET_COLOR, TARGET_COLOR]],
        name="target_mark",
        visible=True,
        collidable=False,
        tags=["target"],
        layer=1,
    ),
    "valve_closed": Sprite(
        pixels=[[CLOSED_COLOR, CLOSED_COLOR]] * 4,
        name="valve_closed",
        visible=True,
        collidable=True,
        tags=["valve", "sys_click"],
        layer=1,
    ),
    "valve_open": Sprite(
        pixels=[[OPEN_COLOR, OPEN_COLOR]] * 4,
        name="valve_open",
        visible=True,
        collidable=True,
        tags=["valve", "sys_click"],
        layer=1,
    ),
    "vessel_outline": Sprite(
        pixels=_vessel_outline_pixels(),
        name="vessel_outline",
        visible=True,
        collidable=True,
        tags=["vessel"],
        layer=0,
    ),
}


# ---------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------
def _surface_row(vessel_y, level):
    """Grid row of the top of liquid for the given level (0..INTERNAL_H)."""
    return vessel_y + 1 + (INTERNAL_H - level)


def _cursor_x(vessel_x):
    """Cursor (3-wide) horizontally centered above the vessel (8-wide)."""
    return vessel_x + 2


def _build_vessel_sprites(vessel_x, target, cap):
    out = [sprites["vessel_outline"].clone().set_position(vessel_x, VESSEL_TOP_Y)]
    fill = sprites["liquid_fill"].clone().set_position(vessel_x + 1, VESSEL_TOP_Y + 1)
    out.append(fill)
    target_y = _surface_row(VESSEL_TOP_Y, target)
    out.append(sprites["target_mark"].clone().set_position(vessel_x + 5, target_y))
    if cap is not None:
        cap_y = _surface_row(VESSEL_TOP_Y, cap)
        # 1-wide × 3-tall vertical lip on the OUTSIDE of the left wall, centered on the surface row.
        out.append(sprites["overflow_cap"].clone().set_position(vessel_x - 1, cap_y - 1))
    return out


def _build_valve_sprites(valve_x, is_open, fixed):
    op = sprites["valve_open"].clone().set_position(valve_x, VALVE_Y)
    if fixed:
        return op, None
    cl = sprites["valve_closed"].clone().set_position(valve_x, VALVE_Y)
    if is_open:
        cl.set_interaction(InteractionMode.REMOVED)
    else:
        op.set_interaction(InteractionMode.REMOVED)
    return op, cl


def _build_cursor(first_vessel_x):
    return sprites["pour_cursor"].clone().set_position(_cursor_x(first_vessel_x), CURSOR_Y)


def _build_level(vessel_specs, valve_specs, max_steps):
    sprite_list = []
    for vs in vessel_specs:
        sprite_list.extend(_build_vessel_sprites(vs["x"], vs["target"], vs["cap"]))
    for ve in valve_specs:
        op, cl = _build_valve_sprites(ve["x"], ve["is_open"], ve["fixed"])
        sprite_list.append(op)
        if cl is not None:
            sprite_list.append(cl)
    sprite_list.append(_build_cursor(vessel_specs[0]["x"]))
    return Level(
        sprites=sprite_list,
        grid_size=(64, 64),
        data={
            "max_steps": max_steps,
            "vessels": vessel_specs,
            "valves": valve_specs,
        },
    )


# ---------------------------------------------------------------------
# Levels
# ---------------------------------------------------------------------
L1_VESSELS = [
    {"name": "A", "x": 23, "target": 4, "cap": None},
    {"name": "B", "x": 33, "target": 4, "cap": None},
]
L1_VALVES = [
    {"x": 31, "left_index": 0, "right_index": 1, "is_open": True, "fixed": True},
]

L2_VESSELS = [
    {"name": "A", "x": 16, "target": 3, "cap": None},
    {"name": "B", "x": 26, "target": 2, "cap": None},
    {"name": "C", "x": 36, "target": 5, "cap": None},
]
L2_VALVES = [
    {"x": 24, "left_index": 0, "right_index": 1, "is_open": True, "fixed": False},
    {"x": 34, "left_index": 1, "right_index": 2, "is_open": True, "fixed": False},
]

L3_VESSELS = [
    {"name": "A", "x": 12, "target": 9, "cap": None},
    {"name": "B", "x": 23, "target": 9, "cap": None},
    {"name": "C", "x": 34, "target": 2, "cap": 2},
    {"name": "D", "x": 45, "target": 9, "cap": None},
]
L3_VALVES = [
    {"x": 20, "left_index": 0, "right_index": 1, "is_open": False, "fixed": False},
    {"x": 31, "left_index": 1, "right_index": 2, "is_open": False, "fixed": False},
    {"x": 42, "left_index": 2, "right_index": 3, "is_open": False, "fixed": False},
]


levels = [
    _build_level(L1_VESSELS, L1_VALVES, max_steps=12),
    _build_level(L2_VESSELS, L2_VALVES, max_steps=18),
    _build_level(L3_VESSELS, L3_VALVES, max_steps=20),
]


# ---------------------------------------------------------------------
# HUD widget
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    """Draws a depleting bar at the bottom row reflecting actions remaining."""

    def __init__(self, game: "Pn5d") -> None:
        self._game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self._game._max_steps <= 0:
            return frame
        steps_left = max(0, self._game._max_steps - self._game._action_count)
        ratio = steps_left / self._game._max_steps
        width = frame.shape[1]
        bar_width = int(np.ceil(width * ratio))
        frame[frame.shape[0] - 1, :] = HUD_BG
        if bar_width > 0:
            frame[frame.shape[0] - 1, :bar_width] = HUD_FG
        return frame


# ---------------------------------------------------------------------
# The game class
# ---------------------------------------------------------------------
class Pn5d(NovaBaseGame):
    def __init__(self) -> None:
        self._max_steps = 0
        self._cursor_index = 0
        self._vessels: list[dict] = []
        self._valves: list[dict] = []
        self._step_bar = StepCounterHud(self)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_bar],
        )
        super().__init__(
            game_id="pn5d",
            levels=levels,
            camera=camera,
            available_actions=[3, 4, 5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        # Reset the live level to a clean clone, per the universal-scaffold pattern.
        self._levels[self._current_level_index] = self._clean_levels[self._current_level_index].clone()
        live = self.current_level

        self._max_steps = live.get_data("max_steps")
        vessel_specs = live.get_data("vessels")
        valve_specs = live.get_data("valves")

        outlines = sorted(live.get_sprites_by_tag("vessel"), key=lambda s: s.x)
        fills = sorted(live.get_sprites_by_tag("fill"), key=lambda s: s.x)
        self._vessels = []
        for spec, outline, fill in zip(vessel_specs, outlines, fills):
            self._vessels.append(
                {
                    "name": spec["name"],
                    "outline_sprite": outline,
                    "fill_sprite": fill,
                    "level": 0,
                    "target": spec["target"],
                    "cap": spec["cap"],
                    "x": outline.x,
                    "y": outline.y,
                    "cursor_x": _cursor_x(outline.x),
                }
            )

        # Group valve sprites by base x; each group has open + optional closed.
        valve_sprites = live.get_sprites_by_tag("valve")
        grouped: dict[int, list] = {}
        for s in valve_sprites:
            grouped.setdefault(s.x, []).append(s)
        self._valves = []
        for spec in valve_specs:
            pair = grouped.get(spec["x"], [])
            open_sp = next((s for s in pair if s.name == "valve_open"), None)
            closed_sp = next((s for s in pair if s.name == "valve_closed"), None)
            self._valves.append(
                {
                    "open_sprite": open_sp,
                    "closed_sprite": closed_sp,
                    "is_open": spec["is_open"],
                    "left_index": spec["left_index"],
                    "right_index": spec["right_index"],
                    "fixed": spec["fixed"],
                }
            )

        self._cursor_index = 0
        self._refresh_visuals()

    def step(self) -> None:
        a = self.action.id
        if a == GameAction.ACTION3:
            if self._cursor_index > 0:
                self._cursor_index -= 1
        elif a == GameAction.ACTION4:
            if self._cursor_index < len(self._vessels) - 1:
                self._cursor_index += 1
        elif a == GameAction.ACTION5:
            self._do_pour()
        elif a == GameAction.ACTION6:
            self._handle_click()

        self._refresh_visuals()

        if self._all_targets_met():
            self.complete_action()
            self.next_level()
            return

        if self._action_count >= self._max_steps:
            self.complete_action()
            self.lose()
            return

        self.complete_action()

    # -------- helpers --------

    def _connected_group(self, start_index: int) -> set:
        group = {start_index}
        frontier = [start_index]
        while frontier:
            cur = frontier.pop()
            for valve in self._valves:
                if not valve["is_open"]:
                    continue
                other = None
                if valve["left_index"] == cur:
                    other = valve["right_index"]
                elif valve["right_index"] == cur:
                    other = valve["left_index"]
                if other is not None and other not in group:
                    group.add(other)
                    frontier.append(other)
        return group

    def _do_pour(self) -> None:
        group = self._connected_group(self._cursor_index)
        for vi in group:
            self._vessels[vi]["level"] += 1
        for v in self._vessels:
            if v["cap"] is not None and v["level"] > v["cap"]:
                v["level"] = v["cap"]
            if v["level"] > INTERNAL_H:
                v["level"] = INTERNAL_H

    def _handle_click(self) -> None:
        data = self.action.data
        if not isinstance(data, dict):
            return
        try:
            x = int(data.get("x", -1))
            y = int(data.get("y", -1))
        except (TypeError, ValueError):
            return
        grid = self.camera.display_to_grid(x, y)
        if grid is None:
            return
        gx, gy = grid
        sprite = self.current_level.get_sprite_at(gx, gy, "valve")
        if sprite is None:
            return
        for valve in self._valves:
            if valve["fixed"]:
                continue
            if sprite is valve["open_sprite"] or sprite is valve["closed_sprite"]:
                self._toggle_valve(valve)
                break

    def _toggle_valve(self, valve: dict) -> None:
        if valve["closed_sprite"] is None:
            return
        valve["is_open"] = not valve["is_open"]
        if valve["is_open"]:
            valve["closed_sprite"].set_interaction(InteractionMode.REMOVED)
            valve["open_sprite"].set_interaction(InteractionMode.TANGIBLE)
        else:
            valve["open_sprite"].set_interaction(InteractionMode.REMOVED)
            valve["closed_sprite"].set_interaction(InteractionMode.TANGIBLE)

    def _refresh_visuals(self) -> None:
        for v in self._vessels:
            self._update_fill(v)
        cursor_sprites = self.current_level.get_sprites_by_tag("cursor")
        if cursor_sprites:
            cursor = cursor_sprites[0]
            v = self._vessels[self._cursor_index]
            cursor.set_position(v["cursor_x"], CURSOR_Y)

    def _update_fill(self, vessel: dict) -> None:
        fill = vessel["fill_sprite"]
        level = vessel["level"]
        new_pixels = np.full((INTERNAL_H, VESSEL_W - 2), -1, dtype=np.int32)
        if level > 0:
            new_pixels[INTERNAL_H - level :, :] = FILL_COLOR
        fill.pixels = new_pixels

    def _all_targets_met(self) -> bool:
        return all(v["level"] == v["target"] for v in self._vessels)

    def _get_hidden_state(self) -> np.ndarray:
        rows = max(1, len(self._vessels) + len(self._valves))
        state = np.zeros((rows, 1), dtype=np.int16)
        for i, v in enumerate(self._vessels):
            state[i, 0] = v["level"]
        for j, vl in enumerate(self._valves):
            state[len(self._vessels) + j, 0] = 1 if vl["is_open"] else 0
        return state
