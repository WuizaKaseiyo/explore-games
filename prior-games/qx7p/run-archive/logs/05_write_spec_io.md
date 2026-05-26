# Step #05: write_spec (round 2 — revising after critique)

## Inputs Consumed
- mechanic-spec.md (round 1).
- critique-revisions.md (round 1).

## Deliverables Produced
- mechanic-spec.md (revised in-place):
  - Issue 1: §5 rewrites action mapping. `available_actions = [1, 2, 5, 6]` global; ACTION5 gated to L3 only via `_get_valid_actions()`.
  - Issue 2: §3 sprite roster — chevron carets replaced with 3 × 3 yellow square bookend markers (`scan_line_marker_left/right`); "carets" wording purged.
  - Issue 3: §4 witnesses for L1, L2, L3 use shortest direction per column. Totals: L1 15, L2 15, L3 15. Step budgets unchanged.
  - Issue 4: §3 target patches grow from 6 × 3 flat fill to 8 × 5 with 1-px palette-3 grey border around 6 × 3 colour interior.

## Notes
- L2 witness was already minimal (issue 3 only affected L1 and L3).
- L3 witness drops from 23 → 15 actions; step budget 100 now ~6.6× witness — extremely generous, well over the difficulty-rules § d "be generous" floor.
- All four critique issues addressed concretely; round-2 critique should pass.
