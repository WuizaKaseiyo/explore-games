# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (autonomous mode — no seed in user input).
- skills/mechanic-novelty/taxonomy-of-25-games.md (25 reference families).
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md.
- prior-games/index.md (33 prior games).
- skills/mechanism-details/s5i5.md (closest reference candidate).
- skills/code/id-generation.md.

## Deliverables Produced
- mechanic-pick.md: 4-char ID `zw91`, family `inflate-fit-burst`, 1-paragraph description, distinguishing rules vs s5i5/nb6t/gv47/ka59/ft09 + pz4t/kp9z, full 8-dimension negative-similarity walk. Verdict: NOVEL.

## Notes
- Autonomous mode (no seed). Picked a mechanic where the player's own footprint size is the load-bearing variable — rare in the corpus.
- Composition arc: L1 = move + size-cycle (2 mechs), L2 adds inflate-push (3 mechs), L3 adds overload-burst (4 mechs). +1 each level promotion.
- Plan to render at grid_size=(64,64) scale=1 with sprites that have rich internal pixel detail; avatar at sizes 5×5 / 11×11 / 17×17 px with cross marking; movement in 4-px hops via internal tile convention.
- Palette plan: bg=2, walls=4 brick with 5 accents, avatar=12+13, socket=11, blocks=15+6, HUD=9→0. No `{4,8,9}` trap.
- Verb-axis: arrows + modal ACTION5 (the freedom slot) — 9/25 reference games use ACTION5 modally.
