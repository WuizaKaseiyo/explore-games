# Step #02: pick_mechanic

## Inputs Consumed
- skills/global/* (from #01 study, internalised): action enum, color legend, paths
- skills/design-constraints/core-knowledge-priors.md (from study): allowed prior categories
- skills/design-constraints/forbidden-elements.md (from study): no symbols/letters/clipart
- skills/design-constraints/composition-and-tutorial.md (from study): 3-level structure with +1-or-+2 mechanics per promotion
- skills/mechanic-novelty/taxonomy-of-25-games.md (from study): 25 reference families
- skills/mechanic-novelty/similarity-check.md (from study): positive distinguishing-rule procedure
- skills/mechanic-novelty/negative-similarity-check.md (from study): 8-dimension surface-overlap test
- skills/mechanic-novelty/prior-games-index-format.md (from study): index.md schema
- skills/code/id-generation.md (from this state): 4-char ID rules
- prior-games/index.md (from corpus): 81 entries
- prior-games/{gh4r,hp9c,lz7q,qd6n,tc8s,tx4q,vk6m,vw3p,xv4n}/mechanism-detail.md (sampling): uncommitted recent priors not yet in index
- skills/mechanism-details/*.md (from #01 study): quick-ref summaries for 25 references

## Deliverables Produced
- mechanic-pick.md: chosen mechanic family `polyomino-walker-rotate` with ID `hb5n`, one-paragraph description, distinguishing rules against 4 reference near-misses (cn04, ar25, tu93, and the broader walker family) and 6 prior-games near-misses (xv4n, zw91, nz3v, pz4t, nb6t, lt7m), plus an explicit 8-dimension negative-similarity walk concluding NOVEL.

## Notes
- The novelty angle: ACTION5 rotates the AVATAR'S OWN BODY (rigid 3-4 cell polyomino) rather than rotating a selected piece, the world, a wedge, or the camera. Surveying 25 references + 90 priors, none has a rotating-walker-avatar — closest are cn04/ar25/pz4t/xv4n (rotate selected pieces in placement context, no walking) and nz3v (2×2 square avatar walks while a separate wedge rotates).
- ID `hb5n` chosen randomly; verified non-colliding via grep against reference list + index.md + untracked prior-game directory names.
- Autonomous mode (no user seed); the mechanic was chosen freely.
- No "open questions" left for write_spec — the per-level mechanic ladder (L1 walk+rotate, L2 +growth-pickup, L3 +rotation-lock) is also sketched in mechanic-pick.md so the spec can build on it directly.
