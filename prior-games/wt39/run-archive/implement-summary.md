# implement-summary — wt39

- Source: `prior-games/wt39/wt39.py` (337 lines)
- Metadata: `prior-games/wt39/metadata.json`

## Implemented rule (3-5 lines)

A single pawn glides cell-by-cell in the pressed cardinal direction
across a 14×14 tiled arena bordered by walls; the slide ends when
the pawn meets a wall, an angled-bumper deflector (which turns the
glide ninety degrees in flight per a fixed deflection rule), or a
brittle thaw-tile cracked by a previous slide. Thaw-tiles are
passable on first traversal; once a slide enters and exits one,
the engine swaps that cell's frozen sprite for a cracked sprite,
which then behaves as a wall for every subsequent slide. The level
advances when, after a slide settles, the pawn's grid position
equals the goal's; the level ends in loss when the per-level step
budget runs out.

## Runtime smoke test

- Instantiation: ✅
- L1 witness `[RIGHT, DOWN]`: ✅ advanced to L2.
- L2 witness `[RIGHT, LEFT, DOWN]`: ✅ advanced to L3.
- L3 witness `[RIGHT, LEFT, DOWN, UP]`: ✅ state = WIN (full game cleared).
