"""Smoke-test runner for fz5j. Run from repo root."""

import importlib.util
import sys
import traceback
from pathlib import Path

import numpy as np
from novaengine import ActionInput, GameAction
from PIL import Image


def load_game():
    src = Path("prior-games/fz5j/fz5j.py")
    spec = importlib.util.spec_from_file_location("smoke_fz5j", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, getattr(mod, "Fz5j")


def main():
    mod, GameClass = load_game()
    src_text = Path("prior-games/fz5j/fz5j.py").read_text()
    LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
    BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)
    g = GameClass()
    n_levels = len(g._levels)

    results = {}

    # CHECK_CAMERA_VIEWPORT
    results["camera_viewport"] = []
    for i in range(n_levels):
        g.set_level(i)
        gw, gh = g.current_level.grid_size or (64, 64)
        cw, ch = g.camera._width, g.camera._height
        results["camera_viewport"].append(
            {"level": i + 1, "match": cw == gw and ch == gh, "cam": (cw, ch), "grid": (gw, gh)}
        )

    # CHECK_SPRITE_CONTENT
    results["sprite_content"] = []
    for i in range(n_levels):
        g.set_level(i)
        frame = g.camera.render(g.current_level.get_sprites())
        unique = set(np.unique(frame[frame != LETTER_BOX]).tolist())
        results["sprite_content"].append(
            {"level": i + 1, "n_distinct": len(unique), "values": sorted(unique)}
        )

    # CHECK_ACTION_BRANCHES (static text)
    g_fresh = GameClass()
    declared = list(g_fresh._available_actions)
    branches = {}
    for aid in declared:
        needle = f"GameAction.ACTION{aid}"
        branches[aid] = needle in src_text
    results["action_branches"] = branches

    # CHECK_ACTION_RUNTIME
    runtime_results = {}
    for aid in declared:
        try:
            g_fresh = GameClass()
            g_fresh.perform_action(ActionInput(id=GameAction.RESET), raw=True)
            if aid == 6:
                g_fresh.perform_action(
                    ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True
                )
            else:
                g_fresh.perform_action(ActionInput(id=GameAction.from_id(aid)), raw=True)
            runtime_results[aid] = "OK"
        except Exception as e:
            runtime_results[aid] = f"FAIL: {type(e).__name__}: {e}"
    results["action_runtime"] = runtime_results

    # CHECK_PALETTE_RANGE
    palette_range = []
    for i in range(n_levels):
        g.set_level(i)
        frame = g.camera.render(g.current_level.get_sprites())
        palette_range.append(
            {"level": i + 1, "min": int(frame.min()), "max": int(frame.max())}
        )
    results["palette_range"] = palette_range

    # CHECK_WIN_PATH_EXISTS
    results["win_path"] = "self.next_level()" in src_text or "self.win()" in src_text

    # CHECK_LOSE_PATH_EXISTS
    results["lose_path"] = "self.lose()" in src_text

    # CHECK_CAMERA_DEFAULT
    grid_sizes = [g._levels[i].grid_size for i in range(n_levels)]
    needs_resize = any(grid_sizes[i] != grid_sizes[0] for i in range(1, n_levels))
    has_resize = "self.camera.width" in src_text and "self.camera.height" in src_text
    results["camera_default"] = {"needs": needs_resize, "has": has_resize}

    # Render PNGs for visual check
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
    out_dir = Path("workspace/smoke-frames")
    out_dir.mkdir(parents=True, exist_ok=True)
    g_fresh = GameClass()
    g_fresh.perform_action(ActionInput(id=GameAction.RESET), raw=True)
    for L in range(min(3, n_levels)):
        g_fresh.set_level(L)
        frame = g_fresh.camera.render(g_fresh.current_level.get_sprites())
        rgb = PALETTE[np.clip(frame, 0, 15)]
        img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
        img.save(out_dir / f"level_{L+1}.png")

    # Custom checks
    sys.path.insert(0, str(Path("workspace").resolve()))
    import importlib
    spec_custom = importlib.util.spec_from_file_location(
        "smoke_test_custom",
        Path("workspace/smoke-test-custom.py"),
    )
    custom = importlib.util.module_from_spec(spec_custom)
    spec_custom.loader.exec_module(custom)
    custom_results = {}
    for fn_name in dir(custom):
        if fn_name.startswith("check_"):
            fn = getattr(custom, fn_name)
            try:
                passed, observed = fn(GameClass)
                custom_results[fn_name] = {"passed": passed, "observed": observed}
            except Exception:
                custom_results[fn_name] = {
                    "passed": False,
                    "observed": f"EXCEPTION: {traceback.format_exc().splitlines()[-1]}",
                }
    results["custom"] = custom_results

    print("=" * 70)
    print("UNIVERSAL CHECKS")
    print("=" * 70)
    for cv in results["camera_viewport"]:
        print(f"  camera_viewport L{cv['level']}: cam={cv['cam']} grid={cv['grid']} match={cv['match']}")
    for sc in results["sprite_content"]:
        print(f"  sprite_content L{sc['level']}: n={sc['n_distinct']} values={sc['values']}")
    print(f"  action_branches: {results['action_branches']}")
    print(f"  action_runtime: {results['action_runtime']}")
    for pr in results["palette_range"]:
        print(f"  palette_range L{pr['level']}: [{pr['min']}, {pr['max']}]")
    print(f"  win_path_exists: {results['win_path']}")
    print(f"  lose_path_exists: {results['lose_path']}")
    print(f"  camera_default: {results['camera_default']}")
    print()
    print("=" * 70)
    print("CUSTOM CHECKS")
    print("=" * 70)
    for name, res in results["custom"].items():
        print(f"  {name}: passed={res['passed']} observed={res['observed']}")


if __name__ == "__main__":
    main()
