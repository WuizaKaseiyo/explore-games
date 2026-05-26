# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, notes, prior-games corpus rules
- states/study.md (from harness root): state description specifies 4 reading inputs
- skills/global/* (registered): action-enum, color-legend, paths
- skills/conventions/from-tech-report.md, cross-cut-frequencies.md, reference-game-patterns.md
- skills/design-constraints/* : core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules
- skills/mechanic-novelty/* : taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format
- skills/mechanism-details/<id>.md (25 quick-ref summaries)
- prior-games/index.md (cumulative novelty source-of-truth)
- 25 deep-analysis markdown files at deep-analysis-3lvls/<id>/<id>-deep-analysis.md
- 25 × 3 level screenshots at .../deep-analysis-3lvls/<id>/level_{1,2,3}.png
- Five reference-game source files in full from game_sources_3_lvls/<id>/<hash>/<id>.py

## Deliverables Produced
- None (state has no deliverables; cached patterns file replaces per-run study-notes).

## Notes
- 60 prior games in `prior-games/index.md`. Novelty bar is high; many obvious mechanic families exhausted.
- 5 source files dispatched in parallel via Explore agents to fit context budget — returned tight architectural summaries. Files: cn04 (click+arrows+ACTION5 rotate), sk48 (full keyboard, undo via state-snapshot stack), sb26 (click + ACTION5 commit + ACTION7 undo, phase-tick marker walk), m0r0 (arrows + click, mirror-axis movement on quadrant), sp80 (click-grab + arrow-slide + ACTION5 pour, multi-frame water animation).
- Key code idioms now anchored: phase-tick step() (return without complete_action() during animation), `RenderableUserDisplay.render_interface(frame)` painting frame[0,:] or frame[63,:], sprite tag-based queries via `level.get_sprite_at(gx,gy,tag)` and `level.get_sprites_by_tag(...)`, `camera.display_to_grid(int(x), int(y))` for ACTION6 click coords, `level.get_data(key)` for per-level params, `sprite.color_remap(None, c)`, `set_interaction(InteractionMode.INTANGIBLE)`, `set_layer(n)`, `set_position(x,y)`, `rotate(90)`, `try_move_sprite(...)`.
- Surveyed prior-games families to identify unused / under-explored mechanic territory (see pick_mechanic).
- Transition condition met: all four reading inputs done. Proceeding to pick_mechanic.
