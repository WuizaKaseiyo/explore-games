# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (from harness root): autonomous-mode framing, no seed.
- states/pick_mechanic.md (from harness root).
- skills/mechanic-novelty/taxonomy-of-25-games.md (from #01 study).
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md, prior-games-index-format.md.
- skills/design-constraints/core-knowledge-priors.md, forbidden-elements.md.
- skills/code/id-generation.md.
- prior-games/index.md (24 priors).
- 25 reference mechanism-details summaries (from #01 study).
- Initial-frame screenshots for closest priors (bx84, gv47, kp9z, gx7m, vp6h) and references (cn04, sp80, m0r0, ka59).

## Deliverables Produced
- mechanic-pick.md: 4-character ID `pf3w`, mechanic-family tag `wavefront-converge-timing`, one-paragraph description, per-level escalation preview, novelty checks against all 7 candidate near-misses in the 25-game taxonomy and all 6 candidate near-misses in `prior-games/index.md` (bx84, vp6h, gv47, vn8d, kp9z, gx7m), plus axis-1 (preexisting video games) novelty argument.

## Notes
- Negative-similarity walk for the closest priors all came in well below the 3-of-8 reject threshold (max 2-3 shared dimensions, with all heavy-weighted dimensions [6 visual signature, 7 pixel grain, 8 core dynamic] DIFFERENT).
- Critical distinguishing axis from all priors and references: **temporal axis**. No prior or reference uses an `ACTION5`-as-global-tick verb where the puzzle is about *when* (which inter-tick gap) to fire actions. cd82 has a ring orbit but no time-elapsed-between-placements axis; sp80's commit triggers a one-shot sim and resets; bx84's beam is instantaneous; vn8d's cascade is single-shot. `pf3w` is the first wavefront-synchronization puzzle in the corpus.
- The mechanic's success hinges on: (a) clear visual rendering of expanding BFS frontiers as colored 1-cell outlines, (b) emitter sprites with internal counter-ring detail to surface the per-emitter age, (c) target sprites whose center-pixel changes from hollow→filled exactly on the arrival tick (no on-screen text). All three are concrete and feasible in the engine.
- Ready to proceed to write_spec.

