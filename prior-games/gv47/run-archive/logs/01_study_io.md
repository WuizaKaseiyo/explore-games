# Step #01: study

## Inputs Consumed
- task-overview.md: workflow framing, repo paths.
- skills/global/{paths,action-enum,color-legend}.md: action enum + 16-colour palette + path conventions.
- skills/conventions/from-tech-report.md: §3.4 design philosophy + 12-question gate.
- skills/design-constraints/{core-knowledge-priors,forbidden-elements,composition-and-tutorial,checklist,difficulty-rules}.md: priors, forbidden glyphs, 3-level structure, 16-item checklist, difficulty rules.
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md: 25-row mechanic taxonomy + similarity protocol + negative test + index schema.
- prior-games/index.md: 5 priors so far — kf42, qz73, kx14, qb84, lq5x.
- All 25 deep-analysis "Mechanic essence" / "Frequency-table contributions" sections under deep-analysis-3lvls/<id>/<id>-deep-analysis.md.
- Three reference-game sources read in full:
    - `sp80` (874 lines, click+arrow+modal): pour-shelf-route. Action subset [1,2,3,4,5,6]. State-machine in `step()` with "change" vs "spill" mode, pour attempts capped at 4, view rotation handled by remapping action ids in `lnqtlqefzv`.
    - `tu93` (1251 lines, arrow-only): maze-pickup-train. Action subset [1,2,3,4]. Big maze sprite `vhlesexlqd` with palette-2 corridors; `step()` cycles through phases 0/1/2 (move-then-resolve-followers-then-resolve-chasers), and the maze-step is a 3-cell hop guarded by `reqagoikbz.pixels[i, xjsopnydkp] == 2`.
    - `r11l` (1822 lines, click-only): centroid-puppet-leg. Action subset [6]. Single ACTION6 verb that either (a) selects a footprint, or (b) drags it to a location; centroid widget chases the average and an animated tween `tpjhojnaoa` runs across multiple `step()` invocations until `tjffy >= gfwuu`.
- Rendered initial frames (level_1.png) opened: cn04, sp80, tu93, sb26, sk48, tr87, lp85, cd82, ka59, m0r0, wa30, ls20, r11l, dc22 (reference); lq5x, qb84, kx14, qz73, kf42 (priors). Used to internalise palette range and pixel-grain breadth.

## Deliverables Produced
- workspace/study-notes.md: cross-cut frequencies (10 metrics quantified across 25 games), 8 recurring design moves with concrete source citations, 5 anti-patterns with reasoning, 4 open questions framing pick_mechanic.

## Notes
- Took the screenshot pass at ~14 reference games + 5 priors rather than all 75 — sufficient for visual-signature internalisation per the negative-similarity-check standard.
- Three full source reads cover the action-vocabulary spectrum: r11l (pure click), tu93 (pure arrows), sp80 (click+arrow+modal). Confirmed the multi-tick `step()` animation pattern is universal in games with mid-action animation.
- Five priors observed: kf42 sparse-pawn, qz73 hollow-rings-on-grey, kx14 split-tone tank, qb84 graph-of-pluses, lq5x dark+yellow-rings. The candidate must diverge palette AND board-content from these.
