"""Custom smoke-test checks for bx84.

Each check returns (passed: bool, observed: str). Run alongside
the universal checks.
"""

from novaengine import ActionInput, GameAction


def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2


def check_l1_minimal_solve(GameClass):
    """L1 witness (one click at grid (8, 8)) advances to L2."""
    g = GameClass()
    g.set_level(0)
    fx, fy = _grid_to_display_px(g.current_level.grid_size, 8, 8)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    return g._current_level_index == 1, f"level after L1 solve={g._current_level_index}"


def check_click_empty_places_mirror(GameClass):
    """Clicking an empty grid cell adds a mirror_bs sprite there."""
    g = GameClass()
    g.set_level(0)
    n_before = sum(1 for s in g.current_level.get_sprites() if s.name == "mirror_bs")
    fx, fy = _grid_to_display_px(g.current_level.grid_size, 5, 5)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    n_after = sum(1 for s in g.current_level.get_sprites() if s.name == "mirror_bs")
    return n_after == n_before + 1, f"mirror_bs count before={n_before} after={n_after}"


def check_filter_recolours_beam(GameClass):
    """In L2, after the level loads, the beam past the filter cell shows palette-9 (blue) on the overlay."""
    g = GameClass()
    g.set_level(1)
    overlay = next(s for s in g.current_level.get_sprites() if s.name == "beam_overlay")
    # Filter is at (3, 2). Beam path on row 2 starts at (2, 2). Cell (4, 2) is past the filter.
    # Beam_overlay only paints empty cells, so (2, 2) should be palette-11 (yellow, pre-filter)
    # and (4, 2) should be palette-9 (blue, post-filter).
    pre_filter = int(overlay.pixels[2, 2])  # (y=2, x=2)
    post_filter = int(overlay.pixels[2, 4])  # (y=2, x=4)
    passed = pre_filter == 11 and post_filter == 9
    return passed, f"pre_filter (2, 2)={pre_filter} post_filter (4, 2)={post_filter}"


def check_prism_toggle_changes_branch(GameClass):
    """In L3, clicking the prism cell toggles its sprite from prism_es to prism_en (or back)."""
    g = GameClass()
    g.set_level(2)
    prism_initial = next(s for s in g.current_level.get_sprites() if "prism" in s.tags)
    initial_name = prism_initial.name
    fx, fy = _grid_to_display_px(g.current_level.grid_size, 4, 8)  # prism at (4, 8)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    prism_after = next(s for s in g.current_level.get_sprites() if "prism" in s.tags)
    after_name = prism_after.name
    return after_name != initial_name, f"prism before={initial_name} after={after_name}"
