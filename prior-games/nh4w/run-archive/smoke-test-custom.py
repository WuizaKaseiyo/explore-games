"""Custom smoke checks for nh4w (Arc-Loft Lobber).

Each check follows the strict template in
`skills/code/smoke-test-checks.md`:
≤ 5 setup actions, ONE action under test, ONE boolean assertion.
"""

import importlib.util
from pathlib import Path
from novaengine import ActionInput, GameAction


def _load_game_class():
    src = Path("prior-games/nh4w/nh4w.py")
    spec = importlib.util.spec_from_file_location("smoke_nh4w_custom", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "Nh4w")


def check_action4_moves_launcher_right(GameClass) -> tuple[bool, str]:
    """ACTION4 moves the launcher pawn 4 pixels right (one walking step)."""
    g = GameClass()
    g.set_level(0)
    x0 = g.launcher.x
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    return g.launcher.x == x0 + 4, f"x0={x0} x1={g.launcher.x}"


def check_action3_blocked_at_left_edge(GameClass) -> tuple[bool, str]:
    """ACTION3 from launcher.x=0 is a no-op (cannot walk past playfield left edge)."""
    g = GameClass()
    g.set_level(0)
    g.launcher.set_position(0, g.launcher.y)
    x0 = g.launcher.x
    g.perform_action(ActionInput(id=GameAction.ACTION3))
    return g.launcher.x == x0, f"x0={x0} x1={g.launcher.x}"


def check_action6_fires_arc_lands_on_target_l1(GameClass) -> tuple[bool, str]:
    """ACTION6 click from in-range launcher position lands on the target and advances past L1."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    score_before = g._score
    ai = ActionInput(id=GameAction.ACTION6, data={"x": 56, "y": 51})
    g.perform_action(ai)
    ticks = 0
    while g.flight_phase >= 0 and ticks < 200:
        g.perform_action(ai)
        ticks += 1
    return g._score == score_before + 1, f"score {score_before} -> {g._score}, ticks={ticks}"


def check_action_counter_increments_per_walk(GameClass) -> tuple[bool, str]:
    """ACTION4 increments the engine action counter by one."""
    g = GameClass()
    g.set_level(0)
    n0 = g._action_count
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    return g._action_count == n0 + 1, f"before={n0} after={g._action_count}"


CHECKS = [
    check_action4_moves_launcher_right,
    check_action3_blocked_at_left_edge,
    check_action6_fires_arc_lands_on_target_l1,
    check_action_counter_increments_per_walk,
]


if __name__ == "__main__":
    GameClass = _load_game_class()
    all_pass = True
    for ch in CHECKS:
        passed, observed = ch(GameClass)
        marker = "✅" if passed else "❌"
        print(f"{marker} {ch.__name__}: {observed}")
        if not passed:
            all_pass = False
    print("\nALL PASS" if all_pass else "\nSOME FAILURES")
