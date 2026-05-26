"""Run the 9 universal smoke checks + the custom checks for vp6h.

Writes either smoke-test-pass.md or smoke-test-failures.md depending on
the outcome.
"""

import importlib.util
import sys
import traceback
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[5]
WS = Path(__file__).resolve().parent
GAME_ID = "vp6h"
PASCAL = "Vp6h"
src = REPO_ROOT / f"prior-games/{GAME_ID}/{GAME_ID}.py"

# Add the workspace to sys.path so we can import smoke-test-custom
sys.path.insert(0, str(WS))


def load_game_class():
    spec = importlib.util.spec_from_file_location(f"smoke_{GAME_ID}", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    GC = getattr(mod, PASCAL)
    return GC, mod


def render_frame(g):
    return g.camera.render(g.current_level.get_sprites())


GameClass, game_mod = load_game_class()
LETTER_BOX = getattr(game_mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(game_mod, "BACKGROUND_COLOR", 0)

results = {}


def record(check, status, **kwargs):
    results.setdefault(check, []).append({"status": status, **kwargs})


# CHECK_CAMERA_VIEWPORT
g = GameClass()
N_LEVELS = len(g._levels)

for L in range(N_LEVELS):
    g.set_level(L)
    gw, gh = g.current_level.grid_size or (64, 64)
    cam_w, cam_h = g.camera._width, g.camera._height
    match = cam_w == gw and cam_h == gh
    record("CHECK_CAMERA_VIEWPORT", "PASS" if match else "FAIL",
           level=L + 1, observed=f"camera={cam_w}x{cam_h} grid={gw}x{gh}")

# CHECK_SPRITE_CONTENT
for L in range(N_LEVELS):
    g.set_level(L)
    frame = render_frame(g)
    distinct = set(np.unique(frame[frame != LETTER_BOX]).tolist())
    record("CHECK_SPRITE_CONTENT",
           "PASS" if len(distinct) >= 2 else "FAIL",
           level=L + 1, observed=f"{len(distinct)} distinct: {sorted(distinct)}")

# CHECK_ACTION_BRANCHES
src_text = src.read_text()
for action_id in g._available_actions:
    needle = f"GameAction.ACTION{action_id}"
    record(
        "CHECK_ACTION_BRANCHES",
        "PASS" if needle in src_text else "FAIL",
        level="all",
        observed=f"ACTION{action_id} {'present' if needle in src_text else 'absent'} in source",
    )

# CHECK_ACTION_RUNTIME
from novaengine import ActionInput, GameAction
for action_id in g._available_actions:
    g_fresh = GameClass()
    try:
        if action_id == 6:
            g_fresh.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True)
        else:
            g_fresh.perform_action(ActionInput(id=GameAction.from_id(action_id)), raw=True)
        record("CHECK_ACTION_RUNTIME", "PASS", level="all",
               observed=f"ACTION{action_id} no exception")
    except Exception as e:
        record("CHECK_ACTION_RUNTIME", "FAIL", level="all",
               observed=f"ACTION{action_id} raised {type(e).__name__}: {e}")

# CHECK_PALETTE_RANGE
for L in range(N_LEVELS):
    g.set_level(L)
    frame = render_frame(g)
    mn, mx = int(frame.min()), int(frame.max())
    record("CHECK_PALETTE_RANGE",
           "PASS" if (mn >= 0 and mx <= 15) else "FAIL",
           level=L + 1, observed=f"range [{mn}, {mx}]")

# CHECK_WIN_PATH_EXISTS
has_next = "self.next_level()" in src_text or "next_level(" in src_text
has_win = "self.win()" in src_text
record("CHECK_WIN_PATH_EXISTS",
       "PASS" if (has_next or has_win) else "FAIL",
       level="static", observed=f"next_level={has_next} win={has_win}")

# CHECK_LOSE_PATH_EXISTS
has_lose = "self.lose()" in src_text
record("CHECK_LOSE_PATH_EXISTS",
       "PASS" if has_lose else "FAIL",
       level="static", observed=f"lose={has_lose}")

# CHECK_CAMERA_DEFAULT
needs_per_level = any(
    g._levels[i].grid_size != g._levels[0].grid_size for i in range(1, N_LEVELS)
)
if needs_per_level:
    has_resize = "self.camera.width" in src_text and "self.camera.height" in src_text
    record("CHECK_CAMERA_DEFAULT",
           "PASS" if has_resize else "FAIL",
           level="static", observed=f"resize_present={has_resize}")
else:
    has_resize = "self.camera.width" in src_text and "self.camera.height" in src_text
    record("CHECK_CAMERA_DEFAULT", "PASS",
           level="static",
           observed=f"levels share grid_size; resize_present={has_resize}")

# CHECK_VISUAL_SANITY: render PNGs to workspace/smoke-frames
try:
    from PIL import Image
except ImportError:
    print("PIL not installed; skipping PNG render", file=sys.stderr)
    Image = None

PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)

if Image is not None:
    out_dir = WS / "smoke-frames"
    out_dir.mkdir(parents=True, exist_ok=True)
    for L in range(min(3, N_LEVELS)):
        g.set_level(L)
        frame = render_frame(g)
        rgb = PALETTE[frame.clip(0, 15)]
        img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
        img.save(out_dir / f"level_{L + 1}.png")
    print(f"Rendered PNGs to {out_dir}")

# CUSTOM CHECKS
import importlib
custom_spec = importlib.util.spec_from_file_location("smoke_custom", WS / "smoke-test-custom.py")
custom_mod = importlib.util.module_from_spec(custom_spec)
custom_spec.loader.exec_module(custom_mod)

custom_checks = [
    "check_arrow_moves_avatar",
    "check_click_top_rail_slides_lantern",
    "check_pickup_in_shadow_collects_crystal",
    "check_pickup_in_light_is_no_op",
]

custom_results = []
for name in custom_checks:
    fn = getattr(custom_mod, name)
    try:
        passed, observed = fn(GameClass)
        custom_results.append((name, "PASS" if passed else "FAIL", observed))
    except Exception as e:
        tb = traceback.format_exc()
        custom_results.append((name, "FAIL", f"raised: {type(e).__name__}: {e}\n{tb}"))


# Summary
print("\n=== UNIVERSAL CHECKS ===")
for check_name, rows in results.items():
    for r in rows:
        print(f"{r['status']:5} {check_name} L{r.get('level','-')} :: {r.get('observed','')}")

print("\n=== CUSTOM CHECKS ===")
for name, status, observed in custom_results:
    print(f"{status:5} {name} :: {observed}")

# Aggregate
all_pass = all(r["status"] == "PASS" for rows in results.values() for r in rows)
all_pass = all_pass and all(s == "PASS" for _, s, _ in custom_results)
print("\n=== AGGREGATE ===")
print("ALL PASS" if all_pass else "FAILURES PRESENT")
