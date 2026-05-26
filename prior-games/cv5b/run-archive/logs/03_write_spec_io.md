# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (id=cv5b, family=arc-launch-target)
- skills/code/spec-template.md (9-section template)
- skills/design-constraints/{composition-and-tutorial,difficulty-rules,checklist}.md
- skills/global/{action-enum,color-legend}.md
- skills/conventions/reference-game-patterns.md (cached patterns)

## Deliverables Produced
- workspace/mechanic-spec.md: full 9-section spec with EXACTLY 3 levels.
  L1: 2 mechanics (walk + arc-fire); L2: 4 (+power-cycle, +shield-blocks-arc;
  +2); L3: 5 (+wind-deflects-arc; +1). All inheritance + counterfactual
  necessity stated per mechanic per level. Witnesses written out
  per level (L1=7 actions, L2=8 actions, L3=30 actions). Difficulty
  justifications cover (a) random-resistance, (b) human-tractable, (c)
  planning depth, (d) step budget per level.

## Notes
- Action-enum: ACTION7 omitted (no undo) per checklist item 22.
- Palette deliberately {10,14,12,11,13,5,7,0,1,4} — avoids the {4,8,9}
  cautionary signature from kf42→vh68.
- Grid 64×64 (default camera) for max pixel-density; checklist item 20
  satisfied by giving primary sprites internal pattern (launcher 6×6 with
  charge-dot interior; targets as 4×3 rings; shields as 2×6 bars).
- Sprite-swap idiom (3 launcher variants at same cell, swap interaction
  modes on power-cycle) inherited from universal-scaffold.
