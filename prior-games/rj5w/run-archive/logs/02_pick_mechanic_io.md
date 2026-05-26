# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (from harness root): seed input is empty → autonomous mode
- skills/code/id-generation.md: 4-char rules
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md
- skills/mechanism-details/{ar25,cn04,m0r0,lp85,vc33,sk48,bx84}.md (closest near-misses for the candidate)
- skills/conventions/reference-game-patterns.md (open-questions list to resolve)
- prior-games/index.md (full 36-row registry) + prior-games/fb7t/metadata.json (unindexed 37th)
- 8 reference screenshots (cn04, sp80, m0r0, lp85, wa30, sb26, tu93, cd82) for visual signature comparison
- 3 prior-game smoke screenshots (qm4t, zw91, nb6t)

## Deliverables Produced
- mechanic-pick.md (one-paragraph description of `axis-fold-mirror`, ID `rj5w`, full positive- and negative-similarity-check tables, action subset, prior coverage, open issues for write_spec).

## Notes
- Autonomous mechanic chosen: **paper-folding reflection** — the player
  positions a fold-line cursor along the playfield and commits; the
  shorter half flips onto the longer, teleporting pawns to mirrored
  positions. Composition: L1 vertical-only fold; L2 adds horizontal
  fold; L3 adds anchor walls + burn cells.
- ID `rj5w` chosen; not in 25-game reserved list, not in
  prior-games/index.md, not English, opaque.
- ID-generation collision check: scanned full prior-games/ directory
  (incl. unindexed fb7t).
- Both the positive `similarity-check.md` test and the negative
  `negative-similarity-check.md` test pass. The closest near-miss is
  `ar25` (shape-mirror-cover); the distinguishing rule is that ar25
  uses static mirrors and pieces co-exist at both real and reflected
  positions, while `rj5w` reflects pawns discretely on commit and
  pawns never co-exist at both spots.
- Action subset finalised as `[1, 2, 3, 4, 5, 6]`.
