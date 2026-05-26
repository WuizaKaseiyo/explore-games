# Step #04: critique_spec (visit 1)

## Inputs Consumed
- mechanic-spec.md (the just-written spec)
- skills/design-constraints/checklist.md (items 1-21)
- skills/design-constraints/difficulty-rules.md (§ 3 critique check)
- skills/design-constraints/forbidden-elements.md
- skills/mechanic-novelty/{similarity-check, negative-similarity-check, taxonomy-of-25-games}.md
- skills/mechanism-details/* (retained from study)

## Deliverables Produced
- critique-revisions.md: 3 substantive issues flagged.
  1. L2 win predicate unwinnable: yellow decoy socket can't be filled but the predicate "every target_socket filled" requires it.
  2. pusher_knob "handle protrusion encoding direction" reads as a directional arrow / cultural convention (forbidden-elements violation).
  3. L3 chain A down-branch positions extend off the 64×64 grid (`(20, 62)` ball spans y=62..67).

## Notes
- All other checklist items 1-21 + difficulty-rules § 3 + similarity + negative-similarity tests pass.
- Issues are fixable with localised edits to §3 (pusher_knob redesign + dead_end_wall sprite added) and §4 (L2 layout: drop yellow decoy; L3 layout: shift positions, add dead-end walls).
- Transitioning back to `write_spec`. Visit 1 of 10 critique cap; ample budget remaining.
