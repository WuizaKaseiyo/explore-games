# implement-summary — pj7k

## Files emitted
- `prior-games/pj7k/pj7k.py` — 420 lines.
- `prior-games/pj7k/metadata.json`.

## Summary
A single coloured-faced cube avatar moves on a small cell grid via
arrow-key rolls, with each roll deterministically permuting which
of its six face-colours becomes top vs bottom; the colour that
ends up on the bottom after a roll is deposited as paint on the
landed cell. ACTION5 twists the cube in place, cycling the four
side faces. Some cells in the final level are gated by a colour
requirement that the cube can only enter if its bottom-after-roll
matches. The level is solved when each marked target cell shows
the paint colour matching the target's required colour.

## Verification performed
- AST parse: passed.
- Class instantiation via the venv's novaengine: succeeded; level
  count = 3; initial faces and cube position match the spec.
- Face permutation traces (twist, east) verified against §4 Level 2
  witness step 1-2 of `mechanic-spec.md`.
- `__pycache__` cleaned.
