# Step #10: smoke_test (round 1 — clean pass)

## Inputs Consumed
- `prior-games/kx14/kx14.py`: the just-implemented game source (512 lines).
- `workspace/mechanic-spec.md`: per-level layout + mechanic descriptions for the visual sanity pass.
- `skills/code/smoke-test-checks.md`: full Tier-1 check spec including custom-check template and constraints.

## Deliverables Produced
- `workspace/smoke-test-custom.py`: 3 custom checks (within the 2-4 range), each conforming to the template (≤ 5 setup actions, 1 action under test, 1 boolean assertion, deterministic, ≤ 1s wall-clock).
- `workspace/smoke-frames/level_{1,2,3}.png`: rendered initial frames for each level (used for the visual sanity pass).
- `workspace/smoke-test-pass.md`: per-level PASS table for the 9 universal checks + 3 custom checks.

## Notes
- **All 9 universal checks pass cleanly.** No camera viewport mismatch, no sprite-content emptiness, all action slots branched and runtime-safe, palette range within [0, 15] for every level, `next_level()` and `lose()` reachable, per-level camera resize present.
- **Visual sanity per level matches the spec.** L1: 1 ball + 1 target on a water/air cross-section, both correctly placed. L2: 1 ball + 1 target + 1 platform (left side), correctly placed. L3: 2 balls (orange + green) + 2 colour-matched target rings + 1 middle platform, correctly placed. HUD step bar at top edge in all 3 frames. Background palette is light grey for air + light blue for water; balls are orange + green internally-patterned 5×5 sprites; platform is a 15×5 grey bar with black edges. Visual signature confirmed distinct from priors kf42 (dark walled box + tiny coloured pawns) and qz73 (grey field + small radial tips).
- **Custom checks chosen to exercise each of the three player-facing mechanics across the three levels:** raise (M1), tilt (M2), anchor (M4). The platform mechanic (M3) is exercised implicitly by the visual sanity check showing the platform sprite at the right position; a custom check would have to use ≥ 5 setup actions to trigger a platform-block, which exceeds the template constraint.
- **Visit count check:** this is the 1st entry to `smoke_test` (state_log row count = 1). Within the 3-visit cap with 2 visits to spare.
- **Transition:** → `finalize`. All checks pass, no failures to fix.
