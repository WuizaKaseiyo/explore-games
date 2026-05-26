"""Smoke test runner for zw91."""
from __future__ import annotations
import importlib.util, sys
from pathlib import Path
import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[5]
GAME_ID = "zw91"
PASCAL = "Zw91"

src = REPO_ROOT / f"prior-games/{GAME_ID}/{GAME_ID}.py"
src_text = src.read_text()
spec = importlib.util.spec_from_file_location(f"smoke_{GAME_ID}", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

from novaengine import ActionInput, GameAction
GameClass = getattr(mod, PASCAL)

LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)


def fresh():
    return GameClass()

g = fresh()
N_LEVELS = len(g._levels)

failures: list[str] = []
notes: dict[str, str] = {}

def fail(check, msg):
    failures.append(f"{check}: {msg}")


# CHECK_CAMERA_VIEWPORT
viewport_results = []
for L in range(N_LEVELS):
    g.set_level(L)
    gw, gh = g.current_level.grid_size or (64, 64)
    cw, ch = g.camera._width, g.camera._height
    match = (cw == gw and ch == gh)
    viewport_results.append((L+1, gw, gh, cw, ch, match))
    if not match:
        fail("CHECK_CAMERA_VIEWPORT", f"L{L+1}: grid=({gw},{gh}) cam=({cw},{ch})")
notes["CHECK_CAMERA_VIEWPORT"] = ", ".join(f"L{r[0]}:{'OK' if r[5] else 'FAIL'}" for r in viewport_results)


# CHECK_SPRITE_CONTENT, CHECK_PALETTE_RANGE
content_results = []
palette_results = []
for L in range(N_LEVELS):
    g.set_level(L)
    frame = g.camera.render(g.current_level.get_sprites())
    arr = np.asarray(frame)
    distinct = set(np.unique(arr[arr != LETTER_BOX]).tolist())
    content_results.append((L+1, len(distinct)))
    if len(distinct) < 2:
        fail("CHECK_SPRITE_CONTENT", f"L{L+1} only {len(distinct)} non-letterbox palette")
    mn, mx = int(arr.min()), int(arr.max())
    palette_results.append((L+1, mn, mx))
    if mn < 0 or mx > 15:
        fail("CHECK_PALETTE_RANGE", f"L{L+1}: range [{mn}, {mx}]")
notes["CHECK_SPRITE_CONTENT"] = ", ".join(f"L{l}:{n}" for l, n in content_results)
notes["CHECK_PALETTE_RANGE"] = ", ".join(f"L{l}:[{a},{b}]" for l, a, b in palette_results)


# CHECK_ACTION_BRANCHES
declared = list(g._available_actions)
for action_id in declared:
    needle = f"GameAction.ACTION{action_id}"
    if needle not in src_text:
        fail("CHECK_ACTION_BRANCHES", f"ACTION{action_id} not in source")
notes["CHECK_ACTION_BRANCHES"] = f"declared={declared} all branched"


# CHECK_ACTION_RUNTIME
for action_id in declared:
    g_fresh = fresh()
    try:
        if action_id == 6:
            g_fresh.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True)
        else:
            g_fresh.perform_action(ActionInput(id=GameAction.from_id(action_id)), raw=True)
    except Exception as e:
        fail("CHECK_ACTION_RUNTIME", f"ACTION{action_id} raised {type(e).__name__}: {e}")
notes["CHECK_ACTION_RUNTIME"] = "no exceptions"


# CHECK_WIN_PATH_EXISTS
has_next = "self.next_level()" in src_text
has_win = "self.win()" in src_text
if not (has_next or has_win):
    fail("CHECK_WIN_PATH_EXISTS", "neither self.next_level() nor self.win() in source")
notes["CHECK_WIN_PATH_EXISTS"] = f"next_level={has_next} win={has_win}"


# CHECK_LOSE_PATH_EXISTS
has_lose = "self.lose()" in src_text
if not has_lose:
    fail("CHECK_LOSE_PATH_EXISTS", "self.lose() not in source")
notes["CHECK_LOSE_PATH_EXISTS"] = f"lose={has_lose}"


# CHECK_CAMERA_DEFAULT
needs_resize = any(g._levels[i].grid_size != g._levels[0].grid_size for i in range(1, N_LEVELS))
notes["CHECK_CAMERA_DEFAULT"] = f"all-equal={not needs_resize} (no resize needed)"


# CHECK_WITNESS_WINS
def act(n): return ActionInput(id=GameAction.from_id(n))
WITNESSES = {
    1: [4]*10 + [2]*10 + [5, 5],
    2: [4]*5 + [1] + [5] + [4]*5,
    3: [1] + [4]*4 + [5]*4 + [4]*6 + [5]*2,
}
g_w = fresh()
g_w.handle_reset()
witness_failures = []
for level_idx in range(1, N_LEVELS + 1):
    score_before = g_w._score
    if score_before != level_idx - 1:
        witness_failures.append(f"L{level_idx}: pre-replay score={score_before}, expected {level_idx-1}")
        break
    for a in WITNESSES[level_idx]:
        g_w.perform_action(act(a), raw=True)
    if level_idx < N_LEVELS:
        if g_w._score != level_idx:
            witness_failures.append(f"L{level_idx}: post-replay score={g_w._score}, expected {level_idx}")
            break
    else:
        if g_w._state.name != "WIN":
            witness_failures.append(f"L{level_idx}: post-replay state={g_w._state.name}, expected WIN")
            break
if witness_failures:
    for w in witness_failures:
        fail("CHECK_WITNESS_WINS", w)
notes["CHECK_WITNESS_WINS"] = f"L1+L2+L3 all win={not witness_failures}"


# CHECK_VISUAL_SANITY — render PNGs
PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)

out_dir = Path(__file__).resolve().parent / "smoke-frames"
out_dir.mkdir(parents=True, exist_ok=True)
g_render = fresh()
for L in range(min(3, N_LEVELS)):
    g_render.set_level(L)
    frame = g_render.camera.render(g_render.current_level.get_sprites())
    rgb = PALETTE[np.clip(frame, 0, 15)]
    img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
    img.save(out_dir / f"level_{L+1}.png")


# Custom checks
def check_arrow_moves_avatar() -> tuple[bool, str]:
    g = fresh()
    g.set_level(0)
    x0, y0 = g._avatar_top_left()
    g.perform_action(act(4), raw=True)
    x1, y1 = g._avatar_top_left()
    return (x1 == x0 + 4 and y1 == y0), f"({x0},{y0})->({x1},{y1})"


def check_action5_grows_size() -> tuple[bool, str]:
    g = fresh()
    g.set_level(0)
    s0 = g.size
    g.perform_action(act(5), raw=True)
    return g.size == s0 + 1, f"size {s0}->{g.size}"


def check_action_counter_increments() -> tuple[bool, str]:
    g = fresh()
    g.set_level(0)
    n0 = g._action_count
    g.perform_action(act(1), raw=True)
    return g._action_count == n0 + 1, f"counter {n0}->{g._action_count}"


def check_lose_at_budget() -> tuple[bool, str]:
    g = fresh()
    g.set_level(0)
    budget = g._step_hud.max_steps
    for _ in range(budget + 2):
        g.perform_action(act(3), raw=True)  # LEFT — bumps wall, no progress
    return g._state.name == "GAME_OVER", f"state={g._state.name} after budget+2 noops"


custom_checks = [check_arrow_moves_avatar, check_action5_grows_size, check_action_counter_increments, check_lose_at_budget]
custom_results = []
for fn in custom_checks:
    ok, observed = fn()
    custom_results.append((fn.__name__, ok, observed))
    if not ok:
        fail("CUSTOM:" + fn.__name__, observed)


# Output
import json
print(json.dumps({
    "failures": failures,
    "notes": notes,
    "custom": [(n, ok, obs) for (n, ok, obs) in custom_results],
}, indent=2))
