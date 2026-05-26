# Step #04: critique_spec (visit 1 of ≤10)

## Inputs Consumed
- mechanic-spec.md (from #03): the full 9-section spec under review.
- mechanic-pick.md (from #02): the novelty pick context.
- skills/design-constraints/checklist.md (from harness): 22 checklist items.
- skills/design-constraints/forbidden-elements.md (from harness): cultural-convention prohibition.
- skills/design-constraints/difficulty-rules.md (from harness): stage-conflation guard for L2 planning.
- skills/design-constraints/composition-and-tutorial.md (from harness): level-progression rules.
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md (from harness): novelty re-check on full spec.
- skills/code/universal-scaffold.md (from harness): camera/grid_size invariant.

## Deliverables Produced
- critique-revisions.md: per-mechanic counterfactual table for all (mechanic, level) pairs; independent enumeration of L2/L3 alternate strategies; **two CRITICAL issues** (Issue #1 forbidden chevron-arrow on `block_directional`, Issue #2 stage-conflation in L2 planning-depth justification); two MINOR (Issue #3 explicit camera viewport note in §6, Issue #4 optional avatar repeat). Novelty re-check: still NOVEL. **Verdict: REJECT → transition back to write_spec.**

## Notes
- Counterfactual table verifies item 12 strictly: every (M, L) row answered "no" with a concrete grounding (cell/sprite/rule). L3 M4 verified by enumeration — the greedy "deliver block_D first" alternate collides with block_C at column 5; the "couple block_C from non-south" alternate fails the chevron-direction match.
- Issue #1 — the `block_directional` pixel pattern unambiguously reads as an arrow shape pointing east; rotations produce arrows in the other cardinals. `forbidden-elements.md` lists "an arrow shape implying direction" as a hard prohibition. Replace with a 2-pixel magenta edge-stripe along the haul-side edge — abstract, topological, not arrow-shaped.
- Issue #2 — spec L2's planning-depth wrong-path was "walking without ACTION5", which is a discovery-stage misstep (the player hasn't yet learned the beam mechanic). Per `difficulty-rules.md` § c stage-conflation guard, the wrong-path must be a post-discovery failure. Redesigned L2 to force an order: block_orange at (8, 8) blocks block_yellow's straight south path; the post-discovery wrong path "deliver yellow first along straight south" gets a real collision rejection that requires the player to reason about haul-path geometry.
- Issue #3 — one-line addition to §6 to acknowledge the camera viewport is the 64×64 default (no resize needed because all levels declare grid_size = (64, 64)).
- Issue #4 — optional avatar revisit; the current pattern doesn't unambiguously read as a face, but the resemblance could be reduced.
- Visit count: 1 of ≤10. Plenty of revision budget for subsequent passes.
- Novelty re-check on fleshed-out spec: positive similarity-check + negative-similarity-check both confirm NOVEL.
