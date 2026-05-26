"""Custom smoke-test checks for zd7m (cohort-step routing)."""

import importlib.util
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "prior-games/zd7m/zd7m.py"


def _load_game_class():
    spec = importlib.util.spec_from_file_location("smoke_zd7m", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "Zd7m"), mod


def check_cohort_step_moves_all_pawns(GameClass) -> tuple[bool, str]:
    """One DOWN press moves every pawn one cell down on L1."""
    g = GameClass()
    g.set_level(0)
    pawns = g.current_level.get_sprites_by_tag("pawn")
    initial = [(p.name, p.x, p.y) for p in pawns]
    from novaengine import GameAction, ActionInput
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)
    after = [(p.name, p.x, p.y) for p in pawns]
    moved = all(a[2] == b[2] - 1 for a, b in zip(initial, after))
    return moved, f"initial={initial} after={after}"


def check_anchor_blocks_yellow_right(GameClass) -> tuple[bool, str]:
    """The anchor at (7, 10) blocks yellow's RIGHT on L2 while pink moves."""
    g = GameClass()
    g.set_level(1)
    pink = next(p for p in g.current_level.get_sprites_by_tag("pawn") if p.name == "pawn_pink")
    yellow = next(p for p in g.current_level.get_sprites_by_tag("pawn") if p.name == "pawn_yellow")
    from novaengine import GameAction, ActionInput
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    return (pink.x == 5 and yellow.x == 4), f"pink.x={pink.x} yellow.x={yellow.x}"


def check_portal_teleports_yellow(GameClass) -> tuple[bool, str]:
    """On L3, the four-DOWN sequence after RIGHT × 10 teleports yellow to (17, 17)."""
    g = GameClass()
    g.set_level(2)
    from novaengine import GameAction, ActionInput
    for _ in range(10):
        g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    for _ in range(4):
        g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)
    yellow = next(p for p in g.current_level.get_sprites_by_tag("pawn") if p.name == "pawn_yellow")
    return (yellow.x == 17 and yellow.y == 17), f"yellow=({yellow.x},{yellow.y})"


def check_lose_at_step_budget(GameClass) -> tuple[bool, str]:
    """Pressing UP × budget on L1 (no progress) fires lose at the budget limit."""
    g = GameClass()
    g.set_level(0)
    from novaengine import GameAction, ActionInput, GameState
    budget = g._step_budget
    for _ in range(budget):
        g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
        if g._state == GameState.GAME_OVER:
            break
    return g._state == GameState.GAME_OVER, f"state={g._state.name} action_count={g._action_count}"


CHECKS = [
    ("check_cohort_step_moves_all_pawns", check_cohort_step_moves_all_pawns),
    ("check_anchor_blocks_yellow_right", check_anchor_blocks_yellow_right),
    ("check_portal_teleports_yellow", check_portal_teleports_yellow),
    ("check_lose_at_step_budget", check_lose_at_step_budget),
]


if __name__ == "__main__":
    GameClass, _ = _load_game_class()
    failed = 0
    for name, fn in CHECKS:
        try:
            ok, observed = fn(GameClass)
        except Exception as e:
            ok, observed = False, f"EXCEPTION {type(e).__name__}: {e}"
        status = "PASS" if ok else "FAIL"
        print(f"{status}  {name}: {observed}")
        if not ok:
            failed += 1
    sys.exit(0 if failed == 0 else 1)
