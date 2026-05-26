# Step #04: critique_spec

## Inputs Consumed
- `mechanic-spec.md` (from #03 write_spec).
- skills/design-constraints/checklist.md (22 items, from #01 study).
- skills/design-constraints/composition-and-tutorial.md, difficulty-rules.md (from #01 study).
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md (from #01 study).
- prior-games/index.md (60 entries, from #02 pick_mechanic context).

## Deliverables Produced
- `critique-pass.md`: per-item PASS verdicts for all 22 checklist items + novelty re-check (NOVEL). Notes for implementation re: witness pixel-precision and geometric tightening.

## Notes
- All 22 items pass (the state-file says "1-18" but the checklist itself defines 22 items; checked all 22).
- Most rigorous items (11, 12, 18, 19, 21): all pass with detailed counter-arguments.
- Most borderline near-miss is gx7m gear-mesh-cascade (sign-flip propagation through a mesh ↔ opposite-phase 2-pulley cable). Distinguishing rule recorded: scope difference (2-pair binary vs N-gear mesh).
- Implementation must tighten witness pixel-coords to match `CHECK_WITNESS_WINS`. Witness lengths are ~6, ~16, ~30 for L1/L2/L3; budgets are 30, 80, 150 (5× generous).
- Visit count for critique_spec: 1 of 10 (pass on first visit).

