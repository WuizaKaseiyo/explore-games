# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing and FSM map
- states/study.md (from harness root): four reading inputs required
- skills/global/{action-enum,color-legend,paths}.md
- skills/conventions/{from-tech-report,cross-cut-frequencies,reference-game-patterns}.md
- skills/design-constraints/{core-knowledge-priors,forbidden-elements,composition-and-tutorial,checklist,difficulty-rules}.md
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md
- prior-games/index.md (60 prior generated games — cumulative novelty floor)
- 25 deep-analyses (deep-analysis-3lvls/<id>/<id>-deep-analysis.md): read 23 in full (bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, m0r0, r11l[partial], re86, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30); ar25/ls20/s5i5 backed by skills/mechanism-details summaries (deep-analysis exceeds context-read limit)
- Initial-frame screenshots viewed: cn04, sp80, m0r0, tu93, wa30 level_1.png (visual style + palette + sprite-grain awareness)
- 5 reference-game source files in full: cn04 (click+arrow+ACTION5 selection-rotate), sk48 (arrow+click+undo, snake-grow with snapshot undo), sp80 (click+arrow+ACTION5 modal pour with view-rotation), tu93 (arrow-only 3-phase state machine), sb26 (click+ACTION5+ACTION7 commit-row with snapshot undo)

## Deliverables Produced
- None (per state spec — study consumes the cached patterns file and writes no per-run notes).

## Notes
- Cached patterns + cross-cut frequencies file replace the per-run study-notes.md; rules internalised include: step-counter HUD universal, tag-based sprite querying universal, ACTION5=distinctive verb slot, ACTION7=strict-undo-or-omit, no on-screen text, palette diversity required, mechanic must compose across L1/L2/L3 (one or two new mechanics per level promotion, all earlier mechanics required), no big-blocks-on-empty-field, no behavioural state encoded as pixel-mutation, no random.random() in step, no low-resolution upscaled chunky cells.
- 60 priors recorded in index.md — cover a wide breadth of physics/objectness/topology/agentness mechanic space; pick_mechanic must navigate around all of them.
- Per the study state's `## Next States` condition: all four reading inputs are completed; transition to pick_mechanic with no deliverables.
