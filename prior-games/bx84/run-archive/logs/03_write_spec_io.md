# Step #03: write_spec

## Inputs Consumed
- task-overview.md, states/write_spec.md
- skills/code/spec-template.md (9 sections required)
- skills/code/universal-scaffold.md (game-class structure, sprite-name semantic, Camera viewport must match grid_size)
- skills/code/novaengine-api.md (Sprite/Level/Camera/NovaBaseGame signatures)
- skills/design-constraints/{checklist,composition-and-tutorial,core-knowledge-priors,difficulty-rules,forbidden-elements}.md
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check}.md
- workspace/mechanic-pick.md (chosen mechanic family + ID `bx84`)

## Deliverables Produced
- workspace/mechanic-spec.md — full 9-section spec with EXACTLY 3 levels, witness solutions per level, per-mechanic counterfactual necessity rows, difficulty justifications including L3 commute test (the spec's most-finicky item).

## Notes / Design Decisions
- Switched the L3 third target from `target_green` (palette-14) to `target_yellow_north` (palette-11) mid-spec because the north-branch beam never passes the filter and so remains palette-11; lighting target_green would require a colour mismatch or a second filter, both worse design. Two yellow targets at different positions (north and south of emitter row) is the cleanest fit.
- L3's order-dependence emerges from sticky-but-only-on-click target lighting + the prism-toggle mechanic. Beam tracing at level-load is for visualisation only; targets are NOT marked at level-load (only on `ACTION6` traces). This is the linchpin that makes "swap clicks 1 and 2 → witness broken" hold: the south branch only exists when the prism is in state ES, and the player must place a mirror (and re-trace) WHILE the prism is still ES to capture target_yellow_south's lit-state. Toggling first robs the player of that opportunity.
- All sprite sizes finalised:
  - Emitter, mirrors, filter, prism: 1×1.
  - Targets: 3×3 hollow rings (so visually distinct from 1×1 filters even when palettes match).
  - Beam overlay: 16×16 (covers the whole grid, transparent except along the beam path on empty cells).
- Action palette: pure click `[6]`.
- Camera: viewport set to `(16, 16)` in `on_set_level`; engine scales 4× to fill 64×64.
- Step budgets per level: 30 / 50 / 80 (monotonically non-decreasing, satisfies difficulty-rules.md § d).
