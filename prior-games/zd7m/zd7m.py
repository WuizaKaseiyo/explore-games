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

# Movable pawn: solid colour ring with off-white centre dot.
def _pawn_pixels(c: int) -> list[list[int]]:
    return [
        [c, c, c],
        [c, 1, c],
        [c, c, c],
    ]


# Target: hollow ring of pawn colour (centre transparent).
def _target_pixels(c: int) -> list[list[int]]:
    return [
        [c, c, c],
        [c, -1, c],
        [c, c, c],
    ]


# Anchor: 2-tone grey/off-black checker.
_ANCHOR_PIXELS = [
    [3, 4, 3],
    [4, 3, 4],
    [3, 4, 3],
]


# Portal: purple "+" cross — visually distinct from target rings.
_PORTAL_PIXELS = [
    [-1, 15, -1],
    [15, 15, 15],
    [-1, 15, -1],
]


sprites = {
    "pawn_pink": Sprite(
        pixels=_pawn_pixels(7),
        name="pawn_pink",
        visible=True,
        collidable=True,
        tags=["pawn"],
        layer=2,
    ),
    "pawn_yellow": Sprite(
        pixels=_pawn_pixels(11),
        name="pawn_yellow",
        visible=True,
        collidable=True,
        tags=["pawn"],
        layer=2,
    ),
    "pawn_blue": Sprite(
        pixels=_pawn_pixels(10),
        name="pawn_blue",
        visible=True,
        collidable=True,
        tags=["pawn"],
        layer=2,
    ),
    "target_pink": Sprite(
        pixels=_target_pixels(7),
        name="target_pink",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target"],
        layer=1,
    ),
    "target_yellow": Sprite(
        pixels=_target_pixels(11),
        name="target_yellow",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target"],
        layer=1,
    ),
    "target_blue": Sprite(
        pixels=_target_pixels(10),
        name="target_blue",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target"],
        layer=1,
    ),
    "anchor_block": Sprite(
        pixels=_ANCHOR_PIXELS,
        name="anchor_block",
        visible=True,
        collidable=True,
        tags=["anchor"],
        layer=1,
    ),
    "portal_a": Sprite(
        pixels=_PORTAL_PIXELS,
        name="portal_a",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["portal_a"],
        layer=0,
    ),
    "portal_b": Sprite(
        pixels=_PORTAL_PIXELS,
        name="portal_b",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["portal_b"],
        layer=0,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------

levels = [
    # L1 — base dynamic system (cohort-step + colour-matching).
    Level(
        sprites=[
            sprites["pawn_pink"].clone().set_position(4, 4),
            sprites["pawn_yellow"].clone().set_position(10, 4),
            sprites["pawn_blue"].clone().set_position(16, 4),
            sprites["target_pink"].clone().set_position(4, 14),
            sprites["target_yellow"].clone().set_position(10, 14),
            sprites["target_blue"].clone().set_position(16, 14),
        ],
        grid_size=(20, 20),
        data={"step_budget": 25},
    ),
    # L2 — adds anchor mechanic.
    Level(
        sprites=[
            sprites["pawn_pink"].clone().set_position(4, 4),
            sprites["pawn_yellow"].clone().set_position(4, 10),
            sprites["target_pink"].clone().set_position(14, 4),
            sprites["target_yellow"].clone().set_position(4, 14),
            sprites["anchor_block"].clone().set_position(7, 10),
            sprites["anchor_block"].clone().set_position(14, 7),
        ],
        grid_size=(20, 20),
        data={"step_budget": 30},
    ),
    # L3 — adds portal pair (chamber accessible only via teleport).
    Level(
        sprites=[
            sprites["pawn_pink"].clone().set_position(4, 4),
            sprites["pawn_yellow"].clone().set_position(4, 11),
            sprites["target_pink"].clone().set_position(14, 4),
            sprites["target_yellow"].clone().set_position(17, 17),
            sprites["anchor_block"].clone().set_position(7, 11),
            sprites["anchor_block"].clone().set_position(14, 7),
            sprites["anchor_block"].clone().set_position(16, 14),
            sprites["anchor_block"].clone().set_position(14, 16),
            sprites["anchor_block"].clone().set_position(5, 8),
            sprites["portal_a"].clone().set_position(4, 14),
            sprites["portal_b"].clone().set_position(17, 17),
        ],
        grid_size=(20, 20),
        data={"step_budget": 30},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------

BACKGROUND_COLOR = 4
PADDING_COLOR = 5

HUD_FILL = 14   # remaining-steps colour (green)
HUD_EMPTY = 4   # consumed-steps colour (off-black)

TELEPORT_FRAMES = 6


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    """Horizontal bar at frame row 0 showing remaining steps."""

    def __init__(self, max_steps: int = 0):
        self.max_steps = max_steps
        self.current = max_steps

    def reset(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current = max_steps

    def set_current(self, remaining: int) -> None:
        self.current = max(0, min(remaining, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        width = frame.shape[1]
        filled = int(round(width * self.current / self.max_steps))
        for x in range(width):
            frame[0, x] = HUD_FILL if x < filled else HUD_EMPTY
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------

class Zd7m(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_ui = StepCounterHud(0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        super().__init__(
            game_id="zd7m",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )
        self._step_budget = 0
        self._teleport_phase = -1
        self._pending_teleport: list[tuple[Sprite, Sprite]] = []

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        self._step_budget = level.get_data("step_budget") or 30
        self._step_counter_ui.reset(self._step_budget)
        self._teleport_phase = -1
        self._pending_teleport = []

    # ---- helpers ----------------------------------------------------

    @staticmethod
    def _rects_overlap(
        ax: int, ay: int, aw: int, ah: int,
        bx: int, by: int, bw: int, bh: int,
    ) -> bool:
        return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah

    def _can_move_to(self, pawn: Sprite, nx: int, ny: int) -> bool:
        gw, gh = self.current_level.grid_size or (64, 64)
        if nx < 0 or ny < 0:
            return False
        if nx + pawn.width > gw or ny + pawn.height > gh:
            return False
        pw, ph = pawn.width, pawn.height
        for other in self.current_level.get_sprites():
            if other is pawn:
                continue
            tags = getattr(other, "tags", []) or []
            if "anchor" not in tags and "pawn" not in tags:
                continue
            if other.interaction == InteractionMode.REMOVED:
                continue
            if self._rects_overlap(
                nx, ny, pw, ph,
                other.x, other.y, other.width, other.height,
            ):
                return False
        return True

    def _portal_at(self, x: int, y: int) -> Sprite | None:
        for portal in self.current_level.get_sprites_by_tag("portal_a"):
            if portal.x == x and portal.y == y:
                return portal
        return None

    def _portal_b(self) -> Sprite | None:
        portals = self.current_level.get_sprites_by_tag("portal_b")
        return portals[0] if portals else None

    def _check_win(self) -> bool:
        pawns = self.current_level.get_sprites_by_tag("pawn")
        if not pawns:
            return False
        targets = self.current_level.get_sprites_by_tag("target")
        for pawn in pawns:
            matched = False
            for target in targets:
                if target.x == pawn.x and target.y == pawn.y:
                    if int(target.pixels[0, 0]) == int(pawn.pixels[0, 0]):
                        matched = True
                    break
            if not matched:
                return False
        return True

    def _action_to_delta(self, aid) -> tuple[int, int]:
        if aid == GameAction.ACTION1:
            return 0, -1
        if aid == GameAction.ACTION2:
            return 0, 1
        if aid == GameAction.ACTION3:
            return -1, 0
        if aid == GameAction.ACTION4:
            return 1, 0
        return 0, 0

    def _resolve_teleport_animation(self) -> None:
        portal_a_list = self.current_level.get_sprites_by_tag("portal_a")
        portal_b_list = self.current_level.get_sprites_by_tag("portal_b")
        pulse_on = (self._teleport_phase % 2) == 0
        for portal in portal_a_list + portal_b_list:
            if pulse_on:
                portal.pixels = np.array(_PORTAL_PIXELS, dtype=portal.pixels.dtype)
            else:
                portal.pixels = np.array(
                    [[15, 15, 15], [15, 15, 15], [15, 15, 15]],
                    dtype=portal.pixels.dtype,
                )
        for pawn, _portal in self._pending_teleport:
            if self._teleport_phase < TELEPORT_FRAMES // 2:
                pawn.set_interaction(InteractionMode.REMOVED)
            else:
                pawn.set_interaction(InteractionMode.TANGIBLE)

    def _commit_teleports(self) -> None:
        portal_b = self._portal_b()
        if portal_b is None:
            self._pending_teleport = []
            return
        for pawn, _portal in self._pending_teleport:
            pawn.set_position(portal_b.x, portal_b.y)
            pawn.set_interaction(InteractionMode.TANGIBLE)
        self._pending_teleport = []
        portal_a_list = self.current_level.get_sprites_by_tag("portal_a")
        portal_b_list = self.current_level.get_sprites_by_tag("portal_b")
        for portal in portal_a_list + portal_b_list:
            portal.pixels = np.array(_PORTAL_PIXELS, dtype=portal.pixels.dtype)

    # ---- step -------------------------------------------------------

    def step(self) -> None:
        if self._teleport_phase >= 0:
            self._teleport_phase += 1
            if self._teleport_phase >= TELEPORT_FRAMES:
                self._commit_teleports()
                self._teleport_phase = -1
                won = self._check_win()
                if not won and self._action_count >= self._step_budget:
                    self.lose()
                self.complete_action()
                if won:
                    self.next_level()
                return
            self._resolve_teleport_animation()
            return

        dx, dy = self._action_to_delta(self.action.id)
        if dx == 0 and dy == 0:
            self.complete_action()
            return

        pawns = sorted(
            self.current_level.get_sprites_by_tag("pawn"),
            key=lambda p: (p.y, p.x),
        )
        landed_on_portal: list[tuple[Sprite, Sprite]] = []
        for pawn in pawns:
            nx, ny = pawn.x + dx, pawn.y + dy
            if self._can_move_to(pawn, nx, ny):
                pawn.set_position(nx, ny)
                portal = self._portal_at(nx, ny)
                if portal is not None:
                    landed_on_portal.append((pawn, portal))

        self._step_counter_ui.set_current(
            self._step_budget - self._action_count - 1
        )

        if landed_on_portal:
            self._pending_teleport = landed_on_portal
            self._teleport_phase = 0
            self._resolve_teleport_animation()
            return

        won = self._check_win()
        if not won and self._action_count + 1 >= self._step_budget:
            self.lose()
        self.complete_action()
        if won:
            self.next_level()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._step_counter_ui.current
        state[0, 1] = self._teleport_phase
        return state
