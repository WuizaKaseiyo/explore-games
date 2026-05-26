# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02): ID, family, distinguishing rules.
- workspace/study-notes.md (from #01).
- skills/code/{spec-template,universal-scaffold,novaengine-api,id-generation}.md.
- skills/design-constraints/{checklist,composition-and-tutorial,difficulty-rules,core-knowledge-priors,forbidden-elements}.md.
- skills/global/{action-enum,color-legend,paths}.md.

## Deliverables Produced
- workspace/mechanic-spec.md: 9-section spec covering Title, Mechanic family (rolling-cube-face-paint), Sprite roster (cube, target_*, paint_*, wall, gate_*, step bar HUD), Level progression (3 levels: L1 rolling-paint with [E,E] witness; L2 +twist with [twist,E,E,E,twist,S] witness; L3 +walls with [twist,E,E,E,twist,S] witness through walled layout), Action mapping (1..5 with full rolling/twist permutation tables), HUD state (faces dict, cube position, step counter), Win/Lose, Novelty note.

## Notes
- Several iterations of L3 layout were attempted in-spec (showing the design search) before settling on a wall-based L3 with strict-necessity argument that critique_spec must verify against the actual solver.
- The L3 strict-necessity-of-walls argument is admittedly hand-wavy in the current draft; flagged for critique. May need a second `write_spec` pass after critique.
- Mechanic count discipline: L1=1, L2=2, L3=3 — every earlier mechanic carried forward in witness.
- All face permutation formulas (north/south/east/west/twist) are explicitly tabulated in §5 to make the implementation step deterministic.
- Background palette = 1 (off-white) chosen to diverge from prior-games' dark-grey signatures.
