# Implement summary — pz4t

- Source: `prior-games/pz4t/pz4t.py`
- Metadata: `prior-games/pz4t/metadata.json`

## Implemented rule

The board has dark-grey **target shadows** marking where each
coloured **component** must be placed. The player clicks anywhere
on a component to pick it up — the clicked pixel becomes the
**anchor**. Clicking a board cell while holding a component
places it such that the anchor pixel lands on the clicked cell
(`sprite.position = click − anchor`). ACTION5 rotates the held
component 90° clockwise (anchor follows the rotation); ACTION7
flips it horizontally (anchor mirrors). The level wins when every
component's pixels exactly cover its matching colour's target
shadows; the only failure mode is exhausting the per-level step
counter.

## Verification

- AST parse: clean.
- `Pz4t()` instantiates; level count = 3; cameras resize per-level.
- Full witness across all 3 levels (4 + 7 + 10 actions) drives
  `GameState.WIN`.
- L2's red component is initially vertical 1×3 but the red target
  is horizontal — rotation strictly required to fit.
- L3's red component is a Z-tetromino but the red target is an
  S-shape — flip strictly required (no rotation of Z produces S).
