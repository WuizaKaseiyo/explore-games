"""Custom smoke checks for kp9z."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


REPO_ROOT = Path(__file__).resolve().parents[5]
SRC_PATH = REPO_ROOT / "prior-games/kp9z/kp9z.py"


def _load():
    spec = importlib.util.spec_from_file_location("smoke_kp9z", SRC_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2


def check_drop_increments_source(GameClass):
    """Click on the L1 source increments its grain count by 1."""
    g = GameClass()
    g.set_level(0)
    src_pos = (1, 1)  # L1 source row, col
    before = g.grain_counts[src_pos]
    fx, fy = _grid_to_display_px((64, 64), 27, 27)  # L1 source mid-cell
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}),
        raw=True,
    )
    after = g.grain_counts[src_pos]
    return after == before + 1, f"before={before} after={after}"


def check_l1_minimal_solve(GameClass):
    """L1 witness (4 clicks on source) advances to level 2."""
    g = GameClass()
    g.set_level(0)
    fx, fy = _grid_to_display_px((64, 64), 27, 27)
    for _ in range(4):
        g.perform_action(
            ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}),
            raw=True,
        )
    return g._current_level_index == 1, f"level after solve={g._current_level_index}"


def check_sink_absorbs(GameClass):
    """L2 source A topple delivers grains to sinks without raising sink count."""
    g = GameClass()
    g.set_level(1)  # L2
    fx, fy = _grid_to_display_px((64, 64), 32, 22)  # L2 source A mid-cell
    for _ in range(4):
        g.perform_action(
            ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}),
            raw=True,
        )
    # After source A topples, the north sink (0, 2) and south sink (2, 2)
    # should each have absorbed one grain — count stays at 0.
    sink_count = g.grain_counts[(0, 2)] + g.grain_counts[(2, 2)]
    return sink_count == 0, f"sink_count_total={sink_count}"


def check_redirector_forwards(GameClass):
    """L3 source A topple chain delivers exactly 1 grain to target (3, 1) via redirector at (2, 1)."""
    g = GameClass()
    g.set_level(2)  # L3
    fx, fy = _grid_to_display_px((64, 64), 22, 22)  # L3 source A mid-cell
    for _ in range(4):
        g.perform_action(
            ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}),
            raw=True,
        )
    target_count = g.grain_counts.get((3, 1), -1)
    return target_count == 1, f"target_(3,1)_count={target_count}"


CUSTOM_CHECKS = [
    check_drop_increments_source,
    check_l1_minimal_solve,
    check_sink_absorbs,
    check_redirector_forwards,
]


def main():
    mod = _load()
    GameClass = mod.Kp9z
    print("# Custom checks for kp9z")
    failures = []
    for fn in CUSTOM_CHECKS:
        try:
            passed, observed = fn(GameClass)
            print(f"  {fn.__name__}: {'PASS' if passed else 'FAIL'} ({observed})")
            if not passed:
                failures.append((fn.__name__, observed, fn.__doc__))
        except Exception as e:
            import traceback as tb
            print(f"  {fn.__name__}: RAISED {type(e).__name__}: {e}")
            print(tb.format_exc())
            failures.append((fn.__name__, f"RAISED {type(e).__name__}: {e}", fn.__doc__))
    print(f"\nCustom check failures: {len(failures)}")
    return failures


if __name__ == "__main__":
    main()
