# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): game ID `vd3g`, family `valley-dig-roll`, mechanic description.
- skills/code/spec-template.md: 9-section template structure.
- skills/code/universal-scaffold.md: file structure guidance + camera viewport rule.
- skills/code/novaengine-api.md: engine API surface.
- skills/design-constraints/composition-and-tutorial.md: 3-level structure.
- skills/design-constraints/difficulty-rules.md: per-level a/b/c/d justification.
- skills/design-constraints/checklist.md: 21-item compliance.

## Deliverables Produced
- mechanic-spec.md: 9-section spec covering title, mechanic family (vd3g `valley-dig-roll`), sprite roster (1 terrain canvas + 3 marble colour variants + per-cell-type pixel patterns), per-level layout / mechanics / necessity / witness / difficulty for L1 (6 actions, budget 16), L2 (31 actions, budget 50), L3 (30 actions, budget 80), action mapping (ACTION6 only), HUD spec, win/lose predicates, and novelty note vs 7 closest priors.

## Notes
- Single-action-set: ACTION6 only. Click toggles non-wall non-target cell. Anchor cells flip together.
- Marble settling rule: marble on HIGH with adjacent LOW rolls priority N→E→S→W; marble on LOW stays.
- L1 +1 mechanic = dig+roll. L2 = + walls. L3 = + anchor pairs.
- All cell types have internal 4×4 pixel pattern (no flat-coloured chunky blocks per checklist item 20).
- No hidden state: every cell type is fully readable from the rendered frame; marble identity is encoded in hue; targets show coloured ring matching marble.
