# Step #05: write_spec (revision pass 1)

## Inputs Consumed
- mechanic-spec.md (existing, from #03 write_spec).
- critique-revisions.md (from #04 critique_spec): 1 issue flagged (item 20).

## Deliverables Produced
- mechanic-spec.md (revised in place): § 3 Sprite roster rewritten end-to-end; § 4 opening paragraph rewritten to clarify logical-vs-pixel coord conventions; § 5 ACTION6 action mapping rewritten to specify click-to-logical-cell conversion. Witness coordinates kept as logical-cell coords with display-coord conversion noted (`(lcx*4 + offset)`).

## Sections changed
- § 3 Sprite roster (full rewrite)
- § 4 opening paragraph (added pixel-vs-logical-coord clarification)
- § 5 ACTION6 description (added explicit logical-cell conversion via `// 4`)

## Sections unchanged
- § 1 Title
- § 2 Mechanic family
- § 4 per-level mechanics, witness solutions, difficulty justifications, BFS distances
- § 6 HUD and per-game state
- § 7 Win condition
- § 8 Lose condition
- § 9 Novelty note

## Notes
- Per critique-revisions.md: switched to `grid_size=(64, 64)` with `LOGICAL_CELL_SIZE=4`. Sprite pixel matrices redesigned at 4×4-pixel-per-logical-cell granularity using filled-frame (F) and hollow-frame (H) templates that visibly damage on 2:1 downsampling.
- All numeric content in § 4 (BFS distances, witness lengths, step budgets, stagger arithmetic) is unchanged because it operates at logical-cell granularity, which is unaffected by the pixel-resolution switch.
- All counterfactual necessity claims in § 4 are unchanged (mechanics still operate on logical-cell coordinates).
- All novelty arguments in § 9 are unchanged.
- Ready to re-enter critique_spec (pass 2).
