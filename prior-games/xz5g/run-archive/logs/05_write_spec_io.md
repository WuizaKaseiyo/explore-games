# Step #05: write_spec (revision pass)

## Inputs Consumed
- mechanic-spec.md (visit #03 draft)
- critique-revisions.md (visit #04): 4 revision items.
- skills/code/spec-template.md
- skills/design-constraints/{checklist,difficulty-rules}.md (re-checked)
- skills/conventions/reference-game-patterns.md (no-hidden-state cue rules)

## Deliverables Produced
- mechanic-spec.md (revised in place):
  - Added revision-history block.
  - § 3 sprite roster: explicit pixel matrices for avatar,
    avatar_target, companion, companion_target; anchor_pin
    redefined as visit-checkpoint with stamped-state pixel
    variants.
  - § 4 L3: M4 redefined as visit-checkpoint (was: rejection-
    on-collide). Layout updated — anchor_pin moved (52, 32)
    → (12, 32) so CCW1 path lands avatar on it. Witness
    re-traced; M4 now observably triggered. L3 (b) human
    discovery pathway narrated step-by-step. L3 (c) trivial
    heuristic re-described to match new visit-clause failure
    mode. L3 (d) step budget restored to 50 (≥ L2's 30 per
    don't-shrink rule).
  - § 5 ACTION5: rejection rules clarified (out-of-bounds +
    rotatable-rotatable collision, no anchor_pin rejection);
    visit-checkpoint update appended.
  - § 6 internal state: added `_visited_pins`.
  - § 6 visible cues: anchor_pin visit-state cue (palette 14
    → 11), rejection cue.
  - § 7 win predicate: dual-clause (target-match AND
    visit-checkpoint).
  - § 8: clarified rejection no longer applies to anchor_pins.
  - § 4 L2 (a) random-resistance: prose tightened to own the
    soft "near-zero" framing; centred-symmetry layout retained
    for pedagogical reasons.

## Notes
- All four critique items addressed.
- Spec is internally consistent: L1/L2/L3 witnesses verified
  against rotation formulas; sprite-coord arithmetic
  re-checked end-to-end.
- Self-recheck against checklist 1-22:
  - Item 12 (strict counterfactual): all 10 (mechanic, level)
    pairs now have observable triggers in the witness.
  - Item 18 (difficulty floor/ceiling): all four bullets
    present per-level.
  - Item 22 (ACTION7): omitted; safe.
  - All other items: pass.
- Transition: critique_spec for final re-review.
