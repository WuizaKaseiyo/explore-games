"""Smoke test runner for tb4k — executes universal + custom checks."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
from novaengine import ActionInput, GameAction
from PIL import Image

REPO_ROOT = Path("/Users/nickhe/Programming/NovaPlay-Agents")
src = REPO_ROOT / "prior-games/tb4k/tb4k.py"
WORKSPACE = REPO_ROOT / "runs/2026-05-12T10-38-16/workspace"
sys.path.insert(0, str(WORKSPACE))

spec = importlib.util.spec_from_file_location("smoke_tb4k", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = getattr(mod, "Tb4k")
LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)

results = {}


def fresh():
    return GameClass()


# ---- CHECK_CAMERA_VIEWPORT ----
g = fresh()
cam_match = []
for i in range(len(g._levels)):
    g.set_level(i)
    gw, gh = g.current_level.grid_size or (64, 64)
    cam_w, cam_h = g.camera._width, g.camera._height
    cam_match.append((cam_w == gw and cam_h == gh, (gw, gh), (cam_w, cam_h)))
results["CHECK_CAMERA_VIEWPORT"] = cam_match

# ---- CHECK_SPRITE_CONTENT ----
g = fresh()
content = []
for i in range(len(g._levels)):
    g.set_level(i)
    frame = g.camera.render(g.current_level.get_sprites())
    distinct = set(np.unique(frame[frame != LETTER_BOX]).tolist())
    content.append((len(distinct) >= 2, len(distinct), sorted(distinct)))
results["CHECK_SPRITE_CONTENT"] = content

# ---- CHECK_ACTION_BRANCHES ----
src_text = src.read_text()
declared = list(fresh()._available_actions)
branches = []
for action_id in declared:
    needle = f"GameAction.ACTION{action_id}"
    branches.append((needle in src_text, action_id))
results["CHECK_ACTION_BRANCHES"] = branches

# ---- CHECK_ACTION_RUNTIME ----
runtime = []
for action_id in declared:
    g_fresh = fresh()
    try:
        if action_id == 6:
            g_fresh.perform_action(
                ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True
            )
        else:
            g_fresh.perform_action(
                ActionInput(id=GameAction.from_id(action_id)), raw=True
            )
        runtime.append((True, action_id, None))
    except Exception as e:
        runtime.append((False, action_id, repr(e)))
results["CHECK_ACTION_RUNTIME"] = runtime

# ---- CHECK_PALETTE_RANGE ----
g = fresh()
palette = []
for i in range(len(g._levels)):
    g.set_level(i)
    frame = g.camera.render(g.current_level.get_sprites())
    mn, mx = int(frame.min()), int(frame.max())
    palette.append((mn >= 0 and mx <= 15, mn, mx))
results["CHECK_PALETTE_RANGE"] = palette

# ---- CHECK_WIN_PATH_EXISTS ----
results["CHECK_WIN_PATH_EXISTS"] = (
    "self.next_level()" in src_text or "self.win()" in src_text
)

# ---- CHECK_WITNESS_WINS ----
g = fresh()
WITNESSES = {
    1: [GameAction.ACTION4] * 8 + [GameAction.ACTION2] * 8,
    2: [GameAction.ACTION4] * 4
    + [GameAction.ACTION1] * 2
    + [GameAction.ACTION4] * 4
    + [GameAction.ACTION2] * 2
    + [GameAction.ACTION4] * 4,
    3: [GameAction.ACTION1] * 2
    + [GameAction.ACTION4] * 4
    + [GameAction.ACTION4] * 4
    + [GameAction.ACTION1] * 2
    + [GameAction.ACTION4] * 2,
}
witness_failures = []
N_LEVELS = len(g._levels)
g.handle_reset()
for level_idx in range(1, N_LEVELS + 1):
    score_before = g._score
    if score_before != level_idx - 1:
        witness_failures.append(
            f"L{level_idx}: expected score={level_idx-1} before replay, got {score_before}"
        )
        break
    for aid in WITNESSES[level_idx]:
        g.perform_action(ActionInput(id=aid))
    if level_idx < N_LEVELS:
        if g._score != level_idx:
            witness_failures.append(
                f"L{level_idx}: witness did not advance — score {score_before}→{g._score} (expected {level_idx}); state={g._state.name}"
            )
            break
    else:
        if g._state.name != "WIN":
            witness_failures.append(
                f"L{level_idx}: witness did not reach WIN — state={g._state.name} score={g._score}"
            )
            break
results["CHECK_WITNESS_WINS"] = witness_failures

# ---- CHECK_LOSE_PATH_EXISTS ----
results["CHECK_LOSE_PATH_EXISTS"] = "self.lose()" in src_text

# ---- CHECK_CAMERA_DEFAULT ----
g = fresh()
sizes = [g._levels[i].grid_size for i in range(len(g._levels))]
needs_resize = any(s != sizes[0] for s in sizes[1:])
if needs_resize:
    has_resize = (
        "self.camera.width" in src_text and "self.camera.height" in src_text
    )
    results["CHECK_CAMERA_DEFAULT"] = ("conditional", has_resize)
else:
    results["CHECK_CAMERA_DEFAULT"] = (
        "not_required",
        "self.camera.width" in src_text and "self.camera.height" in src_text,
    )

# ---- CHECK_VISUAL_SANITY — render frames ----
PALETTE = np.array(
    [
        (0xFF, 0xFF, 0xFF),
        (0xD2, 0xD2, 0xD2),
        (0xA0, 0xA0, 0xA0),
        (0x64, 0x64, 0x64),
        (0x3C, 0x3C, 0x3C),
        (0x00, 0x00, 0x00),
        (0xE5, 0x3A, 0xA3),
        (0xFF, 0x7B, 0xCC),
        (0xF9, 0x3C, 0x31),
        (0x1E, 0x93, 0xFF),
        (0x87, 0xD8, 0xF1),
        (0xFF, 0xDC, 0x00),
        (0xFF, 0x85, 0x1B),
        (0x92, 0x12, 0x31),
        (0x4F, 0xCC, 0x30),
        (0x88, 0x37, 0x9B),
    ],
    dtype=np.uint8,
)
out_dir = WORKSPACE / "smoke-frames"
out_dir.mkdir(parents=True, exist_ok=True)
g = fresh()
for L in range(min(3, N_LEVELS)):
    g.set_level(L)
    frame = g.camera.render(g.current_level.get_sprites())
    rgb = PALETTE[frame.clip(0, 15)]
    img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
    img.save(out_dir / f"level_{L+1}.png")
results["CHECK_VISUAL_SANITY"] = "frames rendered (agent to inspect)"

# ---- CUSTOM CHECKS ----
custom_spec = importlib.util.spec_from_file_location(
    "smoke_custom", WORKSPACE / "smoke-test-custom.py"
)
custom_mod = importlib.util.module_from_spec(custom_spec)
custom_spec.loader.exec_module(custom_mod)
custom_results = []
for fn in custom_mod.CUSTOM_CHECKS:
    passed, observed = fn(GameClass)
    custom_results.append((fn.__name__, passed, observed))
results["CUSTOM"] = custom_results


# ---- Print summary ----
import json

print(json.dumps({k: str(v) for k, v in results.items()}, indent=2))
