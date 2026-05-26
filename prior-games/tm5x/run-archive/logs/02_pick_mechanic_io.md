# Step #02: pick_mechanic

## Inputs Consumed
- mechanic-pick.md does not yet exist (this run)
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md (already read in study)
- skills/code/id-generation.md (newly read this state)
- prior-games/index.md (29 entries; cumulative novelty corpus)
- skills/mechanism-details/<id>.md (25 reference summaries; already read in study)
- L1 screenshots opened for negative-similarity check: pf3w, kp9z, gv47, fz5j, mr5q, vd3g priors
- skills/global/action-enum.md (re-confirmed for ACTION5 freedom slot guidance)

## Deliverables Produced
- workspace/mechanic-pick.md: mechanic family `thermal-diffusion-blend`,
  game_id `tm5x`, full description, similarity check vs 25-game
  taxonomy + 29-prior-games corpus, negative-similarity 8-dimension
  walk against pf3w/kp9z/gv47/vd3g (closest near-misses), action
  palette `[1,2,3,4,5]`, palette plan, per-level composition outline
  (L1 walk-and-stamp; L2 + polarity toggle; L3 + insulator walls).
  All checks pass — verdict NOVEL.

## Notes
- Picked thermal-diffusion-blend because it occupies an unexplored
  corner: integer-scalar field that smooths via averaging on every
  tick. Distinct verb from every prior:
  pf3w wavefront = boolean BFS frontier, click+ACTION5;
  kp9z grain = threshold-topple, click;
  gv47 seed = boolean region growth, click;
  vd3g valley = gravity flow, click;
  mr5q polarity = pawn locomotion-on-attraction, click+ACTION5.
- Action set [1,2,3,4,5] is intentionally arrow+ACTION5 only — gives
  visual + verb distinctness from the click-heavy near-misses.
- ID `tm5x` is opaque, lowercase, alphanumeric, not a word; verified
  non-colliding against the 25 reserved + 29 prior IDs.
- All four required reading inputs from previous state digested.
- No seed provided by user → autonomous mode.
