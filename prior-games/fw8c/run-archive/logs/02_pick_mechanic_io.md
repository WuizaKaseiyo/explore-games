# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (from harness): no seed provided → autonomous mode.
- skills/global/* (from study): action enum, color legend, paths.
- skills/design-constraints/core-knowledge-priors.md (from study): allowed prior categories.
- skills/design-constraints/forbidden-elements.md (from study): no letters/digits/clipart/cultural conventions; importantly no arrow-shape glyphs.
- skills/mechanic-novelty/taxonomy-of-25-games.md (from study): 25 reference mechanic families.
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md (from study): novelty procedures (positive + negative tests).
- skills/mechanism-details/*.md (from study): per-game quick-reference summaries.
- prior-games/index.md (from harness, 66 prior entries): existing-corpus novelty set.
- skills/code/id-generation.md (from study): 4-char ID rules.

## Deliverables Produced
- mechanic-pick.md: ID `fw8c`, family `pigment-mix-walk`. Avatar walks chamber accumulating a 3-bit subset of {orange, pink, light-blue} pigments that mix into derived colours per a deterministic table; consumes "slot" sprites whose demanded colour matches the current mixture (which also clears the carrier). Documented prior-art comparison vs. taxonomy near-misses (ls20, re86, sc25) and prior-games near-misses (hr8q, tm5x, pk4m, plus pf3w / gv47 / bx84 cross-checked) with concrete distinguishing rules. Negative-similarity 7-dimension scan against ls20 (closest prior) shows 2 shared dimensions, below the 3-dimension reject threshold. §3.4 prior + forbidden-elements check passes.

## Notes
- Did NOT open `prior-games/<id>/run-archive/smoke-frames/level_*.png` for visual cross-comparison per negative-similarity-check step (those frames may not exist for all priors). Visual divergence argued textually via palette signature: fw8c uses {orange-12, pink-7, light-blue-10} as primary inputs to deliberately diverge from the {red-8, blue-9, green-14} cluster that recurs across many priors.
- Pigment OR-accumulation chosen so that the puzzle's planning surface lives in COLOUR-SET ROUTING (which subset to pick up before reaching slot X under wall constraints), not in temporal ordering — this is the load-bearing distinction from ls20's ordered-cycler walk.
- Critical implementation note for write_spec: the carrier's colour state must be VISIBLE on screen at all times (not hidden state) — checklist item 19. Carrier sprite re-tints to the current mixture each step; that tint IS the persistent visual cue.
