# Step #05: write_spec (revision 1)

## Inputs Consumed
- workspace/critique-revisions.md (the 2 issues from #04)
- workspace/mechanic-spec.md (the prior version)
- skills/design-constraints/{checklist.md, difficulty-rules.md}

## Deliverables Produced
- workspace/mechanic-spec.md updated with two changes:
  - **Issue #1 fix (L3)**: tray composition changed `[m2,m2,m1,m1] → [m2,m2,m2,m1]`. Re-derived counterfactual statements for M2 and M3, re-derived witness (8-action sequence: m1@+2, m2@-1, m2@-3, m2@+3 — triggering M3 once at step 6 with passenger drifting +2→+1), re-derived difficulty (c) (heuristic that fails: counter-stack-against-passenger leads to passenger landing on slot 0 = off-beam = lose at step 2).
  - **Issue #2 fix (sprite)**: `weight_blue` (mass-2) redesigned from "doubled-ring" to "single elongated 4×8 frame" — palette 9 outer frame, palette 5 inner solid fill. No glyph resemblance.

## Notes
- Verified the new L3 counterfactual: every torque-zero solution for `2a+2b+2c+d=0` with `[m2×3, m1×1]` requires both m2@-3 AND m2@+3 (m1 must be at ±2, leaving the three m2 arms summing to ∓1, which forces extreme arms ±3). So every winning sequence places at least one m2@±3, contributing ±6 to tilt_raw → triggers M3 (`|tilt_level| ≥ 2`). M3 is genuinely necessary.
- Verified the new witness path lands passenger safely at +1 at end (still on exposed_arms).
- Verified that the "heavy-first counter-stack" heuristic loses the passenger at step 2 (passenger drifts +2→+1 then +1→0=fulcrum=off-beam).
- All other spec sections unchanged.
- Re-entering critique_spec for visit 2.
