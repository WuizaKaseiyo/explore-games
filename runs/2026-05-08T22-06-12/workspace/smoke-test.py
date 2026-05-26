"""Smoke test for cy3k — 11 universal + custom."""

import importlib.util
import sys
import traceback
from pathlib import Path

import numpy as np

src = Path("prior-games/cy3k/cy3k.py")
spec_loader = importlib.util.spec_from_file_location("smoke_cy3k", src)
mod = importlib.util.module_from_spec(spec_loader)
spec_loader.loader.exec_module(mod)
GameClass = mod.Cy3k

from novaengine import ActionInput, GameAction


def fresh_game():
    return GameClass()


def act(n):
    return ActionInput(id=GameAction.from_id(n), data={})


# Witnesses (cycle each cluster once, in order A→C→D→B)
WITNESSES = {
    1: ([act(5)] +              # cycle A from (0,0)
        [act(4)] * 3 +           # walk to (3,0)
        [act(5)] +              # cycle C
        [act(2)] * 3 +           # walk south to (3,3)
        [act(5)] +              # cycle D
        [act(3)] * 3 +           # walk west to (0,3)
        [act(5)]),              # cycle B
    2: ([act(5)] +              # cycle A from (2,1) — fixed cell at (0,0) stays yellow
        [act(4)] * 1 +           # walk east 1 to (3,1)
        [act(5)] +              # cycle C
        [act(2)] * 2 +           # walk south to (3,3)
        [act(5)] +              # cycle D — fixed (5,5) stays green
        [act(3)] * 3 +           # walk west to (0,3)
        [act(5)]),              # cycle B
    3: ([act(5)] +              # cycle A from (2,2): A→green
        [act(2), act(2)] +       # walk south to (2,4) in B
        [act(5)] +              # cycle B: purple→yellow (BEFORE C, to avoid B-C fusion via transparent)
        [act(4), act(4)] +       # walk east to (4,4) in D
        [act(1)] +              # walk north to (4,3) in C
        [act(5)] +              # cycle C: red→purple
        [act(2)] +              # walk south to (4,4)
        [act(5)]),              # cycle D: green→red
}

TRIVIAL_HEURISTICS = {
    2: [act(4)] * 14,
    3: [act(4)] * 20,
}

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
    for n in [1, 2, 3, 4, 5]:
        assert f"GameAction.ACTION{n}" in txt
    return "PASS"


def check_action_runtime():
    g = fresh_game()
    g.handle_reset()
    for n in [1, 2, 3, 4, 5]:
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
        for ai in WITNESSES[level_idx]:
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
            for ai in WITNESSES[prior]:
                g.perform_action(ai)
        score_before = g._score
        for ai in TRIVIAL_HEURISTICS[level_idx]:
            g.perform_action(ai)
            if g._score > score_before or g._state.name == "WIN":
                break
        if g._score > score_before:
            failures.append(f"L{level_idx}: trivial ADVANCED (score {score_before}->{g._score})")
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
    """Loader expects Pascal-case class name derived from game_id."""
    pascal = "cy3k"[0].upper() + "cy3k"[1:]
    assert hasattr(mod, pascal), f"Expected class `{pascal}` but module has: {[n for n in dir(mod) if not n.startswith('_')]}"
    return "PASS"


def custom_action5_cycles_cluster():
    """ACTION5 at cursor cycles entire 4-connected same-color cluster."""
    g = fresh_game()
    g.handle_reset()
    cursor = g._cursor()
    # L1 cursor at (0,0). Cluster A (yellow) covers x<3, y<3 = 9 cells.
    g.perform_action(act(5))
    # All 9 cells should now be green (yellow+1)
    yellow_count = 0
    green_count = 0
    for x in range(3):
        for y in range(3):
            c = g._color_at(x, y)
            if c == 11:
                yellow_count += 1
            elif c == 14:
                green_count += 1
    assert green_count == 9, f"Expected 9 green cells in cluster A, got {green_count} (yellow={yellow_count})"
    return "PASS"


def custom_l2_fixed_cell_doesnt_cycle():
    """Fixed cell at (0,0) stays at original colour even when its cluster cycles."""
    g = fresh_game()
    g.handle_reset()
    # Advance to L2 by running L1 witness
    for ai in WITNESSES[1]:
        g.perform_action(ai)
    assert g._current_level_index == 1, f"Should be on L2; got idx {g._current_level_index}"
    # On L2, cursor at (2,1). Cycle cluster A.
    g.perform_action(act(5))
    c00 = g._color_at(0, 0)
    assert c00 == 11, f"Fixed cell (0,0) should stay yellow (11), got {c00}"
    # Other cluster A cells should be green (cycled)
    c11 = g._color_at(1, 1)
    assert c11 == 14, f"Non-fixed (1,1) should be green (14), got {c11}"
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
run("custom_action5_cycles_cluster", custom_action5_cycles_cluster)
run("custom_l2_fixed_cell_doesnt_cycle", custom_l2_fixed_cell_doesnt_cycle)

print("=" * 70)
print("SMOKE TEST — cy3k")
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
