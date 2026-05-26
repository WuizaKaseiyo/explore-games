# Step #03: write_spec

## Inputs Consumed
- states/write_spec.md
- mechanic-pick.md (from #02 pick_mechanic): ID dh4j, family tile-coded-stride, sketched mechanics
- skills/code/spec-template.md (9-section structure)
- skills/code/universal-scaffold.md (style rules — readable names, Pascal class, camera resize)
- skills/code/novaengine-api.md (API surface)
- skills/code/id-generation.md (ID rules — used in pick_mechanic)
- skills/design-constraints/checklist.md (16+ items)
- skills/design-constraints/composition-and-tutorial.md (L1/L2/L3 structure)
- skills/design-constraints/difficulty-rules.md (4-bullet per-level template)
- skills/design-constraints/core-knowledge-priors.md
- skills/design-constraints/forbidden-elements.md
- skills/global/action-enum.md (ACTION7 strict-undo)
- skills/global/color-legend.md (16-color palette)
- skills/conventions/reference-game-patterns.md (especially Discoverability + No-Hidden-State sections)

## Deliverables Produced
- mechanic-spec.md: 9-section spec (Title, Mechanic family, Sprite roster, Level progression + witnesses, Action mapping, HUD/state, Win condition, Lose condition, Novelty note). L1 has 3 mechanics (cell-pip-stride, wall-clamp, goal-overlap-wins); L2 adds 1 (filter swap); L3 adds 1 (facing-pivot 90° CW rotation). Each level's witness is enumerated; difficulty bullets (a,b,c,d) populated per level.

## Notes
- L2/L3 layouts noted as "high-level"; exact cell coordinates will be refined during `implement` to match the witness traces (and the critique may flag this — re-design will adjust). Current layouts may have subtle clamp issues I've identified in the trace.
- Per `reference-game-patterns.md` §Discoverability + the "long-distance transitions" note, multi-cell strides MUST animate cell-by-cell so the path is visible. This is incorporated via the `_slide_phase` animation machine in §6.
- Per `forbidden-elements.md`, the chosen palette avoids cultural hot/cold or symbolic readings. Yellow/blue/green/orange/maroon are used as abstract accents, not "hot/cold/danger".
- The avatar's pip-pivot pending indicator (arc decoration) is the persistent visible cue for the M5 state (no hidden state — checklist item 19).
- ACTION7 omitted because the game has no meaningful undo verb (per `action-enum.md` §slot-7-is-strict-undo, omit rather than overload).
