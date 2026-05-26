"""Witness smoke-test runner for gg26."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from novaengine import ActionInput, GameAction


GAME_ID = "gg26"
ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "prior-games" / GAME_ID / f"{GAME_ID}.py"
CLASS_NAME = f"Gg{int(GAME_ID[2:]):02d}"


def action(aid: int | GameAction, data: dict | None = None) -> ActionInput:
    enum = aid if isinstance(aid, GameAction) else GameAction.from_id(aid)
    return ActionInput(id=enum, data=data or {})


def click(x: int, y: int) -> ActionInput:
    return action(GameAction.ACTION6, {"x": int(x), "y": int(y)})


def grid_click(g, x: int, y: int) -> ActionInput:
    cam_w = getattr(g.camera, "_width", 64)
    cam_h = getattr(g.camera, "_height", 64)
    scale = max(1, min(64 // cam_w, 64 // cam_h))
    ox = (64 - cam_w * scale) // 2
    oy = (64 - cam_h * scale) // 2
    return click(ox + x * scale + scale // 2, oy + y * scale + scale // 2)


def cell_click(g, cell: tuple[int, int]) -> ActionInput:
    ox = getattr(g, "OX", 0)
    oy = getattr(g, "OY", 0)
    cell_px = getattr(g, "CELL", 4)
    return grid_click(g, ox + cell[0] * cell_px + cell_px // 2, oy + cell[1] * cell_px + cell_px // 2)


def load_game():
    spec = importlib.util.spec_from_file_location(f"smoke_{GAME_ID}", SRC)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return getattr(mod, CLASS_NAME)


def witness_actions(g):
    level = getattr(g, "level_index", 0)
    fences_by_level = [
        [(3, 6), (7, 4), (8, 3), (13, 5), (14, 6)],
        [(3, 5), (4, 4), (6, 7), (10, 3), (11, 2), (13, 5), (14, 4), (15, 3)],
        [(5, 11), (6, 10), (8, 4), (11, 12), (13, 8), (13, 10), (14, 7), (15, 6)],
    ]
    actions = [cell_click(g, cell) for cell in fences_by_level[level]]
    actions.extend(cell_click(g, (0, 0)) for _ in range(5))
    return actions


def level_solved(g, level_index: int, n_levels: int) -> bool:
    if level_index < n_levels - 1:
        return getattr(g, "level_index", None) == level_index + 1
    return getattr(g, "_state", None).name == "WIN"


def replay_level(GameClass, level_index: int) -> tuple[bool, str]:
    g = GameClass()
    g.set_level(level_index)
    try:
        for ai in witness_actions(g):
            g.perform_action(ai, raw=True)
            if getattr(g, "_state", None).name == "GAME_OVER":
                return False, "entered GAME_OVER during witness"
        if level_solved(g, level_index, len(g._levels)):
            return True, "ok"
        return False, (
            f"did not solve: state={g._state.name} score={g._score} "
            f"enclosed={getattr(g, 'current_enclosed', None)} "
            f"area={getattr(g, 'current_area', None)} "
            f"min_area={getattr(g, 'min_area', None)} "
            f"fences={sorted(getattr(g, 'fences', []))}"
        )
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def main() -> int:
    GameClass = load_game()
    failures = []
    print(f"# witness smoke tests - {GAME_ID}")
    for level_idx in range(len(GameClass()._levels)):
        ok, msg = replay_level(GameClass, level_idx)
        status = "PASS" if ok else "FAIL"
        print(f"{GAME_ID} L{level_idx + 1}: {status} - {msg}")
        if not ok:
            failures.append((level_idx + 1, msg))
    print(f"\n# failures: {len(failures)}")
    for level, msg in failures:
        print(f"- {GAME_ID} L{level}: {msg}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
