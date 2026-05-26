"""Smoke-test runner for kp9z."""

import importlib.util
import sys
import traceback
from pathlib import Path

import numpy as np
from novaengine import ActionInput, GameAction


REPO_ROOT = Path(__file__).resolve().parents[5]
SRC_PATH = REPO_ROOT / "prior-games/kp9z/kp9z.py"
PASCAL = "Kp9z"


def load_module():
    spec = importlib.util.spec_from_file_location("smoke_kp9z", SRC_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mod = load_module()
    GameClass = getattr(mod, PASCAL)
    src_text = SRC_PATH.read_text()

    LETTER_BOX = getattr(mod, "PALETTE_FRAME", 0)
    BACKGROUND = getattr(mod, "PALETTE_BACKDROP", 0)

    g = GameClass()
    N_LEVELS = len(g._levels)
    print(f"# Smoke test for kp9z (N_LEVELS={N_LEVELS})")

    failures = []

    # CHECK_CAMERA_VIEWPORT
    print("\n## CHECK_CAMERA_VIEWPORT")
    for L in range(N_LEVELS):
        g.set_level(L)
        gw, gh = g.current_level.grid_size or (64, 64)
        cam_w = g.camera._width
        cam_h = g.camera._height
        match = cam_w == gw and cam_h == gh
        print(f"  L{L+1}: grid={gw}x{gh}, camera={cam_w}x{cam_h}, match={match}")
        if not match:
            failures.append(("CHECK_CAMERA_VIEWPORT", L, f"camera ({cam_w}, {cam_h}) != grid ({gw}, {gh})"))

    # CHECK_SPRITE_CONTENT
    print("\n## CHECK_SPRITE_CONTENT")
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = g.camera.render(g.current_level.get_sprites())
        non_lb = frame[frame != LETTER_BOX]
        distinct = sorted(set(np.unique(non_lb).tolist()))
        print(f"  L{L+1}: distinct non-letter-box palettes: {distinct} (count={len(distinct)})")
        if len(distinct) < 2:
            failures.append(("CHECK_SPRITE_CONTENT", L, f"only {len(distinct)} distinct non-LB palettes"))

    # CHECK_ACTION_BRANCHES
    print("\n## CHECK_ACTION_BRANCHES")
    for action_id in g._available_actions:
        needle = f"GameAction.ACTION{action_id}"
        present = needle in src_text
        print(f"  ACTION{action_id}: {'OK' if present else 'MISSING'}")
        if not present:
            failures.append(("CHECK_ACTION_BRANCHES", "all", f"ACTION{action_id} not in source"))

    # CHECK_ACTION_RUNTIME
    print("\n## CHECK_ACTION_RUNTIME")
    for action_id in g._available_actions:
        try:
            g_fresh = GameClass()
            prev_count = g_fresh._action_count
            if action_id == 6:
                g_fresh.perform_action(
                    ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}),
                    raw=True,
                )
            else:
                g_fresh.perform_action(
                    ActionInput(id=GameAction.from_id(action_id)),
                    raw=True,
                )
            after_count = g_fresh._action_count
            print(f"  ACTION{action_id}: OK ({prev_count} -> {after_count})")
        except Exception as e:
            tb = traceback.format_exc()
            print(f"  ACTION{action_id}: RAISED {type(e).__name__}: {e}")
            print(tb)
            failures.append(("CHECK_ACTION_RUNTIME", "all", f"ACTION{action_id} raised {type(e).__name__}: {e}"))

    # CHECK_PALETTE_RANGE
    print("\n## CHECK_PALETTE_RANGE")
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = g.camera.render(g.current_level.get_sprites())
        mn, mx = int(frame.min()), int(frame.max())
        in_range = mn >= 0 and mx <= 15
        print(f"  L{L+1}: range [{mn}, {mx}] in_range={in_range}")
        if not in_range:
            failures.append(("CHECK_PALETTE_RANGE", L, f"range [{mn}, {mx}] outside [0,15]"))

    # CHECK_WIN_PATH_EXISTS
    print("\n## CHECK_WIN_PATH_EXISTS")
    has_next_level = "self.next_level()" in src_text
    has_win = "self.win()" in src_text
    win_path_ok = has_next_level or has_win
    print(f"  has_next_level={has_next_level}, has_win={has_win}, win_path_ok={win_path_ok}")
    if not win_path_ok:
        failures.append(("CHECK_WIN_PATH_EXISTS", "all", "no next_level/win calls"))

    # CHECK_LOSE_PATH_EXISTS
    print("\n## CHECK_LOSE_PATH_EXISTS")
    has_lose = "self.lose()" in src_text
    print(f"  has_lose={has_lose}")
    if not has_lose:
        failures.append(("CHECK_LOSE_PATH_EXISTS", "all", "no lose() call"))

    # CHECK_CAMERA_DEFAULT
    print("\n## CHECK_CAMERA_DEFAULT")
    needs_resize = any(
        g._levels[i].grid_size != g._levels[0].grid_size
        for i in range(1, N_LEVELS)
    )
    if needs_resize:
        has_resize = "self.camera.width" in src_text and "self.camera.height" in src_text
        print(f"  needs_per_level_camera={needs_resize}, has_resize={has_resize}")
        if not has_resize:
            failures.append(("CHECK_CAMERA_DEFAULT", "all", "camera not resized per level"))
    else:
        print(f"  needs_per_level_camera=False (all levels same grid_size)")

    print(f"\n# Total failures: {len(failures)}")
    for f in failures:
        print(f"  {f}")

    return failures


if __name__ == "__main__":
    main()
