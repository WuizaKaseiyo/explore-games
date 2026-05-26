"""Custom smoke checks for tk6n: boomerang-arc-catch invariants."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load():
    src = Path("prior-games/tk6n/tk6n.py")
    spec = importlib.util.spec_from_file_location("smoke_tk6n", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, getattr(mod, "Tk6n")


def check_action5_launches_boomerang(GameClass):
    """ACTION5 with boomerang held switches phase to outbound."""
    g = GameClass()
    g.set_level(0)
    p0 = g.boomerang_phase
    g.perform_action(ActionInput(id=GameAction.ACTION5))
    return g.boomerang_phase == "outbound", f"before={p0} after={g.boomerang_phase}"


def check_action1_moves_avatar_up(GameClass):
    """ACTION1 moves avatar one cell up."""
    g = GameClass()
    g.set_level(0)
    y0 = g.avatar.y
    g.perform_action(ActionInput(id=GameAction.ACTION1))
    return g.avatar.y == y0 - 1, f"y0={y0} y1={g.avatar.y}"


def check_boomerang_advances_one_cell(GameClass):
    """After throw + one arrow tick, boomerang has advanced exactly one cell."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.ACTION5))
    bx0, by0 = g.boomerang_pos
    g.perform_action(ActionInput(id=GameAction.ACTION1))
    bx1, by1 = g.boomerang_pos
    moved = abs(bx1 - bx0) + abs(by1 - by0)
    return moved == 1, f"moved {moved} cells (from ({bx0},{by0}) to ({bx1},{by1}))"


def check_lose_at_budget(GameClass):
    """Game enters GAME_OVER state after step_budget actions of no progress."""
    g = GameClass()
    g.set_level(0)
    budget = g.steps_remaining
    for _ in range(budget + 2):
        # Press ACTION3 (left) repeatedly; bumps left edge after a few moves.
        g.perform_action(ActionInput(id=GameAction.ACTION3))
        if g._state.name == "GAME_OVER":
            break
    return g._state.name == "GAME_OVER", f"state={g._state.name} after budget+2"


CUSTOM_CHECKS = [
    check_action5_launches_boomerang,
    check_action1_moves_avatar_up,
    check_boomerang_advances_one_cell,
    check_lose_at_budget,
]


def main():
    mod, GameClass = _load()
    print("# tk6n custom smoke checks\n")
    for check in CUSTOM_CHECKS:
        try:
            passed, observed = check(GameClass)
        except Exception as e:
            passed, observed = False, f"EXCEPTION: {type(e).__name__}: {e}"
        marker = "PASS" if passed else "FAIL"
        print(f"- {marker}: {check.__name__} — {observed}")


if __name__ == "__main__":
    main()
