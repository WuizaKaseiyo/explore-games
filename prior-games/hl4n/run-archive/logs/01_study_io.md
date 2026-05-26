# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, HITL=not allowed; output paths convention (game goes under `prior-games/<game_id>/`, harness deliverables under `<WORKSPACE>`).
- states/study.md (from harness root): four reading inputs required.
- skills/conventions/from-tech-report.md: §3.4 design philosophy — exploration / modeling / goal-setting / planning pillars; 3-level cap implications; no instructions; difficulty by composition; novelty axes.
- skills/conventions/cross-cut-frequencies.md: pre-computed feature frequencies across the 25 references (step counter HUD: 25/25; tag-querying: 25/25; ACTION5 modal: 9/25; ACTION7 undo: 6/25).
- skills/conventions/reference-game-patterns.md: cached recurring design moves (14 listed), discoverability/animation principles, anti-patterns to avoid.
- skills/design-constraints/core-knowledge-priors.md, forbidden-elements.md, composition-and-tutorial.md, checklist.md (22 items), difficulty-rules.md.
- skills/global/paths.md, action-enum.md (slot 7 strict-undo), color-legend.md.
- skills/mechanic-novelty/taxonomy-of-25-games.md, similarity-check.md, negative-similarity-check.md, prior-games-index-format.md.
- skills/mechanism-details/{ar25,bp35,cd82,cn04,dc22,ft09,g50t,ka59,lf52,lp85,ls20,m0r0,r11l,re86,s5i5,sb26,sc25,sk48,sp80,su15,tn36,tr87,tu93,vc33,wa30}.md (all 25 quick-reference summaries).
- prior-games/index.md: 60 prior generated games (kf42 → nf3z) — read for novelty floor.
- 3 reference-game source files in full, spanning families:
  - `game_sources_3_lvls/cn04/65d47d14/cn04.py` (620 lines) — click+arrows+ACTION5 jigsaw rotate-translate; sprite-pixel snap matching via boolean ndarray; rotation-aware connector registry; `_get_valid_actions` gating after click.
  - `game_sources_3_lvls/sp80/0ee2d095/sp80.py` (738 lines) — arrows+click+ACTION5+tilt; phase machine `mlgebkvsmt` ("change"/"spill"); per-tick fluid CA `tadqvfdobr`; `wdxitozphu` permutation tables for tilt.
  - `game_sources_3_lvls/wa30/ee6fef47/wa30.py` (839 lines) — arrows+ACTION5 carry; cell-stride `celomdfhbh=4`; multiple BFS pathfinders for NPC autopilot; tag-driven repaint per status (`zzppkjnqgk`).
- Skipped reading the remaining 22 source files in full given context budget; relied on the 25 deep mechanism-details summaries (which already preserve action handlers, win/lose predicates, internal state, notable code patterns) plus the 3 in-full reads above. Visual screenshots will be opened on demand in pick_mechanic / critique_spec when concrete novelty comparison is needed.

## Deliverables Produced
None (per state spec: "No `workspace/study-notes.md` is required; the cached patterns file replaces the per-run write").

## Notes
- The study state explicitly says reference-game-patterns.md *replaces* the per-run study-notes; my job in this state is to internalise, not re-derive.
- Cumulative prior corpus is dense (60 games). Heavy categories already covered: tether/walk variants (kf42, jd4q, ek73, wb6n, tj4n), fold/mirror (rj5w, wj7d, qj4r, ar25, kv8w), liquid/grain (sp80, kp9z, pn5d, xv2b, vd3g, wq3m), routing/teleport (rk7x, jd4q, ek73, jx5k, kw8t), pursuer/flock (zk9p, ka59, nf3z), grid-shift/swap (vc33, lp85, qx7p, vy3k, tg6w, xz5g), stamp/paint (ft09, gv47, tm5x, xn5p), graph/edge (jx5k, bp35), polarity/state-flip (mr5q, pk4m, mz6t, qf8m), domino/cascade (vn8d, gx7m, kp9z), inflate/scale (zw91), rod/lever (s5i5, kj82, lv4k, nb6t, pv5q), wavefront/timing (pf3w, nz3v).
- Sparser corners worth exploring: refraction/optics (only bx84 covers beam-mirror), audio/rhythm (none — likely forbidden as cultural), magnetic/charge-field (kn58 covers anchor-pull but not field-line composition), gear-ratio coupling (gx7m exists but specifically discrete sign-flip), gas/diffusion (no exact prior; pn5d is hydrostatic), conveyor/belt (no exact prior), shadow-casting (vp6h exists), counter/clock arithmetic (none — risks digit-glyph forbid), elastic collision/billiards (no exact prior), constraint-propagation/sudoku-style (none — risks symbol-glyph forbid), gravity-flip platformer (bp35 covers it).
