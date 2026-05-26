# Step #05: write_spec (revision)

## Inputs Consumed
- mechanic-spec.md (existing, from #03)
- critique-revisions.md (from #04)

## Deliverables Produced
- mechanic-spec.md (revised in place):
  - L1 mechanic count reduced from 2 (M1+M2) to 1 (M1 only); M2's
    decoratively-listed L1 row removed; necessity rewritten with
    plausible alternates that trip on M1.
  - L2 header `N+1 = 3` → `N+2 = 3`; M2 explicitly tagged as newly
    introduced at L2 alongside M3.
  - L2 witness count `171` → `179`. Difficulty justification (a)
    exponent updated `5⁻¹⁷¹` → `5⁻¹⁷⁹`. Step budget ratio updated.
  - L2 difficulty (b) Human-tractable updated to mention both
    M2 and M3 as new mechanics.
- L3 unchanged (counterfactuals + witness already correct).

## Notes
- Functional gameplay, sprite roster, action mapping, and
  win/lose conditions are unchanged. Only the mechanic-counting
  framing and one numeric off-by-8 typo were touched.
- Per the harness's revision-cap rule, this is round 1 of write_spec
  re-entry (revision-cap is 10 critique_spec entries).
