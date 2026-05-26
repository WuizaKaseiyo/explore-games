"""Custom smoke-test checks for game yf3h."""

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
    spec = importlib.util.spec_from_file_location(f"smoke_{GAME_ID}", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, PASCAL)


GameClass = _load_class()


def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2


def check_action_counter_increments() -> tuple[bool, str]:
    """ACTION6 increments _action_count by 1."""
    g = GameClass()
    g.set_level(0)
    n0 = g._action_count
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True
    )
    return g._action_count == n0 + 1, f"before={n0} after={g._action_count}"


def check_arm_emitter_toggle() -> tuple[bool, str]:
    """Clicking the L1 emitter at its grid centre toggles its arm-state.
    Two consecutive clicks return to the disarmed state."""
    g = GameClass()
    g.set_level(0)
    em = g.current_level.get_sprites_by_tag("emitter")[0]
    fx, fy = _grid_to_display_px(g.current_level.grid_size, em.x + 2, em.y + 2)
    # First click: arm
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True
    )
    armed_after_1 = em in g._armed_emitters
    # Second click: disarm
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True
    )
    armed_after_2 = em in g._armed_emitters
    ok = armed_after_1 and not armed_after_2
    return ok, f"after_click1={armed_after_1} after_click2={armed_after_2}"


def check_phase_delay_tile_toggle() -> tuple[bool, str]:
    """Clicking the L3 phase-delay tile at its grid centre toggles its
    active state."""
    g = GameClass()
    g.set_level(2)
    tiles = g.current_level.get_sprites_by_tag("phase_delay")
    if not tiles:
        return False, "no phase_delay tile in L3"
    tile = tiles[0]
    fx, fy = _grid_to_display_px(g.current_level.grid_size, tile.x + 1, tile.y + 1)
    n_before = len(g._delay_tiles_active)
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True
    )
    n_after = len(g._delay_tiles_active)
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True
    )
    n_after_2 = len(g._delay_tiles_active)
    ok = (n_before == 0 and n_after == 1 and n_after_2 == 0)
    return ok, f"counts={n_before}/{n_after}/{n_after_2}"


def check_l1_minimal_solve() -> tuple[bool, str]:
    """Spec's L1 witness `[arm emitter_red, fire]` advances level."""
    g = GameClass()
    g.set_level(0)
    em = g.current_level.get_sprites_by_tag("emitter")[0]
    fx, fy = _grid_to_display_px(g.current_level.grid_size, em.x + 2, em.y + 2)
    # Action 1: arm emitter (consume 1 step).
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True
    )
    # Action 2: fire — this triggers the multi-tick animation.
    g.perform_action(
        ActionInput(id=GameAction.ACTION5), raw=True
    )
    new_level = g._current_level_index
    # If the engine advanced, _current_level_index should be 1 (or game won).
    advanced = new_level == 1 or g._state.name in ("WIN",)
    return advanced, f"level after solve={new_level} state={g._state.name if hasattr(g, '_state') else '?'}"


CHECKS = [
    check_action_counter_increments,
    check_arm_emitter_toggle,
    check_phase_delay_tile_toggle,
    check_l1_minimal_solve,
]


def main() -> None:
    for check in CHECKS:
        try:
            passed, observed = check()
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] {check.__name__}: {observed}")
        except Exception as e:
            print(f"  [ERR ] {check.__name__}: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
