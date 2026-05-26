# Step #04: critique_spec

## Inputs Consumed
- workspace/mechanic-spec.md (from #03 write_spec): full 9-section spec.
- workspace/mechanic-pick.md (from #02 pick_mechanic): for re-running novelty against the pick.
- workspace/study-notes.md (from #01 study): for cross-referencing claims.
- skills/design-constraints/checklist.md: 16 items + 10a.
- skills/design-constraints/{composition-and-tutorial,core-knowledge-priors,forbidden-elements}.md: rule definitions.
- skills/mechanic-novelty/{similarity-check,negative-similarity-check,taxonomy-of-25-games}.md: re-run novelty.
- prior-games/index.md: 4 prior rows + each prior's mechanism-detail.md.
- skills/global/{action-enum,color-legend}.md.

## Deliverables Produced
- workspace/critique-pass.md: verdict PASS — every checklist item (1-16 + 10a) explicitly marked ✅, including walk-only refutation for L1, walk-no-wax refutation for L2, four-mechanic strict-required argument for L3, and an adjacent-action commute that breaks L3 solvability. Adversarial failure-mode sweep (spec-drift, sprite-glyph collision, pseudo-multi-mechanic, tutorial difficulty, level count, negative-similarity drift) all clear.

## Notes
- This is critique_spec visit #1. The cap is 5; we're well under.
- The most adversarial parts of the review were:
  - L3 strict-required-by-witness: verified all four mechanics are necessary, not just "exercised". Without any one of {walk, rotate, wax, filter}, the level is unsolvable (computed). 
  - Sprite-glyph collision: 3×3 yellow with central off-black pixel deliberately doesn't read as "8" or "0" or any digit/letter at the rendered resolution.
  - Negative-similarity drift: the L2/L3 additions did NOT pull lq5x closer to any prior or taxonomy entry; if anything, the dark-arena-with-lit-cone visual is further from the priors' flat-colour boards than at pick-time.
- The transition condition for `implement` (all checklist items pass + novelty NOVEL for every row) is satisfied. Proceeding.
