# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera viewport == level.grid_size (64×64 every level) |
| CHECK_SPRITE_CONTENT | ✅ | ✅ | ✅ | each level shows ≥ 2 distinct non-letter-box palette values |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions branched in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on first action of each type |
| CHECK_PALETTE_RANGE | ✅ | ✅ | ✅ | rendered pixels in [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (64, 64); resize present anyway |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 advanced after 13 actions; L2 after 33; L3 reached WIN after 70 |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY notes
- L1: open arena, avatar (yellow rim + blue body + eye-dot facing
  right) at left-of-centre, pink starburst target east. Matches
  spec § 4 Level 1.
- L2: bounded corridor with dark wall_tall perimeter and a striped
  vertical wall_short barrier mid-corridor; avatar west of barrier,
  target east. Matches spec § 4 Level 2.
- L3: same corridor topology; avatar west, dark-red guard sprite
  east of avatar, wall_short barrier, pink target east of barrier.
  Matches spec § 4 Level 3.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_action5_launches_boomerang | before=held after=outbound | ACTION5 fires throw |
| check_action1_moves_avatar_up | y0=32 y1=31 | UP arrow walks 1 cell up |
| check_boomerang_advances_one_cell | moved 1 cell (22,33)→(23,33) | post-throw arrow advances boomerang exactly 1 cell |
| check_lose_at_budget | state=GAME_OVER after budget+2 | step exhaustion → lose |

Visit count: 1/6.
