"""Custom smoke checks for lv4k.

Each check follows the strict template in
`skills/code/smoke-test-checks.md` § Custom checks: ≤ 5 setup actions,
ONE action under test, ONE boolean assertion, fully deterministic.
"""

from novaengine import ActionInput, GameAction


def _click_at(g, x: int, y: int):
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y}), raw=True
    )


def check_click_selects_tray_weight(GameClass):
    """Click on a tray weight selects it (the modal verb-1 of lv4k)."""
    g = GameClass()
    g.set_level(0)
    selected_before = g.selected_weight
    # ACTION under test: click tray slot at (8, 47) — first m1 in the L1 tray.
    _click_at(g, 8, 47)
    selected_after = g.selected_weight
    observed = (
        f"selected before={selected_before!r}, after={selected_after!r}"
    )
    return (selected_before is None and selected_after is not None), observed


def check_place_changes_torque(GameClass):
    """Placing a mass-1 weight at arm -2 changes torque from 0 to -2."""
    g = GameClass()
    g.set_level(0)
    # Setup (2 actions): select first tray weight at (8, 47).
    _click_at(g, 8, 47)
    torque_before = g._compute_torque()
    # ACTION under test: place at arm -2 (x=16).
    _click_at(g, 16, 26)
    torque_after = g._compute_torque()
    observed = f"torque before={torque_before}, after={torque_after}"
    return (torque_before == 0 and torque_after == -2), observed


def check_passenger_displaces_on_high_tilt(GameClass):
    """L3 passenger shifts one slot when |tilt_level| >= 2 after a placement."""
    g = GameClass()
    g.set_level(2)
    passenger_before = g.passenger_arm  # +2 by spec
    # Setup (1 action): select an m2 from the tray (at tray-x=12).
    _click_at(g, 12, 47)
    # ACTION under test: place m2 at arm -3 (x=8). torque = -6, level = -2 → displace.
    _click_at(g, 8, 26)
    passenger_after = g.passenger_arm
    observed = f"passenger before={passenger_before}, after={passenger_after}"
    return (passenger_before == 2 and passenger_after == 1), observed


def check_l1_minimal_solve_advances(GameClass):
    """L1's 4-action witness solution advances to L2."""
    g = GameClass()
    g.set_level(0)
    # Setup (3 actions): select m1, place at arm -2, select m1#2.
    _click_at(g, 8, 47)
    _click_at(g, 16, 26)
    _click_at(g, 20, 47)
    level_before = g._current_level_index
    # ACTION under test: place m1#2 at arm +2 (x=48). Torque = 0 → win → advance.
    _click_at(g, 48, 26)
    level_after = g._current_level_index
    observed = f"level before={level_before}, after={level_after}"
    return (level_before == 0 and level_after == 1), observed
