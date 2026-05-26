"""Custom mechanic-invariant checks for dj5h.

Each function follows the strict template in `code/smoke-test-checks.md`:
- ≤ 5 setup actions
- ONE action under test
- ONE boolean assertion
- fully deterministic, < 1s wall-clock
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load():
    src = Path("prior-games/dj5h/dj5h.py")
    spec = importlib.util.spec_from_file_location("smoke_dj5h_custom", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, mod.Dj5h


def check_action4_moves_avatar_right():
    """ACTION4 (right) moves the avatar by exactly WALK_STEP=4 pixels in +x when the destination is walkable."""
    mod, GameClass = _load()
    g = GameClass()
    g.set_level(0)
    avatar = g._level_sprite("avatar")
    x0 = avatar.x
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    avatar = g._level_sprite("avatar")
    passed = avatar.x == x0 + mod.WALK_STEP
    return passed, f"x0={x0} x1={avatar.x}"


def check_click_on_wheel_selects_pulley():
    """ACTION6 inside a pulley wheel's footprint sets `active_pulley` to that wheel."""
    mod, GameClass = _load()
    g = GameClass()
    g.set_level(0)
    # PA wheel at (28, 5) on L1
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 30, "y": 7}), raw=True)
    passed = g.active_pulley == "PA"
    return passed, f"active_pulley={g.active_pulley!r}"


def check_action5_flips_pulley_state():
    """ACTION5 with an active pulley flips that pulley's state from LEFT_HIGH ↔ LEFT_LOW."""
    mod, GameClass = _load()
    g = GameClass()
    g.set_level(0)
    # Setup: select PA via click.
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 30, "y": 7}), raw=True)
    s0 = g.pulley_state["PA"]
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    s1 = g.pulley_state["PA"]
    passed = s0 != s1
    return passed, f"before={s0} after={s1}"


def check_toggle_carries_avatar_when_on_low_platform():
    """ACTION5 carries the avatar with the platform when avatar's foot is on a LOW platform that rises to HIGH."""
    mod, GameClass = _load()
    g = GameClass()
    g.set_level(0)
    # Setup: click PA, toggle so red drops LOW, walk avatar onto red, then toggle back.
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 30, "y": 7}), raw=True)  # 1
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)                          # 2 (red→LOW)
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)                          # 3 (12→16)
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)                          # 4 (16→20)
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)                          # 5 (20→24); avatar on red
    # Action under test: ACTION5 (red rises HIGH, avatar carried up).
    avatar = g._level_sprite("avatar")
    y0 = avatar.y
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    avatar = g._level_sprite("avatar")
    # Expectation: avatar.y dropped from row 53 (LOW) to row 11 (HIGH).
    passed = avatar.y < y0
    return passed, f"y0={y0} y1={avatar.y}"


CHECKS = [
    check_action4_moves_avatar_right,
    check_click_on_wheel_selects_pulley,
    check_action5_flips_pulley_state,
    check_toggle_carries_avatar_when_on_low_platform,
]


if __name__ == "__main__":
    for fn in CHECKS:
        ok, observed = fn()
        print(f"{'PASS' if ok else 'FAIL'} {fn.__name__}: {observed}")
