"""Custom smoke-test checks for bw7k. Each function returns (passed, observed).

Run with the GameClass injected from the smoke-test runner."""

from novaengine import ActionInput, GameAction


def check_up_moves_actor(GameClass, mod):
    """Pressing UP moves the actor's y-coordinate by -STRIDE (Pattern A)."""
    g = GameClass()
    g.set_level(0)
    actor = g.current_level.get_sprites_by_tag("actor")[0]
    y0 = actor.y
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    return actor.y == y0 - mod.STRIDE, f"y0={y0} y1={actor.y}"


def check_anchor_spawns_shade(GameClass, mod):
    """Stepping onto anchor_red spawns exactly one shade_red sprite (Pattern C-ish)."""
    g = GameClass()
    g.set_level(0)
    # 5 setup actions (within the cap of 5): walk UP×5 to land on anchor_red at (12, 36).
    for _ in range(5):
        g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    shades = g.current_level.get_sprites_by_tag("shade_red")
    return len(shades) == 1, f"shade_red count={len(shades)}"


def check_shade_lands_at_target_l1(GameClass, mod):
    """In L1, the spawned shade rests at target_red's cell (Pattern F-style minimal solve)."""
    g = GameClass()
    g.set_level(0)
    for _ in range(5):
        g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    s = g.current_level.get_sprites_by_tag("shade_red")[0]
    t = g.current_level.get_sprites_by_tag("target_red")[0]
    return (s.x, s.y) == (t.x, t.y), f"shade=({s.x},{s.y}) target=({t.x},{t.y})"


def check_l1_witness_wins(GameClass, mod):
    """L1's 13-UP witness advances the engine past L1 (Pattern F)."""
    g = GameClass()
    g.handle_reset()
    score_before = g._score
    for _ in range(13):
        g.perform_action(ActionInput(id=GameAction.ACTION1))
    return g._score == 1, f"score before={score_before} after={g._score} state={g._state.name}"
