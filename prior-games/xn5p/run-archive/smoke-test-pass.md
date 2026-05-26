# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera == level.grid_size (20, 20) all levels |
| CHECK_SPRITE_CONTENT | 7 | 7 | 8 | distinct non-letter-box palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on any of ACTION1..5 |
| CHECK_PALETTE_RANGE | 0..11 | 0..11 | 0..14 | all in [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | levels share grid_size=(20, 20); per-level resize still wired |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY notes

- **L1**: red ring on left, yellow avatar in middle, blue plus on right. Vertical wall column with single channel where avatar sits. HUD bar visible at bottom row.
- **L2**: red main top-left, avatar yellow top-right, red obstacle in middle channel, blue bottom-right. Two narrow channels visible.
- **L3**: red main top-left, avatar yellow top-right, red obstacle middle, green X-shape in vertical alcove, blue bottom-right. Alcove's wall ceiling visible.
- No catastrophic rendering bugs (no corner-patch, no glyph-resembling sprites).
- All sprites use 3×3 internal pixel structure (no 1×1 flat-cell rendering).

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_walk_moves_avatar | x0=10 → x1=7 | ACTION3 (west) moves avatar 3 cells west on L1 |
| check_stamp_creates_wall | after_stamp count=1 at_pos=1 | ACTION5 at empty cell creates wall_stamp at avatar's position |
| check_push_moves_molecule | obstacle red (10, 7) → (7, 7) | walking into a molecule cell pushes it one stride |
| check_toggle_removes_stamp | after_stamp=1, after_toggle=0 | L3 stamp-toggle: re-pressing ACTION5 removes the stamp |

Visit count: 1/6.
