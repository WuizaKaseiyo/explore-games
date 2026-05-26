"""Custom smoke checks for pn5d. Each is single-action, single-assertion."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
from novaengine import ActionInput, GameAction


def _load_game_class():
    src = Path("prior-games/pn5d/pn5d.py")
    spec = importlib.util.spec_from_file_location("smoke_pn5d", src)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod.Pn5d


def check_pour_raises_connected_group():
    """ACTION5 raises every vessel in the cursor's connected group by 1."""
    GameClass = _load_game_class()
    g = GameClass()
    g.set_level(0)  # L1: 2 vessels with fixed-open valve, both at level 0
    levels_before = [v["level"] for v in g._vessels]
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    levels_after = [v["level"] for v in g._vessels]
    expected = [b + 1 for b in levels_before]
    return levels_after == expected, f"before={levels_before} after={levels_after}"


def check_click_toggles_valve():
    """ACTION6 on a non-fixed valve flips its is_open flag."""
    GameClass = _load_game_class()
    g = GameClass()
    g.set_level(1)  # L2: 2 toggleable valves, both initially open
    valve = g._valves[0]
    before = valve["is_open"]
    # Click center of valve_open sprite at (24, 18). It's 2-wide x 4-tall.
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 19}), raw=True
    )
    after = valve["is_open"]
    return after != before, f"before={before} after={after}"


def check_overflow_cap_clips_surface():
    """At L3, pouring with all valves open clips C's surface to its cap (= 2)."""
    GameClass = _load_game_class()
    g = GameClass()
    g.set_level(2)  # L3: 4 vessels, 3 valves initially closed, C cap = 2
    # Open all three valves: clicks at (20, 19), (31, 19), (42, 19)
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 20, "y": 19}), raw=True
    )
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 31, "y": 19}), raw=True
    )
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 42, "y": 19}), raw=True
    )
    # Pour 5 times: A, B, D should hit 5; C should clip at 2.
    for _ in range(5):
        g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    c_level = g._vessels[2]["level"]  # vessel C is index 2
    return c_level == 2, f"C level after 5 pours with all valves open = {c_level}"


def check_witness_l1_wins():
    """L1 witness — 4 pours — advances past L1."""
    GameClass = _load_game_class()
    g = GameClass()
    g.set_level(0)
    score_before = g._score
    for _ in range(4):
        g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    return g._score > score_before, f"score {score_before} → {g._score}"


CUSTOM_CHECKS = [
    check_pour_raises_connected_group,
    check_click_toggles_valve,
    check_overflow_cap_clips_surface,
    check_witness_l1_wins,
]


if __name__ == "__main__":
    for fn in CUSTOM_CHECKS:
        try:
            ok, msg = fn()
            tag = "PASS" if ok else "FAIL"
            print(f"{tag} {fn.__name__}: {msg}")
        except Exception as e:
            print(f"ERROR {fn.__name__}: {type(e).__name__}: {e}")
