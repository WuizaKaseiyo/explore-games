"""bx84."""

import numpy as np
from novaengine import (
    NovaBaseGame,
    Camera,
    GameAction,
    Level,
    RenderableUserDisplay,
    Sprite,
)

# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------
_EMITTER_PIXELS = [
    [3, 3, 3, -1],
    [3, 3, 3, 11],
    [3, 3, 3, 11],
    [3, 3, 3, -1],
]

_FILTER_PIXELS = [
    [11, 11, 9, 9],
    [11, 11, 9, 9],
    [9, 9, 11, 11],
    [9, 9, 11, 11],
]

_MIRROR_BS_PIXELS = [
    [7, -1, -1, -1],
    [-1, 7, -1, -1],
    [-1, -1, 7, -1],
    [-1, -1, -1, 7],
]

_MIRROR_SL_PIXELS = [
    [-1, -1, -1, 7],
    [-1, -1, 7, -1],
    [-1, 7, -1, -1],
    [7, -1, -1, -1],
]

_PRISM_ES_PIXELS = [
    [12, 12, 12, 12],
    [12, 12, 12, 12],
    [12, 12, 12, 12],
    [12, 12, 12, 12],
]

_PRISM_EN_PIXELS = [
    [13, 13, 13, 13],
    [13, 13, 13, 13],
    [13, 13, 13, 13],
    [13, 13, 13, 13],
]


def _hollow_square(c: int):
    return [
        [c, c, c, c],
        [c, -1, -1, c],
        [c, -1, -1, c],
        [c, c, c, c],
    ]


sprites = {
    "emitter": Sprite(
        pixels=_EMITTER_PIXELS,
        name="emitter",
        visible=True,
        collidable=True,
        tags=["emitter"],
    ),
    "filter": Sprite(
        pixels=_FILTER_PIXELS,
        name="filter",
        visible=True,
        collidable=True,
        tags=["filter"],
    ),
    "mirror_bs": Sprite(
        pixels=_MIRROR_BS_PIXELS,
        name="mirror_bs",
        visible=True,
        collidable=True,
        tags=["mirror"],
    ),
    "mirror_sl": Sprite(
        pixels=_MIRROR_SL_PIXELS,
        name="mirror_sl",
        visible=True,
        collidable=True,
        tags=["mirror"],
    ),
    "prism_es": Sprite(
        pixels=_PRISM_ES_PIXELS,
        name="prism_es",
        visible=True,
        collidable=True,
        tags=["prism"],
    ),
    "prism_en": Sprite(
        pixels=_PRISM_EN_PIXELS,
        name="prism_en",
        visible=True,
        collidable=True,
        tags=["prism"],
    ),
    "target_blue": Sprite(
        pixels=_hollow_square(9),
        name="target_blue",
        visible=True,
        collidable=True,
        tags=["target"],
    ),
    "target_yellow": Sprite(
        pixels=_hollow_square(11),
        name="target_yellow",
        visible=True,
        collidable=True,
        tags=["target"],
    ),
    "target_yellow_north": Sprite(
        pixels=_hollow_square(11),
        name="target_yellow_north",
        visible=True,
        collidable=True,
        tags=["target"],
    ),
    "target_yellow_south": Sprite(
        pixels=_hollow_square(11),
        name="target_yellow_south",
        visible=True,
        collidable=True,
        tags=["target"],
    ),
    "target_dual": Sprite(
        pixels=[
            [-1, 11, 11, -1],
            [ 9, -1, -1,  9],
            [ 9, -1, -1,  9],
            [-1, 11, 11, -1],
        ],
        name="target_dual",
        visible=True,
        collidable=True,
        tags=["target"],
    ),
}

# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
levels = [
    Level(
        sprites=[
            sprites["emitter"].clone().set_position(4, 32),
            sprites["target_yellow"].clone().set_position(32, 44),
        ],
        grid_size=(64, 64),
        data={
            "emit_direction": "east",
            "lives": 3,
            "win_targets": ["target_yellow"],
        },
    ),
    Level(
        sprites=[
            sprites["emitter"].clone().set_position(4, 8),
            sprites["target_yellow"].clone().set_position(12, 32),
            sprites["filter"].clone().set_position(28, 44),
            sprites["target_blue"].clone().set_position(40, 44),
        ],
        grid_size=(64, 64),
        data={
            "emit_direction": "east",
            "lives": 3,
            "win_targets": ["target_yellow", "target_blue"],
        },
    ),
    Level(
        sprites=[
            sprites["emitter"].clone().set_position(4, 32),
            sprites["target_dual"].clone().set_position(16, 12),
            sprites["filter"].clone().set_position(32, 32),
            sprites["target_yellow_south"].clone().set_position(16, 44),
            sprites["target_blue"].clone().set_position(48, 44),
        ],
        grid_size=(64, 64),
        data={
            "emit_direction": "east",
            "lives": 3,
            "win_targets": [
                "target_yellow_south",
                "target_blue",
                "target_dual:11",
                "target_dual:9",
            ],
        },
    ),
]

# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 5
PADDING_COLOR = 4

GRID_W = 64
GRID_H = 64
STRIDE = 4

BEAM_COLOR = 11

# Cardinal direction vectors keyed by `level.data["emit_direction"]`.
DIRECTIONS = {
    "east": (1, 0),
    "west": (-1, 0),
    "south": (0, 1),
    "north": (0, -1),
}


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class LivesHud(RenderableUserDisplay):
    """Three pips on the bottom rows showing emissions remaining."""

    PIP_COLUMNS = [(20, 24), (30, 34), (40, 44)]
    LIT_COLOUR = 11
    SPENT_COLOUR = 5
    BAR_COLOUR = 4

    def __init__(self, max_lives: int = 3) -> None:
        self.max_lives = max_lives
        self.lives = max_lives

    def set_max(self, max_lives: int) -> None:
        self.max_lives = max_lives
        self.lives = max_lives

    def set_lives(self, lives: int) -> None:
        self.lives = max(0, min(lives, self.max_lives))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        frame[62:64, :] = self.BAR_COLOUR
        for i, (sx, ex) in enumerate(self.PIP_COLUMNS):
            colour = self.LIT_COLOUR if i < self.lives else self.SPENT_COLOUR
            frame[62:64, sx:ex] = colour
        return frame


# ---------------------------------------------------------------------
# 5. GAME CLASS
# ---------------------------------------------------------------------
BEAM_HOLD_TICKS = 8


class Bx84(NovaBaseGame):
    def __init__(self) -> None:
        self.lives_hud = LivesHud(3)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.lives_hud],
        )
        # Per-game state (reset in on_set_level).
        self.targets_lit: dict[str, bool] = {}
        self.targets_lit_this_emit: dict[str, bool] = {}
        self.lives_remaining: int = 0
        self.beam_overlay: Sprite | None = None
        # Animation state.
        self.beam_animation_active: bool = False
        self.active_beams: list[tuple[int, int, int, int, int]] = []
        self.beam_visited: set[tuple[int, int, int, int]] = set()
        self.beam_hold_remaining: int = 0
        super().__init__(
            game_id="bx84",
            levels=levels,
            camera=camera,
            available_actions=[5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (GRID_W, GRID_H)
        self.camera.width = gw
        self.camera.height = gh
        max_lives = int(level.get_data("lives") or 3)
        self.lives_remaining = max_lives
        self.lives_hud.set_max(max_lives)
        self.lives_hud.set_lives(max_lives)
        win_targets = level.get_data("win_targets") or []
        self.targets_lit = {name: False for name in win_targets}
        self.targets_lit_this_emit = {}
        self.beam_animation_active = False
        self.active_beams = []
        self.beam_visited = set()
        self.beam_hold_remaining = 0
        self.beam_overlay = Sprite(
            pixels=np.full((gh, gw), -1, dtype=np.int8),
            name="beam_overlay",
            visible=True,
            collidable=False,
            tags=["beam_overlay"],
            layer=10,
        )
        level.add_sprite(self.beam_overlay)

    def step(self) -> None:
        if self.beam_animation_active:
            self._advance_animation()
            return
        if self.action.id == GameAction.ACTION6:
            ax = int(self.action.data.get("x", -1))
            ay = int(self.action.data.get("y", -1))
            cell = self.camera.display_to_grid(ax, ay)
            if cell is not None:
                gx, gy = cell
                self._handle_click(int(gx), int(gy))
            self.complete_action()
            return
        if self.action.id == GameAction.ACTION5:
            if self.lives_remaining <= 0:
                self.lose()
                self.complete_action()
                return
            self._start_emission()
            return
        self.complete_action()

    # --- helpers --------------------------------------------------------

    def _sprite_at(self, gx: int, gy: int) -> Sprite | None:
        # Bounding-box check across all sprites except the beam overlay.
        # Iterates in current sprite order; the first match wins. Order is
        # stable enough for our purposes because at most one non-overlay
        # sprite occupies any given cell.
        for s in self.current_level.get_sprites():
            if s.name == "beam_overlay":
                continue
            if (
                gx >= s.x
                and gx < s.x + s.width
                and gy >= s.y
                and gy < s.y + s.height
            ):
                return s
        return None

    def _handle_click(self, gx: int, gy: int) -> None:
        gw, gh = self.current_level.grid_size or (GRID_W, GRID_H)
        if not (0 <= gx < gw and 0 <= gy < gh):
            return
        # Snap click to the 4-pixel placement grid (sprites are 4x4 and live
        # at multiple-of-4 positions). Without this, a click at e.g. (33, 33)
        # would place a mirror at an off-stride position that the beam
        # tracer (which advances on stride-4) could never hit.
        gx = (gx // STRIDE) * STRIDE
        gy = (gy // STRIDE) * STRIDE
        sprite_here = self._sprite_at(gx, gy)
        if sprite_here is None:
            self.current_level.add_sprite(
                sprites["mirror_bs"].clone().set_position(gx, gy)
            )
            return
        if "mirror" in sprite_here.tags:
            self.current_level.remove_sprite(sprite_here)
            if sprite_here.name == "mirror_bs":
                self.current_level.add_sprite(
                    sprites["mirror_sl"].clone().set_position(gx, gy)
                )
            # mirror_sl → leave empty (removed above)
            return
        if "prism" in sprite_here.tags:
            other = "prism_en" if sprite_here.name == "prism_es" else "prism_es"
            self.current_level.remove_sprite(sprite_here)
            self.current_level.add_sprite(
                sprites[other].clone().set_position(sprite_here.x, sprite_here.y)
            )
            return
        # filter, target_*, emitter, beam_overlay → no-op.

    def _filter_swap(self, sprite: Sprite, current_colour: int) -> int:
        # The filter sprite has two distinct palettes; swap to the other.
        colours = {int(c) for c in sprite.pixels.flatten().tolist() if c >= 0}
        for c in colours:
            if c != current_colour:
                return c
        return current_colour

    def _side_colour(self, sprite: Sprite, dx: int, dy: int) -> int:
        # Return the palette of the side the beam entered through, picking
        # the middle pixel to avoid corner ambiguity.
        pixels = sprite.pixels
        if pixels.ndim != 2:
            return -1
        H, W = pixels.shape
        if dx > 0:
            return int(pixels[H // 2, 0])
        if dx < 0:
            return int(pixels[H // 2, W - 1])
        if dy > 0:
            return int(pixels[0, W // 2])
        if dy < 0:
            return int(pixels[H - 1, W // 2])
        return -1

    def _record_target_hit(self, name: str, colour: int) -> None:
        # Try the per-colour key first (dual targets), then the plain name
        # (single-colour targets).
        keyed = f"{name}:{colour}"
        if keyed in self.targets_lit_this_emit:
            self.targets_lit_this_emit[keyed] = True
        elif name in self.targets_lit_this_emit:
            self.targets_lit_this_emit[name] = True

    def _start_emission(self) -> None:
        if self.beam_overlay is None:
            self.complete_action()
            return
        self.beam_overlay.pixels[:] = -1
        self.targets_lit_this_emit = {name: False for name in self.targets_lit}
        emitters = self.current_level.get_sprites_by_tag("emitter")
        if not emitters:
            self._resolve_emission()
            return
        emitter = emitters[0]
        direction = self.current_level.get_data("emit_direction") or "east"
        ddx, ddy = DIRECTIONS.get(direction, (1, 0))
        if ddx > 0:
            start_x = emitter.x + STRIDE
        elif ddx < 0:
            start_x = emitter.x - STRIDE
        else:
            start_x = emitter.x
        if ddy > 0:
            start_y = emitter.y + STRIDE
        elif ddy < 0:
            start_y = emitter.y - STRIDE
        else:
            start_y = emitter.y
        self.active_beams = [(start_x, start_y, ddx, ddy, BEAM_COLOR)]
        self.beam_visited = set()
        self.beam_hold_remaining = BEAM_HOLD_TICKS
        self.beam_animation_active = True

    def _advance_animation(self) -> None:
        if not self.active_beams:
            if self.beam_hold_remaining > 0:
                self.beam_hold_remaining -= 1
                return
            self._resolve_emission()
            return
        gw, gh = self.current_level.grid_size or (GRID_W, GRID_H)
        new_beams: list[tuple[int, int, int, int, int]] = []
        for (x, y, dx, dy, colour) in self.active_beams:
            if (x, y, dx, dy) in self.beam_visited:
                continue
            self.beam_visited.add((x, y, dx, dy))
            if not (0 <= x < gw and 0 <= y < gh):
                continue
            sprite_here = self._sprite_at(x, y)
            if sprite_here is None:
                if self.beam_overlay is not None:
                    self.beam_overlay.pixels[y:y + STRIDE, x:x + STRIDE] = colour
                new_beams.append((x + dx * STRIDE, y + dy * STRIDE, dx, dy, colour))
                continue
            name = sprite_here.name
            if name == "mirror_bs":
                ndx, ndy = dy, dx
                new_beams.append((x + ndx * STRIDE, y + ndy * STRIDE, ndx, ndy, colour))
                continue
            if name == "mirror_sl":
                ndx, ndy = -dy, -dx
                new_beams.append((x + ndx * STRIDE, y + ndy * STRIDE, ndx, ndy, colour))
                continue
            if "filter" in sprite_here.tags:
                new_colour = self._filter_swap(sprite_here, colour)
                new_beams.append((x + dx * STRIDE, y + dy * STRIDE, dx, dy, new_colour))
                continue
            if "prism" in sprite_here.tags:
                new_beams.append((x + dx * STRIDE, y + dy * STRIDE, dx, dy, colour))
                if name == "prism_es":
                    pdx, pdy = 0, 1
                else:
                    pdx, pdy = 0, -1
                new_beams.append((x + pdx * STRIDE, y + pdy * STRIDE, pdx, pdy, colour))
                continue
            if "target" in sprite_here.tags:
                side_colour = self._side_colour(sprite_here, dx, dy)
                if side_colour == colour:
                    self._record_target_hit(name, colour)
                new_beams.append((x + dx * STRIDE, y + dy * STRIDE, dx, dy, colour))
                continue
            # emitter or unknown sprite: stop this branch.
        self.active_beams = new_beams

    def _resolve_emission(self) -> None:
        for name, lit in self.targets_lit_this_emit.items():
            if lit:
                self.targets_lit[name] = True
        self.beam_animation_active = False
        self.active_beams = []
        self.beam_visited = set()
        if self.targets_lit and all(self.targets_lit.values()):
            self.next_level()
            self.complete_action()
            return
        self.lives_remaining -= 1
        self.lives_hud.set_lives(self.lives_remaining)
        if self.beam_overlay is not None:
            self.beam_overlay.pixels[:] = -1
        if self.lives_remaining <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 1), dtype=np.int16)
        state[0, 0] = self.lives_remaining
        return state
