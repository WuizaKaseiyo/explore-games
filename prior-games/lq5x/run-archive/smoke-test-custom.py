"""Custom smoke-test checks for lq5x — mechanic-specific invariants."""

from novaengine import ActionInput, GameAction


def check_walk_moves_lantern(GameClass) -> tuple[bool, str]:
    """ACTION4 (RIGHT) advances the lantern's x by 1."""
    g = GameClass()
    g.set_level(0)
    x0 = g.lantern.x
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    return g.lantern.x == x0 + 1, f"x0={x0} x1={g.lantern.x}"


def check_action5_rotates_facing(GameClass) -> tuple[bool, str]:
    """ACTION5 advances the cone facing by exactly +1 mod 4."""
    g = GameClass()
    g.set_level(0)
    f0 = g.facing
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    return g.facing == (f0 + 1) % 4, f"f0={f0} f1={g.facing}"


def check_wax_pickup_extends_range(GameClass) -> tuple[bool, str]:
    """In L2, walking UP onto the (3,6) wax pickup increases cone_range by 2."""
    g = GameClass()
    g.set_level(1)
    r0 = g.cone_range
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    return g.cone_range == r0 + 2, f"r0={r0} r1={g.cone_range}"


def check_l1_minimal_solve(GameClass) -> tuple[bool, str]:
    """The 5-action L1 witness sequence advances to level 2."""
    g = GameClass()
    g.set_level(0)
    for aid in [
        GameAction.ACTION5,
        GameAction.ACTION4,
        GameAction.ACTION2,
        GameAction.ACTION2,
        GameAction.ACTION5,
    ]:
        g.perform_action(ActionInput(id=aid), raw=True)
    return g._current_level_index == 1, f"level after solve={g._current_level_index}"
