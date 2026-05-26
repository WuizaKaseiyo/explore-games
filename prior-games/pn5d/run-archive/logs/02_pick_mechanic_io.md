# Step #02: pick_mechanic

## Inputs Consumed
- skills/global/* (cached from study)
- skills/design-constraints/core-knowledge-priors.md (cached)
- skills/mechanic-novelty/{taxonomy-of-25-games.md, similarity-check.md, negative-similarity-check.md} (cached)
- skills/code/id-generation.md (full)
- prior-games/index.md (full, 49 priors)
- prior-games/kx14/mechanism-detail.md (full — closest near-miss for the candidate)

## Deliverables Produced
- workspace/mechanic-pick.md — game ID `pn5d`, family `vessel-equalize-flow`, full positive + negative similarity check.

## Notes
- No user seed; chose autonomously.
- Surveyed under-explored corners of the priors-cube. Recent priors are dominated by geometric/topological folding (rj5w, wj7d, qj4r), beam/LOS optics (bx84, kw8t, vp6h), and trail/wake mechanics (ek73, jd4q, tj4n). Liquid mechanics are nearly absent (only kx14, sp80) and neither uses connected-vessel equilibration.
- Considered but rejected:
  - shepherd-flock (sheep follow avatar) — too close to zk9p (`pursuer-merge-walk`) on the agent-following-player dynamic.
  - liquid-color-mixing — risks colour-cultural-convention violations.
  - electrical-circuit / pipe-rotation — viable but more visually busy and harder to teach.
- Settled on `vessel-equalize-flow` as the cleanest fit: physics-prior + topology-prior, novel verb (pour-and-equilibrate), action subset `[3, 4, 5, 6]` not used by any of the 25 references.
- ID `pn5d` selected via random procedure; verified clean against reference list and prior-games index.
