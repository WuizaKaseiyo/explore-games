# Step #02: pick_mechanic

## Inputs Consumed
- states/pick_mechanic.md (from harness root): family-novelty + ID requirements.
- skills/code/id-generation.md: 4-char alphanumeric, opaque, non-colliding generation rule.
- skills/design-constraints/core-knowledge-priors.md (from #01): four allowed prior categories.
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check}.md (from #01): novelty floor + decision matrix + 8-dim qualitative test.
- skills/mechanism-details/*.md (from #01): per-game quick-references for distinguishing-rule articulation.
- prior-games/index.md (from #01): 27 cumulative priors.
- skills/conventions/reference-game-patterns.md (from #01): open-questions list (action palette / priors corner / distinctive-verb home).
- prior-games/{fz5j,wt39,zd7m,zk9p}/run-archive/smoke-frames/level_1.png: visually verified palette + sprite grain divergence for the closest near-miss priors. (fz5j is corridor-with-pulsing-tiles + small green/yellow markers; wt39 is sparse white-on-black scattered blocks; zd7m is a 2×3 same-shaped pad grid; zk9p is decorative noise-cells with sparse pawns. None overlap with ek73's intended magenta-wake + yellow-cross-avatar + brick-walls + 4-pointed-star-collectibles signature.)
- (Run input: no seed. Autonomous mechanic pick.)

## Deliverables Produced
- `workspace/mechanic-pick.md`: ID `ek73`, family `wake-trail-evade`, one-paragraph mechanic description, full taxonomy + prior-games similarity tables (positive check), 8-dim negative similarity walk against the closest priors with engineered divergences on dim 6/7/8, and the open-design-questions hand-off to `write_spec`.

## Notes
- ID `ek73` was confirmed not in the 25 reference list and not in `prior-games/index.md`. Not an English word.
- Five near-miss flags from the positive similarity check (`g50t`, `sk48`, `fz5j`, `wt39`, `zd7m`); each has a concrete distinguishing rule that survives the description-level test (win condition / primary action / primary constraint — only one of three matches per row, never all three).
- The closest concern is `fz5j` (phase-step-tile): shared dims 1 (object-on-grid), 2 (walk-avatar), 4 (lose-on-step-on-bad-cell). That is exactly 3, the threshold. Dim 4 sharing is real (both punish stepping on transient bad cells). The accept-rationale rests on dim 8 (heavy) clearly diverging — fz5j's bad cells are level-clocked, ek73's are player-created — and dims 6/7 (also heavy) are engineered to diverge by palette + sprite grain choice. The kf42→vh68 cautionary tale is the explicit anti-pattern this rationale is checked against.
- Dim 8 (core dynamic): "plan around my own past inputs as transient hard constraints on my next input" is genuinely absent from every prior I walked. Closest semantic neighbour is g50t (ghost-replay) but the constraint shape (commit-then-replay vs continuous-decay-tail) is fundamentally different.
- Action palette committed: `[1, 2, 3, 4]`. ACTION5 deliberately absent because the distinctive verb is "arrow press creates wake", not a separate modal slot. Pure-arrow is documented as one of ~7/25 reference patterns.
- Per-level mechanic plan handed off to `write_spec`: L1 = walk + wake-decay (K=3); L2 = + wake-clearer pads (one-shot floor pads that erase active wake); L3 = + wake-anchor cells (freeze current wake into permanent stone walls). Each level's witness must exercise EVERY mechanic at that level — to be enforced and re-derived in `write_spec` and `critique_spec`.
