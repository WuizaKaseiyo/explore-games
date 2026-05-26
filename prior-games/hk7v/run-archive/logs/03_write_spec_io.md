# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic)
- skills/code/spec-template.md (newly read)
- skills/code/universal-scaffold.md (newly read)
- skills/code/novaengine-api.md (newly read)
- skills/global/* (carried memory)
- skills/design-constraints/* (carried memory)
- skills/mechanic-novelty/* (carried memory)

## Deliverables Produced
- mechanic-spec.md: full 9-section spec for `hk7v`. Action subset
  `[1,2,3,4,5]`. Three levels with witnesses (87 / 171 / 319 actions),
  step budgets 150 / 250 / 500. Mechanics M1 (overhead-manipulator),
  M2 (color-pairing), M3 (rope-clearance-above-wall), M4 (gravity-
  stacking-disassembly). Per-mechanic-per-level necessity table
  satisfied. No-hidden-state, no-low-resolution, ACTION7-omitted
  rules satisfied.

## Notes
- Grid is 64×64 (no upscaling) per checklist 20.
- Sprites have internal pixel pattern (blocks 5×5 with 2-colour
  inset; trolley 5×4 multi-palette; hook 5×4 U-claw; wall 3×36
  with grain).
- Wall row range 20..55 chosen so that hook at minimum y=8 (rope
  length 0) carrying a block at y=12 (block bottom at 16) clears
  wall top 20 with a 4-row margin.
- Block stacking uses adjacency: block.y of stacked block = lower
  block.y - 5 (5-tall blocks). L3 stack heights: yellow y=43,
  blue y=48, red y=53.
- Win predicate uses block.y==53 (resting on floor row 57 since
  block is 5-tall starting y=53) AND block.x==target.x+1.
