# Smoke test PASS

Visit count: 1/6.

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (32, 32) matches level.grid_size for every level |
| CHECK_SPRITE_CONTENT | 6 | 8 | 8 | distinct non-letter-box palette values (≥ 2 required) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions (1, 2, 3, 4) referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on any action |
| CHECK_PALETTE_RANGE | 1..10 | 1..13 | 1..13 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 8E+8S advances to L2; L2 4E+2N+4E+2S+4E advances to L3; L3 2N+4E+4E+2N+2E reaches WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | All levels share grid_size (32, 32); per-level resize present anyway in `on_set_level` |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at `workspace/smoke-frames/level_*.png` |

### Visual sanity per-level commentary

- **L1**: Dark beveled brick at upper-left, blue goal at lower-right, white step-counter bar across the top centre. No holes (correct for L1), no lives pips (correct — L1 has `lives=0`). ✅
- **L2**: Dark brick on the left edge, blue goal on the right edge, step-counter bar at top. Red-cross-hatched hole pattern in the middle forming the three-row hazard layout (y=3 row of 3 holes, single hole at (8, 4), y=5 row of 5 holes). Three orange-red life pips visible in the top-right corner. ✅
- **L3**: Dark brick on the left at mid-height, blue goal at top-right (at y=1), step-counter bar at top. Vertical red-cross-hatched hole band in the middle (cx ∈ [6..9]) with a visible single-row gap at y=3 — the bridge. Three life pips at top-right. ✅

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_east_tumble_changes_state` | before=standing after=lying_h | ACTION4 from standing produces lying_h state (M1 mechanic) |
| `check_two_east_tumbles_shift_anchor_by_2` | start=(3,3) after_two_E=(5,3) state=standing | Two consecutive E tumbles shift the standing anchor by exactly +2 cells (Bloxorz physics) |
| `check_hole_kill_decrements_lives_and_respawns` | lives0=3 lives1=2 cell=(2, 4) start=(2, 4) | Driving onto the (8, 4) hole at L2 decrements lives 3→2 AND respawns the brick at the level-start cell |
| `check_l1_witness_advances` | level_after_witness=1 brick=standing@(2, 4) | L1's 16-action witness advances the engine past L1 (next_level fired; brick respawned at L2 start) |
