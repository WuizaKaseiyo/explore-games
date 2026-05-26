"""NovaPlay game pf3w."""

from collections import deque

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
# 0. CONSTANTS
# ---------------------------------------------------------------------
LOGICAL_CELL_SIZE = 4
LOGICAL_GRID = 16
PIXEL_GRID = 64
BACKGROUND_COLOR = 1   # off-white
PADDING_COLOR = 5      # black
WALL_FRAME = 3         # grey
WALL_INNER = 4         # off-black
DIM_FRAME = 3          # grey for inactive slot
BLUE = 10              # light-blue
MAGENTA = 6            # magenta
DARK_INNER = 4         # off-black, inner-frame palette
YELLOW_CENTER = 11     # yellow

INF_DIST = 1_000_000
# Activating an emitter sets T_activated = current_global_tick - VISIBLE_RADIUS_OFFSET,
# so on the activation step the wavefront radius is 1 (hidden under the slot's arm
# cells -- no visible ripple yet, just the lit slot center) and the FIRST ACTION5
# after activation jumps the radius to 2, producing the first visible Manhattan-2
# ring outside the slot's 3x3 footprint.
VISIBLE_RADIUS_OFFSET = 1


# ---------------------------------------------------------------------
# 1. SPRITE PIXEL HELPERS
# ---------------------------------------------------------------------
def _filled(frame_color: int, inner_color: int) -> list[list[int]]:
    return [
        [frame_color, frame_color, frame_color, frame_color],
        [frame_color, inner_color, inner_color, frame_color],
        [frame_color, inner_color, inner_color, frame_color],
        [frame_color, frame_color, frame_color, frame_color],
    ]


def _hollow(frame_color: int) -> list[list[int]]:
    return [
        [frame_color, frame_color, frame_color, frame_color],
        [frame_color, -1, -1, frame_color],
        [frame_color, -1, -1, frame_color],
        [frame_color, frame_color, frame_color, frame_color],
    ]


def _trans() -> list[list[int]]:
    return [[-1] * 4 for _ in range(4)]


def _compose_3x3(cells: list[list[list[list[int]]]]) -> list[list[int]]:
    result = []
    for cr in range(3):
        for pr in range(4):
            row = []
            for cc in range(3):
                row.extend(cells[cr][cc][pr])
            result.append(row)
    return result


_T = _trans()

_emitter_dim_pixels = _compose_3x3([
    [_T, _hollow(DIM_FRAME), _T],
    [_hollow(DIM_FRAME), _T, _hollow(DIM_FRAME)],
    [_T, _hollow(DIM_FRAME), _T],
])

_emitter_lit_blue_pixels = _compose_3x3([
    [_T, _filled(BLUE, DARK_INNER), _T],
    [_filled(BLUE, DARK_INNER), _filled(YELLOW_CENTER, DARK_INNER), _filled(BLUE, DARK_INNER)],
    [_T, _filled(BLUE, DARK_INNER), _T],
])

_emitter_lit_magenta_pixels = _compose_3x3([
    [_T, _filled(MAGENTA, DARK_INNER), _T],
    [_filled(MAGENTA, DARK_INNER), _filled(YELLOW_CENTER, DARK_INNER), _filled(MAGENTA, DARK_INNER)],
    [_T, _filled(MAGENTA, DARK_INNER), _T],
])

_target_blue_pixels = _compose_3x3([
    [_hollow(BLUE), _hollow(BLUE), _hollow(BLUE)],
    [_hollow(BLUE), _T, _hollow(BLUE)],
    [_hollow(BLUE), _hollow(BLUE), _hollow(BLUE)],
])

_target_magenta_pixels = _compose_3x3([
    [_hollow(MAGENTA), _hollow(MAGENTA), _hollow(MAGENTA)],
    [_hollow(MAGENTA), _T, _hollow(MAGENTA)],
    [_hollow(MAGENTA), _hollow(MAGENTA), _hollow(MAGENTA)],
])

_wall_unit_pixels = [
    [WALL_FRAME, WALL_INNER, WALL_INNER, WALL_FRAME],
    [WALL_INNER, WALL_FRAME, WALL_FRAME, WALL_INNER],
    [WALL_INNER, WALL_FRAME, WALL_FRAME, WALL_INNER],
    [WALL_FRAME, WALL_INNER, WALL_INNER, WALL_FRAME],
]

_wavefront_blank_pixels = [[-1] * PIXEL_GRID for _ in range(PIXEL_GRID)]


# ---------------------------------------------------------------------
# 2. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "emitter_slot_dim_blue": Sprite(
        pixels=[row[:] for row in _emitter_dim_pixels],
        name="emitter_slot_dim_blue",
        visible=True,
        collidable=True,
        tags=["sys_click", "slot_dim", "slot_blue_color"],
    ),
    "emitter_slot_dim_magenta": Sprite(
        pixels=[row[:] for row in _emitter_dim_pixels],
        name="emitter_slot_dim_magenta",
        visible=True,
        collidable=True,
        tags=["sys_click", "slot_dim", "slot_magenta_color"],
    ),
    "emitter_slot_lit_blue": Sprite(
        pixels=[row[:] for row in _emitter_lit_blue_pixels],
        name="emitter_slot_lit_blue",
        visible=True,
        collidable=True,
        tags=["slot_lit", "emitter_blue"],
        layer=2,
    ),
    "emitter_slot_lit_magenta": Sprite(
        pixels=[row[:] for row in _emitter_lit_magenta_pixels],
        name="emitter_slot_lit_magenta",
        visible=True,
        collidable=True,
        tags=["slot_lit", "emitter_magenta"],
        layer=2,
    ),
    "target_blue": Sprite(
        pixels=[row[:] for row in _target_blue_pixels],
        name="target_blue",
        visible=True,
        collidable=True,
        tags=["target", "target_blue"],
        layer=2,
    ),
    "target_magenta": Sprite(
        pixels=[row[:] for row in _target_magenta_pixels],
        name="target_magenta",
        visible=True,
        collidable=True,
        tags=["target", "target_magenta"],
        layer=2,
    ),
    "wall_unit": Sprite(
        pixels=[row[:] for row in _wall_unit_pixels],
        name="wall_unit",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=0,
    ),
    "wavefront_blue": Sprite(
        pixels=[row[:] for row in _wavefront_blank_pixels],
        name="wavefront_blue",
        visible=True,
        collidable=False,
        tags=["wavefront", "wavefront_blue"],
        layer=1,
    ),
    "wavefront_magenta": Sprite(
        pixels=[row[:] for row in _wavefront_blank_pixels],
        name="wavefront_magenta",
        visible=True,
        collidable=False,
        tags=["wavefront", "wavefront_magenta"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 3. LEVEL BUILDERS
# ---------------------------------------------------------------------
def _border_walls() -> list[Sprite]:
    walls = []
    for lcx in range(LOGICAL_GRID):
        walls.append(
            sprites["wall_unit"]
            .clone()
            .set_position(lcx * LOGICAL_CELL_SIZE, 0)
        )
        walls.append(
            sprites["wall_unit"]
            .clone()
            .set_position(lcx * LOGICAL_CELL_SIZE, (LOGICAL_GRID - 1) * LOGICAL_CELL_SIZE)
        )
    for lcy in range(1, LOGICAL_GRID - 1):
        walls.append(
            sprites["wall_unit"]
            .clone()
            .set_position(0, lcy * LOGICAL_CELL_SIZE)
        )
        walls.append(
            sprites["wall_unit"]
            .clone()
            .set_position((LOGICAL_GRID - 1) * LOGICAL_CELL_SIZE, lcy * LOGICAL_CELL_SIZE)
        )
    return walls


def _l3_central_wall() -> list[Sprite]:
    walls = []
    for lcy in list(range(1, 7)) + list(range(8, LOGICAL_GRID - 1)):
        walls.append(
            sprites["wall_unit"]
            .clone()
            .set_position(8 * LOGICAL_CELL_SIZE, lcy * LOGICAL_CELL_SIZE)
        )
    return walls


def _slot_at(lcx_center: int, lcy_center: int, color: str) -> Sprite:
    name = "emitter_slot_dim_blue" if color == "blue" else "emitter_slot_dim_magenta"
    px = (lcx_center - 1) * LOGICAL_CELL_SIZE
    py = (lcy_center - 1) * LOGICAL_CELL_SIZE
    return sprites[name].clone().set_position(px, py)


def _target_at(lcx_center: int, lcy_center: int, color: str) -> Sprite:
    name = "target_blue" if color == "blue" else "target_magenta"
    px = (lcx_center - 1) * LOGICAL_CELL_SIZE
    py = (lcy_center - 1) * LOGICAL_CELL_SIZE
    return sprites[name].clone().set_position(px, py)


_l1_sprites = (
    _border_walls()
    + [
        _slot_at(3, 8, "blue"),
        _target_at(12, 8, "blue"),
        sprites["wavefront_blue"].clone().set_position(0, 0),
        sprites["wavefront_magenta"].clone().set_position(0, 0),
    ]
)

_l2_sprites = (
    _border_walls()
    + [
        _slot_at(3, 4, "blue"),
        _slot_at(3, 12, "blue"),
        _target_at(12, 4, "blue"),
        _target_at(10, 12, "blue"),
        sprites["wavefront_blue"].clone().set_position(0, 0),
        sprites["wavefront_magenta"].clone().set_position(0, 0),
    ]
)

_l3_sprites = (
    _border_walls()
    + _l3_central_wall()
    + [
        _slot_at(2, 2, "blue"),
        _slot_at(4, 13, "magenta"),
        _target_at(13, 13, "blue"),
        _target_at(13, 2, "magenta"),
        sprites["wavefront_blue"].clone().set_position(0, 0),
        sprites["wavefront_magenta"].clone().set_position(0, 0),
    ]
)

levels = [
    Level(sprites=_l1_sprites, grid_size=(PIXEL_GRID, PIXEL_GRID), data={"step_budget": 30}),
    Level(sprites=_l2_sprites, grid_size=(PIXEL_GRID, PIXEL_GRID), data={"step_budget": 35}),
    Level(sprites=_l3_sprites, grid_size=(PIXEL_GRID, PIXEL_GRID), data={"step_budget": 70}),
]


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self.max_steps = 0
        self.current_steps = 0

    def set_max(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_current(self, current_steps: int) -> None:
        self.current_steps = max(0, min(current_steps, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        ratio = self.current_steps / self.max_steps
        fill = round(PIXEL_GRID * ratio)
        for x in range(PIXEL_GRID):
            if x < fill:
                frame[0, x] = 14
            else:
                frame[0, x] = 5
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Pf3w(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_hud = StepCounterHud()
        self._global_tick: int = 0
        self._active_emitters: list[dict] = []
        self._walkable: np.ndarray | None = None
        self._max_steps: int = 0
        self._wavefront_blue_sprite: Sprite | None = None
        self._wavefront_magenta_sprite: Sprite | None = None
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_hud],
        )
        super().__init__(
            game_id="pf3w",
            levels=levels,
            camera=camera,
            available_actions=[5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        self.camera.width = PIXEL_GRID
        self.camera.height = PIXEL_GRID
        self._global_tick = 0
        self._active_emitters = []

        self._walkable = np.ones((LOGICAL_GRID, LOGICAL_GRID), dtype=bool)
        for wall in level.get_sprites_by_tag("wall"):
            lcx = wall.x // LOGICAL_CELL_SIZE
            lcy = wall.y // LOGICAL_CELL_SIZE
            if 0 <= lcx < LOGICAL_GRID and 0 <= lcy < LOGICAL_GRID:
                self._walkable[lcy, lcx] = False

        self._max_steps = level.get_data("step_budget") or 50
        self._step_counter_hud.set_max(self._max_steps)
        self._step_counter_hud.set_current(self._max_steps)

        wb = level.get_sprites_by_name("wavefront_blue")
        wm = level.get_sprites_by_name("wavefront_magenta")
        self._wavefront_blue_sprite = wb[0] if wb else None
        self._wavefront_magenta_sprite = wm[0] if wm else None
        if self._wavefront_blue_sprite is not None:
            self._wavefront_blue_sprite.pixels[:, :] = -1
        if self._wavefront_magenta_sprite is not None:
            self._wavefront_magenta_sprite.pixels[:, :] = -1

        for target in level.get_sprites_by_tag("target"):
            self._set_target_lit(target, lit=False)

    def _bfs_distances(self, start_lcx: int, start_lcy: int) -> np.ndarray:
        dist = np.full((LOGICAL_GRID, LOGICAL_GRID), INF_DIST, dtype=np.int32)
        if not (0 <= start_lcx < LOGICAL_GRID and 0 <= start_lcy < LOGICAL_GRID):
            return dist
        if self._walkable is None or not bool(self._walkable[start_lcy, start_lcx]):
            return dist
        dist[start_lcy, start_lcx] = 0
        q: deque[tuple[int, int]] = deque([(start_lcx, start_lcy)])
        while q:
            cx, cy = q.popleft()
            d = int(dist[cy, cx])
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < LOGICAL_GRID and 0 <= ny < LOGICAL_GRID:
                    if self._walkable[ny, nx] and dist[ny, nx] > d + 1:
                        dist[ny, nx] = d + 1
                        q.append((nx, ny))
        return dist

    def _activate_slot_at_pixel(self, click_px: int, click_py: int) -> bool:
        click_lcx = click_px // LOGICAL_CELL_SIZE
        click_lcy = click_py // LOGICAL_CELL_SIZE
        for slot in list(self.current_level.get_sprites_by_tag("slot_dim")):
            slot_lcx_tl = slot.x // LOGICAL_CELL_SIZE
            slot_lcy_tl = slot.y // LOGICAL_CELL_SIZE
            if (slot_lcx_tl <= click_lcx < slot_lcx_tl + 3
                    and slot_lcy_tl <= click_lcy < slot_lcy_tl + 3):
                if "slot_blue_color" in slot.tags:
                    color = "blue"
                    lit_template = "emitter_slot_lit_blue"
                else:
                    color = "magenta"
                    lit_template = "emitter_slot_lit_magenta"
                slot_x, slot_y = slot.x, slot.y
                center_lcx = slot_lcx_tl + 1
                center_lcy = slot_lcy_tl + 1
                self.current_level.remove_sprite(slot)
                lit = sprites[lit_template].clone().set_position(slot_x, slot_y)
                self.current_level.add_sprite(lit)
                dist = self._bfs_distances(center_lcx, center_lcy)
                self._active_emitters.append({
                    "sprite": lit,
                    "color": color,
                    "T_activated": self._global_tick - VISIBLE_RADIUS_OFFSET,
                    "center_lcx": center_lcx,
                    "center_lcy": center_lcy,
                    "distance_grid": dist,
                })
                return True
        return False

    def _paint_frontier_cell(self, sprite: Sprite, lcx: int, lcy: int, color_val: int) -> None:
        py0 = lcy * LOGICAL_CELL_SIZE
        px0 = lcx * LOGICAL_CELL_SIZE
        sprite.pixels[py0, px0:px0 + 4] = color_val
        sprite.pixels[py0 + 3, px0:px0 + 4] = color_val
        sprite.pixels[py0 + 1, px0] = color_val
        sprite.pixels[py0 + 1, px0 + 3] = color_val
        sprite.pixels[py0 + 2, px0] = color_val
        sprite.pixels[py0 + 2, px0 + 3] = color_val

    def _update_wavefront_sprites(self) -> None:
        if self._wavefront_blue_sprite is not None:
            self._wavefront_blue_sprite.pixels[:, :] = -1
        if self._wavefront_magenta_sprite is not None:
            self._wavefront_magenta_sprite.pixels[:, :] = -1
        for emitter in self._active_emitters:
            radius = self._global_tick - emitter["T_activated"]
            if radius < 0:
                continue
            if emitter["color"] == "blue":
                target_sprite = self._wavefront_blue_sprite
                color_val = BLUE
            else:
                target_sprite = self._wavefront_magenta_sprite
                color_val = MAGENTA
            if target_sprite is None:
                continue
            mask = (emitter["distance_grid"] == radius)
            cells = np.argwhere(mask)
            for lcy, lcx in cells:
                self._paint_frontier_cell(target_sprite, int(lcx), int(lcy), color_val)

    def _set_target_lit(self, target: Sprite, lit: bool) -> None:
        if lit:
            center_pixels = np.array(_filled(YELLOW_CENTER, DARK_INNER), dtype=target.pixels.dtype)
            target.pixels[4:8, 4:8] = center_pixels
        else:
            target.pixels[4:8, 4:8] = -1

    def _is_cell_in_frontier(self, lcx: int, lcy: int, color: str) -> bool:
        for emitter in self._active_emitters:
            if emitter["color"] != color:
                continue
            radius = self._global_tick - emitter["T_activated"]
            if radius < 0:
                continue
            if 0 <= lcy < LOGICAL_GRID and 0 <= lcx < LOGICAL_GRID:
                if int(emitter["distance_grid"][lcy, lcx]) == radius:
                    return True
        return False

    def _update_target_lit_states(self) -> None:
        for target in self.current_level.get_sprites_by_tag("target"):
            target_lcx_tl = target.x // LOGICAL_CELL_SIZE
            target_lcy_tl = target.y // LOGICAL_CELL_SIZE
            center_lcx = target_lcx_tl + 1
            center_lcy = target_lcy_tl + 1
            color = "blue" if "target_blue" in target.tags else "magenta"
            self._set_target_lit(target, self._is_cell_in_frontier(center_lcx, center_lcy, color))

    def _all_targets_lit(self) -> bool:
        for target in self.current_level.get_sprites_by_tag("target"):
            target_lcx_tl = target.x // LOGICAL_CELL_SIZE
            target_lcy_tl = target.y // LOGICAL_CELL_SIZE
            center_lcx = target_lcx_tl + 1
            center_lcy = target_lcy_tl + 1
            color = "blue" if "target_blue" in target.tags else "magenta"
            if not self._is_cell_in_frontier(center_lcx, center_lcy, color):
                return False
        return True

    def step(self) -> None:
        self._step_counter_hud.set_current(self._max_steps - self._action_count)
        if self._action_count >= self._max_steps:
            self.lose()
            self.complete_action()
            return

        if self.action.id == GameAction.ACTION6:
            click_x = int(self.action.data.get("x", -1))
            click_y = int(self.action.data.get("y", -1))
            converted = self.camera.display_to_grid(click_x, click_y)
            if converted:
                px, py = converted
                self._activate_slot_at_pixel(int(px), int(py))
        elif self.action.id == GameAction.ACTION5:
            self._global_tick += 1

        self._update_wavefront_sprites()
        self._update_target_lit_states()

        if self._all_targets_lit():
            self.next_level()
            self.complete_action()
            return

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._global_tick
        state[0, 1] = self._max_steps - self._action_count
        return state

    def _get_valid_actions(self) -> list[ActionInput]:
        valid: list[ActionInput] = [ActionInput(id=GameAction.ACTION5)]
        for slot in self.current_level.get_sprites_by_tag("slot_dim"):
            center_px = slot.x + LOGICAL_CELL_SIZE + 1
            center_py = slot.y + LOGICAL_CELL_SIZE + 1
            valid.append(
                ActionInput(
                    id=GameAction.ACTION6,
                    data={"x": center_px, "y": center_py},
                )
            )
        return valid
