# Critique revisions for `mechanic-spec.md` — visit 1/10

## Issue 1 — L1 random-resistance too high

- **Violated rule**: `design-constraints/checklist.md` item 18 / `difficulty-rules.md` § 2.a — random / vision-blind agent must have **near-zero** chance of solving L1.
- **Offending spec section**: `mechanic-spec.md` § 4 Level 1 — *"Difficulty justification (a) Random-resistance: a uniform-random policy across the 4 valid actions {3,4,5,6} hits the witness sequence with probability (1/4)^4 ≈ 0.4% per consecutive 4-window. Over a 40-step budget there are ≈37 windows, giving cumulative success ≈ 14%."*
- **Why it fails**: 14% cumulative success is not "near-zero". The current witness is length 4 — too short for the 4-action vocabulary at L1 to dilute random-policy success below the threshold.
- **Concrete fix**:
  1. Change the base anchor cell from `(8, 32)` to `(16, 32)` in L1 (and align L2, L3 to the same base — the spec says "base at (8, 32) every level" but moving it uniformly is fine; alternatively the base can stay at (8, 32) for L2/L3 if the level-data dict allows per-level bases. To minimise per-level divergence, change the base to `(16, 32)` for all three levels; recompute the L2 and L3 witnesses).
  2. Change the L1 target from `(20, 8)` to `(4, 8)`.
  3. New L1 witness: `[ACTION3, ACTION3, ACTION5, ACTION3, ACTION5, ACTION3]` (length 6). Reaches pose `(W, N, N)` with tip `(4, 8)`.
  4. New random-resistance: P(uniform-4 hits a length-6 sequence) ≈ (1/4)^6 ≈ 0.024%; cumulative over 40 windows ≈ 0.85% ≈ near-zero. ✓

**Cascade**: moving the base affects L2 and L3 witnesses. Re-derive:

  - **L2** (target should now be at a position requiring length-adjust). Pick target `(8, 8)`. Required pose: from base `(16, 32)`, need tip `(8, 8)` = base + `(-8, -24)`. Pose `(W length 8, N length 12, N length 12)`: hinge_0 (16, 32) → seg_0 W8 → hinge_1 (8, 32) → seg_1 N12 → hinge_2 (8, 20) → seg_2 N12 → tip (8, 8). ✓
    - Witness: from (E12, E12, E12) active=0:
      - ACTION3 (θ_0 E→N), ACTION3 (θ_0 N→W). Pose (W12, E12, E12). Tip = (16-12, 32) + (12, 0) + (12, 0) = (4, 32) + (24, 0) = (28, 32). In bounds.
      - ACTION2 ×4 (L_0: 12→8). Pose (W8, E12, E12). Tip = (16-8, 32) + (12, 0) + (12, 0) = (8, 32) + (24, 0) = (32, 32). In bounds.
      - ACTION5 (active 0→1).
      - ACTION3 (θ_1 N). Pose (W8, N12, E12). Tip = (16-8, 32) + (0, -12) + (12, 0) = (8, 20) + (12, 0) = (20, 20).
      - ACTION5 (active 1→2).
      - ACTION3 (θ_2 N). Pose (W8, N12, N12). Tip = (16-8, 32) + (0, -12) + (0, -12) = (8, 8). ✓
    - Witness length: 2 + 4 + 1 + 1 + 1 + 1 = 10 actions.
    - Random-resistance: P(uniform-6) ≈ (1/6)^10 ≈ 1.7×10⁻⁸ per window; over budget 100 → cumulative ≈ 1.5×10⁻⁶. Near-zero. ✓
    - Step budget = 100 (10× witness, generous).

  - **L3** (object red and drop-zone red recomputed for new base). Place object red at `(8, 8)` (Manhattan reachable from base 16+24 = 40 ≤ 42; pose (W length 8, N12, N12) tip (8, 8) ✓). Place drop-zone red at `(28, 20)` (Manhattan from base 16+12 = 28 ≤ 42; pose (W4, N12, ? E):  hinge_0 (16, 32) → seg_0 W4 → hinge_1 (12, 32). Hmm tip needs to be (28, 20). From hinge_1 (12, 32), with seg_1 N12 → hinge_2 (12, 20). seg_2 ? to reach (28, 20): seg_2 E length 16 — exceeds max 14. Pose (E12, N12, E?): hinge_0 (16, 32) → hinge_1 (28, 32). seg_1 N12 → hinge_2 (28, 20). seg_2 E length 0? Not allowed. Hmm. Pose (E12, N12, ANY length 0)? Not allowed. So drop-zone (28, 20) needs pose (E12, N12, ?) with seg_2 of length needing tip exactly at (28, 20) without seg_2 displacement. Set seg_2 N length 0: tip stays at hinge_2 (28, 20). But length 0 invalid. Try (E14, N12, W2)? hinge_2 = (16+14, 32-12) = (30, 20). seg_2 W length 2 → tip (28, 20). ✓ Length-adjust required (extend seg 0 to 14, retract seg 2 to 2, rotate seg 2 W).

      Or simpler: drop-zone at (32, 20). Pose (E12, N12, E12) tip (16+12+0+12, 32-12+0) = (40, 20). Hmm.
      Pose (E12, N12, E?): tip x = 16+12+L_2 = 28+L_2. For tip (32, 20): L_2 = 4. Witness includes retract seg 2 from 12 to 4. Pose (E12, N12, E4). Tip = (28+4, 20) = (32, 20). ✓ This works without extending.

    Use drop-zone red at `(32, 20)`. Object red at `(8, 8)`.

    Witness L3:
      - **Phase 1 (pickup at (8, 8))**: from initial (E12, E12, E12) active=0.
        - ACTION3, ACTION3 (θ_0 E→N→W). Pose (W12, E12, E12).
        - ACTION2 ×4 (L_0 12→8). Pose (W8, E12, E12).
        - ACTION5 (active 0→1).
        - ACTION3 (θ_1 N). Pose (W8, N12, E12).
        - ACTION5 (active 1→2).
        - ACTION3 (θ_2 N). Pose (W8, N12, N12). Tip (8, 8). ✓ Object red picked up.
        - Phase 1 actions: 2 + 4 + 1 + 1 + 1 + 1 = 10.
      - **Phase 2 (drop at (32, 20))**: from current pose (W8, N12, N12) active=2.
        - ACTION4 (θ_2 N→E). Pose (W8, N12, E12). Tip = (16-8, 32) + (0, -12) + (12, 0) = (8, 20) + (12, 0) = (20, 20). Not target.
        - ACTION5 (active 2→0).
        - ACTION3, ACTION3 (θ_0 W→S→E). Two CCW rotates: W (180) → S (270) → E (0=360). Pose (E8, N12, E12). Tip = (16+8, 32) + (0, -12) + (12, 0) = (24, 20) + (12, 0) = (36, 20). Not target.
        - ACTION1 ×4 (L_0 8→12). Wait — need tip x = 32. With pose (E?, N12, E12): tip x = 16 + L_0 + 12 = 28 + L_0. For 32: L_0 = 4. So retract from 8 to 4 (ACTION2 ×4), not extend.
        - Re-derive: from (W8, N12, E12) we need pose `(E_or_W length L_0, N12, E12)` with tip x = 32. Pose options:
          - (E L_0, N12, E12): tip = (16 + L_0 + 0 + 12, 32 + 0 - 12 + 0) = (28 + L_0, 20). For x=32, L_0 = 4. Pose (E4, N12, E12). Tip (32, 20). ✓
          - (W L_0, N12, E12): tip = (16 - L_0 + 0 + 12, 20) = (28 - L_0, 20). For x=32, L_0 = -4. Invalid.
        - So target pose is (E4, N12, E12). From (W8, N12, N12) active=2:
          - ACTION4 (θ_2 N→E). Pose (W8, N12, E12). Active=2.
          - ACTION5 (active 2→0).
          - ACTION3 (θ_0 W→S). Pose (S8, N12, E12). hinge_1 = (16, 40). seg_1 N12 → hinge_2 (16, 28). seg_2 E12 → tip (28, 28). In bounds.
          - ACTION3 (θ_0 S→E). Wait, S CCW = ?. S = 270. CCW (+90) = 360 = 0 = E. ✓ Pose (E8, N12, E12). Tip = (16+8, 32) + (0, -12) + (12, 0) = (24, 20) + (12, 0) = (36, 20). 
          - ACTION2 ×4 (L_0 8→4). Pose (E4, N12, E12). Tip = (16+4, 32) + (0, -12) + (12, 0) = (20, 20) + (12, 0) = (32, 20). ✓
          - ACTION6 click @ (32, 20) → drop red.
        - Phase 2 actions: 1 + 1 + 2 + 4 + 1 = 9. Hmm let me recount: ACTION4 (1), ACTION5 (1), ACTION3 ×2 (2), ACTION2 ×4 (4), ACTION6 (1) = 9.
      - Total L3 witness: 10 + 9 = 19 actions.
    - Random-resistance: P(uniform-6)^19 ≈ (1/6)^19 ≈ 1.7×10⁻¹⁵. Astronomically near-zero. ✓
    - Step budget = 100. ≥ L2's. ✓ Witness 19 → buffer 5.3×.

**OR** simpler alternative: keep base at `(8, 32)` and just lengthen L1's witness via a different route.

Looking at the current L1 with base (8, 32): westward rotation of seg 0 puts hinge_1 at (-4, 32) — out of bounds and rejected. So we can't generate W-poses naturally. The 4-direction structure means the only N/S/W rotation that's in-bounds is rotating downstream segments.

Actually there's a simpler fix: keep base at (8, 32) and pick a target reachable only via 6-action witness without needing W poses.

**Simpler fix**: keep base at `(8, 32)`. Make L1 target = `(8, 8)`. Pose `(N, N, ?)`: hinge_0 (8, 32). seg_0 N12 → hinge_1 (8, 20). seg_1 N12 → hinge_2 (8, 8). seg_2 ? from (8, 8). For tip = (8, 8), seg_2 must contribute (0, 0) — only achievable with L_2 = 0 (invalid) or seg_2 = self-cancelling (e.g., a "loop" — also invalid given seg_2 has nonzero length).

Hmm — without length-adjust at L1, we can't get tip exactly at (8, 8) with all L=12.

Alternative target reachable with all 4 directions used at L1: pose `(N, E, S)`: hinge_0 (8,32). seg_0 N12 → (8, 20). seg_1 E12 → (20, 20). seg_2 S12 → (20, 32). Tip (20, 32). Witness: ACTION3 (hinge 0 N), ACTION5, [ACTION3 or stay E], ACTION5, ACTION4 (hinge 2 E→S). Length 5.

Pose `(N, N, E)`: tip (20, 8). Same as old target. Witness `[ACTION3, ACTION5, ACTION3]` (since seg 2 stays E by default). Length 3. Even shorter.

Let me re-examine what unique tips have witness ≥ 6:
- Need witness using rotation at all three hinges OR multiple rotations on one hinge.
- Pose (W, N, N) requires θ_0 = W (which is 180° rotation = 2 CCW or 2 CW from initial E). Plus rotations at hinges 1 and 2 (each 90°). Total 2 + 1 + 1 + 2 cycles = 6 actions. (Cycles: 0→1→2 = 2 ACTION5s.)
- But pose (W, N, N) at base (8, 32): hinge_1 (-4, 32). Out of bounds. Rejected.

So can't access W-pose at base (8, 32). 

Decision: **MOVE base to (16, 32)** for all three levels. Then W-pose is in-bounds and L1 witness can be length 6.

OK committing to base (16, 32). Re-derive ALL three levels.

Issue 1 fix specifics — see "Cascade" subsection above for L2 and L3 re-derived witnesses.

## Issue 2 — M1 wording is over-narrow

- **Violated rule**: internal consistency between `mechanic-spec.md` § 4 Level 1 (defining M1 as ACTION5-specific) and § 5 Action mapping (defining ACTION6 click on hinge as also setting active).
- **Offending spec section**: `mechanic-spec.md` § 4 Level 1 — *"M1 cycle-active-hinge — ACTION5 advances the active-hinge index modulo N_hinges…"*
- **Why it fails**: ACTION6 click-on-hinge also changes the active hinge (§ 5). The mechanic's *distinguishing behavior* is "active hinge changes"; both ACTION5 and ACTION6 implement this. The spec's wording suggests only ACTION5 does.
- **Concrete fix**: rename M1 to **"change-active-hinge"**. Update the description to: *"Two implementations: ACTION5 cycles the active-hinge index forward (modulo N); ACTION6 click on a hinge cell sets the active hinge directly to that hinge's index."* Update the counterfactual claim to: *"L1 cannot be solved without triggering M1 (change-active-hinge) because…"*. The structural counterfactual still holds — without ANY change to active hinge, only seg 0 is mutable.

## Summary of revisions needed

1. **Base relocation**: move base anchor from `(8, 32)` to `(16, 32)` for all three levels. This puts W-rotation in-bounds, enabling longer L1 witness.
2. **L1 target → `(4, 8)`**, witness length 6: `[ACTION3, ACTION3, ACTION5, ACTION3, ACTION5, ACTION3]`. Random-resistance ≈ 0.85% ≈ near-zero. ✓
3. **L2 target → `(8, 8)`**, witness length 10. Random-resistance ≈ 1.5×10⁻⁶. ✓
4. **L3 object_red at `(8, 8)`, drop_zone_red at `(32, 20)`**, witness length 19. Random-resistance ≈ 1.7×10⁻¹⁵. ✓
5. **M1 renamed** to "change-active-hinge"; description and counterfactual updated to mention both ACTION5 and ACTION6 paths.

Step budgets unchanged (40 / 100 / 100). All still generous over witness.
