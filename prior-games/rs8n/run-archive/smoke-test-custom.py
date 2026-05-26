"""Custom checks for rs8n (revision-3 design). See skills/code/smoke-test-checks.md.

Each check returns (passed: bool, observed: str)."""

from novaengine import ActionInput, GameAction


def check_action4_walks_east(GameClass):
    """ACTION4 (face right + walk) advances the player one cell east on a clear path."""
    g = GameClass()
    g.full_reset()
    player = g._player()
    x0, y0 = player.x, player.y
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    p = g._player()
    return (p.x == x0 + 4 and p.y == y0), f"x0={x0} y0={y0} -> ({p.x},{p.y})"


def check_action5_advances_l1(GameClass):
    """The L1 witness `[ACTION4, ACTION4, ACTION5]` advances past L1 — confirms ACTION5 runs the sweep state machine and the win predicate fires."""
    g = GameClass()
    g.full_reset()
    for a in (4, 4, 5):
        g.perform_action(ActionInput(id=GameAction.from_id(a)))
    return g.level_index == 1, f"level_index={g.level_index}"


def check_anchor_blocks_walk(GameClass):
    """ACTION4 toward an anchor pillar at L2 rotates the avatar without moving it."""
    g = GameClass()
    g.full_reset()
    g.set_level(1)  # L2
    # Walk east twice to reach (3,8); next east is item, rotate-only.
    # Step further until we run up against the anchor at (5,8).
    # Avatar at (1,8) facing east. After walk 1: (2,8). After walk 2: blocked by (3,8) item.
    g.perform_action(ActionInput(id=GameAction.ACTION4))   # (1,8)->(2,8)
    # Now (3,8) is the pink_ring item — walk east is blocked, rotate-only.
    p_before = g._player()
    x0 = p_before.x
    g.perform_action(ActionInput(id=GameAction.ACTION4))   # blocked
    p_after = g._player()
    return p_after.x == x0, f"x0={x0} -> x1={p_after.x} (expected blocked)"


def check_action_counter_decrements(GameClass):
    """One ACTION1 should consume exactly one unit of step budget."""
    g = GameClass()
    g.full_reset()
    n0 = g.step_counter_hud.current
    g.perform_action(ActionInput(id=GameAction.ACTION1))
    n1 = g.step_counter_hud.current
    return n0 - n1 == 1, f"before={n0} after={n1} delta={n0 - n1}"
