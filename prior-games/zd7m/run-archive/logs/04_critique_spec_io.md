# Step #04: critique_spec

## Inputs Consumed
- mechanic-spec.md (from #03)
- mechanic-pick.md (from #02)
- skills/design-constraints/checklist.md (items 1-20)
- skills/design-constraints/composition-and-tutorial.md
- skills/design-constraints/difficulty-rules.md
- skills/design-constraints/forbidden-elements.md
- skills/design-constraints/core-knowledge-priors.md
- skills/mechanic-novelty/similarity-check.md
- skills/mechanic-novelty/negative-similarity-check.md
- skills/mechanic-novelty/taxonomy-of-25-games.md
- skills/mechanic-novelty/prior-games-index-format.md
- prior-games/index.md (19 entries)

## Deliverables Produced
- critique-pass.md: All 20 checklist items pass; per-mechanic counterfactual
  table; novelty verdict NOVEL on both axes. PASS — proceed to implement.

## Notes
- L1's M2 colour-matching counterfactual is the weakest in the spec because
  geometrically the only "all on a target" cohort position is also colour-correct.
  The colour predicate is structurally part of every win check, so it still
  triggers — passes item 12 in the strict reading. Flagged but not blocking.
- All grid-bound and anchor-overlap math verified for L1, L2, L3 witnesses.
- L3 chamber genuinely portal-only: walk-around alternatives all blocked by
  cohort coupling + anchor (7, 10) preventing yellow from leaving column 4.
