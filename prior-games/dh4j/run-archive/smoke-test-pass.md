# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera == level.grid_size = (64, 64) for every level |
| CHECK_SPRITE_CONTENT | 7 | 9 | 10 | distinct non-letter-box palette values per level (all ≥ 2) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions (1..4) referenced via GameAction.ACTIONn |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | every action runs without exception against a fresh game instance |
| CHECK_PALETTE_RANGE | 0..14 | 0..14 | 0..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels have grid_size (64, 64) — no per-level resize required |
| CHECK_WITNESS_WINS | PASS | PASS | PASS | replayed witnesses: L1 [UP, UP] → score 1; L2 [R, R, L, L, U, U, U] → score 2; L3 [R, U, R, R, L, L, L, U, U] → WIN |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered initial frames match spec: avatar + walls + goal + (L2 filter) + (L3 pivot + filter) all visible in correct grid positions; HUD legend chip + step counter visible; no chunky rendering. PNGs at `workspace/smoke-frames/level_*.png` |

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_stride_1_walks_one_cell | y0=40, y1=32 (-8 px) | UP press from a 1-pip yellow cell moves avatar one cell up |
| check_stride_3_leaps_over_wall | pre=(24, 32) → score=1 | UP press from the L1 stride-3 cell at (3, 4) leaps over the y=3 wall row and lands on the goal at (3, 1), advancing to L2 |
| check_filter_toggles_legend | pre=yellow, post=blue | landing on the L2 filter cell at (5, 5) toggles the legend from yellow to blue |
| check_pivot_arms_bonus_then_consumes_on_next_press | armed_bonus=1, armed_pivot=True, post_bonus=0, post_armed=None | landing on the L3 pivot at (3, 5) arms `_pending_bonus = 1`; the next press consumes both the bonus and the pivot cell, regardless of slide success |

Visit count: 1/6.
