# Step #06: smoke_test

## Inputs Consumed
- `prior-games/gx7m/gx7m.py` (from #05).
- skills/code/smoke-test-checks.md — the 9 universal checks + the custom-check template.
- workspace/mechanic-spec.md — for the visual-sanity comparison.

## Deliverables Produced
- workspace/smoke-test-pass.md — 9 universal checks ✅, 4 custom checks ✅.
- workspace/smoke-test-custom.py — 4 mechanic-specific checks (one each for: disc rotation on click, cascade sign flip across mesh, ratchet-blocked no-op, clutch disengage isolation).
- workspace/smoke-frames/{level_1,level_2,level_3}.png — rendered initial-state PNGs of all 3 levels.

## Notes
- All 9 universal checks pass on first visit; no fix_implementation loop needed.
- Custom checks exercise the three named mechanics (cascade, ratchet, clutch) at minimum once each. Each check uses ≤ 5 setup actions, ONE action under test, and ONE boolean assertion — conforms to the strict template.
- L2/L3 visual layout has the tang sprites rendering on the east interior of their owner-disc's collar frame (because frames abut and there is no gap between adjacent collars). The tangs remain functionally correct (clicks at tang coords still cycle the owner's state) and visually legible in the rendered PNGs. Acceptable per CHECK_VISUAL_SANITY (no catastrophic bug; no letter/digit resemblance).
- Visit count for smoke_test: 1 of 6 (revision cap untouched).
