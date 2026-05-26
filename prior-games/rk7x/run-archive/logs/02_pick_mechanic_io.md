# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (run input: autonomous, no seed)
- skills/global/* (action-enum.md, color-legend.md, paths.md)
- skills/design-constraints/core-knowledge-priors.md (which priors are allowed)
- skills/mechanic-novelty/taxonomy-of-25-games.md (full novelty floor)
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md, prior-games-index-format.md
- skills/code/id-generation.md (4-char ID rules + reserved list)
- skills/mechanism-details/* (read in #01 for all 25)
- prior-games/index.md (16 prior entries — kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p)
- 15 prior-game level_1.png screenshots opened in #01.
- 25 reference-game level_1.png screenshots opened in #01.

## Deliverables Produced
- workspace/mechanic-pick.md: 4-character ID `rk7x`, mechanic family
  `live-switch-routing`, full description, per-level mechanic count plan,
  per-near-miss positive distinguishing rules, negative similarity-check
  walk against all priors, palette plan, NOVEL verdict.

## Notes
- The candidate is "edit junction switches in real-time while a coloured
  courier auto-walks the corridor network one cell per click". Each player
  click ticks the courier, so clicks-on-switches and clicks-on-empty-space
  are both free routing-edits but each costs one tick of the courier's
  budget.
- Most relevant near-misses: tn36 (program-pawn-trace; distinct because
  edit-during-execution rather than compose-then-run), bp35 (gravity-fall;
  distinct because player is NOT the auto-mover), and tu93 (multi-agent
  grid; distinct because couriers ignore player-as-input). Negative-check
  ruled all out at <3 dimensions of overlap.
- L1=1 mechanic (live switch routing). L2=L1+2 (colour-order stops + dead-end
  branches). L3=L2+2 (dual couriers + conflict cells). Each promotion
  satisfies the strict +1-or-+2 rule and the carry-forward requirement.
- ID `rk7x` checked against the reserved 25 (no collision) and the 16
  priors (no collision).
- Palette plan deliberately avoids the kf42→vh68 cautionary palette
  signature `{4 wall, 8 red, 9 blue}`. Walls = 5 (black) framing, courier
  = 11/12 (yellow/orange), switches = 14/6 (green/magenta), stops = 10
  (light-blue), terminal = 15 (purple), HUD = 3 (grey).
