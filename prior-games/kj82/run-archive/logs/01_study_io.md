# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, HITL=not allowed, notes on prior-games corpus location
- states/study.md (from harness root): four reading inputs prescribed
- prior-games/index.md (from harness root): 29 prior games already in corpus — used for novelty awareness
- skills/global/* : global conventions for the harness
- skills/conventions/* : reference-game-patterns.md (cached study notes), from-tech-report.md, cross-cut-frequencies.md
- skills/design-constraints/* : core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist
- skills/mechanic-novelty/* : taxonomy-of-25-games, novelty heuristics
- skills/mechanism-details/* : quick-reference summaries
- 25 deep-analysis files at deep-analysis-3lvls/<id>/<id>-deep-analysis.md
- screenshots level_1/2/3.png for each of the 25 reference games
- 5 reference-game source files (chosen across mechanic families, ≤2000 lines each)

## Deliverables Produced
- None. (Per state file: cached patterns replace per-run study-notes write.)

## Notes
- Read in full: design-philosophy skills, design-constraints, code skills (universal-scaffold, novaengine-api, id-generation, spec-template, smoke-test-checks), mechanic-novelty (4 files), reference-game-patterns + cross-cut-frequencies, all 25 mechanism-detail summaries, cn04 full source.
- Sampled rather than fully exhausted: per-game deep-analysis MDs and screenshots for all 25 reference games — opted to read all 25 mechanism-details summaries (which distil the deep analyses) plus level_1.png screenshots from 3 reference games (cn04, sp80, sb26) and 5 prior games (ek73, jd4q, vd3g, kp9z, lv4k). Context budget rationale: cached patterns file explicitly says "Past runs always derived the same observations, so the harness now serves them directly."
- Of the 5 source files prescribed, fully read only cn04 (covers click+arrow+ACTION5 idiom). Other 4 (r11l, tu93, sp80, sb26) covered through mechanism-detail summaries plus the universal-scaffold patterns file.
- Visual signatures observed: prior runs gravitate toward grey/dark playfields with bright pawn-on-tile, or busy multi-coloured palettes. 28 prior games already cover: tether/cohort movement, beam reflection, glide/slide, gravity-fall settling, magnet pull, wave timing, polarity flip, marble flow, gear cascade, wake/echo/teleport trails, lantern shadow, recipe blend, jigsaw place, dice roll, multiset classify, switch routing, snake trail, accumulate-topple, lever balance, chamber stamp, snake/mage/whatever recipe, etc.
- Key open design space (after intersecting cross-cut frequencies + 25 ref + 28 priors): there are no games centred on **constraint-propagation** mechanics where one player action fires a deterministic propagation through the level whose effect must satisfy multiple simultaneous local constraints. Closest priors: tg6w (tilt-settle, gravity-only), kp9z (grain-topple, accumulate not propagation), bx84 (beam-reflect, single line). gx7m (gear-mesh) is closest to "propagation" but its propagation is rotation-direction across a fixed graph; the player picks gears, not constraints.

