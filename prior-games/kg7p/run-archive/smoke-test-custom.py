"""Custom smoke checks for kg7p (beam-tether-haul)."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load_game_class():
    src = Path("prior-games/kg7p/kg7p.py")
    spec = importlib.util.spec_from_file_location("smoke_kg7p", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Kg7p


def check_east_moves_avatar(GameClass):
    """ACTION4 (east) moves the avatar one cell (4 px) to the east."""
    g = GameClass()
    g.set_level(0)
    x0 = g.avatar.x
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    return g.avatar.x == x0 + 4, f"x0={x0} x1={g.avatar.x}"


def check_action5_toggles_beam(GameClass):
    """ACTION5 toggles the beam state."""
    g = GameClass()
    g.set_level(0)
    b0 = g.beam_on
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    return g.beam_on != b0, f"before={b0} after={g.beam_on}"


def check_beam_couples_block_on_walk(GameClass):
    """After walking east up to the cell before a block with beam on, the next east walk couples it."""
    g = GameClass()
    g.set_level(0)
    # Setup: turn beam on, walk east 4 times — avatar (3,8) -> (7,8), couple block at (8,8) on step 5.
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)  # beam on
    for _ in range(4):
        g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    coupled = g.coupled_block is not None
    return coupled, f"coupled={coupled} block_x={g.coupled_block.x if g.coupled_block else None}"


def check_lose_at_budget(GameClass):
    """Exhausting the step budget on L1 triggers the lose state."""
    g = GameClass()
    g.set_level(0)
    budget = g.level_budget
    # Send budget+1 action5 toggles (does not advance towards the win)
    for _ in range(budget + 1):
        g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    return g._state.name in ("GAME_OVER",), f"state_after_budget+1={g._state.name}"


if __name__ == "__main__":
    GameClass = _load_game_class()
    for fn in (
        check_east_moves_avatar,
        check_action5_toggles_beam,
        check_beam_couples_block_on_walk,
        check_lose_at_budget,
    ):
        ok, obs = fn(GameClass)
        print(f"{'PASS' if ok else 'FAIL'} {fn.__name__}: {obs}")
