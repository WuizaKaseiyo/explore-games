# Step #02: pick_mechanic

## Inputs Consumed
- Run seed: (none — autonomous mode; no seed provided)
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md (read in #01 study, retained)
- skills/design-constraints/core-knowledge-priors.md (retained)
- skills/code/id-generation.md
- prior-games/index.md (33 prior games)
- skills/mechanism-details/* — all 25 retained
- prior screenshots viewed (10+) for visual signature anchoring

## Deliverables Produced
- mechanic-pick.md: 4-char ID `qn7w`, family `pulse-chain-eject`, full one-paragraph description, similarity-check distinguishing rules against 5 reference near-misses + 9 prior near-misses (vn8d, kp9z, bx84, ka59, kn58, xn5p, gx7m, rk7x, vd3g, wt39), and negative-similarity-check pass against vn8d (closest), kp9z, bx84.

## Notes
- Considered ~20 candidate mechanics during deliberation. Strongest contenders: `pulse-chain-eject` (Newton's cradle), `fold-collapse-merge`, `ring-enclose-classify`. Rejected `ring-enclose-classify` — would collide with xn5p (chamber-stamp-partition: "pawn walks chamber and stamps walls to subdivide region") on the partition family. Rejected `fold-collapse-merge` — implementation complexity (shrinking playfield across folds) too high for one-pass generation.
- Selected `pulse-chain-eject` because the **distinguishing feature is binary and observable**: intermediate chain balls do not move during the cascade; only the terminal ball ejects. This is the inverse of vn8d's "every pillar falls" dynamic and kp9z's "neighbour-broadcast" sandpile.
- Action palette planned: `[6]` for L1 (pure click — pusher knobs only) probably extends to `[6]` across all three levels; this also keeps the action enum minimal per checklist item 5. Will finalise during `write_spec`.
- Visual plan (for write_spec): native 64×64 detail, balls as 6×6 round sprites with internal highlight/shadow pattern, pusher-knob with protruding handle, hollow target sockets with concentric ring, chain rails as 3-pixel-wide lines connecting balls. This satisfies checklist item 20 (no upscaled chunky cells) and item 21 (UI teaches: pusher's handle reads as "graspable", socket's hollow centre reads as "expecting an arrival").
