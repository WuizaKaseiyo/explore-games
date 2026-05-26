# implement-summary.md

## Files written
- `prior-games/zw91/zw91.py` — 594 lines.
- `prior-games/zw91/metadata.json`.

## Plain-English rule (no level coordinates)
The player controls one square avatar that moves one tile per arrow press. ACTION5 cycles the avatar through three sizes — small, medium, large — and from large into a one-shot loaded "overloaded" state visible as a halo, then fires a single burst that destroys nearby push-blocks and cracked-pattern walls. Growing the avatar pushes any push-blocks in the new footprint outward (radial direction); blocks roll until they hit a wall or a cracked-pattern wall. The level is won when the avatar's body fits a same-shape socket-ring at matching size.

## Verification
- `ast.parse` succeeded (parses as valid Python).
- Instantiation succeeded; level count = 3.
- All three levels' witnesses replay end-to-end and reach state WIN (verified during implement).
- One geometric / push-rule discovery during implementation: the witness's burst-firing position was moved from tile (7, 6) to tile (6, 6) and `BURST_RADIUS` widened from 8 to 12 cells (3 tiles) so all three shove-blocks push east cleanly during the size 2→3 cycle. Spec patched accordingly; counterfactual still holds (M3 fires inside the 2→3 cycle at tile (6, 6) because all three blocks lie inside the new footprint).
