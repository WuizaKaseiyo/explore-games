# Step #02: pick_mechanic

## Inputs Consumed
- states/pick_mechanic.md: instructions for this state
- skills/code/id-generation.md: 4-char ID rules + reserved IDs
- skills/mechanic-novelty/{taxonomy-of-25-games.md, similarity-check.md, negative-similarity-check.md, prior-games-index-format.md}: novelty checks
- skills/design-constraints/core-knowledge-priors.md: which priors are allowed
- skills/mechanism-details/<id>.md × 25: cached mechanism summaries for cross-checking
- prior-games/index.md: 15 prior generated games (kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39)
- L1 screenshots reviewed in #01 for visual-signature comparison
- Run input: no seed (autonomous mode)

## Deliverables Produced
- workspace/mechanic-pick.md — game ID `zk9p`, family `pursuer-merge-walk`, full description, similarity-check pass against taxonomy (no near-misses requiring distinguishing rules beyond cosmetic family-name overlap with m0r0), similarity-check pass against priors (closest comparator kn58, distinguished concretely), negative-similarity-check pass against kn58 (0 dims), ka59 (2 dims), tu93 (2 dims), g50t (0-1 dims).

## Notes
- Identified that the prior-games corpus has zero pursuit/agentness mechanics; this opens the agentness prior cube as fresh hunting ground.
- Mechanic centres on inducing enemy-on-enemy collisions (a verb that does not appear in any prior or reference): the player's role is "bait" rather than "fighter" or "collector".
- ACTION5 verb: "tick-skip" — held for L3 introduction, gated to no-op or non-advancing in L1/L2 (or could be excluded from `available_actions` until L3; will decide in spec).
- 4-character ID `zk9p` chosen by random pick; checked against both lists and English-word filter.
