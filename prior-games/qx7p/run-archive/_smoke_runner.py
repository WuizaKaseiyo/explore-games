"""Run the universal + custom smoke checks for qx7p and report."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from novaengine import ActionInput, GameAction

REPO = Path.cwd()
GAME_ID = "qx7p"
PASCAL = "Qx7p"
SRC = REPO / f"prior-games/{GAME_ID}/{GAME_ID}.py"
WORKSPACE = REPO / "runs/2026-05-07T21-16-41/workspace"
SMOKE_FRAMES = WORKSPACE / "smoke-frames"
SMOKE_FRAMES.mkdir(parents=True, exist_ok=True)

# Load the game module.
spec = importlib.util.spec_from_file_location(f"smoke_{GAME_ID}", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = getattr(mod, PASCAL)
LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)
SRC_TEXT = SRC.read_text()

PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)


def render_level(g, level_idx: int) -> np.ndarray:
    g.set_level(level_idx)
    return g.camera.render(g.current_level.get_sprites())


def save_frame(level_idx: int, frame: np.ndarray) -> Path:
    rgb = PALETTE[frame.clip(0, 15)]
    img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
    out = SMOKE_FRAMES / f"level_{level_idx + 1}.png"
    img.save(out)
    return out


# ---------------------------------------------------------------------
# Universal checks
# ---------------------------------------------------------------------
results = {}

g = GameClass()
N_LEVELS = len(g._levels)

# 1. CHECK_CAMERA_VIEWPORT
viewport_rows = []
for L in range(N_LEVELS):
    g.set_level(L)
    gw, gh = g.current_level.grid_size or (64, 64)
    cw, ch = g.camera._width, g.camera._height
    viewport_rows.append((L + 1, gw, gh, cw, ch, gw == cw and gh == ch))
results["CHECK_CAMERA_VIEWPORT"] = viewport_rows

# 2. CHECK_SPRITE_CONTENT
sprite_rows = []
for L in range(N_LEVELS):
    frame = render_level(g, L)
    distinct = set(np.unique(frame[frame != LETTER_BOX]).tolist())
    sprite_rows.append((L + 1, len(distinct), len(distinct) >= 2))
results["CHECK_SPRITE_CONTENT"] = sprite_rows

# 3. CHECK_ACTION_BRANCHES
declared = list(g._available_actions)
branch_results = []
for action_id in declared:
    needle = f"GameAction.ACTION{action_id}"
    branch_results.append((action_id, needle in SRC_TEXT))
results["CHECK_ACTION_BRANCHES"] = branch_results

# 4. CHECK_ACTION_RUNTIME
runtime_results = []
for action_id in declared:
    g_fresh = GameClass()
    g_fresh.full_reset()
    try:
        if action_id == 6:
            g_fresh.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}))
        else:
            g_fresh.perform_action(ActionInput(id=GameAction.from_id(action_id), data={}))
        runtime_results.append((action_id, True, ""))
    except Exception as e:
        runtime_results.append((action_id, False, repr(e)))
results["CHECK_ACTION_RUNTIME"] = runtime_results

# 5. CHECK_PALETTE_RANGE
palette_rows = []
for L in range(N_LEVELS):
    frame = render_level(g, L)
    mn, mx = int(frame.min()), int(frame.max())
    palette_rows.append((L + 1, mn, mx, mn >= 0 and mx <= 15))
results["CHECK_PALETTE_RANGE"] = palette_rows

# 6. CHECK_WIN_PATH_EXISTS
results["CHECK_WIN_PATH_EXISTS"] = ("self.next_level()" in SRC_TEXT) or ("self.win()" in SRC_TEXT)

# 7. CHECK_WITNESS_WINS
A = GameAction
def click(x, y):
    return ActionInput(id=A.ACTION6, data={"x": x, "y": y})
def act(n):
    return ActionInput(id=A.from_id(n), data={})

# Witnesses extracted from spec:
#   L1: click(16,14), [ACTION1]*4, click(32,14), [ACTION2]*5, click(48,14), [ACTION1]*3
#   L2: click(12,14), [ACTION1]*4, click(40,14), [ACTION1]*6, click(54,14), [ACTION1]*2
#   L3: ACTION5, ACTION5, click(6,14), [ACTION2]*5, click(30,14), [ACTION2]*4, click(54,14), [ACTION2]*3
WITNESSES = {
    1: [click(16, 14)] + [act(1)] * 4 + [click(32, 14)] + [act(2)] * 5 + [click(48, 14)] + [act(1)] * 3,
    2: [click(12, 14)] + [act(1)] * 4 + [click(40, 14)] + [act(1)] * 6 + [click(54, 14)] + [act(1)] * 2,
    3: [act(5), act(5)] + [click(6, 14)] + [act(2)] * 5 + [click(30, 14)] + [act(2)] * 4 + [click(54, 14)] + [act(2)] * 3,
}

g_witness = GameClass()
g_witness.full_reset()
witness_failures = []
for L in range(1, N_LEVELS + 1):
    score_before = g_witness._score
    expected_before = L - 1
    if score_before != expected_before:
        witness_failures.append(f"L{L}: pre-replay _score={score_before}, expected {expected_before}")
        break
    for ai in WITNESSES[L]:
        g_witness.perform_action(ai)
    score_after = g_witness._score
    state_after = g_witness._state.name
    if L < N_LEVELS:
        if score_after != L:
            witness_failures.append(f"L{L}: post-replay _score={score_after}, expected {L}; state={state_after}")
            break
    else:
        if state_after != "WIN" and score_after != L:
            witness_failures.append(f"L{L}: final witness did not win (_score={score_after}, state={state_after})")
            break

results["CHECK_WITNESS_WINS"] = (witness_failures == [], witness_failures)

# 8. CHECK_LOSE_PATH_EXISTS
results["CHECK_LOSE_PATH_EXISTS"] = "self.lose()" in SRC_TEXT

# 9. CHECK_CAMERA_DEFAULT — all levels share same grid_size, no resize needed.
all_grid_sizes = [g._levels[i].grid_size for i in range(N_LEVELS)]
needs_resize = any(gs != all_grid_sizes[0] for gs in all_grid_sizes[1:])
if needs_resize:
    has_resize = ("self.camera.width" in SRC_TEXT and "self.camera.height" in SRC_TEXT)
    results["CHECK_CAMERA_DEFAULT"] = has_resize
else:
    results["CHECK_CAMERA_DEFAULT"] = True  # exempt — uniform 64x64

# 10. CHECK_VISUAL_SANITY — render PNGs; defer to agent inspection
saved = []
for L in range(N_LEVELS):
    frame = render_level(g, L)
    saved.append(save_frame(L, frame))
results["CHECK_VISUAL_SANITY_PNGS"] = saved

# ---------------------------------------------------------------------
# Custom checks
# ---------------------------------------------------------------------
# Load custom checks from smoke-test-custom.py.
custom_spec = importlib.util.spec_from_file_location(
    "smoke_custom", WORKSPACE / "smoke-test-custom.py"
)
custom_mod = importlib.util.module_from_spec(custom_spec)
custom_spec.loader.exec_module(custom_mod)

custom_results = {}
for fn_name in [n for n in dir(custom_mod) if n.startswith("check_")]:
    fn = getattr(custom_mod, fn_name)
    try:
        passed, observed = fn(GameClass)
        custom_results[fn_name] = (passed, observed, "")
    except Exception as e:
        custom_results[fn_name] = (False, "", repr(e))

results["CUSTOM"] = custom_results

# ---------------------------------------------------------------------
# Print
# ---------------------------------------------------------------------
import json
def _short(v):
    if isinstance(v, list):
        return [_short(x) for x in v]
    if isinstance(v, tuple):
        return tuple(_short(x) for x in v)
    if isinstance(v, dict):
        return {k: _short(x) for k, x in v.items()}
    if isinstance(v, Path):
        return str(v.relative_to(REPO))
    return v
print(json.dumps(_short(results), indent=2, default=str))
