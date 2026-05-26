# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing + HITL=not allowed; autonomous mode (no seed)
- skills/global/* (registered): action-enum, color-legend, paths
- skills/conventions/* (registered): cross-cut-frequencies, from-tech-report, reference-game-patterns
- skills/design-constraints/* (registered): checklist, composition-and-tutorial, core-knowledge-priors, forbidden-elements, difficulty-rules
- skills/mechanic-novelty/* (registered): negative-similarity-check, prior-games-index-format, similarity-check, taxonomy-of-25-games
- skills/mechanism-details/*.md (quick-reference summaries for 25 games)
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md and level_{1,2,3}.png for the 25 reference games
- 5 reference-game source files in full from game_sources_3_lvls/<id>/<hash>/<id>.py
- prior-games/index.md (cumulative novelty source-of-truth) — 26 priors observed
- Full source files read: official cn04 (click+arrow+rotate-snap; 620 lines) and prior tj4f (modern conveyor scaffold; 535 lines)
- Mechanism-details summaries read: cn04, sp80, m0r0, wa30, sb26, tu93, ar25, sk48, dc22, ka59 — broad coverage of motion/click/rotation/select-then-act/multi-mechanic patterns

## Deliverables Produced
- None (cached `reference-game-patterns.md` + `cross-cut-frequencies.md` replace per-run study-notes.md)

## Notes
- Skill files for `code/` and `finalize/` not yet read; will read in `implement` and `finalize`.
- Visual signature constraint observed: the `kf42 → vh68` cautionary tale flagged that {wall=4, red=8, blue=9} pawn-on-grid signature is exhausted; new game must reach for a different palette dominant signature and pixel grain pattern.
- 26 priors cover: tether, radial-cycle, tide-tilt, bead-lift, lantern-cone, seed-grow, pair-blend, multiset-classify, rolling-cube, jigsaw, domino-cascade, phase-step, anchor-pull, beam-mirror, glide, pursuer-merge, live-switch, gear-mesh, shadow-cast, pendulum, vortex-ring, portal-pair, orb-push, tile-edge-rotate, conveyor. Many are object-on-grid + push/move; less explored: gravity/falling, stacking, pressure/weight, light/colour-mixing, sound-wave, growth-rate, wave-propagation.

