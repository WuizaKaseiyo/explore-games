# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, HITL=not allowed
- states/study.md (from harness root): four reading-input requirements
- 25 deep-analyses + level_1/2/3 screenshots (from deep-analysis-3lvls/<id>/): evidence layer
- 5 full source reads (selected to span families; ≤2000 lines)
- design-philosophy skill files (from skills/conventions, skills/design-constraints)
- skills/conventions/reference-game-patterns.md (cached recurring patterns)
- skills/global/* (paths, color-legend, action-enum)
- skills/mechanic-novelty/* (taxonomy + similarity rules)
- skills/mechanism-details/<id>.md (all 25 quick reference summaries)
- 5 reference-game source files (with grep-narrowed reads on the larger ones):
  - cn04 (621 lines) — click+arrows+ACTION5 rotate, click-to-select pattern
  - tu93 (~1100 lines, class portion) — pure-arrow, 3-phase animation step()
  - sp80 (738 lines) — click+arrows+ACTION5 pour, multi-frame splash animation, rotation-aware action remapping
  - sb26 (~830 lines, class portion) — click+ACTION5 commit+ACTION7 undo, multi-stage commit-marker walk
  - m0r0 (~700 lines, class portion) — click+arrows+ACTION5 mirror-orb merge with crash flash
- prior-games/index.md (19 prior generated games for novelty floor)

## Deliverables Produced
- None (per state's transition contract).

## Notes
- Cached reference-game-patterns.md and cross-cut-frequencies.md serve the synthesis; no new study-notes.md required.
- Heavy familiarity sources: mechanism-details summaries (all 25), cached patterns, 4 source-class reads spanning different action palettes.
- Visual-signature opening of L1 PNGs deferred to negative-similarity-check at pick_mechanic time, where the comparison is concrete.
- Open question for pick_mechanic: 19 prior games + 25 reference games leave little untouched. Hunting grounds: agentness x topology; pure topology w/o pawn; new use of ACTION5 freedom slot; data-flow / dataflow / signal mechanics not yet seen.
