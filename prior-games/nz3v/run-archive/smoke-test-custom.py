"""Custom smoke checks for nz3v.

Each function returns (bool, str) — (passed, observed).
"""
from novaengine import ActionInput, GameAction


def check_action4_moves_avatar_east(GameClass) -> tuple[bool, str]:
    """ACTION4 moves the avatar one cell east when destination is in lit sector."""
    g = GameClass()
    g.set_level(0)
    avatar = g._avatar()
    x0 = avatar.x
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    return avatar.x == x0 + 1, f"x0={x0} x1={avatar.x}"


def check_action_counter_increments(GameClass) -> tuple[bool, str]:
    """Each action increments the engine action counter by 1."""
    g = GameClass()
    g.set_level(0)
    n0 = g._action_count
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    return g._action_count == n0 + 1, f"before={n0} after={g._action_count}"


def check_rotor_advances_after_K_actions(GameClass) -> tuple[bool, str]:
    """After K=6 valid NW-phase actions, rotor angle advances from NW (0) to NE (1)."""
    g = GameClass()
    g.set_level(0)
    setup = [4, 4, 4, 4, 2]
    for a in setup:
        g.perform_action(ActionInput(id=GameAction.from_id(a)))
    angle_before = g._rotor_angle
    g.perform_action(ActionInput(id=GameAction.ACTION2))
    return g._rotor_angle == 1 and angle_before == 0, (
        f"angle_before={angle_before} angle_after={g._rotor_angle}"
    )


def check_stop_tile_freezes_rotor(GameClass) -> tuple[bool, str]:
    """Stepping on a stop-tile at L2 sets _frozen_remaining > 0."""
    g = GameClass()
    g.set_level(1)
    setup = [2, 2, 2]
    for a in setup:
        g.perform_action(ActionInput(id=GameAction.from_id(a)))
    frozen_before = g._frozen_remaining
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    return g._frozen_remaining > 0 and frozen_before == 0, (
        f"frozen_before={frozen_before} frozen_after={g._frozen_remaining}"
    )


CUSTOM_CHECKS = [
    check_action4_moves_avatar_east,
    check_action_counter_increments,
    check_rotor_advances_after_K_actions,
    check_stop_tile_freezes_rotor,
]
