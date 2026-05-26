# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera 64×64 == grid_size 64×64 |
| CHECK_SPRITE_CONTENT | 4 | 5 | 6 | distinct non-letter-box palettes |
| CHECK_ACTION_BRANCHES | ✅ | — | — | ACTION6 referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | — | — | ACTION6 runs without exception (action_count 0→1) |
| CHECK_PALETTE_RANGE | 2..14 | 2..14 | 2..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | self.next_level() and self.win() both found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | self.lose() found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size=(64,64); per-level camera resize present in `on_set_level` (defensively no-op) |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered initial frames match spec; PNGs at workspace/smoke-frames/level_*.png |

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_drop_increments_source | before=0 after=1 | clicking on L1 source advances grain count by 1 |
| check_l1_minimal_solve | level after solve=1 | 4 clicks on L1 source advance to L2 |
| check_sink_absorbs | sink_count_total=0 | L2 source A topple deposits to north/south sinks; sinks remain at 0 |
| check_redirector_forwards | target_(3,1)_count=1 | L3 source A topple → redirector(2,1) → target(3,1) ends at exactly 1 |

## Visual sanity per level

- **L1**: 4×4 cell grid, source at (1,1) with magenta center + top notch, 4 targets at cardinals with maroon centers + green corner pips, 11 regulars blank, HUD bar visible at row 63.
- **L2**: 5×5 cell grid, 2 sources at (1,2) and (3,2) (magenta + top notch), 3 sinks in middle column (blue + left notch), 4 targets at the diagonal corners around the sources (maroon + green corner pip), 16 regulars blank, HUD visible.
- **L3**: 5×5 cell grid, 2 sources at (1,1) and (1,3), 6 sinks (top corners, sides, shared center cell (1,2), and (2,2)), 2 redirectors at (2,1) and (2,3) with orange centers + bottom-edge notch, 2 targets at (3,1) and (3,3), HUD visible.

Visit count: 1/6.
