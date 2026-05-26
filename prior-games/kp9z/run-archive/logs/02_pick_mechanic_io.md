# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (HITL=not allowed; autonomous = no seed)
- prior-games/index.md (26 priors)
- skills/mechanic-novelty/taxonomy-of-25-games.md (25 reference families)
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md
- skills/design-constraints/core-knowledge-priors.md, forbidden-elements.md
- skills/code/id-generation.md
- skills/conventions/reference-game-patterns.md (study cache)

## Brainstorm survey
Reviewed mechanic families across 51 games. Heavily explored: object-on-grid push (pq6m, vk8m, kn58, wt39), conveyor/flow (tj4f, sp80), beam/illumination (bx84, lq5x, vp6h), regions/colour (gv47, hr8q, dc22), recipes/sequences (sb26, hr8q, tn36, tr87), pendulum/momentum (fq8d), gear-mesh (gx7m), vortex (vk8m), portals (qx9d), domino chain (vn8d), pulley/anchor (kn58), tether (kf42), tide/tilt (kx14).

Underexplored: per-cell integer-counter dynamics with automatic redistribution. Picked Abelian-sandpile-style "grain accumulation + threshold-topple", visualized as sub-cell pip patterns.

## Deliverables Produced
- workspace/mechanic-pick.md: ID `kp9z`, family `grain-accumulate-topple`, full positive + negative similarity walks against all 26 priors and the 25 reference families.

## Notes
- Considered & rejected: tide-flip (kx14 too close), tilt-maze (Labyrinth-known), cone-sweep (lq5x), spinner-plate (qz73), cog-wedge (gx7m), bridge-build-decay (fz5j), polarity-magnet (kn58), zip-line (qx9d), inchworm (sk48 too close), kaleidoscope (ar25), tile-stack (Tetris-axis-1).
- Selected sandpile: closest matchup is vn8d (cascade-toppling). Five concrete distinguishing rules in §9 of mechanic-pick.md. Negative check shows ≤1 shared dimension with any prior.
- Ridiculously safe palette baseline tentatively: backdrop 2 light-grey, dark border 4, grain 11 yellow, target 13 maroon, sink 9 blue, rapid-topple 12 orange, HUD 14 green. Final palette decided in spec.
