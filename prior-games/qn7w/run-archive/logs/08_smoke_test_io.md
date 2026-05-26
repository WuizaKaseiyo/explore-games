# Step #08: smoke_test (visit 1)

## Inputs Consumed
- prior-games/qn7w/qn7w.py (the implemented game)
- mechanic-spec.md (witness sequences for L1, L2, L3)
- skills/code/smoke-test-checks.md (10 universal checks + custom-check template)

## Deliverables Produced
- smoke-test-custom.py: 4 custom checks (one per essential mechanic invariant — pulse-eject end-to-end, junction-cycle, dead_end_wall consumption, merge_pad two-deposit fill).
- smoke-test-pass.md: per-check verdict table with universal + custom; 10/10 universal PASS + 4/4 custom PASS.
- smoke-frames/level_1.png, level_2.png, level_3.png — rendered initial frames per level.

## Notes
- All universal checks PASS:
  - CHECK_CAMERA_VIEWPORT: camera (64,64) matches grid (64,64) for all 3 levels.
  - CHECK_SPRITE_CONTENT: 4/6/8 distinct palette values per level (well above the ≥2 threshold).
  - CHECK_ACTION_BRANCHES + CHECK_ACTION_RUNTIME: ACTION6 declared and branched and runs without exception.
  - CHECK_PALETTE_RANGE: all rendered pixels within [0, 15] for every level.
  - CHECK_WIN_PATH_EXISTS: `self.next_level()` is in source.
  - CHECK_WITNESS_WINS: L1 witness (1 click) advances 0→1; L2 witness (2 clicks) advances 1→2; L3 witness (4 clicks) reaches WIN state.
  - CHECK_LOSE_PATH_EXISTS: `self.lose()` is in source.
  - CHECK_CAMERA_DEFAULT: all levels are 64×64; resize is defensive but present.
  - CHECK_VISUAL_SANITY: all 3 rendered frames match spec layouts (sprite count, placement, HUD presence).
- All 4 custom checks PASS, end-to-end exercising the four essential invariants of the mechanic.
- L3 visual sanity — note the merge_pad's orange centre pip is small and could blend with the orange ball-highlight palette in some viewing conditions; this is a cosmetic concern, not a failure. The pad is clearly the convergence point in the rendering.
- No revisions needed; first-visit pass. Visit count: 1 of 6.
- Transitioning to `finalize`.
