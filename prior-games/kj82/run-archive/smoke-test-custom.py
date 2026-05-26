"""Custom smoke-test checks for kj82.

Each function takes the loaded GameClass and returns (passed, observed).
"""

from novaengine import ActionInput, GameAction


def _act(n):
    table = {
        1: GameAction.ACTION1,
        2: GameAction.ACTION2,
        3: GameAction.ACTION3,
        4: GameAction.ACTION4,
        5: GameAction.ACTION5,
        6: GameAction.ACTION6,
    }
    return ActionInput(id=table[n], data={})


def _click_grid(gx, gy):
    """Convert grid (gx, gy) → display pixel (centre of cell at scale 2)."""
    return ActionInput(id=GameAction.ACTION6, data={"x": gx * 2 + 1, "y": gy * 2 + 1})


def check_click_selects_plank(GameClass):
    """ACTION6 click on a plank cell sets that plank as active."""
    g = GameClass()
    g.handle_reset()
    # L1 plank_main covers (10..17, 10..11). Click on (13, 10).
    g.perform_action(_click_grid(13, 10))
    return g._active_plank is not None, f"active_plank={g._active_plank}"


def check_pivot_increments_orientation(GameClass):
    """ACTION5 with an active plank advances orientation by 1 (mod 4)."""
    g = GameClass()
    g.handle_reset()
    g.perform_action(_click_grid(13, 10))
    o0 = g._active_plank.orientation
    g.perform_action(_act(5))
    o1 = g._active_plank.orientation
    return o1 == (o0 + 1) % 4, f"o0={o0} o1={o1}"


def check_walk_moves_pawn_after_pivot(GameClass):
    """After click+pivot, ACTION2 (south walk) moves pawn 1 cell south."""
    g = GameClass()
    g.handle_reset()
    g.perform_action(_click_grid(13, 10))
    g.perform_action(_act(5))
    y0 = g._pawn.y
    g.perform_action(_act(2))
    return g._pawn.y == y0 + 1, f"y0={y0} y1={g._pawn.y}"


def check_lose_at_budget(GameClass):
    """Doing budget+1 actions on L1 without winning fires lose()."""
    g = GameClass()
    g.handle_reset()
    # Spam ACTION3 (left) — pawn at (13, 10) cannot leave plank to the left
    # at every step (plank_main east cells are (10..17, 10..11), so left is OK
    # until (10, 10), then blocked). Mostly no-op walks plus eventually budget.
    # L1 budget is 30. Run 31 actions without winning.
    for _ in range(31):
        g.perform_action(_act(3))
    return g._state.name == "GAME_OVER", f"state={g._state.name} actions={g._action_count}"
