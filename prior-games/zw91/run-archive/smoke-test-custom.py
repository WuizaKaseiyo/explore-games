"""Custom smoke checks for zw91 — 4 essential mechanic invariants.

Each check follows the strict template:
- ≤ 1s wall-clock, fully deterministic.
- ≤ 5 setup actions, ONE action under test, ONE boolean assertion.
"""
from novaengine import ActionInput, GameAction


def act(n):
    return ActionInput(id=GameAction.from_id(n))


def check_arrow_moves_avatar(GameClass) -> tuple[bool, str]:
    """ACTION4 (RIGHT) advances the avatar's top-left x by exactly 4 cells."""
    g = GameClass()
    g.set_level(0)
    x0, y0 = g._avatar_top_left()
    g.perform_action(act(4), raw=True)
    x1, y1 = g._avatar_top_left()
    return (x1 == x0 + 4 and y1 == y0), f"({x0},{y0})->({x1},{y1})"


def check_action5_grows_size(GameClass) -> tuple[bool, str]:
    """ACTION5 from size 1 in open space inflates to size 2."""
    g = GameClass()
    g.set_level(0)
    s0 = g.size
    g.perform_action(act(5), raw=True)
    return g.size == s0 + 1, f"size {s0}->{g.size}"


def check_action_counter_increments(GameClass) -> tuple[bool, str]:
    """Every action advances the engine's _action_count by 1."""
    g = GameClass()
    g.set_level(0)
    n0 = g._action_count
    g.perform_action(act(1), raw=True)
    return g._action_count == n0 + 1, f"counter {n0}->{g._action_count}"


def check_lose_at_budget(GameClass) -> tuple[bool, str]:
    """When the step counter exhausts, the game state becomes GAME_OVER."""
    g = GameClass()
    g.set_level(0)
    budget = g._step_hud.max_steps
    for _ in range(budget + 2):
        g.perform_action(act(3), raw=True)  # LEFT — bumps perimeter wall, no progress
    return g._state.name == "GAME_OVER", f"state={g._state.name} after budget+2"
