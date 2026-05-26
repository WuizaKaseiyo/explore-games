"""Custom smoke checks for ds5q (wall-erode-chain)."""
from novaengine import ActionInput, GameAction


def check_arrow_moves_avatar(GameClass) -> tuple[bool, str]:
    """ACTION4 (right) moves the avatar +8 pixels (one tile) east."""
    g = GameClass()
    avatar = g._active_avatar()
    x0 = avatar.x
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    x1 = g._active_avatar().x
    return x1 == x0 + 8, f"x0={x0} x1={x1}"


def check_uncharged_erode_is_noop(GameClass) -> tuple[bool, str]:
    """At L2 the avatar is uncharged; ACTION5 must not change wall hardness."""
    g = GameClass()
    g.set_level(1)  # L2
    walls_before = sorted(g.wall_hardness.items())
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    walls_after = sorted(g.wall_hardness.items())
    return walls_before == walls_after, f"before={walls_before} after={walls_after}"


def check_charge_pad_sets_state(GameClass) -> tuple[bool, str]:
    """At L2 walking onto the red pad sets charge_state to 'red'."""
    g = GameClass()
    g.set_level(1)  # L2
    # 4 moves north + 1 move east lands on red pad at tile (1, 0)
    for _ in range(4):
        g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION4), raw=True)
    return g.charge_state == "red", f"charge_state={g.charge_state}"


def check_l3_layered_hardness(GameClass) -> tuple[bool, str]:
    """At L3 the (3, 1) red wall starts at hardness 2 (multi-strike required)."""
    g = GameClass()
    g.set_level(2)  # L3
    h = g.wall_hardness.get((3, 1))
    return h == 2, f"wall_hardness[(3,1)]={h}"
