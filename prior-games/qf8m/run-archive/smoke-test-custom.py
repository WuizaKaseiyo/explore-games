"""Custom smoke-test checks for qf8m.

Each check is a function returning (passed: bool, observed: str).
Hard constraints per the smoke-test-checks template:
  - ≤ 1 second wall time
  - fully deterministic
  - ≤ 5 setup actions
  - exactly ONE action under test
  - exactly ONE boolean assertion
"""

import importlib.util
import sys
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load_game_class():
    src = Path("prior-games/qf8m/qf8m.py")
    spec = importlib.util.spec_from_file_location("smoke_qf8m_custom", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Qf8m


GameClass = _load_game_class()


def _click_cell(g, col, row):
    px = 2 + col * 8 + 4
    py = 2 + row * 8 + 4
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": px, "y": py}),
        raw=True,
    )


def check_rook_click_flips_row_and_col():
    """One rook click toggles every cell in its row OR col (9 cells total in L1)."""
    g = GameClass()
    g.set_level(0)
    initial_lit = sum(1 for s in g._cell_state.values() if s == 1)
    _click_cell(g, 2, 2)
    after_lit = sum(1 for s in g._cell_state.values() if s == 1)
    return (
        after_lit - initial_lit == 9,
        f"initial_lit={initial_lit} after_lit={after_lit}",
    )


def check_bishop_click_flips_diagonals_only():
    """One bishop click at (1,1) in L2 toggles cells on i-j=0 and i+j=2 (7 cells)."""
    g = GameClass()
    g.set_level(1)  # L2 has bishop tile at (1,1)
    initial_lit = sum(1 for s in g._cell_state.values() if s == 1)
    _click_cell(g, 1, 1)
    after_lit = sum(1 for s in g._cell_state.values() if s == 1)
    return (
        after_lit - initial_lit == 7,
        f"initial_lit={initial_lit} after_lit={after_lit}",
    )


def check_tristate_advances_mod_3():
    """Two flips touching the L3 tri-state cell at (2,2) advance state 0 -> 1 -> 2."""
    g = GameClass()
    g.set_level(2)  # L3 has tri-state at (2,2)
    # Click bishop(1,1): main diagonal i-j=0 contains (2,2) -> first flip.
    _click_cell(g, 1, 1)
    # Click bishop(3,3): main diagonal i-j=0 contains (2,2) -> second flip.
    _click_cell(g, 3, 3)
    return (
        g._cell_state[(2, 2)] == 2,
        f"tristate(2,2) state after 2 flips = {g._cell_state[(2, 2)]}",
    )


def check_l1_witness_advances_level():
    """L1's named 2-action witness advances past level 1."""
    g = GameClass()
    g.handle_reset()
    score_before = g._score
    _click_cell(g, 1, 1)
    _click_cell(g, 3, 3)
    return (
        g._score == score_before + 1,
        f"score before={score_before} after={g._score}",
    )


CUSTOM_CHECKS = [
    check_rook_click_flips_row_and_col,
    check_bishop_click_flips_diagonals_only,
    check_tristate_advances_mod_3,
    check_l1_witness_advances_level,
]


if __name__ == "__main__":
    for fn in CUSTOM_CHECKS:
        passed, observed = fn()
        status = "PASS" if passed else "FAIL"
        print(f"{status} | {fn.__name__} | {observed}")
        if not passed:
            sys.exit(1)
