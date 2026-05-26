"""mr8k."""

from __future__ import annotations

import numpy as np
from novaengine import NovaBaseGame, Camera, Level, RenderableUserDisplay, Sprite


BACKGROUND_COLOR = 4
PADDING_COLOR = 4
PANEL_COLOR = 1
FLOOR_COLOR = 1
WALL_COLOR = 5
NORTH_COLOR = 8
SOUTH_COLOR = 9
CORE_COLOR = 5
PULSE_COLOR = 14
STEP_COLOR = 14
STEP_EMPTY = 4
ACTIVE_BORDER = 1
BUTTON_BORDER = 5

CELL = 4
GRID_CELLS = 16
GRID_W = GRID_CELLS * CELL
GRID_H = GRID_CELLS * CELL

CHAMBER_X0 = 3
CHAMBER_X1 = 12
CHAMBER_Y0 = 1
CHAMBER_Y1 = 10
MAGNET_CELL = (8, 5)

POLARITY_ORDER = ["N", "S"]
POLE_BUTTONS = {
    "N": (1, 12),
    "S": (5, 12),
}
PULSE_BUTTON = (12, 12)
BUTTON_SIZE = 2

CROSS_FLOOR_CELLS = {
    (x, 5) for x in range(4, 13)
} | {
    (8, y) for y in range(2, 9)
}
CROSS_FLOOR_CELLS.discard(MAGNET_CELL)


def _cell(cx: int, cy: int) -> tuple[int, int]:
    return (cx * CELL, cy * CELL)


def _panel_pixels() -> list[list[int]]:
    return [[PANEL_COLOR] * 4 for _ in range(4)]


def _floor_pixels() -> list[list[int]]:
    return [[FLOOR_COLOR] * 4 for _ in range(4)]


def _wall_pixels() -> list[list[int]]:
    return [[WALL_COLOR] * 4 for _ in range(4)]


def _piece_pixels(polarity: str) -> list[list[int]]:
    color = NORTH_COLOR if polarity == "N" else SOUTH_COLOR
    return [
        [-1, color, color, -1],
        [color, CORE_COLOR, CORE_COLOR, color],
        [color, CORE_COLOR, CORE_COLOR, color],
        [-1, color, color, -1],
    ]


def _target_pixels(polarity: str) -> list[list[int]]:
    color = NORTH_COLOR if polarity == "N" else SOUTH_COLOR
    return [
        [color, color, color, color],
        [color, -1, -1, color],
        [color, -1, -1, color],
        [color, color, color, color],
    ]


def _magnet_pixels(polarity: str) -> list[list[int]]:
    active = NORTH_COLOR if polarity == "N" else SOUTH_COLOR
    other = SOUTH_COLOR if polarity == "N" else NORTH_COLOR
    return [
        [other, other, active, active],
        [other, CORE_COLOR, CORE_COLOR, active],
        [other, CORE_COLOR, CORE_COLOR, active],
        [other, other, active, active],
    ]


def _button_canvas(fill: int, border: int) -> np.ndarray:
    pixels = np.full((8, 8), fill, dtype=np.int16)
    pixels[0, :] = border
    pixels[7, :] = border
    pixels[:, 0] = border
    pixels[:, 7] = border
    return pixels


def _pole_button_pixels(polarity: str, *, active: bool) -> list[list[int]]:
    fill = NORTH_COLOR if polarity == "N" else SOUTH_COLOR
    border = ACTIVE_BORDER if active else BUTTON_BORDER
    pixels = _button_canvas(fill, border)
    pixels[2:6, 3:5] = CORE_COLOR
    pixels[3:5, 2:6] = CORE_COLOR
    return pixels.tolist()


def _pulse_button_pixels() -> list[list[int]]:
    pixels = _button_canvas(PULSE_COLOR, BUTTON_BORDER)
    pixels[3:5, 3:5] = CORE_COLOR
    return pixels.tolist()


sprites = {
    "panel": Sprite(
        pixels=_panel_pixels(),
        name="panel",
        visible=True,
        collidable=False,
        tags=["panel"],
        layer=1,
    ),
    "floor": Sprite(
        pixels=_floor_pixels(),
        name="floor",
        visible=True,
        collidable=False,
        tags=["floor"],
        layer=1,
    ),
    "wall": Sprite(
        pixels=_wall_pixels(),
        name="wall",
        visible=True,
        collidable=False,
        tags=["wall"],
        layer=2,
    ),
    "target_N": Sprite(
        pixels=_target_pixels("N"),
        name="target_N",
        visible=True,
        collidable=False,
        tags=["target_N"],
        layer=2,
    ),
    "target_S": Sprite(
        pixels=_target_pixels("S"),
        name="target_S",
        visible=True,
        collidable=False,
        tags=["target_S"],
        layer=2,
    ),
    "piece_N": Sprite(
        pixels=_piece_pixels("N"),
        name="piece_N",
        visible=True,
        collidable=False,
        tags=["piece_N"],
        layer=5,
    ),
    "piece_S": Sprite(
        pixels=_piece_pixels("S"),
        name="piece_S",
        visible=True,
        collidable=False,
        tags=["piece_S"],
        layer=5,
    ),
    "magnet": Sprite(
        pixels=_magnet_pixels("N"),
        name="magnet",
        visible=True,
        collidable=False,
        tags=["magnet"],
        layer=4,
    ),
    "button_N": Sprite(
        pixels=_pole_button_pixels("N", active=True),
        name="button_N",
        visible=True,
        collidable=False,
        tags=["button_N"],
        layer=4,
    ),
    "button_S": Sprite(
        pixels=_pole_button_pixels("S", active=False),
        name="button_S",
        visible=True,
        collidable=False,
        tags=["button_S"],
        layer=4,
    ),
    "pulse_button": Sprite(
        pixels=_pulse_button_pixels(),
        name="pulse_button",
        visible=True,
        collidable=False,
        tags=["pulse_button"],
        layer=4,
    ),
}


def _clone(name: str, cx: int, cy: int) -> Sprite:
    return sprites[name].clone().set_position(*_cell(cx, cy))


def _build_level(
    *,
    pieces: list[dict[str, object]],
    targets: list[dict[str, object]],
    pulse_budget: int,
    initial_pole: str = "N",
) -> Level:
    placed: list[Sprite] = []

    for cy in range(12, 16):
        for cx in range(0, GRID_CELLS):
            placed.append(_clone("panel", cx, cy))

    for cy in range(CHAMBER_Y0, CHAMBER_Y1 + 1):
        for cx in range(CHAMBER_X0, CHAMBER_X1 + 1):
            if (cx, cy) in CROSS_FLOOR_CELLS or (cx, cy) == MAGNET_CELL:
                placed.append(_clone("floor", cx, cy))
            else:
                placed.append(_clone("wall", cx, cy))

    for target in targets:
        polarity = str(target["polarity"])
        tx, ty = tuple(target["cell"])
        placed.append(_clone(f"target_{polarity}", tx, ty))

    placed.append(_clone("magnet", *MAGNET_CELL))

    for piece in pieces:
        polarity = str(piece["polarity"])
        px, py = tuple(piece["cell"])
        placed.append(_clone(f"piece_{polarity}", px, py))

    placed.append(_clone("button_N", *POLE_BUTTONS["N"]))
    placed.append(_clone("button_S", *POLE_BUTTONS["S"]))
    placed.append(_clone("pulse_button", *PULSE_BUTTON))

    return Level(
        sprites=placed,
        grid_size=(GRID_W, GRID_H),
        data={
            "pieces": pieces,
            "targets": targets,
            "pulse_budget": pulse_budget,
            "initial_pole": initial_pole,
        },
    )


levels = [
    _build_level(
        pieces=[
            {"cell": [5, 5], "polarity": "N"},
        ],
        targets=[
            {"cell": [4, 5], "polarity": "N"},
        ],
        pulse_budget=1,
        initial_pole="N",
    ),
    _build_level(
        pieces=[
            {"cell": [6, 5], "polarity": "N"},
            {"cell": [12, 5], "polarity": "S"},
        ],
        targets=[
            {"cell": [4, 5], "polarity": "N"},
            {"cell": [10, 5], "polarity": "S"},
        ],
        pulse_budget=2,
        initial_pole="N",
    ),
    _build_level(
        pieces=[
            {"cell": [4, 5], "polarity": "N"},
            {"cell": [5, 5], "polarity": "S"},
            {"cell": [8, 2], "polarity": "S"},
        ],
        targets=[
            {"cell": [6, 5], "polarity": "N"},
            {"cell": [7, 5], "polarity": "S"},
            {"cell": [8, 4], "polarity": "S"},
        ],
        pulse_budget=4,
        initial_pole="N",
    ),
]


class PulseHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self.pulses_remaining = 0
        self.max_pulses = 1

    def set_state(self, *, pulses_remaining: int, max_pulses: int) -> None:
        self.pulses_remaining = max(0, pulses_remaining)
        self.max_pulses = max(1, max_pulses)

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        filled = int(round((self.pulses_remaining / self.max_pulses) * 6))
        for idx in range(6):
            x0, y0 = _cell(idx + 1, 0)
            color = STEP_COLOR if idx < filled else STEP_EMPTY
            frame[y0 + 1 : y0 + 3, x0 + 1 : x0 + 3] = color
        return frame


class Mr8k(NovaBaseGame):
    def __init__(self) -> None:
        self._hud = PulseHud()
        self._anim_queue: list[list[tuple[int, int]]] = []
        self._pending_pulse_success = False
        camera = Camera(
            width=GRID_W,
            height=GRID_H,
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self._hud],
        )
        super().__init__(
            game_id="mr8k",
            levels=levels,
            camera=camera,
            available_actions=[6],
        )

    def on_set_level(self, level: Level) -> None:
        raw_pieces = level.get_data("pieces") or []
        raw_targets = level.get_data("targets") or []
        self.pulse_budget = int(level.get_data("pulse_budget") or 1)
        self.pulses_used = 0
        self.pole = str(level.get_data("initial_pole") or "N")
        self._pending_pulse_success = False
        self._anim_queue = []

        self.piece_defs = [
            {
                "start": tuple(piece["cell"]),
                "polarity": str(piece["polarity"]),
            }
            for piece in raw_pieces
        ]
        self.target_defs = [
            {
                "cell": tuple(target["cell"]),
                "polarity": str(target["polarity"]),
            }
            for target in raw_targets
        ]
        self.targets_by_cell = {
            target["cell"]: target["polarity"] for target in self.target_defs
        }

        self.magnet_sprite = next(s for s in level.get_sprites() if s.name == "magnet")
        self.n_button_sprite = next(s for s in level.get_sprites() if s.name == "button_N")
        self.s_button_sprite = next(s for s in level.get_sprites() if s.name == "button_S")
        self.pulse_button_sprite = next(s for s in level.get_sprites() if s.name == "pulse_button")
        self.piece_sprites = [
            sprite for sprite in level.get_sprites() if sprite.name in {"piece_N", "piece_S"}
        ]

        self._reset_state()
        self._sync_controls()
        self._refresh_hud()

    def _reset_state(self) -> None:
        self.pieces = []
        for definition, sprite in zip(self.piece_defs, self.piece_sprites):
            cell = tuple(definition["start"])
            polarity = str(definition["polarity"])
            locked = self.targets_by_cell.get(cell) == polarity
            sprite.pixels = np.array(_piece_pixels(polarity), dtype=np.int16)
            sprite.set_position(*_cell(*cell))
            self.pieces.append(
                {
                    "cell": cell,
                    "polarity": polarity,
                    "locked": locked,
                    "sprite": sprite,
                }
            )

    def _refresh_hud(self) -> None:
        self._hud.set_state(
            pulses_remaining=self.pulse_budget - self.pulses_used,
            max_pulses=self.pulse_budget,
        )

    def _sync_controls(self) -> None:
        self.magnet_sprite.pixels = np.array(_magnet_pixels(self.pole), dtype=np.int16)
        self.n_button_sprite.pixels = np.array(
            _pole_button_pixels("N", active=self.pole == "N"),
            dtype=np.int16,
        )
        self.s_button_sprite.pixels = np.array(
            _pole_button_pixels("S", active=self.pole == "S"),
            dtype=np.int16,
        )

    def _click_cell(self) -> tuple[int, int] | None:
        click_x = int(self.action.data.get("x", -1000))
        click_y = int(self.action.data.get("y", -1000))
        grid = self.camera.display_to_grid(click_x, click_y)
        if grid is None:
            return None
        return (grid[0] // CELL, grid[1] // CELL)

    def _hit_box(self, clicked: tuple[int, int], origin: tuple[int, int]) -> bool:
        return (
            origin[0] <= clicked[0] < origin[0] + BUTTON_SIZE
            and origin[1] <= clicked[1] < origin[1] + BUTTON_SIZE
        )

    def _move_priority(self, piece: dict[str, object]) -> int:
        x, y = tuple(piece["cell"])
        toward = str(piece["polarity"]) != self.pole
        dist = abs(x - MAGNET_CELL[0]) + abs(y - MAGNET_CELL[1])
        return dist if toward else -dist

    def _next_cell(self, piece: dict[str, object]) -> tuple[int, int]:
        x, y = tuple(piece["cell"])
        mx, my = MAGNET_CELL
        toward = str(piece["polarity"]) != self.pole
        if x == mx:
            dy = 1 if y < my else -1
            if not toward:
                dy *= -1
            return (x, y + dy)
        dx = 1 if x < mx else -1
        if not toward:
            dx *= -1
        return (x + dx, y)

    def _pulse(self) -> bool:
        self._anim_queue = []
        occupied = {tuple(piece["cell"]) for piece in self.pieces}
        for piece in sorted(self.pieces, key=self._move_priority):
            if bool(piece["locked"]):
                continue
            next_cell = self._next_cell(piece)
            if next_cell == MAGNET_CELL or next_cell not in CROSS_FLOOR_CELLS:
                continue
            current_cell = tuple(piece["cell"])
            occupied.remove(current_cell)
            if next_cell in occupied:
                occupied.add(current_cell)
                continue
            piece["cell"] = next_cell
            occupied.add(next_cell)
            if self.targets_by_cell.get(next_cell) == piece["polarity"]:
                piece["locked"] = True

        self._anim_queue.append([tuple(piece["cell"]) for piece in self.pieces])
        return all(bool(piece["locked"]) for piece in self.pieces)

    def _advance_anim_frame(self) -> None:
        positions = self._anim_queue.pop(0)
        for piece, cell in zip(self.pieces, positions):
            piece["sprite"].set_position(*_cell(*cell))

    def _resolve_after_pulse(self) -> None:
        self._refresh_hud()
        if self._pending_pulse_success:
            self.next_level()
            self.complete_action()
            return
        if self.pulses_used >= self.pulse_budget:
            self.lose()
            self.complete_action()
            return
        self.complete_action()

    def step(self) -> None:
        if self._anim_queue:
            self._advance_anim_frame()
            if self._anim_queue:
                return
            self._resolve_after_pulse()
            return

        clicked = self._click_cell()
        if clicked is None:
            self.complete_action()
            return

        if self._hit_box(clicked, POLE_BUTTONS["N"]):
            self.pole = "N"
            self._sync_controls()
            self.complete_action()
            return
        if self._hit_box(clicked, POLE_BUTTONS["S"]):
            self.pole = "S"
            self._sync_controls()
            self.complete_action()
            return

        if self._hit_box(clicked, PULSE_BUTTON):
            success = self._pulse()
            self.pulses_used += 1
            self._pending_pulse_success = success
            self._refresh_hud()
            if self._anim_queue:
                self._advance_anim_frame()
                if self._anim_queue:
                    return
                self._resolve_after_pulse()
                return
            if success:
                self.next_level()
            elif self.pulses_used >= self.pulse_budget:
                self.lose()
            self.complete_action()
            return

        self.complete_action()

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def _get_valid_actions(self):
        return super()._get_valid_actions()
