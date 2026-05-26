"""Stack-Pillar-Lift."""

import numpy as np
from novaengine import NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 0
FLOOR_COLOR = 11
PILLAR_COLOR = 13
BASE_COLOR = 5
CLAW_COLOR = 6
CAP_MARK = 14
TARGET_EMPTY = 5
TARGET_PANEL = 12
TARGET_SEPARATOR = 0
UNDO_OFF = 1
UNDO_ON = 3

BLOCK_COLORS = {
    "r": 2,
    "y": 4,
    "g": 3,
    "p": 9,
}


class StepBarHud(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.game.max_steps <= 0:
            return frame
        ratio = max(0.0, min(1.0, self.game.steps_left / self.game.max_steps))
        filled = int(round(frame.shape[0] * ratio))
        cutoff = frame.shape[0] - filled
        for y in range(frame.shape[0]):
            frame[y, frame.shape[1] - 1] = 4 if y >= cutoff else 5
        return frame


class Gg07(NovaBaseGame):
    WIDTH = 21
    HEIGHT = 21
    BASE_Y = 19
    RAIL_Y = 2
    HELD_Y = 3
    UNDO_POS = (0, 2)
    TARGET_X = 18
    TARGET_TOP_Y = 2
    TARGET_SLOTS = 3
    TARGET_SPACING = 4
    PILLAR_XS = [2, 5, 8, 11, 14]

    def __init__(self) -> None:
        self.hud = StepBarHud(self)
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=BACKGROUND_COLOR,
            interfaces=[self.hud],
        )
        levels = [
            Level(grid_size=(self.WIDTH, self.HEIGHT), sprites=[], data={"Level": 1}),
            Level(grid_size=(self.WIDTH, self.HEIGHT), sprites=[], data={"Level": 2}),
            Level(grid_size=(self.WIDTH, self.HEIGHT), sprites=[], data={"Level": 3}),
        ]

        self.pillars = []
        self.targets = []
        self.capacities = []
        self.fixed_bases = []
        self.holder = None
        self.lift_origin = None
        self.crane_index = 0
        self.undo_required = False
        self.undo_used = False
        self.max_steps = 0
        self.steps_left = 0

        super().__init__(
            game_id="gg07",
            levels=levels,
            camera=camera,
            available_actions=[3, 4, 5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        self.camera.width = self.WIDTH
        self.camera.height = self.HEIGHT
        self.holder = None
        self.lift_origin = None
        self.crane_index = 0
        self.undo_used = False

        lvl = level.get_data("Level")
        if lvl == 1:
            self.max_steps = 13
            self.undo_required = False
            self.capacities = [None, None, None]
            self.fixed_bases = [False, False, False]
            self.pillars = [["r", "y"], [], ["g", "p"]]
            self.targets = [["r", "p"], [], ["g", "y"]]
        elif lvl == 2:
            self.max_steps = 22
            self.undo_required = True
            self.capacities = [None, None, None, None]
            self.fixed_bases = [False, False, False, False]
            self.pillars = [["r", "y"], ["g"], [], ["p"]]
            self.targets = [[], ["g", "y", "p"], ["r"], []]
        else:
            self.max_steps = 19
            self.undo_required = True
            self.capacities = [None, None, 1, 1, None]
            self.fixed_bases = [False, False, False, False, False]
            self.pillars = [["y"], ["g", "p"], [], [], []]
            self.targets = [["p"], ["g", "y"], [], [], []]

        self.steps_left = self.max_steps
        self._sync_sprites()

    def _consume_step(self) -> None:
        self.steps_left -= 1

    def _move_crane(self, delta: int) -> bool:
        new_index = self.crane_index + delta
        if not 0 <= new_index < len(self.pillars):
            return False
        self.crane_index = new_index
        if self.holder is not None:
            self.lift_origin = None
        return True

    def _lift(self) -> bool:
        stack = self.pillars[self.crane_index]
        if not stack:
            return False
        self.holder = stack.pop()
        self.lift_origin = self.crane_index
        return True

    def _drop(self) -> bool:
        cap = self.capacities[self.crane_index]
        if cap is not None and len(self.pillars[self.crane_index]) >= cap:
            return False
        self.pillars[self.crane_index].append(self.holder)
        self.holder = None
        self.lift_origin = None
        return True

    def _operate_crane(self) -> bool:
        if self.holder is None:
            return self._lift()
        return self._drop()

    def _undo_lift(self) -> bool:
        if self.holder is None or self.lift_origin != self.crane_index:
            return False
        self.pillars[self.crane_index].append(self.holder)
        self.holder = None
        self.lift_origin = None
        self.undo_used = True
        return True

    def _check_win(self) -> bool:
        if self.holder is not None:
            return False
        return self.pillars == self.targets

    def _block_sprite(self, color_key: str, name: str, layer: int, x: int, y: int) -> Sprite:
        return Sprite([[BLOCK_COLORS[color_key]]], name=name, layer=layer).set_position(x, y)

    def _sync_sprites(self) -> None:
        sprites = []

        for y in range(1, self.HEIGHT):
            for x in range(self.WIDTH):
                color = FLOOR_COLOR if (x + y) % 2 == 0 else TARGET_PANEL
                sprites.append(Sprite([[color]], name=f"floor_{x}_{y}", layer=0).set_position(x, y))

        crane_x = self.PILLAR_XS[self.crane_index]
        sprites.append(Sprite([[CLAW_COLOR]], name="crane_left", layer=5).set_position(crane_x - 1, self.RAIL_Y))
        sprites.append(Sprite([[CLAW_COLOR]], name="crane_head", layer=5).set_position(crane_x, self.RAIL_Y))
        sprites.append(Sprite([[CLAW_COLOR]], name="crane_right", layer=5).set_position(crane_x + 1, self.RAIL_Y))
        sprites.append(Sprite([[CLAW_COLOR]], name="crane_cable", layer=5).set_position(crane_x, self.HELD_Y))
        if self.holder is not None:
            sprites.append(self._block_sprite(self.holder, "held_block", 6, crane_x, self.HELD_Y + 1))

        ux, uy = self.UNDO_POS
        undo_color = UNDO_ON if (not self.undo_required or self.undo_used) else UNDO_OFF
        sprites.append(Sprite([[undo_color]], name="undo_marker", layer=5).set_position(ux, uy))

        for y in range(1, self.HEIGHT):
            sprites.append(Sprite([[TARGET_SEPARATOR]], name=f"target_separator_{y}", layer=2).set_position(16, y))
        for idx in range(len(self.pillars)):
            top_y = self.TARGET_TOP_Y + idx * self.TARGET_SPACING
            for dy in range(self.TARGET_SLOTS):
                for dx in range(3):
                    sprites.append(
                        Sprite([[TARGET_PANEL]], name=f"target_panel_{idx}_{dx}_{dy}", layer=1)
                        .set_position(self.TARGET_X - 1 + dx, top_y + dy)
                    )

        for idx, stack in enumerate(self.pillars):
            px = self.PILLAR_XS[idx]
            cap = self.capacities[idx]
            height = cap if cap is not None else 5
            for h in range(height + 1):
                y = self.BASE_Y - h
                if 5 <= y <= self.BASE_Y:
                    sprites.append(Sprite([[PILLAR_COLOR]], name=f"pillar_{idx}_{h}", layer=1).set_position(px, y))
            if self.fixed_bases[idx]:
                sprites.append(Sprite([[BASE_COLOR]], name=f"fixed_base_{idx}", layer=3).set_position(px, self.BASE_Y))
            if cap is not None:
                sprites.append(Sprite([[CAP_MARK]], name=f"cap_{idx}", layer=5).set_position(px + 1, self.BASE_Y - cap))

            for depth, color_key in enumerate(stack):
                y = self.BASE_Y - depth
                sprites.append(self._block_sprite(color_key, f"block_{idx}_{depth}", 4, px, y))

            target_top_y = self.TARGET_TOP_Y + idx * self.TARGET_SPACING
            slots = self.targets[idx]
            for slot in range(self.TARGET_SLOTS):
                tx = self.TARGET_X
                ty = target_top_y + (self.TARGET_SLOTS - 1 - slot)
                if slot < len(slots):
                    sprites.append(self._block_sprite(slots[slot], f"target_{idx}_{slot}", 3, tx, ty))
                else:
                    sprites.append(Sprite([[TARGET_EMPTY]], name=f"target_empty_{idx}_{slot}", layer=2).set_position(tx, ty))

        self.current_level._sprites = sprites

    def step(self) -> None:
        acted = False
        if self.action.id == GameAction.ACTION3:
            acted = self._move_crane(-1)
        elif self.action.id == GameAction.ACTION4:
            acted = self._move_crane(1)
        elif self.action.id == GameAction.ACTION5:
            acted = self._undo_lift()
        elif self.action.id == GameAction.ACTION6:
            acted = self._operate_crane()

        if acted:
            self._consume_step()

        self._sync_sprites()
        if self._check_win():
            self.next_level()
        elif self.steps_left <= 0:
            self.lose()

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        rows = []
        for stack in self.pillars:
            row = [BLOCK_COLORS[color_key] for color_key in stack]
            row += [0] * (5 - len(row))
            rows.append(row[:5])
        return np.array(rows, dtype=np.int16)
