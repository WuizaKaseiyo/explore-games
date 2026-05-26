"""Custom smoke checks for ng52 (multiset-signature classifier)."""

from __future__ import annotations

from novaengine import ActionInput, GameAction


def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2


def _co(o):
    return o.x + o.width // 2, o.y + o.height // 2


def _cm(b):
    x0, y0, x1, y1 = b.holding_rect
    return (x0 + x1) // 2, (y0 + y1) // 2


def _click(g, gx, gy):
    fx, fy = _grid_to_display_px(g.current_level.grid_size, gx, gy)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)


def _commit(g):
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)


def check_click_selects_object(GameClass) -> tuple[bool, str]:
    """Clicking a pool object marks it as the current selection."""
    g = GameClass()
    g.set_level(0)
    target = g.objects[0]
    _click(g, *_co(target))
    return g.selection is target, f"selection={g.selection.sprite.name if g.selection else None}"


def check_place_in_bin(GameClass) -> tuple[bool, str]:
    """Selecting a pool object then clicking a bin's holding area places the object in that bin."""
    g = GameClass()
    g.set_level(0)
    target = g.objects[0]
    bin0 = g.bins[0]
    _click(g, *_co(target))
    _click(g, *_cm(bin0))
    return target.container == "bin_0" and target in bin0.placed, f"container={target.container} placed={[o.sprite.name for o in bin0.placed]}"


def check_failed_commit_resets_pool(GameClass) -> tuple[bool, str]:
    """Committing with a wrong placement returns every placed object to its original pool position."""
    g = GameClass()
    g.set_level(0)
    target = g.objects[0]
    pool_pos = target.pool_position
    bin1 = g.bins[1]  # 4-blue bin
    _click(g, *_co(target))
    _click(g, *_cm(bin1))   # place 3-blue object in 4-blue bin (mismatch)
    _commit(g)              # mismatch → snap-back-to-pool
    return target.container == "pool" and (target.x, target.y) == pool_pos, f"container={target.container} pos=({target.x},{target.y}) expected={pool_pos}"


def check_l1_minimal_solve(GameClass) -> tuple[bool, str]:
    """The 7-action L1 witness advances past L1."""
    g = GameClass()
    g.set_level(0)
    o1, o2, o3 = g.objects
    b0, b1, b2 = g.bins
    for o, b in ((o1, b0), (o2, b1), (o3, b2)):
        _click(g, *_co(o))
        _click(g, *_cm(b))
    _commit(g)
    return g._current_level_index == 1, f"level after solve={g._current_level_index}"


CUSTOM_CHECKS = [
    ("check_click_selects_object", check_click_selects_object),
    ("check_place_in_bin", check_place_in_bin),
    ("check_failed_commit_resets_pool", check_failed_commit_resets_pool),
    ("check_l1_minimal_solve", check_l1_minimal_solve),
]
