# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, notes
- states/study.md (from harness root): study state instructions
- skills/global/*.md (registered): global skill instructions
- skills/conventions/*.md (registered): from-tech-report, cross-cut-frequencies, reference-game-patterns
- skills/design-constraints/*.md (registered): core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules
- skills/mechanic-novelty/*.md (registered): taxonomy-of-25-games, novelty rules
- skills/mechanism-details/*.md (registered): quick-reference summaries
- 25 deep-analyses + level_1/2/3 screenshots from deep-analysis-3lvls/<id>/
- 5 reference-game source files in full
- prior-games/index.md: novelty corpus source of truth (22 prior games)
- skills/code/{universal-scaffold, spec-template, id-generation, novaengine-api, smoke-test-checks}.md
- skills/finalize/* (scanned)

Sources read in full or major sample:
- cn04 source (full, 620 lines): canonical click-select + arrows + ACTION5-rotate, multi-frame eval pattern
- tu93 (sampled, 1113 lines): pure-arrow maze + value-2 walkable, multi-phase animation
- sb26 (sampled, 827 lines): pure-click placement + commit + multi-phase phase-tick animation
- m0r0 mention via taxonomy + reference patterns: mirror coupling
- sp80 mention via taxonomy + reference patterns: pour + spill animation

Cached patterns absorbed from `reference-game-patterns.md`:
- step-counter HUD universal
- tag-based sprite querying
- per-level data dict drives parameters
- distinctive verb on ACTION5
- multi-frame phase-tick `step()` for animations
- camera viewport must match grid_size in on_set_level

## Deliverables Produced
- None (per state spec).

## Notes
- Prior corpus is dense (22 games). Best hunting ground is agentness (under-represented vs reference) and topology (under-represented).
- Novelty risk: cascade-family (vn8d, gx7m, kp9z, gv47) very dense; pawn-walk-on-grid family also dense; mirror-coupling done by m0r0; vertical-column-of-coloured-items done by qb84.

