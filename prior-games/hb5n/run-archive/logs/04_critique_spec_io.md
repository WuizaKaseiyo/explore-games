# Step #04: critique_spec (pass #1)

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec): full 9-section spec
- mechanic-pick.md (from #02 pick_mechanic): novelty argument baseline
- skills/design-constraints/checklist.md (from study): 22 items
- skills/design-constraints/composition-and-tutorial.md (from study)
- skills/design-constraints/difficulty-rules.md (from study)
- skills/design-constraints/core-knowledge-priors.md (from study)
- skills/design-constraints/forbidden-elements.md (from study)
- skills/mechanic-novelty/similarity-check.md (from study)
- skills/mechanic-novelty/negative-similarity-check.md (from study)
- prior-games/index.md + 9 untracked priors' mechanism-detail.md (sampled during study)

## Deliverables Produced
- critique-revisions.md: identifies one load-bearing failure (item 12 strict counterfactual necessity for M4 = rotation-lock); proposes replacing M4 with PIVOT-RESET as a strictly-necessary alternative; lists all required spec changes. All other checklist items (1-22) and novelty checks pass.

## Notes
- The rotation-lock-cell mechanic looked clean at pick-time but adversarial reading of checklist item 12 ("Is there any way to win L within the step budget without ever triggering M?") shows the witness never triggers M4's distinguishing behaviour because it never presses ACTION5 on a lock cell. The alternate "rotate-at-(4,2)" path also wins, just with a slightly different witness length — making M4 redundant-decorative.
- The proposed replacement (PIVOT-RESET) targets a T-silhouette unreachable by A-pivot rotations of the 4-cell J, making M4 a HARD geometric gate. Strict counterfactual now passes: without M4, the target is unreachable.
- Visit count of critique_spec so far: 1. Cap is 10. Plenty of budget remaining.
- Transition back to write_spec for one revision.
