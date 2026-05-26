# Step #07: write_spec (revision 2)

## Inputs Consumed
- mechanic-spec.md (rev 1, from #05)
- critique-revisions.md (round 2, from #06)

## Deliverables Produced
- mechanic-spec.md (revision 2): L3 layout redesigned as 1-cell-
  tall horizontal corridor at y=32 with walls filling all other
  interior cells. Witness unchanged (10 actions). M2 and M3
  necessity paragraphs updated.

## Notes
- Single targeted change: L3 layout. Witness arithmetic untouched.
- Now no vy-bypass possible: corridor's vertical extent = 1 cell;
  any vy impulse hits ceiling/floor wall and zeroes.
- Cap and flipper remain unique chokepoints; hazard cells block
  flipper-skip.
- Returning to critique_spec for round 3 — should pass.
