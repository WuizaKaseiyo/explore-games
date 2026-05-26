# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing and starting state
- states/study.md (from harness root): study description and 4 reading inputs
- skills/global/* (registered skill): global guidance
- skills/conventions/* (registered skill): from-tech-report, cross-cut-frequencies, reference-game-patterns
- skills/design-constraints/* (registered skill): core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist
- skills/mechanic-novelty/* (registered skill): taxonomy-of-25-games
- skills/mechanism-details/* (registered skill): quick-reference summaries
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md for 25 reference games
- deep-analysis-3lvls/<id>/level_{1,2,3}.png for 25 reference games
- 5 reference game source files (in full): cn04 (mixed-action click+arrow+ACTION5 rotate, 620 lines), sp80 (mixed click+arrow+commit, tilt mechanic, 738 lines), tr87 (pure-arrow symbol cycling, 696 lines), wa30 (cardinal motion + ACTION5 pickup, 839 lines), sk48 (cardinal+click+undo snake trail, 643 lines)
- prior-games/index.md (cumulative novelty source-of-truth; 71 prior games)
- Screenshots sampled for visual fluency: cn04, tu93, sp80, sb26, m0r0, ka59, wa30, lp85, vc33, ar25, cd82, r11l, ft09, tr87, s5i5, sk48, bp35, dc22, g50t, ls20, re86, su15, sc25, lf52 (24 L1 frames)

## Deliverables Produced
- (none required by study → pick_mechanic transition; cached patterns + cross-cut frequencies + taxonomy obviated re-derivation per state spec)

## Notes
- The prior-games corpus is at 71 entries. Many mechanic families are already explored — pulleys, mirrors, fold/reflection, conveyors, magnets, beams, portals, gear meshes, projectiles, etc. The "open" corners of the priors-cube include: explicit *probability* / counting / partial-info (agentness with hidden state); explicit time/clock periodicity beyond fz5j; rotation-of-the-camera-itself (vy3k did quadrant swap; nothing about rotating the world around the player); "social"-style multi-agent coordination beyond merge/lure; **a "magnification / zoom" verb** (no game lets you change camera-detail-level); **a "weight / scale balance" beyond lv4k**; **a "rope / string with slack" rather than fixed tether**; **information-revealing flashlight beam (different from lq5x's cone-illuminate / vp6h's shadow-cast)**; **predicate-evaluation games** (place a piece, evaluate against a formula); **"breath / charge meter that you choose when to spend" verbs**.
- Strong recurring anti-patterns to avoid: pawns+target+walls on a small grid (kf42/vh68 cautionary tale); single-mechanic-scaled-across-levels; chunky upscaled grids reading as crude; ACTION7 used for anything other than undo.
