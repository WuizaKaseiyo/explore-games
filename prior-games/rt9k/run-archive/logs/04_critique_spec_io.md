# Step #04: critique_spec

## Inputs Consumed
- mechanic-spec.md (from #03)
- skills/design-constraints/checklist.md (items 1-22)
- skills/design-constraints/forbidden-elements.md
- skills/design-constraints/composition-and-tutorial.md
- skills/design-constraints/difficulty-rules.md
- skills/design-constraints/core-knowledge-priors.md
- skills/mechanic-novelty/similarity-check.md
- skills/mechanic-novelty/negative-similarity-check.md
- skills/mechanic-novelty/taxonomy-of-25-games.md
- prior-games/index.md (re-checked); unindexed prior-games mechanism-detail.md (re-checked the most-similar candidates)
- skills/global/action-enum.md (item 22 strict-undo verification)

## Deliverables Produced
- critique-pass.md: PASS verdict on all 22 checklist items + novelty positive + negative-similarity. Per-mechanic counterfactual table for items 11/12 walked through alternates concretely (DOWN-first wrap, UP-first wrap, LEFT-wrap-and-walk greedy).

## Notes
- The most adversarial review went into item 12 (no trivial fallback). I traced multiple plausible alternate paths at L2 and L3 and verified that each fails at a concrete cell/sprite. The L3 yellow-filter necessity was the trickiest: I had to confirm that *any* path arriving at (13,7) tone=yellow must pass through `filter_yellow` — by tracing from the goal cell backward through tone-change requirements (yellow at goal → tone change from green → wrap UP from (13,0) → lands at (13,14) which IS filter_yellow), and ruling out alternative tone-change sequences (DOWN-wrap from green→magenta, RIGHT-wrap from green→magenta, none of which give yellow at the right cell without re-passing filter_yellow). The conclusion: filter_yellow is on every winning path.
- Item 21 (UI teaches) deserved attention because the wrap mechanic itself is not statically visible. The argument that survives critique is: discoverability *through a small number of exploratory actions* satisfies the "no instructions" principle (cited from `from-tech-report.md` § 4), and 2-3 LEFT presses against the left edge reliably reveal the wrap. The static frame DOES communicate the cast (avatar, wall, goal) and the role of each (controllable / obstacle / target) via shape alone.
- Negative similarity re-walk: the closest prior is pk4m, sharing dimensions 1, 3, 4, 5 (universal-board pattern). On dimensions 6 (palette signature: three-tone vs two-tone), 7 (4×4 ring sprites vs unspecified pk4m grain), and 8 (topology-coupled tone vs free-toggle tone), the candidate diverges. Per the rule, dimensions 6/7/8 are heavily weighted; passing on those three is the load-bearing test.
- No revisions required. Single visit to critique_spec; transitioning to implement.
