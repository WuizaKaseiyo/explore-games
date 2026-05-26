# Step #05: write_spec (revision 1)

## Inputs Consumed
- mechanic-spec.md (rev 0, from #03)
- critique-revisions.md (round 1, from #04)
- All design-constraints + scaffold + novaengine-api in head.

## Deliverables Produced
- mechanic-spec.md (revision 1):
  - §3: cap_band → 1×1 sprite; target → palette 11 yellow;
    hazard → palette 13 maroon; flipper → bowtie pattern (no
    crossing diagonals).
  - §4 L2: target moved to (55, 32); wrong-path argument
    rewritten as post-discovery (ram-east-wall vs symmetric-decel
    decision); witness 13 actions.
  - §4 L3: layout redesigned — hazard wall full chamber height
    (y ∈ [8, 56]); wall column gap shrunk to 3 cells (y ∈
    [31, 33]) aligned with cap-band; cap_band placed as 3
    instances filling passage (28, 31..33); witness 10 actions
    re-derived; step budget bumped to 60.
  - §5: explicit per-axis slide rule (horizontal first, then
    vertical, each with full collision per cell-step).
  - §6: wake_pixel lifecycle paragraph added (remove at start
    of step, rebuild after slide).
  - §9: ek73, jd4q distinguishing rules added.

## Notes
- All 11 critique issues addressed.
- Witness arithmetic rechecked end-to-end.
- Geometry now passes counterfactual: cap covers full passage at
  L3; hazard column blocks vy detour; flipper is unique vx
  reversal path.
- Transition condition met. Returning to critique_spec for round 2.
