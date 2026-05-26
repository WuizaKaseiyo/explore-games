# Step #08: smoke_test (visit 1)

## Inputs Consumed
- prior-games/tk6n/tk6n.py
- prior-games/tk6n/metadata.json
- mechanic-spec.md (revision 2)
- skills/code/smoke-test-checks.md

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom checks (boomerang launch,
  avatar walk, boom-advance-1-per-tick, lose-at-budget).
- workspace/smoke-test-pass.md: all 10 universal + 4 custom checks
  PASS.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames.

## Notes
- Visual sanity confirmed via L1/L2/L3 PNG inspection: avatar is the
  yellow-rimmed blue square with east-pointing eye-dot, target is
  the magenta/pink starburst, walls render as expected (crossbar
  perimeter for wall_tall, horizontal stripe for wall_short), guard
  in L3 is the dark-red hexagonal silhouette.
- All three witness sequences from the spec advance the level:
  L1 in 13 actions (budget 30), L2 in 33 actions (budget 60),
  L3 in 70 actions (budget 100). All comfortably within budget.
- No revisions required. Transition to finalize.
