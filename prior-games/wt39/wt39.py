"""wt39 — single-pawn glide puzzle on a tiled arena."""

from typing import Optional

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


# ----------------------------------------------------------------------
# 1. SPRITE BANK
# ----------------------------------------------------------------------

sprites = {
    "bumper_back": Sprite(
        pixels=[[12]],
        name="bumper_back",
        visible=True,
        collidable=True,
        tags=["bumper", "bumper_back"],
    ),
    "goal": Sprite(
        pixels=[[13]],
        name="goal",
        visible=True,
        collidable=False,
        tags=["goal"],
    ),
    "pawn": Sprite(
        pixels=[[8]],
        name="pawn",
        visible=True,
        collidable=True,
        tags=["pawn"],
    ),
    "thaw_cracked": Sprite(
        pixels=[[2]],
        name="thaw_cracked",
        visible=True,
        collidable=True,
        tags=["thaw", "cracked"],
    ),
    "thaw_frozen": Sprite(
        pixels=[[10]],
        name="thaw_frozen",
        visible=True,
        collidable=False,
        tags=["thaw", "frozen"],
    ),
    "wall_block": Sprite(
        pixels=[[4]],
        name="wall_block",
        visible=True,
        collidable=True,
        tags=["wall"],
    ),
}


# ----------------------------------------------------------------------
# 2. LEVEL BUILDERS
# ----------------------------------------------------------------------

GRID_W = 14
GRID_H = 14


def _perimeter_walls():
    placed = []
    for x in range(GRID_W):
        placed.append(sprites["wall_block"].clone().set_position(x, 0))
        placed.append(sprites["wall_block"].clone().set_position(x, GRID_H - 1))
    for y in range(1, GRID_H - 1):
        placed.append(sprites["wall_block"].clone().set_position(0, y))
        placed.append(sprites["wall_block"].clone().set_position(GRID_W - 1, y))
    return placed


def _level_one_sprites():
    # 5-slide zig-zag through the arena. Each slide stops at an interior
    # wall; witness = [RIGHT, DOWN, LEFT, DOWN, RIGHT].
    # (2,2) -RIGHT-> (10,2) -DOWN-> (10,5) -LEFT-> (3,5) -DOWN-> (3,10)
    #          -RIGHT-> (10,10) = goal.
    placed = _perimeter_walls()
    placed.append(sprites["pawn"].clone().set_position(2, 2))
    placed.append(sprites["goal"].clone().set_position(10, 10))
    for x, y in [(11, 2), (10, 6), (2, 5), (3, 11), (11, 10)]:
        placed.append(sprites["wall_block"].clone().set_position(x, y))
    return placed


def _level_two_sprites():
    # 5-slide route requiring TWO bumper deflections, both
    # counterfactually necessary.
    # Witness: [RIGHT, LEFT, DOWN, RIGHT, RIGHT].
    # (2,2) -RIGHT-> bumper(10,2) -> DOWN col10 -> wall(10,5) -> (10,4)
    #          -LEFT-> wall(3,4) -> (4,4)
    #          -DOWN-> wall(4,8) -> (4,7)
    #          -RIGHT-> bumper(9,7) -> DOWN col9 -> wall(9,11) -> (9,10)
    #          -RIGHT-> wall(11,10) -> (10,10) = goal.
    # bumper(10,2) is necessary because col 10 rows 1-4 are sealed
    # except via the press-1 deflection. bumper(9,7) is necessary
    # because col 9 has no slide-stops at rows 1-10 (no wall at
    # (10, ROW) or (8, ROW) for any ROW < 11), so without the
    # press-4 E->S deflection the pawn cannot reach (9, 10) and
    # therefore cannot reach the goal at (10, 10).
    placed = _perimeter_walls()
    placed.append(sprites["pawn"].clone().set_position(2, 2))
    placed.append(sprites["goal"].clone().set_position(10, 10))
    for x, y in [(10, 5), (3, 4), (4, 8), (9, 11), (11, 10)]:
        placed.append(sprites["wall_block"].clone().set_position(x, y))
    placed.append(sprites["bumper_back"].clone().set_position(10, 2))
    placed.append(sprites["bumper_back"].clone().set_position(9, 7))
    return placed


def _level_three_sprites():
    # 6-slide route on a layout DISTINCT from L2 (different bumper2
    # position, no wall(9,11), thaws replace one wall and add a
    # decorative blue tile).
    # Witness: [RIGHT, LEFT, DOWN, RIGHT, UP, RIGHT].
    # (2,2) -RIGHT-> bumper(10,2) -> DOWN col10 -> wall(10,5) -> (10,4)
    #          -LEFT-> wall(3,4) -> (4,4)
    #          -DOWN-> col4 passes thaw(4,5) [cracks]
    #                 -> wall(4,8) -> (4,7)
    #          -RIGHT-> bumper(8,7) -> DOWN col8 passes thaw(8,9)
    #                 [cracks] -> perimeter -> (8,12)
    #          -UP   -> cracked thaw(8,9) is now wall -> stops (8,10)
    #          -RIGHT-> wall(11,10) -> (10,10) = goal.
    #
    # Bumper(10,2) is counterfactually necessary (same argument as L2).
    # Bumper(8,7) is counterfactually necessary: col 8 has no slide-
    # stops at any row (no wall at (7,ROW) or (9,ROW) for any ROW),
    # so without the press-4 E->S deflection the pawn cannot enter
    # col 8 — and therefore cannot cross thaw(8,9) to crack it.
    # Thaw(8,9) is counterfactually necessary: with it frozen, no
    # slide-stop terminates at (8,10) because col 8 has no walls
    # between rows 1 and 12; only the cracked thaw provides the
    # UP-stop one cell below. Thaw(4,5) cracks during the press-3
    # DOWN slide in col 4 and is visually consumed (not load-
    # bearing on its own — wall(4,8) already provides the DOWN-stop
    # at (4,7)).
    #
    # L3 obstacles distinct from L2: bumper2 at (8,7) vs L2's (9,7);
    # wall(9,11) absent in L3; thaws(4,5) and (8,9) replace L2's
    # wall(9,11). Goal cell (10,10) shared with L2, but the route
    # to reach it traverses col 8 with thaw-cracking instead of
    # col 9 with wall-stopping.
    placed = _perimeter_walls()
    placed.append(sprites["pawn"].clone().set_position(2, 2))
    placed.append(sprites["goal"].clone().set_position(10, 10))
    for x, y in [(10, 5), (3, 4), (4, 8), (11, 10)]:
        placed.append(sprites["wall_block"].clone().set_position(x, y))
    placed.append(sprites["bumper_back"].clone().set_position(10, 2))
    placed.append(sprites["bumper_back"].clone().set_position(8, 7))
    placed.append(sprites["thaw_frozen"].clone().set_position(4, 5))
    placed.append(sprites["thaw_frozen"].clone().set_position(8, 9))
    return placed


levels = [
    Level(
        sprites=_level_one_sprites(),
        grid_size=(GRID_W, GRID_H),
        data={"step_budget": 50},
    ),
    Level(
        sprites=_level_two_sprites(),
        grid_size=(GRID_W, GRID_H),
        data={"step_budget": 100},
    ),
    Level(
        sprites=_level_three_sprites(),
        grid_size=(GRID_W, GRID_H),
        data={"step_budget": 140},
    ),
]


# ----------------------------------------------------------------------
# 3. CONSTANTS
# ----------------------------------------------------------------------

BACKGROUND_COLOR = 0
PADDING_COLOR = 5

HUD_FILL_COLOR = 8
HUD_EMPTY_COLOR = 5

# Direction deltas, indexed by GameAction id (1=UP, 2=DOWN, 3=LEFT, 4=RIGHT).
_DIR = {
    GameAction.ACTION1: (0, -1),
    GameAction.ACTION2: (0, 1),
    GameAction.ACTION3: (-1, 0),
    GameAction.ACTION4: (1, 0),
}

# A bumper_back ("\\") deflection map: incoming (dx, dy) -> outgoing (dx, dy).
# E -> S, S -> E, W -> N, N -> W.
_DEFLECT_BACK = {
    (1, 0): (0, 1),
    (0, 1): (1, 0),
    (-1, 0): (0, -1),
    (0, -1): (-1, 0),
}


# ----------------------------------------------------------------------
# 4. HUD
# ----------------------------------------------------------------------

class StepCounterHud(RenderableUserDisplay):
    """Top-row depleting bar; remaining/total controls the visible width."""

    def __init__(self, total: int = 0):
        super().__init__()
        self._total = max(1, total)
        self._remaining = self._total

    def reset(self, total: int) -> None:
        self._total = max(1, total)
        self._remaining = self._total

    def set_remaining(self, remaining: int) -> None:
        self._remaining = max(0, min(self._total, remaining))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        cols = frame.shape[1]
        filled = int(round(cols * self._remaining / self._total))
        frame[0, :filled] = HUD_FILL_COLOR
        frame[0, filled:] = HUD_EMPTY_COLOR
        return frame


# ----------------------------------------------------------------------
# 5. THE GAME CLASS
# ----------------------------------------------------------------------

class Wt39(NovaBaseGame):
    def __init__(self) -> None:
        self._step_hud = StepCounterHud(0)
        self._step_budget = 0
        self._steps_remaining = 0
        self._anim_queue: list[tuple[int, int, Optional[Sprite]]] = []
        camera = Camera(
            width=GRID_W,
            height=GRID_H,
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_hud],
        )
        super().__init__(
            game_id="wt39",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    # -- per-level setup --------------------------------------------

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (GRID_W, GRID_H)
        self._camera.width = gw
        self._camera.height = gh

        budget = level.get_data("step_budget") or 0
        self._step_budget = int(budget)
        self._steps_remaining = int(budget)
        self._step_hud.reset(self._step_budget)
        self._step_hud.set_remaining(self._steps_remaining)
        self._anim_queue = []

    # -- helpers ---------------------------------------------------

    def _pawn(self) -> Optional[Sprite]:
        for sprite in self.current_level.get_sprites_by_tag("pawn"):
            return sprite
        return None

    def _goal(self) -> Optional[Sprite]:
        for sprite in self.current_level.get_sprites_by_tag("goal"):
            return sprite
        return None

    def _blocker_at(self, x: int, y: int) -> Optional[Sprite]:
        """Return a sprite at (x, y) that should stop a slide, or None."""
        for sprite in self.current_level.get_sprites():
            if sprite.x != x or sprite.y != y:
                continue
            if sprite.interaction == InteractionMode.REMOVED:
                continue
            tags = sprite.tags
            if "wall" in tags or "cracked" in tags:
                return sprite
            if "bumper" in tags:
                return sprite
        return None

    def _frozen_thaw_at(self, x: int, y: int) -> Optional[Sprite]:
        for sprite in self.current_level.get_sprites_by_tag("frozen"):
            if sprite.x == x and sprite.y == y:
                return sprite
        return None

    def _bumper_at(self, x: int, y: int) -> Optional[Sprite]:
        for sprite in self.current_level.get_sprites_by_tag("bumper"):
            if sprite.x == x and sprite.y == y:
                return sprite
        return None

    def _crack(self, frozen: Sprite) -> None:
        """Replace a frozen thaw at its cell with a cracked thaw."""
        x, y = frozen.x, frozen.y
        self.current_level.remove_sprite(frozen)
        cracked = sprites["thaw_cracked"].clone().set_position(x, y)
        self.current_level.add_sprite(cracked)

    def _compute_slide_path(
        self, dx: int, dy: int
    ) -> list[tuple[int, int, Optional[Sprite]]]:
        """Pre-compute every cell the pawn will visit during a slide.

        Returns a list of frame entries `(next_x, next_y, thaw_to_crack_now)`.
        For each entry the engine will: set the pawn to (next_x, next_y) and,
        if `thaw_to_crack_now` is non-None, replace that frozen thaw with a
        cracked thaw — the thaw being cracked is always the one the pawn just
        left, so cracking is visually concurrent with the pawn moving on.
        """
        pawn = self._pawn()
        if pawn is None:
            return []

        path: list[tuple[int, int, Optional[Sprite]]] = []
        cx, cy = pawn.x, pawn.y
        prev_thaw: Optional[Sprite] = None
        gw = self._camera.width
        gh = self._camera.height

        while True:
            nx, ny = cx + dx, cy + dy
            if nx < 0 or nx >= gw or ny < 0 or ny >= gh:
                break

            blocker = self._blocker_at(nx, ny)
            if blocker is not None:
                if "bumper" in blocker.tags:
                    path.append((nx, ny, prev_thaw))
                    cx, cy = nx, ny
                    prev_thaw = None
                    new_dir = _DEFLECT_BACK.get((dx, dy))
                    if new_dir is None:
                        break
                    dx, dy = new_dir
                    continue
                break

            frozen = self._frozen_thaw_at(nx, ny)
            path.append((nx, ny, prev_thaw))
            cx, cy = nx, ny
            prev_thaw = frozen

        return path

    # -- engine entry ----------------------------------------------

    def step(self) -> None:
        # Continuing an in-flight slide animation: advance one cell per frame.
        if self._anim_queue:
            self._advance_anim_frame()
            if self._anim_queue:
                # More frames remain — render this frame, do NOT complete the
                # action so the engine calls step() again.
                return
            self._resolve_post_slide()
            return

        self._step_hud.set_remaining(self._steps_remaining)
        delta = _DIR.get(self.action.id)
        if delta is None or self._steps_remaining <= 0:
            self.complete_action()
            return

        self._anim_queue = self._compute_slide_path(delta[0], delta[1])
        self._steps_remaining -= 1
        self._step_hud.set_remaining(self._steps_remaining)

        if not self._anim_queue:
            # Slide blocked at zero distance (e.g. wall directly ahead): no
            # animation to play, resolve outcome immediately.
            self._resolve_post_slide()
            return

        # Play first animation frame this tick; subsequent frames will be
        # produced by re-entry into step() while the queue is non-empty.
        self._advance_anim_frame()
        if self._anim_queue:
            return
        self._resolve_post_slide()

    def _advance_anim_frame(self) -> None:
        nx, ny, thaw_to_crack = self._anim_queue.pop(0)
        pawn = self._pawn()
        if pawn is not None:
            pawn.set_position(nx, ny)
        if thaw_to_crack is not None:
            self._crack(thaw_to_crack)

    def _resolve_post_slide(self) -> None:
        pawn = self._pawn()
        goal = self._goal()
        if (
            pawn is not None
            and goal is not None
            and pawn.x == goal.x
            and pawn.y == goal.y
        ):
            self.next_level()
            self.complete_action()
            return
        if self._steps_remaining <= 0:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((1, 1), dtype=np.int16)
        state[0, 0] = self._steps_remaining
        return state
