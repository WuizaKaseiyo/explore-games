# Step #02: pick_mechanic

## Inputs Consumed
- `task-overview.md` (run input: empty / autonomous)
- `skills/mechanic-novelty/taxonomy-of-25-games.md`
- `skills/mechanic-novelty/similarity-check.md`
- `skills/mechanic-novelty/negative-similarity-check.md`
- `skills/mechanic-novelty/prior-games-index-format.md`
- `skills/mechanism-details/{su15, ar25, r11l}.md` (taxonomy near-misses)
- `skills/code/id-generation.md`
- `prior-games/index.md` — full corpus, 34 entries
- `prior-games/gv47/run-archive/smoke-frames/level_1.png` (closest prior — opened for negative-similarity check)
- `prior-games/xn5p/run-archive/smoke-frames/level_1.png` (visual cross-check)
- `prior-games/lv4k/run-archive/smoke-frames/level_1.png` (visual cross-check)

## Deliverables Produced
- `mechanic-pick.md`: 4-char ID `qm4t`, family `convex-pen-trap`, full mechanic
  description, similarity-check rows against every taxonomy and prior-games
  near-miss with concrete distinguishing rules, and the negative-similarity
  walk against gv47/su15/ng52.

## Notes
- Considered ~20 candidate mechanics; rejected most on near-prior overlap
  (e.g. tether/lasso → gv47 surround; ghost-time-delay → g50t; vector-sum
  thrusters → pf3w + kn58; weave-thread → sk48 trail; vision-cone navigation
  → ls20 patrolling enemies + bullets).
- Final choice anchored on a primitive — convex-hull point-in-polygon —
  that is absent from both the 25 reference families and the 34-prior corpus.
  The closest prior (gv47) shares only the "click + ACTION5" verb skeleton
  and step-counter lose mode (2 of 8 negative-similarity dimensions).
- ID `qm4t`: `q` + `m` + `4` + `t`. Verified collision-free.
- Open question for `write_spec`: how richly to render critters and posts.
  Plan is for critters to be 5×5 multi-pixel sprites with 2-pixel eyes and a
  multi-pixel body interior; posts to be 1-pixel-wide × 3-pixel-tall spikes
  with a 2-pixel cap; pen-outline as a 1-pixel-wide axis-or-diagonal closed
  polygon; tally HUD as a row of coloured swatch dots — none of which read as
  letters, digits, or real-world clipart. Resolution will be at the display-
  pixel level (no upscaled chunky cell-blocks).
