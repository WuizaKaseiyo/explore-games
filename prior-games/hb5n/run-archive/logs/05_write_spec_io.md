# Step #05: write_spec (revision pass #1)

## Inputs Consumed
- critique-revisions.md (from #04 critique_spec): single load-bearing issue identified (M4 fails strict counterfactual)
- mechanic-spec.md (from #03 write_spec): prior draft to edit

## Deliverables Produced
- mechanic-spec.md (updated): replaced M4 = "rotation-lock" with M4 = "pivot-reset" throughout. Updated §1 title, §2 mechanic-family paragraph, §3 sprite roster (removed `rotation_lock`, added `pivot_reset`; replaced `target_slot_j_rot90` with `target_slot_t_b_pivot_rot90`), §4 L3 in full (new layout, new B-pivot mechanics derivation, new witness, new necessity table, new difficulty justification), §5 action mapping (clarified ACTION5's pivot dependence), §6 added `anchor_index` state and `pivot_reset_cells` set, §9 added pivot-reset distinguishing rules vs nz3v and pv5q.

## Notes
- The pivot-reset mechanic transfers the anchor designation from cell A to cell B (the cell at relative offset (-1, 0) in the rotation-0 frame). The avatar's relative-cells list is re-baselined so B becomes the new (0, 0).
- Why this passes strict counterfactual: the A-pivot 4-cell J's 4 rotations all produce asymmetric J/L silhouettes. The B-pivot 4-cell shape (cells at B(0,0), A(1,0), C(0,1), D(0,-1) after re-baselining) produces 4 different silhouettes — including a T-shape at rotation 90. The target slot is a T, so M4 is the unique path to a winning configuration.
- L3 layout simplified to outer ring + 2 small decorative wall clusters; the geometric necessity (T vs J/L) provides the planning challenge, not maze navigation.
- Witness L3 = 20 actions (1 less than the original draft). Budget 80, generous.
- After revision, critique re-runs (next step) should pass cleanly.
