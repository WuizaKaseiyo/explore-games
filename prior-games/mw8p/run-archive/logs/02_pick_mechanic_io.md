# Step #02: pick_mechanic

## Inputs Consumed
- `task-overview.md` (from #01 study): no seed; autonomous mode.
- `skills/design-constraints/core-knowledge-priors.md`: confirmed
  agentness + objectness usage; no physics/topology needed.
- `skills/mechanic-novelty/taxonomy-of-25-games.md`: walked 25 rows,
  flagged tu93 / ka59 / m0r0 as nearest taxonomy entries.
- `skills/mechanic-novelty/similarity-check.md`: applied the family /
  description / distinguishing-rule procedure for each near-miss.
- `skills/mechanic-novelty/negative-similarity-check.md`: walked the
  8-dimension grid against every prior near-miss; zk9p is the nearest
  prior at 4 shared coarse dims (D1/2/4/5) but all three principle
  dims (D6/7/8) diverge.
- `skills/mechanic-novelty/prior-games-index-format.md`: confirmed
  index schema for later finalize append.
- `prior-games/index.md` (80 rows): novelty bar; closest are zk9p,
  nf3z, ek73, jd4q, bw7k — all distinguished.
- `prior-games/` directory listing (80 in-progress / prior-game
  directories) checked for ID collision against `mw8p`.
- `skills/code/id-generation.md`: ID generation rules applied to
  produce `mw8p` (verified non-colliding, opaque, alphanumeric).
- `skills/mechanism-details/{tu93, ka59, m0r0, sb26, sp80, cn04,
  wa30}.md`: deep first-pass on the closest taxonomy entries.

## Deliverables Produced
- `mechanic-pick.md`: 4-char ID `mw8p`, family
  `predator-prey-triangle`, one-paragraph mechanic description,
  concrete distinguishing rules vs tu93 / ka59 / m0r0 / zk9p / nf3z /
  ek73, and the full 8-dimension negative-similarity-check walk vs
  zk9p with an explicit palette+pixel-grain divergence plan.

## Notes
- The negative-similarity-check shared-dim count vs zk9p is 4 (above
  the arithmetic threshold of 3). The check's own guidance is "the
  threshold is judgement, not arithmetic — sharing on dimensions 6, 7,
  or 8 is heavier than sharing on the others, because those are the
  named principles." All three principle dims (D6 palette, D7 pixel
  grain, D8 core dynamic) diverge, and the level goal (D3) also
  diverges. Accepted on the judgment-override clause; `critique_spec`
  will re-evaluate against the fleshed-out spec.
- Mechanic family selection rationale: agentness is one of the
  less-explored priors per `reference-game-patterns.md` § Open
  questions ("agentness shows up in ~6 of 25"). Cyclic
  three-way predation has no taxonomy or prior-games entry — zk9p is
  single-species, nf3z is shepherd-only, ka59 is single-chaser.
- Action mapping plan (defers to spec): `[1, 2, 3, 4]` only, no
  ACTION5/6/7. ACTION5 is the freedom slot but using it here would
  add a non-essential modal verb (the puzzle is rich without one).
  Per `action-enum.md`, omitting ACTION5 is fine; `tu93` and `ls20`
  also use `[1, 2, 3, 4]`.
