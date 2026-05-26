# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, notes, defensive workspace check
- states/study.md: study-state instructions
- skills/global/* (action-enum.md, color-legend.md, paths.md): project-wide conventions
- skills/conventions/from-tech-report.md: distilled NovaPlay design philosophy
- skills/conventions/cross-cut-frequencies.md: pre-computed feature frequencies across 25 games
- skills/conventions/reference-game-patterns.md: cached recurring design moves and anti-patterns
- skills/design-constraints/core-knowledge-priors.md
- skills/design-constraints/forbidden-elements.md
- skills/design-constraints/composition-and-tutorial.md
- skills/design-constraints/checklist.md
- skills/design-constraints/difficulty-rules.md
- skills/mechanic-novelty/taxonomy-of-25-games.md (for picking the 5 source-read targets)
- skills/mechanic-novelty/{similarity-check.md, negative-similarity-check.md, prior-games-index-format.md}
- skills/mechanism-details/<id>.md × 25: quick-reference summaries
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md × 25
- deep-analysis-3lvls/<id>/level_{1,2,3}.png × 25
- 5 chosen reference source files in full (see Notes after the work)
- prior-games/index.md (current corpus state for novelty awareness)

## Deliverables Produced
- None. Study state has no per-run deliverables (cached patterns + frequencies replace `study-notes.md`).

## Notes
- Five source files read end-to-end: cn04 (620), m0r0 (712), sb26 (827), wa30 (839), tu93 (1113). All within the ≤2000-line budget; span click-only (sb26), pure-cardinal (tu93, wa30), and click+arrow+modal (cn04, m0r0).
- Internalised 25 mechanism-detail summaries + 25 reference screenshots (L1 at minimum, plus L2/L3 for the 5 source-pick games and many reference highlights).
- Internalised cross-cut frequencies, reference-game-patterns, design philosophy skill files, taxonomy of 25 games, and similarity-check / negative-similarity-check protocols.
- Visited L1 frames for 14 of the 15 prior games to build visual sense of corpus drift; vn8d frames missing from disk.
- Key code idioms learned: pixel-overlap snap (cn04), 4-quadrant axis-flip lockstep (m0r0), tag-based BFS pathfinding for NPCs (wa30), animation-phase-counter state machine (sb26), 3-phase step (input → enemy tick → win/lose) (tu93).
- Open questions for pick_mechanic noted from reference-game-patterns §"Open questions": action palette, camera mode, beyond-step-counter resources, core-prior pairing.
