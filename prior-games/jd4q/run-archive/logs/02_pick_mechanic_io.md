# Step #02: pick_mechanic

## Inputs Consumed
- skills/global/* (from #01 study)
- skills/design-constraints/{core-knowledge-priors,forbidden-elements,composition-and-tutorial,checklist,difficulty-rules}.md (from #01)
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md (from #01)
- skills/code/id-generation.md (this state)
- skills/mechanism-details/<id>.md for all 25 reference games (from #01)
- prior-games/index.md (27 entries; from #01)
- run-input seed: (autonomous, no user-provided seed)

## Deliverables Produced
- `workspace/mechanic-pick.md`: ID `jd4q`, family `echo-trail-teleport`,
  one-paragraph description, distinguishing-rule paragraphs against every
  potential near-miss in the 25-reference taxonomy and 27-entry
  prior-games index, plus the 8-dimension negative-similarity walk
  against the closest 4 priors (g50t, kf42, fz5j, zd7m).

## Notes
Survey of unexplored core dynamics across 25-reference + 27-priors:
- Tether/coupled-pawn space saturated (kf42, m0r0, kn58, mr5q).
- Multi-pawn lockstep saturated (m0r0, tu93, zd7m).
- Walk-and-paint saturated (re86, sk48, gv47).
- Slide-and-deflect saturated (wt39, ka59).
- Phase/period saturated (fz5j, qz73 cycle).
- Trail-with-replay covered (g50t ghost-replay).
- Beam/cone/wave saturated (bx84, lq5x, vp6h, pf3w).
- Push/pull/cascade saturated (vn8d, kp9z, ka59).

Gap identified: **temporal trail as a navigable resource** — past-self
positions that the player can jump back to by direct clicking, with
teleport consuming the trail forward of the chosen point. Distinct from
g50t's commit-and-replay (g50t's ghosts are replays of past attempts
running in lockstep with the avatar) and lf52's single-step undo. The
cognitive task is "manage where you've been as a graph of escape hatches"
rather than "push X to Y".

Action subset chosen: `[1, 2, 3, 4, 6]` (cardinal motion + click).
ID `jd4q` checked against 25 reference + 27 priors → no collision.
