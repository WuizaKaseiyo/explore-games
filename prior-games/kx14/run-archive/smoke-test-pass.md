# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (60, 60) == grid_size (60, 60) for every level |
| CHECK_SPRITE_CONTENT | 4 | 5 | 6 | distinct non-letterbox palettes (L1: {1, 4, 10, 12}; L2: {1, 4, 5, 10, 12}; L3: {1, 4, 5, 10, 12, 14}) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions (1, 2, 3, 4, 6) referenced in `step()` |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | each of the 5 actions runs without exception on a fresh L1 instance |
| CHECK_PALETTE_RANGE | 1..12 | 1..12 | 1..14 | all within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | per-level camera resize present (`self.camera.width`/`height` set in `on_set_level`); all 3 levels share `grid_size=(60, 60)` so resize is necessary on first level only |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at `workspace/smoke-frames/level_*.png` |

### Visual sanity per level (notes)

- **L1 PASS** — Light grey air upper region; light blue water lower region (filling rows 8–11). One orange ball at left side at water surface (~col 3, row 8). One orange hollow target ring upper-right (~col 8, row 4). Step bar visible on top edge. No catastrophic rendering issues. Matches spec § Levels — Level 1.
- **L2 PASS** — Same layout style. Water fills bottom ~25% (rows 9–11). One orange ball at lower-left (~col 1, row 9). One orange target ring upper-right (~col 10, row 3). One platform (3-cell-wide grey bar with black edges) at left side mid-frame (~row 6, cols 0–2). Step bar visible. Matches spec § Levels — Level 2.
- **L3 PASS** — Water fills bottom ~25%. Two balls — orange at left (~col 3, row 9) and green at right (~col 8, row 9), both at water surface. Two target rings — green at left mid-height (~col 3, row 5), orange at right mid-height (~col 8, row 5). One platform in middle (~row 6, cols 4–6). Step bar visible. Matches spec § Levels — Level 3.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_raise_water_lifts_ball | row before=8 after=7 | L1: ACTION1 raises water by 1 row and lifts the floating ball with it (mechanic M1). |
| check_tilt_right_moves_ball_one_cell | col before=3 after=4 | L1: ACTION4 nudges floating ball one cell right when path is clear (mechanic M2). |
| check_anchor_pins_ball_against_water | row before-raise=9 after-raise=9 (anchored=True) | L3: clicking a ball anchors it; subsequent ACTION1 (water raise) leaves the anchored ball at its original row (mechanic M4). |

Visit count: 1/3.
