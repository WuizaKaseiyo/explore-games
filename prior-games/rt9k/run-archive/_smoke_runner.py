"""Run universal + custom smoke checks for rt9k."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
from novaengine import ActionInput, GameAction
from PIL import Image


GAME_ID = "rt9k"
PASCAL = "Rt9k"
SRC = Path(f"prior-games/{GAME_ID}/{GAME_ID}.py")
spec = importlib.util.spec_from_file_location(f"smoke_{GAME_ID}", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = getattr(mod, PASCAL)
LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)

g = GameClass()
N_LEVELS = len(g._levels)


def _act(n, data=None):
    return ActionInput(id=GameAction.from_id(n), data=data or {})


def _render_initial_frame(game, level_idx):
    game.set_level(level_idx)
    return game.camera.render(game.current_level.get_sprites())


results = {}

# ----- CHECK_CAMERA_VIEWPORT -----
camera_ok = True
camera_details = []
for L in range(N_LEVELS):
    g.set_level(L)
    gw, gh = g.current_level.grid_size or (64, 64)
    cw, ch = g.camera._width, g.camera._height
    ok = cw == gw and ch == gh
    camera_ok = camera_ok and ok
    camera_details.append((L, (gw, gh), (cw, ch), ok))
results["CAMERA_VIEWPORT"] = (camera_ok, camera_details)

# ----- CHECK_SPRITE_CONTENT -----
content_details = []
content_ok = True
for L in range(N_LEVELS):
    g.set_level(L)
    frame = g.camera.render(g.current_level.get_sprites())
    distinct = set(np.unique(frame[frame != LETTER_BOX]).tolist())
    ok = len(distinct) >= 2
    content_ok = content_ok and ok
    content_details.append((L, len(distinct), distinct, ok))
results["SPRITE_CONTENT"] = (content_ok, content_details)

# ----- CHECK_ACTION_BRANCHES -----
src_text = SRC.read_text()
branch_details = []
branch_ok = True
for action_id in g._available_actions:
    needle = f"GameAction.ACTION{action_id}"
    has = needle in src_text
    branch_ok = branch_ok and has
    branch_details.append((action_id, has))
results["ACTION_BRANCHES"] = (branch_ok, branch_details)

# ----- CHECK_ACTION_RUNTIME -----
runtime_details = []
runtime_ok = True
for action_id in g._available_actions:
    g_fresh = GameClass()
    try:
        if action_id == 6:
            g_fresh.perform_action(_act(6, {"x": 32, "y": 32}), raw=True)
        else:
            g_fresh.perform_action(_act(action_id), raw=True)
        runtime_details.append((action_id, "OK"))
    except Exception as e:
        runtime_ok = False
        runtime_details.append((action_id, f"RAISED: {e!r}"))
results["ACTION_RUNTIME"] = (runtime_ok, runtime_details)

# ----- CHECK_PALETTE_RANGE -----
palette_details = []
palette_ok = True
for L in range(N_LEVELS):
    g.set_level(L)
    frame = g.camera.render(g.current_level.get_sprites())
    mn, mx = int(frame.min()), int(frame.max())
    ok = mn >= 0 and mx <= 15
    palette_ok = palette_ok and ok
    palette_details.append((L, mn, mx, ok))
results["PALETTE_RANGE"] = (palette_ok, palette_details)

# ----- CHECK_WIN_PATH_EXISTS -----
has_next = "self.next_level()" in src_text
has_win = "self.win()" in src_text
results["WIN_PATH_EXISTS"] = (has_next or has_win, (has_next, has_win))

# ----- CHECK_LOSE_PATH_EXISTS -----
has_lose = "self.lose()" in src_text
results["LOSE_PATH_EXISTS"] = (has_lose, has_lose)

# ----- CHECK_CAMERA_DEFAULT (per-level resize) -----
needs_per_level = any(g._levels[i].grid_size != g._levels[0].grid_size for i in range(1, N_LEVELS))
if needs_per_level:
    has_resize = "self.camera.width" in src_text and "self.camera.height" in src_text
else:
    has_resize = True  # all levels same grid_size; per-level resize not strictly needed.
results["CAMERA_DEFAULT"] = (has_resize, (needs_per_level, has_resize))

# ----- CHECK_WITNESS_WINS -----
WITNESSES = {
    1: [3] * 9,                                    # L1: 9 LEFT.
    2: [3] * 4 + [2] * 12,                         # L2: 4 LEFT + 12 DOWN.
    3: [3] * 4 + [1] * 15,                         # L3: 4 LEFT + 15 UP.
}
g.handle_reset()
witness_ok = True
witness_details = []
for level_idx in range(1, N_LEVELS + 1):
    score_before = g._score
    if score_before != level_idx - 1:
        witness_ok = False
        witness_details.append(f"L{level_idx}: pre-replay score={score_before} (expected {level_idx-1})")
        break
    for action_int in WITNESSES[level_idx]:
        g.perform_action(_act(action_int), raw=True)
    if level_idx < N_LEVELS:
        if g._score != level_idx:
            witness_ok = False
            witness_details.append(
                f"L{level_idx}: witness did not advance — score {score_before}->{g._score}, "
                f"state={g._state.name if hasattr(g._state,'name') else g._state}"
            )
            break
        else:
            witness_details.append(f"L{level_idx}: advanced score {score_before}->{g._score}")
    else:
        st_name = g._state.name if hasattr(g._state, "name") else str(g._state)
        if st_name != "WIN":
            witness_ok = False
            witness_details.append(f"L{level_idx}: did not reach WIN; state={st_name}, score={g._score}")
            break
        else:
            witness_details.append(f"L{level_idx}: reached WIN")
results["WITNESS_WINS"] = (witness_ok, witness_details)

# ----- Render frames for visual sanity -----
out_dir = Path("runs/2026-05-10T06-16-02/workspace/smoke-frames")
out_dir.mkdir(parents=True, exist_ok=True)

PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)

g_render = GameClass()
for L in range(N_LEVELS):
    g_render.set_level(L)
    frame = g_render.camera.render(g_render.current_level.get_sprites())
    rgb = PALETTE[frame.clip(0, 15)]
    img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
    img.save(out_dir / f"level_{L+1}.png")

# ----- Custom checks -----
custom_spec = importlib.util.spec_from_file_location(
    "rt9k_custom_smoke",
    "runs/2026-05-10T06-16-02/workspace/smoke-test-custom.py",
)
custom_mod = importlib.util.module_from_spec(custom_spec)
custom_spec.loader.exec_module(custom_mod)

custom_results = []
for name, fn in custom_mod.CHECKS:
    ok, observed = fn()
    custom_results.append((name, ok, observed))

results["CUSTOM"] = (all(r[1] for r in custom_results), custom_results)


# ----- Print summary -----
print("=== UNIVERSAL ===")
for k, (ok, det) in results.items():
    if k == "CUSTOM":
        continue
    print(f"  {k}: {'PASS' if ok else 'FAIL'}")
    if isinstance(det, list):
        for row in det:
            print(f"    - {row}")
    else:
        print(f"    - {det}")

print("=== CUSTOM ===")
for name, ok, observed in custom_results:
    print(f"  {'PASS' if ok else 'FAIL'} {name}: {observed}")
