# Step #08: smoke_test

## Inputs Consumed
- prior-games/hk7v/hk7v.py (built in #07)
- mechanic-spec.md (carried)
- skills/code/smoke-test-checks.md (newly read)
- workspace/smoke_test_custom.py (authored this state)

## Deliverables Produced
- workspace/smoke-test-custom.py (4 custom checks)
- workspace/smoke_test_custom.py (importable copy of the same)
- workspace/smoke-frames/level_1.png, level_2.png, level_3.png
  (rendered initial frames per level)
- workspace/smoke-test-pass.md (verdict PASS)

## Notes
- All 10 universal checks pass. CHECK_WITNESS_WINS replays the spec
  witnesses for L1, L2, L3 against the loaded game and each
  advances/wins as expected (L1 score 0→1, L2 score 1→2, L3 reaches
  WIN state).
- All 4 custom checks pass: trolley horizontal motion, hook descent
  stops at block top, grab attaches block to hook, lose triggers at
  step budget exhaustion.
- Visual sanity inspected manually from rendered PNGs: each level's
  scene matches spec (sprite counts and positions; HUD visible).
- Visit count to smoke_test: 1/6 (well within budget).
