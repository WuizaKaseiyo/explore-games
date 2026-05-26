"""Custom smoke-test checks for jx5k. Each check returns (passed, observed_string)."""

import sys
from pathlib import Path

import numpy as np

ROOT = Path("/Users/nickhe/Programming/NovaPlay-Agents")
sys.path.insert(0, str(ROOT / "prior-games/jx5k"))

from novaengine import ActionInput, GameAction, InteractionMode  # noqa: E402
from jx5k import Jx5k  # noqa: E402


def _click(g, x, y):
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y}), raw=True)


def _action5(g):
    g.perform_action(ActionInput(id=GameAction.ACTION5, data={}), raw=True)


def check_click_on_node_selects():
    """ACTION6 click on a node with no current selection sets self._selected_node."""
    g = Jx5k()
    g.set_level(0)
    _click(g, 16, 16)  # display (16, 16) -> grid (8, 8) = n_nw
    return g._selected_node == "n_nw", f"selected={g._selected_node}"


def check_pair_click_creates_edge():
    """ACTION6 pair-click on two same-colour nodes creates an edge."""
    g = Jx5k()
    g.set_level(0)
    _click(g, 16, 16)         # select n_nw
    _click(g, 48, 16)         # click n_ne -> create edge
    pair = ("n_ne", "n_nw")
    state = g._edge_state.get(pair, 0)
    return state == 1, f"edge_state[(n_ne, n_nw)]={state}"


def check_action5_cycles_color_at_l2():
    """At L2, ACTION5 on a selected blue node cycles colour to red."""
    g = Jx5k()
    g.set_level(1)            # L2
    # n1 starts blue at grid (16, 5) -> display (32, 10).
    _click(g, 32, 10)
    before = g._node_color["n1"]
    _action5(g)
    after = g._node_color["n1"]
    return (before == 9 and after == 8), f"before={before} after={after}"


def check_l3_double_edge_advances_cycle():
    """At L3, pair-click on an existing edge advances [single -> double]; same node colours."""
    g = Jx5k()
    g.set_level(2)            # L3
    # Recolour n1 (blue->red) and n3 (blue->red) so all 4 nodes are red.
    _click(g, 32, 16); _action5(g)   # n1 (16, 8) -> display (32, 16)
    _click(g, 32, 48); _action5(g)   # n3 (16, 24) -> display (32, 48)
    n0 = (16, 32)
    n2 = (48, 32)
    # Create n0-n2 single
    _click(g, *n0); _click(g, *n2)
    state_after_first = g._edge_state.get(("n0", "n2"), 0)
    # Create n0-n2 double
    _click(g, *n0); _click(g, *n2)
    state_after_second = g._edge_state.get(("n0", "n2"), 0)
    return (state_after_first == 1 and state_after_second == 2), \
        f"after_first={state_after_first} after_second={state_after_second}"


CHECKS = [
    check_click_on_node_selects,
    check_pair_click_creates_edge,
    check_action5_cycles_color_at_l2,
    check_l3_double_edge_advances_cycle,
]


if __name__ == "__main__":
    failures = []
    for check in CHECKS:
        try:
            passed, observed = check()
        except Exception as exc:
            passed, observed = False, f"raised {type(exc).__name__}: {exc}"
        status = "PASS" if passed else "FAIL"
        print(f"{status} {check.__name__}: {observed}")
        if not passed:
            failures.append(check.__name__)
    if failures:
        sys.exit(1)
