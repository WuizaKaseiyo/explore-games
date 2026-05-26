# Step #10: smoke_test (visit 1/6)

## Inputs Consumed
- prior-games/dh4j/dh4j.py
- mechanic-spec.md v3 (for witnesses + level descriptions)
- skills/code/smoke-test-checks.md (universal checks + custom-check template)

## Deliverables Produced
- workspace/smoke-frames/level_{1,2,3}.png (rendered initial frames)
- workspace/smoke-test-custom.py (4 custom mechanic invariant checks)
- workspace/smoke-test-pass.md (all checks pass)

## Notes
- All 9 universal checks pass (CHECK_VISUAL_SANITY confirmed by visual inspection of the 3 rendered PNGs — sprite counts match spec, layout matches, HUD present, no rendering bugs).
- All 4 custom mechanic-invariant checks pass: stride-1 walking, stride-3 leap-over-wall, filter legend toggle, pivot bonus arming + consumption.
- Visit 1/6. Transition to finalize.
