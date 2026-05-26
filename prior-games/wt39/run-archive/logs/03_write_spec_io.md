# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02 pick_mechanic): family `glide-deflect-thaw`, ID `wt39`.
- skills/code/spec-template.md (from #01 study): 9-section structure.
- skills/design-constraints/{composition-and-tutorial.md, difficulty-rules.md, checklist.md} (from #01 study).
- skills/code/{universal-scaffold.md, novaengine-api.md} (from #01 study).

## Deliverables Produced
- mechanic-spec.md: full 9-section spec. L1 = base slide (witness 2 actions); L2 = +bumper (witness 3 actions); L3 = +thaw (witness 4 actions). Per-mechanic counterfactual necessity articulated. Greedy-fails heuristic: largest-displacement greedy oscillates UP/DOWN in col 2 because col 2 has no walls between rows 1 and 12. Witness commute test: swap actions 2 and 3 of L3 (LEFT and DOWN) — DOWN at (10, 6) is wall-blocked, breaks solution.

## Notes
- Grid 14×14 across all 3 levels with perimeter walls and identical pawn start (2, 2). Reusing geometry simplifies sprite reuse.
- Goal is non-sticky: pawn must STOP on goal cell to win. This is what allows L3's thaw mechanic to be counterfactually necessary — without it, no slide-stop would terminate at (4, 9).
- Action set [1, 2, 3, 4] is unusual (only ls20 and tu93 in the 25 reference set use this). Deliberately minimal to keep the verb palette tight.
- Step budgets: 30/60/80 — generous and increasing per difficulty-rules.md §2.d L3 addendum.
- L3 trace verified by hand. Thaw-cracking timing: thaw mutates AT END of the slide that passes through it.
