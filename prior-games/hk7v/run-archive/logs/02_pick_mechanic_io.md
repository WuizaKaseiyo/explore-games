# Step #02: pick_mechanic

## Inputs Consumed
- skills/global/* (from prior-state memory)
- skills/design-constraints/* (from prior-state memory)
- skills/mechanic-novelty/taxonomy-of-25-games.md (from #01 study)
- skills/mechanic-novelty/similarity-check.md (from #01 study)
- skills/mechanic-novelty/negative-similarity-check.md (from #01 study)
- skills/code/id-generation.md (newly-read this state)
- prior-games/index.md (from #01 study)
- skills/mechanism-details/cn04.md (from #01 study)
- run input: no seed (autonomous mode)

## Deliverables Produced
- mechanic-pick.md: id `hk7v`, family `overhead-trolley-hook`,
  one-paragraph description, distinguishing rules vs the 6 closest
  taxonomy/prior entries (wa30, dj5h, vt6q, nb6t, wb6n, pv5q), and
  composition preview.

## Notes
- Picked autonomously (no seed). The crane/gantry dynamic (Cartesian
  X/Y with rope-clearance constraint and release-gravity stacking) is
  unrepresented in the prior corpus. Closest neighbour `wa30` shares
  only the abstract "deliver objects to colour-matched targets" goal,
  but differs on 6 of the 8 negative-similarity dimensions.
- Considered and rejected: gravity-flip (collides with `tg6w`),
  cellular-automaton-walk (`mz6t`), tower-balance (`lv4k`),
  pegs-through-holes (real-world clipart), Tetris-drop (preexisting
  video game), domino-fuse (`vn8d`).
- Action subset `[1,2,3,4,5]` deliberately omits ACTION6 (no click —
  all manipulation is positional via trolley/hook) and ACTION7
  (per checklist 22, no meaningful undo so omit rather than overload).
