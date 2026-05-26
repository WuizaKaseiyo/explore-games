# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera == level.grid_size = (64, 64) |
| CHECK_SPRITE_CONTENT | 6 | 6 | 7 | distinct non-letterbox palettes per level |
| CHECK_ACTION_BRANCHES | ✅ | — | — | declared `[6]` referenced as `GameAction.ACTION6` in source |
| CHECK_ACTION_RUNTIME | ✅ | — | — | ACTION6 ran without exception, `_action_count` advanced |
| CHECK_PALETTE_RANGE | 1..14 | 1..14 | 1..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 witness (2 clicks) → L2; L2 witness (5 clicks) → L3; L3 witness (8 clicks) → WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | per-level camera resize present (informational; all levels use 64×64) |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered initial frames match spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY notes (per level)
- **L1** PASS — 2 tiles in a row, edge bands clearly visible (red top, blue right, green bottom, yellow left for both tiles); shared inner column shows mismatched yellow vs blue (matches spec L1 initial state); HUD bar at row 63 visible.
- **L2** PASS — 2×2 grid, top-left tile shows the 6×6 black-square inner glyph (the locked tile); other 3 tiles show off-white inner area (regular). All 4 tile bounding boxes visible, edges colored. HUD bar visible.
- **L3** PASS — 3×3 grid, centre tile shows 6×6 black-square inner glyph (the lock); top-left and bottom-right tiles show 6×6 purple-ring inner glyphs (linked-pair members, identical visuals signalling correlation per checklist item 21.2); other 6 tiles show off-white interior (regular). HUD bar visible.

## Custom checks

| Check | Verdict | Observed |
|---|---|---|
| `check_click_rotates_regular_tile` | PASS | r0=0 r1=1 (tile l1_b at L1) |
| `check_click_on_locked_is_noop` | PASS | locked rotation 0→0, _steps_used 0→0 (tile l2_00 at L2) |
| `check_click_on_linked_rotates_both` | PASS | (0→1, 0→1) for both pair members at L3 |
| `check_lose_at_budget` | PASS | final state=GAME_OVER after budget+1 clicks on a single tile (L3, budget=50) |

Visit count: 1/6.
