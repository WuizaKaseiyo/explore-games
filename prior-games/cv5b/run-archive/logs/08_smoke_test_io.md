# Step #08: smoke_test (visit 1)

## Inputs Consumed
- prior-games/cv5b/cv5b.py (generated source)
- workspace/mechanic-spec.md (witnesses)
- skills/code/smoke-test-checks.md (Tier 1 universal + custom)

## Deliverables Produced
- workspace/smoke-test-custom.py (4 custom checks)
- workspace/smoke-test-pass.md
- workspace/smoke-frames/level_{1,2,3}.png

## Notes
- All 9 universal checks PASS: camera viewport, sprite content,
  action branches, action runtime, palette range, win path, lose
  path, camera-default, visual sanity.
- CHECK_WITNESS_WINS verified end-to-end: L1 → L2 → L3 → WIN state.
- 4 custom checks PASS: walk-right, cycle-power, L1-minimal-solve,
  lose-at-budget.
- Visual rendering looks clean: distinct sprites for launcher,
  shield, wind, targets; step-counter HUD visible at top.
