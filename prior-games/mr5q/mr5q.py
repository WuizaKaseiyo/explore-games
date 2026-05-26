"""Generated game (id mr5q)."""

from collections import deque

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

GREEN_RING = 14
ORANGE_RING = 12
PLUS_FILL = 11   # yellow
MINUS_FILL = 6   # magenta

ORB_SIZE = 9

WALL_COLOR_A = 3   # mid-grey
WALL_COLOR_B = 4   # off-black


def _orb_plus_pixels(ring: int) -> list[list[int]]:
    """9×9 sprite: outer ring + interior plus-cross in PLUS_FILL."""
    P = -1
    F = PLUS_FILL
    return [
        [ring, ring, ring, ring, ring, ring, ring, ring, ring],
        [ring,    P,    P,    P,    P,    P,    P,    P, ring],
        [ring,    P,    P,    P,    F,    P,    P,    P, ring],
        [ring,    P,    P,    P,    F,    P,    P,    P, ring],
        [ring,    P,    F,    F,    F,    F,    F,    P, ring],
        [ring,    P,    P,    P,    F,    P,    P,    P, ring],
        [ring,    P,    P,    P,    F,    P,    P,    P, ring],
        [ring,    P,    P,    P,    P,    P,    P,    P, ring],
        [ring, ring, ring, ring, ring, ring, ring, ring, ring],
    ]


def _orb_minus_pixels(ring: int) -> list[list[int]]:
    """9×9 sprite: outer ring + interior horizontal bar in MINUS_FILL."""
    P = -1
    F = MINUS_FILL
    return [
        [ring, ring, ring, ring, ring, ring, ring, ring, ring],
        [ring,    P,    P,    P,    P,    P,    P,    P, ring],
        [ring,    P,    P,    P,    P,    P,    P,    P, ring],
        [ring,    P,    P,    P,    P,    P,    P,    P, ring],
        [ring,    P,    F,    F,    F,    F,    F,    P, ring],
        [ring,    P,    P,    P,    P,    P,    P,    P, ring],
        [ring,    P,    P,    P,    P,    P,    P,    P, ring],
        [ring,    P,    P,    P,    P,    P,    P,    P, ring],
        [ring, ring, ring, ring, ring, ring, ring, ring, ring],
    ]


def _wall_pixels() -> list[list[int]]:
    """3×3 hatched-grey pattern; visually distinct from the orb ring & gate frame."""
    a = WALL_COLOR_B
    b = WALL_COLOR_A
    return [
        [a, b, a],
        [b, a, b],
        [a, b, a],
    ]


sprites = {
    "orb_green_plus": Sprite(
        pixels=_orb_plus_pixels(GREEN_RING),
        name="orb_green_plus",
        visible=True,
        collidable=True,
        tags=["orb", "green", "plus", "sys_click"],
    ),
    "orb_green_minus": Sprite(
        pixels=_orb_minus_pixels(GREEN_RING),
        name="orb_green_minus",
        visible=True,
        collidable=True,
        tags=["orb", "green", "minus", "sys_click"],
    ),
    "orb_orange_plus": Sprite(
        pixels=_orb_plus_pixels(ORANGE_RING),
        name="orb_orange_plus",
        visible=True,
        collidable=True,
        tags=["orb", "orange", "plus", "sys_click"],
    ),
    "orb_orange_minus": Sprite(
        pixels=_orb_minus_pixels(ORANGE_RING),
        name="orb_orange_minus",
        visible=True,
        collidable=True,
        tags=["orb", "orange", "minus", "sys_click"],
    ),
    "wall": Sprite(
        pixels=_wall_pixels(),
        name="wall",
        visible=True,
        collidable=True,
        tags=["wall"],
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

GRID = 64


def _orb_pair(colour: str, x: int, y: int, active: str) -> list[Sprite]:
    """Place one orb instance: both polarity variants pre-placed at (x, y),
    one TANGIBLE and one REMOVED (the universal-scaffold's two-sprite swap)."""
    plus = sprites[f"orb_{colour}_plus"].clone().set_position(x, y)
    minus = sprites[f"orb_{colour}_minus"].clone().set_position(x, y)
    if active == "plus":
        minus.set_interaction(InteractionMode.REMOVED)
    else:
        plus.set_interaction(InteractionMode.REMOVED)
    return [plus, minus]


def _wall_block(x: int, y: int, w_cells: int, h_cells: int) -> list[Sprite]:
    """Tile a rectangular block with 3×3 wall sprites at (x, y) of size (w_cells, h_cells) — w/h
    given in 3-cell units."""
    out = []
    for dx in range(w_cells):
        for dy in range(h_cells):
            out.append(
                sprites["wall"].clone().set_position(x + dx * 3, y + dy * 3)
            )
    return out


level_1 = Level(
    sprites=(
        _orb_pair("green", 8, 28, "plus")
        + _orb_pair("green", 47, 28, "plus")
    ),
    grid_size=(GRID, GRID),
    data={"step_budget": 60},
)

level_2 = Level(
    sprites=(
        # Green pair on the upper row.
        _orb_pair("green", 8, 12, "plus")
        + _orb_pair("green", 47, 12, "plus")
        # Orange pair on the lower row.
        + _orb_pair("orange", 8, 38, "plus")
        + _orb_pair("orange", 47, 38, "plus")
    ),
    grid_size=(GRID, GRID),
    data={"step_budget": 140},
)

level_3 = Level(
    sprites=(
        # Green pair on the upper row — direct fusion, no obstacles.
        _orb_pair("green", 6, 6, "plus")
        + _orb_pair("green", 49, 6, "plus")
        # Orange pair on the lower row — a wall pillar in the middle forces a detour.
        + _orb_pair("orange", 4, 36, "plus")
        + _orb_pair("orange", 51, 36, "plus")
        # Vertical wall pillar centred at x=27..29, spanning y=22..49 (9 wall sprites tall).
        + _wall_block(27, 22, 1, 9)
    ),
    grid_size=(GRID, GRID),
    data={"step_budget": 240},
)

levels = [level_1, level_2, level_3]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 5  # black
PADDING_COLOR = 5


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------


class StepCounterHud(RenderableUserDisplay):
    """Depleting horizontal bar in row 0; left-aligned filled prefix = remaining."""

    def __init__(self, max_steps: int = 0) -> None:
        self.max_steps = max_steps
        self.current = max_steps

    def set_max(self, m: int) -> None:
        self.max_steps = m
        self.current = m

    def set_value(self, current: int) -> None:
        self.current = max(0, min(self.max_steps, current))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        filled = round(64 * (self.current / self.max_steps))
        for x in range(64):
            frame[0, x] = 14 if x < filled else 4
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------


class Mr5q(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_ui = StepCounterHud(max_steps=60)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        super().__init__(
            game_id="mr5q",
            levels=levels,
            camera=camera,
            available_actions=[5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        budget = level.get_data("step_budget") or 60
        self._step_counter_ui.set_max(budget)
        self._step_budget = budget
        self._steps_taken = 0

        # Build the orb-instance list. Each instance has the two pre-paired sprite
        # variants at the same cell; one is TANGIBLE, the other REMOVED.
        self._orbs = []
        seen = set()
        for sprite in level.get_sprites_by_tag("orb"):
            colour = self._orb_colour(sprite)
            key = (sprite.x, sprite.y, colour)
            if key in seen:
                continue
            plus_sprite = self._find_orb_at(level, sprite.x, sprite.y, colour, "plus")
            minus_sprite = self._find_orb_at(level, sprite.x, sprite.y, colour, "minus")
            if plus_sprite is None or minus_sprite is None:
                continue
            seen.add(key)
            active = "plus" if plus_sprite.interaction == InteractionMode.TANGIBLE else "minus"
            self._orbs.append(
                {
                    "plus": plus_sprite,
                    "minus": minus_sprite,
                    "colour": colour,
                    "active": active,
                    "alive": True,
                }
            )

        # Cache static obstacles.
        self._wall_cells = self._compute_wall_cells(level)

    def _compute_wall_cells(self, level: Level) -> set:
        """Return the set of grid cells covered by any wall sprite's pixel pattern."""
        cells = set()
        for w in level.get_sprites_by_tag("wall"):
            for dy in range(w.pixels.shape[0]):
                for dx in range(w.pixels.shape[1]):
                    if w.pixels[dy, dx] >= 0:
                        cells.add((w.x + dx, w.y + dy))
        return cells

    def step(self) -> None:
        if self.action.id == GameAction.ACTION6:
            self._handle_click()
        elif self.action.id == GameAction.ACTION5:
            self._handle_tick()

        self._steps_taken += 1
        remaining = self._step_budget - self._steps_taken
        self._step_counter_ui.set_value(remaining)

        if self._check_win():
            self.complete_action()
            self.next_level()
            return

        if remaining <= 0:
            self.lose()

        self.complete_action()

    def _handle_click(self) -> None:
        px = self.action.data.get("x", -1)
        py = self.action.data.get("y", -1)
        coords = self.camera.display_to_grid(int(px), int(py))
        if not coords:
            return
        gx, gy = coords
        for orb in self._orbs:
            if not orb["alive"]:
                continue
            ox, oy = self._orb_pos(orb)
            if ox <= gx < ox + ORB_SIZE and oy <= gy < oy + ORB_SIZE:
                self._flip_orb(orb)
                return

    def _flip_orb(self, orb: dict) -> None:
        old = orb["active"]
        new = "minus" if old == "plus" else "plus"
        orb[old].set_interaction(InteractionMode.REMOVED)
        orb[new].set_interaction(InteractionMode.TANGIBLE)
        orb["active"] = new

    def _handle_tick(self) -> None:
        positions = {
            i: self._orb_pos(o) for i, o in enumerate(self._orbs) if o["alive"]
        }

        desires = {}
        for i, orb in enumerate(self._orbs):
            if not orb["alive"]:
                continue
            target_idx = self._find_attract_target(i)
            if target_idx is None:
                desires[i] = (0, 0)
                continue
            dx, dy = self._attract_step(
                positions[i], positions[target_idx], positions, i
            )
            desires[i] = (dx, dy)

        # Resolve conflicts: two orbs heading to the same cell → both stall.
        dest_map: dict = {}
        for i, (dx, dy) in desires.items():
            if (dx, dy) == (0, 0):
                continue
            sx, sy = positions[i]
            dest = (sx + dx, sy + dy)
            dest_map.setdefault(dest, []).append(i)
        for dest, indices in dest_map.items():
            if len(indices) > 1:
                for i in indices:
                    desires[i] = (0, 0)

        # Apply moves to both polarity variants of each orb.
        for i, (dx, dy) in desires.items():
            if (dx, dy) == (0, 0):
                continue
            orb = self._orbs[i]
            orb["plus"].move(dx, dy)
            orb["minus"].move(dx, dy)

        # Discharge same-colour opposite-polarity orbs at edge-touching distance.
        self._resolve_discharges()

    def _find_attract_target(self, orb_idx: int) -> int | None:
        orb = self._orbs[orb_idx]
        my_pos = self._orb_pos(orb)
        my_colour = orb["colour"]
        opposite = "minus" if orb["active"] == "plus" else "plus"
        best_idx = None
        best_dist = None
        for i, other in enumerate(self._orbs):
            if not other["alive"] or i == orb_idx:
                continue
            if other["colour"] != my_colour:
                continue
            if other["active"] != opposite:
                continue
            opos = self._orb_pos(other)
            d = abs(opos[0] - my_pos[0]) + abs(opos[1] - my_pos[1])
            if best_dist is None or d < best_dist:
                best_dist = d
                best_idx = i
        return best_idx

    def _attract_step(
        self,
        source: tuple,
        target: tuple,
        positions: dict,
        my_idx: int,
    ) -> tuple:
        """BFS step toward edge-touching neighbourhood of target, with dominant-axis-toward-target
        priority on the BFS expansion order. Walls and other-orb footprints block."""
        sx, sy = source
        tx, ty = target
        if max(abs(sx - tx), abs(sy - ty)) <= ORB_SIZE:
            return (0, 0)
        gw = self.current_level.grid_size[0] if self.current_level.grid_size else 64
        gh = self.current_level.grid_size[1] if self.current_level.grid_size else 64
        dx = tx - sx
        dy = ty - sy
        sx_sign = 1 if dx > 0 else (-1 if dx < 0 else 0)
        sy_sign = 1 if dy > 0 else (-1 if dy < 0 else 0)
        order: list = []
        if abs(dx) >= abs(dy):
            if sx_sign != 0:
                order.append((sx_sign, 0))
            if sy_sign != 0:
                order.append((0, sy_sign))
        else:
            if sy_sign != 0:
                order.append((0, sy_sign))
            if sx_sign != 0:
                order.append((sx_sign, 0))
        for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if d not in order:
                order.append(d)

        visited = {source}
        parent: dict = {}
        queue = deque([source])
        found = None
        while queue:
            cur = queue.popleft()
            if max(abs(cur[0] - tx), abs(cur[1] - ty)) <= ORB_SIZE and cur != source:
                found = cur
                break
            for d in order:
                nx, ny = cur[0] + d[0], cur[1] + d[1]
                if (nx, ny) in visited:
                    continue
                if not self._cell_walkable(nx, ny, positions, my_idx, gw, gh):
                    continue
                visited.add((nx, ny))
                parent[(nx, ny)] = cur
                queue.append((nx, ny))
        if found is None:
            return (0, 0)
        cur = found
        while parent.get(cur) and parent[cur] != source:
            cur = parent[cur]
        if cur == source:
            return (0, 0)
        return (cur[0] - source[0], cur[1] - source[1])

    def _cell_walkable(
        self,
        x: int,
        y: int,
        positions: dict,
        my_idx: int,
        gw: int,
        gh: int,
    ) -> bool:
        # Bounds: orb top-left x..x+8 must fit in grid.
        if x < 0 or y < 0 or x + ORB_SIZE > gw or y + ORB_SIZE > gh:
            return False
        # Walls: any wall cell within the orb's footprint blocks.
        for dx in range(ORB_SIZE):
            for dy in range(ORB_SIZE):
                if (x + dx, y + dy) in self._wall_cells:
                    return False
        # Other-orb bbox overlap blocks.
        for j, opos in positions.items():
            if j == my_idx:
                continue
            ox, oy = opos
            if abs(ox - x) < ORB_SIZE and abs(oy - y) < ORB_SIZE:
                return False
        return True

    def _resolve_discharges(self) -> None:
        to_kill = set()
        for i, oi in enumerate(self._orbs):
            if not oi["alive"] or i in to_kill:
                continue
            for j in range(i + 1, len(self._orbs)):
                oj = self._orbs[j]
                if not oj["alive"] or j in to_kill:
                    continue
                if oi["colour"] != oj["colour"]:
                    continue
                if oi["active"] == oj["active"]:
                    continue
                ax, ay = self._orb_pos(oi)
                bx, by = self._orb_pos(oj)
                if max(abs(ax - bx), abs(ay - by)) <= ORB_SIZE:
                    to_kill.add(i)
                    to_kill.add(j)
        for idx in to_kill:
            orb = self._orbs[idx]
            orb["plus"].set_interaction(InteractionMode.REMOVED)
            orb["minus"].set_interaction(InteractionMode.REMOVED)
            orb["alive"] = False

    def _orb_pos(self, orb: dict) -> tuple:
        active = orb[orb["active"]]
        return (active.x, active.y)

    def _check_win(self) -> bool:
        return all(not o["alive"] for o in self._orbs)

    def _orb_colour(self, sprite: Sprite) -> str:
        for tag in sprite.tags:
            if tag in ("green", "orange"):
                return tag
        return ""

    def _find_orb_at(
        self,
        level: Level,
        x: int,
        y: int,
        colour: str,
        polarity: str,
    ) -> Sprite | None:
        for sprite in level.get_sprites_by_tag("orb"):
            if (
                sprite.x == x
                and sprite.y == y
                and (colour in sprite.tags)
                and (polarity in sprite.tags)
            ):
                return sprite
        return None

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._step_budget - self._steps_taken
        state[0, 1] = sum(1 for o in self._orbs if o["alive"])
        return state

    def _get_valid_actions(self) -> list[ActionInput]:
        actions = [ActionInput(id=GameAction.ACTION5)]
        for orb in self._orbs:
            if not orb["alive"]:
                continue
            x, y = self._orb_pos(orb)
            # Click pixel at the centre of the orb sprite.
            px = x + ORB_SIZE // 2
            py = y + ORB_SIZE // 2
            actions.append(
                ActionInput(id=GameAction.ACTION6, data={"x": int(px), "y": int(py)})
            )
        return actions
