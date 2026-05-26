"""Custom smoke checks for qj4r (rev 3 — anchored targets + animation)."""

import importlib.util
from pathlib import Path
from novaengine import ActionInput, GameAction, InteractionMode

ACTIONS = {
    1: GameAction.ACTION1,
    2: GameAction.ACTION2,
    3: GameAction.ACTION3,
    4: GameAction.ACTION4,
}


def _load_game():
    src = Path("prior-games/qj4r/qj4r.py")
    spec = importlib.util.spec_from_file_location("smoke_qj4r", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Qj4r


def check_fold_reflects_piece():
    """ACTION1 on L1 reflects orange piece's y-coord across horizontal mid-axis."""
    GameClass = _load_game()
    g = GameClass()
    g.set_level(0)
    pieces_before = [s for s in g.current_level.get_sprites_by_tag("orange") if "piece" in s.tags]
    assert len(pieces_before) == 1
    cy0 = (pieces_before[0].y - g._grid_offset) // g._cell_size
    # piece starts at (1, 1); ACTION1 (fold-top-onto-bottom, kept y∈{4..7}) reflects y=1→y=6.
    g.perform_action(ActionInput(id=ACTIONS[1]))
    pieces_after = [s for s in g.current_level.get_sprites_by_tag("orange")
                    if "piece" in s.tags and s.interaction != InteractionMode.REMOVED]
    cy1 = (pieces_after[0].y - g._grid_offset) // g._cell_size
    observed = f"cy0={cy0} cy1={cy1} (expected 7-cy0={7-cy0})"
    return cy1 == 7 - cy0, observed


def check_same_colour_merge():
    """ACTION3 on L2 merges two oranges (count goes 2 → 1 active piece)."""
    GameClass = _load_game()
    g = GameClass()
    g.set_level(1)
    actives_before = [s for s in g.current_level.get_sprites_by_tag("orange")
                      if "piece" in s.tags and s.interaction != InteractionMode.REMOVED]
    g.perform_action(ActionInput(id=ACTIONS[3]))
    actives_after = [s for s in g.current_level.get_sprites_by_tag("orange")
                     if "piece" in s.tags and s.interaction != InteractionMode.REMOVED]
    observed = f"before={len(actives_before)} after={len(actives_after)}"
    return len(actives_before) == 2 and len(actives_after) == 1, observed


def check_l3_two_colour_witness():
    """L3 witness ACTION3+ACTION4 lands both colours on their anchored targets simultaneously."""
    GameClass = _load_game()
    g = GameClass()
    g.set_level(2)
    g.perform_action(ActionInput(id=ACTIONS[3]))
    g.perform_action(ActionInput(id=ACTIONS[4]))
    observed = f"L3 state after witness = {g._state.name}, score = {g._score}"
    return g._state.name == "WIN" or g._score >= 3, observed


def check_anchored_target_lose():
    """A wrong fold that retires the anchored target's cell triggers self.lose()."""
    GameClass = _load_game()
    g = GameClass()
    g.set_level(0)
    # L1 target at (6, 6); ACTION2 (fold-bottom-onto-top, kept y∈{0..3}) retires y=6 → target destroyed → lose.
    g.perform_action(ActionInput(id=ACTIONS[2]))
    observed = f"state after L1 ACTION2 = {g._state.name}"
    return g._state.name == "GAME_OVER", observed


def check_l1_two_fold_witness():
    """L1 requires the player to learn the mechanic over more than one fold."""
    GameClass = _load_game()
    g = GameClass()
    g.set_level(0)
    # No single fold should win L1 (mechanic is observable but goal isn't reached in one action).
    for aid in (1, 2, 3, 4):
        g_test = GameClass()
        g_test.perform_action(ActionInput(id=ACTIONS[aid]))
        if g_test._score >= 1:
            return False, f"single ACTION{aid} won L1 prematurely"
    # The two-fold witness [ACTION3, ACTION1] wins L1.
    g.perform_action(ActionInput(id=ACTIONS[3]))
    g.perform_action(ActionInput(id=ACTIONS[1]))
    observed = f"L1 score after 2-fold witness = {g._score}"
    return g._score >= 1, observed


if __name__ == "__main__":
    checks = [
        ("check_fold_reflects_piece", check_fold_reflects_piece),
        ("check_same_colour_merge", check_same_colour_merge),
        ("check_l3_two_colour_witness", check_l3_two_colour_witness),
        ("check_l1_two_fold_witness", check_l1_two_fold_witness),
        ("check_anchored_target_lose", check_anchored_target_lose),
    ]
    for name, fn in checks:
        try:
            passed, observed = fn()
            print(f"{name}: {'PASS' if passed else 'FAIL'} — {observed}")
        except Exception as e:
            print(f"{name}: ERROR — {e!r}")
