# Step #04: critique_spec (visit 1)

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec)
- skills/design-constraints/checklist.md (read in study; verifying
  items 1-22)
- skills/mechanic-novelty/similarity-check.md (re-running on full
  spec)
- skills/mechanic-novelty/negative-similarity-check.md (re-running)
- skills/code/spec-template.md (re-checking 9-section structure)

## Deliverables Produced
- critique-revisions.md: 4 numbered issues (1 major, 1 major, 1
  minor, 1 major) + acceptance line for items 1-22 except 11/12/18
  which were partially flagged.

## Notes
- Major issue 1: L2's geometry allows an alternate path the avatar
  can walk to reach a cell BETWEEN the walls without ever crossing
  wall_short, breaking the M2 counterfactual. Concrete fix sketched.
- Major issue 2: L1 witness has two non-canonical sequences and
  ends with a defer-to-smoke-test note that violates the
  concrete-witness gate.
- Major issue 4: L3 witness is narrative only; explicit action list
  required.
- Minor issue 3: target_dim / target_lit need explicit
  collidable=False to permit avatar walk-through.
- Novelty: the fleshed-out spec did not drift from pick_mechanic's
  novelty position; 8-dim negative test re-walked vs vt6q with same
  1-dim overlap (step counter only).
