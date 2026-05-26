# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == level.grid_size (64,64) all 3 levels |
| CHECK_SPRITE_CONTENT | 5 | 5 | 5 | distinct non-letter-box palette values: {2, 4, 8, 11, 14} per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | ACTION6 declared and referenced in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | ACTION6 runs without exception |
| CHECK_PALETTE_RANGE | 2..14 | 2..14 | 2..14 | within [0, 15] all 3 levels |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | self.next_level() found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | self.lose() found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | levels share grid_size (64,64); resize present in on_set_level |
| CHECK_WITNESS_WINS | PASS | PASS | PASS | L1 (6 actions) advances to L2; L2 (10 actions) advances to L3; L3 (15 actions) → GameState.WIN |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per-level notes
- **L1 PASS**: 8 row markers stacked at left edge; ZERO column markers (correct — L1 omits them); 3 lock-target rings (red, yellow, green) at distinct playfield positions; green HUD bar at bottom row. Plain grey background.
- **L2 PASS**: 8 row markers (left) + 8 column markers (top); 5 lock-target rings spread across the playfield; HUD bar visible.
- **L3 PASS**: 8 row markers + 8 column markers; 7 lock-target rings — including the diagonal cluster from rows 5-7 — visible at distinct positions; HUD bar visible.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_row_marker_click_recolors_row | row_tints[3]: before=2 after=8 expected=8 | one click cycles BG→red on the targeted row |
| check_l2_column_overrides_row | after col_5=yellow override at cell(5,3): expected 11 got 11 | L2 column override rule: column tint wins over row tint |
| check_l3_brighter_wins_row_dominates | row_3=14 brighter than col_2=8: cell(2,3) expected 14 got 14 | L3 brighter-wins rule: row tint wins when palette index higher |
| check_l1_minimal_solve | after L1 witness: level_index=1 | the spec's 6-action L1 witness advances past L1 |

Visit count: 1/6.
