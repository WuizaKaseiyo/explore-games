# Step #02: pick_mechanic

## Inputs Consumed
- skills/mechanic-novelty/* (taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format)
- skills/code/id-generation.md (for ID format/collision check)
- prior-games/index.md (17 priors as of run start)
- mechanism-details summaries for all 25 references (carried over from study)
- prior-games/lq5x/run-archive/smoke-frames/level_1.png (negative-similarity visual check, since lq5x is the closest near-miss by flavour)
- prior-games/bx84/run-archive/smoke-frames/level_1.png (negative-similarity visual check)
- (no run input seed — autonomous mode)

## Deliverables Produced
- workspace/mechanic-pick.md: game_id `vp6h`, family `shadow-cast-collect`; one-paragraph description; per-mechanic inventory; full positive-similarity-check distinguishing rules vs lq5x, bx84, lf52, ar25, kn58, gv47, fz5j; negative-similarity-check walked against lq5x level_1.png with verdict "shares 1, 4, 5 only — passes (heavy axes 6, 8 diverge cleanly)".

## Notes
- Considered and rejected: pendulum-swing-hook (clipart concern), gear-train (clipart "gear" reads as real-world object), wave-ripple (too close to gv47), conveyor-belt-routing (too close to rk7x live-switch-routing), buoyancy-stack (kx14 already exists), inertia-glide (wt39 already exists), echo-sonar-fog (close to lf52 + lq5x), color-flood-walk (close to gv47 + re86), phase-shift-realm (close to fz5j), accretion-snowball (close to pj7k), domino-piston (close to vn8d), magnetic-bistable (close to kn58), pair-rope-friction (close to kf42), tile-stamp (close to ft09), pump-flow (close to sp80), tile-rotation-cluster (close to lp85), Lights-Out (cultural-convention reject), tug-of-war (poor UX), liquid-vault (kx14).
- Settled on shadow-cast-collect: closest prior is lq5x (lantern theme), but the geometry is *inverted* (light=hostile vs light=safe), the lantern is *stationary on a rail* (not avatar-carried), and L3 introduces *dual-shadow intersection* — a compositional rule change rather than a single-cone modification.
- ID `vp6h`: not in 25 references, not in 17 priors, not English word, lowercase alphanumeric.
