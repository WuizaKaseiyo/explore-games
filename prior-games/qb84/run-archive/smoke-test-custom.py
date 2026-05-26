"""Custom smoke checks for qb84.

Each check follows the strict template in
`code/smoke-test-checks.md` § Custom checks: instantiate a fresh game,
set a level, perform ≤5 setup actions, perform ONE action under test,
return (bool, observed_str).

Run from repo root via:
    python -c "
    import sys; sys.path.insert(0, 'prior-games/qb84')
    sys.path.insert(0, 'workspace')
    import smoke_test_custom as m
    GameClass = __import__('qb84').Qb84
    for name in m.__all__:
        passed, obs = getattr(m, name)(GameClass)
        print(f'{name}: {\"PASS\" if passed else \"FAIL\"} — {obs}')
    "
"""
from __future__ import annotations

from novaengine import ActionInput, GameAction


def _fire(g, action_id: int) -> None:
    g.perform_action(ActionInput(id=getattr(GameAction, f"ACTION{action_id}")), raw=True)


def check_lift_swaps_colors(GameClass) -> tuple[bool, str]:
    """ACTION1 on a bead with an above-peg swaps the bead and peg body colours."""
    g = GameClass()
    g.perform_action(ActionInput(id=GameAction.RESET), raw=True)
    g.set_level(0)
    bead = g._chain[0]
    peg = g._pegs_above[0]
    bead_before = g._bead_color(bead)
    peg_before = g._peg_color(peg)
    _fire(g, 1)
    bead_after = g._bead_color(bead)
    observed = f"bead {bead_before}->{bead_after} peg {peg_before}->{g._peg_color(peg)}"
    passed = (bead_after == peg_before)
    return passed, observed


def check_sticky_locks_bead(GameClass) -> tuple[bool, str]:
    """After a swap with a sticky peg, the bead's locked flag flips True."""
    g = GameClass()
    g.perform_action(ActionInput(id=GameAction.RESET), raw=True)
    g.set_level(1)
    # Walk cursor 0 -> 2 (B2 has a sticky above-peg).
    _fire(g, 4)
    _fire(g, 4)
    bead = g._chain[2]
    locked_before = g._bead_locked.get(bead, False)
    _fire(g, 1)
    locked_after = g._bead_locked.get(bead, False)
    observed = f"locked before={locked_before} after={locked_after}"
    passed = (locked_after is True and locked_before is False)
    return passed, observed


def check_pair_propagation_sets_neighbour(GameClass) -> tuple[bool, str]:
    """ACTION1 on a pair-A peg propagates the partner peg's colour into the chain neighbour."""
    g = GameClass()
    g.perform_action(ActionInput(id=GameAction.RESET), raw=True)
    g.set_level(2)
    # Walk cursor 0 -> 5 (B5 has pair-A above-peg pg_l3_c, neighbour is B6).
    for _ in range(5):
        _fire(g, 4)
    neighbour = g._chain[6]
    pair_b_color_at_start = g._peg_color(g._pegs_above[6])  # pg_l3_d (pair-B)
    _fire(g, 1)
    neighbour_after = g._bead_color(neighbour)
    observed = f"partner_color_at_start={pair_b_color_at_start} neighbour_after={neighbour_after}"
    passed = (neighbour_after == pair_b_color_at_start)
    return passed, observed


def check_lose_at_budget(GameClass) -> tuple[bool, str]:
    """Exhausting the per-level step counter triggers self.lose()."""
    g = GameClass()
    g.perform_action(ActionInput(id=GameAction.RESET), raw=True)
    g.set_level(0)
    budget = g._max_steps
    # Fire ACTION3 (cursor decrement) repeatedly — always consumes a step.
    # Stop just before the bead colour matches the target by accident.
    for _ in range(budget):
        _fire(g, 3)
    state = g._state
    observed = f"state after {budget} ACTION3s: {state}"
    passed = (state.name == "GAME_OVER")
    return passed, observed


__all__ = [
    "check_lift_swaps_colors",
    "check_sticky_locks_bead",
    "check_pair_propagation_sets_neighbour",
    "check_lose_at_budget",
]
