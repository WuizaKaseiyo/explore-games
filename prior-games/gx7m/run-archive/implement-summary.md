# Implement summary — gx7m

## Files

- `prior-games/gx7m/gx7m.py` — 463 lines.
- `prior-games/gx7m/metadata.json`.

## Implementation summary

The game stores per-disc rotation, per-ratchet direction state, and
per-clutch engagement state. Each `ACTION6` click is dispatched by
the sprite-tag at the click cell: tang sprites cycle their owner's
direction or engagement; disc sprites trigger a BFS-cascade through
the live mesh-graph (clutch state determines which edges are live).
The cascade flips sign at every hop and gates rotation at ratchet
discs by direction. Win predicate compares each disc's `rotation`
to its target; the engine auto-fires `win()` after the last level.

## Validation

- Syntax: `ast.parse` OK.
- Instantiation: `Gx7m()` instantiates without exception.
- L1 witness (2 actions): rotations advance through `[90, 270, 90]`
  to targets `[180, 180, 180]`, win fires, advances to L2.
- L2 witness (5 actions): tang → CW, R-hub fires the asymmetric
  cascade, three pink-hub clicks bring pink up to 180° while the
  ratchet blocks back-cascade. Targets `[180, 90, 270]` met, advances
  to L3.
- L3 witness (11 actions): clutch disengage isolates `{green}` and
  `{orange}` from `{pink, magenta, lblue}`; green-hub + two orange-hub
  clicks set those two sub-components; magenta-tang, magenta-hub,
  three pink-hub, two lblue-hub clicks resolve the remaining sub-
  component. Final rotations `[180, 90, 90, 90, 180]` match targets,
  game state transitions to `GameState.WIN`.
