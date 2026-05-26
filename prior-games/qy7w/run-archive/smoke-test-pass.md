# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == grid_size (64, 64) on every level |
| CHECK_SPRITE_CONTENT | {3,5,7,8,9,11} | {3,5,7,8,9,11} | {3,5,7,8,9,11,14} | distinct non-letter-box palette values per frame |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | declared `[6]`; `GameAction.ACTION6` referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | ACTION6 dispatches without exception |
| CHECK_PALETTE_RANGE | (3, 11) | (3, 11) | (3, 14) | min/max within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | all 3 witnesses replayed: L1→L2→L3→WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all 3 levels use the same grid_size — no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered frames at `workspace/smoke-frames/level_*.png` show 3 strands + caps + slots + crossings + HUD per spec |

### CHECK_VISUAL_SANITY notes per level
- **L1**: 3 strand bars (red/blue/yellow) descending from coloured caps to hollow framed slots (yellow/red/blue). 3 grey binary-crossing rectangles each with a "+" PASS marker. Pink HUD bar at bottom row. Matches spec § L1.
- **L2**: Same 3 strands. 3 binary crossings + 1 wider long crossing (35-px) with two "+" markers. Yellow blocker visible at (col 1, y=36) as a small framed yellow square. Matches spec § L2.
- **L3**: Same 3 strands. 4 binary crossings + 1 long crossing. Green dye-station sprite (concentric green/black rings, abstract, not face-like) at (col 0, y=38); strand 0's colour visibly shifts to green below it. Yellow blocker at (col 1, y=42). Bottom slot 0 is green-framed (instead of red as in L1/L2). Matches spec § L3.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_binary_toggle_reroutes_strands | before=[(0,8),(1,9),(2,11)] after=[(0,8),(2,9),(1,11)] | L1 C2 click swapped strands 1 and 2's columns |
| check_long_toggle_swaps_outer_columns | before=[(0,8),(1,9),(2,11)] after=[(2,8),(1,9),(0,11)] | L2 long-crossing click swapped strands 0 and 2; col 1 unchanged |
| check_shift_changes_bottom_colour | strand 0 bottom colour=14 | L3 initial routing: strand 0 (R) routes through shift_green at (col=0, y=38) and arrives at bottom with palette 14 (green) |
| check_step_budget_lose | state after budget+1 actions=GAME_OVER | exhausting L1's 30-step budget on a non-winning toggle pattern triggers `lose()` → engine state GAME_OVER |

Visit count: 1/6.
