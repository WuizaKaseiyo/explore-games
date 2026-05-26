"""qn7w."""

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
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "chain_ball_blue": Sprite(
        pixels=[
            [-1, 10, 10, 9, 9, -1],
            [10, 10, 9, 9, 9, 9],
            [10, 9, 9, 9, 9, 9],
            [10, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9],
            [-1, 9, 9, 9, 9, -1],
        ],
        name="chain_ball_blue",
        visible=True,
        collidable=True,
        tags=["chain_ball", "ball_blue"],
    ),
    "chain_ball_yellow": Sprite(
        pixels=[
            [-1, 12, 12, 11, 11, -1],
            [12, 12, 11, 11, 11, 11],
            [12, 11, 11, 11, 11, 11],
            [12, 11, 11, 11, 11, 11],
            [11, 11, 11, 11, 11, 11],
            [-1, 11, 11, 11, 11, -1],
        ],
        name="chain_ball_yellow",
        visible=True,
        collidable=True,
        tags=["chain_ball", "ball_yellow"],
    ),
    "pusher_knob": Sprite(
        pixels=[
            [-1, 4, 4, 4, 4, -1],
            [4, 15, 15, 15, 15, 4],
            [4, 15, 4, 4, 15, 4],
            [4, 15, 4, 4, 15, 4],
            [4, 15, 15, 15, 15, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        name="pusher_knob",
        visible=True,
        collidable=True,
        tags=["pusher", "sys_click"],
    ),
    "target_socket_blue": Sprite(
        pixels=[
            [-1, 4, 4, 4, 4, -1],
            [4, 4, -1, -1, 4, 4],
            [4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4],
            [4, 4, -1, -1, 4, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        name="target_socket_blue",
        visible=True,
        collidable=True,
        tags=["target_socket", "socket_blue"],
    ),
    "target_socket_yellow": Sprite(
        pixels=[
            [-1, 4, 4, 4, 4, -1],
            [4, 4, -1, -1, 4, 4],
            [4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4],
            [4, 4, -1, -1, 4, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        name="target_socket_yellow",
        visible=True,
        collidable=True,
        tags=["target_socket", "socket_yellow"],
    ),
    "junction_node": Sprite(
        pixels=[
            [-1, 4, 4, 4, 4, -1],
            [4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4],
            [4, 4, 14, 14, 4, 4],
            [4, 14, 14, 14, 14, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        name="junction_node",
        visible=True,
        collidable=True,
        tags=["junction", "sys_click"],
    ),
    "merge_pad": Sprite(
        pixels=[
            [-1, 4, 4, 4, 4, -1],
            [4, 4, 4, 4, 4, 4],
            [4, 4, 12, 12, 4, 4],
            [4, 4, 12, 12, 4, 4],
            [4, 4, 4, 4, 4, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        name="merge_pad",
        visible=True,
        collidable=True,
        tags=["merge_pad"],
    ),
    "dead_end_wall": Sprite(
        pixels=[
            [5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5],
        ],
        name="dead_end_wall",
        visible=True,
        collidable=True,
        tags=["wall", "dead_end"],
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS  (exactly 3)
# ---------------------------------------------------------------------
levels = [
    # Level 1: single horizontal chain, single pusher, single socket.
    Level(
        sprites=[
            sprites["pusher_knob"].clone().set_position(8, 30),
            sprites["chain_ball_blue"].clone().set_position(14, 30),
            sprites["chain_ball_blue"].clone().set_position(20, 30),
            sprites["chain_ball_blue"].clone().set_position(26, 30),
            sprites["chain_ball_blue"].clone().set_position(32, 30),
            sprites["target_socket_blue"].clone().set_position(38, 30),
        ],
        grid_size=(64, 64),
        data={
            "step_budget": 6,
            "chains": [
                {
                    "pusher": (8, 30),
                    "stem": [(14, 30), (20, 30), (26, 30), (32, 30)],
                    "junction": None,
                    "branches": {},
                    "default_active_branch": None,
                    "axis": (1, 0),
                }
            ],
        },
    ),
    # Level 2: stem -> junction with up-branch (target) and down-branch (wall).
    Level(
        sprites=[
            sprites["pusher_knob"].clone().set_position(4, 30),
            sprites["chain_ball_blue"].clone().set_position(10, 30),
            sprites["chain_ball_blue"].clone().set_position(16, 30),
            sprites["chain_ball_blue"].clone().set_position(22, 30),
            sprites["junction_node"].clone().set_position(28, 30),
            sprites["chain_ball_blue"].clone().set_position(28, 24),
            sprites["chain_ball_blue"].clone().set_position(28, 18),
            sprites["chain_ball_blue"].clone().set_position(28, 12),
            sprites["chain_ball_blue"].clone().set_position(28, 36),
            sprites["chain_ball_blue"].clone().set_position(28, 42),
            sprites["chain_ball_blue"].clone().set_position(28, 48),
            sprites["target_socket_blue"].clone().set_position(28, 6),
            sprites["dead_end_wall"].clone().set_position(28, 54),
        ],
        grid_size=(64, 64),
        data={
            "step_budget": 16,
            "chains": [
                {
                    "pusher": (4, 30),
                    "stem": [(10, 30), (16, 30), (22, 30)],
                    "junction": (28, 30),
                    "branches": {
                        "up": {
                            "balls": [(28, 24), (28, 18), (28, 12)],
                            "axis": (0, -1),
                        },
                        "down": {
                            "balls": [(28, 36), (28, 42), (28, 48)],
                            "axis": (0, 1),
                        },
                    },
                    "default_active_branch": "down",
                    "stem_axis": (1, 0),
                }
            ],
        },
    ),
    # Level 3: two chains converging on merge_pad.
    Level(
        sprites=[
            # Chain A (blue, lower half)
            sprites["pusher_knob"].clone().set_position(2, 46),
            sprites["chain_ball_blue"].clone().set_position(8, 46),
            sprites["chain_ball_blue"].clone().set_position(14, 46),
            sprites["junction_node"].clone().set_position(20, 46),
            sprites["chain_ball_blue"].clone().set_position(20, 40),
            sprites["chain_ball_blue"].clone().set_position(20, 34),
            sprites["chain_ball_blue"].clone().set_position(20, 28),
            sprites["chain_ball_blue"].clone().set_position(20, 52),
            sprites["dead_end_wall"].clone().set_position(20, 58),
            # Chain B (yellow, upper half)
            sprites["pusher_knob"].clone().set_position(56, 22),
            sprites["chain_ball_yellow"].clone().set_position(50, 22),
            sprites["chain_ball_yellow"].clone().set_position(44, 22),
            sprites["junction_node"].clone().set_position(38, 22),
            sprites["chain_ball_yellow"].clone().set_position(32, 22),
            sprites["chain_ball_yellow"].clone().set_position(26, 22),
            sprites["chain_ball_yellow"].clone().set_position(38, 28),
            sprites["dead_end_wall"].clone().set_position(38, 34),
            sprites["merge_pad"].clone().set_position(20, 22),
        ],
        grid_size=(64, 64),
        data={
            "step_budget": 30,
            "chains": [
                {
                    "pusher": (2, 46),
                    "stem": [(8, 46), (14, 46)],
                    "junction": (20, 46),
                    "branches": {
                        "up": {
                            "balls": [(20, 40), (20, 34), (20, 28)],
                            "axis": (0, -1),
                        },
                        "down": {
                            "balls": [(20, 52)],
                            "axis": (0, 1),
                        },
                    },
                    "default_active_branch": "down",
                    "stem_axis": (1, 0),
                },
                {
                    "pusher": (56, 22),
                    "stem": [(50, 22), (44, 22)],
                    "junction": (38, 22),
                    "branches": {
                        "left": {
                            "balls": [(32, 22), (26, 22)],
                            "axis": (-1, 0),
                        },
                        "down": {
                            "balls": [(38, 28)],
                            "axis": (0, 1),
                        },
                    },
                    "default_active_branch": "down",
                    "stem_axis": (-1, 0),
                },
            ],
        },
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 0  # white
PADDING_COLOR = 0
BALL_SIZE = 6
GRID_W = 64
GRID_H = 64


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 30):
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_current(self, remaining: int) -> None:
        self.current_steps = max(0, min(remaining, self.max_steps))

    def set_max(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        ratio = self.current_steps / self.max_steps
        bar_width = round(64 * ratio)
        bar_width = max(0, min(bar_width, 64))
        for x in range(64):
            if x < bar_width:
                frame[63, x] = 4
            else:
                frame[63, x] = 0
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
def _empty_socket_pixels() -> np.ndarray:
    return np.array(
        [
            [-1, 4, 4, 4, 4, -1],
            [4, 4, -1, -1, 4, 4],
            [4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4],
            [4, 4, -1, -1, 4, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        dtype=np.int16,
    )


def _filled_socket_pixels(color: int) -> np.ndarray:
    return np.array(
        [
            [-1, 4, 4, 4, 4, -1],
            [4, 4, color, color, 4, 4],
            [4, color, color, color, color, 4],
            [4, color, color, color, color, 4],
            [4, 4, color, color, 4, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        dtype=np.int16,
    )


def _empty_merge_pad_pixels() -> np.ndarray:
    return np.array(
        [
            [-1, 4, 4, 4, 4, -1],
            [4, 4, 4, 4, 4, 4],
            [4, 4, 12, 12, 4, 4],
            [4, 4, 12, 12, 4, 4],
            [4, 4, 4, 4, 4, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        dtype=np.int16,
    )


def _half_merge_pad_pixels(color: int) -> np.ndarray:
    return np.array(
        [
            [-1, 4, 4, 4, 4, -1],
            [4, 4, 4, 4, 4, 4],
            [4, 4, 12, 12, 4, 4],
            [4, 4, color, color, 4, 4],
            [4, 4, 4, 4, 4, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        dtype=np.int16,
    )


def _full_merge_pad_pixels() -> np.ndarray:
    return np.array(
        [
            [-1, 4, 4, 4, 4, -1],
            [4, 4, 4, 4, 4, 4],
            [4, 4, 0, 0, 4, 4],
            [4, 4, 0, 0, 4, 4],
            [4, 4, 4, 4, 4, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        dtype=np.int16,
    )


def _junction_pixels(active_branch) -> np.ndarray:
    base = np.array(
        [
            [-1, 4, 4, 4, 4, -1],
            [4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        dtype=np.int16,
    )
    if active_branch == "down":
        base[3, 2:4] = 14
        base[4, 1:5] = 14
    elif active_branch == "up":
        base[1, 1:5] = 14
        base[2, 2:4] = 14
    elif active_branch == "left":
        base[1:5, 1] = 14
        base[2:4, 2] = 14
    elif active_branch == "right":
        base[1:5, 4] = 14
        base[2:4, 3] = 14
    return base


# Pulse-flash helpers — each returns the "currently carrying the pulse" variant of
# the element. Magenta (palette 6) is unused elsewhere in the game, so it reads
# unambiguously as "this is where the pulse is right now."

def _lit_ball_pixels() -> np.ndarray:
    return np.array(
        [
            [-1, 6, 6, 6, 6, -1],
            [6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6],
            [-1, 6, 6, 6, 6, -1],
        ],
        dtype=np.int16,
    )


def _lit_pusher_pixels() -> np.ndarray:
    return np.array(
        [
            [-1, 4, 4, 4, 4, -1],
            [4, 15, 15, 15, 15, 4],
            [4, 15, 6, 6, 15, 4],
            [4, 15, 6, 6, 15, 4],
            [4, 15, 15, 15, 15, 4],
            [-1, 4, 4, 4, 4, -1],
        ],
        dtype=np.int16,
    )


def _lit_junction_pixels() -> np.ndarray:
    return np.array(
        [
            [-1, 6, 6, 6, 6, -1],
            [6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6],
            [-1, 6, 6, 6, 6, -1],
        ],
        dtype=np.int16,
    )


class Qn7w(NovaBaseGame):
    def __init__(self) -> None:
        self._step_counter_ui = StepCounterHud(max_steps=30)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_counter_ui],
        )
        self._chains: list = []
        self._merge_pad_deposits: dict = {}
        self._pending_animation: dict | None = None
        super().__init__(
            game_id="qn7w",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        budget = level.get_data("step_budget") or 30
        self._step_counter_ui.set_max(budget)
        # Build per-chain runtime models (deep copies of mutable state).
        chain_specs = level.get_data("chains") or []
        self._chains = []
        for spec in chain_specs:
            branches = {}
            for bname, bdata in spec.get("branches", {}).items():
                branches[bname] = {
                    "balls": list(bdata["balls"]),
                    "axis": bdata["axis"],
                }
            self._chains.append(
                {
                    "pusher": spec["pusher"],
                    "stem": list(spec["stem"]),
                    "junction": spec.get("junction"),
                    "branches": branches,
                    "active_branch": spec.get("default_active_branch"),
                    "stem_axis": spec.get("stem_axis", (1, 0)),
                    "axis": spec.get("axis", (1, 0)),
                }
            )
        # Reset merge pad deposit counts and pixel state.
        self._merge_pad_deposits = {}
        for pad in level.get_sprites_by_tag("merge_pad"):
            self._merge_pad_deposits[(pad.x, pad.y)] = 0
            pad.pixels = _empty_merge_pad_pixels()
        # Reset target sockets to hollow state.
        for socket in level.get_sprites_by_tag("target_socket"):
            socket.pixels = _empty_socket_pixels()
        # Paint each junction's tab according to its chain's active branch.
        for junction in level.get_sprites_by_tag("junction"):
            jpos = (junction.x, junction.y)
            chain = self._chain_by_junction(jpos)
            if chain is not None:
                junction.pixels = _junction_pixels(chain["active_branch"])
        # No animation pending at level start.
        self._pending_animation = None

    def _chain_by_junction(self, jpos):
        for chain in self._chains:
            if chain.get("junction") == jpos:
                return chain
        return None

    def _chain_by_pusher(self, ppos):
        for chain in self._chains:
            if chain["pusher"] == ppos:
                return chain
        return None

    def step(self) -> None:
        # If a pulse animation is in flight, advance one frame and return
        # without completing the action — the engine keeps re-rendering until
        # `complete_action()` finally fires inside `_advance_animation`.
        if self._pending_animation is not None:
            self._advance_animation()
            return
        budget = self.current_level.get_data("step_budget") or 30
        self._step_counter_ui.set_current(budget - self._action_count)
        if self._action_count >= budget:
            self.lose()
            self.complete_action()
            return
        if self.action.id != GameAction.ACTION6:
            self.complete_action()
            return
        ax = self.action.data.get("x", -1)
        ay = self.action.data.get("y", -1)
        coords = self.camera.display_to_grid(int(ax), int(ay))
        if coords is None:
            self.complete_action()
            return
        gx, gy = coords
        clicked = self.current_level.get_sprite_at(gx, gy, tag="sys_click")
        if clicked is None:
            self.complete_action()
            return
        if "pusher" in clicked.tags:
            self._fire_pulse(clicked)
            # _fire_pulse sets up _pending_animation; do NOT complete the
            # action here — animation ticks will call complete_action() when
            # they finish.
            if self._pending_animation is not None:
                return
            # Fall through to complete_action (e.g. nothing to eject).
        elif "junction" in clicked.tags:
            self._cycle_junction(clicked)
        # Win check (only reachable for junction clicks and no-op pusher clicks).
        if self._check_win():
            self.complete_action()
            self.next_level()
            return
        self.complete_action()

    def _cycle_junction(self, junction_sprite: Sprite) -> None:
        jpos = (junction_sprite.x, junction_sprite.y)
        chain = self._chain_by_junction(jpos)
        if chain is None:
            return
        branches = list(chain["branches"].keys())
        if not branches:
            return
        current = chain.get("active_branch")
        if current in branches:
            idx = branches.index(current)
            chain["active_branch"] = branches[(idx + 1) % len(branches)]
        else:
            chain["active_branch"] = branches[0]
        junction_sprite.pixels = _junction_pixels(chain["active_branch"])

    def _fire_pulse(self, pusher_sprite: Sprite) -> None:
        """Begin a pulse animation along the chain attached to this pusher.

        Builds the ordered propagation path (pusher → stem balls → junction →
        active branch balls → terminal) and stores it as `_pending_animation`.
        The actual eject is deferred until `_advance_animation` walks the path
        to its end and calls `_finalize_eject`.
        """
        ppos = (pusher_sprite.x, pusher_sprite.y)
        chain = self._chain_by_pusher(ppos)
        if chain is None:
            return
        terminal_pos, eject_axis = self._terminal_and_axis(chain)
        if terminal_pos is None:
            return
        terminal_ball = self._sprite_at_position(
            terminal_pos[0], terminal_pos[1], "chain_ball"
        )
        if terminal_ball is None:
            return
        ball_color = self._ball_color(terminal_ball)
        # Build the propagation path as a list of (kind, sprite, original_pixels)
        # tuples. The original pixels are stored so each element returns to its
        # exact pre-pulse appearance after the flash moves on.
        path = [("pusher", pusher_sprite, pusher_sprite.pixels.copy())]
        for stem_pos in chain.get("stem", []):
            ball = self._sprite_at_position(stem_pos[0], stem_pos[1], "chain_ball")
            if ball is not None:
                path.append(("ball", ball, ball.pixels.copy()))
        if chain.get("junction") is not None:
            jx, jy = chain["junction"]
            junction = self._sprite_at_position(jx, jy, "junction")
            if junction is not None:
                path.append(("junction", junction, junction.pixels.copy()))
            active = chain.get("active_branch")
            if active is not None and active in chain["branches"]:
                for ball_pos in chain["branches"][active]["balls"]:
                    ball = self._sprite_at_position(
                        ball_pos[0], ball_pos[1], "chain_ball"
                    )
                    if ball is not None:
                        path.append(("ball", ball, ball.pixels.copy()))
        self._pending_animation = {
            "path": path,
            "tick": 0,
            "ball_color": ball_color,
            "terminal_ball": terminal_ball,
            "terminal_pos": terminal_pos,
            "eject_axis": eject_axis,
            "chain": chain,
            "phase": "flash",  # "flash" → "fly" → "absorb"
        }

    def _advance_animation(self) -> None:
        """Advance the pulse animation by one frame.

        Three phases, each consuming one or more engine ticks:
          flash  — walk a magenta flash along the propagation path
          fly    — visually relocate the terminal ball to its eject destination
          absorb — finalize the eject (fill socket / deposit on pad / consume)
        """
        anim = self._pending_animation
        if anim is None:
            return
        if anim["phase"] == "flash":
            path = anim["path"]
            tick = anim["tick"]
            # Restore previously-lit element to its pre-pulse appearance.
            if tick > 0 and tick - 1 < len(path):
                _, prev_sprite, prev_pixels = path[tick - 1]
                prev_sprite.pixels = prev_pixels.copy()
            if tick < len(path):
                # Light up the current element.
                kind, sprite, _ = path[tick]
                if kind == "ball":
                    sprite.pixels = _lit_ball_pixels()
                elif kind == "pusher":
                    sprite.pixels = _lit_pusher_pixels()
                elif kind == "junction":
                    sprite.pixels = _lit_junction_pixels()
                anim["tick"] = tick + 1
                return
            # Path exhausted — transition to fly phase.
            anim["phase"] = "fly"
            return
        if anim["phase"] == "fly":
            # Move the terminal ball one ball-width along the eject axis so the
            # player sees it physically arrive at its destination.
            dx, dy = anim["eject_axis"]
            tx, ty = anim["terminal_pos"]
            anim["terminal_ball"].set_position(tx + dx * BALL_SIZE, ty + dy * BALL_SIZE)
            anim["phase"] = "absorb"
            return
        # absorb: finalize the eject and clear animation state.
        self._finalize_eject(anim)
        self._pending_animation = None
        if self._check_win():
            self.complete_action()
            self.next_level()
            return
        self.complete_action()

    def _finalize_eject(self, anim: dict) -> None:
        """Apply the eject's logical effect: update destination, remove the
        terminal ball sprite from the level, and pop the chain's terminal."""
        tx, ty = anim["terminal_pos"]
        dx, dy = anim["eject_axis"]
        eject_x = tx + dx * BALL_SIZE
        eject_y = ty + dy * BALL_SIZE
        self._process_eject(eject_x, eject_y, anim["ball_color"])
        self.current_level.remove_sprite(anim["terminal_ball"])
        self._remove_terminal_from_chain(anim["chain"])

    def _sprite_at_position(self, x, y, tag):
        for s in self.current_level.get_sprites_by_tag(tag):
            if s.x == x and s.y == y:
                return s
        return None

    def _terminal_and_axis(self, chain):
        active = chain.get("active_branch")
        if active is not None and active in chain["branches"]:
            balls = chain["branches"][active]["balls"]
            if balls:
                return (balls[-1], chain["branches"][active]["axis"])
            # Active branch is empty: pulse dies; no eject.
            return (None, None)
        # No junction (L1 case): eject from end of stem in chain axis.
        stem = chain.get("stem", [])
        if stem:
            return (stem[-1], chain.get("axis", (1, 0)))
        return (None, None)

    def _ball_color(self, ball_sprite: Sprite) -> int:
        if "ball_blue" in ball_sprite.tags:
            return 9
        if "ball_yellow" in ball_sprite.tags:
            return 11
        return 9

    def _process_eject(self, eject_x: int, eject_y: int, ball_color: int) -> None:
        if eject_x < 0 or eject_y < 0 or eject_x >= GRID_W or eject_y >= GRID_H:
            return
        # Check target_socket first (position-match, since hollow sockets have
        # transparent centres that fool get_sprite_at).
        socket = self._sprite_at_position(eject_x, eject_y, "target_socket")
        if socket is not None:
            expected = 9 if "socket_blue" in socket.tags else 11
            if ball_color == expected:
                socket.pixels = _filled_socket_pixels(ball_color)
            return
        pad = self._sprite_at_position(eject_x, eject_y, "merge_pad")
        if pad is not None:
            key = (pad.x, pad.y)
            count = self._merge_pad_deposits.get(key, 0) + 1
            self._merge_pad_deposits[key] = count
            if count == 1:
                pad.pixels = _half_merge_pad_pixels(ball_color)
            elif count >= 2:
                pad.pixels = _full_merge_pad_pixels()
            return
        # Otherwise (wall, empty, etc.) — silently consumed.

    def _remove_terminal_from_chain(self, chain) -> None:
        active = chain.get("active_branch")
        if active is not None and active in chain["branches"]:
            balls = chain["branches"][active]["balls"]
            if balls:
                balls.pop()
                return
        stem = chain.get("stem", [])
        if stem:
            stem.pop()

    def _check_win(self) -> bool:
        for socket in self.current_level.get_sprites_by_tag("target_socket"):
            # Empty if centre [2, 2] is -1.
            if int(socket.pixels[2, 2]) == -1:
                return False
        for pad in self.current_level.get_sprites_by_tag("merge_pad"):
            key = (pad.x, pad.y)
            if self._merge_pad_deposits.get(key, 0) < 2:
                return False
        return True

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        for i, chain in enumerate(self._chains[:4]):
            branches = list(chain.get("branches", {}).keys())
            active = chain.get("active_branch")
            state[i, 0] = branches.index(active) if active in branches else -1
            state[i, 1] = sum(
                len(b["balls"]) for b in chain.get("branches", {}).values()
            ) + len(chain.get("stem", []))
        for i, ((px, py), count) in enumerate(
            list(self._merge_pad_deposits.items())[:4]
        ):
            state[i, 2] = count
        state[3, 3] = self._step_counter_ui.current_steps
        return state

    def _get_valid_actions(self):
        valid = []
        for sprite in self.current_level.get_sprites_by_tag("sys_click"):
            cx = sprite.x + 3
            cy = sprite.y + 3
            valid.append(
                ActionInput(id=GameAction.ACTION6, data={"x": cx, "y": cy})
            )
        return valid
