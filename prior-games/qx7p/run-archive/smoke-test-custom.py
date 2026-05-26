"""Custom smoke checks for qx7p — column-shift row-align mechanic invariants.

Each function takes the GameClass and returns (passed: bool, observed: str).
"""

from novaengine import ActionInput, GameAction


def check_action1_shifts_active_column(GameClass) -> tuple[bool, str]:
    """ACTION1 increments active column's position by 1 mod 12."""
    g = GameClass()
    g.full_reset()
    # Setup: click col_l1_a to make it active.
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 16, "y": 14}))
    pos_before = g.column_positions["col_l1_a"]
    # Action under test.
    g.perform_action(ActionInput(id=GameAction.ACTION1, data={}))
    pos_after = g.column_positions["col_l1_a"]
    return pos_after == (pos_before + 1) % 12, f"before={pos_before} after={pos_after}"


def check_click_sets_active_column(GameClass) -> tuple[bool, str]:
    """ACTION6 inside a column sets it as the active column."""
    g = GameClass()
    g.full_reset()
    target_name = "col_l1_b"
    # Action under test: click col_l1_b at (32, 14).
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 14}))
    active_name = g.active_column.name if g.active_column is not None else None
    return active_name == target_name, f"active={active_name}"


def check_bound_pair_partners_move_opposite(GameClass) -> tuple[bool, str]:
    """In L2, shifting bound col_l2_a by +1 drives partner col_l2_b by -1."""
    g = GameClass()
    g.full_reset()
    g.set_level(1)  # L2 (zero-indexed)
    # Setup: select col_l2_a.
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 12, "y": 14}))
    a_before = g.column_positions["col_l2_a"]
    b_before = g.column_positions["col_l2_b"]
    # Action under test.
    g.perform_action(ActionInput(id=GameAction.ACTION1, data={}))
    a_after = g.column_positions["col_l2_a"]
    b_after = g.column_positions["col_l2_b"]
    delta_a = (a_after - a_before) % 12
    delta_b = (b_after - b_before) % 12
    passed = delta_a == 1 and delta_b == 11
    return passed, f"da={delta_a} db={delta_b}"


def check_action5_advances_scan_line_in_l3(GameClass) -> tuple[bool, str]:
    """ACTION5 in L3 advances the scan-line index by 1."""
    g = GameClass()
    g.full_reset()
    g.set_level(2)  # L3
    idx_before = g.scan_line_idx
    g.perform_action(ActionInput(id=GameAction.ACTION5, data={}))
    idx_after = g.scan_line_idx
    return idx_after == (idx_before + 1) % len(g.scan_line_rows), f"before={idx_before} after={idx_after}"
