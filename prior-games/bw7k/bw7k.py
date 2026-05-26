"""bw7k."""

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
    "actor": Sprite(
        pixels=[
            [10, 9, 9, 10],
            [9, 5, 5, 9],
            [9, 5, 5, 9],
            [10, 9, 9, 10],
        ],
        name="actor",
        visible=True,
        collidable=True,
        tags=["actor"],
        layer=3,
    ),
    "actor_goal": Sprite(
        pixels=[
            [9, 9, 9, 9],
            [9, -1, -1, 9],
            [9, -1, -1, 9],
            [9, 9, 9, 9],
        ],
        name="actor_goal",
        visible=True,
        collidable=False,
        tags=["actor_goal"],
        layer=0,
    ),
    "anchor_red": Sprite(
        pixels=[
            [8, -1, -1, 8],
            [-1, 12, 12, -1],
            [-1, 12, 12, -1],
            [8, -1, -1, 8],
        ],
        name="anchor_red",
        visible=True,
        collidable=False,
        tags=["anchor", "anchor_red"],
        layer=1,
    ),
    "anchor_yellow": Sprite(
        pixels=[
            [11, -1, -1, 11],
            [-1, 14, 14, -1],
            [-1, 14, 14, -1],
            [11, -1, -1, 11],
        ],
        name="anchor_yellow",
        visible=True,
        collidable=False,
        tags=["anchor", "anchor_yellow"],
        layer=1,
    ),
    "shade_red": Sprite(
        pixels=[
            [12, 8, 8, 12],
            [8, 5, 5, 8],
            [8, 5, 5, 8],
            [12, 8, 8, 12],
        ],
        name="shade_red",
        visible=True,
        collidable=False,
        tags=["shade", "shade_red"],
        layer=2,
    ),
    "shade_yellow": Sprite(
        pixels=[
            [14, 11, 11, 14],
            [11, 5, 5, 11],
            [11, 5, 5, 11],
            [14, 11, 11, 14],
        ],
        name="shade_yellow",
        visible=True,
        collidable=False,
        tags=["shade", "shade_yellow"],
        layer=2,
    ),
    "target_red": Sprite(
        pixels=[
            [8, 8, 8, 8],
            [8, -1, -1, 8],
            [8, -1, -1, 8],
            [8, 8, 8, 8],
        ],
        name="target_red",
        visible=True,
        collidable=False,
        tags=["target", "target_red"],
        layer=0,
    ),
    "target_yellow": Sprite(
        pixels=[
            [11, 11, 11, 11],
            [11, -1, -1, 11],
            [11, -1, -1, 11],
            [11, 11, 11, 11],
        ],
        name="target_yellow",
        visible=True,
        collidable=False,
        tags=["target", "target_yellow"],
        layer=0,
    ),
    "wall": Sprite(
        pixels=[
            [3, 3, 3, 3],
            [3, 4, 4, 3],
            [3, 4, 4, 3],
            [3, 3, 3, 3],
        ],
        name="wall",
        visible=True,
        collidable=True,
        tags=["wall"],
        layer=1,
    ),
    "trail_actor": Sprite(
        pixels=[
            [-1, -1, -1, -1],
            [-1, 1, 1, -1],
            [-1, 1, 1, -1],
            [-1, -1, -1, -1],
        ],
        name="trail_actor",
        visible=True,
        collidable=False,
        tags=["trail_actor"],
        layer=-1,
    ),
    "trail_shade_red": Sprite(
        pixels=[
            [-1, -1, -1, -1],
            [-1, 13, 13, -1],
            [-1, 13, 13, -1],
            [-1, -1, -1, -1],
        ],
        name="trail_shade_red",
        visible=True,
        collidable=False,
        tags=["trail_shade", "trail_shade_red"],
        layer=-1,
    ),
    "trail_shade_yellow": Sprite(
        pixels=[
            [-1, -1, -1, -1],
            [-1, 12, 12, -1],
            [-1, 12, 12, -1],
            [-1, -1, -1, -1],
        ],
        name="trail_shade_yellow",
        visible=True,
        collidable=False,
        tags=["trail_shade", "trail_shade_yellow"],
        layer=-1,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
levels = [
    Level(
        sprites=[
            sprites["actor"].clone().set_position(12, 56),
            sprites["anchor_red"].clone().set_position(12, 36),
            sprites["target_red"].clone().set_position(12, 16),
            sprites["actor_goal"].clone().set_position(12, 4),
        ],
        grid_size=(64, 64),
        data={"step_budget": 30},
    ),
    Level(
        sprites=[
            sprites["actor"].clone().set_position(16, 56),
            sprites["anchor_red"].clone().set_position(16, 32),
            sprites["target_red"].clone().set_position(40, 8),
            sprites["actor_goal"].clone().set_position(16, 4),
            sprites["wall"].clone().set_position(36, 8),
        ],
        grid_size=(64, 64),
        data={"step_budget": 50},
    ),
    Level(
        sprites=[
            sprites["actor"].clone().set_position(8, 60),
            sprites["anchor_red"].clone().set_position(8, 36),
            sprites["target_red"].clone().set_position(8, 12),
            sprites["anchor_yellow"].clone().set_position(40, 36),
            sprites["target_yellow"].clone().set_position(40, 12),
            sprites["actor_goal"].clone().set_position(24, 4),
            sprites["wall"].clone().set_position(24, 36),
            sprites["wall"].clone().set_position(44, 16),
        ],
        grid_size=(64, 64),
        data={"step_budget": 60},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 5
PADDING_COLOR = 5
STRIDE = 4
GRID_W = 64
GRID_H = 64

ACTION_VECTOR = {
    GameAction.ACTION1: (0, -STRIDE),
    GameAction.ACTION2: (0, STRIDE),
    GameAction.ACTION3: (-STRIDE, 0),
    GameAction.ACTION4: (STRIDE, 0),
}


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, game: "Bw7k") -> None:
        self._game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        budget = self._game.step_budget
        if budget <= 0:
            return frame
        ratio = max(0.0, min(1.0, self._game.steps_remaining / budget))
        leading = int(np.ceil(64 * ratio))
        frame[63, :] = 3
        frame[63, :leading] = 2
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Bw7k(NovaBaseGame):
    def __init__(self) -> None:
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[StepCounterHud(self)],
        )
        self.step_budget: int = 0
        self.steps_remaining: int = 0
        self.move_history: list[tuple[int, int]] = []
        self.spawned_anchor_names: set[str] = set()
        self.mode: str = "actor"
        self.shades: list[dict] = []
        super().__init__(
            game_id="bw7k",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4],
        )

    def on_set_level(self, level: Level) -> None:
        self.step_budget = int(level.get_data("step_budget") or 30)
        self.steps_remaining = self.step_budget
        self.move_history = []
        self.spawned_anchor_names = set()
        self.mode = "actor"
        self.shades = []
        # drop a trail dot at the actor's start cell so the player sees the trail
        # primed from action 0.
        actor = self._actor()
        if actor is not None:
            self._drop_trail("trail_actor", actor.x, actor.y)

    # --- helpers ---

    def _actor(self) -> Sprite | None:
        actors = self.current_level.get_sprites_by_tag("actor")
        return actors[0] if actors else None

    def _is_blocked(self, x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return True
        if x + STRIDE > GRID_W or y + STRIDE > GRID_H:
            return True
        for w in self.current_level.get_sprites_by_tag("wall"):
            if w.x == x and w.y == y:
                return True
        return False

    def _drop_trail(self, sprite_name: str, x: int, y: int) -> None:
        trail = sprites[sprite_name].clone().set_position(x, y)
        self.current_level.add_sprite(trail)

    def _trigger_anchor_if_landed(self) -> bool:
        actor = self._actor()
        if actor is None:
            return False
        triggered = False
        for anchor in self.current_level.get_sprites_by_tag("anchor"):
            if anchor.name in self.spawned_anchor_names:
                continue
            if anchor.x != actor.x or anchor.y != actor.y:
                continue
            color = "red" if "anchor_red" in anchor.tags else "yellow"
            shade_sprite = (
                sprites[f"shade_{color}"]
                .clone()
                .set_position(anchor.x, anchor.y)
            )
            self.current_level.add_sprite(shade_sprite)
            self.shades.append({
                "sprite": shade_sprite,
                "snapshot": list(self.move_history),
                "pointer": 0,
                "color": color,
            })
            self.spawned_anchor_names.add(anchor.name)
            anchor.set_interaction(InteractionMode.REMOVED)
            # drop a same-coloured trail dot at the shade's spawn cell so
            # the player sees where its trail starts.
            self._drop_trail(f"trail_shade_{color}", anchor.x, anchor.y)
            triggered = True
        return triggered

    def _advance_shades_one_step(self) -> bool:
        """Advance every active shade by one tape entry. Return True when all are exhausted."""
        all_done = True
        for s in self.shades:
            if s["pointer"] >= len(s["snapshot"]):
                continue
            all_done = False
            dx, dy = s["snapshot"][s["pointer"]]
            sprite = s["sprite"]
            nx, ny = sprite.x + dx, sprite.y + dy
            if not self._is_blocked(nx, ny):
                sprite.set_position(nx, ny)
                self._drop_trail(f"trail_shade_{s['color']}", nx, ny)
            s["pointer"] += 1
        return all_done

    def _check_win(self) -> bool:
        actor = self._actor()
        if actor is None:
            return False
        actor_goals = self.current_level.get_sprites_by_tag("actor_goal")
        if not actor_goals:
            return False
        ag = actor_goals[0]
        if (actor.x, actor.y) != (ag.x, ag.y):
            return False
        targets = self.current_level.get_sprites_by_tag("target")
        for t in targets:
            color = "red" if "target_red" in t.tags else "yellow"
            placed = False
            for s in self.current_level.get_sprites_by_tag(f"shade_{color}"):
                if (s.x, s.y) == (t.x, t.y):
                    placed = True
                    break
            if not placed:
                return False
        return True

    # --- step ---

    def step(self) -> None:
        # Shade-replay mode: each tick advances every active shade by ONE tape
        # entry, then yields back to the engine without consuming a new action.
        # The animation continues until every shade has finished its tape, then
        # control returns to the actor.
        if self.mode == "shade_replay":
            all_done = self._advance_shades_one_step()
            if self._check_win():
                self.next_level()
                self.complete_action()
                return
            if all_done:
                self.mode = "actor"
                if self.steps_remaining <= 0:
                    self.lose()
                self.complete_action()
                return
            # mid-animation: do NOT complete_action so the engine re-renders
            # and re-enters step() on the next frame.
            return

        # Actor mode.
        if self.action.id not in ACTION_VECTOR:
            self.complete_action()
            return
        dx, dy = ACTION_VECTOR[self.action.id]
        actor = self._actor()
        if actor is None:
            self.complete_action()
            return
        nx, ny = actor.x + dx, actor.y + dy
        if not self._is_blocked(nx, ny):
            actor.set_position(nx, ny)
            self._drop_trail("trail_actor", nx, ny)
        self.move_history.append((dx, dy))
        triggered = self._trigger_anchor_if_landed()
        self.steps_remaining -= 1
        if self._check_win():
            self.next_level()
            self.complete_action()
            return
        if triggered:
            self.mode = "shade_replay"
            # Yield to the engine to begin animating on the next frame.
            return
        if self.steps_remaining <= 0:
            self.lose()
        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.array([self.steps_remaining], dtype=np.int16)
