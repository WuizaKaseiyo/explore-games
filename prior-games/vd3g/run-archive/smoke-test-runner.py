"""Smoke-test runner for vd3g — runs the 10 universal checks + custom checks."""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

REPO = Path("/Users/nickhe/Programming/NovaPlay-Agents")
SRC_FILE = REPO / "prior-games/vd3g/vd3g.py"
WORKSPACE = REPO / "runs/2026-05-07T19-59-42/workspace"
SMOKE_FRAMES = WORKSPACE / "smoke-frames"
SMOKE_FRAMES.mkdir(parents=True, exist_ok=True)

GAME_ID = "vd3g"
PASCAL = "Vd3g"

# Load the module
spec = importlib.util.spec_from_file_location("smoke_vd3g", SRC_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.modules["smoke_vd3g"] = mod
GameClass = getattr(mod, PASCAL)
src_text = SRC_FILE.read_text()
LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)

g = GameClass()
N_LEVELS = len(g._levels)

from novaengine import ActionInput, GameAction


def render_level(g, idx):
    g.set_level(idx)
    return g.camera.render(g.current_level.get_sprites())


# =====================================================================
# CHECK_CAMERA_VIEWPORT
# =====================================================================
viewport_results = []
for idx in range(N_LEVELS):
    g_fresh = GameClass()
    g_fresh.set_level(idx)
    gw, gh = g_fresh.current_level.grid_size or (64, 64)
    cam_w, cam_h = g_fresh.camera._width, g_fresh.camera._height
    match = cam_w == gw and cam_h == gh
    viewport_results.append((idx, gw, gh, cam_w, cam_h, match))
    print(f"CHECK_CAMERA_VIEWPORT L{idx+1}: grid=({gw},{gh}) camera=({cam_w},{cam_h}) match={match}")
viewport_pass = all(r[5] for r in viewport_results)

# =====================================================================
# CHECK_SPRITE_CONTENT
# =====================================================================
content_results = []
for idx in range(N_LEVELS):
    g_fresh = GameClass()
    frame = render_level(g_fresh, idx)
    distinct = set(np.unique(frame[frame != LETTER_BOX]).tolist())
    content_results.append((idx, len(distinct), distinct))
    print(f"CHECK_SPRITE_CONTENT L{idx+1}: distinct non-letter-box palette count = {len(distinct)} = {sorted(distinct)}")
content_pass = all(r[1] >= 2 for r in content_results)

# =====================================================================
# CHECK_ACTION_BRANCHES
# =====================================================================
declared = list(g._available_actions)
branch_results = []
for action_id in declared:
    needle = f"GameAction.ACTION{action_id}"
    found = needle in src_text
    branch_results.append((action_id, found))
    print(f"CHECK_ACTION_BRANCHES ACTION{action_id}: source contains '{needle}' = {found}")
branches_pass = all(r[1] for r in branch_results)

# =====================================================================
# CHECK_ACTION_RUNTIME
# =====================================================================
runtime_results = []
for action_id in declared:
    g_fresh = GameClass()
    try:
        if action_id == 6:
            g_fresh.perform_action(
                ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}),
                raw=True,
            )
        else:
            g_fresh.perform_action(ActionInput(id=GameAction.from_id(action_id)), raw=True)
        runtime_results.append((action_id, True, None))
    except Exception as e:
        runtime_results.append((action_id, False, repr(e)))
    print(f"CHECK_ACTION_RUNTIME ACTION{action_id}: ok = {runtime_results[-1][1]} err = {runtime_results[-1][2]}")
runtime_pass = all(r[1] for r in runtime_results)

# =====================================================================
# CHECK_PALETTE_RANGE
# =====================================================================
palette_results = []
for idx in range(N_LEVELS):
    g_fresh = GameClass()
    frame = render_level(g_fresh, idx)
    mn, mx = int(frame.min()), int(frame.max())
    palette_results.append((idx, mn, mx, mn >= 0 and mx <= 15))
    print(f"CHECK_PALETTE_RANGE L{idx+1}: min={mn} max={mx} ok={palette_results[-1][3]}")
palette_pass = all(r[3] for r in palette_results)

# =====================================================================
# CHECK_WIN_PATH_EXISTS
# =====================================================================
has_next_level = "self.next_level()" in src_text
has_win = "self.win()" in src_text
win_path_pass = has_next_level or has_win
print(f"CHECK_WIN_PATH_EXISTS: next_level={has_next_level} win={has_win} pass={win_path_pass}")

# =====================================================================
# CHECK_WITNESS_WINS
# =====================================================================
def click(c, r):
    return ActionInput(id=GameAction.ACTION6, data={"x": c * 4 + 1, "y": r * 4 + 1})


def witness_l1():
    return [click(5, 6), click(5, 6),
            click(5, 7), click(5, 7),
            click(5, 8), click(5, 8)]


def witness_l2():
    cells = [(3,5),(3,6),(3,7),(3,8),(4,8),(5,8),(6,8),(7,8),
             (8,8),(9,8),(10,8),(11,8),(12,8),(12,7),(12,6),(12,5)]
    out = []
    for c, r in cells:
        out.append(click(c, r))
        out.append(click(c, r))
    return out


def witness_l3():
    out = []
    for c, r in [(4,6),(5,6),(6,6),(7,6)]:
        out.append(click(c, r)); out.append(click(c, r))
    for c, r in [(11,9),(10,9),(9,9)]:
        out.append(click(c, r)); out.append(click(c, r))
    out.append(click(8, 6)); out.append(click(8, 6))
    for c, r in [(9,6),(10,6),(11,6)]:
        out.append(click(c, r)); out.append(click(c, r))
    for c, r in [(7,9),(6,9),(5,9),(4,9)]:
        out.append(click(c, r)); out.append(click(c, r))
    return out


WITNESSES = {1: witness_l1(), 2: witness_l2(), 3: witness_l3()}

g_w = GameClass()
g_w.handle_reset()
witness_failures = []
for level_idx in range(1, N_LEVELS + 1):
    score_before = g_w._score
    if score_before != level_idx - 1:
        witness_failures.append(
            f"L{level_idx}: expected score {level_idx-1}, got {score_before}"
        )
        break
    for ai in WITNESSES[level_idx]:
        g_w.perform_action(ai)
    if level_idx < N_LEVELS:
        if g_w._score != level_idx:
            witness_failures.append(
                f"L{level_idx}: witness did not advance (score went "
                f"{score_before} -> {g_w._score}, expected {level_idx}); "
                f"state = {g_w._state.name}"
            )
            break
    else:
        if g_w._state.name != "WIN":
            witness_failures.append(
                f"L{level_idx}: witness did not reach WIN "
                f"(state = {g_w._state.name}, score = {g_w._score})"
            )
            break
witness_pass = len(witness_failures) == 0
print(f"CHECK_WITNESS_WINS: pass={witness_pass} failures={witness_failures}")

# =====================================================================
# CHECK_LOSE_PATH_EXISTS
# =====================================================================
has_lose = "self.lose()" in src_text
lose_pass = has_lose
print(f"CHECK_LOSE_PATH_EXISTS: lose found = {has_lose}")

# =====================================================================
# CHECK_CAMERA_DEFAULT (per-level camera resize when grids differ)
# =====================================================================
needs_resize = any(
    g._levels[i].grid_size != g._levels[0].grid_size
    for i in range(1, N_LEVELS)
)
if needs_resize:
    has_resize = "self.camera.width" in src_text and "self.camera.height" in src_text
else:
    has_resize = True  # no resize needed
print(f"CHECK_CAMERA_DEFAULT: needs_resize={needs_resize} has_resize_code={has_resize}")
camera_default_pass = has_resize

# =====================================================================
# RENDER FRAMES for visual sanity
# =====================================================================
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
    g_render = GameClass()
    for idx in range(min(3, N_LEVELS)):
        g_render.set_level(idx)
        frame = g_render.camera.render(g_render.current_level.get_sprites())
        rgb = PALETTE[frame.clip(0, 15)]
        img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
        img.save(SMOKE_FRAMES / f"level_{idx+1}.png")
    print("Frames rendered to", SMOKE_FRAMES)
except Exception as e:
    print("Frame render failed:", e)

# =====================================================================
# CUSTOM CHECKS
# =====================================================================

def check_click_toggles_normal_cell():
    """Clicking a NORMAL HIGH cell flips it to LOW (no marble roll into it)."""
    g = GameClass()
    g.set_level(0)
    # Click a faraway HIGH cell at (10, 2) — far from marble (5, 5).
    h0 = int(g.heights[2, 10])
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 10*4+1, "y": 2*4+1}))
    h1 = int(g.heights[2, 10])
    return h0 == 1 and h1 == 0, f"h0={h0} h1={h1}"


def check_marble_rolls_to_dug_low():
    """Digging the cell south of marble makes marble roll one cell south."""
    g = GameClass()
    g.set_level(0)
    marble = g.current_level.get_sprites_by_tag("marble")[0]
    y0 = marble.y // 4
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 5*4+1, "y": 6*4+1}))
    y1 = marble.y // 4
    return y1 == y0 + 1, f"y0={y0} y1={y1}"


def check_anchor_click_flips_partner():
    """Clicking one anchor cell flips its paired anchor cell too."""
    g = GameClass()
    g.set_level(2)  # L3 has the anchor pair
    h_a_before = int(g.heights[6, 8])
    h_b_before = int(g.heights[9, 8])
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 8*4+1, "y": 6*4+1}))
    h_a_after = int(g.heights[6, 8])
    h_b_after = int(g.heights[9, 8])
    return h_a_before != h_a_after and h_b_before != h_b_after, \
        f"a:{h_a_before}->{h_a_after} b:{h_b_before}->{h_b_after}"


def check_lose_at_budget_exhaustion():
    """Spending more than max_steps clicks triggers lose."""
    g = GameClass()
    g.set_level(0)
    budget = g.max_steps
    # Spend (budget+1) wall-clicks (no-ops, but each consumes a step).
    for _ in range(budget + 1):
        g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 0, "y": 32}))
    return g._state.name == "GAME_OVER", f"state after budget+1 clicks = {g._state.name}"


custom_checks = [
    ("check_click_toggles_normal_cell", check_click_toggles_normal_cell),
    ("check_marble_rolls_to_dug_low", check_marble_rolls_to_dug_low),
    ("check_anchor_click_flips_partner", check_anchor_click_flips_partner),
    ("check_lose_at_budget_exhaustion", check_lose_at_budget_exhaustion),
]
custom_results = []
for name, fn in custom_checks:
    try:
        passed, observed = fn()
    except Exception as e:
        passed, observed = False, f"exception: {e!r}"
    custom_results.append((name, passed, observed))
    print(f"CUSTOM {name}: pass={passed} observed={observed}")

# =====================================================================
# Aggregate
# =====================================================================
all_pass = (
    viewport_pass and content_pass and branches_pass and runtime_pass
    and palette_pass and win_path_pass and witness_pass and lose_pass
    and camera_default_pass and all(r[1] for r in custom_results)
)
print(f"\nALL_PASS = {all_pass}")
print(f"Frames at: {SMOKE_FRAMES}")

# Save aggregate JSON for the agent to consume
result_json = {
    "viewport_pass": viewport_pass,
    "content_pass": content_pass,
    "branches_pass": branches_pass,
    "runtime_pass": runtime_pass,
    "palette_pass": palette_pass,
    "win_path_pass": win_path_pass,
    "witness_pass": witness_pass,
    "witness_failures": witness_failures,
    "lose_pass": lose_pass,
    "camera_default_pass": camera_default_pass,
    "custom_results": [(n, p, o) for (n, p, o) in custom_results],
    "all_pass": all_pass,
}
(WORKSPACE / "smoke-test-aggregate.json").write_text(json.dumps(result_json, indent=2))
