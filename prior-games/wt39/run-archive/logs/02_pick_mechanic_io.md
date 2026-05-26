# Step #02: pick_mechanic

## Inputs Consumed
- skills/mechanic-novelty/taxonomy-of-25-games.md (from #01 study): 25 reference families.
- prior-games/index.md (from harness root): 14 prior games.
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md (from #01 study).
- skills/design-constraints/core-knowledge-priors.md (from #01 study).
- skills/code/id-generation.md (from #01 study).
- skills/conventions/reference-game-patterns.md "Open questions" section (from #01 study).

## Deliverables Produced
- mechanic-pick.md: chose `glide-deflect-thaw` family with ID `wt39`. Pawn glides until obstruction; bumpers deflect 90°; thaw-tiles vanish after one cross. L1 = base glide; L2 += bumpers; L3 += thaw-tiles. Distinguishing rules vs kn58, vn8d, ar25, ka59, m0r0, pj7k, fz5j, bx84 articulated. Negative-similarity passes (max 2-3 dimensions shared with closest priors).

## Notes
- Closest near-misses: vn8d (chain reaction; different core dynamic), kn58 (single-action far-reaching motion; different input cardinality), pj7k (one-step-per-press with face permutation; no momentum). All distinguished by the unbounded-glide-until-collision physics.
- Action set is minimal: `[1, 2, 3, 4]` only (cardinal motion). No ACTION5/6/7. This intentionally diverges from the modal/click-heavy reference set.
- Selected mechanic family deliberately under-represented in priors: directional-momentum / inertia. Of 25 reference + 14 priors = 39 mechanics, none use unbounded slide-until-wall.
- Visual palette plan: ice (10 light-blue, 1 off-white), walls (4 off-black), pawn (8 red), goal (matching), bumpers (12 orange w/ stripe), thaw-tiles (15 purple or 11 yellow). Distinct from kn58/bx84 palettes.
