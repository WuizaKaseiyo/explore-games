# Step #05: write_spec (round 2 — revising after critique #04)

## Inputs Consumed
- workspace/critique-revisions.md (#04 deliverable, 5 issues)
- workspace/mechanic-spec.md (round 1 spec, modified in place)
- skills/code/spec-template.md (re-checked structure)

## Deliverables Produced
- workspace/mechanic-spec.md (revised in place)
  - §4 L2 wall-block necessity: rewritten to name (8, 4) as the cell that blocks cyan's tick-2 step, with concrete trace of what happens without walls (cyan reaches (8, 12) on tick 11). Addresses critique issue 1.
  - §4 L2 orth-major necessity: rewritten with the Manh-rule counterfactual (cyan stuck at (8, 3) forever; L2 unwinnable). Addresses issue 2.
  - §4 L3 phase-pursuer necessity: rewritten to name corridor cell (9, 9) as the unique walkable connection between bait region and corridor merge region; wall geometry (y=8 row + x=4 col) forces traversal. Addresses issue 4.
  - §4 L3 tick-skip necessity: rewritten with structural counterfactual referencing T_bait, B, C_RY, C_CG; argues both red-yellow and cyan trajectories pin the avatar to B on T_bait+1, so ACTION5 is the only move. Addresses issue 3.
  - §4 L3 step-budget justification: rewritten to use absolute-slack measure (76 spare actions) rather than ratio. Addresses issue 5.

## Notes
- §4 sections are the only changes. §1-3 and §5-9 unchanged.
- Witnesses (action sequences) unchanged in form, but the mechanic-necessity reasoning around them is now structural rather than arithmetic.
- Transition: critique_spec round 2.
