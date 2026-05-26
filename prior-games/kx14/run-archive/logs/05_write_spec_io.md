# Step #05: write_spec (round 2 — addressing critique-revisions.md)

## Inputs Consumed
- `workspace/critique-revisions.md` (from #04 critique_spec): one issue — L3 witness has a duplicate aborted-draft block; needs cleanup to a single canonical witness sequence.
- `workspace/mechanic-spec.md` (from #03 write_spec): the spec to revise. All other 9 sections passed critique.

## Deliverables Produced
- `workspace/mechanic-spec.md` (updated): only §4 → "Level 3" → witness was modified. The aborted draft block ("`ACTION3, ACTION3, ACTION3, ACTION3, ACTION3,   # tilt left ×5; orange (3,5)→… wait, see correction below`") and the "Correction:" preface are deleted. The new witness is presented as a single numbered sequence (1..21) with a per-action comment explaining the resulting ball position and water level. The bracketed click-pixel translation note is preserved.

## Notes
- Targeted edit only — every other section of the spec passed critique unchanged. No other sections touched.
- The new witness is functionally equivalent to the corrected block from round 1; the change is presentational. Same 21-action count, same mechanic exercise (M1+M2+M3+M4 each used at least once, M1 and M2 each used in both directions), same ending state (orange at (8,5), green at (3,5)).
- Quoted critique-revisions.md issue and noted the address explicitly in the spec block header so a future reviewer can confirm the fix corresponds to the flagged item.
