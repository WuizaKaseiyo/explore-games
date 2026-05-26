# Step #08: smoke_test

## Inputs Consumed
- prior-games/hb5n/hb5n.py: the generated source.
- prior-games/hb5n/metadata.json: metadata.
- mechanic-spec.md: per-level witness sequences for CHECK_WITNESS_WINS.
- skills/code/smoke-test-checks.md: 10 universal checks + custom-check template.

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom check functions exercising essential mechanic invariants (east translates anchor, rotate changes silhouette, pickup grows avatar, wall blocks translation).
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames for CHECK_VISUAL_SANITY.
- workspace/smoke-test-pass.md: PASS verdict per check.

## Notes
- All 10 universal checks PASS on first attempt: camera viewport matches grid_size (64,64); 8-10 distinct non-letter-box palette values per level; every declared action (1..5) has a branch and runs without exception; rendered pixels are in [1, 14]; `next_level()` and `lose()` both reachable; CHECK_WITNESS_WINS replays all 3 spec witnesses end-to-end and reaches WIN state with score=3.
- CHECK_VISUAL_SANITY: agent inspected the 3 PNGs and confirmed each matches the spec's layout (avatar at top-left, target slot at bottom-right, pickup adjacent to avatar at L2/L3, pivot-reset visible at L3, HUD bottom-row, wall ring). No letters/digits/clipart; no catastrophic rendering bug.
- 4 custom checks PASS: all essential mechanic invariants verified (movement, rotation, growth, wall collision).
- Visit count: 1/6. No revisions needed.
- Transition to finalize.
