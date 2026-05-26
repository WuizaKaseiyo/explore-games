"""Custom smoke checks for pq5w. Each function tests ONE essential
mechanic invariant with <= 5 setup actions and ONE boolean assertion.
"""

from novaengine import ActionInput, GameAction


def check_right_walks_avatar(GameClass):
    """ACTION4 from L1 start moves the avatar +STRIDE in x."""
    g = GameClass()
    g.set_level(0)
    avatar = g.current_level.get_sprites_by_tag("player")[0]
    x0 = avatar.x
    g.perform_action(ActionInput(id=GameAction.ACTION4, data={}), raw=True)
    return avatar.x == x0 + 4, f"x0={x0} x1={avatar.x}"


def check_walk_onto_anchor_sets_pending(GameClass):
    """Walking onto the anchor portal in L1 sets _teleport_pending."""
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.ACTION4, data={}), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION4, data={}), raw=True)
    return g._teleport_pending is not None, f"pending={g._teleport_pending}"


def check_click_relocates_float_portal(GameClass):
    """Select-then-place: clicking the float portal selects it, then a
    second click on a valid floor cell relocates it."""
    g = GameClass()
    g.set_level(1)  # L2
    float_p = g.current_level.get_sprites_by_tag("float")[0]
    # First click: select the float portal at its current cell (40, 12).
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 42, "y": 14}), raw=True)
    # Second click: place at (8, 36).
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 10, "y": 38}), raw=True)
    return (float_p.x, float_p.y) == (8, 36), f"after=({float_p.x},{float_p.y})"


def check_click_on_float_toggles_selected(GameClass):
    """Clicking the float portal toggles _float_selected from False to True."""
    g = GameClass()
    g.set_level(1)  # L2
    before = g._float_selected
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 42, "y": 14}), raw=True)
    return (before is False) and (g._float_selected is True), f"before={before} after={g._float_selected}"


def check_step_used_increments(GameClass):
    """Each handled action increments the private step counter."""
    g = GameClass()
    g.set_level(0)
    n0 = g._steps_used
    g.perform_action(ActionInput(id=GameAction.ACTION1, data={}), raw=True)
    return g._steps_used == n0 + 1, f"before={n0} after={g._steps_used}"
