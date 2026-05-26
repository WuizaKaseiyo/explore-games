# Step #04: critique_spec (round 1)

## Inputs Consumed
- mechanic-spec.md (from #03)
- skills/design-constraints/checklist.md (items 1–21)
- skills/design-constraints/difficulty-rules.md
- skills/mechanic-novelty/{similarity-check,negative-similarity-check,taxonomy-of-25-games}.md
- skills/mechanism-details/{ar25,m0r0,cn04,lp85,sk48,bx84}.md (closest near-misses)
- prior-games/index.md
- skills/code/spec-template.md (verifying section structure)

## Deliverables Produced
- critique-revisions.md: 2 issues flagged.
  - Issue 1 (BLOCKER): item 12 violation at L3 — wall-anchored reflection (M4) is not counterfactually required because the witness's double-V-fold + lock structure naturally returns yellow to its target on the second V-fold without needing walls. Fix: drop walls (preferred) or redesign L3.
  - Issue 2 (sharpen): L2 planning-depth wrong-alternative is a discovery-stage misstep; replace with a genuine post-discovery alternative.

## Notes
- All other checklist items (1–11, 13–21) appear to pass on first read.
- Novelty checks (positive against taxonomy + priors; negative shared-dimensions test) all pass.
- L3's "double V-fold" insight is a real post-discovery planning step and the spec articulates it correctly — keep that wording.
- Transition: route back to write_spec for revision (1st revision; cap is 10 critique visits per run).
