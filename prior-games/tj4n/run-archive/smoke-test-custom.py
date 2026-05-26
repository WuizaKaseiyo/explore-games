"""Custom smoke checks for tj4n. 4 checks; each ≤1s, ≤5 setup actions, single boolean."""

import importlib.util
from pathlib import Path
from novaengine import ActionInput, GameAction
from novaengine.enums import InteractionMode

SRC = Path("prior-games/tj4n/tj4n.py")


def _load():
    spec = importlib.util.spec_from_file_location("smoke_tj4n", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Tj4n


def _act(n):
    return ActionInput(id=GameAction.from_id(n), data={})


def check_up_moves_avatar():
    """ACTION1 moves the avatar up by exactly one logical cell (4 pixels)."""
    GameClass = _load()
    g = GameClass()
    g.set_level(0)
    y0 = g._avatar_pos[1]
    g.perform_action(_act(1), raw=True)
    return g._avatar_pos[1] == y0 - 4, f"y0={y0} y1={g._avatar_pos[1]}"


def check_step_deposits_trail_at_old_position():
    """A successful move deposits a trail_cell sprite at the avatar's previous cell."""
    GameClass = _load()
    g = GameClass()
    g.set_level(0)
    old_pos = g._avatar_pos
    g.perform_action(_act(1), raw=True)  # one move
    trail_at_old = any(
        s.x == old_pos[0] and s.y == old_pos[1] and "trail" in (s.tags or [])
        for s in g.current_level.get_sprites()
    )
    return trail_at_old, f"old_pos={old_pos} trail_present={trail_at_old}"


def check_closure_advances_level():
    """Closing a loop on L1 that encloses all targets advances to L2 (next_level fires)."""
    GameClass = _load()
    g = GameClass()
    g.set_level(0)
    # Replay the spec L1 witness; observable effect we assert is that the engine
    # advances the level index past L1.
    L1 = (
        [_act(1)] * 2
        + [_act(4)] * 6
        + [_act(2)] * 3
        + [_act(3)] * 6
        + [_act(1)] * 1
    )
    for ai in L1:
        g.perform_action(ai, raw=True)
    return g._current_level_index == 1, f"level_index_after_L1_witness={g._current_level_index}"


def check_blocked_by_forbidden():
    """Avatar cannot step onto a forbidden cell (movement is blocked)."""
    GameClass = _load()
    g = GameClass()
    g.set_level(1)  # L2 has forbiddens; L2 layout has avatar at (32, 52), forbiddens at (32, 20)
    # Move avatar UP via x=32: should hit forbidden at y=20 and stop.
    # Avatar at (32, 52). 8 moves up reach (32, 20). The 9th move from (32, 24) to (32, 20) is blocked.
    for _ in range(7):
        g.perform_action(_act(1), raw=True)
    pos_before = g._avatar_pos  # should be (32, 24)
    g.perform_action(_act(1), raw=True)  # try to step onto forbidden at (32, 20)
    return g._avatar_pos == pos_before, f"before={pos_before} after={g._avatar_pos}"


CHECKS = [
    ("check_up_moves_avatar", check_up_moves_avatar),
    ("check_step_deposits_trail_at_old_position", check_step_deposits_trail_at_old_position),
    ("check_closure_advances_level", check_closure_advances_level),
    ("check_blocked_by_forbidden", check_blocked_by_forbidden),
]


if __name__ == "__main__":
    for name, fn in CHECKS:
        passed, observed = fn()
        marker = "PASS" if passed else "FAIL"
        print(f"{marker}: {name} | {observed}")
