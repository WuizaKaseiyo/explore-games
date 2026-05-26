# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera resized to (12,12), (14,14), (14,14) per level |
| CHECK_SPRITE_CONTENT | 3 | 4 | 5 | distinct non-letter-box palette values per level (background 5 + sprites + cone overlay) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions (1-5) referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | every action runs without exception; counter increments to 1 |
| CHECK_PALETTE_RANGE | 1..11 | 1..12 | 1..12 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` present |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` present |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | levels have different grid_size; source mutates `self.camera.width` / `height` in `on_set_level` |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered frames at workspace/smoke-frames/level_*.png match the spec's per-level layout — see notes below |

### Visual sanity per-level diagnoses

- **L1 — PASS**: rendered frame shows 1 yellow lantern (top, ~y=3) with an off-white cone extending UP (cone facing N, R=4 = 3×4 cells), and 2 yellow ring targets: one at bottom-left (~grid (3, 8)) and one at centre-right (~grid (8, 6)). HUD step bar visible at bottom row. Matches spec § L1 layout.
- **L2 — PASS**: lantern roughly centre-top with R=2 cone facing N (small off-white area), an orange wax pickup directly adjacent to lantern (matches `(3, 6)` placement), and 2 yellow ring targets — one near top of frame (matches `centre (3, 1)`) and one near bottom (matches `centre (3, 12)`). HUD bottom. Matches spec § L2 layout.
- **L3 — PASS**: lantern at upper-left with R=2 cone facing E (off-white area extending right from lantern), wax pickup directly E of lantern (matches `(3, 2)`), red filter cell visible mid-left of frame (matches `(2, 8)`), yellow ring target upper-right (matches `centre (8, 2)`), red ring target lower-left (matches `centre (2, 11)`). 5 distinct game-element clusters — sprite count and quadrant placement match spec. HUD bottom. Matches spec § L3 layout.
- No sprite reads as a digit or letter at the rendered scale (lantern = small yellow square; targets = hollow square rings; pickup/filter = single cells). No catastrophic rendering bug.

## Custom checks

| Check | Result | Observed | Notes |
|---|---|---|---|
| `check_walk_moves_lantern` | PASS | `x0=3 x1=4` | ACTION4 (RIGHT) advances lantern's x by 1 |
| `check_action5_rotates_facing` | PASS | `f0=0 f1=1` | ACTION5 advances cone facing by exactly +1 mod 4 |
| `check_wax_pickup_extends_range` | PASS | `r0=2 r1=4` | walking onto L2's wax pickup at (3, 6) increments cone_range from 2 to 4 (one-shot pickup) |
| `check_l1_minimal_solve` | PASS | `level after solve=1` | the spec's 5-action L1 witness `[5, 4, 2, 2, 5]` advances `_current_level_index` from 0 to 1 |

Visit count: 1/3.
