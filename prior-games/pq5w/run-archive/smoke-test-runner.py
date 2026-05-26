"""Smoke-test runner for pq5w. Exercises the universal checks and the
custom checks; prints a structured summary."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
from novaengine import ActionInput, GameAction


GAME_ID = "pq5w"
PASCAL = "Pq5w"
SRC = Path(f"prior-games/{GAME_ID}/{GAME_ID}.py")


def load_game_class():
    spec = importlib.util.spec_from_file_location(f"smoke_{GAME_ID}", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, PASCAL), mod


def render_frame(g):
    g.camera.width = g.current_level.grid_size[0]
    g.camera.height = g.current_level.grid_size[1]
    return g.camera.render(g.current_level.get_sprites())


def main():
    GameClass, mod = load_game_class()
    LETTER_BOX = getattr(mod, "PADDING_COLOR", 0)
    BACKGROUND = getattr(mod, "BACKGROUND_COLOR", 0)
    g = GameClass()
    N_LEVELS = len(g._levels)
    src_text = SRC.read_text()
    declared = list(g._available_actions)

    failures = []

    # CHECK_CAMERA_VIEWPORT
    print("=== CHECK_CAMERA_VIEWPORT ===")
    for L in range(N_LEVELS):
        g.set_level(L)
        gw, gh = g.current_level.grid_size or (64, 64)
        cam_w, cam_h = g.camera._width, g.camera._height
        ok = (cam_w == gw and cam_h == gh)
        print(f"  L{L+1}: grid={gw,gh} camera={cam_w,cam_h} {'OK' if ok else 'FAIL'}")
        if not ok:
            failures.append(("CHECK_CAMERA_VIEWPORT", L+1, f"grid={gw,gh} camera={cam_w,cam_h}"))

    # CHECK_SPRITE_CONTENT
    print("=== CHECK_SPRITE_CONTENT ===")
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = render_frame(g)
        distinct = set(np.unique(frame[frame != LETTER_BOX]).tolist())
        ok = len(distinct) >= 2
        print(f"  L{L+1}: distinct={sorted(distinct)} {'OK' if ok else 'FAIL'}")
        if not ok:
            failures.append(("CHECK_SPRITE_CONTENT", L+1, f"distinct={distinct}"))

    # CHECK_ACTION_BRANCHES
    print("=== CHECK_ACTION_BRANCHES ===")
    for action_id in declared:
        needle = f"GameAction.ACTION{action_id}"
        ok = needle in src_text
        print(f"  ACTION{action_id}: {'OK' if ok else 'FAIL'}")
        if not ok:
            failures.append(("CHECK_ACTION_BRANCHES", action_id, "needle missing"))

    # CHECK_ACTION_RUNTIME
    print("=== CHECK_ACTION_RUNTIME ===")
    for action_id in declared:
        try:
            g_fresh = GameClass()
            if action_id == 6:
                g_fresh.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 32, "y": 32}), raw=True)
            else:
                g_fresh.perform_action(ActionInput(id=GameAction.from_id(action_id), data={}), raw=True)
            print(f"  ACTION{action_id}: OK")
        except Exception as e:
            print(f"  ACTION{action_id}: FAIL {type(e).__name__}: {e}")
            failures.append(("CHECK_ACTION_RUNTIME", action_id, f"{type(e).__name__}: {e}"))

    # CHECK_PALETTE_RANGE
    print("=== CHECK_PALETTE_RANGE ===")
    for L in range(N_LEVELS):
        g.set_level(L)
        frame = render_frame(g)
        mn, mx = int(frame.min()), int(frame.max())
        ok = (mn >= 0 and mx <= 15)
        print(f"  L{L+1}: range=[{mn},{mx}] {'OK' if ok else 'FAIL'}")
        if not ok:
            failures.append(("CHECK_PALETTE_RANGE", L+1, f"range=[{mn},{mx}]"))

    # CHECK_WIN_PATH_EXISTS
    print("=== CHECK_WIN_PATH_EXISTS ===")
    has_next = "self.next_level()" in src_text
    has_win = "self.win()" in src_text
    ok = has_next or has_win
    print(f"  next_level={has_next} win={has_win} {'OK' if ok else 'FAIL'}")
    if not ok:
        failures.append(("CHECK_WIN_PATH_EXISTS", "all", "missing"))

    # CHECK_LOSE_PATH_EXISTS
    print("=== CHECK_LOSE_PATH_EXISTS ===")
    has_lose = "self.lose()" in src_text
    print(f"  lose={has_lose} {'OK' if has_lose else 'FAIL'}")
    if not has_lose:
        failures.append(("CHECK_LOSE_PATH_EXISTS", "all", "missing"))

    # CHECK_CAMERA_DEFAULT
    print("=== CHECK_CAMERA_DEFAULT ===")
    needs_resize = any(
        g._levels[i].grid_size != g._levels[0].grid_size
        for i in range(1, N_LEVELS)
    )
    if needs_resize:
        has_resize = "self.camera.width" in src_text and "self.camera.height" in src_text
        print(f"  needs={needs_resize} has_resize={has_resize} {'OK' if has_resize else 'FAIL'}")
        if not has_resize:
            failures.append(("CHECK_CAMERA_DEFAULT", "all", "missing"))
    else:
        print("  same grid_size across levels; check OK by vacuity")

    # CHECK_WITNESS_WINS
    print("=== CHECK_WITNESS_WINS ===")
    A = GameAction
    def click(x, y):
        return ActionInput(id=A.ACTION6, data={"x": x, "y": y})
    def act(n):
        return ActionInput(id=A.from_id(n), data={})

    WITNESSES = {
        1: [act(4), act(4), act(4), act(4), act(4)],
        2: [
            click(42, 14),  # select float at (40, 12)
            click(10, 38),  # place float at (8, 36), deselect
            act(4),         # walk onto float at (8, 36) -> teleport pending
            act(4),         # resolve -> at anchor (24, 16)
            act(4),         # (28, 16)
            act(4),         # (32, 16)
            act(4),         # (36, 16)
            act(4),         # (40, 16) goal
        ],
        3: [
            click(42, 14),  # select float at (40, 12)
            click(10, 38),  # place float at (8, 36), deselect
            act(4),         # walk onto float -> teleport pending
            act(4),         # resolve -> at anchor (24, 16)
            act(1),         # UP to (24, 12)
            click(10, 38),  # select float at (8, 36)
            click(38, 18),  # place float at (36, 16), deselect
            act(2),         # DOWN onto anchor (24, 16) -> teleport pending
            act(2),         # resolve -> at float (36, 16)
            act(4),         # RIGHT to (40, 16) goal
        ],
    }
    g.handle_reset()
    witness_ok = True
    for level_idx in range(1, N_LEVELS + 1):
        score_before = g._score
        if score_before != level_idx - 1:
            print(f"  L{level_idx}: pre-witness score={score_before} expected {level_idx-1} FAIL")
            failures.append(("CHECK_WITNESS_WINS", level_idx, f"pre score {score_before}"))
            witness_ok = False
            break
        for ai in WITNESSES[level_idx]:
            g.perform_action(ai)
        if level_idx < N_LEVELS:
            if g._score != level_idx:
                print(f"  L{level_idx}: witness did NOT advance; score={g._score} state={g._state.name} FAIL")
                failures.append(("CHECK_WITNESS_WINS", level_idx, f"score after={g._score} state={g._state.name}"))
                witness_ok = False
                break
            else:
                print(f"  L{level_idx}: advanced; score={g._score}")
        else:
            if g._state.name != "WIN":
                print(f"  L{level_idx}: did NOT reach WIN; state={g._state.name} score={g._score} FAIL")
                failures.append(("CHECK_WITNESS_WINS", level_idx, f"state={g._state.name}"))
                witness_ok = False
                break
            else:
                print(f"  L{level_idx}: reached WIN; state={g._state.name}")

    # Custom checks (defined in workspace/smoke-test-custom.py)
    print("=== CUSTOM CHECKS ===")
    custom_path = Path("runs/2026-05-10T12-58-03/workspace/smoke-test-custom.py")
    if custom_path.exists():
        custom_spec = importlib.util.spec_from_file_location("smoke_custom", custom_path)
        custom_mod = importlib.util.module_from_spec(custom_spec)
        custom_spec.loader.exec_module(custom_mod)
        for name in dir(custom_mod):
            if name.startswith("check_"):
                fn = getattr(custom_mod, name)
                try:
                    passed, observed = fn(GameClass)
                    status = "OK" if passed else "FAIL"
                    print(f"  {name}: {status} ({observed})")
                    if not passed:
                        failures.append(("CUSTOM", name, observed))
                except Exception as e:
                    print(f"  {name}: FAIL exception {type(e).__name__}: {e}")
                    failures.append(("CUSTOM", name, f"{type(e).__name__}: {e}"))
    else:
        print("  (no custom-check file)")

    print()
    if failures:
        print(f"FAILURES: {len(failures)}")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    else:
        print("ALL CHECKS PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
