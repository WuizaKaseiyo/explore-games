"""Universal smoke-test runner for pj7k. Writes PNGs and reports."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from novaengine import ActionInput, GameAction


SRC = Path("prior-games/pj7k/pj7k.py")
PASCAL = "Pj7K"
ID = "pj7k"

PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)


def load():
    spec = importlib.util.spec_from_file_location(f"smoke_{ID}", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, getattr(mod, PASCAL)


def main():
    mod, GameClass = load()
    g = GameClass()
    LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
    BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)
    N_LEVELS = len(g._levels)
    src_text = SRC.read_text()
    failures = []

    # CHECK_CAMERA_VIEWPORT
    for L in range(N_LEVELS):
        g.set_level(L)
        gw, gh = g.current_level.grid_size or (64, 64)
        cw, ch = g.camera._width, g.camera._height
        if (cw, ch) != (gw, gh):
            failures.append(("CHECK_CAMERA_VIEWPORT", L+1,
                             f"camera ({cw},{ch}), grid ({gw},{gh}) mismatch"))

    # CHECK_SPRITE_CONTENT
    distinct_per_level = []
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = g.camera.render(g.current_level.get_sprites())
        non_lb = frame[frame != LETTER_BOX]
        distinct = set(np.unique(non_lb).tolist()) if non_lb.size else set()
        distinct_per_level.append(distinct)
        if len(distinct) < 2:
            failures.append(("CHECK_SPRITE_CONTENT", L+1,
                             f"only {len(distinct)} non-letterbox palettes"))

    # CHECK_ACTION_BRANCHES
    declared = list(g._available_actions)
    for aid in declared:
        needle = f"GameAction.ACTION{aid}"
        if needle not in src_text:
            failures.append(("CHECK_ACTION_BRANCHES", "all",
                             f"ACTION{aid} declared but no step branch"))

    # CHECK_ACTION_RUNTIME
    for aid in declared:
        gf = GameClass()
        try:
            if aid == 6:
                gf.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True)
            else:
                gf.perform_action(ActionInput(id=GameAction.from_id(aid)), raw=True)
        except Exception as e:
            failures.append(("CHECK_ACTION_RUNTIME", "all",
                             f"ACTION{aid} raised {type(e).__name__}: {e}"))

    # CHECK_PALETTE_RANGE
    palette_ranges = []
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = g.camera.render(g.current_level.get_sprites())
        mn, mx = int(frame.min()), int(frame.max())
        palette_ranges.append((mn, mx))
        if mn < 0 or mx > 15:
            failures.append(("CHECK_PALETTE_RANGE", L+1,
                             f"frame min/max ({mn},{mx}) outside [0,15]"))

    # CHECK_WIN_PATH_EXISTS
    if not ("self.next_level()" in src_text or "self.win()" in src_text):
        failures.append(("CHECK_WIN_PATH_EXISTS", "all", "no next_level()/win() found"))

    # CHECK_LOSE_PATH_EXISTS
    if "self.lose()" not in src_text:
        failures.append(("CHECK_LOSE_PATH_EXISTS", "all", "no lose() found"))

    # CHECK_CAMERA_DEFAULT
    grids = [g._levels[i].grid_size for i in range(N_LEVELS)]
    needs_resize = any(grids[i] != grids[0] for i in range(1, N_LEVELS))
    if needs_resize:
        if not ("self.camera.width" in src_text and "self.camera.height" in src_text):
            failures.append(("CHECK_CAMERA_DEFAULT", "all",
                             f"levels differ ({grids}) but no camera resize"))
    # In our case all grid_size=(16,16) so this check is vacuously OK.

    # CHECK_VISUAL_SANITY — render PNGs
    out_dir = Path("workspace/smoke-frames")
    out_dir.mkdir(parents=True, exist_ok=True)
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = g.camera.render(g.current_level.get_sprites())
        rgb = PALETTE[frame.clip(0, 15)]
        img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
        img.save(out_dir / f"level_{L+1}.png")

    # Print summary
    print(f"=== UNIVERSAL CHECKS — {len(failures)} failures ===")
    for f in failures:
        print(" ", f)
    print(f"distinct palettes per level: {[len(d) for d in distinct_per_level]}")
    print(f"palette ranges: {palette_ranges}")
    print(f"PNGs: {out_dir}")
    print()
    return failures


if __name__ == "__main__":
    sys.exit(0 if not main() else 1)
