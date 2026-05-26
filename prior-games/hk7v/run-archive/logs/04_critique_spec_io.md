# Step #04: critique_spec

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec)
- skills/design-constraints/checklist.md (carried memory)
- skills/design-constraints/difficulty-rules.md (carried memory)
- skills/design-constraints/composition-and-tutorial.md (carried memory)
- skills/mechanic-novelty/* (carried memory)
- prior-games/index.md (carried memory)

## Deliverables Produced
- critique-revisions.md: 2 issues flagged. Spec must be revised before implement.

## Notes
- Trace-checked all three witnesses: L1 87 actions ✓, L2 actually 179 (spec says 171 — off by 8), L3 319 ✓.
- Trace-checked all per-mechanic counterfactuals: all hold concretely
  EXCEPT M2 (colour-pairing) at L1, which is trivially satisfied
  because L1 has only one colour. Per checklist 12, distinguishing
  behaviour of M2 is the colour comparison's *failure mode*; with
  one colour, no plausible alternate can trigger that failure, so
  M2 is decorative at L1.
- All checklist items 1-10, 13-22 pass. Item 11 (+1-or-+2 rule)
  passes whether L1 has 1 or 2 mechanics — the recount with L1=1,
  L2=3 (+2), L3=4 (+1) is cleaner and resolves the item 12 borderline.
- Novelty re-check vs full spec: still novel, no drift at L2 or L3.
- Negative-similarity 8-dimensional re-walk: candidate diverges from
  every prior on ≥5 dimensions; no prior shares 3+ dimensions.
