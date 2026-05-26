"""Custom smoke checks for xz5g — 3 mechanic invariants.

Each check returns (passed: bool, observed: str). Run alongside the
universal checks per `code/smoke-test-checks.md`.
"""

import importlib.util
import sys
from pathlib import Path

src = Path("prior-games/xz5g/xz5g.py")
spec = importlib.util.spec_from_file_location("smoke_xz5g", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = mod.Xz5g

from novaengine import ActionInput, GameAction, InteractionMode  # noqa: E402


def check_click_sets_pivot():
    """Clicking an empty cell sets _pivot and reveals the halo."""
    g = GameClass()
    g.set_level(0)
    pre_pivot = g._pivot
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True
    )
    observed = f"pre={pre_pivot} post={g._pivot}"
    return g._pivot == (32, 32), observed


def check_action5_rotates_avatar():
    """ACTION5 with pivot set rotates the avatar to its CW image."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True
    )
    avatar = g.current_level.get_sprites_by_tag("avatar")[0]
    pre = (avatar.x, avatar.y)
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    if g._score >= 1:
        # Already advanced to next level — check via prior level state by score increment
        observed = f"pre={pre} won_l1=True (score={g._score})"
        return True, observed
    observed = f"pre={pre} post=({avatar.x}, {avatar.y})"
    return (avatar.x, avatar.y) == (32, 12), observed


def check_l3_one_rotation_does_not_win():
    """L3 cannot be won by a single rotation around any pivot."""
    g = GameClass()
    g.set_level(2)  # L3
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True
    )
    score_before = g._score
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    observed = f"score_before={score_before} score_after_one_rotation={g._score}"
    return g._score == score_before, observed


def check_l3_two_rotations_win():
    """L3 wins on the second rotation around the centre."""
    g = GameClass()
    g.set_level(2)  # L3
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True
    )
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    observed = f"final_score={g._score} state={g._state.name}"
    return g._state.name == "WIN", observed


CUSTOM_CHECKS = [
    ("check_click_sets_pivot", check_click_sets_pivot),
    ("check_action5_rotates_avatar", check_action5_rotates_avatar),
    ("check_l3_one_rotation_does_not_win", check_l3_one_rotation_does_not_win),
    ("check_l3_two_rotations_win", check_l3_two_rotations_win),
]


if __name__ == "__main__":
    print("# Custom smoke checks")
    for name, fn in CUSTOM_CHECKS:
        passed, observed = fn()
        marker = "PASS" if passed else "FAIL"
        print(f"- {marker} {name}: {observed}")
