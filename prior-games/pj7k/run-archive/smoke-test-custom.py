"""Custom smoke checks for pj7k — exercise mechanic invariants.

Each function returns (passed: bool, observed: str).
"""
import importlib.util
from pathlib import Path

import numpy as np
from novaengine import ActionInput, GameAction


def _load_game_class():
    src = Path("prior-games/pj7k/pj7k.py")
    spec = importlib.util.spec_from_file_location("smoke_pj7k", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Pj7K, mod


def _act(g, aid):
    g.perform_action(ActionInput(id=GameAction.from_id(aid)), raw=True)


def check_east_paints_right_face_on_bottom(GameClass) -> tuple[bool, str]:
    """L1 east-roll deposits initial right-face colour on the cell entered."""
    g = GameClass()
    g.set_level(0)
    # Cube starts at logical (0, 1) with right=12 (orange).
    _act(g, 4)  # east → (1, 1)
    # paint at (1, 1) should be 12 (orange)
    paint = g._paint_at_cell(1, 1)
    if paint is None:
        return False, "no paint at (1,1) after east"
    colour = g._paint_colour(paint)
    return colour == 12, f"paint at (1,1) = {colour}; expected 12"


def check_twist_does_not_move(GameClass) -> tuple[bool, str]:
    """ACTION5 must not change cube position."""
    g = GameClass()
    g.set_level(0)
    cube = g._cube_sprite()
    x0, y0 = cube.x, cube.y
    _act(g, 5)  # twist
    return (cube.x, cube.y) == (x0, y0), f"before=({x0},{y0}) after=({cube.x},{cube.y})"


def check_lock_blocks_wrong_face(GameClass) -> tuple[bool, str]:
    """L3 lock at (1, 0) requires green; rolling east without a prior twist
    should be REJECTED (cube stays at (0, 0))."""
    g = GameClass()
    g.set_level(2)
    cube = g._cube_sprite()
    x0, y0 = cube.x, cube.y
    _act(g, 4)  # east, but bottom-after-roll = orange (12), not green (14)
    return (cube.x, cube.y) == (x0, y0), (
        f"cube moved from ({x0},{y0}) to ({cube.x},{cube.y}); lock should reject"
    )


def check_l1_minimal_solve(GameClass) -> tuple[bool, str]:
    """Spec L1 witness [E, E] must complete level 1."""
    g = GameClass()
    g.set_level(0)
    _act(g, 4)
    _act(g, 4)
    return g._current_level_index == 1, f"level after solve={g._current_level_index}"


CUSTOM_CHECKS = [
    check_east_paints_right_face_on_bottom,
    check_twist_does_not_move,
    check_lock_blocks_wrong_face,
    check_l1_minimal_solve,
]


if __name__ == "__main__":
    GameClass, _mod = _load_game_class()
    rows = []
    for fn in CUSTOM_CHECKS:
        passed, observed = fn(GameClass)
        rows.append((fn.__name__, passed, observed))
        marker = "PASS" if passed else "FAIL"
        print(f"{marker} {fn.__name__}: {observed}")
