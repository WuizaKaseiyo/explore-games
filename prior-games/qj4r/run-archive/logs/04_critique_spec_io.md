# Step #04: critique_spec (round 1)

## Inputs Consumed
- workspace/mechanic-spec.md (from #03)
- skills/design-constraints/checklist.md (re-read items 1-21; load-bearing items 11, 12, 18)
- skills/design-constraints/composition-and-tutorial.md
- skills/design-constraints/difficulty-rules.md
- skills/mechanic-novelty/{similarity-check,negative-similarity-check}.md

## Deliverables Produced
- workspace/critique-revisions.md: 6 numbered issues with quoted offending sections + concrete fixes; recommendation to swap L2 mechanic from "obstacle" to "merge" and defer obstacle to L3 where M2 can be made unambiguously necessary.

## Notes
- Critique is round 1 of 10. Looping back to write_spec with the recommended restructure.
- The fold geometry is clean enough to support the simpler progression (L1=fold, L2=merge, L3=obstacle); the original spec's mixing of obstacles at L2 produced unverified geometry.
- Item 11 (mechanic inheritance / +1-or-+2 per level): structurally OK in the original spec (L1=1 mechanic, L2=2 mechanics, L3=3 mechanics — all +1 transitions).
- Item 12 (counterfactual necessity): primary failure was at L2 obstacle; restructure should make M3 (merge) necessary at L2 via piece-count predicate and M2 (obstacle) necessary at L3 via cell-blocking-of-the-only-witness-path.
