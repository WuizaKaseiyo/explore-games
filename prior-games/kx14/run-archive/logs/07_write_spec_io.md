# Step #07: write_spec (round 3 — addressing critique-revisions.md round 2)

## Inputs Consumed
- `workspace/critique-revisions.md` (round 2): two issues — Issue 2 (L1 witness count off-by-one), Issue 3 (re-projection pseudocode high/low semantics inverted).
- `workspace/mechanic-spec.md`: the spec to revise.

## Deliverables Produced
- `workspace/mechanic-spec.md` (updated): two targeted edits.
  - §4 → "Level 1" → witness header: "(10 actions)" → "(9 actions)"; companion sentence "fires after the 10th action" → "fires after the 9th action".
  - §6 → re-projection pseudocode: rename `_highest_platform_in_col_in_range` → `_max_platform_row_in_col_in_range`; rename `_lowest_platform_in_col_in_range` → `_min_platform_row_in_col_in_range`; rewrite the inline comments to explicitly state the row-coord convention (row 0 = top, row 11 = bottom) and the "closest from below / closest from above" intuition so a future reader cannot mis-translate the helper-function names.

## Notes
- Both edits are surgical — no other section of the spec was touched.
- The witness traces in §4 (L1, L2, L3) were already derived from the *correct* physics (the ones described by the rewritten pseudocode); only the algorithmic documentation was wrong, so no per-level re-tracing was needed. The L2 witness has a "blocked at platform row 6" comment that depends on the max-platform-row semantics — that's the case we want to enforce.
- Issue 1 (round 1, L3 witness duplicate-block) and Issues 2-3 (round 2) all addressed across rounds; the spec should now pass critique cleanly.
