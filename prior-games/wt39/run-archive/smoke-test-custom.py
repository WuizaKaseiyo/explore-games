"""Custom smoke checks for wt39 — one essential mechanic invariant per check."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load_game_class():
    src = Path("prior-games/wt39/wt39.py")
    spec = importlib.util.spec_from_file_location("smoke_wt39", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "Wt39")


def check_right_slides_until_wall(GameClass) -> tuple[bool, str]:
    """RIGHT from L1 start (2, 2) glides east and stops at (8, 2) — one cell west of the wall at (9, 2)."""
    g = GameClass()
    g.set_level(0)
    pawn = g._pawn()
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    observed = f"x={pawn.x} y={pawn.y}"
    return (pawn.x == 8 and pawn.y == 2), observed


def check_bumper_deflects_right_to_down(GameClass) -> tuple[bool, str]:
    """L2 bumper at (10, 2) deflects an east-going slide southward; pawn ends at (10, 6)."""
    g = GameClass()
    g.set_level(1)
    pawn = g._pawn()
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    observed = f"x={pawn.x} y={pawn.y}"
    return (pawn.x == 10 and pawn.y == 6), observed


def check_thaw_cracks_after_one_pass(GameClass) -> tuple[bool, str]:
    """L3 thaw at (4, 8) is replaced by a cracked sprite after a slide passes through it."""
    g = GameClass()
    g.set_level(2)
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)  # RIGHT to (10, 6) via bumper
    g.perform_action(ActionInput(id=GameAction.ACTION3), raw=True)  # LEFT to (4, 6)
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)  # DOWN through thaw to (4, 10)
    cracked = [s for s in g.current_level.get_sprites_by_tag("cracked") if s.x == 4 and s.y == 8]
    observed = f"cracked-at-4-8 count={len(cracked)}"
    return len(cracked) == 1, observed


def check_lose_at_budget(GameClass) -> tuple[bool, str]:
    """Press RIGHT 30 times on L1 (budget=30). The 30th wins (witness is shorter), so test L2 instead with a non-progress loop:
    on L1 a single RIGHT/DOWN solves; instead test that pressing UP from start consumes budget without progress and the level resets when budget runs out.
    Approach: spam UP (which goes to (2, 1)) then DOWN (which goes back to (2, 12)) for budget+1 actions on L1 starting fresh — should hit lose."""
    g = GameClass()
    g.set_level(0)
    budget = g._step_budget
    # Alternating UP/DOWN ping-pongs the pawn between (2, 1) and (2, 12); never reaches goal at (8, 7).
    for i in range(budget):
        action_id = GameAction.ACTION1 if i % 2 == 0 else GameAction.ACTION2
        g.perform_action(ActionInput(id=action_id), raw=True)
    observed = f"state after exhausting budget: {g._state.name}, steps={g._steps_remaining}"
    return g._state.name == "GAME_OVER", observed


if __name__ == "__main__":
    GameClass = _load_game_class()
    for fn in [
        check_right_slides_until_wall,
        check_bumper_deflects_right_to_down,
        check_thaw_cracks_after_one_pass,
        check_lose_at_budget,
    ]:
        passed, obs = fn(GameClass)
        marker = "✅" if passed else "❌"
        print(f"{marker} {fn.__name__}: {obs}")
