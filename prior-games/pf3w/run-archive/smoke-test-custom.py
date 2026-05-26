"""Custom smoke-test checks for pf3w."""

from novaengine import ActionInput, GameAction


def check_action6_activates_slot(GameClass) -> tuple[bool, str]:
    """ACTION6 click on the L1 slot's center cell creates an active emitter."""
    g = GameClass()
    g.set_level(0)
    n0 = len(g._active_emitters)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 13, "y": 33}))
    n1 = len(g._active_emitters)
    return n1 == n0 + 1, f"emitters before={n0} after={n1}"


def check_action5_advances_global_tick(GameClass) -> tuple[bool, str]:
    """ACTION5 increments the global tick counter by exactly 1."""
    g = GameClass()
    g.set_level(0)
    t0 = g._global_tick
    g.perform_action(ActionInput(id=GameAction.ACTION5))
    t1 = g._global_tick
    return t1 == t0 + 1, f"tick before={t0} after={t1}"


def check_l1_minimal_solve(GameClass) -> tuple[bool, str]:
    """L1's witness solution (1 ACTION6 + 8 ACTION5) advances to level 2."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 13, "y": 33}))
    for _ in range(8):
        g.perform_action(ActionInput(id=GameAction.ACTION5))
    return g._current_level_index == 1, f"level after L1 witness={g._current_level_index}"


def check_lose_at_budget(GameClass) -> tuple[bool, str]:
    """ACTION5-spamming past L1's step budget triggers a lose state."""
    g = GameClass()
    g.set_level(0)
    budget = g._max_steps  # 30 for L1
    for _ in range(budget + 1):
        g.perform_action(ActionInput(id=GameAction.ACTION5))
    return g._state.name == "GAME_OVER", f"state after budget+1={g._state.name}"


CUSTOM_CHECKS = [
    check_action6_activates_slot,
    check_action5_advances_global_tick,
    check_l1_minimal_solve,
    check_lose_at_budget,
]
