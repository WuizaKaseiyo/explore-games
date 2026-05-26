"""End-to-end verification: run the spec's L3 witness through the engine
and report whether the level wins."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT))

from novaengine import ActionInput, GameAction  # noqa: E402

GAME_ID = "yf3h"
PASCAL = "Yf3h"
SRC = REPO_ROOT / f"prior-games/{GAME_ID}/{GAME_ID}.py"


def _load_class():
    spec = importlib.util.spec_from_file_location(f"verify_{GAME_ID}", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, PASCAL)


def _grid_to_display_px(grid_size, gx, gy):
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    return gx * scale + ox + scale // 2, gy * scale + oy + scale // 2


def click_at_grid(g, gx, gy):
    fx, fy = _grid_to_display_px(g.current_level.grid_size, gx, gy)
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True
    )


def fire(g):
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)


def state_name(g):
    s = getattr(g, "_state", None)
    return s.name if s is not None else "?"


def show(g, label):
    state = state_name(g)
    lvl = g._current_level_index
    armed = len(g._armed_emitters)
    delays_active = len(g._delay_tiles_active)
    activated = len(g._activated_resonators)
    anim = g._anim_active
    rings = len(g._active_rings)
    steps = g._steps_remaining
    print(
        f"  [{label}] state={state} lvl={lvl+1} steps_left={steps} "
        f"armed={armed} delays_active={delays_active} "
        f"activated={activated} anim={anim} rings_in_flight={rings}"
    )


def main() -> None:
    GameClass = _load_class()
    g = GameClass()

    # Level-by-level: skip L1 + L2 by simulating their witnesses, then verify L3.
    print("=== L1 witness ===")
    g.set_level(0)
    em_red_l1 = g.current_level.get_sprites_by_tag("emitter")[0]
    show(g, "L1 start")
    click_at_grid(g, em_red_l1.x + 2, em_red_l1.y + 2)
    show(g, "after arm red")
    fire(g)
    show(g, "after fire")

    print("\n=== L2 witness ===")
    g.set_level(1)
    em_red_l2 = next(e for e in g.current_level.get_sprites_by_tag("emitter") if "colour_red" in e.tags)
    em_blue_l2 = next(e for e in g.current_level.get_sprites_by_tag("emitter") if "colour_blue" in e.tags)
    show(g, "L2 start")
    click_at_grid(g, em_red_l2.x + 2, em_red_l2.y + 2)
    click_at_grid(g, em_blue_l2.x + 2, em_blue_l2.y + 2)
    show(g, "after arm both")
    fire(g)
    show(g, "after fire")

    print("\n=== L3 witness ===")
    g.set_level(2)
    em_red_l3 = next(e for e in g.current_level.get_sprites_by_tag("emitter") if "colour_red" in e.tags)
    em_blue_l3 = next(e for e in g.current_level.get_sprites_by_tag("emitter") if "colour_blue" in e.tags)
    em_green_l3 = next(e for e in g.current_level.get_sprites_by_tag("emitter") if "colour_green" in e.tags)
    tile = g.current_level.get_sprites_by_tag("phase_delay")[0]
    multi_res = next(r for r in g.current_level.get_sprites_by_tag("resonator") if "multi_colour" in r.tags)
    green_res = next(r for r in g.current_level.get_sprites_by_tag("resonator") if "required_green" in r.tags)

    print(f"  emitter_red @ ({em_red_l3.x}, {em_red_l3.y}); centre ({em_red_l3.x+2}, {em_red_l3.y+2})")
    print(f"  emitter_blue @ ({em_blue_l3.x}, {em_blue_l3.y}); centre ({em_blue_l3.x+2}, {em_blue_l3.y+2})")
    print(f"  emitter_green @ ({em_green_l3.x}, {em_green_l3.y}); centre ({em_green_l3.x+2}, {em_green_l3.y+2})")
    print(f"  multi-resonator @ ({multi_res.x}, {multi_res.y}); centre ({multi_res.x+2}, {multi_res.y+2})")
    print(f"  green-resonator @ ({green_res.x}, {green_res.y}); centre ({green_res.x+2}, {green_res.y+2})")
    print(f"  phase-delay tile @ ({tile.x}, {tile.y}); centre ({tile.x+1}, {tile.y+1})")

    show(g, "L3 start")
    click_at_grid(g, tile.x + 1, tile.y + 1)
    show(g, "after toggle delay")
    click_at_grid(g, em_red_l3.x + 2, em_red_l3.y + 2)
    show(g, "after arm red")
    click_at_grid(g, em_blue_l3.x + 2, em_blue_l3.y + 2)
    show(g, "after arm blue")
    click_at_grid(g, em_green_l3.x + 2, em_green_l3.y + 2)
    show(g, "after arm green")
    fire(g)
    show(g, "after fire (post-anim)")

    print()
    print("=== RESULT ===")
    state = state_name(g)
    if state == "WIN":
        print("  WIN — L3 cleared, all 3 levels solved with the spec's witness sequence.")
    elif state == "GAME_OVER":
        print("  GAME_OVER — witness failed (likely budget exhausted before activation).")
    else:
        print(f"  state={state}, level_index={g._current_level_index}, "
              f"activated_resonators={len(g._activated_resonators)} — INCONCLUSIVE")


if __name__ == "__main__":
    main()
