# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (autonomous mode — no seed): noted "user MAY pass an optional one-line seed; if absent, the agent picks autonomously"
- skills/mechanic-novelty/taxonomy-of-25-games.md (re-read for picking): 25 reference families
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md, prior-games-index-format.md (full): novelty rules
- skills/code/id-generation.md (full)
- skills/global/action-enum.md (re-read): the 4 distinctive-verb patterns; chose "Distinctive verb on ACTION1-4" subset
- prior-games/index.md (re-read): 24 prior generated games
- 4 prior-games initial frames (zd7m, wt39, kn58, kp9z, kx14): visual-signature comparison for negative similarity check
- skills/design-constraints/core-knowledge-priors.md (re-read): confirmed objectness + physics + geometry combo

## Deliverables Produced
- mechanic-pick.md: 4-char ID `tg6w`, mechanic-family tag `settle-pile-tilt`, one-paragraph description, distinguishing rules against 3 closest taxonomy entries (g50t, tu93, sp80) and 5 closest priors (zd7m, wt39, kn58, kx14, kp9z), 8-dimension negative-similarity table with verdict NOVEL.

## Notes
- Considered ~20 candidate mechanics in scratch deliberation; the corpus is dense (49 mechanics taken across reference + priors). Settled on settle-pile-tilt as the cleanest novel candidate with three composable mechanics (gravity-rotate slide-to-end, colour-permeable walls, sticky-pads).
- Closest concern is zd7m (3 shared dimensions: multi-block-on-grid, step-counter lose, 3×3 pixel grain). Below the rejection threshold; the core dynamic dimension is fundamentally different (one-cell coordinated step vs slide-to-end pile) and the visual signature will be distinct.
- ID `tg6w` chosen per the recommended random-prefix-suffix procedure; verified non-collision against the 25 reserved + 24 prior list.
- Action subset is pure-arrow `[1, 2, 3, 4]` — the gravity vector lives directly on the four cardinal slots, which is the most expressive home for this mechanic.
