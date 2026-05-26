# Step #04: critique_spec (visit 1 of max 10)

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec)
- design-constraints/checklist.md (items 1-22)
- mechanic-novelty/similarity-check.md
- mechanic-novelty/negative-similarity-check.md
- prior-games/index.md

## Deliverables Produced
- critique-revisions.md: 11 issues (8 critical, 3 sub-critical),
  each with checklist-item violation, offending quote, and concrete
  fix. Action-items list for revision.

## Notes
- Major holes in L3 geometry: cap counterfactual fails (alt y-paths
  bypass cap), flipper counterfactual fails (vy-routing bypasses
  hazard).
- Multi-axis velocity behavior was hand-waved in spec; real action
  model permits diagonal velocity.
- L3 step budget shrank from L2's 50 to 40 — violates difficulty-
  rules § 2.d.
- Cultural-color violations: target green-ring, hazard red-spikes.
- Flipper hatched-X reads as letter / multiplication symbol.
- Non-trivial revision required. Transitioning back to write_spec.
