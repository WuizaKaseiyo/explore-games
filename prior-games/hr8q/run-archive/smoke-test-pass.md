# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera 64×64 == grid_size 64×64 |
| CHECK_SPRITE_CONTENT | 6 | 8 | 10 | distinct non-letter-box palettes |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | ACTION5 + ACTION6 both branched |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions |
| CHECK_PALETTE_RANGE | 0..15 | 0..15 | 0..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | uniform 64×64 grid; resize present anyway |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per level
- **L1** — Target purple chip top-left, 2 empty input slots + 1 result slot below, vertical divider, magenta + light-blue ingredient blocks on right, single mix-rule strip at bottom showing `[magenta][light-blue][purple]`. Step bar visible at top. Matches spec § Levels — Level 1.
- **L2** — Target maroon chip, same 2 slots + result, 3 ingredients (magenta, light-blue, pink), 2 mix-rule strips visible at bottom. Matches spec § Levels — Level 2.
- **L3** — Target blue chip, **3** input slots visible (the third slot is the L3 new mechanic), 4 ingredients (magenta, light-blue, pink, yellow), 3 mix-rule strips visible (1 pair + 2 triple). Matches spec § Levels — Level 3.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_click_fills_slot | slot[0]=6 expected=6 | ACTION6 on a primary fills slot1 with that block's colour |
| check_l1_minimal_solve | level after solve=1 | the 3-action L1 witness advances past L1 |
| check_mismatched_commit_distils | ingredients before=3 after=4 | mismatched commit at L2 distils a new intermediate |
| check_lose_at_budget | state after budget+1=GAME_OVER | exhausting the budget without solving fires self.lose() |

Visit count: 1/3.
