# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == grid_size (64,64) per level |
| CHECK_SPRITE_CONTENT | 4 | 5 | 7 | distinct non-letter-box palette values |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions [1,2,3,4] referenced in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions |
| CHECK_PALETTE_RANGE | 1..14 | 1..14 | 1..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | next_level() in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | lose() in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size=(64,64); per-level resize not needed |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity notes
- **L1**: green avatar dot at left, two light-blue phase-2 frames (yellow centre dots, both currently open) along the middle row, yellow goal ring at the right edge. Wall ring around the whole field. Step-counter HUD as a yellow bottom-row bar. Matches spec § L1. PASS.
- **L2**: same row layout as L1 plus a solid-black square between the two pulsing tiles — this is the phase-3 tile rendering its currently-closed variant at step 0 (offset 1, 0%3=0 ≠ 1). Will pulse to magenta after the first action. Matches spec § L2. PASS.
- **L3**: avatar top-left corner; row-1 corridor with phase-2 (open, light-blue) and a solid-black square (phase-3 currently closed at step 0); row-2 wall barrier with the single gap at col 10; col-10 corridor descending between bracket walls; phase-4 currently-closed (solid black) at (10,5); fragile-phase-3 currently-open (magenta with red top-left corner pixel) at (10,12); yellow goal ring at (10,14). Matches spec § L3. PASS.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_right_moves_avatar | x0=4 x1=8 | ACTION4 on plain floor moves avatar east one logical cell (4 px) |
| check_phase_tile_blocks_on_wrong_residue | x_before=12 x_after=12 | phase-2-off-0 rejects entry at step 3 (3%2=1 ≠ 0) — avatar stays at (3,5) |
| check_step_counter_ticks_on_blocked_move | n0=0 n1=1 x=4 | wall-bounce LEFT against perimeter ticks counter without moving avatar |
| check_lose_at_budget | final_state=GAME_OVER | exhausting L1 budget of 22 via wall-bounces fires GAME_OVER |

Visit count: 1/6.
