# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (32, 32) == grid_size (32, 32) all 3 levels |
| CHECK_SPRITE_CONTENT | 8 | 9 | 10 | distinct non-letterbox palette values; well over 2 |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | All 6 declared actions reference `GameAction.ACTION{n}` in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | Each action runs without exception |
| CHECK_PALETTE_RANGE | 0..13 | 0..13 | 0..14 | All within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1's witness advances to L2; L2's to L3; L3's to WIN. score progression 0→1→2→3 |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | All levels share grid_size (32, 32); per-level resize present in `on_set_level` |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec descriptions; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per level

- **L1**: 1 short orange/maroon plank (with black anchor fixture + yellow pip at left end) holding the red-ring pawn; magenta-ringed goal tile below. HUD yellow bar at bottom-row centre. ~5 distinct shapes visible — matches spec ("1 plank + 1 pawn + 1 goal + HUD"). PASS.
- **L2**: 2 long horizontal planks separated vertically; black solid post between them; pawn on the top plank; magenta goal at right end of bottom plank. HUD bar at bottom. ~6 distinct shapes — matches spec. PASS.
- **L3**: 2 horizontal planks (top long, bottom short); black post between them; green spring sprite on the bottom plank's right end; magenta goal to the right of the spring. HUD bar at bottom. ~7 distinct shapes — matches spec. PASS.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_click_selects_plank` | active_plank=<_PlankState …> | Click on plank cell at (13, 10) sets `_active_plank` to that plank. |
| `check_pivot_increments_orientation` | o0=0 o1=1 | ACTION5 with active plank advances orientation (0=east → 1=south). |
| `check_walk_moves_pawn_after_pivot` | y0=13 y1=14 | ACTION2 advances pawn's y by 1 when destination is on a plank cell. |
| `check_lose_at_budget` | state=GAME_OVER actions=30 | Spamming 31 walk-actions on L1 (without winning) drives the step counter to 0 and triggers `lose()`. |

Visit count: 1/6.
