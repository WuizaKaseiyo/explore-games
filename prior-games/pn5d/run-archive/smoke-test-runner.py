"""Single-shot smoke test runner for pn5d. Runs all universal + custom checks."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
from novaengine import ActionInput, GameAction


SRC = Path("prior-games/pn5d/pn5d.py")


def load():
    spec = importlib.util.spec_from_file_location("smoke_pn5d", SRC)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    mod = load()
    GameClass = mod.Pn5d
    LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
    BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)
    g = GameClass()
    N = len(g._levels)
    src_text = SRC.read_text()

    results = {}

    # CHECK_CAMERA_VIEWPORT
    cam_match = []
    for i in range(N):
        g.set_level(i)
        gw, gh = g.current_level.grid_size or (64, 64)
        cw, ch = g.camera._width, g.camera._height
        cam_match.append((gw, gh) == (cw, ch))
    results["CHECK_CAMERA_VIEWPORT"] = (all(cam_match), f"per-level matches={cam_match}")

    # CHECK_SPRITE_CONTENT
    distincts = []
    for i in range(N):
        g.set_level(i)
        frame = g.camera.render(g.current_level.get_sprites())
        non_lb = set(np.unique(frame[frame != LETTER_BOX]).tolist())
        distincts.append(len(non_lb))
    results["CHECK_SPRITE_CONTENT"] = (
        all(d >= 2 for d in distincts),
        f"distinct counts per level={distincts}",
    )

    # CHECK_ACTION_BRANCHES
    declared = list(g._available_actions)
    missing = [a for a in declared if f"GameAction.ACTION{a}" not in src_text]
    results["CHECK_ACTION_BRANCHES"] = (
        not missing,
        f"declared={declared} missing={missing}",
    )

    # CHECK_ACTION_RUNTIME
    runtime_errors = []
    for action_id in declared:
        g_fresh = GameClass()
        try:
            if action_id == 6:
                g_fresh.perform_action(
                    ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}),
                    raw=True,
                )
            else:
                g_fresh.perform_action(
                    ActionInput(id=GameAction.from_id(action_id)), raw=True
                )
        except Exception as e:
            runtime_errors.append(f"ACTION{action_id}: {type(e).__name__}: {e}")
    results["CHECK_ACTION_RUNTIME"] = (
        not runtime_errors,
        f"errors={runtime_errors}" if runtime_errors else "no exceptions",
    )

    # CHECK_PALETTE_RANGE
    ranges = []
    for i in range(N):
        g.set_level(i)
        frame = g.camera.render(g.current_level.get_sprites())
        ranges.append((int(frame.min()), int(frame.max())))
    in_range = all(0 <= mn and mx <= 15 for mn, mx in ranges)
    results["CHECK_PALETTE_RANGE"] = (in_range, f"per-level (min,max)={ranges}")

    # CHECK_WIN_PATH_EXISTS
    has_win = "self.next_level()" in src_text or "self.win()" in src_text
    results["CHECK_WIN_PATH_EXISTS"] = (has_win, "next_level/win calls present" if has_win else "missing")

    # CHECK_LOSE_PATH_EXISTS
    has_lose = "self.lose()" in src_text
    results["CHECK_LOSE_PATH_EXISTS"] = (has_lose, "lose() present" if has_lose else "missing")

    # CHECK_CAMERA_DEFAULT
    sizes = [g._levels[i].grid_size for i in range(N)]
    needs_per_level = any(s != sizes[0] for s in sizes[1:])
    if needs_per_level:
        has_resize = (
            "self.camera.width" in src_text and "self.camera.height" in src_text
        )
        results["CHECK_CAMERA_DEFAULT"] = (
            has_resize,
            f"sizes={sizes} resize_present={has_resize}",
        )
    else:
        results["CHECK_CAMERA_DEFAULT"] = (True, f"all levels share grid_size={sizes[0]}")

    # CHECK_WITNESS_WINS
    A = GameAction
    def click(x, y):
        return ActionInput(id=A.ACTION6, data={"x": x, "y": y})
    def act(n):
        return ActionInput(id=A.from_id(n), data={})

    # L1 witness: 4 pours.
    # L2 witness (10 actions): pour x2, click(24,19), click(34,19), pour, ACTION4 x2, pour x3.
    # L3 witness (12 actions): click(20,19), click(31,19), click(42,19), pour x9.
    WITNESSES = {
        1: [act(5), act(5), act(5), act(5)],
        2: [
            act(5), act(5),
            click(24, 19),
            click(34, 19),
            act(5),
            act(4), act(4),
            act(5), act(5), act(5),
        ],
        3: [
            click(20, 19), click(31, 19), click(42, 19),
            act(5), act(5), act(5), act(5), act(5),
            act(5), act(5), act(5), act(5),
        ],
    }

    g_w = GameClass()
    g_w.handle_reset()
    witness_failures = []
    for level_idx in range(1, N + 1):
        score_before = g_w._score
        if score_before != level_idx - 1:
            witness_failures.append(
                f"L{level_idx}: score == {score_before} before replay (expected {level_idx-1}); "
                f"state == {g_w._state.name}"
            )
            break
        for ai in WITNESSES[level_idx]:
            g_w.perform_action(ai)
        if level_idx < N:
            if g_w._score != level_idx:
                witness_failures.append(
                    f"L{level_idx}: score after witness = {g_w._score} (expected {level_idx}); "
                    f"state = {g_w._state.name}; vessels={[v['level'] for v in g_w._vessels]}; "
                    f"valves={[v['is_open'] for v in g_w._valves]}"
                )
                break
        else:
            if g_w._state.name != "WIN":
                witness_failures.append(
                    f"L{level_idx}: state after witness = {g_w._state.name} (expected WIN); "
                    f"score = {g_w._score}; vessels={[v['level'] for v in g_w._vessels]}"
                )
                break
    results["CHECK_WITNESS_WINS"] = (
        not witness_failures,
        f"failures={witness_failures}" if witness_failures else "all 3 witnesses won",
    )

    # CHECK_VISUAL_SANITY: render PNGs.
    try:
        from PIL import Image
    except ImportError:
        results["CHECK_VISUAL_SANITY"] = (False, "PIL not available")
    else:
        PALETTE = np.array(
            [
                (0xFF, 0xFF, 0xFF), (0xD2, 0xD2, 0xD2), (0xA0, 0xA0, 0xA0),
                (0x64, 0x64, 0x64), (0x3C, 0x3C, 0x3C), (0x00, 0x00, 0x00),
                (0xE5, 0x3A, 0xA3), (0xFF, 0x7B, 0xCC), (0xF9, 0x3C, 0x31),
                (0x1E, 0x93, 0xFF), (0x87, 0xD8, 0xF1), (0xFF, 0xDC, 0x00),
                (0xFF, 0x85, 0x1B), (0x92, 0x12, 0x31), (0x4F, 0xCC, 0x30),
                (0x88, 0x37, 0x9B),
            ],
            dtype=np.uint8,
        )
        out_dir = Path(
            "runs/2026-05-08T21-16-07/workspace/smoke-frames"
        )
        out_dir.mkdir(parents=True, exist_ok=True)
        for i in range(N):
            g.set_level(i)
            frame = g.camera.render(g.current_level.get_sprites())
            rgb = PALETTE[frame.clip(0, 15)]
            img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
            img.save(out_dir / f"level_{i+1}.png")
        results["CHECK_VISUAL_SANITY"] = (True, f"PNGs written to {out_dir}")

    # Custom checks
    custom_path = Path(
        "runs/2026-05-08T21-16-07/workspace/smoke-test-custom.py"
    )
    custom_spec = importlib.util.spec_from_file_location("smoke_custom", custom_path)
    custom_module = importlib.util.module_from_spec(custom_spec)
    custom_spec.loader.exec_module(custom_module)

    custom_results = []
    for fn in custom_module.CUSTOM_CHECKS:
        try:
            ok, msg = fn()
            custom_results.append((fn.__name__, ok, msg))
        except Exception as e:
            custom_results.append((fn.__name__, False, f"{type(e).__name__}: {e}"))

    # Print
    print("=== Universal checks ===")
    for k, (ok, msg) in results.items():
        tag = "PASS" if ok else "FAIL"
        print(f"  {tag} {k}: {msg}")

    print("=== Custom checks ===")
    for name, ok, msg in custom_results:
        tag = "PASS" if ok else "FAIL"
        print(f"  {tag} {name}: {msg}")

    all_ok = all(ok for ok, _ in results.values()) and all(ok for _, ok, _ in custom_results)
    print(f"\nOverall: {'ALL PASS' if all_ok else 'FAILURES PRESENT'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
