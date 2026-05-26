# Step #02: pick_mechanic

## Inputs Consumed
- states/pick_mechanic.md (from harness root)
- skills/code/id-generation.md (rules for 4-char ID)
- skills/mechanic-novelty/{taxonomy-of-25-games.md, similarity-check.md, negative-similarity-check.md, prior-games-index-format.md}
- prior-games/index.md (cumulative novelty list — 19 entries)
- skills/mechanism-details/*.md (read in study; consulted for near-miss judgements)
- prior-games/<id>/run-archive/smoke-frames/level_1.png for kx14, pz4t, vp6h, gx7m, pj7k, kn58 (visual signature comparison per negative-similarity-check.md)
- skills/design-constraints/core-knowledge-priors.md (to confirm "basic physics" prior allowed)

## Deliverables Produced
- workspace/mechanic-pick.md: 4-char ID `lv4k`, family `lever-balance-torque`, one-paragraph description, action mapping, per-level mechanic progression with witness traces, positive similarity-check matrix vs. taxonomy + priors, negative similarity-check 8-dimension table vs. visually closest priors, implementation-feasibility notes.

## Notes
- Run input: no seed provided; chose autonomously.
- The cn04+sp80+wa30 source-reading pattern (click+arrow+ACTION5 select-and-move-and-modal) was tempting but exhausted by 11/25 references; went pure-click + modal instead.
- Considered alternatives: knot-crossing-flip, weave-loom, sand-physics, echo-shadow-hazard, fold-paper-half, magnet-polarity, bubble-rise, brick-stack — rejected each on either preexisting-video-game similarity (sand/Tetris/Lights-Out) or excessive surface overlap with priors per negative-check.
- Lever-balance-torque is genuinely under-explored: the taxonomy + priors include zero rigid-body equilibrium games. The mechanic uses physics + objectness priors (allowed by core-knowledge-priors.md).
- Visual signature differentiator: a horizontal beam dominating the centre + fulcrum + tray below is not the layout of any prior I reviewed. Most priors render scattered grid pieces or a walkable arena; lv4k's strong horizontal anchor is a structural break.
- Note an orphan dir `prior-games/kp9z/` exists on disk but is NOT in `index.md`; per `prior-games-index-format.md` the index is the source of truth, so I treat kp9z as not-a-prior. Its mechanic per its `metadata.json` ("Grain Accumulate Topple Cascade") is anyway unrelated to lever-balance.
