"""Custom smoke checks for fw8c."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load_game():
    src = Path("prior-games/fw8c/fw8c.py")
    spec = importlib.util.spec_from_file_location("smoke_fw8c_custom", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, mod.Fw8c


def _act(n):
    return ActionInput(id=GameAction.from_id(n), data={})


def check_arrow_moves_carrier():
    """ACTION4 (right) moves the carrier sprite by STEP_SIZE pixels in +x."""
    mod, GameClass = _load_game()
    g = GameClass()
    g.set_level(0)
    carrier = g._get_carrier()
    x0 = carrier.x
    g.perform_action(_act(4), raw=True)
    return carrier.x == x0 + mod.STEP_SIZE, f"x0={x0} x1={carrier.x}"


def check_pad_pickup_sets_pigment():
    """Stepping onto pad_orange sets the carrier's pigment_set bit 0."""
    mod, GameClass = _load_game()
    g = GameClass()
    g.set_level(0)
    # Carrier starts at cell (1,1). pad_orange in L1 is at cell (3,3).
    # Walk: R, R, D, D
    for aid in [4, 4, 2, 2]:
        g.perform_action(_act(aid), raw=True)
    return g._pigment_set == mod.PIGMENT_ORANGE, (
        f"pigment_set={g._pigment_set:#b} expected={mod.PIGMENT_ORANGE:#b}"
    )


def check_slot_consume_clears_pigment():
    """Stepping onto slot_orange while state {orange} consumes the slot
    AND clears the carrier's pigment_set."""
    mod, GameClass = _load_game()
    g = GameClass()
    g.set_level(0)
    # Witness for L1: 4,4,2,2,4,4,4,2,2
    for aid in [4, 4, 2, 2, 4, 4, 4, 2, 2]:
        g.perform_action(_act(aid), raw=True)
    # After A9 the carrier should have consumed slot_orange and the level
    # should have advanced or be at win state.
    return g._pigment_set == 0, f"post-consume pigment_set={g._pigment_set}"


def check_door_blocks_when_unmatched():
    """At L3, the carrier with empty pigment_set cannot enter the door cell."""
    mod, GameClass = _load_game()
    g = GameClass()
    g.set_level(2)  # L3
    carrier = g._get_carrier()
    # door_green is at cell (4, 4). Walk carrier toward it without picking
    # up both pigments, then attempt to enter.
    # From (1,1) walk R,R,R,D,D,D — passes through pad_orange at (1,3) only
    # if going down column 1, but here we go right first.
    # Path: (1,1)→(2,1)→(3,1)→(4,1)→(4,2)→(4,3)→(4,4). At (4,4) door blocks.
    for aid in [4, 4, 4, 2, 2]:
        g.perform_action(_act(aid), raw=True)
    # Now at (4,3). State {} (no pad crossed). Attempting D should be blocked.
    x_before = carrier.x
    y_before = carrier.y
    g.perform_action(_act(2), raw=True)
    # Carrier should not have moved — door is TANGIBLE because state ≠ {O,P}.
    return carrier.x == x_before and carrier.y == y_before, (
        f"before=({x_before},{y_before}) after=({carrier.x},{carrier.y}) "
        f"pigment_set={g._pigment_set}"
    )


CHECKS = [
    check_arrow_moves_carrier,
    check_pad_pickup_sets_pigment,
    check_slot_consume_clears_pigment,
    check_door_blocks_when_unmatched,
]


if __name__ == "__main__":
    for fn in CHECKS:
        passed, observed = fn()
        print(f"{'PASS' if passed else 'FAIL'} {fn.__name__}: {observed}")
