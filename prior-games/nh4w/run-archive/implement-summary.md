# implement-summary

## Files written
- `prior-games/nh4w/nh4w.py` (441 lines)
- `prior-games/nh4w/metadata.json`

## Verification
- Syntax-check: `python -c "import ast; ast.parse(open(... 'nh4w.py').read())"` PASS.
- Runtime instantiation: `Nh4w()` constructed; 3 levels, available_actions=[3, 4, 6], grid_size=(64,64) for each.
- Sprites per level confirmed: L1 = floor + launcher + target_yellow; L2 adds wall_h8; L3 adds wall_h8 + ceiling_c6 + ceiling_c14 + target_blue.

## Implementation summary (no spec coordinates)
A floor-bound launcher pawn walks left/right with arrow inputs. Clicking any cell fires a small projectile in a discrete parabolic arc whose peak height grows with horizontal distance. Brick walls block low arcs (peak too short to clear), and tapered hanging stalactites block high arcs (peak too tall to fit under). Each level wins when every coloured target on the floor has been hit.

## Spec → implementation deltas
- Spec L3 used ceiling clearances (5, 13). Implementation uses (6, 14) so that the bbox-collision rule "alt < clearance clears" gives the same witness outcome (yellow only fires from one walking position; blue only from a different walking position; "fire both shots from the same position" still fails). Witness sequence and step count unchanged.
- All other geometry, mechanics, and witness sequences match the round-2 spec exactly.
