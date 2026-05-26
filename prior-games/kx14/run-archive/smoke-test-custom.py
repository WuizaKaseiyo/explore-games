"""Custom smoke-test checks for kx14 (tide-tilt-buoyant)."""

import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load() -> type:
    src = Path("prior-games/kx14/kx14.py")
    spec = importlib.util.spec_from_file_location("smoke_kx14_for_custom", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "Kx14")


def check_raise_water_lifts_ball(GameClass) -> tuple[bool, str]:
    """ACTION1 raises the water surface and lifts the floating ball one cell up."""
    g = GameClass()
    g.set_level(0)
    b0 = g._balls[0]
    r0 = b0["row"]
    g.perform_action(ActionInput(id=GameAction.ACTION1, data={}), raw=True)
    r1 = g._balls[0]["row"]
    return r1 == r0 - 1, f"row before={r0} after={r1}"


def check_tilt_right_moves_ball_one_cell(GameClass) -> tuple[bool, str]:
    """ACTION4 tilts the floating ball exactly one cell rightward (when path clear)."""
    g = GameClass()
    g.set_level(0)
    b0 = g._balls[0]
    c0 = b0["col"]
    g.perform_action(ActionInput(id=GameAction.ACTION4, data={}), raw=True)
    c1 = g._balls[0]["col"]
    return c1 == c0 + 1, f"col before={c0} after={c1}"


def check_anchor_pins_ball_against_water(GameClass) -> tuple[bool, str]:
    """Anchored ball stays put when water level rises (level 3 has anchor enabled)."""
    g = GameClass()
    g.set_level(2)
    b0 = g._balls[0]
    c, r0 = b0["col"], b0["row"]
    # Click the ball to anchor it.
    cam = g.camera
    grid_size = g.current_level.grid_size
    gw, gh = grid_size
    scale = max(1, min(64 // gw, 64 // gh))
    ox = (64 - gw * scale) // 2
    oy = (64 - gh * scale) // 2
    cell_pixel = 5
    fx = c * cell_pixel + ox + 2
    fy = r0 * cell_pixel + oy + 2
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": fx, "y": fy}), raw=True
    )
    # Now raise water with ACTION1 — anchored ball should NOT move.
    g.perform_action(ActionInput(id=GameAction.ACTION1, data={}), raw=True)
    r1 = g._balls[0]["row"]
    return r1 == r0, f"row before-raise={r0} after-raise={r1} (anchored={g._balls[0]['anchored']})"


def main() -> int:
    GameClass = _load()
    checks = [
        check_raise_water_lifts_ball,
        check_tilt_right_moves_ball_one_cell,
        check_anchor_pins_ball_against_water,
    ]
    failures = []
    for fn in checks:
        passed, observed = fn(GameClass)
        verdict = "PASS" if passed else "FAIL"
        doc = (fn.__doc__ or "").strip().splitlines()[0]
        print(f"{verdict}: {fn.__name__} — {observed} :: {doc}")
        if not passed:
            failures.append((fn.__name__, observed, doc))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
