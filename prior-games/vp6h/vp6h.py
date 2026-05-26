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
    "avatar": Sprite(
        pixels=[[6, 13], [13, 6]],
        name="avatar",
        visible=True,
        collidable=True,
        tags=["avatar"],
        layer=3,
    ),
    "crystal": Sprite(
        pixels=[[10, 15], [15, 10]],
        name="crystal",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["crystal"],
        layer=2,
    ),
    "ground": Sprite(
        pixels=[[1] * 16 for _ in range(16)],
        name="ground",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["ground"],
        layer=-2,
    ),
    "lantern_bot": Sprite(
        pixels=[[11, 11, 11, 11, 11]],
        name="lantern_bot",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["lantern_bot", "lantern_rail_bot", "sys_click"],
        layer=1,
    ),
    "lantern_top": Sprite(
        pixels=[[11, 11, 11, 11, 11]],
        name="lantern_top",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["lantern_top", "lantern_rail_top", "sys_click"],
        layer=1,
    ),
    "pillar_short": Sprite(
        pixels=[[3], [3], [3]],
        name="pillar_short",
        visible=True,
        collidable=True,
        tags=["pillar"],
        layer=1,
    ),
    "pillar_tall": Sprite(
        pixels=[[3], [3], [3], [3], [3]],
        name="pillar_tall",
        visible=True,
        collidable=True,
        tags=["pillar"],
        layer=1,
    ),
    "rail_marker_bot": Sprite(
        pixels=[[2] * 16],
        name="rail_marker_bot",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["rail_bot"],
        layer=0,
    ),
    "rail_marker_top": Sprite(
        pixels=[[2] * 16],
        name="rail_marker_top",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["rail_top"],
        layer=0,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS  (exactly 3)
# ---------------------------------------------------------------------
levels = [
    Level(
        sprites=[
            sprites["ground"].clone().set_position(0, 0),
            sprites["rail_marker_top"].clone().set_position(0, 0),
            sprites["lantern_top"].clone().set_position(5, 0),
            sprites["pillar_tall"].clone().set_position(7, 3),
            sprites["crystal"].clone().set_position(7, 11),
            sprites["avatar"].clone().set_position(2, 13),
        ],
        grid_size=(16, 16),
        data={
            "step_budget": 40,
            "has_bot_lantern": False,
            "top_lantern_x": 5,
            "bot_lantern_x": 5,
        },
    ),
    Level(
        sprites=[
            sprites["ground"].clone().set_position(0, 0),
            sprites["rail_marker_top"].clone().set_position(0, 0),
            sprites["lantern_top"].clone().set_position(5, 0),
            sprites["pillar_short"].clone().set_position(14, 5),
            sprites["crystal"].clone().set_position(2, 11),
            sprites["crystal"].clone().set_position(6, 11),
            sprites["crystal"].clone().set_position(14, 11),
            sprites["avatar"].clone().set_position(1, 13),
        ],
        grid_size=(16, 16),
        data={
            "step_budget": 70,
            "has_bot_lantern": False,
            "top_lantern_x": 5,
            "bot_lantern_x": 5,
        },
    ),
    Level(
        sprites=[
            sprites["ground"].clone().set_position(0, 0),
            sprites["rail_marker_top"].clone().set_position(0, 0),
            sprites["rail_marker_bot"].clone().set_position(0, 15),
            sprites["lantern_top"].clone().set_position(5, 0),
            sprites["lantern_bot"].clone().set_position(5, 15),
            sprites["pillar_short"].clone().set_position(2, 5),
            sprites["pillar_short"].clone().set_position(10, 5),
            sprites["pillar_short"].clone().set_position(13, 8),
            sprites["crystal"].clone().set_position(2, 11),
            sprites["crystal"].clone().set_position(7, 8),
            sprites["crystal"].clone().set_position(13, 4),
            sprites["avatar"].clone().set_position(1, 13),
        ],
        grid_size=(16, 16),
        data={
            "step_budget": 120,
            "has_bot_lantern": True,
            "top_lantern_x": 5,
            "bot_lantern_x": 5,
        },
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 4
PADDING_COLOR = 5

GRID_W = 16
GRID_H = 16
LANTERN_WIDTH = 5

LIT_GROUND = 1
SHADED_GROUND = 4

AVATAR_FOOTPRINT = 2
AVATAR_MIN_COL = 0
AVATAR_MAX_COL = GRID_W - AVATAR_FOOTPRINT  # 14
AVATAR_MIN_ROW = 1                           # row 0 is the top rail
AVATAR_MAX_ROW = GRID_H - 1 - AVATAR_FOOTPRINT  # 13

TOP_RAIL_ROW = 0
BOT_RAIL_ROW = GRID_H - 1                    # 15

HUD_BAR_ROW = 63
HUD_BAR_FILL = 12  # orange
HUD_BAR_EMPTY = 4  # off-black


# ---------------------------------------------------------------------
# 4. HUD
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    def __init__(self, max_steps: int = 0) -> None:
        self._max = max_steps
        self._current = max_steps

    def reset(self, max_steps: int) -> None:
        self._max = max_steps
        self._current = max_steps

    def set_current(self, value: int) -> None:
        self._current = max(0, min(value, self._max))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self._max <= 0:
            return frame
        ratio = self._current / self._max
        n_filled = int(round(64 * ratio))
        if n_filled > 64:
            n_filled = 64
        for x in range(64):
            frame[HUD_BAR_ROW, x] = HUD_BAR_FILL if x < n_filled else HUD_BAR_EMPTY
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Vp6h(NovaBaseGame):
    def __init__(self) -> None:
        self._step_hud = StepCounterHud(0)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_hud],
        )
        self._top_lantern_x = 5
        self._bot_lantern_x = 5
        self._has_bot_lantern = False
        self._step_budget = 0
        self._steps_taken = 0
        self._lit_top: set[tuple[int, int]] = set()
        self._lit_bot: set[tuple[int, int]] = set()
        self._opaque_by_col: dict[int, set[int]] = {}
        super().__init__(
            game_id="vp6h",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 6],
        )

    # ---------- per-level setup ----------

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (GRID_W, GRID_H)
        self.camera.width = gw
        self.camera.height = gh

        budget = level.get_data("step_budget")
        self._step_budget = budget if isinstance(budget, int) and budget > 0 else 50

        has_bot = level.get_data("has_bot_lantern")
        self._has_bot_lantern = bool(has_bot)

        top_x = level.get_data("top_lantern_x")
        self._top_lantern_x = top_x if isinstance(top_x, int) else 5

        bot_x = level.get_data("bot_lantern_x")
        self._bot_lantern_x = bot_x if isinstance(bot_x, int) else 5

        self._steps_taken = 0
        self._step_hud.reset(self._step_budget)

        self._refresh_opaque_index(level)
        self._recompute_lit()
        self._repaint_ground(level)

    # ---------- shadow geometry ----------

    def _refresh_opaque_index(self, level: Level) -> None:
        self._opaque_by_col = {}
        for pillar in level.get_sprites_by_tag("pillar"):
            ph, pw = pillar.pixels.shape
            for dy in range(ph):
                for dx in range(pw):
                    if int(pillar.pixels[dy, dx]) >= 0:
                        col = pillar.x + dx
                        row = pillar.y + dy
                        self._opaque_by_col.setdefault(col, set()).add(row)

    def _recompute_lit(self) -> None:
        self._lit_top = self._compute_lit_for_rail(self._top_lantern_x, downward=True)
        if self._has_bot_lantern:
            self._lit_bot = self._compute_lit_for_rail(self._bot_lantern_x, downward=False)
        else:
            self._lit_bot = set()

    def _compute_lit_for_rail(self, x_left: int, downward: bool) -> set[tuple[int, int]]:
        lit: set[tuple[int, int]] = set()
        x_right = x_left + LANTERN_WIDTH - 1
        for x in range(x_left, x_right + 1):
            if x < 0 or x >= GRID_W:
                continue
            opaque_rows = self._opaque_by_col.get(x, set())
            if downward:
                if opaque_rows:
                    first = min(opaque_rows)
                    for y in range(0, first):
                        lit.add((x, y))
                else:
                    for y in range(GRID_H):
                        lit.add((x, y))
            else:
                if opaque_rows:
                    last = max(opaque_rows)
                    for y in range(last + 1, GRID_H):
                        lit.add((x, y))
                else:
                    for y in range(GRID_H):
                        lit.add((x, y))
        return lit

    def _is_safe(self, x: int, y: int) -> bool:
        if (x, y) in self._lit_top:
            return False
        if self._has_bot_lantern and (x, y) in self._lit_bot:
            return False
        return True

    # ---------- ground repaint ----------

    def _repaint_ground(self, level: Level | None = None) -> None:
        if level is None:
            level = self.current_level
        ground_list = level.get_sprites_by_tag("ground")
        if not ground_list:
            return
        ground = ground_list[0]
        for y in range(GRID_H):
            for x in range(GRID_W):
                ground.pixels[y, x] = SHADED_GROUND if self._is_safe(x, y) else LIT_GROUND

    # ---------- avatar movement ----------

    def _avatar(self) -> Sprite | None:
        avatars = self.current_level.get_sprites_by_tag("avatar")
        return avatars[0] if avatars else None

    def _is_walkable(self, x: int, y: int) -> bool:
        if x < AVATAR_MIN_COL or x > AVATAR_MAX_COL:
            return False
        if y < AVATAR_MIN_ROW or y > AVATAR_MAX_ROW:
            return False
        for dy in range(AVATAR_FOOTPRINT):
            for dx in range(AVATAR_FOOTPRINT):
                cx = x + dx
                cy = y + dy
                if cy in self._opaque_by_col.get(cx, set()):
                    return False
        return True

    # ---------- crystal pickup ----------

    def _try_pickup(self) -> None:
        avatar = self._avatar()
        if avatar is None:
            return
        ax = avatar.x
        ay = avatar.y
        ax2 = ax + AVATAR_FOOTPRINT
        ay2 = ay + AVATAR_FOOTPRINT
        for crystal in list(self.current_level.get_sprites_by_tag("crystal")):
            if crystal.interaction == InteractionMode.REMOVED:
                continue
            ch, cw = crystal.pixels.shape
            cx = crystal.x
            cy = crystal.y
            cx2 = cx + cw
            cy2 = cy + ch
            if ax < cx2 and ax2 > cx and ay < cy2 and ay2 > cy:
                if self._is_safe(ax, ay):
                    crystal.set_interaction(InteractionMode.REMOVED)

    def _crystals_remaining(self) -> int:
        count = 0
        for crystal in self.current_level.get_sprites_by_tag("crystal"):
            if crystal.interaction != InteractionMode.REMOVED:
                count += 1
        return count

    # ---------- lantern slide ----------

    def _slide_lantern(self, gx: int, *, top: bool) -> None:
        new_left = max(0, min(GRID_W - LANTERN_WIDTH, gx - LANTERN_WIDTH // 2))
        if top:
            self._top_lantern_x = new_left
            for sprite in self.current_level.get_sprites_by_tag("lantern_top"):
                sprite.set_position(new_left, TOP_RAIL_ROW)
        else:
            self._bot_lantern_x = new_left
            for sprite in self.current_level.get_sprites_by_tag("lantern_bot"):
                sprite.set_position(new_left, BOT_RAIL_ROW)

    # ---------- step ----------

    def step(self) -> None:
        action = self.action

        self._steps_taken += 1
        self._step_hud.set_current(self._step_budget - self._steps_taken)

        if action.id == GameAction.ACTION6:
            data = action.data or {}
            x_pix = int(data.get("x", 0))
            y_pix = int(data.get("y", 0))
            grid = self.camera.display_to_grid(x_pix, y_pix)
            if grid is not None:
                gx, gy = grid
                if gy == TOP_RAIL_ROW:
                    self._slide_lantern(gx, top=True)
                    self._recompute_lit()
                    self._repaint_ground()
                elif gy == BOT_RAIL_ROW and self._has_bot_lantern:
                    self._slide_lantern(gx, top=False)
                    self._recompute_lit()
                    self._repaint_ground()
        elif action.id in (
            GameAction.ACTION1,
            GameAction.ACTION2,
            GameAction.ACTION3,
            GameAction.ACTION4,
        ):
            avatar = self._avatar()
            if avatar is not None:
                dx, dy = 0, 0
                if action.id == GameAction.ACTION1:
                    dy = -1
                elif action.id == GameAction.ACTION2:
                    dy = 1
                elif action.id == GameAction.ACTION3:
                    dx = -1
                elif action.id == GameAction.ACTION4:
                    dx = 1
                new_x = avatar.x + dx
                new_y = avatar.y + dy
                if self._is_walkable(new_x, new_y):
                    avatar.set_position(new_x, new_y)
                    self._try_pickup()

        if self._crystals_remaining() == 0:
            self.complete_action()
            self.next_level()
            return

        if self._steps_taken >= self._step_budget:
            self.complete_action()
            self.lose()
            return

        self.complete_action()

    # ---------- engine hooks ----------

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = max(0, self._step_budget - self._steps_taken)
        state[0, 1] = self._top_lantern_x
        state[0, 2] = self._bot_lantern_x if self._has_bot_lantern else -1
        state[0, 3] = self._crystals_remaining()
        return state
