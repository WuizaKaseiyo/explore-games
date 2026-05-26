# Step #04: critique_spec (visit 1/10)

## Inputs Consumed
- states/critique_spec.md
- mechanic-spec.md (the spec under review)
- mechanic-pick.md
- skills/design-constraints/checklist.md (22 items)
- skills/design-constraints/composition-and-tutorial.md
- skills/design-constraints/difficulty-rules.md
- skills/design-constraints/forbidden-elements.md
- skills/mechanic-novelty/similarity-check.md
- skills/mechanic-novelty/negative-similarity-check.md
- prior-games/index.md plus unindexed prior-games (lz7q, vk6m, etc.) consulted earlier

## Deliverables Produced
- critique-revisions.md: 8 numbered issues with concrete fixes; consolidated mechanic to 4 mechanics across 3 levels (2/3/4 — each +1 promotion); revised filter (2↔3 swap) and pivot (+1 stride-bonus); re-walked negative-similarity check after revisions; explicit witness traces for L1 (2 actions), L2 (7 actions), L3 (7 actions). Verdict: TRANSITION BACK to write_spec for v2.

## Notes
- The spec v1 conflated two incompatible mechanic semantics: "wall-clamp slide" (intermediate cells matter) and "leap-over wall" (only destination matters). The leap-over interpretation is the one that makes M1's variable stride truly novel; the wall-clamp interpretation reduces M1 to a step-budget optimization that isn't strictly necessary.
- M5 as originally specified (rotate next press's direction) was not counterfactually necessary because rotated-direction is reachable by directly-pressing-the-rotated-direction. Replaced with stride-bonus +1 which expands reachable cells.
- The wall thicknesses across levels create a clean composition: L1 has 1-row wall (max stride 3 = 3-pip yellow leaps), L2 has 2-row wall (requires filter to make 2-pip a stride-3), L3 has 3-row wall (requires filter AND pivot for stride-4).
- This is critique iteration 1; budget allows up to 10. Returning to write_spec for v2.
