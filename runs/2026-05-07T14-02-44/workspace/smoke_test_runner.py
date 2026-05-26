"""Run the 9 universal smoke-test checks for game yf3h."""

from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT))

GAME_ID = "yf3h"
PASCAL = "Yf3h"
SRC = REPO_ROOT / f"prior-games/{GAME_ID}/{GAME_ID}.py"
WORKSPACE = Path(__file__).resolve().parent
SMOKE_FRAMES = WORKSPACE / "smoke-frames"


def load_game() -> tuple[Any, Any, int, int]:
    spec = importlib.util.spec_from_file_location(f"smoke_{GAME_ID}", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    GameClass = getattr(mod, PASCAL)
    g = GameClass()
    LETTER_BOX = getattr(mod, "PALETTE_PADDING", 0)
    BACKGROUND = getattr(mod, "PALETTE_BACKGROUND", 0)
    return mod, g, LETTER_BOX, BACKGROUND


def main() -> dict[str, Any]:
    print(f"Loading {GAME_ID}...")
    mod, g, LETTER_BOX, BACKGROUND = load_game()
    src_text = SRC.read_text()
    N_LEVELS = len(g._levels)
    print(f"Loaded. {N_LEVELS} levels; LETTER_BOX={LETTER_BOX}; BACKGROUND={BACKGROUND}")

    results: dict[str, Any] = {"failures": [], "checks": {}}

    # ----- CHECK_CAMERA_VIEWPORT (per level) -----
    print("\nCHECK_CAMERA_VIEWPORT")
    cam_results = []
    for li in range(N_LEVELS):
        g.set_level(li)
        gw, gh = g.current_level.grid_size or (64, 64)
        cam_w, cam_h = g.camera._width, g.camera._height
        match = (cam_w == gw and cam_h == gh)
        cam_results.append({"level": li + 1, "grid_size": (gw, gh),
                            "camera": (cam_w, cam_h), "match": match})
        print(f"  L{li+1}: grid_size={gw}x{gh}, camera={cam_w}x{cam_h}, match={match}")
        if not match:
            results["failures"].append(("CHECK_CAMERA_VIEWPORT",
                f"L{li+1}: grid_size={gw}x{gh} but camera={cam_w}x{cam_h}"))
    results["checks"]["CHECK_CAMERA_VIEWPORT"] = cam_results

    # ----- CHECK_SPRITE_CONTENT (per level) -----
    print("\nCHECK_SPRITE_CONTENT")
    sprite_content = []
    for li in range(N_LEVELS):
        g.set_level(li)
        frame = g.camera.render(g.current_level.get_sprites())
        # Apply HUD overlay
        for hud in (g.camera._interfaces if hasattr(g.camera, "_interfaces") else []):
            frame = hud.render_interface(frame)
        non_lb = frame[frame != LETTER_BOX]
        distinct = set(non_lb.tolist()) if non_lb.size else set()
        sprite_content.append({"level": li + 1, "distinct_non_letterbox": sorted(distinct)})
        print(f"  L{li+1}: distinct_non_letterbox={sorted(distinct)}")
        if len(distinct) < 2:
            results["failures"].append(("CHECK_SPRITE_CONTENT",
                f"L{li+1}: only {len(distinct)} distinct palette values"))
    results["checks"]["CHECK_SPRITE_CONTENT"] = sprite_content

    # ----- CHECK_ACTION_BRANCHES -----
    print("\nCHECK_ACTION_BRANCHES")
    declared = list(g._available_actions)
    branch_failures = []
    for action in declared:
        action_id = int(getattr(action, "value", action))
        needle = f"GameAction.ACTION{action_id}"
        if needle not in src_text:
            results["failures"].append(("CHECK_ACTION_BRANCHES",
                f"ACTION{action_id} declared but '{needle}' not in source"))
            branch_failures.append(action_id)
        print(f"  ACTION{action_id}: '{needle}' present={needle in src_text}")
    results["checks"]["CHECK_ACTION_BRANCHES"] = branch_failures

    # ----- CHECK_ACTION_RUNTIME -----
    print("\nCHECK_ACTION_RUNTIME")
    from novaengine import ActionInput, GameAction
    runtime_failures = []
    for action in declared:
        action_id = int(getattr(action, "value", action))
        try:
            g_fresh = mod.Yf3h()
            prev_count = g_fresh._action_count
            if action_id == 6:
                g_fresh.perform_action(
                    ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True
                )
            else:
                g_fresh.perform_action(
                    ActionInput(id=GameAction.from_id(action_id)), raw=True
                )
            new_count = g_fresh._action_count
            print(f"  ACTION{action_id}: ran OK; action_count {prev_count}→{new_count}")
        except Exception as e:
            results["failures"].append(("CHECK_ACTION_RUNTIME",
                f"ACTION{action_id}: {type(e).__name__}: {e}"))
            runtime_failures.append((action_id, repr(e)))
            traceback.print_exc()
    results["checks"]["CHECK_ACTION_RUNTIME"] = runtime_failures

    # ----- CHECK_PALETTE_RANGE (per level) -----
    print("\nCHECK_PALETTE_RANGE")
    palette_failures = []
    for li in range(N_LEVELS):
        g.set_level(li)
        frame = g.camera.render(g.current_level.get_sprites())
        for hud in (g.camera._interfaces if hasattr(g.camera, "_interfaces") else []):
            frame = hud.render_interface(frame)
        mn, mx = int(frame.min()), int(frame.max())
        ok = (mn >= 0 and mx <= 15)
        print(f"  L{li+1}: range [{mn}, {mx}], ok={ok}")
        if not ok:
            results["failures"].append(("CHECK_PALETTE_RANGE",
                f"L{li+1}: frame contains palette {mn}..{mx} (outside [0, 15])"))
        palette_failures.append({"level": li + 1, "range": (mn, mx), "ok": ok})
    results["checks"]["CHECK_PALETTE_RANGE"] = palette_failures

    # ----- CHECK_WIN_PATH_EXISTS -----
    print("\nCHECK_WIN_PATH_EXISTS")
    has_next = "self.next_level()" in src_text
    has_win = "self.win()" in src_text
    print(f"  next_level()={has_next}; win()={has_win}")
    if not (has_next or has_win):
        results["failures"].append(("CHECK_WIN_PATH_EXISTS",
            "Neither self.next_level() nor self.win() found in source"))
    results["checks"]["CHECK_WIN_PATH_EXISTS"] = (has_next, has_win)

    # ----- CHECK_LOSE_PATH_EXISTS -----
    print("\nCHECK_LOSE_PATH_EXISTS")
    has_lose = "self.lose()" in src_text
    print(f"  lose()={has_lose}")
    if not has_lose:
        results["failures"].append(("CHECK_LOSE_PATH_EXISTS",
            "self.lose() not found in source"))
    results["checks"]["CHECK_LOSE_PATH_EXISTS"] = has_lose

    # ----- CHECK_CAMERA_DEFAULT -----
    print("\nCHECK_CAMERA_DEFAULT")
    sizes = [g._levels[i].grid_size for i in range(N_LEVELS)]
    needs_resize = any(sizes[i] != sizes[0] for i in range(1, N_LEVELS))
    has_resize = ("self.camera.width" in src_text and "self.camera.height" in src_text)
    print(f"  level grid_sizes={sizes}; needs_resize={needs_resize}; has_resize={has_resize}")
    if needs_resize and not has_resize:
        results["failures"].append(("CHECK_CAMERA_DEFAULT",
            f"Levels have different grid sizes {sizes} but no per-level camera resize"))
    results["checks"]["CHECK_CAMERA_DEFAULT"] = (sizes, needs_resize, has_resize)

    # ----- Render initial frames for CHECK_VISUAL_SANITY -----
    print("\nRendering initial frames for CHECK_VISUAL_SANITY")
    SMOKE_FRAMES.mkdir(parents=True, exist_ok=True)
    PALETTE = np.array([
        (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
        (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
        (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
        (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
        (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
        (0x88, 0x37, 0x9B),
    ], dtype=np.uint8)

    for li in range(min(3, N_LEVELS)):
        g.set_level(li)
        frame = g.camera.render(g.current_level.get_sprites())
        for hud in (g.camera._interfaces if hasattr(g.camera, "_interfaces") else []):
            frame = hud.render_interface(frame)
        rgb = PALETTE[frame.clip(0, 15)]
        img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
        path = SMOKE_FRAMES / f"level_{li+1}.png"
        img.save(path)
        print(f"  L{li+1}: saved {path} (frame range [{int(frame.min())}, {int(frame.max())}])")

    print(f"\n{'=' * 60}")
    print(f"FAILURES ({len(results['failures'])}):")
    for chk, msg in results["failures"]:
        print(f"  [{chk}] {msg}")

    return results


if __name__ == "__main__":
    main()
