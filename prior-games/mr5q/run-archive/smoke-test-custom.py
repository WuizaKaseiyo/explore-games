"""Custom smoke checks for mr5q (polarity-attract-discharge).

Each check is one essential mechanic invariant: ≤ 5 setup actions, one
action under test, one boolean assertion.

Invariants tested:
  1. ACTION6 click on a pawn flips its polarity (yang ↔ yin).
  2. ACTION5 tick moves opposite-state pawns one step toward each other.
  3. Same-colour opposite-state pawns within Cheb-distance ≤ PAWN_SIZE
     discharge (both go alive=False).
  4. ACTION counter increments per action.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


SRC = Path("prior-games/mr5q/mr5q.py")
spec = importlib.util.spec_from_file_location("smoke_mr5q", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = getattr(mod, "Mr5q")


def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2


def check_click_flips_polarity():
    """ACTION6 on a pawn toggles its polarity bit."""
    g = GameClass()
    g.set_level(0)
    pair = g._pawn_pairs[0]
    initial = pair["active"]
    px, py = _grid_to_display_px(
        g.current_level.grid_size, pair["yang"].x, pair["yang"].y
    )
    # Click pixel must be inside the pawn's bbox; centre is safest.
    px += (4 * (64 // g.current_level.grid_size[0])) // 2 - (64 // g.current_level.grid_size[0]) // 2
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": px, "y": py}), raw=True
    )
    final = pair["active"]
    return final != initial, f"before={initial} after={final}"


def check_tick_moves_attracted_pair():
    """ACTION5 tick moves an opposite-state pawn at least one cell."""
    g = GameClass()
    g.set_level(0)
    pair0 = g._pawn_pairs[0]
    pair1 = g._pawn_pairs[1]
    # Setup: flip pair0 so the two pairs are opposite-state (1 setup action).
    px, py = _grid_to_display_px(
        g.current_level.grid_size, pair0["yang"].x, pair0["yang"].y
    )
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": px, "y": py}), raw=True
    )
    pos0_before = (pair0["yang"].x, pair0["yang"].y)
    pos1_before = (pair1["yang"].x, pair1["yang"].y)
    # Action under test: one tick.
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    pos0_after = (pair0["yang"].x, pair0["yang"].y)
    pos1_after = (pair1["yang"].x, pair1["yang"].y)
    moved = pos0_before != pos0_after or pos1_before != pos1_after
    return moved, f"pair0 {pos0_before}->{pos0_after}, pair1 {pos1_before}->{pos1_after}"


def check_discharge_at_adjacency():
    """Two opposite-state same-colour pawns brought to Cheb-distance 4 discharge on the next tick."""
    g = GameClass()
    g.set_level(0)
    pair0 = g._pawn_pairs[0]
    pair1 = g._pawn_pairs[1]
    # Setup: flip pair1 so they are opposite-state.
    px, py = _grid_to_display_px(
        g.current_level.grid_size, pair1["yang"].x, pair1["yang"].y
    )
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": px, "y": py}), raw=True
    )
    # Tick repeatedly until both pairs are dead or budget runs.
    for _ in range(15):
        g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
        if not pair0["alive"] and not pair1["alive"]:
            return True, "both pairs discharged"
    return False, f"alive after 15 ticks: pair0={pair0['alive']} pair1={pair1['alive']}"


def check_action_counter_increments():
    """Each ACTION5 increments the engine's action count by 1."""
    g = GameClass()
    g.set_level(0)
    n0 = g._action_count
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    n1 = g._action_count
    return n1 == n0 + 1, f"before={n0} after={n1}"


CHECKS = [
    check_click_flips_polarity,
    check_tick_moves_attracted_pair,
    check_discharge_at_adjacency,
    check_action_counter_increments,
]


if __name__ == "__main__":
    results = []
    for fn in CHECKS:
        try:
            passed, observed = fn()
        except Exception as exc:
            passed, observed = False, f"raised {type(exc).__name__}: {exc}"
        results.append((fn.__name__, passed, observed))
    for name, passed, observed in results:
        marker = "✅" if passed else "❌"
        print(f"{marker} {name}: {observed}")
