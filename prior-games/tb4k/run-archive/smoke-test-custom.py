"""Custom mechanic-specific smoke checks for tb4k."""

from novaengine import ActionInput, GameAction


def check_east_tumble_changes_state(GameClass):
    """ACTION4 (east) from standing must produce lying_h state."""
    g = GameClass()
    g.set_level(0)
    state_before = g.brick_state
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    passed = state_before == "standing" and g.brick_state == "lying_h"
    return passed, f"before={state_before} after={g.brick_state}"


def check_two_east_tumbles_shift_anchor_by_2(GameClass):
    """Two ACTION4 tumbles from standing shift the standing anchor by +2 cells east."""
    g = GameClass()
    g.set_level(0)
    cx0, cy0 = g.brick_cell
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    cx1, cy1 = g.brick_cell
    passed = g.brick_state == "standing" and cx1 == cx0 + 2 and cy1 == cy0
    return passed, f"start=({cx0},{cy0}) after_two_E=({cx1},{cy1}) state={g.brick_state}"


def check_hole_kill_decrements_lives_and_respawns(GameClass):
    """Driving the brick onto a hole at L2 decrements lives by 1 and resets brick to start."""
    g = GameClass()
    g.set_level(1)  # L2
    start = g.start_cell
    lives0 = g.lives_remaining
    # 4 east tumbles → standing at (6, 4); one more E → lying-h [(6,4),(7,4)] both solid;
    # one more E → standing (8, 4) which is a hole → death.
    for _ in range(6):
        g.perform_action(ActionInput(id=GameAction.ACTION4))
    passed = g.lives_remaining == lives0 - 1 and g.brick_cell == start
    return passed, f"lives0={lives0} lives1={g.lives_remaining} cell={g.brick_cell} start={start}"


def check_l1_witness_advances(GameClass):
    """The spec's L1 witness (8E + 8S) must advance the engine past L1."""
    g = GameClass()
    g.set_level(0)
    for _ in range(8):
        g.perform_action(ActionInput(id=GameAction.ACTION4))
    for _ in range(8):
        g.perform_action(ActionInput(id=GameAction.ACTION2))
    passed = g._current_level_index == 1
    return passed, f"level_after_witness={g._current_level_index} brick={g.brick_state}@{g.brick_cell}"


CUSTOM_CHECKS = [
    check_east_tumble_changes_state,
    check_two_east_tumbles_shift_anchor_by_2,
    check_hole_kill_decrements_lives_and_respawns,
    check_l1_witness_advances,
]
