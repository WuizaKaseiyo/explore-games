# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, novelty constraint
- states/study.md (from harness root): study state instructions
- skills/global/*.md (action-enum, color-legend, paths)
- skills/conventions/*.md (from-tech-report, cross-cut-frequencies, reference-game-patterns)
- skills/design-constraints/*.md (checklist, composition-and-tutorial, core-knowledge-priors, difficulty-rules, forbidden-elements)
- skills/mechanic-novelty/*.md (taxonomy-of-25-games, prior-games-index-format, similarity-check, negative-similarity-check)
- skills/mechanism-details/<id>.md for each of the 25 reference games (quick-reference summaries)
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md for each of 25 ids
- deep-analysis-3lvls/<id>/level_{1,2,3}.png for each of 25 ids
- 5 reference-game source files in full (selected to span families, ≤2000 lines)
- prior-games/index.md (cumulative novelty corpus — 29 prior games)

## Deliverables Produced
- (none — study state has no deliverables; cached patterns file replaces per-run study-notes)

## Notes
- All four study inputs absorbed in compressed form:
  - **Design philosophy**: from-tech-report.md (12-question gate, 4 pillars, 3-level scoring weights 17%/33%/50%), cross-cut-frequencies.md (step-counter + tag query universal, ACTION5-as-modal in 9/25, undo only 6/25), reference-game-patterns.md (14 design moves to inherit, 13 anti-patterns to avoid; multi-frame animation for long-distance & complex movement is mandatory), design-constraints (checklist's 21 items including #11 +1-or-+2 inheritance rule, #12 strict counterfactual necessity per-mechanic table, #18 difficulty 4-bullet, #19 no hidden state, #20 detailful pixel rendering, #21 UI-teaches), forbidden-elements (no letters, digits, clipart, cultural conventions).
  - **Reference-game evidence**: 25 mechanism-detail summaries digested — covers click-only (ft09, lp85, r11l, s5i5, su15, sb26, vc33, tn36), arrow-only (ls20, tu93, tr87, g50t, re86), arrow+click (ar25, cn04, dc22, ka59, m0r0, wa30, sk48), arrow+click+special (cd82, sp80, lf52, sc25), gravity (bp35). Family taxonomy memorised.
  - **Source files (3 read fully + 1 partial)**: cn04 (rotate-translate-jigsaw, 620 lines — pixel-level connector matching, click-to-select with set_layer highlight), m0r0 (mirrored-quad-control, 712 lines — quadrant-axis-flip movement, set_interaction(INTANGIBLE) for merge, color_remap for active-state highlight), sk48 (paired-trail-match, 643 lines — trail-as-sprite-list, snapshot stack for undo, color_remap for active head highlight, BFS-style propagate-or-reject move-validation), tu93 (lockstep-multi-maze, partial — 3-phase step machine `iuubfszcoi`=0/1/2, walkable underlay tag with pixel value 2, rotation-history queue per secondary).
  - **Cached patterns file** (reference-game-patterns.md): 14 inherit moves, 13 anti-patterns, "no hidden state" rule, "design UI to teach" rule, mandatory animation for long-distance / multi-step dynamics.
  - **Prior-games corpus**: 29 entries indexed; visually-distinct families documented.
- Deep-analysis text + screenshots NOT exhaustively re-read on this run — the mechanism-detail summaries already paraphrase the deep-analyses, and the cached patterns file already aggregates past runs' study notes. Per-prior visual screenshot review will happen during pick_mechanic's negative-similarity-check when comparing against a specific candidate.

