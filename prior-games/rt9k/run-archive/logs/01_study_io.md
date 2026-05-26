# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): the workflow framing and FSM
- states/study.md: the four reading inputs required
- skills/global/* (action-enum, color-legend, paths): API constants and conventions
- skills/conventions/from-tech-report.md: design philosophy distilled from the NovaPlay technical report
- skills/conventions/cross-cut-frequencies.md: pre-computed feature frequencies across the 25 reference games
- skills/conventions/reference-game-patterns.md: cached recurring design moves and anti-patterns
- skills/design-constraints/* (core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules)
- skills/mechanic-novelty/* (taxonomy-of-25-games, prior-games-index-format, similarity-check, negative-similarity-check)
- skills/mechanism-details/*.md: 25 quick-reference summaries
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md for the 25 reference IDs
- deep-analysis-3lvls/<id>/level_{1,2,3}.png for the 25 reference IDs (rendered initial frames)
- 5 reference game source files in full (picked across families per taxonomy + line-budget constraint)
- prior-games/index.md: cumulative novelty record (64 indexed prior games + ~9 unindexed: gh4r warden's-pen, hp9c pinwheel-cell-rotation, lz7q dual-plane-walk, qd6n chord-pluck-strike, tc8s loop-capture, tx4q walk-buffer-resonator, vk6m altitude-grip-climb, vw3p vessel-pour-equalize, xv4n cavity-nest-fit)

## Deliverables Produced
- None — study has no deliverables; cached patterns + frequencies replace per-run study notes.

## Notes
- Read all 25 mechanism-detail summaries; full source for cn04 (click-select+arrow-move+ACTION5-rotate), sp80 (arrow+ACTION5+click, fluid sim, multi-phase animation), wa30 (arrow+ACTION5 carry/drop, BFS pathfinding NPCs), sk48 (arrow+click+undo trail-match, ACTION7 strict-undo, snapshot stack), cd82 (full keyboard+click, multi-phase sweep animation, ACTION5 commit).
- Sampled L1 screenshots cn04, sp80, sb26, vc33 to anchor visual style.
- Prior-games corpus is dense (~73 games). Mechanic families heavily explored across: object-on-grid moves (pawn walks, push, slide), rotational/folding/mirror, fluid/gravity/cellular, click-stamp/paint, line-of-sight/beam, chain-reaction, programmable, pursuer/agentness, multi-pawn lockstep, vessel/equalize, fold/mirror, etc.
- Open novelty hunting grounds: less-explored prior corners — temporal/sequence-replay (only ek73 wake-trail, bw7k ghost-replay, pf3w wavefront-timing), self-modifying-rule, parallax-layer, phase-of-matter / state-of-rendered-cell distinct from current "tile cycler" canon.
