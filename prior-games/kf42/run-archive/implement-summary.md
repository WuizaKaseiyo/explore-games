# implement-summary — Run #01 (`kf42`)

## Files written
- `prior-games/kf42/kf42.py` — 407 lines.
- `prior-games/kf42/metadata.json` — schema-compliant.

## Verification
- `ast.parse` of `kf42.py`: PASS (no SyntaxError).
- Runtime smoke test (instantiation + level-0 attribute reads + 3
  simulated actions): PASS. Click correctly selects a pawn,
  arrow-keys advance the active pawn, the tether constraint is
  observable in pawn position changes.
- `__pycache__` cleaned.

## Plain-English summary of the implemented rule
The player controls one of two coloured pawns by clicking; arrows
step the selected pawn one cell. The two pawns are joined by a
distance constraint, so when one is moved far enough, the other is
dragged a single cell toward it. Pads on the floor change a pawn's
colour the moment it walks onto one. The level ends when both
pawns simultaneously occupy a target whose colour matches their
current body colour.
