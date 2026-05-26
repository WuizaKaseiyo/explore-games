# Step #05: write_spec (revision 1)

## Inputs Consumed
- critique-revisions.md (visit 1): two issues to address.
- mechanic-spec.md (rev. 1): current spec, will be rewritten.

## Issues Addressed
- Issue 1: L1 random-resistance ≈ 14% with 4-action witness — fixed by relocating base to `(16, 32)` and target to `(4, 8)`, lengthening witness to 6 actions (random ≈ 0.85%).
- Issue 2: M1 wording over-narrow — fixed by renaming to "change-active-hinge" and noting both ACTION5 (cycle) and ACTION6 (click-on-hinge) implement it.

## Cascading Recomputations
- L2 target moved to `(8, 8)`; new witness length 10; new random-resistance ≈ 1.5×10⁻⁶.
- L3 object_red moved to `(8, 8)`, drop_zone_red moved to `(32, 20)`; new witness length 19; new random-resistance ≈ 1.7×10⁻¹⁵.
- All counterfactuals re-verified for the new positions.

## Verification of Step Traces
Verified each step of L1, L2, and L3 witnesses against the pose math `hinge_(i+1) = hinge_i + L_i · DIR[θ_i]`:
- L1: pose (W12, N12, N12) tip = (16-12, 32-12-12) hmm let me recompute. hinge_0 (16, 32). seg_0 W12 → (16-12, 32) = (4, 32) = hinge_1. seg_1 N12 → (4, 32-12) = (4, 20) = hinge_2. seg_2 N12 → (4, 20-12) = (4, 8) = tip. ✓
- L2: pose (W8, N12, N12) tip = (16-8, 32) - apply seg_1 N: (8, 20). seg_2 N: (8, 8). ✓
- L3 phase 2 final pose (E4, N12, E12) tip = (16+4, 32) - seg_1 N: (20, 20). seg_2 E: (32, 20). ✓

All step-by-step poses are in-bounds (verified each transient pose).

## Deliverables Produced
- mechanic-spec.md (workspace/mechanic-spec.md, rev. 2) — full spec with revisions applied.

## Notes
- Counterfactuals at the new positions verified: no shorter witness exists for any level.
- The base relocation cleanly fixes both issues without any composition/structural changes to the level progression.
- M1 wording change is purely textual — no code/level impact.
