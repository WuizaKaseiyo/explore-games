"""Universal smoke checks for mr5q. Runs all 9 Tier-1 checks except
CHECK_VISUAL_SANITY which is performed separately by rendering frames
to PNG and inspecting them with vision."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
from novaengine import ActionInput, GameAction


SRC = Path("prior-games/mr5q/mr5q.py")
sp = importlib.util.spec_from_file_location("smoke_mr5q", SRC)
mod = importlib.util.module_from_spec(sp)
sp.loader.exec_module(mod)
GameClass = getattr(mod, "Mr5q")
LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)

src_text = SRC.read_text()


def report(check_id, results):
    print(f"\n=== {check_id} ===")
    for k, v in results.items():
        print(f"  {k}: {v}")


# ---- 1. CHECK_CAMERA_VIEWPORT ----
g = GameClass()
N_LEVELS = len(g._levels)
results = {}
for i in range(N_LEVELS):
    g.set_level(i)
    gw, gh = g.current_level.grid_size or (64, 64)
    cam_w, cam_h = g.camera._width, g.camera._height
    match = (cam_w == gw and cam_h == gh)
    results[f"L{i+1}"] = f"cam=({cam_w},{cam_h}) grid=({gw},{gh}) match={match}"
report("CHECK_CAMERA_VIEWPORT", results)

# ---- 2. CHECK_SPRITE_CONTENT ----
results = {}
g = GameClass()
for i in range(N_LEVELS):
    g.set_level(i)
    frame = g.camera.render(g.current_level.get_sprites())
    arr = np.array(frame)
    distinct = set(np.unique(arr[arr != LETTER_BOX]).tolist())
    results[f"L{i+1}"] = f"distinct non-letterbox palettes = {distinct} (count={len(distinct)})"
report("CHECK_SPRITE_CONTENT", results)

# ---- 3. CHECK_ACTION_BRANCHES ----
g = GameClass()
declared = list(g._available_actions)
results = {}
for action_id in declared:
    needle = f"GameAction.ACTION{action_id}"
    results[f"ACTION{action_id}"] = f"in source: {needle in src_text}"
report("CHECK_ACTION_BRANCHES", results)

# ---- 4. CHECK_ACTION_RUNTIME ----
results = {}
for action_id in declared:
    g = GameClass()
    try:
        if action_id == 6:
            g.perform_action(
                ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}),
                raw=True,
            )
        else:
            g.perform_action(ActionInput(id=GameAction.from_id(action_id)), raw=True)
        results[f"ACTION{action_id}"] = "no exception"
    except Exception as exc:
        results[f"ACTION{action_id}"] = f"raised {type(exc).__name__}: {exc}"
report("CHECK_ACTION_RUNTIME", results)

# ---- 5. CHECK_PALETTE_RANGE ----
results = {}
g = GameClass()
for i in range(N_LEVELS):
    g.set_level(i)
    frame = g.camera.render(g.current_level.get_sprites())
    arr = np.array(frame)
    mn, mx = int(arr.min()), int(arr.max())
    results[f"L{i+1}"] = f"min={mn}, max={mx}, in [0,15]={(mn>=0 and mx<=15)}"
report("CHECK_PALETTE_RANGE", results)

# ---- 6. CHECK_WIN_PATH_EXISTS ----
print(f"\n=== CHECK_WIN_PATH_EXISTS ===")
print(f"  next_level() in source: {'self.next_level()' in src_text}")
print(f"  win() in source: {'self.win()' in src_text}")

# ---- 7. CHECK_LOSE_PATH_EXISTS ----
print(f"\n=== CHECK_LOSE_PATH_EXISTS ===")
print(f"  lose() in source: {'self.lose()' in src_text}")

# ---- 8. CHECK_CAMERA_DEFAULT ----
g = GameClass()
sizes = [g._levels[i].grid_size for i in range(N_LEVELS)]
needs_per_level = any(sizes[i] != sizes[0] for i in range(1, N_LEVELS))
print(f"\n=== CHECK_CAMERA_DEFAULT ===")
print(f"  level grid_sizes: {sizes}")
print(f"  needs_per_level_camera: {needs_per_level}")
print(f"  source mutates self.camera.width: {'self.camera.width' in src_text}")
print(f"  source mutates self.camera.height: {'self.camera.height' in src_text}")
