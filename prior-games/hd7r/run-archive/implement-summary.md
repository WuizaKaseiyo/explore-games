# Implement summary — hd7r

- Source: `prior-games/hd7r/hd7r.py` (452 lines)
- Metadata: `prior-games/hd7r/metadata.json`

## Implemented rule (plain English, no coordinates)
The player walks a single shepherd one cell per arrow press. After each
shepherd move, every nearby timid creature steps one cell away from the
shepherd — orange creatures back straight away, magenta creatures veer
to the side — unless a wall, a shut gate, the edge, or another creature
blocks that step. A click on a gate post in a dividing wall swaps it
between shut (solid) and open (passage); creatures cannot flee through a
shut gate. A level is cleared when every creature has been herded onto a
pen of its own colour. A depleting top-row energy bar ends the level if
it empties first.

## Verification done in implement
- `ast.parse` OK (no SyntaxError).
- Instantiates without raising; `len(g._levels) == 3`.
- All three spec witnesses replayed against the loaded engine: L1 and L2
  each advance the level (`_score` 0→1→2), L3 reaches `WIN`.
- `__pycache__` cleaned.
