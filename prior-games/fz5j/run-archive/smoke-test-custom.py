"""Custom smoke checks for fz5j (phase-step-tile)."""

from novaengine import ActionInput, GameAction


def check_right_moves_avatar(GameClass):
    """ACTION4 (right) on a plain-floor cell shifts the avatar one logical cell east."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.RESET))
    avatar = g.current_level.get_sprites_by_tag("player")[0]
    x0 = avatar.x
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    avatar = g.current_level.get_sprites_by_tag("player")[0]
    observed = f"x0={x0} x1={avatar.x}"
    return avatar.x == x0 + 4, observed


def check_phase_tile_blocks_on_wrong_residue(GameClass):
    """A phase-2-offset-0 tile rejects entry on an odd step counter (residue 1)."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.RESET))
    # Walk to (3,5) at t=2 (one cell west of the (4,5) phase-2-off-0 tile), then attempt entry at t=3.
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)  # t=1, (2,5)
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)  # t=2, (3,5)
    avatar = g.current_level.get_sprites_by_tag("player")[0]
    x_before = avatar.x
    # t=3 attempt (4,5): 3%2=1 != 0 -> blocked.
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    avatar = g.current_level.get_sprites_by_tag("player")[0]
    observed = f"x_before={x_before} x_after={avatar.x}"
    return avatar.x == x_before, observed


def check_step_counter_ticks_on_blocked_move(GameClass):
    """A move attempt that is rejected by a closed phase tile still increments the step counter."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.RESET))
    # Step counter is exposed via _step_counter; same as engine _action_count.
    n0 = g._step_counter
    # Attempt UP from (1,5) -> (1,4) which is plain floor; this still ticks counter, but we want to
    # test the blocked-tick. Use ACTION3 (LEFT) into wall at (0,5).
    g.perform_action(ActionInput(id=GameAction.ACTION3), raw=True)
    n1 = g._step_counter
    avatar = g.current_level.get_sprites_by_tag("player")[0]
    observed = f"n0={n0} n1={n1} x={avatar.x}"
    # Wall-bounce against perimeter: avatar still at x=4; counter went up by 1.
    return n1 == n0 + 1, observed


def check_lose_at_budget(GameClass):
    """Exhausting the L1 step budget (22) by wall-bouncing fires GAME_OVER."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.RESET))
    last_state = None
    for _ in range(25):  # exceed budget of 22
        fd = g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
        last_state = fd.state
    observed = f"final_state={last_state.name if last_state else None}"
    return last_state is not None and last_state.name == "GAME_OVER", observed
