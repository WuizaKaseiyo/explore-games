# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02)
- skills/code/spec-template.md
- skills/code/universal-scaffold.md
- skills/code/novaengine-api.md
- skills/code/id-generation.md
- skills/design-constraints/checklist.md
- skills/design-constraints/composition-and-tutorial.md
- skills/design-constraints/difficulty-rules.md
- skills/design-constraints/forbidden-elements.md
- skills/design-constraints/core-knowledge-priors.md
- skills/global/color-legend.md
- skills/global/action-enum.md
- skills/global/paths.md
- skills/conventions/reference-game-patterns.md

## Deliverables Produced
- mechanic-spec.md: 9-section spec with concrete L1/L2/L3 layouts on
  grid_size=(20, 20), 3×3 sprites, witness solutions
  (L1: DOWN×10; L2: RIGHT×10 + DOWN×4; L3: RIGHT×10 + DOWN×4 with portal),
  per-mechanic counterfactuals, difficulty justification per level.

## Notes
- Action set [1, 2, 3, 4]. No click, no ACTION5/7.
- Mechanic count: L1=2, L2=3 (+anchor), L3=4 (+portal). +1 per promotion.
- Visual signature distinct from kn58/wt39 (palette + 3×3 patterned sprites).
- Pawn-pawn collision resolution: row-then-col deterministic order.
- Portal teleport is animated (6 frames, multi-phase step()).
- L3 includes a guard anchor at (5, 8) to widen witness-vs-greedy gap;
  greedy-DOWN-first heuristic still wins but at 17 actions vs witness 14.
