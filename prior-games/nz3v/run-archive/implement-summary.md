# implement-summary — nz3v

## Files written
- `prior-games/nz3v/nz3v.py` (415 lines)
- `prior-games/nz3v/metadata.json`

## Implementation summary

The game class `Nz3v` implements a 12×12-cell environment where a
central rotor pillar sweeps a quadrant of the playfield clockwise
(or counter-clockwise after a one-shot switch trigger) one
quadrant per K=6 actions; the player avatar walks the playfield
with the four arrow actions and dies if its destination cell is
not in the currently-lit quadrant. Stop-tile sprites freeze the
rotation count for K'=4 additional actions when stepped on
(visible cue: wedge tint shifts palette 11 → palette 7); the
counter-rotation switch (L3 only) reverses the rotor's direction
of advance for the rest of the level. Three HUD widgets — the
WedgeOverlay (4-corner-dot pattern in lit cells), the
RotorDirectionMarker (single magenta pixel showing where the
rotor will advance to next), and the StepCounterHud — surface
all internal state so no game state is hidden from the player.

## Verifications

- Syntax: `ast.parse` succeeds.
- Instantiation: `Nz3v()` constructs with 3 levels and
  `_available_actions = [1, 2, 3, 4]`.
- L1 witness (18 actions, target at (10, 10)): WIN.
- L2 witness (15 actions, target at (10, 1)): WIN.
- L3 witness (15 actions, target at (1, 10)): GameState.WIN reported.
- Dark-cell death: stepping into NW cell while wedge=NE triggers GAME_OVER.
- Step-budget exhaustion: walking 5 ACTION4 from (1, 1) crosses NW→NE boundary at action 5 with wedge still NW → dark cell → GAME_OVER (validates the lose path).
