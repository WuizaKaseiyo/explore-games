"""Custom mechanic-invariant checks for xn5p — chamber-stamp-partition."""

import importlib.util
from pathlib import Path
from novaengine import GameAction, ActionInput

_src = Path("prior-games/xn5p/xn5p.py")
_spec = importlib.util.spec_from_file_location("smoke_xn5p_custom", _src)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
GameClass = _mod.Xn5p


def check_walk_moves_avatar() -> tuple[bool, str]:
    """ACTION3 (west) moves the avatar one 3-cell stride west when destination is open."""
    g = GameClass()
    g.set_level(0)
    avatar = g._avatar_sprite()
    x0, y0 = avatar.x, avatar.y
    g.perform_action(ActionInput(id=GameAction.ACTION3), raw=True)
    avatar2 = g._avatar_sprite()
    passed = (avatar2.x == x0 - 3 and avatar2.y == y0)
    return passed, f"x0={x0} -> x1={avatar2.x} (expected {x0 - 3})"


def check_stamp_creates_wall() -> tuple[bool, str]:
    """ACTION5 at an empty cell creates a wall_stamp sprite at the avatar's position.

    Walked first to a non-partition-completing cell (south of start) to avoid
    triggering an L1 next_level that would clear the just-placed stamp.
    """
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)  # south
    avatar = g._avatar_sprite()
    ax, ay = avatar.x, avatar.y
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    stamps = [
        s for s in g.current_level.get_sprites()
        if "wall_stamp" in (getattr(s, "tags", []) or [])
    ]
    matching = [s for s in stamps if s.x == ax and s.y == ay]
    passed = (len(stamps) >= 1 and len(matching) == 1)
    return passed, f"after_stamp count={len(stamps)} at_pos={len(matching)}"


def check_push_moves_molecule() -> tuple[bool, str]:
    """On L2, walking the avatar west into the obstacle red molecule pushes it one stride west."""
    g = GameClass()
    g.set_level(1)
    # Avatar starts at lattice (5, 0) = (16, 1). Path to push: south, south, west, west.
    for aid in (GameAction.ACTION2, GameAction.ACTION2, GameAction.ACTION3):
        g.perform_action(ActionInput(id=aid), raw=True)
    # Avatar should now be at lattice (4, 2) = (13, 7); obstacle red at lattice (3, 2) = (10, 7).
    obstacle_before = None
    for s in g.current_level.get_sprites():
        tags = getattr(s, "tags", []) or []
        if "molecule_red" in tags and s.x == 10 and s.y == 7:
            obstacle_before = (s.x, s.y)
    g.perform_action(ActionInput(id=GameAction.ACTION3), raw=True)
    obstacle_after = None
    for s in g.current_level.get_sprites():
        tags = getattr(s, "tags", []) or []
        if "molecule_red" in tags and s.y == 7:
            # The pushable obstacle's expected new position is (7, 7) = lattice (2, 2).
            if s.x == 7:
                obstacle_after = (s.x, s.y)
    passed = (obstacle_before == (10, 7) and obstacle_after == (7, 7))
    return passed, f"before={obstacle_before} after={obstacle_after}"


def check_toggle_removes_stamp() -> tuple[bool, str]:
    """On L3, pressing ACTION5 twice at the same cell creates then removes a stamp."""
    g = GameClass()
    g.set_level(2)
    # Avatar starts at lattice (5, 0) = (16, 1). ACTION5 alone places a stamp at the avatar's cell.
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    n_after_stamp = sum(
        1 for s in g.current_level.get_sprites()
        if "wall_stamp" in (getattr(s, "tags", []) or [])
    )
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    n_after_toggle = sum(
        1 for s in g.current_level.get_sprites()
        if "wall_stamp" in (getattr(s, "tags", []) or [])
    )
    passed = (n_after_stamp == 1 and n_after_toggle == 0)
    return passed, f"after_stamp={n_after_stamp} after_toggle={n_after_toggle}"


CHECKS = [
    check_walk_moves_avatar,
    check_stamp_creates_wall,
    check_push_moves_molecule,
    check_toggle_removes_stamp,
]


if __name__ == "__main__":
    for fn in CHECKS:
        passed, observed = fn()
        status = "PASS" if passed else "FAIL"
        print(f"{status} {fn.__name__}: {observed}")
