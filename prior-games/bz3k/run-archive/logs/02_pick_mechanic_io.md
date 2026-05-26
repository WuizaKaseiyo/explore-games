# Step #02: pick_mechanic

## Inputs Consumed
- states/pick_mechanic.md (state spec)
- skills/global/* (already in head)
- skills/design-constraints/core-knowledge-priors.md
- skills/mechanic-novelty/taxonomy-of-25-games.md
- skills/mechanic-novelty/similarity-check.md
- skills/mechanic-novelty/negative-similarity-check.md
- skills/code/id-generation.md
- prior-games/index.md (60 prior families)
- run input: no seed (autonomous)

## Deliverables Produced
- mechanic-pick.md: 4-char ID `bz3k`, family `drift-impulse-cardinal`,
  one-paragraph description, distinguishing rules vs. closest taxonomy
  rows (m0r0, tu93) and prior-games rows (wt39, kn58, tg6w, vt6q, zd7m,
  zw91, kx14). Negative-similarity check walked across all 8 dimensions
  vs. wt39 (closest) — heavy axes (6/7/8) differ; verdict NOVEL.

## Notes
- Drift-impulse-cardinal occupies under-explored territory: persistent
  inter-turn velocity on a single cardinal-only avatar. Closest analogue
  is wt39 (glide-deflect-thaw), but wt39 fires one-shot glides whose
  velocity resets between actions; drift-impulse accumulates velocity
  across actions.
- Hidden-state risk identified: velocity (vx, vy). Mitigation: a
  pixel-smear *wake* trailing the avatar persistently surfaces both
  magnitude and direction.
- Composition plan: L1 = drift-impulse + speed-zero-target-latch;
  L2 = + velocity-cap-band; L3 = + velocity-flipper-plate.
- Transition condition met (novel mechanic, both similarity checks pass,
  non-colliding ID). Proceeding to write_spec.
