# Smoke test PASS — gv47

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (12,12) == level.grid_size |
| CHECK_SPRITE_CONTENT | 5 | 5 | 9 | distinct non-letterbox palette values |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | both ACTION5 + ACTION6 branched in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on either action |
| CHECK_PALETTE_RANGE | 0..14 | 0..14 | 0..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` present |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` present |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (12,12); resize-on-set still in source |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY notes per level

- **L1.** Yellow seed top-left; yellow target bottom-right; vertical
  wall column with the spec's expected gap at row 5; green step-bar
  HUD at the top edge. PASS.
- **L2.** Yellow seed top-left, blue seed bottom-left, yellow target
  top-right, green mix-target middle. HUD bar present. PASS.
- **L3.** Three seeds (yellow top-left, red top-middle, blue bottom-
  left), red and purple targets visible side-by-side (pip cells
  distinct at (9, 5) and (11, 5)), green target bottom, 2×2 wall
  block lower-middle, light-blue wind-strip on east edge, HUD bar
  at top. The red and purple target frames render visually adjacent
  with no separator cell — cosmetic, not a failure (pip cells are
  still individually addressable for the win predicate). PASS.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_click_seed_grows_region | before=9 after=21 | a single grow click adds the 4-cardinal ring of the 3×3 seed |
| check_action5_mixes_when_in_contact | regions_after_mix=1 | yellow + blue regions in contact fuse into 1 region under the L2 mixing table |
| check_wind_extends_growth | before=9 after=26 | with east wind, one grow click adds 17 cells (>12 = unbiased ring count); wind bias active |
| check_lose_when_budget_exhausted | state=GAME_OVER, steps_remaining=0 | clicks at empty pixel still consume the step budget; lose fires when budget hits 0 |

Visit count: 1/3.
