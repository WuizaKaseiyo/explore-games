# Step #05: write_spec (revision 2)

## Inputs Consumed
- mechanic-spec.md (existing — to revise)
- critique-revisions.md (from #04 critique_spec): 3 issues to address.

## Deliverables Produced
- mechanic-spec.md (revised in place):
  - § 3 Sprite roster: replaced `item_yellow_xcross` (X-pattern) with `item_yellow_checker` (2-pixel checkerboard); replaced `item_orange_diag` (diagonal stripe) with `item_orange_blob` (filled rounded square). Both rows annotated with the critique-pass-1 issue they address.
  - § 4 L3 *Setup*: removed wall at (2,10); kept wall at (5,10) as the east bound. Annotated with critique-pass-1 issue 1.
  - § 4 L1, L2, L3 setups + witnesses + counterfactuals: every textual reference updated from xcross/diag → checker/blob (sprite names, tag names, witness pickup-order phrasing, no-anchor counterfactual reverse-assignment).
  - § 3 preview row entry: `preview_yellow_xcross` / `preview_orange_diag` → `preview_yellow_checker` / `preview_orange_blob`.

## Notes
- All 3 critique issues addressed in a single pass; no other sections needed mutation.
- Self-consistency re-verified: L1 / L2 / L3 witnesses still produce target-matching final states given the renamed sprites; counterfactuals still hold (the rename is purely cosmetic — pickup order and reverse-assignment positions are unchanged).
- Transition to critique_spec for pass 2 (visit count will be 2/10).
