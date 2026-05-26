"""Universal smoke checks for hl4n."""

import importlib.util
from pathlib import Path
import numpy as np
from PIL import Image

SRC = Path("prior-games/hl4n/hl4n.py")
src_text = SRC.read_text()
spec = importlib.util.spec_from_file_location("smoke_hl4n", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = mod.Hl4N

from novaengine import ActionInput, GameAction

LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)


def render_frame(g):
    return g.camera.render(g.current_level.get_sprites())


def main():
    g = GameClass()
    N_LEVELS = len(g._levels)
    print(f"N_LEVELS={N_LEVELS}, LETTER_BOX={LETTER_BOX}, BACKGROUND={BACKGROUND}")

    results = {}

    # CHECK_CAMERA_VIEWPORT
    cv = []
    for L in range(N_LEVELS):
        g.set_level(L)
        gw, gh = g.current_level.grid_size or (64, 64)
        cv.append((gw, gh, g.camera._width, g.camera._height, gw == g.camera._width and gh == g.camera._height))
    results["CAMERA_VIEWPORT"] = cv
    print(f"CAMERA_VIEWPORT: {cv}")

    # CHECK_SPRITE_CONTENT
    sc = []
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = render_frame(g)
        distinct = sorted(set(frame[frame != LETTER_BOX].tolist()))
        sc.append((L, len(distinct), distinct))
    results["SPRITE_CONTENT"] = sc
    print(f"SPRITE_CONTENT: {sc}")

    # CHECK_ACTION_BRANCHES
    declared = list(g._available_actions)
    branches = {a: f"GameAction.ACTION{a}" in src_text for a in declared}
    results["ACTION_BRANCHES"] = branches
    print(f"ACTION_BRANCHES: {branches}")

    # CHECK_ACTION_RUNTIME
    runtime = {}
    for a in declared:
        gf = GameClass()
        try:
            if a == 6:
                gf.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}))
            else:
                gf.perform_action(ActionInput(id=GameAction.from_id(a)))
            runtime[a] = "OK"
        except Exception as e:
            runtime[a] = f"FAIL: {repr(e)}"
    results["ACTION_RUNTIME"] = runtime
    print(f"ACTION_RUNTIME: {runtime}")

    # CHECK_PALETTE_RANGE
    pr = []
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = render_frame(g)
        mn, mx = int(frame.min()), int(frame.max())
        pr.append((L, mn, mx, mn >= 0 and mx <= 15))
    results["PALETTE_RANGE"] = pr
    print(f"PALETTE_RANGE: {pr}")

    # CHECK_WIN_PATH_EXISTS
    wpe = "self.next_level()" in src_text or "self.win()" in src_text
    results["WIN_PATH_EXISTS"] = wpe
    print(f"WIN_PATH_EXISTS: {wpe}")

    # CHECK_LOSE_PATH_EXISTS
    lpe = "self.lose()" in src_text
    results["LOSE_PATH_EXISTS"] = lpe
    print(f"LOSE_PATH_EXISTS: {lpe}")

    # CHECK_CAMERA_DEFAULT
    needs = any(g._levels[i].grid_size != g._levels[0].grid_size for i in range(1, N_LEVELS))
    has_resize = ("self.camera.width" in src_text and "self.camera.height" in src_text)
    results["CAMERA_DEFAULT"] = (needs, has_resize)
    print(f"CAMERA_DEFAULT: needs={needs}, has_resize={has_resize}")

    # CHECK_WITNESS_WINS
    g2 = GameClass()
    g2.handle_reset()
    failures = []
    A = GameAction
    def click(x, y):
        return ActionInput(id=A.ACTION6, data={"x": x, "y": y})

    WITNESSES = {
        1: [click(4, 20)] + [click(4, 32)] * 2 + [click(4, 44)] * 3,
        2: [click(4, 20)] + [click(32, 4)] * 2 + [click(4, 38)] * 3 + [click(4, 44)] * 3 + [click(4, 32)],
        3: [click(14, 4)] * 3 + [click(32, 4)] * 2 + [click(20, 4)] + [click(38, 4)] * 3 + [click(50, 4)] * 2 + [click(4, 44)] + [click(4, 26)] * 3,
    }

    for L in range(1, N_LEVELS + 1):
        score_before = g2._score
        if score_before != L - 1:
            failures.append(f"L{L}: expected score={L-1} before, got {score_before}")
            break
        for ai in WITNESSES[L]:
            g2.perform_action(ai)
        if L < N_LEVELS:
            if g2._score != L:
                failures.append(f"L{L}: witness did not advance: score {score_before} -> {g2._score}, state={g2._state.name}")
                break
        else:
            if g2._state.name != "WIN":
                failures.append(f"L{L}: not WIN, state={g2._state.name}, score={g2._score}")
                break
    results["WITNESS_WINS"] = failures or "PASS"
    print(f"WITNESS_WINS: {results['WITNESS_WINS']}")

    # CHECK_VISUAL_SANITY (render frames, save PNG)
    PALETTE = np.array([
        (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
        (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
        (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
        (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
        (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
        (0x88, 0x37, 0x9B),
    ], dtype=np.uint8)
    out_dir = Path("runs/2026-05-09T00-56-34/workspace/smoke-frames")
    out_dir.mkdir(parents=True, exist_ok=True)
    for L in range(min(3, N_LEVELS)):
        g.set_level(L)
        frame = render_frame(g)
        clipped = np.clip(frame, 0, 15).astype(np.int64)
        rgb = PALETTE[clipped]
        img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
        img.save(out_dir / f"level_{L+1}.png")
    print(f"saved frames to {out_dir}")

    return results


if __name__ == "__main__":
    main()
