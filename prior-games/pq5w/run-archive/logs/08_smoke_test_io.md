# Step #08: smoke_test (visit 1)

## Inputs Consumed
- prior-games/pq5w/pq5w.py
- workspace/mechanic-spec.md (for witnesses)
- code/smoke-test-checks.md (universal-check templates + custom-check rules)

## Deliverables Produced
- workspace/smoke-test-runner.py (universal-check driver)
- workspace/smoke-test-custom.py (4 custom-check functions)
- workspace/smoke-frames/level_{1,2,3}.png (rendered initial frames)
- workspace/smoke-test-pass.md (one row per check, all ✅)

## Notes
- Hit one bug in the runner: `GameAction(int)` raised
  ValueError because the enum values aren't ints. Fixed by using
  `GameAction.from_id(int)` per the smoke-test-checks template.
- All universal checks PASS on first iteration of the runtime; the
  spec's witnesses for L1 (5 actions), L2 (7 actions), L3 (8
  actions) advance the game from L1 → L2 → L3 → WIN as expected.
- All 4 custom checks PASS.
- Visual-sanity PASS: all three rendered initial frames show the
  spec's described scenes (avatar/portals/walls/goal/forbidden +
  HUD bar) in the right regions, with sprite shapes carrying the
  intended visual cues.
- Visit count: 1/6 — well under the cap.
- Transitioning to finalize.
