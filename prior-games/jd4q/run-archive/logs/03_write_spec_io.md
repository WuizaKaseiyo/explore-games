# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): id jd4q, family echo-trail-teleport, distinguishing rules, negative-similarity check.
- skills/code/spec-template.md (this state): 9-section template structure
- skills/code/universal-scaffold.md (this state): scaffold conventions
- skills/code/novaengine-api.md (this state): Sprite/Level/Camera/NovaBaseGame API
- skills/design-constraints/{checklist,composition-and-tutorial,difficulty-rules,core-knowledge-priors,forbidden-elements}.md (from #01 study)

## Deliverables Produced
- `workspace/mechanic-spec.md`: 9-section spec covering Title, Mechanic family + priors, Sprite roster (4×4 stride-4), Level progression with mechanics + counterfactual + witness + difficulty per level (L1=walk only N=1; L2=walk+echo-teleport+closing-doors N+2=3; L3=+echo-eraser N+1=4), Action mapping `[1,2,3,4,6]`, HUD (StepCounterHud at top row), Win condition (per-level required_pickups + on-goal), Lose condition (step budget exhausted), Novelty note vs all 25 reference + 27 priors.

## Notes
- Grid sized at 64×64 with cell-stride 4 (logical 16×16 maze of 4×4-pixel cells). All sprites are 4×4 with internal pixel structure to satisfy checklist 20 (no chunky upscaling).
- Echo trail length K=16 chosen so witness teleport-back jumps stay alive.
- ACTION6 disabled at L1 via `_get_valid_actions` to avoid hidden-mechanic violation (echo-teleport not yet a level-1 mechanic).
- L3's eraser placement at the only path to goal forces M4 distinguishing-behavior to fire in every winning sequence (per checklist 12) AND constrains visit-ordering (C must be last) so the trivial nearest-greedy heuristic genuinely fails (per difficulty-rules.md L3 (d) requirement).
- Witness lengths: L1=11, L2=19, L3=44; budgets 30/60/100 give 2-3× margin per difficulty-rules.md "generous over witness".
- All 5 sprite role classes (avatar, echo, door, pickup, eraser) have distinct palettes and internal pixel structure; no `{4,8,9}` cautionary-tale palette.
