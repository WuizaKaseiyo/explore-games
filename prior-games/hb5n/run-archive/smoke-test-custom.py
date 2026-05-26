"""Custom smoke-test checks for hb5n.

Each check follows the strict template in
`skills/code/smoke-test-checks.md` § Custom checks:
- ≤ 5 setup actions
- exactly ONE action under test
- exactly ONE boolean assertion
- returns (bool passed, str observed)

Tests essential mechanic invariants for the polyomino-walker game:
- C1: ACTION4 (east) translates the anchor's x by +1.
- C2: ACTION5 rotates the polyomino (cell set changes).
- C3: walking adjacent to a pickup absorbs it (cell count grows).
- C4: walking near but NOT adjacent to a pickup leaves it un-absorbed.
"""

from novaengine import ActionInput, GameAction


def check_east_moves_anchor(GameClass):
    """ACTION4 translates the avatar's anchor x by +1 when unobstructed."""
    g = GameClass()
    g.set_level(0)
    x0, y0 = g.avatar_anchor
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    x1, y1 = g.avatar_anchor
    passed = (x1 == x0 + 1 and y1 == y0)
    return passed, f"anchor before=({x0},{y0}) after=({x1},{y1})"


def check_rotate_changes_silhouette(GameClass):
    """ACTION5 changes the avatar's absolute cell set when geometrically free."""
    g = GameClass()
    g.set_level(0)
    cells_before = sorted(set(g._absolute_cells()))
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    cells_after = sorted(set(g._absolute_cells()))
    passed = (cells_after != cells_before)
    return passed, f"before={cells_before} after={cells_after}"


def check_adjacency_absorbs_pickup(GameClass):
    """When an avatar cell becomes adjacent to a pickup, the pickup is absorbed."""
    g = GameClass()
    g.set_level(1)  # L2: avatar at (2,2), pickup at (5,4)
    # Setup (4 actions): walk to anchor (3,4) — one east of where the
    # pickup will become adjacent. After the next east step, anchor at
    # (4,4) is adjacent to pickup (5,4).
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)  # → (2,3)
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)  # → (2,4)
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)  # → (3,4)
    n_before = len(g.avatar_relative_cells)
    # Action under test: step east; anchor reaches (4,4) which is adjacent to (5,4).
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    n_after = len(g.avatar_relative_cells)
    passed = (n_after == n_before + 1)
    return passed, f"cells before={n_before} after={n_after}"


def check_non_adjacent_pickup_not_absorbed(GameClass):
    """Walking with all avatar cells > 1 cell away from a pickup leaves it un-absorbed."""
    g = GameClass()
    g.set_level(1)  # L2: avatar at (2,2), pickup at (5,4)
    # Setup (0 actions): the avatar starts at (2,2) with body cells
    # (1,2) and (1,3). The nearest cell to pickup (5,4) is (2,2) at
    # Manhattan distance 5 — far from adjacency.
    n_before = len(g.avatar_relative_cells)
    pickup_count_before = len(g.pickup_cells)
    # Action under test: step south. New cells (2,3), (1,3), (1,4).
    # Nearest cell to (5,4) is (1,4) at Manhattan distance 4 — still not adjacent.
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)
    n_after = len(g.avatar_relative_cells)
    pickup_count_after = len(g.pickup_cells)
    passed = (n_after == n_before and pickup_count_after == pickup_count_before)
    return passed, f"cells {n_before}→{n_after}; pickups {pickup_count_before}→{pickup_count_after}"


CUSTOM_CHECKS = [
    ("check_east_moves_anchor", check_east_moves_anchor),
    ("check_rotate_changes_silhouette", check_rotate_changes_silhouette),
    ("check_adjacency_absorbs_pickup", check_adjacency_absorbs_pickup),
    ("check_non_adjacent_pickup_not_absorbed", check_non_adjacent_pickup_not_absorbed),
]
