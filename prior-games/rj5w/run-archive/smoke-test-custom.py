"""Custom smoke checks for rj5w. Each returns (bool, str)."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


_SRC = Path(
    "prior-games/rj5w/rj5w.py"
).resolve()
_spec = importlib.util.spec_from_file_location("smoke_rj5w", _SRC)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
GameClass = _mod.Rj5w


def _act(n: int) -> ActionInput:
    return ActionInput(id=GameAction.from_id(n), data={})


def _click(x: int, y: int) -> ActionInput:
    return ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y})


def check_v_fold_reflects_pawn() -> tuple[bool, str]:
    """ACTION5 (V-fold) box-reflects an unlocked 5x5 pawn through F_v
    (anchor x → 2*F_v - x - 4, since the sprite footprint mirrors as a whole)."""
    g = GameClass()
    g.set_level(0)
    pawn = g.current_level.get_sprites_by_tag("pawn_green")[0]
    fv0 = g.fv
    x0 = pawn.x
    g.perform_action(_act(5))
    expected_x = 2 * fv0 - x0 - 4
    return (
        pawn.x == expected_x,
        f"fv={fv0} x0={x0} expected={expected_x} got={pawn.x}",
    )


def check_axis_toggle_via_click() -> tuple[bool, str]:
    """Clicking a cell on the H-line cursor (gy == fh) makes H the active axis."""
    g = GameClass()
    g.set_level(1)
    before = g.active_axis
    fh = g.fh
    g.perform_action(_click(20, fh))
    return (
        g.active_axis == "H" and before == "V",
        f"before={before} after={g.active_axis} fh={fh}",
    )


def check_lock_freezes_pawn() -> tuple[bool, str]:
    """A pawn locked on its target stays put on the next V-fold."""
    g = GameClass()
    g.set_level(2)
    # L3 initial F_v=28; bring F_v to 32 so the V-fold lands green on its target.
    for _ in range(4):
        g.perform_action(_act(4))
    g.perform_action(_act(5))  # V-fold #1: green should lock on target.
    green = g.current_level.get_sprites_by_tag("pawn_green")[0]
    pos_after_fold1 = (green.x, green.y)
    g.perform_action(_act(5))  # V-fold #2: locked green should NOT move.
    return (
        (green.x, green.y) == pos_after_fold1,
        f"after_fold1={pos_after_fold1} after_fold2=({green.x}, {green.y})",
    )


def check_lose_at_budget() -> tuple[bool, str]:
    """The step budget firing zero triggers GameState.GAME_OVER."""
    g = GameClass()
    g.set_level(0)
    budget = g.step_budget
    # Fire ACTION3 budget times; each decrements step_budget by 1.
    for _ in range(budget):
        g.perform_action(_act(3))
    return (
        g._state.name == "GAME_OVER",
        f"budget0={budget} state={g._state.name}",
    )


CHECKS = [
    check_v_fold_reflects_pawn,
    check_axis_toggle_via_click,
    check_lock_freezes_pawn,
    check_lose_at_budget,
]
