"""Custom smoke checks for ek73."""
import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load():
    src = Path("prior-games/ek73/ek73.py")
    spec = importlib.util.spec_from_file_location("ek73_smoke_custom", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Ek73


def _act(n):
    return ActionInput(id=GameAction.from_id(n), data={})


def check_arrow_moves_avatar(GameClass) -> tuple[bool, str]:
    """ACTION4 (right) advances the player by exactly one logical cell east."""
    g = GameClass()
    g.set_level(0)
    p = g.current_level.get_sprites_by_tag("player")[0]
    x0 = p.x
    g.perform_action(_act(4))
    x1 = p.x
    return x1 == x0 + 4, f"x0={x0} x1={x1} (expected x0+4)"


def check_self_wake_kills(GameClass) -> tuple[bool, str]:
    """Stepping back onto your own age-1 wake fires GAME_OVER."""
    g = GameClass()
    g.set_level(0)
    # Move east one cell, then immediately west — west cell is age-1 wake.
    g.perform_action(_act(4))
    g.perform_action(_act(3))
    return g._state.name == "GAME_OVER", f"state after east-then-west={g._state.name}"


def check_clearer_pad_wipes_wake(GameClass) -> tuple[bool, str]:
    """Stepping on the clearer pad at L2 (8,5) clears the wake state."""
    g = GameClass()
    g.set_level(1)  # L2
    # Avatar starts at (2, 8). Walk to clearer at (8, 5):
    # 6 east on row 8 to (8, 8); 1 north to (8, 7); 2 north to (8, 5) — clearer fires.
    for ai in [_act(4)]*6 + [_act(1)]*3:
        if g._state.name in ("GAME_OVER", "WIN"):
            break
        g.perform_action(ai)
    return len(g._wake) == 0, f"wake count after clearer={len(g._wake)}"


def check_warp_pair_teleports(GameClass) -> tuple[bool, str]:
    """At L3, stepping on warp pad A at (1, 9) teleports to (14, 9)."""
    g = GameClass()
    g.set_level(2)  # L3
    # Avatar starts at (8, 8). Walk west 7 to (1, 8); south 1 to (1, 9) warp.
    # But the column-8 wake from going north to collect would interfere — instead,
    # take a fresh route: 7 west then 1 south to warp.
    for ai in [_act(3)]*7 + [_act(2)]*1:
        if g._state.name in ("GAME_OVER", "WIN"):
            break
        g.perform_action(ai)
    p = g.current_level.get_sprites_by_tag("player")[0]
    return (p.x // 4, p.y // 4) == (14, 9), f"player cell after warp={(p.x // 4, p.y // 4)}"


CHECKS = [check_arrow_moves_avatar, check_self_wake_kills, check_clearer_pad_wipes_wake, check_warp_pair_teleports]


if __name__ == "__main__":
    GameClass = _load()
    for fn in CHECKS:
        passed, observed = fn(GameClass)
        print(f"{'PASS' if passed else 'FAIL'} {fn.__name__}: {observed}")
