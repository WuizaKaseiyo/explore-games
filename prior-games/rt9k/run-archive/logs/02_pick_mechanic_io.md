# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (run input: autonomous, no seed)
- skills/global/* (re-internalised from #01)
- skills/design-constraints/core-knowledge-priors.md
- skills/mechanic-novelty/taxonomy-of-25-games.md
- skills/mechanic-novelty/similarity-check.md
- skills/mechanic-novelty/negative-similarity-check.md
- skills/mechanic-novelty/prior-games-index-format.md
- skills/code/id-generation.md
- skills/mechanism-details/*.md (25 quick-reference summaries — re-checked closest near-misses: m0r0, g50t, tu93, bp35)
- prior-games/index.md (64 indexed entries) + 9 unindexed prior-game `mechanism-detail.md` (gh4r, hp9c, lz7q, qd6n, tc8s, tx4q, vk6m, vw3p, xv4n)

## Deliverables Produced
- mechanic-pick.md: game ID `rt9k`, mechanic family `torus-wrap-tone-cycle`, one-paragraph description, taxonomy + prior-games similarity check with concrete distinguishing rules vs each near-miss (pk4m, lz7q, gh4r, wt39, bz3k, jd4q, ek73; m0r0, g50t, tu93, bp35), and negative-similarity audit walking the 7 dimensions.

## Notes
- The corpus is dense (~73 prior games + 25 references). No
  obviously-empty mechanic family remains; novelty had to be
  established by combining a topological prior (torus surface)
  with a tone-cycle that is *structurally tied* to topology
  (only edge-cross changes tone). This combination is unattested
  in either taxonomy or prior-games corpus.
- Per the cautionary `kf42 → vh68` failure, palette and sprite-
  grain signatures will be deliberately chosen during write_spec
  to diverge from pk4m (closest prior) and from other recent
  priors. Specifically: avoid red/blue duotone, avoid 1×1
  rectangle pawns, lean on chevron edge markers + 4×4 striped
  avatar + ringed-frame walls.
- The mechanic uses §3.4 priors *geometry/topology* (torus
  surface — a topological structure) + *objectness* (avatar +
  walls + goal sprites). No physics, no agentness — keeps the
  prior-pair light and clearly within §3.4 categories.
- ID generation: `rt9k` was chosen as 2-letter prefix `rt` +
  2-char suffix `9k`. Not in the 25 reference IDs, not in the
  `prior-games/index.md`'s game_id column, not in any unindexed
  prior-games subfolder, not an English word. Per
  `id-generation.md` § Recommended generation procedure step 5,
  no regeneration needed.
- Decision was deliberate: many tempting mechanic ideas were
  rejected because they shared 5+ dimensions with priors per
  `negative-similarity-check.md` (e.g., pheromone trail vs nf3z;
  beam-bend vs bx84; conveyor toggle vs rk7x). The chosen
  mechanic clears the negative check on dimensions 6, 7, 8 (the
  weighted-heavy dimensions) by virtue of the topological frame.
