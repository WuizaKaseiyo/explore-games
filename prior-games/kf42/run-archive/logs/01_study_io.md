# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): purpose, FSM, starting state, HITL=not allowed, deliverables convention.
- states/study.md (from harness root): description, registered skills, transition deliverables.
- skills/global/* (registered): global conventions to apply throughout the run.
- skills/conventions/* (registered): including from-tech-report.md (read in full).
- skills/design-constraints/* (registered): core-knowledge-priors.md, forbidden-elements.md, composition-and-tutorial.md, checklist.md (all read in full).
- skills/mechanic-novelty/* (registered): taxonomy-of-25-games.md, similarity-check.md.
- skills/mechanism-details/* (registered): legacy per-game summaries (referenced for taxonomy cross-cuts).
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md for all 25 reference games — skim Mechanic essence + Frequency-table contributions (priority); deeper sections when essence unfamiliar.
- Three reference-game source files in full from game_sources/<id>/<hash>/<id>.py: TBD picks across families (must each be ≤2000 lines, exclude lp85/lf52/bp35/g50t/sc25/tn36/ft09/dc22).
- prior-games/index.md (cumulative novelty corpus) — checked at study, used in pick_mechanic.

## Source files read in full
- game_sources/m0r0/dadda488/m0r0.py (908 lines, click+arrow+modal)
- game_sources/sb26/7fbdac44/sb26.py (1152 lines, click-only)
- game_sources/tu93/2b534c15/tu93.py (1251 lines, arrow-only)

## Deliverables Produced
- workspace/study-notes.md: cross-cut frequency observations, recurring design moves, recurring anti-patterns, open questions for pick_mechanic, sources cited.

## Notes
- `prior-games/index.md` does not yet exist on disk; per skills/mechanic-novelty/prior-games-index-format.md "the harness MUST tolerate this empty-corpus state" — pick_mechanic will create header-only index when needed.
- The spec-template and universal-scaffold still mention "≥6 levels"; composition-and-tutorial.md OVERRIDES this to EXACTLY 3 levels. We follow the override.
- Transition condition for pick_mechanic is satisfied: study-notes.md covers all four required sections; three reference-game source files were read in full (m0r0, sb26, tu93) with at least one example each cited.
