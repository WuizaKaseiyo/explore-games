# Step #06: smoke_test

## Inputs Consumed
- prior-games/lq5x/lq5x.py (from #05 implement): the generated game source.
- workspace/mechanic-spec.md: per-level layout descriptions used for visual sanity.
- workspace/implement-summary.md: confirmed witness sequences.
- skills/code/smoke-test-checks.md: 8 universal checks + custom-check template + visual-sanity protocol.

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom checks (`check_walk_moves_lantern`, `check_action5_rotates_facing`, `check_wax_pickup_extends_range`, `check_l1_minimal_solve`) — each follows the strict template (≤5 setup actions, 1 action under test, 1 boolean assertion).
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames per level.
- workspace/smoke-test-pass.md: 8 universal checks + 1 visual sanity (per level) + 4 custom checks all PASS.

## Notes
- All 8 universal checks pass on first attempt. No bugs surfaced beyond the one fixed during the implement state's smoke-test.
- Visual sanity verified by reading the three level_*.png frames against the spec § L1/L2/L3 layout — sprite count matches (3/4/5 game-element clusters), quadrant placement matches, HUD bar visible at bottom row of each, no sprite resembles a digit or letter at the rendered scale, and the cone overlay correctly paints the cone region in off-white (yellow cone) for L1/L2 facing N and L3 facing E.
- All 4 custom checks pass: walk moves lantern by 1 cell; ACTION5 increments facing mod 4; L2 wax pickup increments cone_range from 2 to 4 on pickup; L1's 5-action witness solves L1 cleanly.
- Visit count: 1/3. The transition condition for `finalize` (every universal + every custom check returns PASS) is satisfied. Proceeding.
