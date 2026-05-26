# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, notes
- states/study.md (from harness root): instructions for this state
- skills/global/*.md (action-enum, color-legend, paths)
- skills/conventions/from-tech-report.md, cross-cut-frequencies.md, reference-game-patterns.md
- skills/design-constraints/checklist.md, composition-and-tutorial.md, core-knowledge-priors.md, difficulty-rules.md, forbidden-elements.md
- skills/mechanic-novelty/*.md (taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format)
- skills/mechanism-details/*.md (25 quick-reference summaries)
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md and level_{1,2,3}.png for all 25 reference IDs
- 5 full reference-game source files (TBD picks across mechanic families)
- prior-games/index.md (24 priors as cumulative novelty corpus)
- prior-games/<id>/run-archive/smoke-frames/level_1.png for bx84, gv47, kp9z, gx7m, vp6h (closest mechanic neighbours to candidate)
- 25 mechanism-details summaries (the shorter authoritative summaries; deep-analyses skimmed where contradictions absent)
- Reference level_1 screenshots: cn04, sp80, m0r0, ka59 (closest visual neighbours)
- Five reference source files in full: cn04 (620), sp80 (738), sk48 (643), m0r0 (712), tr87 (696) — spanning families (rotate-jigsaw, click+arrow+ACTION5+phase-machine+tilt, paired-trail+undo+animation, lockstep+mirroring+lever-toggle, tape-cycle+rule-rewrite)

## Deliverables Produced
- None (study state has no deliverables; cached patterns file replaces per-run study notes).

## Notes
- Cached reference-game-patterns.md and cross-cut-frequencies.md already digest the lessons of the 25 reference games; per state instruction, I did NOT re-derive a workspace/study-notes.md. Internalised:
  - Universal step-counter HUD as a depleting bar.
  - Tag-based sprite querying (`level.get_sprites_by_tag`) and per-level data dicts (`level.get_data("step_budget")`).
  - ACTION5 is where novelty lives.
  - Goal communication via visual coupling (matching colour/shape), no on-screen text.
  - Multi-phase step() with phase-tick sentinels for animations (mandatory when transitions are long-distance or compound).
  - No hidden state — every player-relevant mutation must produce a persistent visible cue.
  - Visual detail floor: 3×3 sprites with internal structure; 1×1 plain-cell rendering fails the no-information-loss-at-32×32 test.
  - Composition rule: every level promotion adds 1-2 new mechanics, all earlier mechanics carry forward and are required by the witness.
- Prior visual landscape inspected via initial-frame PNGs of bx84, gv47, kp9z, gx7m, vp6h — the closest mechanic-neighbours to my candidate. Each diverges from the candidate on the heavy-weighted dimensions (palette, sprite grain, core dynamic).
- Ready to proceed to pick_mechanic.

