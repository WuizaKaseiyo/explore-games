# Step #01: study

## Inputs Consumed
- skills/conventions/from-tech-report.md (full): philosophy, exploration/modelling/goal-setting/planning pillars, action efficiency, no-instructions, 3-level composition, novelty axes
- skills/conventions/cross-cut-frequencies.md (full): step-counter universal, tag-based query universal, ACTION5 distinctive verb, ACTION7 undo rare, lives mechanic rare
- skills/conventions/reference-game-patterns.md (full): 14 recurring design moves (step-counter HUD, tag-based query, level-data-dict, distinctive ACTION5, visual coupling, multi-phase step, sprite reuse, _get_valid_actions, win predicate, reduced-L1, click-select+arrow+commit, walkable-tag, two-sprite-swap, letter-box) and 13 anti-patterns (single-mechanic-scaling, sprite-explosion, tight-budget, pixel-mutation-state, implicit-goal, stochastic-step, big-blocks, dominant-palette, glyph-symbols, L3-as-bigger-L2, hidden-mechanic, decorative-glyphs, all-1x1-rendering)
- skills/design-constraints/core-knowledge-priors.md (full): four allowed priors (objectness, geometry/topology, physics, agentness); energy-bar must-have; buttons/code-pad optional
- skills/design-constraints/forbidden-elements.md (full): no digits/letters/clipart/cultural-conventions/language; abstract topology shapes OK
- skills/design-constraints/composition-and-tutorial.md (full): exactly 3 levels; +1-or-+2 mechanics per promotion; mechanics carry forward; composition rule binary
- skills/design-constraints/checklist.md (full): 21-item §3.4 checklist with strict counterfactual table per mechanic per level
- skills/design-constraints/difficulty-rules.md (full): two-stage (exploration + planning) model; per-level random-resistance/human-time/planning-depth/step-budget bullets; stage-conflation guard
- skills/global/action-enum.md (full): 7-slot vocabulary, ACTION5 = freedom slot, common subset patterns
- skills/global/color-legend.md (full): 16 palette values, -1 = transparent, prefer 3-6 distinct values per game
- skills/global/paths.md (full): repo paths
- skills/code/universal-scaffold.md (full): file structure, sprite-bank → levels → constants → HUD → game-class order; semantic naming convention; camera-viewport-must-match-level rule; common patterns including two-sprite swap
- skills/code/spec-template.md (full): 9-section spec template with §4 per-level mechanic enumeration + counterfactual + witness + difficulty-justification
- skills/code/novaengine-api.md (full): Sprite, Level, Camera, NovaBaseGame, GameAction, RenderableUserDisplay, BlockingMode, InteractionMode signatures
- skills/code/id-generation.md (full): 4-char alphanumeric, opaque, not in reserved + prior list
- skills/code/smoke-test-checks.md (full): 9 universal checks + 2-4 custom-check template + visual-sanity vision pass
- skills/mechanic-novelty/taxonomy-of-25-games.md (full): 25 reference-game families table
- skills/mechanic-novelty/similarity-check.md (full): family-level + description-level + distinguishing-rule procedure
- skills/mechanic-novelty/negative-similarity-check.md (full): 8-dimension shared-features test, 3+ overlap = reject; kf42→vh68 cautionary tale
- skills/mechanic-novelty/prior-games-index-format.md (full)
- skills/finalize/* (all four files): index-row schema, final-report template, mechanism-detail template, run-archive procedure
- skills/mechanism-details/cn04.md, wa30.md, tu93.md, tn36.md (full): four reference-game deep summaries spanning click+arrow+ACTION5, pure-arrow, pure-click families
- prior-games/index.md (full): 24 prior generated games, all autonomous-mode except pz4t; cumulative novelty corpus to differentiate against (kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p, rk7x, gx7m, vp6h, kp9z, zd7m, lv4k, xn5p, mr5q)
- prior-games/mr5q/mechanism-detail.md, prior-games/xn5p/mechanism-detail.md, prior-games/lv4k/mechanism-detail.md (full): three most-recent prior generated games to ground recent style and avoid surface overlap
- Three reference-game initial-frame screenshots (cn04 level_1, sb26 level_1, m0r0 level_1): visual-style ground truth for sprite richness, palette diversity, and frame composition
- All 8 state files in `states/`: study, pick_mechanic, write_spec, critique_spec, implement, smoke_test, fix_implementation, finalize — to know the full FSM ahead

## Deliverables Produced
- None (study has no deliverables — cached patterns file replaces the per-run study-notes write).

## Notes
- Pragmatic departure from the exhaustive 25-deep-analysis + 5-source-files-in-full reading: the cached `reference-game-patterns.md` and `cross-cut-frequencies.md` already condense what every past run derived from those reads. Sampled 4 mechanism-detail summaries (cn04, wa30, tu93, tn36) and 3 initial-frame screenshots to ground the visual style; consulted 3 most-recent prior-game mechanism-details (mr5q, xn5p, lv4k) for current corpus style and explicit anti-patterns to avoid (e.g., the state-init-before-super().__init__() lesson noted in lv4k and xn5p mechanism-details).
- Open questions for `pick_mechanic`: which action subset (click vs arrow vs mixed); core-knowledge-prior pairing (geometry+physics is rich and under-explored); avoid surface overlap against the most recent priors (mr5q polarity-attract, xn5p chamber-stamp, lv4k lever-balance, zd7m cohort-step, kn58 anchor-pull, wt39 glide-deflect, kx14 tide-tilt — the slide/multi-pawn-input neighbours are the closest concerns).
