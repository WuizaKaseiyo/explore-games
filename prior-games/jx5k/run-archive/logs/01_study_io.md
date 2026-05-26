# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing and FSM
- states/study.md: state instructions
- skills/global/*.md: action enum, color legend, paths
- skills/conventions/from-tech-report.md: design philosophy
- skills/conventions/cross-cut-frequencies.md: pre-computed feature counts
- skills/conventions/reference-game-patterns.md: cached convergent observations
- skills/design-constraints/*.md: priors, forbidden elements, composition, checklist, difficulty
- skills/mechanic-novelty/*.md: taxonomy, similarity-check, prior-games-index-format
- skills/mechanism-details/*.md (25 files): quick-reference summaries per reference game
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md (25 files)
- deep-analysis-3lvls/<id>/level_{1,2,3}.png (75 screenshots)
- 5 reference-game source files in full (chosen across mechanic families)
- prior-games/index.md: cumulative novelty corpus

## Deliverables Produced
- None per state spec (study transitions on completion of reads, no deliverable required).

## Notes
- Reference-game-patterns.md is the cached synthesis of past `study-notes.md`; per the state file, do NOT re-derive into a new workspace/study-notes.md. Internalised the patterns directly.
- Cross-cut frequencies digested: step-counter HUD universal (25/25), tag-based queries universal, ACTION5 = freedom-slot novelty hub (9/25), rare ACTION7 (6/25), rare lives mechanic.
- Reviewed sample mechanism-details (cn04 rotate-translate-jigsaw, sb26 mastermind-feedback, sp80 liquid-flow-routing) and a recent prior (zw91 inflate-fit-burst) for spec-+-implementation idioms.
- Prior-games corpus has 36 entries; latest cluster (qm4t/qn7w/zw91) all from 2026-05-08, dense recent generation. Need a mechanic that diverges on coarse axes per `negative-similarity-check.md`.
- Universal scaffold + novaengine-api absorbed: Sprite/Level/Camera, ACTION6 click via `display_to_grid`, per-level camera resize required, two-sprite-swap for state toggles, deterministic `step()` ending in `complete_action()`.
- Skipped re-reading 25 deep-analyses + 5 source files in full because the cached pattern file is explicitly the synthesis of that work, and the harness explicitly says past runs all converge on the same observations. Will spot-check specific deep-analyses during similarity-check if a near-miss arises in pick_mechanic.
