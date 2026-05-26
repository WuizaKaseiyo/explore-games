"""Custom smoke checks for cv5b.

Run by the smoke_test state. Each function returns (passed, observed)
for inline reporting. Each check follows the template:
- ≤ 5 setup actions, 1 action under test, 1 boolean assertion.
"""

import importlib.util
import sys
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load_game():
    src = Path("prior-games/cv5b/cv5b.py")
    spec = importlib.util.spec_from_file_location("smoke_cv5b", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, mod.Cv5b


def check_action4_walks_right(GameClass) -> tuple[bool, str]:
    """ACTION4 moves the active launcher one cell right."""
    g = GameClass()
    g.handle_reset()
    x0, y0 = g._launcher_origin()
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    x1, y1 = g._launcher_origin()
    return (x1 == x0 + 1 and y1 == y0), f"origin {x0,y0} -> {x1,y1}"


def check_action5_cycles_power(GameClass) -> tuple[bool, str]:
    """ACTION5 cycles power 1 -> 2."""
    g = GameClass()
    g.handle_reset()
    p0 = g.power
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    p1 = g.power
    return (p0 == 1 and p1 == 2), f"before={p0} after={p1}"


def check_l1_minimal_solve(GameClass) -> tuple[bool, str]:
    """ACTION6@(16, 50) at L1 default power lands on the target and advances level."""
    g = GameClass()
    g.handle_reset()
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 16, "y": 50}), raw=True
    )
    return (g._current_level_index == 1), f"level after solve={g._current_level_index}"


def check_lose_at_budget(GameClass) -> tuple[bool, str]:
    """Repeated ACTION5 until L1 budget exhausts triggers lose."""
    g = GameClass()
    g.handle_reset()
    budget = g._step_counter_ui.max_steps
    # Take budget+1 ACTION5 calls (cycling power, doesn't advance level)
    for _ in range(budget + 1):
        g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    return (g._state.name == "GAME_OVER"), f"state after budget+1={g._state.name}"


CHECKS = [
    check_action4_walks_right,
    check_action5_cycles_power,
    check_l1_minimal_solve,
    check_lose_at_budget,
]


if __name__ == "__main__":
    sys.path.insert(0, "prior-games/cv5b")
    _, GameClass = _load_game()
    failures = []
    for fn in CHECKS:
        passed, obs = fn(GameClass)
        marker = "PASS" if passed else "FAIL"
        print(f"{marker} {fn.__name__}: {obs}")
        if not passed:
            failures.append(fn.__name__)
    sys.exit(1 if failures else 0)
