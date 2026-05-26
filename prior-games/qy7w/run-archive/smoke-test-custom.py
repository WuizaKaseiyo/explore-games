"""Custom smoke checks for qy7w. Each check returns (passed, observed)."""

import importlib.util
from pathlib import Path
from novaengine import ActionInput, GameAction


def _load_game_class():
    src = Path("prior-games/qy7w/qy7w.py")
    spec = importlib.util.spec_from_file_location("smoke_qy7w_custom", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Qy7w


GameClass = _load_game_class()


def _click(x, y):
    return ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y})


def check_binary_toggle_reroutes_strands() -> tuple[bool, str]:
    """Toggling a binary crossing actually swaps the strands at its column pair."""
    g = GameClass()
    g.set_level(0)
    before = list(g._bottom_strands)
    # L1 C2 is at (cols 1-2, y=28); valid action exposed at (41, 28).
    g.perform_action(_click(41, 28))
    after = list(g._bottom_strands)
    # Strand 1 and strand 2 should have swapped columns.
    s1_col_before = before[1][0]
    s2_col_before = before[2][0]
    s1_col_after = after[1][0]
    s2_col_after = after[2][0]
    passed = (s1_col_after == s2_col_before) and (s2_col_after == s1_col_before)
    return passed, f"before={before} after={after}"


def check_long_toggle_swaps_outer_columns() -> tuple[bool, str]:
    """Toggling a long crossing swaps strands at columns 0 and 2 (col 1 unchanged)."""
    g = GameClass()
    g.set_level(1)  # L2 has the LONG crossing.
    before = list(g._bottom_strands)
    # L2 C2 (long) valid-action click is at (25, 22).
    g.perform_action(_click(25, 22))
    after = list(g._bottom_strands)
    # Find strand identities at cols 0, 1, 2 before and after.
    by_col_before = {col: idx for idx, (col, _c) in enumerate(before)}
    by_col_after = {col: idx for idx, (col, _c) in enumerate(after)}
    swapped_outer = (
        by_col_before.get(0) == by_col_after.get(2)
        and by_col_before.get(2) == by_col_after.get(0)
    )
    middle_unchanged = by_col_before.get(1) == by_col_after.get(1)
    passed = swapped_outer and middle_unchanged
    return passed, f"before={before} after={after}"


def check_shift_changes_bottom_colour() -> tuple[bool, str]:
    """The shift cell remaps a strand's colour mid-route — visible in bottom_strands."""
    g = GameClass()
    g.set_level(2)  # L3 has the shift cell.
    # In L3 with no toggles, strand_R (idx 0) starts at col 0 and routes through
    # shift_green at (col=0, y=38). At the bottom it should carry colour 14
    # (green), not 8 (red).
    bottom = list(g._bottom_strands)
    strand_0_bottom_colour = bottom[0][1]
    passed = strand_0_bottom_colour == 14
    return passed, f"strand 0 bottom colour={strand_0_bottom_colour} (expected 14=green)"


def check_step_budget_lose() -> tuple[bool, str]:
    """Exhausting the step budget on a non-winning configuration triggers lose."""
    g = GameClass()
    g.set_level(0)
    budget = g.current_level.get_data("step_budget")
    # Toggle C1 budget+1 times. Each toggle alternates state, never reaching the
    # winning configuration (which is C2 + C3 toggled). The level should lose.
    for _ in range(budget + 1):
        g.perform_action(_click(25, 16))  # L1 C1
    state_name = g._state.name if hasattr(g._state, "name") else str(g._state)
    passed = state_name == "GAME_OVER"
    return passed, f"state after budget+1 actions={state_name}"


CHECKS = [
    check_binary_toggle_reroutes_strands,
    check_long_toggle_swaps_outer_columns,
    check_shift_changes_bottom_colour,
    check_step_budget_lose,
]


if __name__ == "__main__":
    for fn in CHECKS:
        passed, observed = fn()
        marker = "PASS" if passed else "FAIL"
        print(f"[{marker}] {fn.__name__}: {observed}")
