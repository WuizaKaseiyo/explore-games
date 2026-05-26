# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == level.grid_size for every level |
| CHECK_SPRITE_CONTENT | 8 | 8 | 8 | distinct non-letter-box palette values per level (≥ 2 required) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions {1, 2, 5, 6} have GameAction.ACTIONn references in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | each action ran without exception (smoke-runner test) |
| CHECK_PALETTE_RANGE | 0..15 | 0..15 | 0..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 witness (15 actions) → L2; L2 witness (15) → L3; L3 witness (15) → WIN. Final `_score=3`, `_state=WIN` |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels uniform 64×64 — no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY notes per level

- **L1 (3 columns):** rendered frame shows 3 tall vertical colour-band columns, 3 framed target swatches at top (green, yellow, purple), a white horizontal scan line crossing the columns, yellow square markers at frame edges, and a thin step-counter HUD at row 0. Matches spec § L1 exactly.
- **L2 (4 columns + 1 bound pair):** 4 columns, 4 target swatches (yellow / purple / green / red), an orange ribbon-and-dot pair connecting the tops of the leftmost two columns (the bound pair), white scan line, edge markers, HUD. Matches spec § L2.
- **L3 (5 columns + 2 bound pairs):** 5 columns, 5 target swatches (red / orange / yellow / green / purple), TWO orange ribbon-and-dot pairs (the two bound pairs), white scan line at the L3 starting row, edge markers, HUD. Matches spec § L3.

No catastrophic rendering bugs — sprites fill the playfield as expected, no collapsed corners, no symbol-resembling shapes, no palette leaks.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_action1_shifts_active_column` | before=0 after=1 | ACTION1 increments active column's `position` by 1 mod 12. Tests M1. |
| `check_click_sets_active_column` | active=col_l1_b | ACTION6 inside col_l1_b's bounding box selects it as active. Tests click-to-select gating. |
| `check_bound_pair_partners_move_opposite` | da=1 db=11 | In L2, ACTION1 on bound col_l2_a drives col_l2_b by -1 (= +11 mod 12). Tests M2 coupling. |
| `check_action5_advances_scan_line_in_l3` | before=0 after=1 | ACTION5 in L3 advances `scan_line_idx` 0→1. Tests M3. |

Visit count: 1/6.
