"""Custom smoke checks for hr8q (pair-blend recipe game)."""

from __future__ import annotations

from novaengine import ActionInput, GameAction


def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2


def check_click_fills_slot(GameClass) -> tuple[bool, str]:
    """ACTION6 on a primary ingredient block fills the next empty input slot with that block's colour."""
    g = GameClass()
    g.set_level(0)
    target = g.ingredients[0]
    gx = int(target.block.x) + 3
    gy = int(target.block.y) + 3
    fx, fy = _grid_to_display_px(g.current_level.grid_size, gx, gy)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    observed = f"slot[0]={g.slot_colors[0]} expected={target.color}"
    return g.slot_colors[0] == target.color, observed


def check_l1_minimal_solve(GameClass) -> tuple[bool, str]:
    """The 3-action L1 witness (click magenta, click light-blue, ACTION5 commit) advances past L1."""
    g = GameClass()
    g.set_level(0)
    seq = [g.ingredients[0], g.ingredients[1]]
    for ing in seq:
        gx = int(ing.block.x) + 3
        gy = int(ing.block.y) + 3
        fx, fy = _grid_to_display_px(g.current_level.grid_size, gx, gy)
        g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    return g._current_level_index == 1, f"level after solve={g._current_level_index}"


def check_mismatched_commit_distils(GameClass) -> tuple[bool, str]:
    """At L2, a 2-slot commit whose result mismatches the target appends a new intermediate to the palette."""
    g = GameClass()
    g.set_level(1)  # L2
    n0 = len(g.ingredients)
    # Click magenta and light-blue to fill slot1, slot2 with (M, LB) -> purple, mismatch with maroon target.
    for ing in (g.ingredients[0], g.ingredients[1]):
        fx, fy = _grid_to_display_px(g.current_level.grid_size, int(ing.block.x) + 3, int(ing.block.y) + 3)
        g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    n1 = len(g.ingredients)
    return n1 == n0 + 1, f"ingredients before={n0} after={n1}"


def check_lose_at_budget(GameClass) -> tuple[bool, str]:
    """Exhausting the L1 step budget without solving fires self.lose()."""
    g = GameClass()
    g.set_level(0)
    budget = g.max_steps
    # Repeatedly fire ACTION5 with empty slots — no-op for state, but each consumes a step.
    for _ in range(budget + 1):
        g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    return g._state.name == "GAME_OVER", f"state after budget+1={g._state.name}"


CUSTOM_CHECKS = [
    ("check_click_fills_slot", check_click_fills_slot),
    ("check_l1_minimal_solve", check_l1_minimal_solve),
    ("check_mismatched_commit_distils", check_mismatched_commit_distils),
    ("check_lose_at_budget", check_lose_at_budget),
]
