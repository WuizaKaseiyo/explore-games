"""Custom smoke-test checks for jd4q."""

import importlib.util
from pathlib import Path

src = Path("prior-games/jd4q/jd4q.py")
spec = importlib.util.spec_from_file_location("smoke_jd4q_custom", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = mod.Jd4q

from novaengine import ActionInput, GameAction


def check_action4_moves_avatar_east() -> tuple[bool, str]:
    """ACTION4 moves the avatar one cell east (4 pixels) when the cell east is floor."""
    g = GameClass()
    g.set_level(0)  # L1: avatar at (8, 8) pixel; corridor is row 2, cells (2..13)
    x0 = g.avatar.x
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    return g.avatar.x == x0 + 4, f"x0={x0} x1={g.avatar.x}"


def check_action_counter_increments() -> tuple[bool, str]:
    """Each non-RESET action advances the engine's _action_count by 1."""
    g = GameClass()
    g.set_level(0)
    n0 = g._action_count
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    return g._action_count == n0 + 1, f"before={n0} after={g._action_count}"


def check_l2_echo_deposits_on_walk() -> tuple[bool, str]:
    """At L2 (echoes_active=True), one ACTION2 from S deposits exactly one echo."""
    g = GameClass()
    g.set_level(1)  # L2
    n0 = len(g.echoes)
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)
    return len(g.echoes) == n0 + 1, f"before={n0} after={len(g.echoes)}"


def check_l1_no_echoes_deposited() -> tuple[bool, str]:
    """At L1 (echoes_active=False), one walk does NOT deposit an echo."""
    g = GameClass()
    g.set_level(0)  # L1
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    return len(g.echoes) == 0, f"after one walk: echoes={len(g.echoes)}"


CHECKS = [
    check_action4_moves_avatar_east,
    check_action_counter_increments,
    check_l2_echo_deposits_on_walk,
    check_l1_no_echoes_deposited,
]


if __name__ == "__main__":
    failures = []
    for fn in CHECKS:
        passed, observed = fn()
        marker = "PASS" if passed else "FAIL"
        print(f"{marker}: {fn.__name__} — {observed}")
        if not passed:
            failures.append((fn.__name__, fn.__doc__, observed))
    print(f"\nfailures: {len(failures)}")
    for name, doc, obs in failures:
        print(f"  {name}: {doc} — observed: {obs}")
