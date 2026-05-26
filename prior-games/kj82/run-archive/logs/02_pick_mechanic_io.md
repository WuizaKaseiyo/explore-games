# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (from harness root): no seed provided → autonomous mode
- skills/mechanic-novelty/* (from #01 study): taxonomy of 25, similarity check, negative similarity check
- skills/design-constraints/core-knowledge-priors.md (from #01 study): allowed priors
- prior-games/index.md (from harness root): 29 prior games to avoid
- skills/mechanism-details/*.md (all 25, from #01 study): per-game mechanic summaries
- skills/code/id-generation.md (from #01 study): ID rules

## Deliverables Produced
- mechanic-pick.md: game ID `kj82`, mechanic family `plank-pivot-walk`, full description, similarity-check + negative-similarity-check rules, visual-signature plan.

## Notes
- Considered ~30 candidate mechanics; rejected most for too-much overlap with priors (kx14 buoyant, gv47 region-grow, sk48 trail, qz73 radial, gx7m mesh, lv4k torque, mr5q polarity, pf3w wavefront, etc.). Chose plank-pivot-walk for two reasons: (1) the rotation is end-pinned not centre-pinned (verb is structurally different from cn04 and pz4t); (2) it composes naturally — base mechanic (rotate to bridge gap), +obstacle (post blocks rotation arc), +sticky (walk-on locks rotation) — three mechanics compose without any mechanic dropping out at L3.
- Chose ID `kj82` randomly per `code/id-generation.md`; verified non-collision and opacity.
- Action subset `[1,2,3,4,5,6]` (no undo) — places kj82 in the same family as cn04, dc22, ka59, m0r0, wa30, sb26 in cross-cut frequencies. Idiomatic.

