"""Smoke test for tw94 — 11 universal + custom."""

import importlib.util
import sys
import traceback
from pathlib import Path

import numpy as np

src = Path("prior-games/tw94/tw94.py")
spec_loader = importlib.util.spec_from_file_location("smoke_tw94", src)
mod = importlib.util.module_from_spec(spec_loader)
spec_loader.loader.exec_module(mod)
GameClass = mod.Tw94

from novaengine import ActionInput, GameAction


def fresh_game():
    return GameClass()


def act(n):
    return ActionInput(id=GameAction.from_id(n), data={})


# Witnesses
WITNESSES = {
    1: [act(4)] * 5,  # 5 east pushes via wrap
    2: ([act(1)] +              # north 1
        [act(4)] * 8 +           # east 8
        [act(2)] * 4 +           # south 4 (now at (9,4))
        [act(4)] * 4 +           # 4 east pushes via wrap (crate_a delivered)
        [act(2)] * 5 +           # south 5
        [act(4)] * 3 +           # east 3 (now at (4,9))
        [act(2)] * 4),           # 4 south pushes via wrap (crate_b delivered)
    3: ([act(1)] +              # north 1
        [act(4)] * 8 +           # east 8
        [act(2)] * 4 +           # south 4
        [act(4)] * 6 +           # 6 east pushes via wrap (14x14 grid)
        [act(2)] * 5 +           # south 5
        [act(4)] * 3 +           # east 3
        [act(2)] * 6),           # 6 south pushes via wrap
}

TRIVIAL_HEURISTICS = {
    2: [act(4)] * 30,
    3: [act(4)] * 35,
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
    for n in [1, 2, 3, 4]:
        assert f"GameAction.ACTION{n}" in txt
    return "PASS"


def check_action_runtime():
    g = fresh_game()
    g.handle_reset()
    for n in [1, 2, 3, 4]:
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


def custom_horizontal_wrap_works_l1():
    """Pushing crate east beyond x=7 on L1 row 4 should wrap to x=0."""
    g = fresh_game()
    g.handle_reset()
    # Pre-conditions: L1, crate_a at (4,4), player at (3,4)
    # Push east 4 times to push crate from (4,4) to (0,4) via wrap
    for _ in range(4):
        g.perform_action(act(4))
    crate = g.current_level.get_sprites_by_tag("crate")[0]
    assert crate.x == 0 and crate.y == 4, f"Expected wrap to (0,4), got ({crate.x},{crate.y})"
    return "PASS"


def custom_l3_odd_row_no_wrap():
    """At L3, walking east at boundary on odd row should fail (no wrap)."""
    g = fresh_game()
    g.handle_reset()
    g._current_level_index = 2
    g.on_set_level(g._levels[2])
    # Move player to (13, 1) — odd row, east boundary
    g._player().set_position(13, 1)
    # ACTION4: try to walk east. Should fail (no H wrap on odd row 1 at L3).
    g.perform_action(act(4))
    p = g._player()
    assert p.x == 13 and p.y == 1, f"Expected stay at (13,1), got ({p.x},{p.y})"
    return "PASS"


def custom_l3_even_row_wraps():
    """At L3, walking east at boundary on even row should wrap."""
    g = fresh_game()
    g.handle_reset()
    g._current_level_index = 2
    g.on_set_level(g._levels[2])
    g._player().set_position(13, 0)  # even row 0
    g.perform_action(act(4))
    p = g._player()
    assert p.x == 0 and p.y == 0, f"Expected wrap to (0,0), got ({p.x},{p.y})"
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
results["CHECK_VISUAL_SANITY"] = "SKIPPED (manual)"
run("custom_horizontal_wrap_works_l1", custom_horizontal_wrap_works_l1)
run("custom_l3_odd_row_no_wrap", custom_l3_odd_row_no_wrap)
run("custom_l3_even_row_wraps", custom_l3_even_row_wraps)

print("=" * 70)
print("SMOKE TEST — tw94")
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
