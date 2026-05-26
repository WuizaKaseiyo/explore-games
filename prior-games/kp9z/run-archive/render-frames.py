"""Render initial frames for kp9z to PNG."""

import importlib.util
from pathlib import Path

import numpy as np
from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[5]
SRC_PATH = REPO_ROOT / "prior-games/kp9z/kp9z.py"
WORKSPACE = REPO_ROOT / "runs/2026-05-06T22-15-15/workspace"

PALETTE = np.array([
    (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
    (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
    (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
    (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
    (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
    (0x88, 0x37, 0x9B),
], dtype=np.uint8)


def main():
    spec = importlib.util.spec_from_file_location("smoke_kp9z", SRC_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    g = mod.Kp9z()
    out_dir = WORKSPACE / "smoke-frames"
    out_dir.mkdir(parents=True, exist_ok=True)
    for L in range(3):
        g.set_level(L)
        frame = g.camera.render(g.current_level.get_sprites())
        rgb = PALETTE[frame.clip(0, 15)]
        img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
        path = out_dir / f"level_{L+1}.png"
        img.save(path)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
