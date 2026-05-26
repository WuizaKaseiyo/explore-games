"""Custom smoke checks for zk9p.

Each check returns (passed: bool, observed: str) and is callable as
`fn(GameClass)`. Run via the smoke-test runner alongside the universal
checks defined in skills/code/smoke-test-checks.md.
"""

from novaengine import ActionInput, GameAction, InteractionMode


def check_up_moves_avatar(GameClass) -> tuple[bool, str]:
    """ACTION1 (UP) decrements the avatar's y by 1 on a clear cell."""
    g = GameClass()
    g.set_level(0)
    avatar = g._avatar()
    y0 = avatar.y
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    return avatar.y == y0 - 1, f"y0={y0} y1={avatar.y}"


def check_pursuer_chases_after_avatar_move(GameClass) -> tuple[bool, str]:
    """A Manhattan pursuer's y advances toward the avatar after one UP."""
    g = GameClass()
    g.set_level(0)
    red = g.current_level.get_sprites_by_name("pursuer_red")[0]
    y0 = red.y
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    return red.y == y0 + 1, f"red.y0={y0} red.y1={red.y}"


def check_l1_minimal_solve_advances_level(GameClass) -> tuple[bool, str]:
    """L1 is solvable: pressing UP four times merges red+yellow and advances to L2."""
    g = GameClass()
    g.set_level(0)
    for _ in range(4):
        g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    return g._current_level_index == 1, f"level_idx after UP×4 = {g._current_level_index}"


def check_lose_at_budget(GameClass) -> tuple[bool, str]:
    """Repeated no-op (ACTION5 in L1) drains the step budget and triggers lose."""
    g = GameClass()
    g.set_level(0)
    budget = g._step_budget
    # ACTION5 in L1 is gated to a no-op (1 unit drain, no pursuer advance).
    # Drain the entire budget; lose() should fire on the action that hits zero.
    for _ in range(budget + 1):
        g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
        if g._state.name == "GAME_OVER":
            break
    return g._state.name == "GAME_OVER", f"state={g._state.name} budget={budget} used={g._step_units_used}"


CHECKS = [
    check_up_moves_avatar,
    check_pursuer_chases_after_avatar_move,
    check_l1_minimal_solve_advances_level,
    check_lose_at_budget,
]
