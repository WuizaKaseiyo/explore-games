# Step #02: pick_mechanic

## Inputs Consumed
- states/pick_mechanic.md (state file)
- skills/global/* (already read in #01)
- skills/design-constraints/* (already internalised in #01)
- skills/mechanic-novelty/similarity-check.md (positive test)
- skills/mechanic-novelty/negative-similarity-check.md (8-dimension test)
- skills/mechanic-novelty/taxonomy-of-25-games.md (taxonomy of 25)
- skills/mechanic-novelty/prior-games-index-format.md
- skills/code/id-generation.md (4-char ID rules)
- prior-games/index.md (74 indexed entries) plus 9 unindexed folder entries (gh4r, hp9c, lz7q, qd6n, tc8s, tx4q, vk6m, vw3p, xv4n) read via their `mechanism-detail.md` files.
- Sampled smoke-frames of unindexed priors (lz7q, hp9c, qd6n, xv4n, gh4r) for visual signature comparison.

## Deliverables Produced
- mechanic-pick.md: ID `dh4j`, mechanic-family `tile-coded-stride`, one-paragraph description, per-near-miss distinguishing rules vs taxonomy and prior-games corpus, and a negative-similarity-check walkthrough vs the two strongest near-misses (bz3k, ls20).

## Notes
- Critical discovery: lz7q (unindexed) is "dual-plane-walk" — exactly the first candidate I would have chosen. The unindexed-folders walk-through prevented a duplicate-mechanic submission.
- Considered many candidates before settling: hue-carrier-swap (too close to qb84/fw8c), zone-overlay-paint (too close to re86/hl4n), beam-multi-emitter (too close to bx84/cd82), sight-cone stealth (visually too close to chasing-NPC games), split-merge-blobs (verb novel but visual-grain unclear), step-distance-walker (selected).
- The chosen mechanic uses a verb category (per-cell-encoded-stride) that has no analogue in the corpus. ACTION space is pure-arrow `[1, 2, 3, 4]` — no click, no ACTION5. This is a relatively rare action subset in the corpus (~7/25 reference games are arrow-only; the prior-games corpus has very few), so the action-palette itself contributes to differentiation.
- Available actions = `[1, 2, 3, 4]` only. No ACTION7 (no undo), per `action-enum.md` slot 7 is strict-undo; the game doesn't have a meaningful undo so omitting is correct.
