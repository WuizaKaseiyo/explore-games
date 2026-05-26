# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing & FSM
- states/study.md (from harness root): study state instructions
- skills/global/action-enum.md, color-legend.md, paths.md (from skills/global)
- skills/conventions/from-tech-report.md, cross-cut-frequencies.md, reference-game-patterns.md
- skills/design-constraints/core-knowledge-priors.md, forbidden-elements.md, composition-and-tutorial.md, checklist.md, difficulty-rules.md
- skills/mechanic-novelty/taxonomy-of-25-games.md, similarity-check.md, negative-similarity-check.md, prior-games-index-format.md
- skills/mechanism-details/<25 game IDs>.md (quick-reference summaries)
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md for all 25 reference games + level_1.png/level_2.png/level_3.png screenshots
- 5 reference-game source files in full (selected to span families, ≤2000 lines each)
- prior-games/index.md (cumulative novelty corpus from prior runs — 60 prior games)
- Sample of prior-games + reference smoke screenshots (kj82, pv5q L1; m0r0 L1) for negative-similarity grounding

## Deliverables Produced
- None (per state spec — `reference-game-patterns.md` replaces the legacy `study-notes.md` write).

## Notes
- Universal scaffold + novaengine-api fully internalised; subagent summarised cn04/ls20/m0r0/sk48/wa30 sources for idiom anchoring (in foreground transcript).
- Prior-games corpus is dense (60 entries) — novelty is the primary risk for pick_mechanic.
- Critical conventions noted: HUD step counter universal (25/25), tag-based sprite querying universal, `available_actions` always a minimal subset, ACTION7 strict-undo-only, ACTION5 is the freedom-slot for novelty.
- L1 may legitimately have multiple interacting mechanics ("base dynamic system"); L2 adds 1 or 2 new mechanics, L3 adds 1 or 2 more, all carry-forward and required.
- Anti-patterns to avoid: low-resolution chunky upscaling, 4-wall + 8-red + 9-blue palette (kf42 cautionary tale), big-blocks-on-empty-field, single-mechanic scaling, hidden state without persistent visual cue.
- Run input: no user seed → autonomous mode; pick mechanic without user mechanic preference.

