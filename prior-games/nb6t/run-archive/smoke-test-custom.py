"""Custom smoke checks for nb6t."""

import importlib.util
from pathlib import Path
from novaengine import ActionInput, GameAction


def _load_class():
    src = Path("prior-games/nb6t/nb6t.py")
    spec = importlib.util.spec_from_file_location("smoke_nb6t_custom", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "Nb6t")


def check_action5_cycles_active_hinge(GameClass) -> tuple[bool, str]:
    """ACTION5 cycles _active_hinge by +1 mod N_segments."""
    g = GameClass()
    g.set_level(0)
    a0 = g._active_hinge
    g.perform_action(ActionInput(id=GameAction.ACTION5))
    passed = g._active_hinge == (a0 + 1) % 3
    return passed, f"before={a0} after={g._active_hinge}"


def check_action3_rotates_active_ccw(GameClass) -> tuple[bool, str]:
    """ACTION3 rotates the active segment's theta by +90."""
    g = GameClass()
    g.set_level(0)
    theta0 = g._pose[g._active_hinge][0]
    g.perform_action(ActionInput(id=GameAction.ACTION3))
    theta1 = g._pose[g._active_hinge][0]
    passed = theta1 == (theta0 + 90) % 360
    return passed, f"theta {theta0} -> {theta1}"


def check_action2_retracts_active_length(GameClass) -> tuple[bool, str]:
    """At L2, ACTION2 reduces the active segment's length by 1."""
    g = GameClass()
    g.set_level(1)
    L0 = g._pose[g._active_hinge][1]
    g.perform_action(ActionInput(id=GameAction.ACTION2))
    L1 = g._pose[g._active_hinge][1]
    passed = L1 == L0 - 1
    return passed, f"length {L0} -> {L1}"


def check_click_on_hinge_sets_active(GameClass) -> tuple[bool, str]:
    """ACTION6 click on a hinge cell sets _active_hinge to that hinge's index.

    Hinge 2 is at grid cell (40, 32) in the initial L1 pose.
    """
    g = GameClass()
    g.set_level(0)
    # In initial pose (E12, E12, E12) from base (16, 32):
    # hinge_0 = (16, 32), hinge_1 = (28, 32), hinge_2 = (40, 32).
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 40, "y": 32}))
    passed = g._active_hinge == 2
    return passed, f"active_hinge={g._active_hinge}"


CHECKS = [
    check_action5_cycles_active_hinge,
    check_action3_rotates_active_ccw,
    check_action2_retracts_active_length,
    check_click_on_hinge_sets_active,
]


if __name__ == "__main__":
    GameClass = _load_class()
    for check in CHECKS:
        try:
            passed, observed = check(GameClass)
            status = "PASS" if passed else "FAIL"
            print(f"{status}: {check.__name__} — {observed}")
        except Exception as e:
            print(f"FAIL: {check.__name__} — exception {type(e).__name__}: {e}")
