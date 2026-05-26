# Step #08: smoke_test (visit 1 of ≤6)

## Inputs Consumed
- prior-games/kg7p/kg7p.py and metadata.json (from #07).
- mechanic-spec.md (from #05): witness solutions for L1, L2, L3.
- skills/code/smoke-test-checks.md (from harness): the 10 universal checks + custom-check template.
- skills/global/* (from harness): action enum, color legend.
- novaengine package (read for NovaBaseGame / Level / Camera signatures).

## Deliverables Produced
- workspace/smoke-frames/level_1.png, level_2.png, level_3.png — rendered initial frames at 64×64 scaled to 512×512 for inspection.
- workspace/smoke-test-custom.py — 4 custom checks (check_east_moves_avatar, check_action5_toggles_beam, check_beam_couples_block_on_walk, check_lose_at_budget). Each conforms to the constraints in code/smoke-test-checks.md § Custom checks: ≤ 1 s wall-clock, fully deterministic, ≤ 5 setup actions, single boolean assertion.
- workspace/smoke-test-pass.md — full table with PASS/observed values per check per level; visual-sanity notes per level; verdict.

## Notes
- Universal checks:
  - CHECK_CAMERA_VIEWPORT: PASS (camera 64×64 matches level grid_size).
  - CHECK_SPRITE_CONTENT: L1=7, L2=7, L3=8 distinct non-letter-box palette values (well above the ≥2 threshold).
  - CHECK_ACTION_BRANCHES: every action ID 1..5 referenced in step().
  - CHECK_ACTION_RUNTIME: each action runs without exception on a fresh game.
  - CHECK_PALETTE_RANGE: 4..15 for every level (within [0, 15]).
  - CHECK_WIN_PATH_EXISTS / CHECK_LOSE_PATH_EXISTS: both PASS.
  - CHECK_WITNESS_WINS: all three spec witnesses (L1 9 actions, L2 29 actions, L3 25 actions) advance their respective levels — STRONG signal that the implementation matches the spec.
  - CHECK_CAMERA_DEFAULT: not needed (all levels share grid_size (64, 64)).
  - CHECK_VISUAL_SANITY: all three rendered frames match the spec's sprite roster + layout. L2's target_orange is hidden beneath the avatar at level start (target is INTANGIBLE on layer 1, avatar on layer 4) but is revealed once the avatar walks — acceptable, the spec calls this out.
- Custom checks: 4/4 PASS.
- Visit count: 1 of ≤6.
- The on-disk artefacts (smoke-test-custom.py, smoke-test-pass.md, smoke-frames/) were already present from a prior run with the same run_id; their contents were verified against the current implementation and confirmed accurate.
