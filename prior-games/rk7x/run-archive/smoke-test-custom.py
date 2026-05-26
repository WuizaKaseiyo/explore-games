"""Custom smoke checks for `rk7x` (live-switch-routing)."""

from __future__ import annotations
import importlib.util, sys
from pathlib import Path

SRC = Path("prior-games/rk7x/rk7x.py")
spec = importlib.util.spec_from_file_location("smoke_rk7x", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = getattr(mod, "Rk7x")

from novaengine import ActionInput, GameAction, InteractionMode  # noqa: E402


def check_off_board_click_ticks_courier() -> tuple[bool, str]:
    """Clicking outside the playfield (letter-box) ticks the courier without
    toggling any switch — the implicit 'wait' verb of live-switch-routing."""
    g = GameClass()
    g.set_level(0)
    courier = list(g._directions.keys())[0]
    x0, y0 = courier.x, courier.y
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 0, "y": 0}), raw=True
    )
    moved = (courier.x, courier.y) != (x0, y0)
    return moved, f"before=({x0},{y0}) after=({courier.x},{courier.y})"


def check_clicking_switch_toggles_blade() -> tuple[bool, str]:
    """Clicking on a switch sprite swaps which twin (H/V) is currently
    TANGIBLE — the toggle verb."""
    g = GameClass()
    g.set_level(0)
    junctions_h = g.current_level.get_sprites_by_tag("junction_h")
    junction_h = junctions_h[0]
    initial_state = junction_h.interaction
    cx, cy = junction_h.x + 1, junction_h.y + 1  # click inside the 4x4 sprite
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": cx, "y": cy}), raw=True
    )
    final_state = junction_h.interaction
    flipped = initial_state != final_state
    return flipped, f"before={initial_state.name} after={final_state.name}"


def check_l1_minimal_solve_wins() -> tuple[bool, str]:
    """The L1 spec witness (one toggle + 13 ticks) advances the level."""
    g = GameClass()
    g.set_level(0)
    # Toggle the only junction at logical cell (8, 7) → grid (32, 28),
    # click in middle of sprite at (33, 29).
    g.perform_action(
        ActionInput(id=GameAction.ACTION6, data={"x": 33, "y": 29}), raw=True
    )
    for _ in range(13):
        g.perform_action(
            ActionInput(id=GameAction.ACTION6, data={"x": 0, "y": 0}), raw=True
        )
    advanced = g._current_level_index == 1
    return advanced, f"current_level_index={g._current_level_index}"


def check_lose_when_courier_hits_wall() -> tuple[bool, str]:
    """If the player never toggles the L1 junction, the courier walks into
    the wall above the junction and the game loses."""
    g = GameClass()
    g.set_level(0)
    # Click off-board for many ticks, never on the junction.
    for _ in range(15):
        if g._state.name in ("GAME_OVER", "WIN"):
            break
        g.perform_action(
            ActionInput(id=GameAction.ACTION6, data={"x": 0, "y": 0}), raw=True
        )
    return g._state.name == "GAME_OVER", f"state={g._state.name}"


CUSTOM_CHECKS = [
    check_off_board_click_ticks_courier,
    check_clicking_switch_toggles_blade,
    check_l1_minimal_solve_wins,
    check_lose_when_courier_hits_wall,
]


if __name__ == "__main__":
    for fn in CUSTOM_CHECKS:
        passed, observed = fn()
        status = "PASS" if passed else "FAIL"
        print(f"{status}  {fn.__name__}  ({observed})")
