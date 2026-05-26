# Step #08: smoke_test (visit 1)

## Inputs Consumed
- prior-games/pf3w/pf3w.py (from #07 implement).
- prior-games/pf3w/metadata.json.
- skills/code/smoke-test-checks.md (universal check definitions + custom-check template).
- mechanic-spec.md (for visual sanity comparison).

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom-check functions following the template constraints (≤ 5 setup actions, single boolean assertion, deterministic, < 1 second runtime each).
- workspace/smoke-frames/level_1.png, level_2.png, level_3.png (rendered initial frames at 512×512 using the spec's RGB palette).
- workspace/smoke-test-pass.md: 9 universal checks + 4 custom checks all PASS.

## Notes
- All 9 universal checks pass on first attempt.
- 4 authored custom checks all pass: ACTION6 activation, ACTION5 tick advance, L1 minimal solve, lose-at-budget.
- Visual sanity inspection of all 3 rendered initial frames confirms sprite count, placement, HUD presence, and absence of catastrophic rendering bug per spec § 4. The 4×4-pixel logical-cell rendering with hollow-frame and filled-frame templates per cell looks clean — sprites are clearly multi-cell shapes (3×3 cells = 12×12 px) with internal sub-cell pattern.
- Minor UX observation (not a failure): in L3, both dim slots render as grey hollow crosses (no color hint until activation). The player must activate to discover which slot is which color. This is acceptable per the spec's "no on-screen text" principle and the discovery-by-play pattern; future polish could add a small color indicator on each dim slot.
- Visit count: 1/6 (well below cap).
- Ready to proceed to finalize.
