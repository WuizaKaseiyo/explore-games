# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (from harness root): autonomous mode (no seed provided this run)
- skills/mechanic-novelty/taxonomy-of-25-games.md: full reference taxonomy
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md, prior-games-index-format.md
- skills/design-constraints/core-knowledge-priors.md: priors envelope
- skills/code/id-generation.md: ID generation rules + reserved set
- prior-games/index.md: 36 prior entries (kf42 → zw91), latest cluster 2026-05-07/08
- skills/mechanism-details/cn04.md, sb26.md, sp80.md (for sample reference shape)
- prior-games/zw91/mechanism-detail.md (recent prior exemplar)

## Inputs not Consumed (rationale)
- Did NOT open every taxonomy deep-analysis or every prior `mechanism-detail.md`. Reasoning: candidate's coarse axes (graph topology + edge construction) diverge enough from any single existing entry that no taxonomy/prior row falls into the family-match → description-match flagged path of `similarity-check.md`. Will spot-check specific deep-analyses in critique_spec when re-running similarity against the fleshed-out spec.

## Deliverables Produced
- mechanic-pick.md: 4-char ID `jx5k`, family `constellation-edge-link`, full one-paragraph description, taxonomy near-miss table (10 entries), prior-games near-miss table (9 entries), negative-similarity walk-through against qm4t/bx84/bp35.

## Notes
- ID generation followed `code/id-generation.md`: lowercase alphanumeric, not in 25 reserved IDs, not in `prior-games/index.md`, not a recognisable English word.
- ACTION5's L1/L2 no-op behaviour was flagged as a potential checklist item-5 minimal-action concern; will revisit in critique. Alternative: only list ACTION5 in `available_actions` when it's actually active, but the engine treats `available_actions` as a static field. Acceptable interpretation: ACTION5 is in the enum because at L3 it carries the distinctive verb; at L1/L2 it is an idle slot the player can poke without effect (this matches the `_get_valid_actions` pattern from the universal scaffold — the action stays declared but is gated to no-op at the level handler).
- Mechanic explicitly draws from priors *Basic geometry & topology* (graph) + *Objectness* (nodes are persistent positioned entities). No physics, no agentness — keeps the prior-set tight per §3.4.
