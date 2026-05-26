"""Custom smoke-test checks for hk7v.

Each check returns (passed: bool, observed: str). Each tests ONE
mechanic invariant with ≤ 5 setup actions and ONE boolean assertion.
"""

from novaengine import ActionInput, GameAction


def check_action4_moves_trolley_right(GameClass):
    """ACTION4 advances the trolley one cell to the right."""
    g = GameClass()
    g.set_level(0)
    x0 = g.trolley.x
    g.perform_action(ActionInput(id=GameAction.ACTION4, data={}), raw=True)
    return g.trolley.x == x0 + 1, f"x0={x0} x1={g.trolley.x}"


def check_action2_lower_blocks_at_block_top(GameClass):
    """ACTION2 lowering hook stops one row above a block in the same column."""
    g = GameClass()
    g.set_level(0)
    # Move trolley above block_red (at column 14).
    for _ in range(14):
        g.perform_action(ActionInput(id=GameAction.ACTION4, data={}), raw=True)
    # Lower hook 60 times — should stop short of hitting block_red.
    for _ in range(60):
        g.perform_action(ActionInput(id=GameAction.ACTION2, data={}), raw=True)
    # block_red is at y=53 with height 5; hook (height 4) should stop at y=49
    # (hook bottom 52, block top 53 — adjacent).
    return g.hook.y == 49, f"hook.y={g.hook.y} (expected 49)"


def check_action5_grabs_block_directly_below(GameClass):
    """ACTION5 grabs a block whose top is directly below the hook bottom."""
    g = GameClass()
    g.set_level(0)
    # Position hook directly above block_red (column 14, hook.y must be 49).
    for _ in range(14):
        g.perform_action(ActionInput(id=GameAction.ACTION4, data={}), raw=True)
    for _ in range(60):
        g.perform_action(ActionInput(id=GameAction.ACTION2, data={}), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION5, data={}), raw=True)
    return g.carrying is not None, f"carrying={g.carrying}"


def check_lose_at_budget(GameClass):
    """Reaching the L1 step budget triggers the lose state."""
    g = GameClass()
    g.set_level(0)
    budget = g.current_level.get_data("step_budget") or 150
    # Spam ACTION1 (no-op when at minimum) until budget exceeded.
    for _ in range(budget + 2):
        g.perform_action(ActionInput(id=GameAction.ACTION1, data={}), raw=True)
    return g._state.name == "GAME_OVER", f"state={g._state.name}"
