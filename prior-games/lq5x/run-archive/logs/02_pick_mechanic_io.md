# Step #02: pick_mechanic

## Inputs Consumed
- workspace/study-notes.md (from #01 study): cross-cut frequencies, design moves, anti-patterns, four open questions about action-set shape, board topology, second failure axis, and core dynamic.
- task-overview.md: autonomous run, no seed.
- prior-games/index.md: 4 prior rows for the novelty floor.
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check}.md: the positive + negative novelty tests.
- skills/design-constraints/{core-knowledge-priors,forbidden-elements,composition-and-tutorial,checklist}.md: prior categories, banned elements, 3-level + one-new-mechanic-per-level rule.
- skills/code/id-generation.md: 4-char ID rules + reserved list of 25 reference IDs.
- skills/global/action-enum.md: subset patterns; ACTION5 as the freedom slot for novelty.

## Deliverables Produced
- workspace/mechanic-pick.md: 4-char ID `lq5x`, family tag `lantern-cone-illuminate`, one-paragraph mechanic, taxonomy + prior-games similarity sweep with concrete distinguishing rules per near-miss, action set `[1,2,3,4,5]` justification, level progression sketch (L1 N=2 → L2 N+1=3 → L3 N+2=4) including the L3 order-matters argument.

## Notes
- Action-set choice: `[1,2,3,4,5]` (arrows + freedom verb, no click, no undo) — none of the four priors uses this shape, so action signature alone is a clean divergence axis.
- Closest taxonomy near-miss: `ls20` (cycler-attribute-match) — both feature an avatar walking a maze with an attribute that must be aligned to a target. Distinguishing rule articulated in mechanic-pick.md §6.
- Negative-similarity sweep walked through all 4 priors + 6 closest taxonomy entries; max overlap with any single one is 2 dimensions out of 8.
- The cone-rotate verb on ACTION5 is the load-bearing identity verb. Filter-cone-colour as L3's added mechanic is what enforces order-matters sequencing (commuting two adjacent filter visits changes cone-colour history and breaks the witness).
