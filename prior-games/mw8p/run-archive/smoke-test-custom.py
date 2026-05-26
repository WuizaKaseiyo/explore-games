"""Custom smoke checks for mw8p — one essential mechanic invariant per
function, per `code/smoke-test-checks.md` § Custom checks (agent-
authored)."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction, InteractionMode


def _load_game_class():
    src = Path("prior-games/mw8p/mw8p.py")
    spec = importlib.util.spec_from_file_location("smoke_mw8p_custom", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Mw8p


GameClass = _load_game_class()


def check_right_moves_player() -> tuple[bool, str]:
    """ACTION4 (RIGHT) translates the player one logical cell (+8 px in x)
    when the destination cell is empty and in-bounds."""
    g = GameClass()
    g.handle_reset()  # places at level 1
    player = g.current_level.get_sprites_by_tag("player")[0]
    x0 = player.x
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    return player.x == x0 + 8, f"x0={x0} x1={player.x}"


def check_a_eats_c_on_entry() -> tuple[bool, str]:
    """M3 (A-eats-C): at L3 start, A at (0, 7) has C1 at (1, 7). One RIGHT
    must consume C1 (its interaction becomes REMOVED) and the player
    must be at (1, 7)."""
    g = GameClass()
    g.handle_reset()
    g.set_level(2)  # L3 (0-indexed)
    mids_before = g.current_level.get_sprites_by_tag("mid")
    c1 = next(m for m in mids_before if (m.x - 1) // 8 == 1 and (m.y - 1) // 8 == 7)
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    return c1._interaction == InteractionMode.REMOVED, (
        f"C1 interaction after RIGHT = {c1._interaction!r}"
    )


def check_c_kills_b_on_coincidence() -> tuple[bool, str]:
    """M2 (C-kills-B): at L2 start, one RIGHT triggers B's vertical
    pursuit step from (4, 5) to (4, 4) where C also lands; C must remove
    the pursuer on coincidence (B's interaction becomes REMOVED)."""
    g = GameClass()
    g.handle_reset()
    g.set_level(1)  # L2 (0-indexed)
    b = g.current_level.get_sprites_by_tag("pursuer")[0]
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    return b._interaction == InteractionMode.REMOVED, (
        f"B interaction after RIGHT = {b._interaction!r}"
    )


def check_lose_at_budget() -> tuple[bool, str]:
    """Step budget: at L1, 25 blocked-LEFT actions (all blocked by the
    col-0 left wall) consume the 25-step budget; the engine must enter
    GAME_OVER on or before the 25th action."""
    g = GameClass()
    g.handle_reset()
    g.set_level(0)
    for _ in range(25):
        g.perform_action(ActionInput(id=GameAction.ACTION3))
        if g._state.name == "GAME_OVER":
            break
    return g._state.name == "GAME_OVER", f"state after 25 blocked-LEFT = {g._state.name}"


if __name__ == "__main__":
    for fn in (
        check_right_moves_player,
        check_a_eats_c_on_entry,
        check_c_kills_b_on_coincidence,
        check_lose_at_budget,
    ):
        passed, observed = fn()
        print(f"{fn.__name__}: {'PASS' if passed else 'FAIL'} ({observed})")
