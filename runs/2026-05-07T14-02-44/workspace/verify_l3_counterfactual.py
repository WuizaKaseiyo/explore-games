"""Counterfactual: without engaging the phase-delay tile, can L3 still be won?
Per the spec, the answer must be NO — M3 (phase-delay) is required."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT))

from novaengine import ActionInput, GameAction  # noqa: E402

GAME_ID = "yf3h"
PASCAL = "Yf3h"
SRC = REPO_ROOT / f"prior-games/{GAME_ID}/{GAME_ID}.py"


def _load_class():
    spec = importlib.util.spec_from_file_location(f"verify_{GAME_ID}", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, PASCAL)


def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2


def click_at_grid(g, gx, gy):
    fx, fy = _grid_to_display_px(g.current_level.grid_size, gx, gy)
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True
    )


def fire(g):
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)


GameClass = _load_class()


def run_strategy(label, actions):
    g = GameClass()
    g.set_level(2)  # straight to L3
    for fn in actions:
        fn(g)
    state = g._state.name if hasattr(g, "_state") else "?"
    activated = len(g._activated_resonators)
    print(f"  [{label}] activated={activated}/2  state={state}")
    return state == "WIN"


def main():
    print("Counterfactual L3 strategies (each starts fresh on L3):\n")

    em_red = lambda g: click_at_grid(g, 3, 7)
    em_blue = lambda g: click_at_grid(g, 13, 8)
    em_green = lambda g: click_at_grid(g, 3, 13)
    delay = lambda g: click_at_grid(g, 13, 4)

    # Strategy A: arm everything, fire (NO delay tile)
    won_a = run_strategy(
        "alt-A: arm all 3, fire (no delay)",
        [em_red, em_blue, em_green, fire],
    )
    # Strategy B: arm only red+blue, fire (no delay)
    won_b = run_strategy(
        "alt-B: arm red+blue only, fire (no delay)",
        [em_red, em_blue, fire],
    )
    # Strategy C: arm only green, fire (no delay)
    won_c = run_strategy(
        "alt-C: arm green only, fire (no delay)",
        [em_green, fire],
    )
    # Strategy D: arm everything, fire 3 times in a row (no delay) — see if repetition helps
    won_d = run_strategy(
        "alt-D: arm + fire × 3 (no delay)",
        [em_red, em_blue, em_green, fire,
         em_red, em_blue, em_green, fire,
         em_red, em_blue, em_green, fire],
    )
    # Strategy E (witness): toggle delay, arm 3, fire — control case, must WIN
    won_e = run_strategy(
        "witness: toggle delay, arm 3, fire",
        [delay, em_red, em_blue, em_green, fire],
    )

    print()
    print("=" * 60)
    no_delay_wins = won_a or won_b or won_c or won_d
    if not no_delay_wins and won_e:
        print("  ✓ M3 IS REQUIRED — no no-delay strategy wins; the witness wins.")
    else:
        print(f"  ✗ Counterfactual broken — alt-A={won_a}, alt-B={won_b}, "
              f"alt-C={won_c}, alt-D={won_d}, witness={won_e}")


if __name__ == "__main__":
    main()
