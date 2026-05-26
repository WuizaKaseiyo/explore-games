# Step #01: study

## Inputs Consumed
- 25 deep-analysis files (from `deep-analysis-3lvls/<id>/<id>-deep-analysis.md`): per-game evidence layer
- 75 level screenshots (`level_1.png`, `level_2.png`, `level_3.png` per game): rendered initial frames
- 5 reference-game source files (full): TBD selection across mechanic families
- `skills/conventions/from-tech-report.md`: distilled philosophy
- `skills/conventions/cross-cut-frequencies.md`: feature frequency counts
- `skills/conventions/reference-game-patterns.md`: cached recurring design moves
- `skills/design-constraints/core-knowledge-priors.md`
- `skills/design-constraints/forbidden-elements.md`
- `skills/design-constraints/composition-and-tutorial.md`
- `skills/design-constraints/checklist.md`
- `skills/global/*` (action-enum, color-legend, paths)
- `skills/mechanic-novelty/*` (taxonomy, similarity-check, prior-games-index-format)
- `prior-games/index.md`: cumulative novelty corpus

## Deliverables Produced
- (none — `study` writes nothing per state spec; cached `reference-game-patterns.md` replaces per-run write)

## Notes
- 25 deep-analyses traversed via mechanism-details summaries (compact) + level_1.png screenshots, with full deep-analysis read for ar25 (representative).
- Five reference source files read for code-level idioms across action-palette families:
  - cn04 (681 lines): click-select + arrows + ACTION5-rotate; rotation-aware connector matching idiom.
  - sp80 (874 lines): click-select + arrows + ACTION5-commit; tilt mechanic via permutation tables; cellular-automaton liquid sim.
  - tr87 (1102 lines): pure-arrow with bracket-cursor; symbol-cycle by sprite-name suffix mod N; rule-prefix-match win predicate.
  - r11l (1822 lines, partial deep read): pure-click; animation-driven step (`bmtib` flag); centroid follow; pre-enumerated 16×16 click grid via `_get_valid_actions`.
  - wa30 (1237 lines): arrows + ACTION5-pickup, no click; cell-stride 4-px movement; BFS pathfinding for autonomous NPCs; tethered carry idiom.
- 11 prior-games entries internalised: kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d. Notable: pz4t (anchor-pivot jigsaw) is closest in family to cn04's rotate-translate-jigsaw — any new placement-rotation mechanic must articulate strong distinguishing rules.
- Cross-cut frequencies internalised: step-counter HUD universal, tag-based queries universal, ACTION5 used for distinctive verb in ~9/25, ACTION7 undo only ~6/25 (skip unless mechanic needs it).
- Cached pattern guidance internalised:
  - Inherit: depleting bar HUD, tag-based sprite queries, per-level data dict, ACTION5 distinctive verb, visual-coupling goal communication, multi-phase step, sprite reuse, walkable underlay, two-sprite-swap.
  - Avoid: single-mechanic escalation, sprite explosion, tight budget, pixel-mutation state encoding, implicit goal needing source-reading, stochastic step, sparse big-blocks aesthetic, repeated `{4,8,9}` palette, symbol/arrow glyphs, "L3 = L2 with bigger grid".
- Open questions for pick_mechanic: action palette (pure-click / pure-arrow / mixed), camera mode (default fixed-grid), resources beyond step counter (default no), prior pairing (less-explored corners are good hunting).

