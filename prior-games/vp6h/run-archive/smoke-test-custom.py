"""Custom smoke checks for vp6h.

Each check follows the strict template: ≤ 5 setup actions, ONE action under
test, ONE boolean assertion. Tests an essential mechanic invariant.
"""

from novaengine import ActionInput, GameAction, InteractionMode


def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2


def check_arrow_moves_avatar(GameClass) -> tuple[bool, str]:
    """ACTION4 (right) on L1 moves the avatar's x-position by +1."""
    g = GameClass()
    g.set_level(0)
    avatars = g.current_level.get_sprites_by_tag("avatar")
    avatar = avatars[0]
    x0 = avatar.x
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    return avatar.x == x0 + 1, f"x0={x0} x1={avatar.x}"


def check_click_top_rail_slides_lantern(GameClass) -> tuple[bool, str]:
    """ACTION6 click at grid (col=2, row=0) on L2 slides top-lantern to cols 0..4."""
    g = GameClass()
    g.set_level(1)  # L2
    fx, fy = _grid_to_display_px(g.current_level.grid_size, 2, 0)
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}),
        raw=True,
    )
    return g._top_lantern_x == 0, f"top_lantern_x after click={g._top_lantern_x}"


def check_pickup_in_shadow_collects_crystal(GameClass) -> tuple[bool, str]:
    """Walking onto a shaded crystal at L1 fires the level transition (L1 solved).

    Setup: 5 ACTION4 (avatar (2,13) -> (7,13)).
    Action under test: ACTION1 (avatar (7,13) -> (7,12) overlapping the only L1
    crystal at (col=7, row=11..12); cell (7, 12) is shaded by the col-7 pillar).
    Assertion: pickup succeeded and the engine advanced to L2 (level idx 1).
    """
    g = GameClass()
    g.set_level(0)
    for _ in range(5):
        g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    # action under test
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    return g._current_level_index == 1, f"level_idx after pickup={g._current_level_index}"


def check_pickup_in_light_is_no_op(GameClass) -> tuple[bool, str]:
    """Walking onto a LIT crystal on L2 does NOT pick it up.

    Setup: 5 ACTION4 (avatar (1,13) -> (6,13)). At L2 default lantern (cols 5..9),
    col 6 is lit (no pillar).
    Action under test: ACTION1 (avatar -> (6,12); footprint covers (6..7, 12..13);
    overlaps crystal B at (col=6, row=11..12) cells (6,12) and (7,12); cell (6, 12)
    is top-LIT → pickup must be a no-op).
    Assertion: crystal B is still TANGIBLE (not REMOVED).
    """
    g = GameClass()
    g.set_level(1)  # L2
    for _ in range(5):
        g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    # avatar at (6, 13)
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    # find crystal at col=6
    crystals = g.current_level.get_sprites_by_tag("crystal")
    crystal_b = next((c for c in crystals if c.x == 6), None)
    assert crystal_b is not None, "crystal B not found at col 6"
    return crystal_b.interaction != InteractionMode.REMOVED, (
        f"crystal_b.interaction={crystal_b.interaction}"
    )
