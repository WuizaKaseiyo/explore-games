# Step #06: smoke_test

## Inputs Consumed
- prior-games/zd7m/zd7m.py (from #05)
- prior-games/zd7m/metadata.json (from #05)
- mechanic-spec.md (for visual-sanity reference)
- skills/code/smoke-test-checks.md (universal + custom check definitions)

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom checks (cohort-step,
  anchor-blocks-yellow-right, portal-teleports-yellow, lose-at-budget).
- workspace/smoke-test-universal.py: scriptable runner for the 8
  programmatic universal checks + PNG renderer.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames.
- workspace/smoke-test-pass.md: structured pass report.

## Notes
- Initial L3 render had portal_b at (17, 17) overlapping target_yellow
  at the same cell with both at layer=0; portal renders on top hid
  the target colour. Fixed by raising target sprite to layer=1
  (portal stays at layer=0).
- All 8 universal automated checks pass on the first try.
- All 4 custom checks pass on the first try.
- Visual sanity pass on L1, L2, L3 PNGs: PASS.
- Visit count: 1/6 — no fix_implementation loop needed.
