"""Run universal + custom smoke-test checks against bw7k."""

import importlib.util
import sys
from pathlib import Path

import numpy as np

REPO = Path("/Users/nickhe/Programming/NovaPlay-Agents")
SRC = REPO / "prior-games/bw7k/bw7k.py"
sys.path.insert(0, str(SRC.parent))

spec = importlib.util.spec_from_file_location("smoke_bw7k", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = mod.Bw7k
g = GameClass()

from novaengine import ActionInput, GameAction

LETTER_BOX = mod.PADDING_COLOR
BACKGROUND = mod.BACKGROUND_COLOR
N_LEVELS = len(g._levels)
src_text = SRC.read_text()

results = {}


def render_frame_at_level(level_idx):
    g_local = GameClass()
    g_local.set_level(level_idx)
    return g_local, g_local.camera.render(g_local.current_level.get_sprites())


# ---- CHECK_CAMERA_VIEWPORT ----
cam_results = []
for L in range(N_LEVELS):
    g.set_level(L)
    gw, gh = g.current_level.grid_size or (64, 64)
    cw, ch = g.camera._width, g.camera._height
    cam_results.append((L + 1, gw, gh, cw, ch, cw == gw and ch == gh))
results["CAMERA_VIEWPORT"] = cam_results

# ---- CHECK_SPRITE_CONTENT ----
sprite_content = []
for L in range(N_LEVELS):
    g_local, frame = render_frame_at_level(L)
    distinct = set(np.unique(frame[frame != LETTER_BOX]).tolist())
    sprite_content.append((L + 1, len(distinct), sorted(distinct)))
results["SPRITE_CONTENT"] = sprite_content

# ---- CHECK_ACTION_BRANCHES ----
declared = list(g._available_actions)
action_branches = []
for aid in declared:
    needle = f"GameAction.ACTION{aid}"
    action_branches.append((aid, needle in src_text))
results["ACTION_BRANCHES"] = action_branches

# ---- CHECK_ACTION_RUNTIME ----
action_runtime = []
for aid in declared:
    g_fresh = GameClass()
    n0 = g_fresh._action_count
    err = None
    try:
        if aid == 6:
            g_fresh.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True)
        else:
            g_fresh.perform_action(ActionInput(id=GameAction.from_id(aid)), raw=True)
    except Exception as e:
        err = repr(e)
    n1 = g_fresh._action_count
    action_runtime.append((aid, err, n0, n1))
results["ACTION_RUNTIME"] = action_runtime

# ---- CHECK_PALETTE_RANGE ----
palette_range = []
for L in range(N_LEVELS):
    g_local, frame = render_frame_at_level(L)
    palette_range.append((L + 1, int(frame.min()), int(frame.max())))
results["PALETTE_RANGE"] = palette_range

# ---- CHECK_WIN_PATH_EXISTS ----
results["WIN_PATH_EXISTS"] = ("self.next_level()" in src_text or "self.win()" in src_text)

# ---- CHECK_LOSE_PATH_EXISTS ----
results["LOSE_PATH_EXISTS"] = "self.lose()" in src_text

# ---- CHECK_CAMERA_DEFAULT ----
sizes = [g._levels[i].grid_size for i in range(N_LEVELS)]
needs_per_level_camera = any(s != sizes[0] for s in sizes)
has_resize = ("self.camera.width" in src_text and "self.camera.height" in src_text)
results["CAMERA_DEFAULT"] = (needs_per_level_camera, has_resize, sizes)

# ---- CHECK_WITNESS_WINS ----
def act(n):
    return ActionInput(id=GameAction.from_id(n), data={})

def click(x, y):
    return ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y})

# L1 witness: 13 × UP (action 1)
W1 = [act(1)] * 13
# L2 witness: RIGHT×6, UP×6, LEFT×6, UP×7 = 25 actions
W2 = [act(4)] * 6 + [act(1)] * 6 + [act(3)] * 6 + [act(1)] * 7
# L3 witness: UP×6, DOWN×1, RIGHT×8, UP×1, UP×8, LEFT×4 = 28 actions
W3 = [act(1)] * 6 + [act(2)] * 1 + [act(4)] * 8 + [act(1)] * 1 + [act(1)] * 8 + [act(3)] * 4

WITNESSES = {1: W1, 2: W2, 3: W3}

g_w = GameClass()
g_w.handle_reset()
witness_failures = []
witness_trace = []
for level_idx in range(1, N_LEVELS + 1):
    score_before = g_w._score
    if score_before != level_idx - 1:
        witness_failures.append(
            f"L{level_idx}: expected score={level_idx-1} before, got {score_before}"
        )
        break
    actor_pre = None
    actors = g_w.current_level.get_sprites_by_tag("actor")
    if actors:
        actor_pre = (actors[0].x, actors[0].y)
    for ai in WITNESSES[level_idx]:
        g_w.perform_action(ai)
    actors_post = g_w.current_level.get_sprites_by_tag("actor")
    actor_post = (actors_post[0].x, actors_post[0].y) if actors_post else None
    state_post = g_w._state.name
    score_post = g_w._score
    witness_trace.append(
        f"L{level_idx}: actor_pre={actor_pre} actor_post={actor_post} "
        f"state={state_post} score={score_post}"
    )
    if level_idx < N_LEVELS:
        if g_w._score != level_idx:
            witness_failures.append(
                f"L{level_idx}: witness did not advance (score {score_before} -> {g_w._score}); state={g_w._state.name}"
            )
            break
    else:
        if g_w._state.name != "WIN":
            witness_failures.append(
                f"L{level_idx}: witness did not reach WIN (state={g_w._state.name}, score={g_w._score})"
            )
results["WITNESS_WINS"] = (witness_failures, witness_trace)

# ---- Render frames for visual sanity ----
from PIL import Image  # type: ignore

PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)

out_dir = Path("/Users/nickhe/Programming/NovaPlay-Agents/runs/2026-05-09T01-02-39/workspace/smoke-frames")
out_dir.mkdir(parents=True, exist_ok=True)
for L in range(min(3, N_LEVELS)):
    g_render = GameClass()
    g_render.set_level(L)
    frame = g_render.camera.render(g_render.current_level.get_sprites())
    rgb = PALETTE[frame.clip(0, 15)]
    img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
    img.save(out_dir / f"level_{L+1}.png")

# ---- CUSTOM CHECKS ----
custom_results = []


def check_up_moves_actor():
    """Pressing UP moves the actor's y-coordinate by -STRIDE."""
    g = GameClass()
    g.set_level(0)
    actors = g.current_level.get_sprites_by_tag("actor")
    actor = actors[0]
    y0 = actor.y
    g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    return actor.y == y0 - mod.STRIDE, f"y0={y0} y1={actor.y}"


def check_anchor_spawns_shade():
    """Stepping onto anchor_red spawns a shade_red sprite in the level."""
    g = GameClass()
    g.set_level(0)
    # Walk UP×5 to step onto anchor at (12, 36).
    for _ in range(5):
        g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    shades = g.current_level.get_sprites_by_tag("shade_red")
    return len(shades) == 1, f"shade_red count={len(shades)}"


def check_shade_lands_at_target_l1():
    """In L1, after the spawn the shade rests at target_red's cell."""
    g = GameClass()
    g.set_level(0)
    for _ in range(5):
        g.perform_action(ActionInput(id=GameAction.ACTION1), raw=True)
    shades = g.current_level.get_sprites_by_tag("shade_red")
    targets = g.current_level.get_sprites_by_tag("target_red")
    s = shades[0]
    t = targets[0]
    return (s.x, s.y) == (t.x, t.y), f"shade=({s.x},{s.y}) target=({t.x},{t.y})"


def check_l1_witness_wins():
    """L1's 13-UP witness advances past L1."""
    g = GameClass()
    g.handle_reset()
    score_before = g._score
    for _ in range(13):
        g.perform_action(ActionInput(id=GameAction.ACTION1))
    return g._score == 1, f"score before={score_before} after={g._score} state={g._state.name}"


for fn in (check_up_moves_actor, check_anchor_spawns_shade,
           check_shade_lands_at_target_l1, check_l1_witness_wins):
    try:
        passed, observed = fn()
    except Exception as e:
        passed, observed = False, f"EXC: {repr(e)}"
    custom_results.append((fn.__name__, passed, observed, fn.__doc__ or ""))

results["CUSTOM"] = custom_results

# ---- Output ----
import json
print(json.dumps({k: str(v) for k, v in results.items()}, indent=2, default=str))
