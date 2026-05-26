# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == grid (64, 64) at every level |
| CHECK_SPRITE_CONTENT | 6 | 7 | 7 | distinct non-letter-box palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | A1, A2, A3, A4, A5, A6 — all referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | every action runs without exception |
| CHECK_PALETTE_RANGE | 0..15 | 0..14 | 0..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1, L2, L3 named witnesses each advance / reach WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all 3 levels use grid_size (64, 64); no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual-sanity inspection (per-level notes)

- **L1**: Single red cross stamp (with white centre accent) above
  a white horizontal crease bisecting the field; matching pink
  shadow cross below the crease. Green HUD bar at top. Purple
  selection halo around the auto-selected red stamp.
- **L2**: Red cross stamp upper-left + blue ring stamp upper-
  middle, both on the active half above a horizontal white
  crease. Pink shadow cross + light-blue shadow ring below the
  crease. Green HUD bar at top. No halo (no auto-select).
- **L3**: Red cross + blue ring stamps in the upper half; pink
  shadow cross also in the upper half (right of red); light-
  blue shadow ring in the lower half (below crease). The
  asymmetric layout is intentional — the player must re-orient
  the crease from horizontal to vertical to fold red onto its
  shadow (since red and pink share y but differ in x). Green
  HUD bar at top.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_arrow_moves_selected_stamp | x0=8 x1=12 | ACTION4 moves the auto-selected L1 stamp right by 4 |
| check_click_selects_stamp_at_l2 | selected = stamp_blue_ring | clicking on a stamp at L2 selects it |
| check_fold_consumes_stamp | interaction = REMOVED | ACTION5 removes the folded stamp |
| check_collision_blocks_stamp_into_other | pre_y=16 post_y=16 | red cannot move DOWN into blue's body at L2 |

Visit count: 1/6.
