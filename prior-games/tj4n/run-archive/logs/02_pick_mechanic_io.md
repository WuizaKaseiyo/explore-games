# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (autonomous mode — no seed)
- prior-games/index.md (45 prior games — read for novelty)
- mechanic-novelty/taxonomy-of-25-games.md (25 reference families)
- mechanic-novelty/similarity-check.md, negative-similarity-check.md, prior-games-index-format.md
- design-constraints/* (priors, forbidden, composition, difficulty, checklist)
- skills/code/id-generation.md
- prior-games/qm4t/mechanism-detail.md (closest near-miss in priors corpus)

## Inputs to write_spec
- mechanic-pick.md (in workspace root, see deliverables)

## Deliverables Produced
- mechanic-pick.md: 4-char ID `tj4n`, family `walk-trail-loop-enclose`, full description, similarity-check (positive + negative) against the closest near-miss qm4t, and an axis-1 note acknowledging the family resemblance to the Qix arcade game.

## Notes
- The Qix similarity is the main risk on axis-1 (vs preexisting video games). Documented for the user's manual review.
- qm4t is the closest harness-detectable prior; the distinguishing rule (convex-hull-of-clicks vs walk-step-arbitrary-polygon) is sharp and concrete.
- Pursuer at L3 is the agentness ingredient (rare in priors — only 6/25 reference games use it).
- The interior-detection algorithm is point-in-polygon ray-casting; cheap on a 16×16 grid.
