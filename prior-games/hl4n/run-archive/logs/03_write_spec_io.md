# Step #03: write_spec

## Inputs Consumed
- task-overview.md, states/write_spec.md.
- mechanic-pick.md (the prior step's deliverable).
- skills/code/spec-template.md (9-section structure).
- skills/code/universal-scaffold.md (style rules — semantic names, no mechanic-spoiling comments).
- skills/code/novaengine-api.md (Sprite/Camera/Level/RUD signatures).
- skills/design-constraints/composition-and-tutorial.md, checklist.md, difficulty-rules.md, core-knowledge-priors.md, forbidden-elements.md.
- skills/global/{action-enum, color-legend, paths}.md.
- skills/mechanic-novelty/* (re-checked for novelty restatement in §9).

## Deliverables Produced
- `mechanic-spec.md`: full 9-section spec for game `hl4n`. Three levels (L1 row-only, L2 column-overrides-row, L3 brighter-wins blend), with per-level lock-target placements, witness solutions, and counterfactual necessity arguments.

## Notes
- The L3 design went through several iterations to find a witness that *forces* M3 (brighter-wins). Initial designs were solvable by L2-style column-only assignments, leaving M3 as a "hidden" mechanic. The final L3 introduces Lock G at `(2, 3)` requiring 14, sharing column 2 with Lock C at `(2, 6)` requiring 8 — col_2 must be 8 for C, so row_3 = 14 is needed for G, and only the brighter-wins rule (max(14, 8) = 14) makes G satisfiable. This is exactly the M3-required path checklist item 12 demands.
- L1 → L2 → L3 mechanic count: 1 → 2 → 3. Each level adds exactly 1 new mechanic, every prior mechanic carried forward and required.
- Step budgets: 30 / 60 / 80 (non-shrinking, generous over witness lengths of 6 / 10 / 15).
- Action palette: pure click `[6]`. No undo (per `action-enum.md` slot 7 strict-undo rule, omit ACTION7 since the game has no meaningful undo — clicking a marker N more times to "back-out" suffices).
- Palette: `{2 BG, 5 padding, 8 red, 11 yellow, 14 green, 4 frame, 3 hint, 0 white-satisfied}`. Deliberately avoids the `{4, 8, 9}` cautionary-tale palette and the kf42/vh68 over-used signature.
- The cell-rule transition L2→L3 (override → brighter-wins) is communicated to the player not by text but by the rendered behavior — clicking a column in L3 may NOT change the cell's color when the row is already brighter, which is observable feedback that triggers re-modeling.
- Did not include a sprite-rendering test of the brighter-wins concept here; the implement state will validate.
