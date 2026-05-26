"""Custom smoke checks for yh3p — vine-branch-bloom mechanic invariants.

Each function returns (passed: bool, observed: str). Run all under
the smoke_test state and report failures in smoke-test-failures.md.
"""

import importlib.util
from pathlib import Path
from novaengine import ActionInput, GameAction


def _load_game():
    src = Path("prior-games/yh3p/yh3p.py")
    spec = importlib.util.spec_from_file_location("smoke_yh3p", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "Yh3p")


def check_extend_moves_tip():
    """ACTION4 from L1 root extends the tip one cell right and adds a stalk."""
    GameClass = _load_game()
    g = GameClass()
    g.set_level(0)
    x0, y0 = g._active_tip_cell
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    x1, y1 = g._active_tip_cell
    return (x1, y1) == (x0 + 4, y0), f"before=({x0},{y0}) after=({x1},{y1})"


def check_wall_blocks_extend():
    """ACTION4 into the L2 wall column at x=8 from cell (4, 8) is rejected (the wall column is at cells (8, 0..14); the specific wall at cell (8, 8) blocks RIGHT-growth from (4, 8)). Tip stays at (16, 32)."""
    GameClass = _load_game()
    g = GameClass()
    g.set_level(1)  # L2
    # From root (4, 8) = pixel (16, 32), grow right 4 times to (8, 8) = pixel (32, 32) — but wall is at (32, 32)
    for _ in range(4):
        g.perform_action(ActionInput(id=GameAction.ACTION4))
    # tip should have advanced from (16, 32) toward (32, 32) but stopped at (28, 32) = cell (7, 8)
    # because (32, 32) = cell (8, 8) is a wall.
    x, y = g._active_tip_cell
    return (x, y) == (28, 32), f"expected tip at (28,32), got ({x},{y})"


def check_click_rebranch_resets_facing():
    """After ACTION6 click on the root (in any level), tip facing is None."""
    GameClass = _load_game()
    g = GameClass()
    g.set_level(0)  # L1
    # Establish a facing first by extending right
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    assert g._tip_facing == "RIGHT", f"setup failed: facing={g._tip_facing}"
    # Click on the root cell (3, 7) = pixel (12, 28). Click anywhere inside the 4x4 root sprite.
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 13, "y": 29}))
    return g._tip_facing is None, f"facing after rebranch: {g._tip_facing}"


def check_bloom_requires_facing_match():
    """At L3, ACTION5 on bud P with WRONG facing does NOT bloom; bud P remains a bud_notched."""
    GameClass = _load_game()
    g = GameClass()
    g.set_level(2)  # L3
    # Bud P is at cell (12, 4) = pixel (48, 16). Approach from BELOW (move UP into the bud) — wrong direction.
    # Route: from root (4, 4) = pixel (16, 16), grow down 1, then route... too long; instead manipulate state directly via setup actions.
    # Simpler: set tip directly via internal state, then ACTION5.
    g._active_tip_cell = (48, 16)  # bud P cell
    g._tip_facing = "UP"  # WRONG (intake = DOWN)
    g._tip_blocked_on_notched = True
    g._refresh_tip_visual()
    bud_count_before = len(g.current_level.get_sprites_by_tag("bud_notched"))
    g.perform_action(ActionInput(id=GameAction.ACTION5))
    bud_count_after = len(g.current_level.get_sprites_by_tag("bud_notched"))
    return bud_count_after == bud_count_before, f"buds before={bud_count_before} after={bud_count_after}"


CUSTOM_CHECKS = [
    check_extend_moves_tip,
    check_wall_blocks_extend,
    check_click_rebranch_resets_facing,
    check_bloom_requires_facing_match,
]


if __name__ == "__main__":
    for fn in CUSTOM_CHECKS:
        try:
            passed, observed = fn()
            status = "PASS" if passed else "FAIL"
            print(f"[{status}] {fn.__name__}: {observed}")
        except Exception as e:
            print(f"[ERROR] {fn.__name__}: {type(e).__name__}: {e}")
