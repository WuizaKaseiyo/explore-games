"""Smoke test for vy3m — 11 universal checks (incl. NEW CHECK_TRIVIAL_FAILS) + custom."""

import importlib.util
import sys
import traceback
from pathlib import Path

import numpy as np

src = Path("prior-games/vy3m/vy3m.py")
spec = importlib.util.spec_from_file_location("smoke_vy3m", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = mod.Vy3m

from novaengine import ActionInput, GameAction


def fresh_game():
    return GameClass()


def act(n):
    return ActionInput(id=GameAction.from_id(n), data={})


# Witness sequences from mechanic-spec.md § 4
WITNESSES = {
    1: [act(4)] * 5,                                                              # 2 walks + 3 pushes
    2: [act(4)] * 6 + [act(5)] + [act(3)] * 2,                                    # 2 walks + 4 pushes + cycle + 2 pulls
    3: [act(4)] * 6 + [act(5)] + [act(3)] * 2 + [act(5)] + [act(4)] * 4,         # push lane + cycle + pull lane + cycle + chain lane
}

# Trivial heuristic sequences from mechanic-spec.md § 4 per-level "Trivial heuristic"
TRIVIAL_HEURISTICS = {
    2: [act(4)] * 12,
    3: [act(4)] * 15,
}

results = {}


def run(name, fn):
    try:
        results[name] = fn()
    except Exception as e:
        results[name] = f"FAIL: {e}\n{traceback.format_exc()[:500]}"


def check_camera_viewport():
    g = fresh_game()
    g.handle_reset()
    for i, lvl in enumerate(g._levels):
        g._current_level_index = i
        g.on_set_level(lvl)
        gw, gh = lvl.grid_size
        assert g.camera.width == gw and g.camera.height == gh, f"L{i+1} camera mismatch"
    return "PASS"


def check_sprite_content():
    g = fresh_game()
    for i, lvl in enumerate(g._levels):
        assert len(lvl.get_sprites()) > 0, f"L{i+1} empty"
    return "PASS"


def check_action_branches():
    txt = src.read_text()
    for n in [1, 2, 3, 4, 5]:
        assert f"GameAction.ACTION{n}" in txt, f"ACTION{n} no branch"
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
    assert oor == 0, f"{oor} pixels OOR"
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
    """NEW CHECK from harness gate fix — trivial heuristics must NOT advance L2/L3."""
    failures = []
    for level_idx in (2, 3):
        g = fresh_game()
        g.handle_reset()
        # Replay prior witnesses to reach target level
        for prior in range(1, level_idx):
            for ai in WITNESSES[prior]:
                g.perform_action(ai)
        score_before = g._score
        # Now at start of level_idx. Replay trivial heuristic.
        for ai in TRIVIAL_HEURISTICS[level_idx]:
            g.perform_action(ai)
            if g._score > score_before or g._state.name == "WIN":
                break
        if g._score > score_before:
            failures.append(f"L{level_idx}: trivial heuristic ADVANCED level (score {score_before}->{g._score}). Level lacks planning.")
        elif g._state.name == "WIN":
            failures.append(f"L{level_idx}: trivial reached WIN. Level lacks planning.")
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


def custom_action5_cycles_class():
    g = fresh_game()
    g.handle_reset()
    g._current_level_index = 1
    g.on_set_level(g._levels[1])
    assert g._active_class == "pusher"
    g.perform_action(act(5))
    assert g._active_class == "puller", f"after cycle, expected puller got {g._active_class}"
    g.perform_action(act(5))
    assert g._active_class == "pusher", f"after 2nd cycle, expected pusher got {g._active_class}"
    return "PASS"


def custom_puller_blocked_by_crate_in_front():
    g = fresh_game()
    g.handle_reset()
    g._current_level_index = 1
    g.on_set_level(g._levels[1])
    g._active_class = "puller"
    puller = g._active_actor()
    assert puller.x == 4 and puller.y == 7
    # crate at (5,7) is east of puller (4,7). ACTION4 (right) into crate should be blocked.
    g.perform_action(act(4))
    puller_after = g.current_level.get_sprites_by_tag("puller")[0]
    assert puller_after.x == 4 and puller_after.y == 7, f"puller moved into crate, x={puller_after.x}"
    crate = g.current_level.get_sprites_by_tag("crate")[0]
    # In L2, crate_a (push lane) should still be at (4,2); crate_b (pull lane) still at (5,7)
    return "PASS"


def custom_stomper_chain_push():
    g = fresh_game()
    g.handle_reset()
    g._current_level_index = 2
    g.on_set_level(g._levels[2])
    g._active_class = "stomper"
    stomper = g._active_actor()
    assert stomper.x == 1 and stomper.y == 12
    # Walk east 1: stomper (1,12)→(2,12)
    g.perform_action(act(4))
    # Walk east 1: stomper attempts (3,12) — has crate1. Chain: crate2 at (4,12), beyond (5,12) empty.
    g.perform_action(act(4))
    # crate1 should now be at (4,12), crate2 at (5,12), stomper at (3,12)
    chain_crates = [c for c in g.current_level.get_sprites_by_tag("crate")
                    if c.name in ("crate_l3c1", "crate_l3c2")]
    positions = sorted([(c.x, c.y) for c in chain_crates])
    expected = sorted([(4, 12), (5, 12)])
    assert positions == expected, f"Chain crates at {positions}, expected {expected}"
    return "PASS"


# Run all checks
run("CHECK_CAMERA_VIEWPORT", check_camera_viewport)
run("CHECK_SPRITE_CONTENT", check_sprite_content)
run("CHECK_ACTION_BRANCHES", check_action_branches)
run("CHECK_ACTION_RUNTIME", check_action_runtime)
run("CHECK_PALETTE_RANGE", check_palette_range)
run("CHECK_WIN_PATH_EXISTS", check_win_path_exists)
run("CHECK_WITNESS_WINS", check_witness_wins)
run("CHECK_TRIVIAL_FAILS", check_trivial_fails)  # NEW
run("CHECK_LOSE_PATH_EXISTS", check_lose_path_exists)
run("CHECK_CAMERA_DEFAULT", check_camera_default)
results["CHECK_VISUAL_SANITY"] = "SKIPPED (vision pass — manual)"
run("custom_action5_cycles_class", custom_action5_cycles_class)
run("custom_puller_blocked_by_crate_in_front", custom_puller_blocked_by_crate_in_front)
run("custom_stomper_chain_push", custom_stomper_chain_push)

print("=" * 70)
print("SMOKE TEST — vy3m (with NEW CHECK_TRIVIAL_FAILS)")
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
