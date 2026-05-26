"""Render initial frames of mr5q L1, L2, L3 to PNGs for visual sanity check."""

import importlib.util
from pathlib import Path

import numpy as np
from PIL import Image


SRC = Path("prior-games/mr5q/mr5q.py")
sp = importlib.util.spec_from_file_location("smoke_mr5q", SRC)
mod = importlib.util.module_from_spec(sp)
sp.loader.exec_module(mod)
GameClass = getattr(mod, "Mr5q")


PALETTE = np.array(
    [
        (0xFF, 0xFF, 0xFF),  # 0 white
        (0xD2, 0xD2, 0xD2),  # 1 off-white / cream
        (0xA0, 0xA0, 0xA0),  # 2 light-grey
        (0x64, 0x64, 0x64),  # 3 grey
        (0x3C, 0x3C, 0x3C),  # 4 off-black
        (0x00, 0x00, 0x00),  # 5 black
        (0xE5, 0x3A, 0xA3),  # 6 magenta
        (0xFF, 0x7B, 0xCC),  # 7 pink
        (0xF9, 0x3C, 0x31),  # 8 red
        (0x1E, 0x93, 0xFF),  # 9 blue
        (0x87, 0xD8, 0xF1),  # 10 light-blue
        (0xFF, 0xDC, 0x00),  # 11 yellow
        (0xFF, 0x85, 0x1B),  # 12 orange
        (0x92, 0x12, 0x31),  # 13 maroon
        (0x4F, 0xCC, 0x30),  # 14 green
        (0x88, 0x37, 0x9B),  # 15 purple
    ],
    dtype=np.uint8,
)


out_dir = Path(
    "runs/2026-05-07T13-19-09-autonomous/workspace/smoke-frames"
)
out_dir.mkdir(parents=True, exist_ok=True)

g = GameClass()
N = len(g._levels)
for L in range(min(3, N)):
    g.set_level(L)
    frame = g.camera.render(g.current_level.get_sprites())
    arr = np.array(frame).clip(0, 15)
    rgb = PALETTE[arr]
    img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
    img.save(out_dir / f"level_{L+1}.png")
    print(f"saved level_{L+1}.png")
