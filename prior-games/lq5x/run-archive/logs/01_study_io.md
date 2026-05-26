# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): autonomous run, no seed; ≥6 levels in source spec is overridden by skills/design-constraints to exactly 3 levels per generated game.
- prior-games/index.md (cumulative novelty floor): 4 prior rows — kf42 (tether-pawn-cycle), qz73 (radial-cycle-lock), kx14 (tide-tilt-buoyant), qb84 (bead-lift-swap).
- prior-games/{kf42,qz73,kx14,qb84}/mechanism-detail.md (per-prior deep view for novelty work).
- prior-games/{kf42,qz73,kx14,qb84}/run-archive/smoke-frames/level_1.png (visual signatures of all four priors).
- skills/global/{action-enum,color-legend,paths}.md.
- skills/conventions/from-tech-report.md (the 12-question philosophy gate).
- skills/design-constraints/{checklist,composition-and-tutorial,core-knowledge-priors,forbidden-elements}.md (hard rules: 16-check + difficulty floor/ceiling + one-new-mechanic-per-level + 3-level cap).
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md (positive + negative similarity tests).
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md — Frequency-table contributions section for all 25 reference games (collated via shell into cross-cut counts).
- deep-analysis-3lvls/<id>/level_1.png for cn04, sp80, tu93, ar25, sb26, lp85, ka59, m0r0, wa30, sk48, cd82, r11l, dc22, ls20, ft09, tn36 (visual signature sample across mechanic families).
- game_sources/cn04/65d47d14/cn04.py (681 lines, full read) — click+arrows+ACTION5 game; the canonical example of `_get_valid_actions` overrides, RenderableUserDisplay subclass HUD, level-data dict for per-level knobs.
- game_sources/sp80/0ee2d095/sp80.py (874 lines, full read) — click+arrows+ACTION5 with state-machine animation phases; tag-heavy queries; viewport rotation level-data.
- game_sources/tu93/2b534c15/tu93.py (1251 lines, key-section read) — pure-arrow `[1,2,3,4]` with phase-machine inside step() and dense tag-based queries.

## Deliverables Produced
- workspace/study-notes.md: covers all four required sections — cross-cut frequency observations (25-game tally), recurring design moves (8 patterns to inherit), recurring anti-patterns (5 anti-patterns to avoid), open questions for pick_mechanic (action-set shape, what is on the board, second failure axis, core dynamic). Cites all three full-source reads explicitly.

## Notes
- The `composition-and-tutorial.md` 3-level override and the `checklist.md` "exactly one new mechanic per level promotion" rule are the load-bearing structural constraints for the next state. The harness wins/loses on whether L2 demands non-trivial planning and L3 demands strictly deeper sequencing where order matters.
- Defensive workspace check: `find workspace -type f ! -name '.gitkeep' ! -path '*/logs/*'` returned no output, so no leftover state from a previous run.
- All four priors share "small discrete coloured sprites against a flat background" as the visual macro-shape. Reaching for a non-pawn-on-grid topology (canvas, ribbon, tape, stack, drawable surface) is the cleanest way to satisfy the negative-similarity test.
- Three priors (kf42, kx14, qb84) all use ACTION6 click + arrows; qz73 uses ACTION5 + ACTION6. None of the priors uses pure-arrow `[1,2,3,4]` or any subset including ACTION7 undo. Action-set shape is one of the cheapest divergence axes.
- The transition condition for `pick_mechanic` (study-notes.md present + 4 sections covered + 3 sources cited) is satisfied. Proceeding.
