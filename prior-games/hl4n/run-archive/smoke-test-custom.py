"""Custom smoke checks for hl4n — exercises the row-tint, col-override, and brighter-wins invariants."""

import importlib.util
from pathlib import Path

SRC = Path("prior-games/hl4n/hl4n.py")
spec = importlib.util.spec_from_file_location("smoke_hl4n", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = mod.Hl4N

from novaengine import ActionInput, GameAction


def _click(g, x, y):
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y}))


def check_row_marker_click_recolors_row():
    """Clicking a row marker advances the row tint by exactly one step in TINT_CYCLE."""
    g = GameClass()
    g.set_level(0)
    r = 3
    before = g.row_tints[r]
    _click(g, 4, 8 + 6 * r + 2)  # click center of row marker for row 3
    after = g.row_tints[r]
    expected_after = mod.TINT_CYCLE[(mod.TINT_CYCLE.index(before) + 1) % len(mod.TINT_CYCLE)]
    return after == expected_after, f"row_tints[{r}]: before={before} after={after} expected={expected_after}"


def check_l2_column_overrides_row():
    """In L2 (rule=1), a non-background column tint overrides the row tint at every cell of that column."""
    g = GameClass()
    g.set_level(1)
    # Set row 3 to red (8) — 1 click on row marker 3
    _click(g, 4, 8 + 6 * 3 + 2)
    # Cell (5, 3) should now show red
    cell = g._cells_by_pos[(5, 3)]
    assert int(cell.pixels[0, 0]) == 8, f"row_tints[3] = 8 expected, cell (5,3) shows {int(cell.pixels[0,0])}"
    # Now set column 5 to yellow (11) — 2 clicks on col marker 5
    _click(g, 8 + 6 * 5 + 2, 4)
    _click(g, 8 + 6 * 5 + 2, 4)
    # Cell (5, 3) should now show yellow (column overrides row)
    after = int(cell.pixels[0, 0])
    return after == 11, f"after col_5=yellow override at cell(5,3): expected 11 got {after}"


def check_l3_brighter_wins_row_dominates():
    """In L3 (rule=2), a brighter row tint wins over a dimmer column tint at the cell."""
    g = GameClass()
    g.set_level(2)
    # Set col_2 to red (8) — 1 click
    _click(g, 8 + 6 * 2 + 2, 4)
    cell = g._cells_by_pos[(2, 3)]
    assert int(cell.pixels[0, 0]) == 8, f"col_2=8 expected at cell(2,3), got {int(cell.pixels[0,0])}"
    # Set row_3 to green (14) — 3 clicks
    _click(g, 4, 8 + 6 * 3 + 2)
    _click(g, 4, 8 + 6 * 3 + 2)
    _click(g, 4, 8 + 6 * 3 + 2)
    # Cell (2, 3) should now show green (brighter wins: max(14, 8) = 14)
    after = int(cell.pixels[0, 0])
    return after == 14, f"row_3=14 brighter than col_2=8: cell(2,3) expected 14 got {after}"


def check_l1_minimal_solve():
    """The spec's L1 witness sequence advances past L1."""
    g = GameClass()
    g.set_level(0)
    _click(g, 4, 20)  # row 2 -> 8
    for _ in range(2):
        _click(g, 4, 32)  # row 4 -> 11
    for _ in range(3):
        _click(g, 4, 44)  # row 6 -> 14
    return g._current_level_index == 1, f"after L1 witness: level_index={g._current_level_index}"


CHECKS = [
    check_row_marker_click_recolors_row,
    check_l2_column_overrides_row,
    check_l3_brighter_wins_row_dominates,
    check_l1_minimal_solve,
]


if __name__ == "__main__":
    for fn in CHECKS:
        try:
            passed, observed = fn()
        except Exception as e:
            passed, observed = False, f"raised {type(e).__name__}: {e}"
        marker = "PASS" if passed else "FAIL"
        print(f"{marker} {fn.__name__}: {observed}")
