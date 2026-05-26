# Step #04: critique_spec (round 1)

## Inputs Consumed
- workspace/mechanic-spec.md (from #03 write_spec): full 9-section spec.
- workspace/mechanic-pick.md (from #02): id + family.
- skills/design-constraints/checklist.md (items 1-21).
- skills/design-constraints/composition-and-tutorial.md, difficulty-rules.md, core-knowledge-priors.md, forbidden-elements.md.
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md, taxonomy-of-25-games.md.
- prior-games/index.md.

## Deliverables Produced
- `workspace/critique-revisions.md` — five issues:
  1. L1 layout has unsealed top/bottom detour around the row-4 corridor → erode is not strictly necessary (item 12 violation).
  2. L2 layout permits a (4, 4) → (4, 2) → (5, 2) → (6, 2) → (6, 3) → (6, 4) → (7, 4) detour that bypasses the blue wall → colour-pickaxe-match for blue is not strictly necessary (item 12 violation).
  3. L3 inherits the same blue-wall detour → same violation.
  4. Avatar's "pickaxe" is real-world clipart → item 7 / forbidden-elements violation.
  5. L3 difficulty rule (c) heuristic-failure argument is a discovery-stage misstep, not post-discovery → stage-conflation guard violation; the geometry forces a unique route making it effectively a 1-action-lookup-table for a fully-informed player.

## Notes
- Items 1, 2, 3, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19, 20 all pass.
- The novelty distinguishing rules in § 9 remain valid; the geometry changes don't shift the family identity.
- Concrete fixes given for each issue. Round 2 of critique should re-run the full checklist on the revised spec.
- This is critique_spec visit count = 1 of the 10-cap.
