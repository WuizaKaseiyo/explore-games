# Step #04: critique_spec (pass 1)

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec): full 9-section spec.
- design-constraints/checklist.md (items 1-21).
- mechanic-novelty/similarity-check.md, negative-similarity-check.md.
- skills/code/universal-scaffold.md (re-read for "Camera viewport must match level grid_size" rules).
- prior-games/index.md (re-checked novelty in spec context).

## Adversarial walk of all 21 checklist items
- Items 1-19, 21: PASS as written.
- **Item 20 (no info loss at 32×32): FAIL.** With `grid_size=(16,16)` at camera scale 4, each sprite-array entry renders as a 4×4 px solid block. Downsample 2:1 preserves the block-level pattern intact (each 4×4 block becomes a 2×2 block of the same color). The visual is purely cell-discrete, with no sub-cell pixel detail. The wavefront sprite especially fails — frontier cells render as 4×4 single-color blocks indistinguishable under downsampling.

## Novelty re-check
- Re-walked `similarity-check.md` and `negative-similarity-check.md` against the full spec (not just the family name). Result: NOVEL — same distinguishing rules as identified in #02 still hold for the fleshed-out L1/L2/L3 spec; no spec-drift toward an existing taxonomy or prior-games entry.

## Deliverables Produced
- critique-revisions.md: 1 numbered issue (item 20), with the offending section quoted, problem explained, and a concrete fix (switch to grid_size=(64,64) with LOGICAL_CELL_SIZE=4 logical cells, redesign all sprites at pixel-array level with internal sub-cell patterns; the redesign is documented in detail with new pixel matrices for each sprite type).

## Notes
- Single issue, narrow representational fix. No mechanic redesign needed; the BFS/timing math, witness solutions, and counterfactual necessity arguments are all unchanged.
- Transition back to write_spec for revision pass 1.
