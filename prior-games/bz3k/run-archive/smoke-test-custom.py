"""Custom smoke checks for bz3k. Each returns (bool, str)."""

from novaengine import ActionInput, GameAction


def check_arrow_applies_impulse(GameClass) -> tuple[bool, str]:
    """ACTION4 from rest produces vx=1."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.ACTION4, data={}))
    return g.vx == 1, f"vx_after_one_press={g.vx}"


def check_consecutive_arrows_accumulate(GameClass) -> tuple[bool, str]:
    """Two →'s in a row produce vx=2 (impulse accumulates)."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.ACTION4, data={}))
    g.perform_action(ActionInput(id=GameAction.ACTION4, data={}))
    return g.vx == 2, f"vx_after_two_presses={g.vx}"


def check_cap_clamps_velocity(GameClass) -> tuple[bool, str]:
    """Traversing a cap_band cell with high vx clamps vx magnitude to 1."""
    g = GameClass()
    g.set_level(2)  # L3 bottom corridor: cap-band at center (28, 50).
    # 5 setup presses build vx to 5; the 6th press is the action under test
    # (its slide passes through the cap cell at center (28, 50)).
    for _ in range(5):
        g.perform_action(ActionInput(id=GameAction.ACTION4, data={}))
    g.perform_action(ActionInput(id=GameAction.ACTION4, data={}))
    return g.vx == 1, f"vx_after_cap_traversal={g.vx}"


def check_up_applies_vy_impulse(GameClass) -> tuple[bool, str]:
    """ACTION1 (UP) from rest produces vy=-1 — vertical-axis analogue of the horizontal impulse rule."""
    g = GameClass()
    g.set_level(0)  # L1 open arena: vy ramp is unblocked anywhere in the chamber.
    g.perform_action(ActionInput(id=GameAction.ACTION1, data={}))
    return g.vy == -1, f"vy_after_one_up_press={g.vy}"
