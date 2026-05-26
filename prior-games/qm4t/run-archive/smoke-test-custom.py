"""Custom smoke checks specific to qm4t (convex-pen-trap)."""

from novaengine import ActionInput, GameAction


def check_action6_places_post(GameClass) -> tuple[bool, str]:
    """Clicking an empty playfield cell adds a vertex_post sprite."""
    g = GameClass()
    g.set_level(0)
    n0 = len(g.current_level.get_sprites_by_tag("vertex_post"))
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 6, "y": 6}))
    n1 = len(g.current_level.get_sprites_by_tag("vertex_post"))
    return n1 == n0 + 1, f"posts before={n0} after={n1}"


def check_action5_with_zero_posts_is_noop(GameClass) -> tuple[bool, str]:
    """ACTION5 with no posts placed does not raise and removes nothing."""
    g = GameClass()
    g.set_level(0)
    n0 = len(g.current_level.get_sprites_by_tag("critter_green"))
    g.perform_action(ActionInput(id=GameAction.ACTION5, data={}))
    n1 = len(g.current_level.get_sprites_by_tag("critter_green"))
    return n1 == n0, f"greens before={n0} after={n1}"


def check_action5_captures_enclosed_green(GameClass) -> tuple[bool, str]:
    """Placing 3 posts around a green critter and committing removes it."""
    g = GameClass()
    g.set_level(0)
    # The 3 greens at L1 are at (20,20), (40,22), (30,40).
    # A triangle (15,15), (50,15), (30,50) encloses all three.
    for x, y in [(15, 15), (50, 15), (30, 50)]:
        g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y}))
    n_greens_before = len(g.current_level.get_sprites_by_tag("critter_green"))
    g.perform_action(ActionInput(id=GameAction.ACTION5, data={}))
    # Game advanced to L2; check that greens were captured.
    return n_greens_before == 3 and g.level_index == 1, f"L1_greens={n_greens_before} level_after={g.level_index}"


def check_strike_on_maroon_capture(GameClass) -> tuple[bool, str]:
    """Capturing only a maroon (at L2) triggers exactly one strike."""
    g = GameClass()
    g.set_level(1)
    # L2 has a maroon at (5, 5) with centre (7.5, 7). Triangle vertices
    # at (4, 4), (15, 4), (7, 13) — all in the playfield (y >= 4) — enclose
    # the maroon centre (verified by ray-cast) and exclude every green
    # (greens are at y >= 20, well below the triangle's bottom apex at y=13).
    for x, y in [(4, 4), (15, 4), (7, 13)]:
        g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y}))
    s0 = g._strikes
    g.perform_action(ActionInput(id=GameAction.ACTION5, data={}))
    s1 = g._strikes
    return s1 == s0 + 1, f"strikes before={s0} after={s1}"
