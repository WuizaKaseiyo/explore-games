"""Custom smoke tests for gv47.

Each check follows the template:
  - <=5 setup actions, ONE action under test, ONE boolean assertion.
"""
import importlib.util
from pathlib import Path

from novaengine import ActionInput, GameAction


def _load_class():
    src = Path("prior-games/gv47/gv47.py")
    spec = importlib.util.spec_from_file_location("smoke_gv47", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Gv47


def _click(x: int, y: int) -> ActionInput:
    return ActionInput(id=GameAction.ACTION6, data={"x": int(x), "y": int(y)})


def check_click_seed_grows_region(GameClass) -> tuple[bool, str]:
    """Clicking inside a seed's bbox increases its region by >= 1 cell."""
    g = GameClass()
    g.set_level(0)
    rid = next(iter(g.regions.keys()))
    n0 = len(g.regions[rid])
    # seed is at grid (1,1) → 3x3 covers (1..3, 1..3); center grid (2,2);
    # camera scale 5, offset 2 → pixel (14, 14).
    g.perform_action(_click(14, 14), raw=True)
    n1 = sum(len(v) for v in g.regions.values())
    return n1 > n0, f"before={n0} after={n1}"


def check_action5_mixes_when_in_contact(GameClass) -> tuple[bool, str]:
    """ACTION5 fuses two adjacent different-coloured regions into one."""
    g = GameClass()
    g.set_level(1)  # L2 has yellow + blue + a (yellow,blue)->green table
    # 4 yellow grows + 4 blue grows so the regions touch
    for _ in range(4):
        g.perform_action(_click(14, 14), raw=True)   # yellow seed
    for _ in range(4):
        g.perform_action(_click(14, 49), raw=True)   # blue seed
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    n_regions = len(g.regions)
    return n_regions == 1, f"regions_after_mix={n_regions}"


def check_wind_extends_growth(GameClass) -> tuple[bool, str]:
    """L3 wind east makes one grow click expand the region by more than the
    L2 (no-wind) ring would on the same starting seed shape."""
    g = GameClass()
    g.set_level(2)
    rid = "r0"   # yellow seed inserted first at L3 setup
    n0 = len(g.regions[rid])
    g.perform_action(_click(14, 14), raw=True)
    n1 = len(g.regions[rid])
    return n1 > 21, f"before={n0} after={n1} (expected >21 with wind east)"


def check_lose_when_budget_exhausted(GameClass) -> tuple[bool, str]:
    """L1 with a stream of misses (clicks at empty corner) drains the step
    counter to 0 and triggers self.lose()."""
    g = GameClass()
    g.set_level(0)
    budget = g.max_steps
    miss_pixel = (62, 62)  # bottom-right pixel; outside any seed bbox
    for _ in range(budget + 1):
        g.perform_action(_click(*miss_pixel), raw=True)
    return g._state.name == "GAME_OVER", f"state={g._state.name}, steps_remaining={g.steps_remaining}"


CHECKS = [
    check_click_seed_grows_region,
    check_action5_mixes_when_in_contact,
    check_wind_extends_growth,
    check_lose_when_budget_exhausted,
]


if __name__ == "__main__":
    GameClass = _load_class()
    for fn in CHECKS:
        ok, note = fn(GameClass)
        marker = "PASS" if ok else "FAIL"
        print(f"{marker} {fn.__name__}: {note}")
