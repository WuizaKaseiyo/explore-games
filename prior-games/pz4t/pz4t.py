"""."""

from typing import Optional

import numpy as np
from novaengine import (
    ActionInput,
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
    "anchor_marker": Sprite(
        pixels=[[1]],
        name="anchor_marker",
        visible=True,
        collidable=False,
        interaction=InteractionMode.REMOVED,
        tags=["anchor"],
        layer=4,
    ),
    "comp_green_bar2": Sprite(
        pixels=[[14, 14]],
        name="comp_green_bar2",
        visible=True,
        collidable=True,
        tags=["component", "green"],
        layer=2,
    ),
    "comp_magenta_bar3": Sprite(
        pixels=[[6, 6, 6]],
        name="comp_magenta_bar3",
        visible=True,
        collidable=True,
        tags=["component", "magenta"],
        layer=2,
    ),
    "comp_red_Z": Sprite(
        pixels=[
            [8, 8, -1],
            [-1, 8, 8],
        ],
        name="comp_red_Z",
        visible=True,
        collidable=True,
        tags=["component", "red"],
        layer=2,
    ),
    "comp_red_bar3": Sprite(
        pixels=[[8, 8, 8]],
        name="comp_red_bar3",
        visible=True,
        collidable=True,
        tags=["component", "red"],
        layer=2,
    ),
    "comp_yellow_L": Sprite(
        pixels=[
            [11, -1],
            [11, 11],
        ],
        name="comp_yellow_L",
        visible=True,
        collidable=True,
        tags=["component", "yellow"],
        layer=2,
    ),
    "comp_yellow_vbar2": Sprite(
        pixels=[[11], [11]],
        name="comp_yellow_vbar2",
        visible=True,
        collidable=True,
        tags=["component", "yellow"],
        layer=2,
    ),
    "target_shadow": Sprite(
        pixels=[[3]],
        name="target_shadow",
        visible=True,
        collidable=False,
        interaction=InteractionMode.INTANGIBLE,
        tags=["target"],
        layer=0,
    ),
}


def _shadows(cells):
    """Return clones of target_shadow positioned at each (x, y) cell."""
    return [sprites["target_shadow"].clone().set_position(x, y) for (x, y) in cells]


# ---------------------------------------------------------------------
# 2. LEVELS — each target is ONE single connected dark-grey region;
#    the components together must tile it exactly.
# ---------------------------------------------------------------------

# L1 target: L-pentomino, 5 cells, top-3 horizontal + 2 vertical down on left.
L1_TARGET_CELLS = [
    (3, 2), (4, 2), (5, 2),
    (3, 3),
    (3, 4),
]

# L2 target: U-shape, 7 cells (top corners + sides + bottom bar).
L2_TARGET_CELLS = [
    (3, 3),         (5, 3),
    (3, 4),         (5, 4),
    (3, 5), (4, 5), (5, 5),
]

# L3 target: 12 cells. Includes an S-tetromino sub-region that requires
# the red Z component to be flipped (mirror_lr) to fit.
L3_TARGET_CELLS = [
    (4, 2), (5, 2), (6, 2),                         # magenta 3-bar
    (4, 3), (5, 3),                                 # part of S-region
    (3, 4), (4, 4), (5, 4),                         # part of S-region + yellow
    (5, 5), (6, 5),                                 # rest of yellow L
    (3, 5), (3, 6),                                 # green 2-bar (vertical, after rotation)
]


levels = [
    Level(
        sprites=[
            sprites["comp_red_bar3"].clone().set_position(1, 8),
            sprites["comp_yellow_vbar2"].clone().set_position(6, 7),
            *_shadows(L1_TARGET_CELLS),
            sprites["anchor_marker"].clone(),
        ],
        grid_size=(10, 10),
        data={"StepBudget": 16},
    ),
    Level(
        sprites=[
            sprites["comp_red_bar3"].clone().set_position(1, 9),
            sprites["comp_yellow_vbar2"].clone().set_position(5, 9),
            sprites["comp_green_bar2"].clone().set_position(8, 10),
            *_shadows(L2_TARGET_CELLS),
            sprites["anchor_marker"].clone(),
        ],
        grid_size=(12, 12),
        data={"StepBudget": 28},
    ),
    Level(
        sprites=[
            sprites["comp_red_Z"].clone().set_position(1, 11),
            sprites["comp_yellow_L"].clone().set_position(5, 11),
            sprites["comp_green_bar2"].clone().set_position(9, 11),
            sprites["comp_magenta_bar3"].clone().set_position(1, 13),
            *_shadows(L3_TARGET_CELLS),
            sprites["anchor_marker"].clone(),
        ],
        grid_size=(14, 14),
        data={"StepBudget": 40},
    ),
]


# ---------------------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 2
PADDING_COLOR = 4

# ACTION1/2 toggle vertical mirror (top-bottom reflection);
# ACTION3/4 toggle horizontal mirror (left-right reflection);
# ACTION5 rotates 90° clockwise; ACTION6 is the click pick-place verb.
VERTICAL_MIRROR_ACTIONS = (GameAction.ACTION1, GameAction.ACTION2)
HORIZONTAL_MIRROR_ACTIONS = (GameAction.ACTION3, GameAction.ACTION4)


# ---------------------------------------------------------------------
# 4. HUD WIDGETS
# ---------------------------------------------------------------------
class StepCounterHud(RenderableUserDisplay):
    """."""

    def __init__(self) -> None:
        self.max_steps = 0
        self.current_steps = 0

    def set_max(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_steps(self, current: int) -> None:
        self.current_steps = max(0, min(current, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame
        ratio = self.current_steps / self.max_steps
        filled = round(64 * ratio)
        for x in range(64):
            if x < filled:
                frame[63, x] = 0
            else:
                frame[63, x] = 5
        return frame


# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Pz4t(NovaBaseGame):
    """."""

    def __init__(self) -> None:
        camera = Camera(background=BACKGROUND_COLOR, letter_box=PADDING_COLOR)
        self._step_counter_ui = StepCounterHud()
        camera.replace_interface([self._step_counter_ui])
        self.held_component: Optional[Sprite] = None
        self.anchor_offset: tuple[int, int] = (0, 0)
        self.steps_left: int = 0
        self.step_budget: int = 0
        super().__init__(
            game_id="pz4t",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        self.held_component = None
        self.anchor_offset = (0, 0)
        budget = level.get_data("StepBudget")
        self.step_budget = int(budget) if budget is not None else 30
        self.steps_left = self.step_budget
        self._step_counter_ui.set_max(self.step_budget)
        for s in level.get_sprites_by_tag("anchor"):
            s.set_interaction(InteractionMode.REMOVED)

    def step(self) -> None:
        self.steps_left = max(0, self.steps_left - 1)
        self._step_counter_ui.set_steps(self.steps_left)

        action_id = self.action.id
        if action_id == GameAction.ACTION6:
            self._handle_click()
        elif action_id == GameAction.ACTION5:
            self._handle_rotate()
        elif action_id in VERTICAL_MIRROR_ACTIONS:
            self._handle_mirror_ud()
        elif action_id in HORIZONTAL_MIRROR_ACTIONS:
            self._handle_mirror_lr()

        if self.steps_left <= 0:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def _handle_click(self) -> None:
        x = int(self.action.data.get("x", 0))
        y = int(self.action.data.get("y", 0))
        cell = self.camera.display_to_grid(x, y)
        if cell is None:
            return
        gx, gy = cell

        if self.held_component is None:
            hit = self.current_level.get_sprite_at(gx, gy, tag="component")
            if hit is None:
                return
            self.held_component = hit
            self.anchor_offset = (gx - hit.x, gy - hit.y)
            self._update_anchor_marker()
        else:
            comp = self.held_component
            comp.set_position(gx - self.anchor_offset[0], gy - self.anchor_offset[1])
            self.held_component = None
            self._hide_anchor_marker()
            if self._check_win():
                self.next_level()

    def _handle_rotate(self) -> None:
        if self.held_component is None:
            return
        old_height = self.held_component.height
        a_c, a_r = self.anchor_offset
        self.held_component.rotate(90)
        self.anchor_offset = (old_height - 1 - a_r, a_c)
        self._update_anchor_marker()

    def _handle_mirror_ud(self) -> None:
        if self.held_component is None:
            return
        comp = self.held_component
        a_c, a_r = self.anchor_offset
        h = comp.height
        comp.set_mirror_ud(not comp._mirror_ud)
        self.anchor_offset = (a_c, h - 1 - a_r)
        self._update_anchor_marker()

    def _handle_mirror_lr(self) -> None:
        if self.held_component is None:
            return
        comp = self.held_component
        a_c, a_r = self.anchor_offset
        w = comp.width
        comp.set_mirror_lr(not comp._mirror_lr)
        self.anchor_offset = (w - 1 - a_c, a_r)
        self._update_anchor_marker()

    def _update_anchor_marker(self) -> None:
        if self.held_component is None:
            return
        comp = self.held_component
        ax = comp.x + self.anchor_offset[0]
        ay = comp.y + self.anchor_offset[1]
        markers = self.current_level.get_sprites_by_tag("anchor")
        if markers:
            m = markers[0]
            m.set_position(ax, ay)
            m.set_interaction(InteractionMode.INTANGIBLE)

    def _hide_anchor_marker(self) -> None:
        for m in self.current_level.get_sprites_by_tag("anchor"):
            m.set_interaction(InteractionMode.REMOVED)

    def _component_filled_cells(self, comp: Sprite) -> set[tuple[int, int]]:
        rendered = comp.render()
        cells: set[tuple[int, int]] = set()
        h, w = rendered.shape
        for r in range(h):
            for c in range(w):
                if int(rendered[r, c]) != -1:
                    cells.add((comp.x + c, comp.y + r))
        return cells

    def _check_win(self) -> bool:
        components = self.current_level.get_sprites_by_tag("component")
        union: set[tuple[int, int]] = set()
        total = 0
        for comp in components:
            cells = self._component_filled_cells(comp)
            if cells & union:
                return False
            union |= cells
            total += len(cells)
        target_cells = {
            (t.x, t.y) for t in self.current_level.get_sprites_by_tag("target")
        }
        return union == target_cells

    def _get_hidden_state(self) -> np.ndarray:
        state = np.zeros((4, 4), dtype=np.int16)
        state[0, 0] = self.steps_left
        state[0, 1] = 1 if self.held_component is not None else 0
        state[0, 2] = self.anchor_offset[0]
        state[0, 3] = self.anchor_offset[1]
        return state

    def _get_valid_actions(self) -> list[ActionInput]:
        return super()._get_valid_actions()
