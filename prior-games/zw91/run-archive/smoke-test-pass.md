# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == level.grid_size for all levels |
| CHECK_SPRITE_CONTENT | 7 | 9 | 10 | distinct non-letter-box palette values |
| CHECK_ACTION_BRANCHES | ✅ | — | — | declared=[1,2,3,4,5]; all 5 referenced in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on any of [1..5] |
| CHECK_PALETTE_RANGE | 1..13 | 1..15 | 1..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | self.next_level() found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | self.lose() found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all-levels-grid_size-equal=True; no per-level resize required |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 reaches L2 (score 0→1), L2 reaches L3 (score 1→2), L3 reaches WIN state |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual-sanity per-level notes
- **L1 PASS**: orange avatar (small) at top-left quadrant, yellow socket-large with diamond pattern at bottom-right, perimeter dark-brick walls, blue HUD bar on row 0. Matches spec § L1 Layout. ~2 distinct game elements visible as expected.
- **L2 PASS**: two chambers separated by vertical wall column at tile_x=8; orange avatar small at left, two purple shove-blocks plugging the wall-column gap, yellow socket-med (with cross etched at center indicating size 2) at right. HUD on row 0. ~5 distinct elements as expected.
- **L3 PASS**: three chambers separated by two wall columns; orange avatar small at left, three purple shove-blocks in the first column's gap, three cracked-pattern (pink/black) breakaway-walls in the second column's gap, yellow socket-large at right. HUD on row 0. ~9 distinct elements as expected.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_arrow_moves_avatar | (8,8)->(12,8) | ACTION4 advances avatar top-left x by exactly 4 cells |
| check_action5_grows_size | size 1->2 | ACTION5 in open space inflates size 1→2 |
| check_action_counter_increments | counter 0->1 | engine `_action_count` advances per action |
| check_lose_at_budget | state=GAME_OVER after budget+2 | step counter exhaustion fires self.lose() |

Visit count: 1/6.

**Verdict:** PASS. Transition to `finalize`.
