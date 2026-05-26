# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing & FSM
- states/study.md (from harness): four-part reading list
- skills/global/* (from harness): action enum, color legend, paths
- skills/conventions/* (from harness): from-tech-report, cross-cut-frequencies, reference-game-patterns
- skills/design-constraints/* (from harness): checklist, composition-and-tutorial, core-knowledge-priors, forbidden-elements, difficulty-rules
- skills/mechanic-novelty/* (from harness): taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format
- skills/mechanism-details/<id>.md for the 25 reference games (from harness)
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md for 25 games (deep analysis text)
- deep-analysis-3lvls/<id>/level_1..3.png for 25 games (rendered screenshots)
- 5 reference game source files in full (selected to span families, <2000 lines each)
- prior-games/index.md (cumulative corpus index)

## Deliverables Produced
- (none — study state has no deliverables; cached `skills/conventions/reference-game-patterns.md` replaces the per-run study-notes write)

## Notes
- Read all 4 design-constraint skill files, 4 conventions files, 4 mechanic-novelty files, 3 global skill files.
- Read all 25 mechanism-detail summaries (the quick-reference layer).
- Read cn04 source in full as the anchoring implementation reference (click-select + arrow-move + ACTION5-rotate template, including the `_get_valid_actions` gating pattern, the rotation-aware connector match registry, the depleting-bar HUD pattern, and the `qdcvayjdkm` RenderableUserDisplay scaffold).
- Sampled L1 screenshots: cn04 (click-select rotate-fit jigsaw pieces with 8-coloured nubs on cyan), tu93 (small dense grey-tile maze with single blue 3-cell pawn and green exit), sp80 (orange playfield with blue shelf above two yellow U-cups, a magenta spout, green top edge — water-pour mechanic).
- Index has 81 prior games; some untracked subdirs under prior-games/ likely from in-flight runs (gh4r, hp9c, lz7q, qd6n, tc8s, tx4q, vk6m, vw3p, xv4n) — treat the on-disk index.md as source of truth for novelty.
- Internalised key patterns from `reference-game-patterns.md`: step-counter HUD universal; ACTION5 = identity verb; sprite-tag query API; multi-phase step() with phase-tick sentinels for animations; reduced state space at L1; visual coupling not symbols; no hidden state cue.
- Open questions for pick_mechanic: action palette, camera mode, resources beyond step counter, prior-pairing. Less-explored corners flagged in patterns.md as candidate hunting grounds.
