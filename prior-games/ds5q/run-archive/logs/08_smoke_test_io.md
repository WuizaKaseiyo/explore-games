# Step #08: smoke_test (round 1)

## Inputs Consumed
- prior-games/ds5q/ds5q.py (from #07).
- workspace/mechanic-spec.md (round 2 from #05) — for witnesses + level descriptions.
- skills/code/smoke-test-checks.md — the 9 universal checks + custom-check guidance.

## Deliverables Produced
- workspace/smoke-test-custom.py — 4 custom checks (`check_arrow_moves_avatar`, `check_uncharged_erode_is_noop`, `check_charge_pad_sets_state`, `check_l3_layered_hardness`).
- workspace/smoke-test-pass.md — all universal + all custom checks PASS.
- workspace/smoke-frames/level_1.png, level_2.png, level_3.png — rendered initial frames for visual sanity inspection.

## Notes
- All 9 universal checks pass.
  - CAMERA_VIEWPORT: 64×64 == 64×64 every level.
  - SPRITE_CONTENT: 6/8/8 distinct non-letterbox palettes.
  - ACTION_BRANCHES: 5/5 actions referenced.
  - ACTION_RUNTIME: 5/5 actions run without exception.
  - PALETTE_RANGE: [0, 14] / [0, 15] / [0, 15].
  - WIN_PATH_EXISTS: `self.next_level()` found.
  - LOSE_PATH_EXISTS: `self.lose()` found.
  - WITNESS_WINS: L1 witness (9 actions) advances to L2; L2 witness (25) advances to L3; L3 witness (22) reaches WIN state.
  - VISUAL_SANITY: renderings match spec.
- All 4 custom checks pass.
- Visit count = 1 of 6 cap. Transition to finalize.
