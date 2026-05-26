# Step #02: pick_mechanic

## Inputs Consumed

- `workspace/study-notes.md` (from #01 study) — frequency tables, design moves, anti-patterns, open questions.
- Run input: NO seed provided (fully autonomous mode).
- `skills/mechanic-novelty/taxonomy-of-25-games.md` (cross-checked against all 25 rows).
- `skills/mechanic-novelty/similarity-check.md` (positive distinguishing-rule procedure).
- `skills/mechanic-novelty/negative-similarity-check.md` (the 8-dimensions test + cautionary tale).
- `prior-games/index.md` (1 prior: kf42 tether-pawn-cycle).
- `prior-games/kf42/{mechanism-detail.md, run-archive/smoke-frames/level_1.png, level_2.png}` (full visual + mechanic check).
- `skills/design-constraints/core-knowledge-priors.md` (the 4 allowed prior categories).
- `skills/design-constraints/forbidden-elements.md` (no clipart / cultural conventions).
- `skills/code/id-generation.md` (4-char ID constraints + collision list).

## Deliverables Produced

- `workspace/mechanic-pick.md`: 4-char ID `qz73`, family tag
  `radial-cycle-lock`, paragraph description, novelty rationale
  vs every taxonomy near-miss + vs the kf42 prior, with the
  8-dimensions negative similarity-check explicitly walked.

## Notes

- Brainstormed ~10 candidate dynamics before settling. Rejected:
  - Tetris-like falling-pieces (preexisting video game — axis-1 violation).
  - Lights-Out toggle / Conway-life / Match-3 (all preexisting).
  - Mirror / fold-symmetry (too close to ar25, cn04).
  - Marble-cascade / shelf-pour (too close to sp80, bp35).
  - Click-to-pull-fruits-radial (too close to su15).
  - Multi-avatar lockstep with mirrored axes (too close to m0r0, tu93).
- Settled on **radial dial-rotation** because it diverges from
  every prior on dimensions 1 (a radial structure is on the board,
  not a movable on a grid) and 8 (the core thinking is "where to
  lock + how many cyclic shifts" — a cyclic-permutation puzzle, not
  a navigation puzzle). It diverges from kf42 specifically on every
  one of the 8 negative-similarity dimensions.
- Kept the spoke pattern abstract (5 spokes, varied lengths, colour
  block on each tip) so the structure does NOT read as a clock face
  / cultural symbol per `forbidden-elements.md`.
- Chose `qz73` after manual generation: not English, no collision
  with the 25 reserved IDs nor with `kf42` in `prior-games/index.md`.
