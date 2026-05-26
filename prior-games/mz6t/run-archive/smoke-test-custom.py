"""Custom smoke checks for `mz6t`.

Each check tests one essential mechanic invariant with ≤5 setup actions
and one boolean assertion. Run alongside the universal smoke checks.
"""

import importlib.util
from pathlib import Path

_SRC = Path("prior-games/mz6t/mz6t.py")
_spec = importlib.util.spec_from_file_location("mz6t_check", _SRC)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

GameClass = _mod.Mz6t

from novaengine import ActionInput, GameAction


def _click(g, x, y):
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y}), raw=True)


def _tick(g):
    g.perform_action(ActionInput(id=GameAction.ACTION5, data={}), raw=True)


def check_click_cycles_state(GameClass):
    """ACTION6 click on a voting cell advances the cell's state by +1 mod 3."""
    g = GameClass()
    g.handle_reset()
    g.set_level(0)
    cell = (0, 0)
    s0 = g._cell_state[cell]
    _click(g, 6, 6)  # cell (col=0, row=0) centre is (6, 6)
    s1 = g._cell_state[cell]
    passed = s1 == (s0 + 1) % 3
    return passed, f"s0={s0} s1={s1}"


def check_tick_propagates_majority(GameClass):
    """ACTION5 tick flips a cell whose 4 neighbours all hold a single
    different colour to that colour (4 ≥ 3 strict-majority)."""
    g = GameClass()
    g.handle_reset()
    g.set_level(0)  # L1 has the (2,2) cell with 4 state-1 neighbours initially
    s_before = g._cell_state[(2, 2)]
    _tick(g)
    # L1 target requires both (1,1) AND (2,2) at state 1; (1,1) wasn't clicked
    # so the level does NOT advance. (2,2) should however have flipped state 1.
    s_after = g._cell_state[(2, 2)]
    passed = s_before == 0 and s_after == 1
    return passed, f"s_before={s_before} s_after={s_after}"


def check_anchor_locks_on_target(GameClass):
    """Clicking an anchor cell to its target colour locks it (subsequent
    clicks no-op)."""
    g = GameClass()
    g.handle_reset()
    g.set_level(2)  # L3 has anchor at (2,2) target state 2
    anchor_cell = (2, 2)
    _click(g, 22, 22)  # state 0 -> 1
    _click(g, 22, 22)  # state 1 -> 2 == target -> LOCK
    locked = anchor_cell in g._anchor_locked
    state_after_lock = g._cell_state[anchor_cell]
    # Click again - should be no-op because anchor is locked.
    _click(g, 22, 22)
    state_after_extra_click = g._cell_state[anchor_cell]
    passed = locked and state_after_lock == 2 and state_after_extra_click == 2
    return passed, f"locked={locked}, state_after_lock={state_after_lock}, after_extra_click={state_after_extra_click}"


def check_win_fires_only_on_tick(GameClass):
    """Click-only sequences cannot win; only ACTION5 fires the win check."""
    g = GameClass()
    g.handle_reset()
    g.set_level(0)
    score_before = g._score
    # On L1, click (1,1) and (2,2) directly to target — without tick this should NOT win.
    _click(g, 14, 14)  # cell (1,1) -> state 1
    _click(g, 22, 22)  # cell (2,2) -> state 1
    score_after_clicks = g._score
    passed = score_after_clicks == score_before  # no advance from clicks alone
    return passed, f"score_before={score_before} score_after_clicks={score_after_clicks}"


CHECKS = [
    check_click_cycles_state,
    check_tick_propagates_majority,
    check_anchor_locks_on_target,
    check_win_fires_only_on_tick,
]


if __name__ == "__main__":
    for fn in CHECKS:
        try:
            passed, observed = fn(GameClass)
            status = "PASS" if passed else "FAIL"
            print(f"{status} {fn.__name__}: {observed}")
        except Exception as e:
            print(f"ERROR {fn.__name__}: {e!r}")
