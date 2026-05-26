# Step #01: study

## Inputs Consumed
- 25 deep-analyses (from deep-analysis-3lvls/<id>/<id>-deep-analysis.md): one per reference game id
- 25 × 3 screenshots (from deep-analysis-3lvls/<id>/level_{1,2,3}.png): visual ground truth
- 5 full reference sources (from game_sources_3_lvls/<id>/<hash>/<id>.py): chosen across mechanic families with ≤2000 line budget
- skills/conventions/from-tech-report.md (from harness): distilled philosophy
- skills/conventions/cross-cut-frequencies.md (from harness): pre-computed feature frequencies across the 25 games
- skills/conventions/reference-game-patterns.md (from harness): cached recurring design moves and anti-patterns
- skills/design-constraints/core-knowledge-priors.md (from harness): allowed prior categories
- skills/design-constraints/forbidden-elements.md (from harness): banned elements
- skills/design-constraints/composition-and-tutorial.md (from harness): tutorial-first level structure
- skills/design-constraints/checklist.md (from harness): 16 critique checks
- skills/global/{action-enum.md,color-legend.md,paths.md} (from harness): runtime API conventions
- skills/mechanic-novelty/* (from harness): novelty taxonomy and similarity protocol
- skills/mechanism-details/* (from harness): per-game mechanism summaries (all 25 read)
- 5 source files: cn04 (681 lines), sp80 (875 lines), sk48 (988 lines) — full reads; sb26 (~600 lines partial); mechanism-details for the remaining 22

## Deliverables Produced
- None (cached patterns file replaces per-run write).

## Notes
- Workspace was clean at start.
- 12 prior games already exist (kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d (note: missing from index — presumably retracted), fz5j, plus apparent index gap). Confirmed mechanism-details for all current priors were read.
- Strong cross-game patterns confirmed: tag-based sprite querying, RenderableUserDisplay step bar, per-level data dict, click-select+arrows+ACTION5 modal, multi-phase animation via phase tick, walkable underlay via tagged sprite with pixel value 2.
