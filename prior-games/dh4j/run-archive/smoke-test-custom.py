"""Custom mechanic-invariant checks for dh4j (tile-coded-stride)."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load_game_class():
    src = Path("prior-games/dh4j/dh4j.py")
    spec = importlib.util.spec_from_file_location("smoke_dh4j", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Dh4j


GameClass = _load_game_class()


def check_stride_1_walks_one_cell() -> tuple[bool, str]:
    """A UP press from a 1-pip yellow floor cell moves the avatar exactly 1 cell up."""
    g = GameClass()
    # L1 avatar starts at (3, 5) on a 1-pip yellow cell.
    av = g._get_avatar()
    y0 = av.y
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    av = g._get_avatar()
    moved = (av.y == y0 - 8)
    return moved, f"y0={y0}, y1={av.y} (expected stride-1 = -8 px)"


def check_stride_3_leaps_over_wall() -> tuple[bool, str]:
    """A UP press from the L1 stride-3 cell at (3,4) leaps over the wall row at y=3 to land on the goal at (3,1)."""
    g = GameClass()
    # Step once to land on the stride-3 cell at (3, 4).
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    av = g._get_avatar()
    pre = (av.x, av.y)
    # Now press UP from the stride-3 cell. Destination should be (3, 1) which is the goal.
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    advanced_level = (g._score == 1)
    return advanced_level, f"pre={pre}, score_after_leap={g._score}"


def check_filter_toggles_legend() -> tuple[bool, str]:
    """Landing on the L2 filter cell at (5,5) toggles the legend from yellow to blue."""
    g = GameClass()
    # Skip past L1 with [UP, UP].
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    assert g._score == 1, "L1 witness failed to advance"
    pre_legend = g._legend
    # Two RIGHT presses to reach the filter at (5, 5).
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    post_legend = g._legend
    toggled = (pre_legend == "yellow" and post_legend == "blue")
    return toggled, f"pre={pre_legend}, post={post_legend}"


def check_pivot_arms_bonus_then_consumes_on_next_press() -> tuple[bool, str]:
    """Landing on the L3 pivot at (3,5) arms _pending_bonus=1; the next press consumes the bonus AND consumes the pivot cell itself."""
    g = GameClass()
    # Skip L1 + L2.
    for a in [GameAction.ACTION1, GameAction.ACTION1]:
        g.perform_action(ActionInput(id=a), raw=True)
    for a in [GameAction.ACTION4, GameAction.ACTION4, GameAction.ACTION3, GameAction.ACTION3, GameAction.ACTION1, GameAction.ACTION1, GameAction.ACTION1]:
        g.perform_action(ActionInput(id=a), raw=True)
    assert g._score == 2, "L2 witness failed to advance"
    # At L3 start (avatar at (3, 6)). UP press lands avatar on pivot at (3, 5).
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    armed_bonus = g._pending_bonus
    pivot_sprite_armed = g._armed_pivot is not None
    # Now press DOWN — pivot bonus should consume regardless of slide outcome.
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)
    consumed_bonus = (g._pending_bonus == 0)
    consumed_pivot = (g._armed_pivot is None)
    passed = armed_bonus == 1 and pivot_sprite_armed and consumed_bonus and consumed_pivot
    return passed, f"armed_bonus={armed_bonus}, armed_pivot={pivot_sprite_armed}, post_bonus={g._pending_bonus}, post_armed={g._armed_pivot}"


if __name__ == "__main__":
    checks = [
        check_stride_1_walks_one_cell,
        check_stride_3_leaps_over_wall,
        check_filter_toggles_legend,
        check_pivot_arms_bonus_then_consumes_on_next_press,
    ]
    for fn in checks:
        passed, obs = fn()
        marker = "PASS" if passed else "FAIL"
        print(f"{marker} {fn.__name__}: {obs}")
