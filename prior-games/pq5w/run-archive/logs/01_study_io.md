# Step #01: study

## Inputs Consumed
- skills/global/* (action-enum, color-legend, paths)
- skills/conventions/from-tech-report.md (12-question gate)
- skills/conventions/cross-cut-frequencies.md (frequency table)
- skills/conventions/reference-game-patterns.md (cached patterns)
- skills/design-constraints/core-knowledge-priors.md
- skills/design-constraints/forbidden-elements.md
- skills/design-constraints/composition-and-tutorial.md (3-level rule, +1-or-+2 rule)
- skills/design-constraints/checklist.md (22 items)
- skills/design-constraints/difficulty-rules.md (per-level four bullets)
- skills/mechanic-novelty/taxonomy-of-25-games.md
- skills/mechanic-novelty/similarity-check.md
- skills/mechanic-novelty/negative-similarity-check.md
- skills/mechanic-novelty/prior-games-index-format.md
- skills/code/* (universal-scaffold, novaengine-api, spec-template, id-generation, smoke-test-checks)
- skills/finalize/* (templates and run-archive)
- skills/mechanism-details/cn04.md, sp80.md (canonical click+arrow+ACTION5 and pure-arrow phase-tick patterns)
- game_sources_3_lvls/cn04/65d47d14/cn04.py (full source — anchored on pixel-level snap, _get_valid_actions gating, RenderableUserDisplay HUD)
- prior-games/index.md (67 prior generated games — large novelty pressure)
- prior-games/rt9k/rt9k.py (canonical recent generated-game style — meaningful names, level functions, single Camera widget)

## Notes
- 67 prior games is a heavy novelty floor. Mechanics already covered: pawns + targets, color/tone cycles, mirror/fold games, fluid/vessels, sokoban variants, snake-trail, portal-trail (jd4q), warp-pads (ek73), lever, wave/timing, beam-reflect, gear-mesh, lighthouses, pickle-cycle, cubed-rolling, grain-cascade, grapple, fold-pair, pivot-rotate, etc.
- Identified candidate: PORTAL-PAIR with RELOCATE — 2 fixed teleport endpoints; ACTION5 drops the most-recently-used portal at avatar's current cell. Distinguishes from jd4q (trail-based, consumed-on-teleport) by being a persistent pair-with-relocation. Distinguishes from ek73 (warp-pads-as-aux) by being the primary verb.
- Picked ID: pq5w (not in 25 reference set, not in prior-games index, not an English word).
