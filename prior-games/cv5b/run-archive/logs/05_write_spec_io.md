# Step #05: write_spec (revision pass 1)

## Inputs Consumed
- workspace/critique-revisions.md (5 issues from #04 critique_spec)
- workspace/mechanic-spec.md (prior version)

## Deliverables Produced
- workspace/mechanic-spec.md (updated):
  - §3 sprite roster: target_ring redefined as 3×3 with explicit
    centre semantics (Issue 4).
  - §4 Power table inserted with revised values; power-3 range 36
    (was 32), apex 15. (Issue 2)
  - §4 L1 demoted to single-mechanic tutorial (arc-fire only;
    target at (16, 50) distance 12, fire-only witness 1 action).
    (Issue 1)
  - §4 L2 mechanic count revised to 3 (+walk +power-cycle from L1).
    Targets at (28, 50) and (50, 50). Witness 14 actions. Step
    budget 30. (Issue 3)
  - §4 L3 mechanic count revised to 5 (+shield-blocks-arc
    +wind-deflects-arc from L2). Target at (50, 50). Witness 31
    actions. Step budget 50. Power-3 range adjusted gives valid
    geometry. (Issue 2, Issue 3)
  - §4 L1 random-resistance bullet acknowledges tutorial exception
    (per from-tech-report.md §3.4). (Issue 5)

## Notes
- Mechanic counts: L1=1, L2=3 (+2), L3=5 (+2). Both increments are +2;
  both within the +1 or +2 rule in checklist item 11.
- Counterfactual table now consistent with witnesses: each witness
  exercises every mechanic in its level's mechanic list, AND no
  alternate winning path within step_budget skips any.
