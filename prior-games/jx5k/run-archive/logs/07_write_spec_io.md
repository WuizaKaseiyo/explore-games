# Step #07: write_spec (revision after critique visit #2)

## Inputs Consumed
- mechanic-spec.md (from #05): the post-visit-1 spec being patched.
- critique-revisions.md (from #06): 2 issues (L2 target/witness inconsistency; ACTION5 deselect semantics).

## Deliverables Produced
- mechanic-spec.md (revised): targeted text edits to:
  - §4 Level 2 *Layout* line: target degrees changed from `[2, 2, 2, 2, 4]` to `[3, 3, 3, 3, 4]`.
  - §4 Level 2 *Difficulty justification (c)* reasoning-chain bullet 3: "+1 degree" → "+2 degree" to match new targets.
  - §5 ACTION5 row: appended explicit "deselect after colour cycle" semantics.
  - §6 `self._selected_node` state-rule: explicit set / clear conditions enumerated.
  - Sections-changed manifest at top of spec updated.

## Notes
- All edits are local; no level-layout or witness changes were needed beyond the target-degree number.
- Verified the L2 witness against new targets:
  - 8 edges (4 radials + 4 perimeter) gives outer nodes degree = 1 (radial) + 2 (two adjacent perimeter edges) = 3 ✓; n4 degree = 4 ✓. Witness wins.
- Verified ACTION5 + selection-state walk-through for L2 and L3 witnesses:
  - L2 step 1-2: ACTION6 select n1; ACTION5 cycles + deselects. State after: no selection. ✓
  - L2 step 3: ACTION6 click n3 → no selection → select n3. ✓
  - L2 step 4: ACTION5 cycles + deselects. ✓
  - L2 step 5+: pair-click flow works as written. ✓
  - L3 same flow.