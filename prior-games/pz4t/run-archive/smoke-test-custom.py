"""Custom smoke checks for pz4t (anchor-pivot-place)."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load_game_class():
    src = Path("prior-games/pz4t/pz4t.py")
    spec = importlib.util.spec_from_file_location("smoke_pz4t", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Pz4t


def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2


def check_click_picks_up_component(GameClass) -> tuple[bool, str]:
    """ACTION6 click on a component sets self.held_component."""
    g = GameClass()
    g.set_level(0)
    comp = g.current_level.get_sprites_by_tag("component")[0]
    fx, fy = _grid_to_display_px(g.current_level.grid_size, comp.x, comp.y)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    return g.held_component is comp, f"held={getattr(g.held_component, 'name', None)}"


def check_anchor_offset_recorded(GameClass) -> tuple[bool, str]:
    """Picking up at the second cell of a 3-cell bar records anchor_offset=(1,0)."""
    g = GameClass()
    g.set_level(0)
    comp = next(c for c in g.current_level.get_sprites_by_tag("component") if c.name == "comp_red_bar3")
    target_gx, target_gy = comp.x + 1, comp.y
    fx, fy = _grid_to_display_px(g.current_level.grid_size, target_gx, target_gy)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    return g.anchor_offset == (1, 0), f"anchor_offset={g.anchor_offset}"


def check_place_uses_anchor(GameClass) -> tuple[bool, str]:
    """After picking with anchor (1, 0) on a 3-bar, clicking grid (5, 2) places sprite at (4, 2)."""
    g = GameClass()
    g.set_level(0)
    comp = next(c for c in g.current_level.get_sprites_by_tag("component") if c.name == "comp_red_bar3")
    fx, fy = _grid_to_display_px(g.current_level.grid_size, comp.x + 1, comp.y)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    fx, fy = _grid_to_display_px(g.current_level.grid_size, 5, 2)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    return (comp.x, comp.y) == (4, 2), f"comp.pos=({comp.x},{comp.y})"


def check_rotate_transforms_anchor(GameClass) -> tuple[bool, str]:
    """Rotating a vertical 1x3 with anchor (0, 0) yields a horizontal 3x1 with anchor (2, 0)."""
    g = GameClass()
    g.set_level(1)
    comp = next(c for c in g.current_level.get_sprites_by_tag("component") if c.name == "comp_red_vbar3")
    fx, fy = _grid_to_display_px(g.current_level.grid_size, comp.x, comp.y)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    return g.anchor_offset == (2, 0) and comp.width == 3, f"anchor={g.anchor_offset} width={comp.width}"


def check_flip_makes_z_into_s(GameClass) -> tuple[bool, str]:
    """Flipping comp_red_Z horizontally produces an S-shaped pixel pattern."""
    g = GameClass()
    g.set_level(2)
    comp = next(c for c in g.current_level.get_sprites_by_tag("component") if c.name == "comp_red_Z")
    fx, fy = _grid_to_display_px(g.current_level.grid_size, comp.x, comp.y)
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True)
    g.perform_action(ActionInput(id=GameAction.ACTION7), raw=True)
    rendered = comp.render()
    expected = [[-1, 8, 8], [8, 8, -1]]
    return rendered.tolist() == expected, f"rendered={rendered.tolist()}"


CUSTOM_CHECKS = [
    check_click_picks_up_component,
    check_anchor_offset_recorded,
    check_place_uses_anchor,
    check_rotate_transforms_anchor,
    check_flip_makes_z_into_s,
]


if __name__ == "__main__":
    GameClass = _load_game_class()
    for fn in CUSTOM_CHECKS:
        passed, observed = fn(GameClass)
        marker = "PASS" if passed else "FAIL"
        print(f"{marker} {fn.__name__}: {observed}")
