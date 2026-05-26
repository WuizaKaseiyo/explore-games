"""Generated game xv2b."""

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


# --------------------------------------------------------------------- #
# 1. SPRITE BANK                                                        #
# --------------------------------------------------------------------- #


def _vessel_frame_pixels():
    rows = []
    for _ in range(30):
        rows.append([2, 3, -1, -1, -1, -1, -1, -1, -1, -1, 3, 2])
    rows.append([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
    rows.append([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
    return rows


def _empty_water_pixels():
    return [[-1] * 8 for _ in range(30)]


sprites = {
    "drain_glyph": Sprite(
        pixels=[
            [5, 5, 5, 5],
            [5, 13, 13, 5],
            [5, 13, 13, 5],
            [4, 4, 4, 4],
        ],
        name="drain_glyph",
        visible=True,
        collidable=True,
        tags=["drain"],
        layer=3,
    ),
    "flow_droplet": Sprite(
        pixels=[[10, 10], [9, 9]],
        name="flow_droplet",
        visible=True,
        collidable=False,
        tags=["flow_droplet"],
        layer=5,
    ),
    "pump_off": Sprite(
        pixels=[
            [3, 3, 3, 3, 3, 3],
            [3, 12, 12, 12, 12, 3],
            [3, 12, 3, 3, 12, 3],
            [3, 3, 3, 3, 3, 3],
        ],
        name="pump_off",
        visible=True,
        collidable=True,
        tags=["pump", "pump_off"],
        layer=3,
    ),
    "pump_on": Sprite(
        pixels=[
            [3, 3, 3, 3, 3, 3],
            [3, 14, 14, 14, 14, 3],
            [3, 14, 0, 0, 14, 3],
            [3, 3, 3, 3, 3, 3],
        ],
        name="pump_on",
        visible=True,
        collidable=True,
        tags=["pump", "pump_on"],
        layer=3,
    ),
    "target_tick": Sprite(
        pixels=[[13, 6, 6, 6]],
        name="target_tick",
        visible=True,
        collidable=False,
        tags=["target_tick"],
        layer=2,
    ),
    "valve_closed": Sprite(
        pixels=[
            [4, 4, 4, 4],
            [3, 3, 11, 3],
            [3, 3, 11, 3],
            [3, 3, 11, 3],
            [3, 3, 11, 3],
            [4, 4, 4, 4],
        ],
        name="valve_closed",
        visible=True,
        collidable=True,
        tags=["valve", "valve_closed"],
        layer=3,
    ),
    "valve_open": Sprite(
        pixels=[
            [4, 4, 4, 4],
            [3, -1, -1, 3],
            [3, 10, 10, 3],
            [3, 10, 10, 3],
            [3, -1, -1, 3],
            [4, 4, 4, 4],
        ],
        name="valve_open",
        visible=True,
        collidable=True,
        tags=["valve", "valve_open"],
        layer=3,
    ),
    "vessel_frame": Sprite(
        pixels=_vessel_frame_pixels(),
        name="vessel_frame",
        visible=True,
        collidable=False,
        tags=["vessel_frame"],
        layer=1,
    ),
    "water_fill": Sprite(
        pixels=_empty_water_pixels(),
        name="water_fill",
        visible=True,
        collidable=False,
        tags=["water_fill"],
        layer=0,
    ),
}


# --------------------------------------------------------------------- #
# 2. LAYOUT CONSTANTS AND PER-LEVEL CONFIG                              #
# --------------------------------------------------------------------- #


BACKGROUND_COLOR = 5
PADDING_COLOR = 4

INTERIOR_HEIGHT = 30
VESSEL_W = 12
VESSEL_H = 32
VESSEL_TOP_Y = 16

# A vessel occupies columns [vx, vx + VESSEL_W). Interior fluid columns are
# [vx + 2, vx + 10) (8 wide). Water fill rows count up from the floor; row
# index in vessel-local coords is 30 - level (top of fill) for level > 0.
VESSEL_POS = {
    "A": (8, VESSEL_TOP_Y),
    "B": (26, VESSEL_TOP_Y),
    "C": (44, VESSEL_TOP_Y),
}

# Gap-x positions for valves / pumps. Gaps are between adjacent vessels.
# A↔B gap: cols 20..25 (6 wide, between A's right wall col 19 and B's left
# wall col 26). Centred 4-wide valve sits at gap_x=20 (cols 20..23). Pump
# is 6-wide and fills the whole gap.
GAP_AB_X = 20
GAP_BC_X = 38


def _slit_to_valve_y(slit_h):
    # Vessel y=16, interior bottom = 16 + 29 = 45. Row of fill at level h
    # corresponds to vessel-local row (30 - h), absolute y = 16 + (30 - h)
    # = 46 - h. Place a 6-tall valve so its slit (sprite rows 1..4) is
    # centred on the slit row.
    slit_abs_y = 46 - slit_h
    return slit_abs_y - 2


LEVEL_DATA = [
    # ------------------------------ Level 1 ------------------------------ #
    {
        "vessels": ["A", "B", "C"],
        "start_levels": {"A": 24, "B": 0, "C": 0},
        "target_levels": {"A": 8, "B": 8, "C": 8},
        "valves": [
            {
                "id": "V_AB",
                "left": "A",
                "right": "B",
                "slit_h": 4,
                "start_open": False,
                "gap_x": GAP_AB_X,
            },
            {
                "id": "V_BC",
                "left": "B",
                "right": "C",
                "slit_h": 4,
                "start_open": False,
                "gap_x": GAP_BC_X,
            },
        ],
        "pumps": [],
        "drains": [],
        "step_budget": 60,
    },
    # ------------------------------ Level 2 ------------------------------ #
    {
        "vessels": ["A", "B", "C"],
        "start_levels": {"A": 12, "B": 24, "C": 0},
        "target_levels": {"A": 12, "B": 8, "C": 8},
        "valves": [
            {
                "id": "V_AB",
                "left": "A",
                "right": "B",
                "slit_h": 4,
                "start_open": False,
                "gap_x": GAP_AB_X,
            },
            {
                "id": "V_BC",
                "left": "B",
                "right": "C",
                "slit_h": 4,
                "start_open": False,
                "gap_x": GAP_BC_X,
            },
        ],
        "pumps": [],
        "drains": ["B"],
        "step_budget": 70,
    },
    # ------------------------------ Level 3 ------------------------------ #
    {
        "vessels": ["A", "B", "C"],
        "start_levels": {"A": 30, "B": 0, "C": 0},
        "target_levels": {"A": 0, "B": 5, "C": 3},
        "valves": [
            {
                "id": "V_AB",
                "left": "A",
                "right": "B",
                "slit_h": 15,
                "start_open": False,
                "gap_x": GAP_AB_X,
            },
            {
                "id": "V_BC",
                "left": "B",
                "right": "C",
                "slit_h": 8,
                "start_open": False,
                "gap_x": GAP_BC_X,
            },
        ],
        "pumps": [
            {
                "id": "P_BC",
                "source": "B",
                "destination": "C",
                "gap_x": GAP_BC_X - 1,
                "gap_y": 18,
            },
        ],
        "drains": ["A"],
        "step_budget": 100,
    },
]


def _build_level(idx):
    data = LEVEL_DATA[idx]
    placed = []

    for vname in data["vessels"]:
        vx, vy = VESSEL_POS[vname]
        placed.append(sprites["vessel_frame"].clone().set_position(vx, vy))
        placed.append(sprites["water_fill"].clone().set_position(vx + 2, vy))

    for vname, target_h in data["target_levels"].items():
        vx, vy = VESSEL_POS[vname]
        tick_y = vy + (INTERIOR_HEIGHT - target_h) - 1
        if tick_y < 0:
            tick_y = 0
        placed.append(sprites["target_tick"].clone().set_position(vx + VESSEL_W, tick_y))

    for v in data["valves"]:
        vy_pos = _slit_to_valve_y(v["slit_h"])
        closed = sprites["valve_closed"].clone().set_position(v["gap_x"], vy_pos)
        opened = sprites["valve_open"].clone().set_position(v["gap_x"], vy_pos)
        if v["start_open"]:
            closed.set_visible(False).set_interaction(InteractionMode.REMOVED)
        else:
            opened.set_visible(False).set_interaction(InteractionMode.REMOVED)
        placed.append(closed)
        placed.append(opened)

    for vname in data["drains"]:
        vx, vy = VESSEL_POS[vname]
        placed.append(sprites["drain_glyph"].clone().set_position(vx + 6, vy + 26))

    for p in data["pumps"]:
        off_sprite = sprites["pump_off"].clone().set_position(p["gap_x"], p["gap_y"])
        on_sprite = sprites["pump_on"].clone().set_position(p["gap_x"], p["gap_y"])
        on_sprite.set_visible(False).set_interaction(InteractionMode.REMOVED)
        placed.append(off_sprite)
        placed.append(on_sprite)

    return Level(sprites=placed, grid_size=(64, 64))


levels = [_build_level(i) for i in range(3)]


# --------------------------------------------------------------------- #
# 3. HUD WIDGETS                                                        #
# --------------------------------------------------------------------- #


class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps=60):
        self.max_steps = max_steps
        self.current = max_steps

    def set_max(self, m):
        self.max_steps = max(0, int(m))
        self.current = self.max_steps

    def set_current(self, c):
        self.current = max(0, min(int(c), self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        bar_w = 32
        x_off = 16
        ratio = self.current / self.max_steps
        filled = int(round(bar_w * ratio))
        if filled > bar_w:
            filled = bar_w
        warning = ratio < 0.25
        fill_color = 8 if warning else 11
        for x in range(bar_w):
            if x < filled:
                frame[63, x_off + x] = fill_color
            else:
                frame[63, x_off + x] = 4
        return frame


# --------------------------------------------------------------------- #
# 4. GAME CLASS                                                         #
# --------------------------------------------------------------------- #


class Xv2b(NovaBaseGame):
    def __init__(self) -> None:
        # Per-game state must be initialised BEFORE super().__init__ because
        # the parent calls `set_level(0)` (which fires `on_set_level`)
        # synchronously from inside its constructor.
        self.water_level = {}
        self.target_level = {}
        self.valves = []
        self.pumps = []
        self.drains = []
        self.step_budget = 60
        self.water_sprites = {}
        self._is_animating = False
        self._anim_phase = 0
        self._anim_max = 3
        self._anim_droplets: list = []
        self._step_hud = StepCounterHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_hud],
        )
        super().__init__(
            game_id="xv2b",
            levels=levels,
            camera=camera,
            available_actions=[5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        data = LEVEL_DATA[self._current_level_index]
        self.step_budget = data["step_budget"]
        self._step_hud.set_max(self.step_budget)
        self.water_level = dict(data["start_levels"])
        self.target_level = dict(data["target_levels"])

        self.water_sprites = {}
        for vname in data["vessels"]:
            vx, vy = VESSEL_POS[vname]
            for s in level.get_sprites_by_tag("water_fill"):
                if s.x == vx + 2 and s.y == vy:
                    self.water_sprites[vname] = s
                    break

        self.valves = []
        for v in data["valves"]:
            vy_pos = _slit_to_valve_y(v["slit_h"])
            closed_sprite = None
            open_sprite = None
            for s in level.get_sprites_by_tag("valve"):
                if s.x == v["gap_x"] and s.y == vy_pos:
                    if "valve_closed" in s.tags:
                        closed_sprite = s
                    elif "valve_open" in s.tags:
                        open_sprite = s
            self.valves.append(
                {
                    "id": v["id"],
                    "left": v["left"],
                    "right": v["right"],
                    "slit_h": v["slit_h"],
                    "is_open": bool(v["start_open"]),
                    "closed_sprite": closed_sprite,
                    "open_sprite": open_sprite,
                }
            )

        self.pumps = []
        for p in data["pumps"]:
            off_sprite = None
            on_sprite = None
            for s in level.get_sprites_by_tag("pump"):
                if s.x == p["gap_x"] and s.y == p["gap_y"]:
                    if "pump_off" in s.tags:
                        off_sprite = s
                    elif "pump_on" in s.tags:
                        on_sprite = s
            self.pumps.append(
                {
                    "id": p["id"],
                    "source": p["source"],
                    "destination": p["destination"],
                    "is_on": False,
                    "off_sprite": off_sprite,
                    "on_sprite": on_sprite,
                }
            )

        self.drains = list(data["drains"])

        # Reset any in-flight animation state when a level starts.
        if self._anim_droplets:
            for droplet in self._anim_droplets:
                try:
                    level.remove_sprite(droplet)
                except Exception:
                    pass
        self._anim_droplets = []
        self._is_animating = False
        self._anim_phase = 0

        for vname in self.water_level:
            self._render_water(vname)

    def _render_water(self, vname: str) -> None:
        if vname not in self.water_sprites:
            return
        h = self.water_level[vname]
        sprite = self.water_sprites[vname]
        new_pixels = np.full((INTERIOR_HEIGHT, 8), -1, dtype=np.int8)
        if h > 0:
            top_row = INTERIOR_HEIGHT - h
            new_pixels[top_row:INTERIOR_HEIGHT, :] = 9
            new_pixels[top_row, :] = 10
        sprite.pixels = new_pixels

    def _toggle_valve(self, valve) -> None:
        if valve["is_open"]:
            valve["is_open"] = False
            valve["open_sprite"].set_visible(False).set_interaction(InteractionMode.REMOVED)
            valve["closed_sprite"].set_visible(True).set_interaction(InteractionMode.TANGIBLE)
        else:
            valve["is_open"] = True
            valve["closed_sprite"].set_visible(False).set_interaction(InteractionMode.REMOVED)
            valve["open_sprite"].set_visible(True).set_interaction(InteractionMode.TANGIBLE)

    def _toggle_pump(self, pump) -> None:
        if pump["is_on"]:
            pump["is_on"] = False
            pump["on_sprite"].set_visible(False).set_interaction(InteractionMode.REMOVED)
            pump["off_sprite"].set_visible(True).set_interaction(InteractionMode.TANGIBLE)
        else:
            pump["is_on"] = True
            pump["off_sprite"].set_visible(False).set_interaction(InteractionMode.REMOVED)
            pump["on_sprite"].set_visible(True).set_interaction(InteractionMode.TANGIBLE)

    def _water_surface_pos(self, vname: str) -> tuple:
        """Centre column of the vessel, at the row of the topmost filled cell."""
        vx, vy = VESSEL_POS[vname]
        level = self.water_level.get(vname, 0)
        if level <= 0:
            surface_y = vy + INTERIOR_HEIGHT - 1
        else:
            surface_y = vy + (INTERIOR_HEIGHT - level)
        return (vx + 5, surface_y)

    def _drain_pos(self, vname: str) -> tuple:
        vx, vy = VESSEL_POS[vname]
        return (vx + 7, vy + 27)

    def _valve_centre(self, valve) -> tuple:
        s = valve["closed_sprite"] if valve["closed_sprite"] is not None else valve["open_sprite"]
        return (s.x + 1, s.y + 2)

    def _pump_centre(self, pump) -> tuple:
        s = pump["off_sprite"] if pump["off_sprite"] is not None else pump["on_sprite"]
        return (s.x + 2, s.y + 1)

    def _simulate_tick(self) -> list:
        """Apply one tick of hydrostatic simulation and return the events list
        consumed by the animation system. Each event is a dict with keys
        `src`, `mid`, `dst` (grid coordinates) plus a `type` tag."""
        snap = dict(self.water_level)
        deltas = {v: 0 for v in self.water_level}
        events: list = []

        for valve in self.valves:
            if not valve["is_open"]:
                continue
            L = valve["left"]
            R = valve["right"]
            H = valve["slit_h"]
            if snap[L] > snap[R] and snap[L] > H:
                deltas[L] -= 1
                deltas[R] += 1
                events.append({
                    "type": "valve",
                    "src": self._water_surface_pos(L),
                    "mid": self._valve_centre(valve),
                    "dst": self._water_surface_pos(R),
                })
            elif snap[R] > snap[L] and snap[R] > H:
                deltas[R] -= 1
                deltas[L] += 1
                events.append({
                    "type": "valve",
                    "src": self._water_surface_pos(R),
                    "mid": self._valve_centre(valve),
                    "dst": self._water_surface_pos(L),
                })

        for pump in self.pumps:
            if not pump["is_on"]:
                continue
            S = pump["source"]
            D = pump["destination"]
            if snap[S] > 0:
                deltas[S] -= 1
                deltas[D] += 1
                events.append({
                    "type": "pump",
                    "src": self._water_surface_pos(S),
                    "mid": self._pump_centre(pump),
                    "dst": self._water_surface_pos(D),
                })

        for v in self.water_level:
            new_level = self.water_level[v] + deltas[v]
            if new_level < 0:
                new_level = 0
            if new_level > INTERIOR_HEIGHT:
                new_level = INTERIOR_HEIGHT
            self.water_level[v] = new_level

        for vname in self.drains:
            if self.water_level[vname] > 0:
                surface_before = self._water_surface_pos(vname)
                self.water_level[vname] -= 1
                events.append({
                    "type": "drain",
                    "src": surface_before,
                    "mid": self._drain_pos(vname),
                    "dst": self._drain_pos(vname),
                })

        for vname in self.water_level:
            self._render_water(vname)

        return events

    def _start_animation(self, events: list) -> None:
        self._is_animating = True
        self._anim_phase = 0
        self._anim_max = 3
        self._anim_droplets = []
        for event in events:
            droplet = sprites["flow_droplet"].clone()
            sx, sy = event["src"]
            droplet.set_position(sx, sy)
            droplet._anim_path = (event["src"], event["mid"], event["dst"])
            self.current_level.add_sprite(droplet)
            self._anim_droplets.append(droplet)

    def _advance_animation(self) -> bool:
        """Step the animation forward by one frame. Returns True when the
        animation has finished and the engine should accept the next action."""
        self._anim_phase += 1
        if self._anim_phase >= self._anim_max:
            for droplet in self._anim_droplets:
                try:
                    self.current_level.remove_sprite(droplet)
                except Exception:
                    pass
            self._anim_droplets = []
            self._is_animating = False
            self._anim_phase = 0
            return True
        for droplet in self._anim_droplets:
            path = getattr(droplet, "_anim_path", None)
            if not path:
                continue
            if self._anim_phase < len(path):
                px, py = path[self._anim_phase]
                droplet.set_position(px, py)
        return False

    def _check_win(self) -> bool:
        for v, target in self.target_level.items():
            if self.water_level[v] != target:
                return False
        return True

    def _check_unwinnable(self) -> bool:
        cur_total = sum(self.water_level.values())
        target_total = sum(self.target_level.values())
        return cur_total < target_total

    def _finalize_tick(self) -> None:
        if self._check_win():
            self.next_level()
            self.complete_action()
            return
        if self._check_unwinnable():
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def step(self) -> None:
        self._step_hud.set_current(self.step_budget - self._action_count)
        if self._action_count >= self.step_budget:
            self.lose()
            self.complete_action()
            return

        # Mid-animation: advance one frame; only finalize when the animation
        # has played out fully so the player sees all the flow indicators.
        if self._is_animating:
            done = self._advance_animation()
            if done:
                self._finalize_tick()
            return

        action = self.action

        if action.id == GameAction.ACTION6:
            x = action.data.get("x", -1)
            y = action.data.get("y", -1)
            grid = self.camera.display_to_grid(int(x), int(y))
            if grid is not None:
                gx, gy = grid
                clicked = self.current_level.get_sprite_at(gx, gy)
                if clicked is not None:
                    if "valve" in clicked.tags:
                        for v in self.valves:
                            if v["closed_sprite"] is clicked or v["open_sprite"] is clicked:
                                self._toggle_valve(v)
                                break
                    elif "pump" in clicked.tags:
                        for p in self.pumps:
                            if p["off_sprite"] is clicked or p["on_sprite"] is clicked:
                                self._toggle_pump(p)
                                break
            self.complete_action()
            return

        if action.id == GameAction.ACTION5:
            events = self._simulate_tick()
            if events:
                self._start_animation(events)
                return
            self._finalize_tick()
            return

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        h = np.zeros((4, 4), dtype=np.int16)
        h[0, 0] = self._step_hud.current
        for i, vname in enumerate(sorted(self.water_level.keys())):
            if i < 4:
                h[1, i] = self.water_level[vname]
        for i, v in enumerate(self.valves):
            if i < 4:
                h[2, i] = 1 if v["is_open"] else 0
        for i, p in enumerate(self.pumps):
            if i < 4:
                h[3, i] = 1 if p["is_on"] else 0
        return h
