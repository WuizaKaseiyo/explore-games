# Step #02: pick_mechanic

## Inputs Consumed
- (no run-input seed): autonomous mode confirmed by user at session start.
- skills/mechanic-novelty/taxonomy-of-25-games.md: full taxonomy of 25 reference games (the static novelty floor).
- skills/mechanic-novelty/similarity-check.md: positive similarity rules.
- skills/mechanic-novelty/negative-similarity-check.md: 7-dimension overlap test (the kf42 → vh68 cautionary tale).
- prior-games/index.md: 22 prior generated games — the cumulative corpus.
- prior-games/{bx84,gv47,kp9z,gx7m}/mechanism-detail.md: deep view of the closest priors to my candidate (read in step #01).
- skills/code/id-generation.md: 4-character ID generation rules and reserved-ID list.
- skills/conventions/reference-game-patterns.md (carried from #01): "Discoverability through observable change", "No hidden state", "Animation mandatory for long-distance / multi-step transitions".
- skills/design-constraints/core-knowledge-priors.md (carried from #01): four allowed priors.

## Deliverables Produced
- mechanic-pick.md: 4-character ID `yf3h`, mechanic family `pulse-arm-burst-resonate`, full mechanic description, similarity-check pass against the closest 5 priors (bx84, gv47, gx7m, kp9z, vn8d) and 3 taxonomy near-misses (cd82, ka59, m0r0), plus a 7-dimension negative-similarity table for each of the 3 closest priors (bx84, gv47, gx7m). Verdict: NOVEL.

## Notes
- Mechanic-family choice rationale: looked for an under-explored corner of (physics + objectness + geometry) priors. The corpus is heavy on (movement + click + match) games; the corner of "transient propagation + multiset-simultaneity" is unoccupied.
- Concrete divergence axes: my emitters fire OMNIDIRECTIONAL CONCENTRIC RINGS (vs bx84's linear beams, gv47's region-fill, gx7m's graph-BFS), and the activation rule is MULTISET ON SAME TICK (a temporal-coordination puzzle that none of the priors have).
- ID `yf3h` chosen by random 2-letter prefix + 2-char suffix per `id-generation.md`; verified absent from the 25-reference reserved list and the 22-prior corpus.
