# Step #08: smoke_test (PASS)

## Inputs Consumed
- prior-games/qx7p/qx7p.py.
- mechanic-spec.md (witness sequences extracted to ActionInput lists).
- skills/code/smoke-test-checks.md (universal check definitions).

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom checks.
- workspace/_smoke_runner.py: harness running universal + custom.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames.
- workspace/smoke-test-pass.md: PASS verdict per check.

## Notes
- All 9 universal checks pass (CHECK_VISUAL_SANITY judged from rendered PNGs).
- All 4 custom checks pass: action1-shifts, click-selects, bound-pair-couple, action5-cycles-scan-line.
- Visit count of `smoke_test` = 1/6.
- Used `_score` and `_state` (engine internals) for witness verification — `win_score` is a property reflecting max possible score, not progress.
