"""Smoke test runner for tm5x.

Runs the 10 universal checks plus the 4 custom checks and reports.
"""

import importlib.util
import sys
import traceback
from pathlib import Path

import numpy as np

REPO_ROOT = Path("/Users/nickhe/Programming/NovaPlay-Agents")
GAME_ID = "tm5x"
PASCAL = "Tm5x"
SRC = REPO_ROOT / f"prior-games/{GAME_ID}/{GAME_ID}.py"
WORKSPACE = REPO_ROOT / f"runs/2026-05-07T21-16-26/workspace"


def load_game_module():
    spec = importlib.util.spec_from_file_location(f"smoke_{GAME_ID}", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    print("=" * 60)
    print("Smoke test for", GAME_ID)
    print("=" * 60)

    mod = load_game_module()
    GameClass = getattr(mod, PASCAL)
    LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
    BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)
    src_text = SRC.read_text()
    g = GameClass()
    N_LEVELS = len(g._levels)
    print(f"  N_LEVELS={N_LEVELS}, BACKGROUND={BACKGROUND}, LETTER_BOX={LETTER_BOX}")

    from novaengine import ActionInput, GameAction, InteractionMode

    results = {"universal": [], "custom": []}

    # ============================================================
    # CHECK_CAMERA_VIEWPORT
    # ============================================================
    print("\n[1] CHECK_CAMERA_VIEWPORT")
    cam_match_per_level = []
    for L in range(N_LEVELS):
        g.set_level(L)
        gw, gh = g.current_level.grid_size or (64, 64)
        cam_w, cam_h = g.camera._width, g.camera._height
        match = cam_w == gw and cam_h == gh
        cam_match_per_level.append((L, gw, gh, cam_w, cam_h, match))
        print(f"  L{L+1}: grid_size={gw,gh}, camera={cam_w,cam_h}, match={match}")
    cam_pass = all(m[5] for m in cam_match_per_level)
    results["universal"].append(
        ("CHECK_CAMERA_VIEWPORT", cam_pass, str(cam_match_per_level))
    )

    # ============================================================
    # CHECK_SPRITE_CONTENT
    # ============================================================
    print("\n[2] CHECK_SPRITE_CONTENT")
    sprite_distinct = []
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = g.camera.render(g.current_level.get_sprites())
        distinct = set(np.unique(frame[frame != LETTER_BOX]).tolist())
        sprite_distinct.append((L, len(distinct), sorted(distinct)))
        print(f"  L{L+1}: distinct_non_letterbox={len(distinct)} values={sorted(distinct)}")
    sprite_pass = all(d[1] >= 2 for d in sprite_distinct)
    results["universal"].append(
        ("CHECK_SPRITE_CONTENT", sprite_pass, str(sprite_distinct))
    )

    # ============================================================
    # CHECK_ACTION_BRANCHES
    # ============================================================
    print("\n[3] CHECK_ACTION_BRANCHES")
    declared = list(g._available_actions)
    branch_results = []
    for action_id in declared:
        needle = f"GameAction.ACTION{action_id}"
        present = needle in src_text
        branch_results.append((action_id, present))
        print(f"  ACTION{action_id}: needle present in source = {present}")
    branch_pass = all(p[1] for p in branch_results)
    results["universal"].append(("CHECK_ACTION_BRANCHES", branch_pass, str(branch_results)))

    # ============================================================
    # CHECK_ACTION_RUNTIME
    # ============================================================
    print("\n[4] CHECK_ACTION_RUNTIME")
    runtime_results = []
    for action_id in declared:
        try:
            g_fresh = GameClass()
            n0 = g_fresh._action_count
            g_fresh.perform_action(
                ActionInput(id=GameAction.from_id(action_id)), raw=True
            )
            n1 = g_fresh._action_count
            runtime_results.append((action_id, "OK", n0, n1))
            print(f"  ACTION{action_id}: OK ({n0}->{n1})")
        except Exception as e:
            runtime_results.append((action_id, "ERROR", repr(e)))
            print(f"  ACTION{action_id}: ERROR {e}")
            traceback.print_exc()
    runtime_pass = all(r[1] == "OK" for r in runtime_results)
    results["universal"].append(("CHECK_ACTION_RUNTIME", runtime_pass, str(runtime_results)))

    # ============================================================
    # CHECK_PALETTE_RANGE
    # ============================================================
    print("\n[5] CHECK_PALETTE_RANGE")
    palette_per_level = []
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = g.camera.render(g.current_level.get_sprites())
        mn, mx = int(frame.min()), int(frame.max())
        ok = 0 <= mn and mx <= 15
        palette_per_level.append((L, mn, mx, ok))
        print(f"  L{L+1}: min={mn} max={mx} ok={ok}")
    palette_pass = all(p[3] for p in palette_per_level)
    results["universal"].append(("CHECK_PALETTE_RANGE", palette_pass, str(palette_per_level)))

    # ============================================================
    # CHECK_WIN_PATH_EXISTS
    # ============================================================
    print("\n[6] CHECK_WIN_PATH_EXISTS")
    has_next_level = "self.next_level()" in src_text
    has_win = "self.win()" in src_text
    win_pass = has_next_level or has_win
    print(f"  has_next_level={has_next_level} has_win={has_win}")
    results["universal"].append(
        ("CHECK_WIN_PATH_EXISTS", win_pass, f"next_level={has_next_level} win={has_win}")
    )

    # ============================================================
    # CHECK_WITNESS_WINS
    # ============================================================
    print("\n[7] CHECK_WITNESS_WINS")
    A = GameAction

    def act(n):
        return ActionInput(id=A.from_id(n), data={})

    # Witnesses from spec.
    L1_WITNESS = [act(2)] * 5
    L2_WITNESS = [act(3)] * 5 + [act(5)] + [act(4)] * 10
    L3_WITNESS = (
        [act(2)] * 12
        + [act(5)]
        + [act(1)] * 10
        + [act(4)] * 10
        + [act(2)] * 10
    )
    WITNESSES = {1: L1_WITNESS, 2: L2_WITNESS, 3: L3_WITNESS}

    g.handle_reset()
    print(f"  after reset: state={g._state.name} score={g._score} action_count={g._action_count}")
    witness_failures = []
    for level_idx in (1, 2, 3):
        score_before = g._score
        if score_before != level_idx - 1:
            witness_failures.append(
                f"L{level_idx}: score before witness was {score_before}, expected {level_idx-1}"
            )
            break
        for ai in WITNESSES[level_idx]:
            g.perform_action(ai, raw=True)
            if g._state.name in ("WIN", "GAME_OVER"):
                break
        print(
            f"  after L{level_idx} witness: state={g._state.name} score={g._score} action_count={g._action_count}"
        )
        if level_idx < 3:
            if g._score != level_idx:
                witness_failures.append(
                    f"L{level_idx}: witness did not advance level "
                    f"(score {score_before}->{g._score}, expected {level_idx}); state={g._state.name}"
                )
                break
        else:
            if g._state.name != "WIN":
                witness_failures.append(
                    f"L{level_idx}: witness did not reach WIN "
                    f"(state={g._state.name}, score={g._score})"
                )
    witness_pass = not witness_failures
    print(f"  failures: {witness_failures}")
    results["universal"].append(("CHECK_WITNESS_WINS", witness_pass, str(witness_failures)))

    # ============================================================
    # CHECK_LOSE_PATH_EXISTS
    # ============================================================
    print("\n[8] CHECK_LOSE_PATH_EXISTS")
    has_lose = "self.lose()" in src_text
    print(f"  has_lose={has_lose}")
    results["universal"].append(("CHECK_LOSE_PATH_EXISTS", has_lose, str(has_lose)))

    # ============================================================
    # CHECK_CAMERA_DEFAULT
    # ============================================================
    print("\n[9] CHECK_CAMERA_DEFAULT")
    needs_per_level_camera = any(
        g._levels[i].grid_size != g._levels[0].grid_size for i in range(1, N_LEVELS)
    )
    if needs_per_level_camera:
        has_resize = "self.camera.width" in src_text and "self.camera.height" in src_text
        cam_default_pass = has_resize
    else:
        cam_default_pass = True
    print(f"  needs_per_level_camera={needs_per_level_camera} pass={cam_default_pass}")
    results["universal"].append(
        ("CHECK_CAMERA_DEFAULT", cam_default_pass, f"needs={needs_per_level_camera}")
    )

    # ============================================================
    # CHECK_VISUAL_SANITY (render frames; vision pass deferred to agent)
    # ============================================================
    print("\n[10] CHECK_VISUAL_SANITY (rendering frames)")
    try:
        from PIL import Image

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

        out_dir = WORKSPACE / "smoke-frames"
        out_dir.mkdir(parents=True, exist_ok=True)
        g_render = GameClass()
        for L in range(min(3, N_LEVELS)):
            g_render.set_level(L)
            frame = g_render.camera.render(g_render.current_level.get_sprites())
            rgb = PALETTE[np.clip(frame, 0, 15)]
            img = Image.fromarray(rgb).resize((512, 512), Image.NEAREST)
            img.save(out_dir / f"level_{L+1}.png")
            print(f"  L{L+1}: saved frame")
        results["universal"].append(("CHECK_VISUAL_SANITY", True, "frames rendered"))
    except Exception as e:
        traceback.print_exc()
        results["universal"].append(("CHECK_VISUAL_SANITY", False, repr(e)))

    # ============================================================
    # Custom checks
    # ============================================================
    print("\n[Custom] Running custom checks")
    sys.path.insert(0, str(WORKSPACE))
    try:
        import smoke_test_custom as smk_custom
    except ImportError:
        # The file is named smoke-test-custom.py with hyphens; importlib it.
        custom_spec = importlib.util.spec_from_file_location(
            "smoke_test_custom", WORKSPACE / "smoke-test-custom.py"
        )
        smk_custom = importlib.util.module_from_spec(custom_spec)
        custom_spec.loader.exec_module(smk_custom)

    custom_checks = [
        smk_custom.check_down_moves_pawn,
        smk_custom.check_action5_toggles_polarity,
        smk_custom.check_action5_swaps_pawn_variant,
        smk_custom.check_imprint_at_pawn_cell,
    ]
    for check in custom_checks:
        try:
            passed, observed = check(GameClass)
            print(f"  {check.__name__}: passed={passed} observed={observed!r}")
            results["custom"].append((check.__name__, passed, observed))
        except Exception as e:
            traceback.print_exc()
            results["custom"].append((check.__name__, False, f"raised {e!r}"))

    # ============================================================
    # Summary
    # ============================================================
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for cat in ("universal", "custom"):
        for name, passed, obs in results[cat]:
            status = "PASS" if passed else "FAIL"
            print(f"  [{cat:9}] {name:32} {status}")

    all_pass = all(r[1] for r in results["universal"]) and all(
        r[1] for r in results["custom"]
    )
    print(f"\nOverall: {'PASS' if all_pass else 'FAIL'}")
    return all_pass, results


if __name__ == "__main__":
    main()
