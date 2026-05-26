"""Run the 9 universal smoke checks for gv47 and emit pass/fail summary."""
import importlib.util
from pathlib import Path

import numpy as np
from PIL import Image

from novaengine import ActionInput, GameAction


SRC = Path("prior-games/gv47/gv47.py")
spec = importlib.util.spec_from_file_location("smoke_gv47", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = mod.Gv47
src_text = SRC.read_text()
LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)

g = GameClass()
N_LEVELS = len(g._levels)

results = []


def fail(check, level, observed, threshold, diag):
    results.append(("FAIL", check, level, observed, threshold, diag))


def pas(check, level, observed):
    results.append(("PASS", check, level, observed, "", ""))


# CHECK_CAMERA_VIEWPORT
for L in range(N_LEVELS):
    g.set_level(L)
    gw, gh = g.current_level.grid_size or (64, 64)
    cw, ch = g.camera._width, g.camera._height
    if (cw, ch) == (gw, gh):
        pas("CHECK_CAMERA_VIEWPORT", L + 1, f"({cw},{ch})==({gw},{gh})")
    else:
        fail("CHECK_CAMERA_VIEWPORT", L + 1, f"({cw},{ch})", f"({gw},{gh})", "camera/grid mismatch")


# CHECK_SPRITE_CONTENT
for L in range(N_LEVELS):
    g_fresh = GameClass()
    g_fresh.set_level(L)
    frame = g_fresh.camera.render(g_fresh.current_level.get_sprites())
    distinct = set(np.unique(frame[frame != LETTER_BOX]).tolist())
    if len(distinct) >= 2:
        pas("CHECK_SPRITE_CONTENT", L + 1, f"{len(distinct)} distinct values")
    else:
        fail("CHECK_SPRITE_CONTENT", L + 1, f"{len(distinct)}", ">=2", "no game content visible")


# CHECK_ACTION_BRANCHES
declared = list(g._available_actions)
for action_id in declared:
    needle = f"GameAction.ACTION{action_id}"
    if needle in src_text:
        pas("CHECK_ACTION_BRANCHES", action_id, f"branch present")
    else:
        fail("CHECK_ACTION_BRANCHES", action_id, "missing", "branch present", f"no {needle} in source")


# CHECK_ACTION_RUNTIME
for action_id in declared:
    g_fresh = GameClass()
    g_fresh.set_level(0)
    try:
        if action_id == 6:
            g_fresh.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True)
        else:
            g_fresh.perform_action(ActionInput(id=GameAction.from_id(action_id)), raw=True)
        pas("CHECK_ACTION_RUNTIME", action_id, "no exception")
    except Exception as e:
        fail("CHECK_ACTION_RUNTIME", action_id, repr(e), "no exception", "step() raised")


# CHECK_PALETTE_RANGE
for L in range(N_LEVELS):
    g_fresh = GameClass()
    g_fresh.set_level(L)
    frame = g_fresh.camera.render(g_fresh.current_level.get_sprites())
    mn, mx = int(frame.min()), int(frame.max())
    if mn >= 0 and mx <= 15:
        pas("CHECK_PALETTE_RANGE", L + 1, f"{mn}..{mx}")
    else:
        fail("CHECK_PALETTE_RANGE", L + 1, f"{mn}..{mx}", "[0,15]", "out-of-range pixel")


# CHECK_WIN_PATH_EXISTS
if "self.next_level()" in src_text or "self.win()" in src_text:
    pas("CHECK_WIN_PATH_EXISTS", "all", "next_level() found")
else:
    fail("CHECK_WIN_PATH_EXISTS", "all", "neither found", "present", "structurally unwinnable")


# CHECK_LOSE_PATH_EXISTS
if "self.lose()" in src_text:
    pas("CHECK_LOSE_PATH_EXISTS", "all", "lose() found")
else:
    fail("CHECK_LOSE_PATH_EXISTS", "all", "missing", "present", "no lose path")


# CHECK_CAMERA_DEFAULT
needs_per_level = any(
    g._levels[i].grid_size != g._levels[0].grid_size for i in range(1, N_LEVELS)
)
if needs_per_level:
    has_resize = ("self.camera.width" in src_text and "self.camera.height" in src_text)
    if has_resize:
        pas("CHECK_CAMERA_DEFAULT", "all", "per-level resize present")
    else:
        fail("CHECK_CAMERA_DEFAULT", "all", "no resize", "resize present", "needs per-level camera mutation")
else:
    pas("CHECK_CAMERA_DEFAULT", "all", "all levels share grid_size; resize not required")


# CHECK_VISUAL_SANITY: render PNGs to workspace/smoke-frames/
PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)
out_dir = Path("workspace/smoke-frames")
out_dir.mkdir(parents=True, exist_ok=True)
for L in range(min(3, N_LEVELS)):
    g_fresh = GameClass()
    g_fresh.set_level(L)
    frame = g_fresh.camera.render(g_fresh.current_level.get_sprites())
    rgb = PALETTE[np.clip(frame, 0, 15)]
    img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
    img.save(out_dir / f"level_{L+1}.png")

print("\n--- universal smoke check results ---")
for r in results:
    print(r[0], r[1], "L=" + str(r[2]), "->", r[3], r[4], r[5])
n_fail = sum(1 for r in results if r[0] == "FAIL")
print(f"\nTotal: {len(results)} checks, {n_fail} failures.")
