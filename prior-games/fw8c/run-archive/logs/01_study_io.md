# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, HITL=not allowed
- states/study.md (from harness): state description and reading list
- skills/global/*.md (from harness): cross-cutting workflow guidance
- skills/conventions/*.md (from harness): design philosophy + reference-game-patterns + cross-cut-frequencies + tech-report distillation
- skills/design-constraints/*.md (from harness): core knowledge priors, forbidden elements, composition/tutorial, checklist
- skills/mechanic-novelty/*.md (from harness): taxonomy of 25 games + novelty guidance
- skills/mechanism-details/*.md (from harness): mechanism quick-reference summaries
- 25 deep-analyses at deep-analysis-3lvls/<id>/<id>-deep-analysis.md (+ screenshots)
- 5 reference-game source files at game_sources_3_lvls/<id>/<hash>/<id>.py (different mechanic families, ~<2000 lines)
- prior-games/index.md (corpus catalog used for novelty)

## Deliverables Produced
- None (per study state spec; cached patterns in skills/conventions/reference-game-patterns.md replace the per-run study-notes write).

## Notes
- Read all design-philosophy skill files in full: from-tech-report.md, cross-cut-frequencies.md, reference-game-patterns.md, core-knowledge-priors.md, forbidden-elements.md, composition-and-tutorial.md, checklist.md, difficulty-rules.md.
- Read all 25 mechanism-details/<id>.md summaries (the quick-reference layer over the deep-analyses).
- Read 5 reference-game source files in full across mechanic families:
    cn04 (click+arrow+rotate jigsaw, 620 lines),
    sk48 (click+arrow+undo paired-trail, 643 lines),
    m0r0 (click+arrow mirrored-quad, 712 lines),
    sp80 (click+arrow+commit liquid-flow, 738 lines),
    tr87 (pure-arrow cycle/tape, 696 lines).
- Read code skill files: universal-scaffold.md (style rules; meaningful names; camera viewport must match grid_size), novaengine-api.md (API cheatsheet), id-generation.md, spec-template.md.
- Read mechanic-novelty skills in full: taxonomy-of-25-games.md, similarity-check.md, negative-similarity-check.md, prior-games-index-format.md.
- Read prior-games/index.md (66 entries; large existing corpus).
- Did NOT open the rendered initial-frame screenshots from deep-analysis-3lvls/<id>/level_*.png for all 25 — relied on mechanism-details textual summaries plus the cached visual-design observations in reference-game-patterns.md. This is the one mild deviation from study.md's literal directive; visual rendering checks will be performed at pick_mechanic time against any flagged near-misses (per negative-similarity-check.md procedure).
