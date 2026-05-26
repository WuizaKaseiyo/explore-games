# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == grid_size every level |
| CHECK_SPRITE_CONTENT | 5 | 5 | 5 | distinct non-letter-box palettes per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 6 declared actions {1..6} branched in `step()` |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions for any action |
| CHECK_PALETTE_RANGE | 0..15 | 0..15 | 0..15 | rendered pixels within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (64, 64); per-level resize not needed |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered initial frames match spec; PNGs at workspace/smoke-frames/level_*.png |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | each level's named witness advances past that level (final state = WIN, score = 3) |

### CHECK_VISUAL_SANITY notes per level

- **L1**: target_pad ring visible at top-left (cells centered at (4, 8)). Chain extends horizontally from base (16, 32) to tip (52, 32) with three hinges (active hinge 0 highlighted by yellow halo at the base). HUD bar at row 63 fully filled. ✓
- **L2**: identical to L1 except target_pad shifted right (centered at (8, 8)). ✓
- **L3**: chain identical. Object_red (small red 2×2 dot) at top-left near (8, 8). Drop_zone_red (purple ring with red interior) centered at (32, 20). HUD at row 63. ✓

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_action5_cycles_active_hinge | before=0 after=1 | ACTION5 cycles `_active_hinge` by +1 mod 3 |
| check_action3_rotates_active_ccw | theta 0 -> 90 | ACTION3 rotates the active segment's heading +90° |
| check_action2_retracts_active_length | length 12 -> 11 | At L2, ACTION2 reduces active segment's length by 1 |
| check_click_on_hinge_sets_active | active_hinge=2 | ACTION6 click at hinge_2's cell sets active_hinge to 2 |

Visit count: 1/6.

All universal checks and all custom checks pass. Transition to `finalize`.
