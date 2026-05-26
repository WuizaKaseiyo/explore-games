# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, autonomous mode (no seed).
- skills/global/{paths.md, action-enum.md, color-legend.md} (from skills/global/): repo paths, action slots, palette 0..15.
- skills/conventions/from-tech-report.md (from skills/conventions/): soft design philosophy, exploration/modeling/goal-setting/planning pillars, RHAE scoring.
- skills/design-constraints/{core-knowledge-priors,forbidden-elements,composition-and-tutorial,checklist,difficulty-rules}.md: hard constraints, the L1/L2/L3 contract, the 16-check critique list.
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md: mechanic taxonomy of all 25 reference games, novelty rules, prior-games index schema.
- skills/mechanism-details/*.md (25 files): per-game mechanic essence, action mapping, level progression, internal state, code patterns.
- prior-games/index.md: 8 prior generated games — kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52.
- Reference source files (full reads): game_sources/cn04/65d47d14/cn04.py, game_sources/sp80/0ee2d095/sp80.py, game_sources/tu93/2b534c15/tu93.py.
- Prior-game level_1.png screenshots: gv47, hr8q, kf42, kx14, lq5x, ng52, qb84, qz73 — visual signatures sampled.

## Deliverables Produced
- workspace/study-notes.md: four required sections (cross-cut frequencies, recurring design moves, recurring anti-patterns, open questions for pick_mechanic). Three reference source files cited (cn04 for selection-then-manipulate idiom, sp80 for multi-phase animation/tilt, tu93 for 3-phase step machine and walkable-underlay collision).

## Notes
- Defensive workspace check passed (workspace was empty modulo .gitkeep).
- Discrepancy noted: task-overview.md cites "≥6 levels" from §3.4 but composition-and-tutorial.md authoritatively overrides to EXACTLY 3 levels. Used the override.
- Visual signature scan of the 8 priors shows dark-grey/grey backgrounds dominate — generated candidate must diverge on palette per negative-similarity-check.md Principle 2.
