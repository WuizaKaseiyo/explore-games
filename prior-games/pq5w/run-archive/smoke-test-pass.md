# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 60) == grid_size each level |
| CHECK_SPRITE_CONTENT | 7 | 7 | 8 | distinct non-letter-box palettes (L3 adds palette-8 red from forbidden) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions branched (1, 2, 3, 4, 6) |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions |
| CHECK_PALETTE_RANGE | 0..14 | 0..14 | 0..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | next_level() found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | lose() found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | same grid_size across levels — vacuous OK; source still mutates camera.width/height in on_set_level |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 advanced (score 1); L2 advanced (score 2); L3 reached WIN |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY per-level notes

- **L1**: yellow avatar at logical (1,7) on the left; dark anchor
  portal at (3,7) right of avatar; full-height grey/black wall
  column at x=8; pink float portal at (12,7) and green goal frame
  at (14,7) on the right; green HUD bar at bottom. Scene matches
  spec. PASS.
- **L2**: yellow avatar at logical (1,9) outside (lower-left);
  closed grey/black walled rectangle in the upper-mid; dark anchor
  portal at (6,4) inside; pink float portal at (10,3) inside upper-
  right corner; green goal frame at (10,4) inside; green HUD bar
  at bottom. Scene matches spec. PASS.
- **L3**: same as L2 + forbidden column (red-cornered tiles) at
  x=8 inside the room, separating the anchor (sub-area-1, left)
  from the float portal + goal (sub-area-2, right). Scene matches
  spec. PASS.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_right_walks_avatar | x0=4 x1=8 | ACTION4 advances avatar +STRIDE in x |
| check_walk_onto_anchor_sets_pending | pending=(48, 28) | walking onto anchor at L1 sets _teleport_pending to float's cell |
| check_click_relocates_float_portal | before=(40,12) after=(8,36) | ACTION6 click at pixel (10,38) relocates float to grid cell origin (8,36) |
| check_step_used_increments | before=0 after=1 | each handled action increments _steps_used by 1 |

Visit count: 1/6.
