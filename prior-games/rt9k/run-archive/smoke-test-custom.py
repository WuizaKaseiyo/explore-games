"""Custom smoke checks for `rt9k` — four mechanic-essential invariants."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


SRC = Path("prior-games/rt9k/rt9k.py")
spec = importlib.util.spec_from_file_location("smoke_rt9k", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
Rt9k = mod.Rt9k


def _act(action_int):
    return ActionInput(id=GameAction.from_id(action_int), data={})


def check_left_moves_avatar() -> tuple[bool, str]:
    """ACTION3 (LEFT) moves the avatar one cell left in open interior."""
    g = Rt9k()
    g.set_level(1)  # L2: avatar at (4, 4); cell at (0, 4) is open.
    avatar = g.current_level.get_sprites_by_tag("player")[0]
    x0, y0 = avatar.x, avatar.y
    g.perform_action(_act(3), raw=True)
    return avatar.x == x0 - 4 and avatar.y == y0, f"x: {x0}->{avatar.x}, y: {y0}->{avatar.y}"


def check_left_wrap_changes_tone() -> tuple[bool, str]:
    """LEFT-wrap from x=0 lands at x=60 AND advances tone by -1 (mod 3)."""
    g = Rt9k()
    g.set_level(1)
    g.perform_action(_act(3), raw=True)  # (4,4) -> (0,4); tone unchanged.
    avatar = g.current_level.get_sprites_by_tag("player")[0]
    tone_before = g._tone
    g.perform_action(_act(3), raw=True)  # (0,4) -> wrap to (60,4); tone -= 1 mod 3.
    expected_tone = (tone_before - 1) % 3
    return avatar.x == 60 and g._tone == expected_tone, (
        f"avatar=({avatar.x},{avatar.y}); tone {tone_before}->{g._tone} (expected {expected_tone})"
    )


def check_wall_blocks_movement() -> tuple[bool, str]:
    """A solid wall at the destination blocks movement (avatar position unchanged)."""
    g = Rt9k()
    g.set_level(1)  # L2: avatar at (4, 4); solid wall column at pixel x=32.
    # Setup (5 RIGHT presses): (4,4) -> (8,4) -> (12,4) -> (16,4) -> (20,4) -> (24,4).
    # Wait, that's only 5 RIGHTs. Need (28, 4) so a 6th RIGHT attempts (32, 4) = wall.
    # Use 6 setup actions — that exceeds the "≤ 5 setup" template constraint.
    # Instead: choose a closer starting level. L1 has avatar at (16, 28); 4
    # setup RIGHT presses land at (32, 28) which IS the wall — but the 4th
    # RIGHT itself is the action under test, only 3 setup. Let's use L1.
    g_l1 = Rt9k()
    g_l1.set_level(0)  # L1: avatar at (16, 28), wall at col 8 (pixel x=32).
    for _ in range(3):  # 3 setup actions: (16,28) -> (20,28) -> (24,28) -> (28,28).
        g_l1.perform_action(_act(4), raw=True)
    avatar = g_l1.current_level.get_sprites_by_tag("player")[0]
    x0, y0 = avatar.x, avatar.y  # expect (28, 28).
    g_l1.perform_action(_act(4), raw=True)  # try to step into wall at (32, 28).
    return avatar.x == x0 and avatar.y == y0, (
        f"avatar=({avatar.x},{avatar.y}); pre-attempt was ({x0},{y0})"
    )


def check_step_budget_decrements() -> tuple[bool, str]:
    """Each action consumes exactly one step from the budget."""
    g = Rt9k()
    g.set_level(0)
    before = g._steps_remaining
    g.perform_action(_act(3), raw=True)
    return g._steps_remaining == before - 1, f"before={before}, after={g._steps_remaining}"


CHECKS = [
    ("check_left_moves_avatar", check_left_moves_avatar),
    ("check_left_wrap_changes_tone", check_left_wrap_changes_tone),
    ("check_wall_blocks_movement", check_wall_blocks_movement),
    ("check_step_budget_decrements", check_step_budget_decrements),
]


if __name__ == "__main__":
    for name, fn in CHECKS:
        ok, observed = fn()
        print(f"{'PASS' if ok else 'FAIL'} {name}: {observed}")
