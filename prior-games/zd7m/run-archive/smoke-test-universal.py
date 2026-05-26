"""Universal smoke-test checks for zd7m, per skills/code/smoke-test-checks.md."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "prior-games/zd7m/zd7m.py"
WORKSPACE = Path(__file__).resolve().parent

PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)


def load():
    spec = importlib.util.spec_from_file_location("smoke_zd7m", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mod = load()
    GameClass = mod.Zd7m
    g = GameClass()
    LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
    BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)
    N_LEVELS = len(g._levels)

    src_text = SRC.read_text()
    declared = list(g._available_actions)

    failures: list[str] = []

    # CHECK_CAMERA_VIEWPORT
    cam_match_per_level = []
    for L in range(N_LEVELS):
        g.set_level(L)
        gw, gh = g.current_level.grid_size or (64, 64)
        cw, ch = g.camera._width, g.camera._height
        cam_match_per_level.append((cw == gw and ch == gh, gw, gh, cw, ch))
    if not all(m[0] for m in cam_match_per_level):
        failures.append(f"CHECK_CAMERA_VIEWPORT: {cam_match_per_level}")

    # CHECK_SPRITE_CONTENT
    distinct_palettes = []
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = g.camera.render(g.current_level.get_sprites())
        non_lb = frame[frame != LETTER_BOX]
        ds = set(np.unique(non_lb).tolist())
        distinct_palettes.append((len(ds), sorted(ds)))
    if not all(p[0] >= 2 for p in distinct_palettes):
        failures.append(f"CHECK_SPRITE_CONTENT: {distinct_palettes}")

    # CHECK_ACTION_BRANCHES
    branches_present = {a: f"GameAction.ACTION{a}" in src_text for a in declared}
    if not all(branches_present.values()):
        failures.append(f"CHECK_ACTION_BRANCHES: {branches_present}")

    # CHECK_ACTION_RUNTIME
    from novaengine import GameAction, ActionInput
    runtime_per_action = {}
    for a in declared:
        try:
            g_fresh = GameClass()
            if a == 6:
                g_fresh.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True)
            else:
                g_fresh.perform_action(ActionInput(id=GameAction.from_id(a)), raw=True)
            runtime_per_action[a] = "OK"
        except Exception as e:
            runtime_per_action[a] = f"{type(e).__name__}: {e}"
    if not all(v == "OK" for v in runtime_per_action.values()):
        failures.append(f"CHECK_ACTION_RUNTIME: {runtime_per_action}")

    # CHECK_PALETTE_RANGE
    palette_per_level = []
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = g.camera.render(g.current_level.get_sprites())
        palette_per_level.append((int(frame.min()), int(frame.max())))
    if not all(0 <= mn and mx <= 15 for mn, mx in palette_per_level):
        failures.append(f"CHECK_PALETTE_RANGE: {palette_per_level}")

    # CHECK_WIN_PATH_EXISTS
    has_win = ("self.next_level()" in src_text) or ("self.win()" in src_text)
    if not has_win:
        failures.append("CHECK_WIN_PATH_EXISTS: neither next_level() nor win() in source")

    # CHECK_LOSE_PATH_EXISTS
    has_lose = "self.lose()" in src_text
    if not has_lose:
        failures.append("CHECK_LOSE_PATH_EXISTS: no self.lose() in source")

    # CHECK_CAMERA_DEFAULT
    needs_per_level_camera = any(
        g._levels[i].grid_size != g._levels[0].grid_size for i in range(1, N_LEVELS)
    )
    if needs_per_level_camera:
        has_resize = ("self.camera.width" in src_text and "self.camera.height" in src_text)
        if not has_resize:
            failures.append("CHECK_CAMERA_DEFAULT: levels have different grid_size but source does not resize camera")
    else:
        has_resize = "n/a (all levels same grid_size)"

    # Render frames to PNG for visual inspection
    out_dir = WORKSPACE / "smoke-frames"
    out_dir.mkdir(parents=True, exist_ok=True)
    for L in range(min(3, N_LEVELS)):
        g.set_level(L)
        frame = g.camera.render(g.current_level.get_sprites())
        rgb = PALETTE[frame.clip(0, 15)]
        img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
        img.save(out_dir / f"level_{L+1}.png")

    print("== Smoke test results ==")
    print(f"CHECK_CAMERA_VIEWPORT      {cam_match_per_level}")
    print(f"CHECK_SPRITE_CONTENT       {distinct_palettes}")
    print(f"CHECK_ACTION_BRANCHES      {branches_present}")
    print(f"CHECK_ACTION_RUNTIME       {runtime_per_action}")
    print(f"CHECK_PALETTE_RANGE        {palette_per_level}")
    print(f"CHECK_WIN_PATH_EXISTS      next_level()={'self.next_level()' in src_text} win()={'self.win()' in src_text}")
    print(f"CHECK_LOSE_PATH_EXISTS     lose()={has_lose}")
    print(f"CHECK_CAMERA_DEFAULT       {has_resize}")
    print(f"PNGs written to            {out_dir}")
    print()
    if failures:
        print("FAILURES:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("ALL UNIVERSAL CHECKS PASS (CHECK_VISUAL_SANITY pending agent vision pass)")
        sys.exit(0)


if __name__ == "__main__":
    main()
