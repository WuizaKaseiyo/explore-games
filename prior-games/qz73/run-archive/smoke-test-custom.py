"""Custom smoke checks for qz73 — radial-cycle-lock mechanic.

Each function returns (passed: bool, observed: str).
Imports are inside main() so this file is also runnable standalone.
"""

from novaengine import ActionInput, GameAction


def check_action5_rotates_unlocked_tip(GameClass):
    """ACTION5 advances every unlocked tip's slot index by +1 mod 8."""
    g = GameClass()
    g.set_level(0)
    tip = g.tips[0]
    s0 = g.tip_slot[tip]
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    s1 = g.tip_slot[tip]
    expected = (s0 + 1) % 8
    return s1 == expected, f"slot before={s0} after={s1} expected={expected}"


def check_action6_toggles_lock(GameClass):
    """ACTION6 click on a tip's centre toggles its lock flag."""
    from qz73 import SLOT_CENTERS

    g = GameClass()
    g.set_level(0)
    tip = g.tips[0]
    cx, cy = SLOT_CENTERS[g.tip_slot[tip]]
    locked0 = g.tip_locked[tip]
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": cx, "y": cy}),
        raw=True,
    )
    locked1 = g.tip_locked[tip]
    return locked1 != locked0, f"locked before={locked0} after={locked1}"


def check_locked_tip_does_not_rotate(GameClass):
    """A locked tip stays in its slot when ACTION5 is fired."""
    from qz73 import SLOT_CENTERS

    g = GameClass()
    g.set_level(0)
    tip = g.tips[0]
    cx, cy = SLOT_CENTERS[g.tip_slot[tip]]
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": cx, "y": cy}),
        raw=True,
    )
    s_before = g.tip_slot[tip]
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    s_after = g.tip_slot[tip]
    return s_after == s_before, f"locked-slot before={s_before} after={s_after}"


def check_l1_minimal_solve(GameClass):
    """Two ACTION5 presses solve level 1 (advance to level 2)."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    return g._current_level_index == 1, (
        f"level idx after 2xACTION5 = {g._current_level_index}"
    )


CHECKS = [
    check_action5_rotates_unlocked_tip,
    check_action6_toggles_lock,
    check_locked_tip_does_not_rotate,
    check_l1_minimal_solve,
]


def main():
    import importlib.util
    from pathlib import Path

    src = Path(
        "prior-games/qz73/qz73.py"
    )
    spec = importlib.util.spec_from_file_location("smoke_qz73", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    GameClass = mod.Qz73
    print("CUSTOM CHECKS:")
    for fn in CHECKS:
        ok, observed = fn(GameClass)
        marker = "PASS" if ok else "FAIL"
        print(f"  [{marker}] {fn.__name__}: {observed}")


if __name__ == "__main__":
    main()
