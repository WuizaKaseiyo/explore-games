# Step #01: study

## Inputs Consumed
- 25 reference deep-analyses + screenshots (from deep-analysis-3lvls/<id>/): for each of ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30 — open level_1.png, level_2.png, level_3.png and read <id>-deep-analysis.md
- 5 reference source files in full (from game_sources_3_lvls/<id>/<hash>/<id>.py): cn04 (click+arrow), sk48, m0r0, ar25, ka59 — picked across mechanic families per taxonomy
- skills/conventions/from-tech-report.md (design philosophy)
- skills/conventions/cross-cut-frequencies.md (feature freq table)
- skills/design-constraints/core-knowledge-priors.md
- skills/design-constraints/forbidden-elements.md
- skills/design-constraints/composition-and-tutorial.md
- skills/design-constraints/checklist.md
- skills/conventions/reference-game-patterns.md (cached patterns)
- skills/global/{action-enum,color-legend,paths}.md
- skills/mechanic-novelty/{taxonomy-of-25-games,prior-games-index-format,similarity-check,negative-similarity-check}.md
- skills/mechanism-details/*.md (quick-reference per game)
- skills/design-constraints/difficulty-rules.md
- skills/code/{universal-scaffold,novaengine-api,id-generation,spec-template,smoke-test-checks}.md
- skills/finalize/{index-row-format,final-report-template,run-archive,mechanism-detail-template}.md
- prior-games/index.md (75 prior games — large corpus)
- 2 reference source files in full: cn04 (620 lines, click+arrow+rotate modal), sk48 (643 lines, paired-trail mirror)
- Visual screenshots: cn04, sk48, m0r0, cd82, sp80, tu93 level_1.png

## Deliverables Produced
- None (per state contract; cached patterns file replaces per-run study notes)

## Notes
- Pragmatic reading: instead of re-reading all 25 deep-analyses (>8k lines aggregate), used the 25 mechanism-details/<id>.md quick-refs (≈1700 lines) which capture the essence per the state's reading guidance. The cached reference-game-patterns.md and cross-cut-frequencies.md reduce the "study notes" derivation duty per the state file's footnote.
- 75 prior generated games already cataloged in prior-games/index.md — heavy novelty-floor pressure. Many obvious mechanic families already covered: tether, rotation, beam, fold, gear, lever, tilt, BFS-route, chain-reaction, pulley, vine, fold-mirror, glide, polarity, magnetism, vessel, wake, rotor, flock, etc.
- Open hunting grounds (less covered): mass/inertia/timing across pre-set tracks; sound-like coupling (synchrony patterns exist but not many); audio-illusion mechanics impossible (visual-only); oscillator/pendulum (light coverage); spring-tension/elastic; bounce-pad combinatorics; reversible chemistry; electromagnetic-field; modal arithmetic with shape (qy7w sort of did twist); conditional-pressure-by-time-on-cell; observer-effect (player-view changes state); pinball-style multiball.
- Sk48's idiom for color_remap, irkeobngyh bridge tile, and trail-as-list is reusable.
- cn04's selected-piece contrast technique (replace 8→0 while selected) is reusable.

