"""gv47 — generated puzzle environment."""

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
# Palette constants
# ---------------------------------------------------------------------
WHITE = 0
LIGHT_GREY = 2
GREY = 3
WALL_COLOR = 4
RED = 8
BLUE = 9
LIGHT_BLUE = 10
YELLOW = 11
GREEN = 14
PURPLE = 15

BACKGROUND_COLOR = LIGHT_GREY
PADDING_COLOR = GREY


# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "seed_yellow": Sprite(
        pixels=[
            [YELLOW, YELLOW, YELLOW],
            [YELLOW, WHITE,  YELLOW],
            [YELLOW, YELLOW, YELLOW],
        ],
        name="seed_yellow",
        visible=True,
        collidable=True,
        tags=["seed", "yellow", "sys_click"],
        layer=1,
    ),
    "seed_blue": Sprite(
        pixels=[
            [BLUE, BLUE, BLUE],
            [BLUE, WHITE, BLUE],
            [BLUE, BLUE, BLUE],
        ],
        name="seed_blue",
        visible=True,
        collidable=True,
        tags=["seed", "blue", "sys_click"],
        layer=1,
    ),
    "seed_red": Sprite(
        pixels=[
            [RED, RED, RED],
            [RED, WHITE, RED],
            [RED, RED, RED],
        ],
        name="seed_red",
        visible=True,
        collidable=True,
        tags=["seed", "red", "sys_click"],
        layer=1,
    ),
    "wall_block": Sprite(
        pixels=[[WALL_COLOR]],
        name="wall_block",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=1,
    ),
    "target_yellow": Sprite(
        pixels=[[YELLOW]],
        name="target_yellow",
        visible=True,
        collidable=True,
        tags=["target", "target_yellow"],
        layer=2,
    ),
    "target_blue": Sprite(
        pixels=[[BLUE]],
        name="target_blue",
        visible=True,
        collidable=True,
        tags=["target", "target_blue"],
        layer=2,
    ),
    "target_red": Sprite(
        pixels=[[RED]],
        name="target_red",
        visible=True,
        collidable=True,
        tags=["target", "target_red"],
        layer=2,
    ),
    "target_green": Sprite(
        pixels=[[GREEN]],
        name="target_green",
        visible=True,
        collidable=True,
        tags=["target", "target_green"],
        layer=2,
    ),
    "target_purple": Sprite(
        pixels=[[PURPLE]],
        name="target_purple",
        visible=True,
        collidable=True,
        tags=["target", "target_purple"],
        layer=2,
    ),
}


_TARGET_COLOR = {
    "target_yellow": YELLOW,
    "target_blue":   BLUE,
    "target_red":    RED,
    "target_green":  GREEN,
    "target_purple": PURPLE,
}

_SEED_COLOR = {
    "yellow": YELLOW,
    "blue":   BLUE,
    "red":    RED,
}


# ---------------------------------------------------------------------
# Level helpers
# ---------------------------------------------------------------------
def _wall_column(x: int, ys) -> list[Sprite]:
    return [sprites["wall_block"].clone().set_position(x, y) for y in ys]


def _wall_row(y: int, xs) -> list[Sprite]:
    return [sprites["wall_block"].clone().set_position(x, y) for x in xs]


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

# L1: single yellow seed, single yellow pip target. The player paints
# the 8 cells around the pip with yellow; the ring auto-dissolves.
_l1_sprites = [
    sprites["seed_yellow"].clone().set_position(1, 1),
    sprites["target_yellow"].clone().set_position(8, 4),
    *_wall_column(5, [2, 5, 6]),
]

# L2: yellow + blue seeds. Yellow target at the top-edge corner so
# yellow can dissolve it without first contacting blue. Green target
# in the centre needs the yellow+blue mix to produce green paint.
_l2_sprites = [
    sprites["seed_yellow"].clone().set_position(1, 1),
    sprites["seed_blue"].clone().set_position(8, 8),
    sprites["target_yellow"].clone().set_position(10, 1),
    sprites["target_green"].clone().set_position(5, 5),
]

# L3: yellow + blue + red seeds. Yellow target at top-edge (single
# colour). Purple target south of centre, reachable by red+blue mix.
_l3_sprites = [
    sprites["seed_yellow"].clone().set_position(1, 1),
    sprites["seed_red"].clone().set_position(1, 8),
    sprites["seed_blue"].clone().set_position(8, 8),
    sprites["target_yellow"].clone().set_position(5, 1),
    sprites["target_purple"].clone().set_position(5, 8),
]


levels = [
    Level(
        sprites=_l1_sprites,
        grid_size=(12, 12),
        data={
            "step_budget": 30,
            "mix_table": [],
        },
    ),
    Level(
        sprites=_l2_sprites,
        grid_size=(12, 12),
        data={
            "step_budget": 60,
            "mix_table": [(YELLOW, BLUE, GREEN)],
        },
    ),
    Level(
        sprites=_l3_sprites,
        grid_size=(12, 12),
        data={
            "step_budget": 100,
            "mix_table": [(RED, BLUE, PURPLE)],
        },
    ),
]


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0) -> None:
        self.max_steps = max_steps
        self.current = max_steps

    def set_max(self, n: int) -> None:
        self.max_steps = n
        self.current = n

    def set_current(self, n: int) -> None:
        self.current = max(0, min(n, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.current / self.max_steps
        filled = int(round(64 * ratio))
        for x in range(64):
            frame[0, x] = GREEN if x < filled else WHITE
        return frame


class TargetRingHud(RenderableUserDisplay):
    """Draws a 1-pixel-thick black ring tightly around each target pip.
    The ring sits at the pixel row immediately outside the pip cell's
    rendered 5×5 area, hugging the pip with no gap."""

    def __init__(self, game: "Gv47") -> None:
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        level = getattr(self.game, "current_level", None)
        if level is None:
            return frame
        try:
            targets = list(level.get_sprites_by_tag("target"))
        except Exception:
            return frame
        if not targets:
            return frame
        gw, gh = level.grid_size or (64, 64)
        scale = max(1, min(64 // gw, 64 // gh))
        ox = (64 - gw * scale) // 2
        oy = (64 - gh * scale) // 2
        for t in targets:
            tx, ty = t.x, t.y
            # Pip's rendered pixel range (inclusive):
            px0 = tx * scale + ox
            py0 = ty * scale + oy
            px1 = px0 + scale - 1
            py1 = py0 + scale - 1
            # 1-pixel ring just outside the pip's pixel area.
            x0 = max(0, px0 - 1)
            y0 = max(0, py0 - 1)
            x1 = min(63, px1 + 1)
            y1 = min(63, py1 + 1)
            if x1 < x0 or y1 < y0:
                continue
            for x in range(x0, x1 + 1):
                if py0 - 1 >= 0:
                    frame[py0 - 1, x] = WALL_COLOR
                if py1 + 1 <= 63:
                    frame[py1 + 1, x] = WALL_COLOR
            for y in range(y0, y1 + 1):
                if px0 - 1 >= 0:
                    frame[y, px0 - 1] = WALL_COLOR
                if px1 + 1 <= 63:
                    frame[y, px1 + 1] = WALL_COLOR
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Gv47(NovaBaseGame):
    def __init__(self) -> None:
        self.step_hud = StepCounterHud(0)
        self.ring_hud = TargetRingHud(self)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_hud, self.ring_hud],
        )
        self.regions: dict[str, set[tuple[int, int]]] = {}
        self.region_color: dict[str, int] = {}
        self.region_seeds: dict[str, list[Sprite]] = {}
        self.paint_sprites: dict[tuple[int, int], Sprite] = {}
        self.last_grown: str | None = None
        self.steps_remaining: int = 0
        self.max_steps: int = 0
        self.mix_table: dict[frozenset, int] = {}
        self._next_region_id: int = 0
        super().__init__(
            game_id="gv47",
            levels=levels,
            camera=camera,
            available_actions=[5, 6],
        )

    # ----- per-level setup ----------------------------------------
    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh

        for s in list(level.get_sprites_by_tag("paint")):
            level.remove_sprite(s)

        self.regions = {}
        self.region_color = {}
        self.region_seeds = {}
        self.paint_sprites = {}
        self.last_grown = None
        self._next_region_id = 0

        budget = level.get_data("step_budget") or 50
        self.max_steps = int(budget)
        self.steps_remaining = self.max_steps
        self.step_hud.set_max(self.max_steps)
        self.step_hud.set_current(self.steps_remaining)

        raw_table = level.get_data("mix_table") or []
        mt: dict[frozenset, int] = {}
        for triple in raw_table:
            a, b, out = triple
            mt[frozenset((int(a), int(b)))] = int(out)
        self.mix_table = mt

        for seed in level.get_sprites_by_tag("seed"):
            color = self._seed_color(seed)
            mask = (seed.pixels >= 0) & (seed.pixels != WHITE)
            seed.pixels[mask] = color

        for seed in level.get_sprites_by_tag("seed"):
            rid = self._new_region_id()
            color = self._seed_color(seed)
            cells = self._sprite_cells(seed)
            self.regions[rid] = cells
            self.region_color[rid] = color
            self.region_seeds[rid] = [seed]

    # ----- helpers ------------------------------------------------
    def _new_region_id(self) -> str:
        rid = f"r{self._next_region_id}"
        self._next_region_id += 1
        return rid

    def _seed_color(self, seed: Sprite) -> int:
        for tag, color in _SEED_COLOR.items():
            if seed.tags and tag in seed.tags:
                return color
        return YELLOW

    def _target_pip_color(self, sprite: Sprite) -> int | None:
        if not sprite.tags:
            return None
        for tag, color in _TARGET_COLOR.items():
            if tag in sprite.tags:
                return color
        return None

    def _sprite_cells(self, sprite: Sprite) -> set[tuple[int, int]]:
        cells: set[tuple[int, int]] = set()
        h, w = sprite.pixels.shape
        for dy in range(h):
            for dx in range(w):
                if int(sprite.pixels[dy, dx]) >= 0:
                    cells.add((sprite.x + dx, sprite.y + dy))
        return cells

    def _blocked_cells(self) -> set[tuple[int, int]]:
        cells: set[tuple[int, int]] = set()
        for w in self.current_level.get_sprites_by_tag("wall"):
            cells |= self._sprite_cells(w)
        for t in self.current_level.get_sprites_by_tag("target"):
            cells |= self._sprite_cells(t)
        return cells

    def _all_painted(self) -> set[tuple[int, int]]:
        out: set[tuple[int, int]] = set()
        for cells in self.regions.values():
            out |= cells
        return out

    def _add_paint(self, x: int, y: int, color: int) -> None:
        s = Sprite(
            pixels=[[int(color)]],
            name=f"paint_{x}_{y}",
            visible=True,
            collidable=False,
            tags=["paint"],
            layer=-1,
        )
        s.set_position(x, y)
        self.current_level.add_sprite(s)
        self.paint_sprites[(x, y)] = s

    def _set_paint_color(self, x: int, y: int, color: int) -> None:
        s = self.paint_sprites.get((x, y))
        if s is None:
            self._add_paint(x, y, color)
        else:
            s.pixels[:] = int(color)

    def _grow(self, rid: str) -> None:
        gw, gh = self.current_level.grid_size or (64, 64)
        blocked = self._blocked_cells()
        all_painted = self._all_painted()
        region = self.regions[rid]
        new_cells: set[tuple[int, int]] = set()
        for (x, y) in region:
            for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < gw and 0 <= ny < gh):
                    continue
                if (nx, ny) in blocked or (nx, ny) in all_painted:
                    continue
                new_cells.add((nx, ny))

        color = self.region_color[rid]
        for (x, y) in new_cells:
            self._add_paint(x, y, color)
        self.regions[rid] = region | new_cells
        if new_cells:
            self.last_grown = rid

    def _contact(self, a: str, b: str) -> bool:
        ca = self.regions[a]
        cb = self.regions[b]
        if not ca or not cb:
            return False
        small, large = (ca, cb) if len(ca) <= len(cb) else (cb, ca)
        for (x, y) in small:
            for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if (x + dx, y + dy) in large:
                    return True
        return False

    def _mix_regions(self) -> None:
        changed = True
        guard = 0
        while changed and guard < 32:
            guard += 1
            changed = False
            rids = list(self.regions.keys())
            for i in range(len(rids)):
                for j in range(i + 1, len(rids)):
                    a, b = rids[i], rids[j]
                    if a not in self.regions or b not in self.regions:
                        continue
                    ca = self.region_color[a]
                    cb = self.region_color[b]
                    if ca == cb:
                        continue
                    pair = frozenset((ca, cb))
                    if pair not in self.mix_table:
                        continue
                    if not self._contact(a, b):
                        continue

                    out_color = self.mix_table[pair]
                    union_cells = self.regions[a] | self.regions[b]
                    seeds = self.region_seeds[a] + self.region_seeds[b]
                    new_rid = self._new_region_id()
                    self.regions[new_rid] = union_cells
                    self.region_color[new_rid] = out_color
                    self.region_seeds[new_rid] = seeds

                    for (x, y) in union_cells:
                        self._set_paint_color(x, y, out_color)
                    for s in seeds:
                        mask = (s.pixels >= 0) & (s.pixels != WHITE)
                        s.pixels[mask] = out_color

                    if self.last_grown in (a, b):
                        self.last_grown = new_rid

                    del self.regions[a]
                    del self.regions[b]
                    del self.region_color[a]
                    del self.region_color[b]
                    del self.region_seeds[a]
                    del self.region_seeds[b]
                    changed = True
                    break
                if changed:
                    break

    def _surround_cells(self, target: Sprite) -> list[tuple[int, int]]:
        """The 8 cells around a 1×1 target pip — Chebyshev distance 1."""
        tx, ty = target.x, target.y
        return [
            (tx - 1, ty - 1), (tx, ty - 1), (tx + 1, ty - 1),
            (tx - 1, ty),                   (tx + 1, ty),
            (tx - 1, ty + 1), (tx, ty + 1), (tx + 1, ty + 1),
        ]

    def _color_at(self, cell: tuple[int, int]) -> int | None:
        for rid, cells in self.regions.items():
            if cell in cells:
                return self.region_color[rid]
        return None

    def _dissolve_targets(self) -> None:
        gw, gh = self.current_level.grid_size or (64, 64)
        for t in list(self.current_level.get_sprites_by_tag("target")):
            pip = self._target_pip_color(t)
            if pip is None:
                continue
            ok = True
            for (cx, cy) in self._surround_cells(t):
                if not (0 <= cx < gw and 0 <= cy < gh):
                    continue  # off-grid → auto-satisfied
                if self._color_at((cx, cy)) != pip:
                    ok = False
                    break
            if not ok:
                continue
            tx, ty = t.x, t.y
            # Find a surround region whose colour matches the pip — that
            # region absorbs the pip cell so the dissolved spot is
            # continuous with the surround paint (and gets recoloured by
            # any future mix that touches the region).
            host_rid: str | None = None
            for (cx, cy) in self._surround_cells(t):
                if not (0 <= cx < gw and 0 <= cy < gh):
                    continue
                for rid, cells in self.regions.items():
                    if (cx, cy) in cells and self.region_color.get(rid) == pip:
                        host_rid = rid
                        break
                if host_rid is not None:
                    break
            self.current_level.remove_sprite(t)
            if host_rid is not None and host_rid in self.regions:
                self.regions[host_rid].add((tx, ty))
                self._add_paint(tx, ty, pip)

    def _check_win(self) -> bool:
        return len(list(self.current_level.get_sprites_by_tag("target"))) == 0

    # ----- main step ----------------------------------------------
    def step(self) -> None:
        if self.steps_remaining > 0:
            self.steps_remaining -= 1
            self.step_hud.set_current(self.steps_remaining)

        action_id = self.action.id
        if action_id == GameAction.ACTION6:
            data = self.action.data or {}
            try:
                px = int(data.get("x", 0))
                py = int(data.get("y", 0))
            except (TypeError, ValueError):
                px = py = 0
            grid = self.camera.display_to_grid(px, py)
            if grid is not None:
                gx, gy = grid
                hit_rid: str | None = None
                for rid, seeds in self.region_seeds.items():
                    for s in seeds:
                        if s.x <= gx < s.x + s.width and s.y <= gy < s.y + s.height:
                            hit_rid = rid
                            break
                    if hit_rid is not None:
                        break
                if hit_rid is not None:
                    self._grow(hit_rid)
        elif action_id == GameAction.ACTION5:
            self._mix_regions()

        # Auto-dissolve runs every step. Check before mix would apply
        # (so a single-colour target dissolves before any mix repaints
        # its surround) AND after — but because mix only fires on
        # ACTION5 explicitly, and ACTION6 grows leave colours intact,
        # one pre-mix and one post-mix dissolve pass per step is
        # sufficient.
        self._dissolve_targets()

        if self._check_win():
            self.next_level()
            self.complete_action()
            return
        if self.steps_remaining <= 0:
            self.lose()

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        out = np.zeros((4, 4), dtype=np.int16)
        out[0, 0] = self.steps_remaining
        out[0, 1] = len(self.regions)
        return out

    def _get_valid_actions(self) -> list[ActionInput]:
        actions: list[ActionInput] = []
        if 5 in self._available_actions:
            actions.append(ActionInput(id=GameAction.ACTION5))
        if 6 in self._available_actions:
            gw, gh = self.current_level.grid_size or (64, 64)
            scale = max(1, min(64 // gw, 64 // gh))
            ox = (64 - gw * scale) // 2
            oy = (64 - gh * scale) // 2
            for gy in range(gh):
                for gx in range(gw):
                    px = gx * scale + ox + scale // 2
                    py = gy * scale + oy + scale // 2
                    actions.append(
                        ActionInput(
                            id=GameAction.ACTION6,
                            data={"x": int(px), "y": int(py)},
                        )
                    )
        return actions
