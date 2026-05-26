"""."""

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
    "ball": Sprite(
        pixels=[
            [-1, 12, 12, 12, -1],
            [12, 4, 4, 4, 12],
            [12, 4, 12, 4, 12],
            [12, 4, 4, 4, 12],
            [-1, 12, 12, 12, -1],
        ],
        name="ball",
        visible=True,
        collidable=True,
        tags=["ball"],
        layer=2,
    ),
    "platform": Sprite(
        pixels=[
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ],
        name="platform",
        visible=True,
        collidable=True,
        tags=["platform"],
        layer=1,
    ),
    "anchored_ball": Sprite(
        pixels=[
            [-1, 12, 12, 12, -1],
            [12, 5, 5, 5, 12],
            [12, 5, 5, 5, 12],
            [12, 5, 5, 5, 12],
            [-1, 12, 12, 12, -1],
        ],
        name="anchored_ball",
        visible=True,
        collidable=True,
        tags=["ball", "anchored"],
        layer=2,
    ),
    "water_layer": Sprite(
        pixels=[[-1] * 60 for _ in range(60)],
        name="water_layer",
        visible=True,
        collidable=False,
        tags=["water"],
        layer=0,
    ),
    "target_ring": Sprite(
        pixels=[
            [-1, 14, 14, 14, -1],
            [14, -1, -1, -1, 14],
            [14, -1, -1, -1, 14],
            [14, -1, -1, -1, 14],
            [-1, 14, 14, 14, -1],
        ],
        name="target_ring",
        visible=True,
        collidable=False,
        tags=["target"],
        layer=1,
    ),
}


# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
levels = [
    Level(
        sprites=[
            sprites["water_layer"].clone().set_position(0, 0),
            sprites["ball"].clone().set_position(15, 40),
            sprites["anchored_ball"]
            .clone()
            .set_position(15, 40)
            .set_interaction(InteractionMode.REMOVED),
            sprites["target_ring"]
            .clone()
            .color_remap(14, 12)
            .set_position(40, 20),
        ],
        grid_size=(60, 60),
        data={"WaterLevel": 8, "StepCounter": 25, "AnchorEnabled": False},
    ),
    Level(
        sprites=[
            sprites["water_layer"].clone().set_position(0, 0),
            sprites["ball"].clone().set_position(5, 45),
            sprites["anchored_ball"]
            .clone()
            .set_position(5, 45)
            .set_interaction(InteractionMode.REMOVED),
            sprites["target_ring"]
            .clone()
            .color_remap(14, 12)
            .set_position(50, 15),
            sprites["platform"].clone().set_position(0, 30),
        ],
        grid_size=(60, 60),
        data={"WaterLevel": 9, "StepCounter": 30, "AnchorEnabled": False},
    ),
    Level(
        sprites=[
            sprites["water_layer"].clone().set_position(0, 0),
            sprites["ball"].clone().set_position(15, 45),
            sprites["anchored_ball"]
            .clone()
            .set_position(15, 45)
            .set_interaction(InteractionMode.REMOVED),
            sprites["ball"]
            .clone()
            .color_remap(12, 14)
            .set_position(40, 45),
            sprites["anchored_ball"]
            .clone()
            .color_remap(12, 14)
            .set_position(40, 45)
            .set_interaction(InteractionMode.REMOVED),
            sprites["target_ring"]
            .clone()
            .color_remap(14, 12)
            .set_position(40, 25),
            sprites["target_ring"].clone().set_position(15, 25),
            sprites["platform"].clone().set_position(20, 30),
        ],
        grid_size=(60, 60),
        data={"WaterLevel": 9, "StepCounter": 45, "AnchorEnabled": True},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 1
PADDING_COLOR = 3
CELL_PIXELS = 5
N_CELLS = 12
WATER_COLOR = 10
HUD_REMAINING_COLOR = 12
HUD_DEPLETED_COLOR = 5


# ---------------------------------------------------------------------
# 4. HUD WIDGET
# ---------------------------------------------------------------------
class StepBarHud(RenderableUserDisplay):
    """."""

    def __init__(self, max_steps: int = 1) -> None:
        self.max_steps = max_steps
        self.remaining = max_steps

    def update(self, remaining: int) -> None:
        self.remaining = max(0, min(remaining, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        bar_width = 60
        bar_x_start = 2
        ratio = self.remaining / self.max_steps
        filled = int(round(bar_width * ratio))
        if filled > bar_width:
            filled = bar_width
        if filled < 0:
            filled = 0
        for x in range(bar_width):
            color = HUD_REMAINING_COLOR if x < filled else HUD_DEPLETED_COLOR
            frame[0, bar_x_start + x] = color
        return frame


# ---------------------------------------------------------------------
# 5. GAME CLASS
# ---------------------------------------------------------------------
class Kx14(NovaBaseGame):
    def __init__(self) -> None:
        self._step_bar = StepBarHud(max_steps=1)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._step_bar],
        )
        self._water_level: int = 0
        self._water_sprite: Sprite | None = None
        self._balls: list[dict] = []
        self._platforms: list[tuple[int, int, int]] = []
        self._targets: list[tuple[int, int, int]] = []
        self._anchor_enabled: bool = False
        self._max_steps: int = 0
        self._steps_used: int = 0
        super().__init__(
            game_id="kx14",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (60, 60)
        self.camera.width = gw
        self.camera.height = gh

        wl = level.get_data("WaterLevel")
        self._water_level = int(wl) if wl is not None else 8
        ms = level.get_data("StepCounter")
        self._max_steps = int(ms) if ms is not None else 25
        self._anchor_enabled = bool(level.get_data("AnchorEnabled"))
        self._steps_used = 0

        self._step_bar.max_steps = self._max_steps
        self._step_bar.update(self._max_steps)

        water_sprites = level.get_sprites_by_tag("water")
        self._water_sprite = water_sprites[0] if water_sprites else None

        self._platforms = []
        for p in level.get_sprites_by_tag("platform"):
            col_start = int(p.x // CELL_PIXELS)
            col_end = col_start + (p.pixels.shape[1] // CELL_PIXELS) - 1
            row = int(p.y // CELL_PIXELS)
            self._platforms.append((col_start, col_end, row))

        self._targets = []
        for t in level.get_sprites_by_tag("target"):
            col = int(t.x // CELL_PIXELS)
            row = int(t.y // CELL_PIXELS)
            color = self._dominant_color(t)
            self._targets.append((col, row, color))

        self._balls = []
        ball_sprites = level.get_sprites_by_tag("ball")
        groups: dict[tuple[int, int], list[Sprite]] = {}
        for b in ball_sprites:
            col = int(b.x // CELL_PIXELS)
            row = int(b.y // CELL_PIXELS)
            groups.setdefault((col, row), []).append(b)
        for (col, row), pair in groups.items():
            float_s: Sprite | None = None
            anchor_s: Sprite | None = None
            for s in pair:
                if "anchored" in s.tags:
                    anchor_s = s
                else:
                    float_s = s
            if float_s is None or anchor_s is None:
                continue
            color = self._dominant_color(float_s)
            self._balls.append(
                {
                    "float_s": float_s,
                    "anchor_s": anchor_s,
                    "col": col,
                    "row": row,
                    "color": color,
                    "anchored": False,
                }
            )

        self._redraw_water()

    # ----- helpers -----

    def _dominant_color(self, sprite: Sprite) -> int:
        flat = sprite.pixels[sprite.pixels >= 0]
        if flat.size == 0:
            return 0
        unique, counts = np.unique(flat, return_counts=True)
        order = np.argsort(-counts)
        for idx in order:
            c = int(unique[idx])
            if c not in (4, 5):
                return c
        return int(unique[order[0]])

    def _max_platform_row_in_col_in_range(
        self, col: int, lo: int, hi: int
    ) -> int | None:
        best: int | None = None
        for cs, ce, row in self._platforms:
            if cs <= col <= ce and lo <= row <= hi:
                if best is None or row > best:
                    best = row
        return best

    def _min_platform_row_in_col_in_range(
        self, col: int, lo: int, hi: int
    ) -> int | None:
        best: int | None = None
        for cs, ce, row in self._platforms:
            if cs <= col <= ce and lo <= row <= hi:
                if best is None or row < best:
                    best = row
        return best

    def _is_platform_cell(self, col: int, row: int) -> bool:
        for cs, ce, prow in self._platforms:
            if prow == row and cs <= col <= ce:
                return True
        return False

    def _cell_occupied_by_other_ball(
        self, col: int, row: int, exclude_index: int
    ) -> bool:
        for i, b in enumerate(self._balls):
            if i == exclude_index:
                continue
            if b["col"] == col and b["row"] == row:
                return True
        return False

    def _redraw_water(self) -> None:
        if self._water_sprite is None:
            return
        wp = max(0, min(60, self._water_level * CELL_PIXELS))
        new_pixels = np.full((60, 60), -1, dtype=np.int8)
        new_pixels[wp:, :] = WATER_COLOR
        self._water_sprite.pixels = new_pixels

    def _reproject_balls(self) -> None:
        for i, b in enumerate(self._balls):
            if b["anchored"]:
                continue
            c = b["col"]
            r = b["row"]
            if r > self._water_level:
                P = self._max_platform_row_in_col_in_range(
                    c, self._water_level, r - 1
                )
                new_r = P + 1 if P is not None else self._water_level
            elif r < self._water_level:
                P = self._min_platform_row_in_col_in_range(
                    c, r + 1, self._water_level
                )
                new_r = P - 1 if P is not None else self._water_level
            else:
                new_r = r

            attempts = 0
            while self._cell_occupied_by_other_ball(c, new_r, i):
                attempts += 1
                if attempts > N_CELLS:
                    new_r = r
                    break
                if r > self._water_level:
                    new_r += 1
                elif r < self._water_level:
                    new_r -= 1
                else:
                    new_r = r
                    break
                if new_r < 0 or new_r >= N_CELLS:
                    new_r = r
                    break

            b["row"] = new_r
            self._sync_ball_position(b)

    def _sync_ball_position(self, b: dict) -> None:
        px = b["col"] * CELL_PIXELS
        py = b["row"] * CELL_PIXELS
        b["float_s"].set_position(px, py)
        b["anchor_s"].set_position(px, py)

    def _tilt(self, dx: int) -> None:
        if dx > 0:
            order = sorted(
                range(len(self._balls)), key=lambda i: -self._balls[i]["col"]
            )
        else:
            order = sorted(
                range(len(self._balls)), key=lambda i: self._balls[i]["col"]
            )
        for i in order:
            b = self._balls[i]
            if b["anchored"]:
                continue
            new_c = b["col"] + dx
            if new_c < 0 or new_c >= N_CELLS:
                continue
            if self._is_platform_cell(new_c, b["row"]):
                continue
            if self._cell_occupied_by_other_ball(new_c, b["row"], i):
                continue
            b["col"] = new_c
            self._sync_ball_position(b)

    def _check_win(self) -> bool:
        for col, row, target_color in self._targets:
            matched = False
            for b in self._balls:
                if (
                    b["col"] == col
                    and b["row"] == row
                    and b["color"] == target_color
                ):
                    matched = True
                    break
            if not matched:
                return False
        return True

    def _toggle_anchor_at_click(self, click_x: int, click_y: int) -> bool:
        if not self._anchor_enabled:
            return False
        gp = self.camera.display_to_grid(int(click_x), int(click_y))
        if gp is None:
            return False
        gx, gy = gp
        cell_col = int(gx) // CELL_PIXELS
        cell_row = int(gy) // CELL_PIXELS
        for b in self._balls:
            if b["col"] == cell_col and b["row"] == cell_row:
                b["anchored"] = not b["anchored"]
                if b["anchored"]:
                    b["float_s"].set_interaction(InteractionMode.REMOVED)
                    b["anchor_s"].set_interaction(InteractionMode.TANGIBLE)
                else:
                    b["float_s"].set_interaction(InteractionMode.TANGIBLE)
                    b["anchor_s"].set_interaction(InteractionMode.REMOVED)
                return True
        return False

    # ----- step -----

    def step(self) -> None:
        self._step_bar.update(self._max_steps - self._steps_used)

        if self._steps_used >= self._max_steps:
            self.lose()
            self.complete_action()
            return

        consumed = False
        action_id = self.action.id

        if action_id == GameAction.ACTION1:
            if self._water_level > 0:
                self._water_level -= 1
                self._redraw_water()
            self._reproject_balls()
            consumed = True
        elif action_id == GameAction.ACTION2:
            if self._water_level < N_CELLS:
                self._water_level += 1
                self._redraw_water()
            self._reproject_balls()
            consumed = True
        elif action_id == GameAction.ACTION3:
            self._tilt(-1)
            self._reproject_balls()
            consumed = True
        elif action_id == GameAction.ACTION4:
            self._tilt(+1)
            self._reproject_balls()
            consumed = True
        elif action_id == GameAction.ACTION6:
            data = getattr(self.action, "data", None) or {}
            cx = int(data.get("x", -1))
            cy = int(data.get("y", -1))
            if self._toggle_anchor_at_click(cx, cy):
                self._reproject_balls()
                consumed = True

        if consumed:
            self._steps_used += 1
            self._step_bar.update(self._max_steps - self._steps_used)

        if self._check_win():
            self.next_level()
            self.complete_action()
            return

        if self._steps_used >= self._max_steps:
            self.lose()

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self._water_level
        state[0, 1] = max(0, self._max_steps - self._steps_used)
        state[0, 2] = sum(1 for b in self._balls if b["anchored"])
        state[0, 3] = len(self._balls)
        for i, b in enumerate(self._balls[:3]):
            state[i + 1, 0] = int(b["col"])
            state[i + 1, 1] = int(b["row"])
            state[i + 1, 2] = int(b["anchored"])
            state[i + 1, 3] = int(b["color"])
        return state
