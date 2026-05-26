# Step #02: pick_mechanic

## Inputs Consumed
- skills/mechanic-novelty/taxonomy-of-25-games.md (from study)
- skills/mechanic-novelty/similarity-check.md
- skills/mechanic-novelty/negative-similarity-check.md
- skills/code/id-generation.md
- skills/design-constraints/core-knowledge-priors.md
- skills/mechanism-details/cn04.md (closest near-miss)
- prior-games/index.md (70 priors enumerated)

## Deliverables Produced
- mechanic-pick.md: ID `wm6q`, family `edge-color-rotate-match`, one-paragraph
  description, similarity check against taxonomy + prior-games (positive +
  negative tests).

## Notes
- Closest near-miss in taxonomy is cn04 (boundary-alignment via rotation); closest
  prior is qf8m (click flips a cell-pattern). Both pass the negative-similarity
  walk well below the 3-dimension threshold.
- Single action: ACTION6 click only. Distinctive verb lives on click.
- Core knowledge priors: objectness + basic geometry. No physics, no agentness.
- Visual richness comes from per-tile internal structure: 4 colour bands + 10×10
  inner glyph area for lock / link / empty.
- Closing IO log here; write_spec consumed mechanic-pick.md as input and produced
  the full 9-section spec in `mechanic-spec.md`.
