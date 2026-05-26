"""Smoke-test orchestration for xv2b."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
from novaengine import ActionInput, GameAction
from PIL import Image

ROOT = Path("/Users/nickhe/Programming/NovaPlay-Agents")
GAME_DIR = ROOT / "prior-games/xv2b"
SRC = GAME_DIR / "xv2b.py"

# Load module
spec = importlib.util.spec_from_file_location("smoke_xv2b", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = mod.Xv2b

g = GameClass()
LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)
N_LEVELS = len(g._levels)
src_text = SRC.read_text()

print(f"Loaded {SRC}, N_LEVELS={N_LEVELS}, LETTER_BOX={LETTER_BOX}, BG={BACKGROUND}")

# ------------------------------------------------------------------ #
# Universal checks                                                   #
# ------------------------------------------------------------------ #

results = []  # list of (check, level, passed, observed, threshold, diagnosis)


def record(check, level, passed, observed, threshold, diagnosis=""):
    results.append({
        "check": check, "level": level, "passed": passed,
        "observed": observed, "threshold": threshold, "diagnosis": diagnosis,
    })


# CHECK_CAMERA_VIEWPORT
for L in range(N_LEVELS):
    g.set_level(L)
    gw, gh = g.current_level.grid_size or (64, 64)
    cam_w, cam_h = g.camera._width, g.camera._height
    match = cam_w == gw and cam_h == gh
    record("CHECK_CAMERA_VIEWPORT", L + 1, match, f"camera ({cam_w},{cam_h}) grid ({gw},{gh})",
           "camera == grid_size", "" if match else "Camera viewport mismatch")

# CHECK_SPRITE_CONTENT
for L in range(N_LEVELS):
    g.set_level(L)
    frame = g.camera.render(g.current_level.get_sprites())
    distinct = set(np.unique(frame[frame != LETTER_BOX]).tolist())
    record("CHECK_SPRITE_CONTENT", L + 1, len(distinct) >= 2,
           f"{len(distinct)} distinct palettes", ">=2 distinct",
           "" if len(distinct) >= 2 else "no game content visible")

# CHECK_ACTION_BRANCHES
declared = list(g._available_actions)
all_branched = True
missing = []
for a in declared:
    if f"GameAction.ACTION{a}" not in src_text:
        all_branched = False
        missing.append(a)
record("CHECK_ACTION_BRANCHES", "all", all_branched,
       f"declared={declared}, missing branches={missing}",
       "every declared action has a branch", "" if all_branched else f"missing: {missing}")

# CHECK_ACTION_RUNTIME
runtime_pass = True
runtime_errs = []
for a in declared:
    g_fresh = GameClass()
    try:
        if a == 6:
            g_fresh.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True)
        else:
            g_fresh.perform_action(ActionInput(id=GameAction.from_id(a)), raw=True)
    except Exception as e:
        runtime_pass = False
        runtime_errs.append(f"ACTION{a}: {type(e).__name__}: {e}")
record("CHECK_ACTION_RUNTIME", "all", runtime_pass,
       "; ".join(runtime_errs) or "no exceptions",
       "no exceptions raised", "" if runtime_pass else "; ".join(runtime_errs))

# CHECK_PALETTE_RANGE
all_in_range = True
range_obs = []
for L in range(N_LEVELS):
    g.set_level(L)
    frame = g.camera.render(g.current_level.get_sprites())
    mn, mx = int(frame.min()), int(frame.max())
    range_obs.append(f"L{L+1}: {mn}..{mx}")
    if mn < 0 or mx > 15:
        all_in_range = False
record("CHECK_PALETTE_RANGE", "all", all_in_range, ", ".join(range_obs),
       "[0,15]", "" if all_in_range else "out-of-range palette")

# CHECK_WIN_PATH_EXISTS
has_win_path = "self.next_level()" in src_text or "self.win()" in src_text
record("CHECK_WIN_PATH_EXISTS", "all", has_win_path,
       "next_level/win in source", "present", "" if has_win_path else "no win path")

# CHECK_LOSE_PATH_EXISTS
has_lose = "self.lose()" in src_text
record("CHECK_LOSE_PATH_EXISTS", "all", has_lose,
       "lose in source", "present", "" if has_lose else "no lose path")

# CHECK_CAMERA_DEFAULT — only required if levels have different grid sizes
needs_resize = any(g._levels[i].grid_size != g._levels[0].grid_size for i in range(1, N_LEVELS))
if needs_resize:
    has_resize = "self.camera.width" in src_text and "self.camera.height" in src_text
    record("CHECK_CAMERA_DEFAULT", "all", has_resize, "resize present", "required", "" if has_resize else "missing")
else:
    record("CHECK_CAMERA_DEFAULT", "all", True, "all levels same grid size; no resize needed", "n/a", "")

# CHECK_WITNESS_WINS
def click(x, y):
    return ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y})
def act(n):
    return ActionInput(id=GameAction.from_id(n), data={})

# Witness coordinates: V_AB at (20, 40) closed; click at (21, 42).
# V_BC at (38, 40) closed; click at (39, 42).
# P_BC at (37, 18) (gap_x = GAP_BC_X - 1 = 37); click at (39, 19).
# Note: pump uses gap_x = GAP_BC_X - 1 = 38 - 1 = 37 in the LEVEL_DATA L3 entry.
WITNESSES = {
    1: [click(21, 42), click(39, 42)] + [act(5)] * 16,
    2: [click(39, 42)] + [act(5)] * 8,
    3: [click(21, 26)] + [act(5)] * 22 + [click(39, 19)] + [act(5)] * 3,
}
# Note for L3 V_AB: slit_h=15 → valve_y = 46-15-2 = 29. So V_AB sprite at (20, 29). click at (21, 31).
WITNESSES[3] = [click(21, 31)] + [act(5)] * 22 + [click(39, 19)] + [act(5)] * 3

g_w = GameClass()
g_w.handle_reset()
witness_pass = True
witness_diagnosis = ""
for level_idx in range(1, N_LEVELS + 1):
    score_before = g_w._score
    if score_before != level_idx - 1:
        witness_pass = False
        witness_diagnosis = f"L{level_idx}: expected score=={level_idx-1} got {score_before}"
        break
    for ai in WITNESSES[level_idx]:
        g_w.perform_action(ai)
    if level_idx < N_LEVELS:
        if g_w._score != level_idx:
            witness_pass = False
            witness_diagnosis = f"L{level_idx}: witness did not advance (score {score_before}->{g_w._score}, state {g_w._state.name})"
            break
    else:
        if g_w._state.name != "WIN":
            witness_pass = False
            witness_diagnosis = f"L{level_idx}: did not reach WIN (state {g_w._state.name}, score {g_w._score})"
            break

record("CHECK_WITNESS_WINS", "all", witness_pass,
       "all 3 witnesses advance" if witness_pass else witness_diagnosis,
       "every witness wins", witness_diagnosis)

# CHECK_VISUAL_SANITY — render frames; visual judgement done separately by the agent
PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)
out_dir = Path(__file__).parent / "smoke-frames"
out_dir.mkdir(parents=True, exist_ok=True)
for L in range(N_LEVELS):
    g.set_level(L)
    frame = g.camera.render(g.current_level.get_sprites())
    rgb = PALETTE[frame.clip(0, 15)]
    img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
    img.save(out_dir / f"level_{L+1}.png")
print(f"Wrote rendered frames to {out_dir}")

# ------------------------------------------------------------------ #
# Custom checks                                                      #
# ------------------------------------------------------------------ #

custom_dir = Path(__file__).parent
sys.path.insert(0, str(custom_dir))
from smoke_test_custom import (
    check_action6_toggles_valve,
    check_action5_with_open_valve_transfers,
    check_l2_drain_consumes,
    check_l3_pump_lifts_uphill,
)

custom_results = []
for fn in [
    check_action6_toggles_valve,
    check_action5_with_open_valve_transfers,
    check_l2_drain_consumes,
    check_l3_pump_lifts_uphill,
]:
    try:
        passed, observed = fn(GameClass)
    except Exception as e:
        passed = False
        observed = f"raised {type(e).__name__}: {e}"
    custom_results.append((fn.__name__, passed, observed, fn.__doc__ or ""))

# ------------------------------------------------------------------ #
# Print summary                                                      #
# ------------------------------------------------------------------ #

print()
print("=" * 70)
print("UNIVERSAL CHECKS")
print("=" * 70)
for r in results:
    status = "PASS" if r["passed"] else "FAIL"
    print(f"  [{status}] {r['check']:30s} (L{r['level']}) {r['observed']}")

print()
print("=" * 70)
print("CUSTOM CHECKS")
print("=" * 70)
for name, passed, observed, doc in custom_results:
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {name:48s} {observed}")

all_pass = all(r["passed"] for r in results) and all(p for _, p, _, _ in custom_results)
print()
print("=" * 70)
print(f"OVERALL: {'PASS' if all_pass else 'FAIL'}")
print("=" * 70)
sys.exit(0 if all_pass else 1)
