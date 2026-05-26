"""Smoke test for dx8m — 11 universal + custom + skeleton-aware."""

import importlib.util
import sys
import traceback
from pathlib import Path

import numpy as np

src = Path("prior-games/dx8m/dx8m.py")
spec_loader = importlib.util.spec_from_file_location("smoke_dx8m", src)
mod = importlib.util.module_from_spec(spec_loader)
spec_loader.loader.exec_module(mod)
GameClass = mod.Dx8m

from novaengine import ActionInput, GameAction


def fresh_game():
    return GameClass()


def act(n):
    return ActionInput(id=GameAction.from_id(n), data={})


def click_cell(g, gx, gy):
    """Compute display pixel from cell coords given current camera."""
    gw, gh = g.current_level.grid_size
    scale = max(1, 64 // max(gw, gh))
    offset_x = (64 - scale * gw) // 2
    offset_y = (64 - scale * gh) // 2
    px = offset_x + gx * scale + scale // 2
    py = offset_y + gy * scale + scale // 2
    return ActionInput(id=GameAction.ACTION6, data={"x": px, "y": py})


# Witnesses (cell-coord based; smoke test converts to display pixels)
def witness_l1(g):
    return [click_cell(g, 1, 1), click_cell(g, 2, 1), click_cell(g, 5, 5)]


def witness_l2(g):
    return [click_cell(g, 4, 1), click_cell(g, 5, 1), click_cell(g, 1, 1), click_cell(g, 6, 2)]


def witness_l3(g):
    return [click_cell(g, 1, 1), click_cell(g, 2, 1),
            click_cell(g, 1, 5), click_cell(g, 2, 5),
            click_cell(g, 1, 9), click_cell(g, 2, 9), click_cell(g, 3, 9), click_cell(g, 4, 9)]


WITNESS_BUILDERS = {1: witness_l1, 2: witness_l2, 3: witness_l3}

# Trivial: ACTION4 (no-op) repeatedly
TRIVIAL_HEURISTICS = {2: [act(4)] * 15, 3: [act(4)] * 20}


results = {}


def run(name, fn):
    try:
        results[name] = fn()
    except Exception as e:
        results[name] = f"FAIL: {e}\n{traceback.format_exc()[:300]}"


def check_camera_viewport():
    g = fresh_game()
    g.handle_reset()
    for i, lvl in enumerate(g._levels):
        g._current_level_index = i
        g.on_set_level(lvl)
        gw, gh = lvl.grid_size
        assert g.camera.width == gw and g.camera.height == gh
    return "PASS"


def check_sprite_content():
    g = fresh_game()
    for i, lvl in enumerate(g._levels):
        assert len(lvl.get_sprites()) > 0
    return "PASS"


def check_action_branches():
    txt = src.read_text()
    for n in [4, 6]:
        assert f"GameAction.ACTION{n}" in txt
    return "PASS"


def check_action_runtime():
    g = fresh_game()
    g.handle_reset()
    for n in [4, 6]:
        if n == 6:
            g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 30, "y": 30}))
        else:
            g.perform_action(act(n))
    return "PASS"


def check_palette_range():
    g = fresh_game()
    g.handle_reset()
    frame = g.camera.render(g.current_level.get_sprites())
    oor = ((frame < 0) | (frame > 15)).sum()
    assert oor == 0
    return "PASS"


def check_win_path_exists():
    txt = src.read_text()
    assert "self.next_level()" in txt or "self.win()" in txt
    return "PASS"


def check_witness_wins():
    g = fresh_game()
    g.handle_reset()
    failures = []
    for level_idx in range(1, 4):
        score_before = g._score
        if score_before != level_idx - 1:
            failures.append(f"L{level_idx}: score_before={score_before}")
            break
        for ai in WITNESS_BUILDERS[level_idx](g):
            g.perform_action(ai)
        if level_idx < 3:
            if g._score != level_idx:
                failures.append(f"L{level_idx}: witness did not advance (score {score_before}->{g._score}, state={g._state.name})")
                break
        else:
            if g._state.name != "WIN":
                failures.append(f"L{level_idx}: witness did not WIN (state={g._state.name}, score={g._score})")
                break
    if failures:
        return f"FAIL: {failures}"
    return "PASS"


def check_trivial_fails():
    failures = []
    for level_idx in (2, 3):
        g = fresh_game()
        g.handle_reset()
        for prior in range(1, level_idx):
            for ai in WITNESS_BUILDERS[prior](g):
                g.perform_action(ai)
        score_before = g._score
        for ai in TRIVIAL_HEURISTICS[level_idx]:
            g.perform_action(ai)
            if g._score > score_before or g._state.name == "WIN":
                break
        if g._score > score_before:
            failures.append(f"L{level_idx}: trivial ADVANCED")
        elif g._state.name == "WIN":
            failures.append(f"L{level_idx}: trivial reached WIN")
    if failures:
        return f"FAIL: {failures}"
    return "PASS"


def check_lose_path_exists():
    txt = src.read_text()
    assert "self.lose()" in txt
    return "PASS"


def check_camera_default():
    txt = src.read_text()
    assert "self.camera.width" in txt and "self.camera.height" in txt
    return "PASS"


def check_class_name_loader():
    pascal = "dx8m"[0].upper() + "dx8m"[1:]
    assert hasattr(mod, pascal), f"Expected `{pascal}`"
    return "PASS"


def custom_click_toggles_cell():
    g = fresh_game()
    g.handle_reset()
    # L1 cell at (1,1) starts off
    assert not g._is_cell_on(1, 1)
    g.perform_action(click_cell(g, 1, 1))
    assert g._is_cell_on(1, 1), "Cell (1,1) should be on after click"
    g.perform_action(click_cell(g, 1, 1))
    assert not g._is_cell_on(1, 1), "Cell (1,1) should be off after second click"
    return "PASS"


def custom_l3_reference_invariant():
    """Region C requires count = on_count(A) + on_count(B); changing A/B changes C's required."""
    g = fresh_game()
    g.handle_reset()
    # Advance to L3
    for ai in WITNESS_BUILDERS[1](g):
        g.perform_action(ai)
    for ai in WITNESS_BUILDERS[2](g):
        g.perform_action(ai)
    assert g._current_level_index == 2
    # On L3, before any clicks: A on=0, B on=0, so C requires 0. Currently C on=0. Region C should be satisfied.
    regions = mod.LEVEL_REGIONS[2]
    region_c = next(r for r in regions if r["name"] == "C")
    assert g._region_required(region_c, regions) == 0, f"C should require 0 initially, got {g._region_required(region_c, regions)}"
    # Toggle one cell in A: A on=1, B on=0, C requires 1.
    g.perform_action(click_cell(g, 1, 1))
    assert g._region_required(region_c, regions) == 1, f"C should require 1 after A toggle"
    return "PASS"


run("CHECK_CAMERA_VIEWPORT", check_camera_viewport)
run("CHECK_SPRITE_CONTENT", check_sprite_content)
run("CHECK_ACTION_BRANCHES", check_action_branches)
run("CHECK_ACTION_RUNTIME", check_action_runtime)
run("CHECK_PALETTE_RANGE", check_palette_range)
run("CHECK_WIN_PATH_EXISTS", check_win_path_exists)
run("CHECK_WITNESS_WINS", check_witness_wins)
run("CHECK_TRIVIAL_FAILS", check_trivial_fails)
run("CHECK_LOSE_PATH_EXISTS", check_lose_path_exists)
run("CHECK_CAMERA_DEFAULT", check_camera_default)
run("CHECK_CLASS_NAME_LOADER", check_class_name_loader)
results["CHECK_VISUAL_SANITY"] = "SKIPPED (manual)"
run("custom_click_toggles_cell", custom_click_toggles_cell)
run("custom_l3_reference_invariant", custom_l3_reference_invariant)

print("=" * 70)
print("SMOKE TEST — dx8m")
print("=" * 70)
for k, v in results.items():
    marker = "✅" if v == "PASS" else ("⏭️ " if v.startswith("SKIPPED") else "❌")
    print(f"{marker} {k}: {v[:200]}")
print()
fails = sum(1 for v in results.values() if v.startswith("FAIL"))
passes = sum(1 for v in results.values() if v == "PASS")
skips = sum(1 for v in results.values() if v.startswith("SKIPPED"))
print(f"{passes} PASS, {fails} FAIL, {skips} SKIPPED")
sys.exit(0 if fails == 0 else 1)
