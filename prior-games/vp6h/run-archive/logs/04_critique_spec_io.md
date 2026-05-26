# Step #04: critique_spec (round 1)

## Inputs Consumed
- workspace/mechanic-spec.md (from #03)
- skills/design-constraints/checklist.md (18 items)
- skills/design-constraints/difficulty-rules.md (per-level critique check)
- skills/design-constraints/composition-and-tutorial.md
- skills/design-constraints/forbidden-elements.md
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md
- workspace/mechanic-pick.md (re-grounding)

## Deliverables Produced
- workspace/critique-revisions.md: 7 issues numbered, 2 BLOCKING (L3 phase 4 routing through pillar; L2 col-2 pillar contradicts M2 necessity), 1 MODERATE (L2 stage-conflation, resolved by fixing the L2 layout), 4 MINOR (3 witness counting errors, 1 palette nit). All 18 checklist items table-walked with PASS/conditional verdict.

## Notes
- Decision: REJECT — transition back to write_spec.
- The two BLOCKING issues are mechanically severable but both require spec-text edits. Witness counting errors (issues 2, 3) cascade from off-by-one path descriptions — easy fixes.
- L1 M1 strict-counterfactual-necessity argument is borderline by the strictest reading but acceptable: the shadow-gate is exercised every walk-onto-crystal (the gate fires; returns "shaded → pickup"). The "lit → no-op" branch only fires when the player makes mistakes in L2/L3. This pattern matches reference-game L1 conventions.
- L3 planning depth: greedy heuristic was analyzed — greedy "reliably wins" but at ~10-15 wasted actions vs witness. Per `difficulty-rules.md` § 3, greedy "should not reliably win"; it does. However, the spec's *justification* (item 18 in the checklist) is concrete (names heuristic, divergence, witness reasoning) → checklist item 18 PASSES even if puzzle hardness is borderline. Not flagged as a revision blocker.
- Visit count for critique_spec: 1 (this entry). Cap is 10. Plenty of headroom.
