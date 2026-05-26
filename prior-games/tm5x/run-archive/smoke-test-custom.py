"""Custom smoke checks for tm5x.

Each check returns (bool_passed, observed_str). The smoke runner
imports this and calls each function; any False result becomes a row
in workspace/smoke-test-failures.md under "## Custom checks".

Constraints (per code/smoke-test-checks.md):
- ≤ 5 setup actions before the action under test.
- One boolean assertion.
- Tests an essential mechanic invariant.
"""

from novaengine import ActionInput, GameAction, InteractionMode


def check_down_moves_pawn(GameClass) -> tuple[bool, str]:
    """ACTION2 (DOWN) moves the active pawn one thermal cell (4 px).

    Tests Pattern A — direction press moves the avatar.
    """
    g = GameClass()
    g.set_level(0)
    pawn = g._active_pawn()
    y0 = pawn.y
    g.perform_action(ActionInput(id=GameAction.ACTION2), raw=True)
    pawn = g._active_pawn()
    return pawn.y == y0 + 4, f"y0={y0} y1={pawn.y}"


def check_action5_toggles_polarity(GameClass) -> tuple[bool, str]:
    """ACTION5 toggles pawn polarity from hot (+1) to cold (-1).

    Tests Pattern C — modal action toggles a state flag.
    """
    g = GameClass()
    g.set_level(0)
    p0 = g._polarity
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    return g._polarity == -p0, f"before={p0} after={g._polarity}"


def check_action5_swaps_pawn_variant(GameClass) -> tuple[bool, str]:
    """After ACTION5, the cold pawn variant becomes TANGIBLE.

    Tests the two-sprite-swap idiom: the spec promises that the pawn
    sprite SEEN by the player swaps from pawn_hot to pawn_cold on
    ACTION5, surfacing polarity as a persistent visual cue (no hidden
    state per checklist item 19). This check asserts the active
    variant has flipped.
    """
    g = GameClass()
    g.set_level(0)
    g.perform_action(ActionInput(id=GameAction.ACTION5), raw=True)
    cold = g.current_level.get_sprites_by_name("pawn_cold")[0]
    return (
        cold.interaction == InteractionMode.TANGIBLE,
        f"pawn_cold.interaction={cold.interaction.name}",
    )


def check_imprint_at_pawn_cell(GameClass) -> tuple[bool, str]:
    """The pawn's thermal cell holds the polarity-driven imprint
    value (+2 when hot, -2 when cold). Tests the core aura-imprint
    rule: the field is a function of pawn position + polarity.
    """
    g = GameClass()
    g.set_level(0)
    # Pawn at thermal (8, 8), hot polarity → cell (8,8) should be +2.
    return (
        int(g._temperature[8, 8]) == 2,
        f"_temperature[8,8]={int(g._temperature[8, 8])} (expected +2)",
    )
