# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == grid_size (64,64) for all levels |
| CHECK_SPRITE_CONTENT | 5 | 7 | 9 | distinct non-letter-box palette values |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | ACTION1-4 all branched in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions; _action_count increments |
| CHECK_PALETTE_RANGE | 1..12 | 0..14 | 0..14 | all within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | self.next_level() found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 (32 actions) → score 1; L2 (27 actions) → score 2; L3 (23 actions) → WIN, score 3 |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | self.lose() found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels grid_size==(64,64); no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY notes per level

- **L1**: T-shape playfield clearly visible — 2-wide horizontal corridor (rows 3-4) at top + 1-wide vertical arm (column 3) descending. Yellow-cross avatar at NW intersection. Two orange-star collectibles: one at east end of horizontal arm, one at south end of vertical arm. Brick-textured walls fill the surround. PASS.
- **L2**: 2-wide horizontal corridor (rows 7-8) with a 2-cell vertical branch up at column 8 to a green-asterisk clearer pad. West-row-5 stub extending from the branch top. Yellow avatar at west end of corridor, orange collectibles at east end and at west end of row-5 stub. PASS.
- **L3**: T-junction visible — horizontal corridor (row 8) + vertical branch (column 8) going up. Yellow avatar at junction centre. Three orange-star collectibles at the three branch ends. Two blue-ringed warp pads visible at SW and SE corners (cells (1,9), (14,9)). PASS.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_arrow_moves_avatar | x0=12 x1=16 | ACTION4 advances player x by CELL_STRIDE=4 |
| check_self_wake_kills | state=GAME_OVER | east-then-west sequence (stepping on age-1 wake) fires lose |
| check_clearer_pad_wipes_wake | wake count=0 | stepping onto clearer pad clears all active wake |
| check_warp_pair_teleports | player cell=(14, 9) | stepping on warp A at (1, 9) teleports to warp B at (14, 9) |

Visit count: 1/6.
