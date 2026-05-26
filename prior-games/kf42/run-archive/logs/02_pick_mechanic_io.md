# Step #02: pick_mechanic

## Inputs Consumed
- workspace/study-notes.md (from #01 study): cross-cut frequencies, recurring moves, anti-patterns, open questions.
- Run input seed: empty (no `--seed` was supplied; autonomous mode).
- skills/global/* (paths.md, action-enum.md, color-legend.md): paths, action slot conventions, palette legend.
- skills/design-constraints/core-knowledge-priors.md: only the four allowed prior categories (objectness, geometry/topology, physics, agentness).
- skills/mechanic-novelty/taxonomy-of-25-games.md: 25-row novelty floor.
- skills/mechanic-novelty/similarity-check.md: family→description→distinguishing-rule procedure.
- skills/mechanism-details/*.md: legacy summaries (consulted on near-miss).
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md (per id) when a row is flagged as a near-miss.
- skills/code/id-generation.md: 4-char ID rules + reserved list.
- prior-games/index.md: empty (header-only) — created at the start of this state because the file did not exist.

## Deliverables Produced
- workspace/mechanic-pick.md: 4-character ID `kf42`, mechanic-family tag `tether-pawn-cycle`, one-paragraph description with explicit prior-categories citation, novelty check against four near-miss taxonomy entries (m0r0, r11l, sk48, ls20) with concrete distinguishing rules, prior-games index empty noted.

## Notes
- Created `prior-games/index.md` (header-only) because it did not previously exist; this matches the "Initial state" clause of `prior-games-index-format.md`. The next-states transition deliverable for `pick_mechanic` (per states/pick_mechanic.md) is satisfied.
- ID generation: `kf` (random letters) + `42` (random digits); not in reserved list; not a word; not a collision.
- Picked mechanic family combines two priors not heavily exercised by the 25 — distance-coupled object pair (physics+objectness+geometry) plus a colour-cycle interaction (objectness self-mutation) — and avoids the obvious dominant families (sokoban, click-to-paint, pour-route, programmable-pawn, rule-rewrite, stamp-canvas, etc.).
