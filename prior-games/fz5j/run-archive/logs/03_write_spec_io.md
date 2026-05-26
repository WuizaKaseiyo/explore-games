# Step #03: write_spec

## Inputs Consumed
- `workspace/mechanic-pick.md` (from #02 pick_mechanic): ID `fz5j`, family `phase-step-tile`, mechanic description.
- `skills/code/spec-template.md`: 9-section template.
- `skills/code/universal-scaffold.md`: file structure conventions, camera-viewport gotcha, simultaneous-conflict resolution, two-sprite-swap idiom.
- `skills/code/id-generation.md`: ID validation.
- `skills/design-constraints/composition-and-tutorial.md`: 3-level structure, +1-or-+2 per level, no-hidden-mechanics, no-trivial-fallback.
- `skills/design-constraints/difficulty-rules.md`: per-level difficulty bullets (random-resistance, human-tractable, planning depth, step budget).
- `skills/design-constraints/checklist.md`: 18 items.
- `skills/design-constraints/forbidden-elements.md`: no symbols/letters/digits/clipart.
- `skills/design-constraints/core-knowledge-priors.md`.
- `skills/global/{action-enum,color-legend,paths}.md`.

## Deliverables Produced
- `workspace/mechanic-spec.md`: 9-section spec for `fz5j`. Core: avatar walks pulsating phase tiles (period 2/3/4) on a pure-arrow `[1,2,3,4]` action palette; ACTION5/6/7 unused. L1 has 14×14 grid with 2 phase-2 tiles in a row (witness 14, budget 22). L2 adds phase-3 (witness 16, budget 30). L3 adds phase-4 + a fragile-phase-3 variant that locks permanently on first blocked attempt (witness 26, budget 40). The fragile rule defeats the L1/L2 retry-in-place strategy and provides L3 commute-test traction (swap of witness actions 12/13 leaves avatar trapped in col-11 dead-end, level unsolvable).

## Notes
- Decided AGAINST including ACTION5 ("wait"): a blocked move (move into wall or closed phase tile) already advances the counter without moving the avatar, so ACTION5 would be redundant with the wall-bounce idiom. Keeps available_actions minimal per checklist item 5.
- Mechanic count progression L1→L2→L3 = 2→3→5 (jumps of +1 then +2). +2 jump on L3 is allowed by composition rules.
- Considered concerns about commute test rigour. Settled on swapping witness actions 12 and 13 (D into (10,2) vs D into (10,3)), where layout walls bracket col-10 such that swap → avatar at (11,1) stuck in dead-end → unsolvable.
- L3's fragile cell creates a "no-retry" constraint that requires precise residue computation; this defeats the "always retry on block" strategy that suffices for L1/L2 (the named trivial heuristic for item 18 L3).
- Aesthetics: 7-color palette (4/5/6/8/10/11/12/14) + background palette 1; visually distinct from kf42→vh68 cautionary `{4,8,9}`. Pulse rates of 2/3/4 produce a deliberate visual rhythm.

