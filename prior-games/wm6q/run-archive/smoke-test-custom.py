"""Custom smoke checks for wm6q. Each is a single function returning
`(bool, str)` per the strict template in skills/code/smoke-test-checks.md."""

import importlib.util
from pathlib import Path

SRC = Path("/Users/nickhe/Programming/NovaPlay-Agents/prior-games/wm6q/wm6q.py")

_spec = importlib.util.spec_from_file_location("smoke_wm6q_custom", SRC)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
GameClass = _mod.Wm6q

from novaengine import ActionInput, GameAction


def _click(x, y):
    return ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y})


def check_click_rotates_regular_tile():
    """Clicking a regular tile advances its rotation by exactly 1 (mod 4)."""
    g = GameClass()
    g.set_level(0)  # L1: two regular tiles, no special tiles
    name = "l1_b"
    r0 = g._tile_rotations[name]
    g.perform_action(_click(40, 32), raw=True)  # tile B centre
    r1 = g._tile_rotations[name]
    return r1 == (r0 + 1) % 4, f"r0={r0} r1={r1}"


def check_click_on_locked_is_noop():
    """Clicking a locked tile does NOT change its rotation and does NOT
    consume a step from the counter."""
    g = GameClass()
    g.set_level(1)  # L2: locked tile at (16, 8) → click at (24, 16) hits it
    locked_name = "l2_00"
    r0 = g._tile_rotations[locked_name]
    used0 = g._steps_used
    g.perform_action(_click(24, 16), raw=True)  # locked tile centre
    r1 = g._tile_rotations[locked_name]
    used1 = g._steps_used
    # Single boolean: the locked tile's rotation did not change.
    return r1 == r0, f"locked rot {r0}→{r1}, steps_used {used0}→{used1}"


def check_click_on_linked_rotates_both():
    """Clicking either linked-pair member advances BOTH members' rotations
    by 1."""
    g = GameClass()
    g.set_level(2)  # L3: linked pair at "l3_00" and "l3_22"
    a, b = "l3_00", "l3_22"
    r_a0 = g._tile_rotations[a]
    r_b0 = g._tile_rotations[b]
    g.perform_action(_click(16, 16), raw=True)  # tile (0,0) centre
    r_a1 = g._tile_rotations[a]
    r_b1 = g._tile_rotations[b]
    # Single boolean: both rotations advanced by 1.
    advanced_both = (r_a1 == (r_a0 + 1) % 4) and (r_b1 == (r_b0 + 1) % 4)
    return advanced_both, f"({r_a0}→{r_a1}, {r_b0}→{r_b1})"


def check_lose_at_budget():
    """Spamming clicks past the step budget on L3 triggers `lose()`. L3
    requires specific rotations across 8 tiles; rotating only one regular
    tile can never satisfy the win predicate, so the budget will exhaust."""
    g = GameClass()
    g.set_level(2)  # L3, budget 50
    budget = g.current_level.get_data("step_budget")
    # Click only on tile (1, 0). Rotating one tile can't satisfy the 12
    # internal-boundary win predicate on its own.
    for _ in range(budget + 1):
        g.perform_action(_click(32, 16), raw=True)  # tile (1, 0) centre
    return g._state.name == "GAME_OVER", f"final state={g._state.name}, steps_used would be {budget}"


CHECKS = [
    check_click_rotates_regular_tile,
    check_click_on_locked_is_noop,
    check_click_on_linked_rotates_both,
    check_lose_at_budget,
]


if __name__ == "__main__":
    for fn in CHECKS:
        try:
            ok, observed = fn()
        except Exception as e:
            ok, observed = False, f"EXCEPTION: {type(e).__name__}: {e}"
        verdict = "PASS" if ok else "FAIL"
        print(f"  {fn.__name__}: {verdict}  ({observed})")
