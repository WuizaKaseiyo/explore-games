"""Smoke test runner — universal + custom checks for wj7d."""
import sys
from pathlib import Path

# Import the game under test
import importlib.util
src = Path("prior-games/wj7d/wj7d.py")
spec = importlib.util.spec_from_file_location("smoke_wj7d", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = getattr(mod, "Wj7d")

# Import custom checks
sys.path.insert(0, "runs/2026-05-08T00-24-04/workspace")
import smoke_test_custom as custom

import numpy as np
from novaengine import GameAction, InteractionMode
from novaengine.enums import ActionInput

# ---------- Setup ----------
g = GameClass()
LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)
N_LEVELS = len(g._levels)
src_text = src.read_text()

results = []
def record(name, level, status, observed=""):
    results.append((name, level, status, observed))

# ---------- 1. CHECK_CAMERA_VIEWPORT ----------
for L in range(N_LEVELS):
    g.set_level(L)
    gw, gh = g.current_level.grid_size or (64, 64)
    cam_w, cam_h = g.camera._width, g.camera._height
    match = (cam_w == gw and cam_h == gh)
    record("CHECK_CAMERA_VIEWPORT", L+1, "PASS" if match else "FAIL",
           f"camera ({cam_w},{cam_h}) vs grid ({gw},{gh})")

# ---------- 2. CHECK_SPRITE_CONTENT ----------
for L in range(N_LEVELS):
    g.set_level(L)
    frame = g.camera.render(g.current_level.get_sprites())
    distinct = set(np.unique(frame[frame != LETTER_BOX]).tolist())
    record("CHECK_SPRITE_CONTENT", L+1,
           "PASS" if len(distinct) >= 2 else "FAIL",
           f"{len(distinct)} distinct: {sorted(distinct)}")

# ---------- 3. CHECK_ACTION_BRANCHES ----------
declared = list(g._available_actions)
for action_id in declared:
    needle = f"GameAction.ACTION{action_id}"
    record("CHECK_ACTION_BRANCHES", f"A{action_id}",
           "PASS" if needle in src_text else "FAIL", needle)

# ---------- 4. CHECK_ACTION_RUNTIME ----------
for action_id in declared:
    g_fresh = GameClass()
    try:
        if action_id == 6:
            g_fresh.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}))
        else:
            g_fresh.perform_action(ActionInput(id=GameAction.from_id(action_id)))
        record("CHECK_ACTION_RUNTIME", f"A{action_id}", "PASS", "no exception")
    except Exception as e:
        record("CHECK_ACTION_RUNTIME", f"A{action_id}", "FAIL", repr(e))

# ---------- 5. CHECK_PALETTE_RANGE ----------
for L in range(N_LEVELS):
    g.set_level(L)
    frame = g.camera.render(g.current_level.get_sprites())
    mn, mx = int(frame.min()), int(frame.max())
    record("CHECK_PALETTE_RANGE", L+1,
           "PASS" if (mn >= 0 and mx <= 15) else "FAIL",
           f"[{mn}, {mx}]")

# ---------- 6. CHECK_WIN_PATH_EXISTS ----------
has_next_level = "self.next_level()" in src_text
has_win = "self.win()" in src_text
record("CHECK_WIN_PATH_EXISTS", "all",
       "PASS" if (has_next_level or has_win) else "FAIL",
       f"next_level={has_next_level} win={has_win}")

# ---------- 7. CHECK_WITNESS_WINS ----------
A = GameAction
def click(x, y): return ActionInput(id=A.ACTION6, data={"x": x, "y": y})
def act(n): return ActionInput(id=A.from_id(n))

WITNESSES = {
    1: [act(4)]*4 + [act(2), act(5)],
    2: [click(24, 24), act(1), act(1), act(3), act(3), act(5),
        click(8, 4), act(4), act(4), act(4), act(4), act(2), act(2), act(2), act(2), act(5)],
    3: [click(32, 31), act(1),
        click(40, 8), act(5),
        click(33, 27), click(33, 27),
        click(16, 12), act(2), act(5)],
}

g2 = GameClass()
g2.handle_reset()
witness_failures = []
for level_idx in range(1, N_LEVELS + 1):
    score_before = g2._score
    if score_before != level_idx - 1:
        witness_failures.append(f"L{level_idx}: pre-score={score_before}, expected {level_idx-1}")
        break
    for ai in WITNESSES[level_idx]:
        g2.perform_action(ai)
    if level_idx < N_LEVELS:
        if g2._score != level_idx:
            witness_failures.append(f"L{level_idx}: did not advance, score={g2._score}, state={g2._state.name}")
            break
    else:
        if g2._state.name != "WIN":
            witness_failures.append(f"L{level_idx}: did not WIN, state={g2._state.name}, score={g2._score}")
            break
record("CHECK_WITNESS_WINS", "all",
       "PASS" if not witness_failures else "FAIL",
       "; ".join(witness_failures) if witness_failures else "all 3 witnesses won")

# ---------- 8. CHECK_LOSE_PATH_EXISTS ----------
record("CHECK_LOSE_PATH_EXISTS", "all",
       "PASS" if "self.lose()" in src_text else "FAIL",
       "lose() found" if "self.lose()" in src_text else "lose() missing")

# ---------- 9. CHECK_CAMERA_DEFAULT ----------
needs_per_level_camera = any(
    g._levels[i].grid_size != g._levels[0].grid_size
    for i in range(1, N_LEVELS)
)
if needs_per_level_camera:
    has_resize = ("self.camera.width" in src_text and "self.camera.height" in src_text)
    record("CHECK_CAMERA_DEFAULT", "all",
           "PASS" if has_resize else "FAIL",
           "per-level resize present" if has_resize else "missing")
else:
    record("CHECK_CAMERA_DEFAULT", "all", "PASS", "all levels same grid_size")

# ---------- 10. CHECK_VISUAL_SANITY (rendering only; agent inspects PNGs) ----------
out_dir = Path("runs/2026-05-08T00-24-04/workspace/smoke-frames")
out_dir.mkdir(parents=True, exist_ok=True)
PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)
try:
    from PIL import Image
    g3 = GameClass()
    for L in range(min(3, N_LEVELS)):
        g3.set_level(L)
        frame = g3.camera.render(g3.current_level.get_sprites())
        rgb = PALETTE[frame.clip(0, 15)]
        img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
        img.save(out_dir / f"level_{L+1}.png")
    record("CHECK_VISUAL_SANITY", "all", "RENDERED",
           f"see {out_dir}/level_*.png; agent inspection pending")
except Exception as e:
    record("CHECK_VISUAL_SANITY", "all", "FAIL", repr(e))

# ---------- Custom checks ----------
for fn_name in [
    "check_arrow_moves_selected_stamp",
    "check_click_selects_stamp_at_l2",
    "check_fold_consumes_stamp",
    "check_collision_blocks_stamp_into_other",
]:
    fn = getattr(custom, fn_name)
    try:
        passed, observed = fn(GameClass)
        record(fn_name, "custom", "PASS" if passed else "FAIL", observed)
    except Exception as e:
        record(fn_name, "custom", "FAIL", repr(e))

# ---------- Print results ----------
for name, level, status, obs in results:
    print(f"{status:6} {name} L={level} | {obs}")

n_fail = sum(1 for r in results if r[2] == "FAIL")
print(f"\n{'='*60}\nFAILURES: {n_fail}/{len(results)}")
