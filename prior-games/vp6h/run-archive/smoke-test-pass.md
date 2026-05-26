# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera == level.grid_size = (16, 16) per level |
| CHECK_SPRITE_CONTENT | 10 | 10 | 10 | distinct non-letter-box palettes per level (palettes {1, 2, 3, 4, 6, 10, 11, 12, 13, 15}) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions (1, 2, 3, 4, 6) referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on each declared action |
| CHECK_PALETTE_RANGE | 1..15 | 1..15 | 1..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | levels share grid_size; resize present |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY — per-level diagnosis

- **L1**: PASS — yellow lantern bar at top centre (cols 5..9), grey pillar at col 7 mid-grid, cyan+purple crystal visible just below the pillar in the lit corridor; magenta+maroon avatar at bottom-left (~col 2 row 13); orange step-counter bar at bottom; no glyphs resembling letters/digits.
- **L2**: PASS — yellow lantern at top centre, single grey pillar visible at col 14, three crystals scattered along the lower row at cols 2 / 6 / 14, avatar at lower-left; orange HUD at bottom; sprites laid out as specified.
- **L3**: PASS — two yellow lantern bars (top and bottom edges); three grey pillars at cols 2, 10, 13 (top-pillar / top-pillar / bot-pillar visually distinct rows); three crystals at cols 2 (lower), 7 (mid), 13 (upper); avatar at lower-left; both rail markers present; HUD bar at bottom.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_arrow_moves_avatar` | x0=2 x1=3 | ACTION4 moves avatar one cell right on L1 |
| `check_click_top_rail_slides_lantern` | top_lantern_x after click = 0 | clicking grid (2, 0) on L2 slides top-lantern leftmost edge to col 0 |
| `check_pickup_in_shadow_collects_crystal` | level_idx after pickup = 1 | 5 ACTION4 + 1 ACTION1 picks up the L1 crystal and the engine advances to L2 |
| `check_pickup_in_light_is_no_op` | crystal at col 6 still TANGIBLE | walking onto B at L2 default lantern (col 6 is top-lit) does NOT remove the crystal; pickup is gated by shadow |

Visit count: 1/6.
