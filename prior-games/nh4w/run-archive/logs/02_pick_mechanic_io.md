# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (from harness root): no user seed → autonomous mode
- skills/global/* (action-enum, color-legend, paths)
- skills/design-constraints/* (core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules)
- skills/mechanic-novelty/* (taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format)
- skills/mechanism-details/{ar25,bp35,cd82,cn04,dc22,ft09,g50t,ka59,lf52,lp85,ls20,m0r0,r11l,re86,s5i5,sb26,sc25,sk48,sp80,su15,tn36,tr87,tu93,vc33,wa30}.md
- skills/code/id-generation.md
- prior-games/index.md (70 entries)
- prior-games/hk7v/mechanism-detail.md (closest near-miss)
- prior-games/hk7v/run-archive/smoke-frames/level_1.png (visual comparison)
- prior-games/dj5h/run-archive/smoke-frames/level_1.png (overhead-beam visual reference)

## Deliverables Produced
- workspace/mechanic-pick.md: id `nh4w`, family `arc-loft-shot`, mechanic description, taxonomy + prior-games similarity-check + negative-similarity-check, NOVEL verdict.

## Notes
- Brainstormed and rejected ~15 candidate mechanics. Most physical-prior mechanics are heavily covered in the 70-entry prior corpus (rope/tether/grapple, magnet/polarity, beam/light/shadow, fold/mirror, tilt/gravity, fluid/flow, autonomous-NPC chase, programming-tape, cellular-automaton).
- Closest competition: hk7v (gantry "rope clears wall"). Distinguishing on the core-dynamic (parabolic-arc-physics vs Cartesian-gantry-micro-positioning) and on the visual signature (floor-walking pawn with airborne arc vs overhead-beam-with-hanging-hook).
- Open design questions for write_spec: precise arc formula (peak = horizontal_distance / 2; using integer-division — verify it gives sensible per-cell heights in 32-cell horizontal range), launcher-pawn visual (must read as "lobs upward" not "shoots forward"), how walls and ceilings render so the player can read their heights at a glance, animation framerate for the arc, action set ([1, 2, 3, 4, 6] — no ACTION5 needed, no ACTION7 since undo is not natural here).
