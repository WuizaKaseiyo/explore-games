"""Custom smoke checks for tg6w.

Each check tests ONE essential mechanic invariant of settle-pile-tilt with
≤ 5 setup actions, ONE action under test, and ONE boolean assertion.
"""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load_game_class():
    src = Path("prior-games/tg6w/tg6w.py")
    spec = importlib.util.spec_from_file_location("smoke_tg6w", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "Tg6w")


GameClass = _load_game_class()


def check_down_advances_l1():
    """L1 ACTION2 (DOWN) slides both yellow blocks to the bottom row, which
    matches both yellow targets and triggers `next_level()`. Tests the M1
    slide-to-end rule end-to-end via the level transition (which only fires
    when every block lands on its same-coloured target after the slide)."""
    g = GameClass()
    g.set_level(0)
    idx_before = g._current_level_index
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)
    idx_after = g._current_level_index
    observed = f"current_level_index: before={idx_before} after={idx_after}"
    passed = idx_after == idx_before + 1
    return passed, observed


def check_no_op_action_consumes_step():
    """L1 ACTION1 (UP) at row 1 produces no block movement (border above)
    but still ticks the step counter — tests that wasted presses cost."""
    g = GameClass()
    g.set_level(0)
    used_before = g._steps_used
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    used_after = g._steps_used
    observed = f"_steps_used: before={used_before} after={used_after}"
    passed = used_after == used_before + 1
    return passed, observed


def check_rim_blocks_wrong_colour():
    """L2 ACTION2 (DOWN): yellow at (3, 1) base (9, 3) passes its yellow-rim
    and lands at (3, 5) base (9, 15); orange at (5, 1) base (15, 3) passes
    its orange-rim and lands at (5, 5) base (15, 15). Tests M2: each block
    crosses ITS rim and only ITS rim."""
    g = GameClass()
    g.set_level(1)
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)
    blocks = g.current_level.get_sprites_by_tag("block")
    cells = sorted((b.name, b.x, b.y) for b in blocks)
    observed = f"after DOWN = {cells}"
    passed = cells == [("block_orange", 15, 15), ("block_yellow", 9, 15)]
    return passed, observed


def check_sticky_catches_first_crosser():
    """L3 witness setup [LEFT, DOWN, RIGHT]: yellow slides through (3, 5)
    sticky-pad on the RIGHT press and gets fixed there (in self._fixed_block_cells).
    Tests M3: sticky catches the first block to slide ACROSS it."""
    g = GameClass()
    g.set_level(2)
    g.perform_action(ActionInput(id=GameAction.ACTION3), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    fixed = sorted(g._fixed_block_cells)
    observed = f"_fixed_block_cells = {fixed}"
    # (3, 5) lattice = (9, 15) base — yellow target / sticky cell.
    passed = (9, 15) in g._fixed_block_cells
    return passed, observed


if __name__ == "__main__":
    checks = [
        check_down_advances_l1,
        check_no_op_action_consumes_step,
        check_rim_blocks_wrong_colour,
        check_sticky_catches_first_crosser,
    ]
    for c in checks:
        passed, obs = c()
        status = "PASS" if passed else "FAIL"
        print(f"  {c.__name__}: {status} — {obs}")
