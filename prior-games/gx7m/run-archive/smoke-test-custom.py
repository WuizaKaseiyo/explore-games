"""Custom mechanic checks for gx7m. Each check returns (passed, observed_str)."""

import importlib.util
import sys
from pathlib import Path

from novaengine import ActionInput, GameAction

_src = Path("prior-games/gx7m/gx7m.py")
_spec = importlib.util.spec_from_file_location("smoke_gx7m", _src)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
GameClass = getattr(_mod, "Gx7m")


def check_disc_click_rotates_90_cw():
    """A click on a disc's hub rotates that disc by 90° CW from its starting rotation."""
    g = GameClass()
    g.set_level(0)
    pink = g.disc_list[0]
    r0 = pink.rotation
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 20, "y": 31}), raw=True)
    r1 = pink.rotation
    return r1 == (r0 + 90) % 360, f"r0={r0} r1={r1}"


def check_cascade_flips_sign_at_neighbor():
    """A click on a disc with a mesh-neighbour rotates the neighbour in the opposite direction."""
    g = GameClass()
    g.set_level(0)
    pink, lblue = g.disc_list[0], g.disc_list[1]
    r_pink_0 = pink.rotation
    r_lblue_0 = lblue.rotation
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 20, "y": 31}), raw=True)
    pink_delta = (pink.rotation - r_pink_0) % 360
    lblue_delta = (lblue.rotation - r_lblue_0) % 360
    return pink_delta == 90 and lblue_delta == 270, (
        f"pink_delta={pink_delta} lblue_delta={lblue_delta}"
    )


def check_ratchet_hub_click_is_noop_when_blocked():
    """Clicking the ratchet's hub while its direction state is BLOCKED leaves all rotations unchanged."""
    g = GameClass()
    g.set_level(1)
    rotations_before = [d.rotation for d in g.disc_list]
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 30, "y": 31}), raw=True)
    rotations_after = [d.rotation for d in g.disc_list]
    return rotations_before == rotations_after, (
        f"before={rotations_before} after={rotations_after}"
    )


def check_clutch_disengage_isolates_subgraph():
    """Disengaging the clutch removes its mesh-edges; clicking a neighbour of the clutch no longer rotates discs on the other side of it."""
    g = GameClass()
    g.set_level(2)
    # Disengage the clutch via its above-the-collar bolt at column 40,
    # rows 22..26. Click any cell in that column (centre = (40, 24)).
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 40, "y": 24}), raw=True)
    # Click lblue-hub. Without disengage, lblue cascade would propagate through clutch_green to orange.
    orange = g.disc_list[4]  # disc_orange is rightmost
    r_orange_before = orange.rotation
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": 30, "y": 31}), raw=True)
    r_orange_after = orange.rotation
    return r_orange_before == r_orange_after, (
        f"orange_before={r_orange_before} orange_after={r_orange_after}"
    )


CHECKS = [
    check_disc_click_rotates_90_cw,
    check_cascade_flips_sign_at_neighbor,
    check_ratchet_hub_click_is_noop_when_blocked,
    check_clutch_disengage_isolates_subgraph,
]


if __name__ == "__main__":
    for fn in CHECKS:
        ok, observed = fn()
        marker = "PASS" if ok else "FAIL"
        print(f"{marker}  {fn.__name__}  — {observed}")
