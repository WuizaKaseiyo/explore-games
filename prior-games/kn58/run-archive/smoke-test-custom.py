"""Custom smoke checks for kn58."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load_game_class():
    src = Path("prior-games/kn58/kn58.py")
    spec = importlib.util.spec_from_file_location("smoke_kn58", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "Kn58")


GameClass = _load_game_class()


def _click(g, cx, cy):
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": cx * 4 + 2, "y": cy * 4 + 2}),
        raw=True,
    )


def check_anchor_pull_orange() -> tuple[bool, str]:
    """A click placing an anchor pulls the orange pawn one cell toward the anchor."""
    g = GameClass()
    g.set_level(0)
    pawn = g.current_level.get_sprites_by_name("pawn_orange")[0]
    x0 = pawn.x
    _click(g, 11, 7)  # anchor at logical (11, 7); pawn at (4, 7) → expect move east to (5, 7).
    moved_east_one_cell = pawn.x == x0 + 4
    return moved_east_one_cell, f"x0={x0} x1={pawn.x} (CELL=4)"


def check_match_sticks_pawn() -> tuple[bool, str]:
    """When a pawn lands on its same-colour target, the pawn enters stuck state."""
    g = GameClass()
    g.set_level(0)
    # Place anchor at (11, 7) and pull orange 7 times.
    for _ in range(7):
        _click(g, 11, 7)
    # After level transition, _current_level_index advances. Confirm via that.
    advanced_to_l2 = g._current_level_index == 1
    return advanced_to_l2, f"level after 7 pulls = {g._current_level_index}"


def check_pawn_pawn_collision_blocks() -> tuple[bool, str]:
    """L3: orange pawn cannot enter the cell occupied by the pre-stuck purple pawn."""
    g = GameClass()
    g.set_level(2)
    orange = g.current_level.get_sprites_by_name("pawn_orange")[0]
    # Orange starts at logical (3, 8). Drive east via anchor at (12, 8).
    # After 4 pulls orange is at (7, 8). Next pull east would be to (8, 8) where purple is stuck.
    for _ in range(5):
        _click(g, 12, 8)
    # After 5 pulls without any wall blocker, orange WOULD reach (8, 8) absent collision.
    # With M4: orange tries east (blocked by stuck purple), no secondary axis (Δy=0). Stays at (7, 8).
    blocked_at_seven = orange.x == 7 * 4 and orange.y == 8 * 4
    return blocked_at_seven, f"orange at logical ({orange.x // 4}, {orange.y // 4}) after 5 east-pulls"


def check_lose_at_budget() -> tuple[bool, str]:
    """The step budget eventually triggers a lose state."""
    g = GameClass()
    g.set_level(0)
    # Click on a cell that does not pull the pawn at all (e.g., on the pawn itself).
    # Pawn is at logical (4, 7). Click at (4, 7) places anchor on pawn — pawn already there, doesn't move.
    # 30 such clicks should exhaust the L1 budget.
    for _ in range(g.step_budget + 1):
        _click(g, 4, 7)
        if g._state.name in ("GAME_OVER", "WIN"):
            break
    # GAME_OVER from lose() or any non-NOT_PLAYED non-WIN state.
    is_lost = g._state.name == "GAME_OVER"
    return is_lost, f"final state = {g._state.name} after {g.step_budget + 1} no-pull clicks"


CHECKS = [
    check_anchor_pull_orange,
    check_match_sticks_pawn,
    check_pawn_pawn_collision_blocks,
    check_lose_at_budget,
]


if __name__ == "__main__":
    for c in CHECKS:
        passed, observed = c()
        marker = "PASS" if passed else "FAIL"
        print(f"{marker}: {c.__name__} — {observed}")
