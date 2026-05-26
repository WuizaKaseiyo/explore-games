# Step #04: critique_spec (round 1)

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec).
- skills/design-constraints/checklist.md (16 + items 19-21 supplemental).
- skills/design-constraints/forbidden-elements.md.
- skills/design-constraints/composition-and-tutorial.md.
- skills/design-constraints/difficulty-rules.md.
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md.
- 25 mechanism-details summaries (re-checked mr5q, m0r0, lp85, vc33, tr87 against L3).
- prior-games/index.md.

## Deliverables Produced
- critique-revisions.md: 4 issues — (1) `available_actions` is global not per-level (fix via `_get_valid_actions`); (2) scan-line carets read as arrows (fix to bookend squares); (3) witnesses not shortest (fix to use `min(k, 12-k)` direction); (4) target patches differ only by fill colour (fix with 1-px grey border).

## Notes
- Novelty checks clean both at the family level and re-run on the full L3 spec.
- Stage-conflation guard on L3 planning depth holds.
- Issues are all concrete and fixable in a single revision pass — round-2 should pass.
- Visit count of `critique_spec`: 1 (this is the first entry; well under the 10-cap).
