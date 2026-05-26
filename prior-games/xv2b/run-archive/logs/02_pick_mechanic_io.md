# Step #02: pick_mechanic

## Inputs Consumed
- states/pick_mechanic.md (from harness root): instructions
- skills/global/* (already in memory)
- skills/design-constraints/* (already in memory)
- skills/mechanic-novelty/taxonomy-of-25-games.md (already)
- skills/mechanic-novelty/similarity-check.md (already)
- skills/mechanic-novelty/negative-similarity-check.md (already)
- skills/mechanic-novelty/prior-games-index-format.md (already)
- skills/code/id-generation.md (just read)
- prior-games/index.md (already)
- run input: no seed provided → autonomous mode
- prior screenshots viewed for negative similarity check: kx14 L1, rk7x L1, vd3g L1, kp9z L1, tg6w L1.

## Deliverables Produced
- workspace/mechanic-pick.md: chose `xv2b` / family `vessel-valve-equalize`. Connected-vessels hydrostatic equalisation with togglable valves; L2 adds drains; L3 adds uphill pumps. Distinguishing rules vs sp80, lv4k, kx14, vd3g, kp9z, rk7x. Action subset [5, 6].

## Notes
- Brainstormed ~25 candidate families; most collided heavily with priors (rope-tension shared 3 dims with kw8t; column-shift = qx7p; phase-coupled = fz5j; chain-couple/decouple bordered sk48+vc33; thermal-diffusion = tm5x; centroid + various magnetism = kn58/mr5q/vt6q; wavefront-convergence = pf3w; gear-mesh = gx7m; hinge-articulation = nb6t).
- The chosen family wins because hydrostatic-equalize-via-valve-graph is genuinely under-explored: kx14 is the only fluid prior, and it is single-tank / surface-raise rather than multi-vessel / valve-toggle.
- Visual signature (thin tall blue columns + small valves between) is fresh — no prior has multi-column water-fill bars side-by-side.
