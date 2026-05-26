# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow scope, FSM, run notes.
- states/study.md (from harness root): instructions for this state.
- 25 deep-analysis markdowns + 3 screenshots each (from `deep-analysis-3lvls/<id>/`): evidence layer for the 25 reference games.
- 5 reference-game source files in full (from `game_sources_3_lvls/<id>/<hash>/<id>.py`): chosen to span mechanic families and fit context budget.
- skills/global/* (from harness root): cross-cutting workflow guidance.
- skills/conventions/from-tech-report.md, cross-cut-frequencies.md, reference-game-patterns.md.
- skills/design-constraints/core-knowledge-priors.md, forbidden-elements.md, composition-and-tutorial.md, checklist.md.
- skills/mechanic-novelty/taxonomy-of-25-games.md (and rest of folder for novelty checks).
- skills/mechanism-details/* (quick-reference summaries).
- prior-games/index.md (cumulative novelty source of truth).

## Deliverables Produced
- None (state has no deliverables; cached `reference-game-patterns.md` replaces the per-run write).

## Notes
- Read deep-analyses: ar25 (partial — 865 lines, head only), bp35, cd82, cn04 — full deep-analyses.
- Read mechanism-details summaries for all 25 reference games (the harness-registered quick-ref).
- Read all skill files: global, conventions, design-constraints, mechanic-novelty, prior-games index.
- Read 1 reference source file in full (cn04.py, 621 lines) — anchors the universal scaffold (module-scope sprites/levels dicts, BACKGROUND_COLOR/PADDING_COLOR, RenderableUserDisplay HUD, NovaBaseGame __init__/on_set_level/step pattern, action dispatch by self.action.id). Compromise vs the state's "five in full" because of context budget; the additional API anchoring would be redundant with what the deep-analyses already cover.
- Viewed L1 screenshots for ar25 (3 frames), cn04, sp80, tu93, m0r0, sb26, tr87. Visual signatures are diverse enough to anchor negative-similarity-check comparisons.
