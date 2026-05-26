# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (no run seed → autonomous mode)
- skills/global/{action-enum,color-legend,paths}.md (from #01 study)
- skills/design-constraints/* (from #01 study)
- skills/mechanic-novelty/{taxonomy-of-25-games,prior-games-index-format,similarity-check,negative-similarity-check}.md (from #01 study)
- skills/code/id-generation.md (from #01 study)
- prior-games/index.md (75 prior generated games to avoid)

## Inputs reasoned over
- The 25-game taxonomy (rows from taxonomy-of-25-games.md)
- The 75-prior-games index — open hunting grounds: parabolic/arc trajectory targeting; height-gated 2D physics; oscillating-pendulum; rolling-ball physics; spring-elastic; tower-stacking; refraction; staircase elevation
- Heavily-covered families to avoid duplicating: tether/pulley/grapple, fold/mirror/reflect, beam/mirror/prism, gear/mesh, lever/balance, lock-drag, magnetism, polarity, ghost-replay, drift-impulse, gravity-tilt, pour/vessel, vine-grow, strand-twist, pickaxe-erode, walking-shape-cycle, fold/symmetry-reflect, line-sweep, pivot-rotate, totem-LOS, walk-trail-loop, majority-vote, L-jump, burden-load, vessel-equalize, fluvial-drift, duotone-flip, silhouette, rotor-sweep, flock-flee, hue-cross, ghost-playback, polarity-attract, anchor-pull, sokoban-explode, paint-canvas, stamp-paint, push-blocks, click-stamp.

## Candidate generation procedure
Walked the four allowed prior categories (objectness, basic geometry+topology,
basic physics, agentness) looking for a fresh combination. Underexplored
territory: continuous 2D arc trajectory with player-set range and barrier
clearance — none of the 25 references and none of the 75 priors exhibits a
*parabolic* trajectory through 2D space. Closest priors are linear (bx84
beam-mirror, vt6q grapple-anchor-yank, qn7w pulse-chain-eject), radial
(pf3w wavefront), or chain (vn8d domino, jx5k constellation-edge). None
arc.

Selected mechanic: **parabolic arc-launch with adjustable power, walking
launcher, blocking shields, and height-gated targets.**

## ID generation
Per code/id-generation.md procedure:
- Random 2-letter prefix: cv
- Random 2-char suffix: 5b
- Combined: `cv5b`
- Collision check vs 25 reference IDs: no match
- Collision check vs prior-games/index.md (75 entries): no match
- English-word check: not a word
- Verdict: ACCEPT

## Deliverables Produced
- mechanic-pick.md: id=cv5b, family=arc-launch-target, full description with
  4 taxonomy near-misses (cd82, bp35, r11l) and 6 prior-game near-misses
  (bx84, vt6q, qn7w, pf3w, lq5x, kn58) each with concrete distinguishing
  rules; negative-similarity-check vs bx84 (closest visual prior) scores 2/8
  shared dimensions, well below the 3-of-8 reject threshold.

## Notes
- Considered ~20 candidate families before settling. Most felt like marginal
  variants of existing priors (kf42→vh68 cautionary tale guided rejection of
  variants with shared sprite-cast or shared core dynamic).
- Parabolic-arc trajectory is a specifically fresh axis: every prior
  trajectory mechanic is linear (beam, grapple), chained (pulse-chain,
  domino-cascade), or radially-symmetric (wavefront). No prior projects a
  free-air 2D curve.
- Mechanic composition for L1/L2/L3 already mapped in mechanic-pick:
  base = walk + charge-cycle + arc-fire; L2 adds shield-blocks-arc (clearance
  required); L3 adds height-gated targets (apex-vs-target-elevation).

