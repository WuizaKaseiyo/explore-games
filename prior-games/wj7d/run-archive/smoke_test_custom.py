"""Custom smoke-test checks for wj7d."""

from novaengine import GameAction, InteractionMode
from novaengine.enums import ActionInput


def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2


def check_arrow_moves_selected_stamp(GameClass):
    """ACTION4 (RIGHT) moves the selected stamp +ARROW_STEP px on x."""
    g = GameClass()
    g.set_level(0)
    pawn = g.selected_stamp  # auto-selected at L1
    x0, y0 = pawn.x, pawn.y
    g.perform_action(ActionInput(id=GameAction.ACTION4))
    return pawn.x == x0 + 4, f"x0={x0} x1={pawn.x}"


def check_click_selects_stamp_at_l2(GameClass):
    """ACTION6 click on a stamp's cell selects it (at L2 where no auto-select)."""
    g = GameClass()
    g.set_level(1)  # L2
    if g.selected_stamp is not None:
        return False, f"unexpected auto-select at L2: {g.selected_stamp.name}"
    fx, fy = _grid_to_display_px(g.current_level.grid_size, 24, 24)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}))
    return (
        g.selected_stamp is not None and g.selected_stamp.name == "stamp_blue_ring",
        f"selected = {g.selected_stamp.name if g.selected_stamp else None}",
    )


def check_fold_consumes_stamp(GameClass):
    """ACTION5 with a selected stamp removes the stamp from active interaction."""
    g = GameClass()
    g.set_level(0)
    pawn = g.selected_stamp
    g.perform_action(ActionInput(id=GameAction.ACTION5))
    return pawn.interaction == InteractionMode.REMOVED, (
        f"interaction after fold = {pawn.interaction}"
    )


def check_collision_blocks_stamp_into_other(GameClass):
    """At L2, red cannot reach (24, 20) while blue body still occupies (24, 24-29)."""
    g = GameClass()
    g.set_level(1)  # L2
    fx, fy = _grid_to_display_px(g.current_level.grid_size, 8, 4)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}))
    for _ in range(4):
        g.perform_action(ActionInput(id=GameAction.ACTION4))  # red x: 8 → 24
    for _ in range(3):
        g.perform_action(ActionInput(id=GameAction.ACTION2))  # red y: 4 → 16
    # 4th DOWN should be rejected (collision with blue at 24..29 rows 24..29)
    pre_y = g.selected_stamp.y
    g.perform_action(ActionInput(id=GameAction.ACTION2))
    post_y = g.selected_stamp.y
    return post_y == pre_y, f"pre_y={pre_y} post_y={post_y}"
