# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (21, 21) == level.grid_size (21, 21) |
| CHECK_SPRITE_CONTENT | 3 | 4 | 5 | distinct non-letterbox palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions referenced as `GameAction.ACTION{1..4}` in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | each declared action runs without exception |
| CHECK_PALETTE_RANGE | 1..11 | 1..12 | 1..12 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | per-level camera resize present (defensive — all 3 levels share grid_size, so mismatch impossible by construction) |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at `workspace/smoke-frames/level_*.png` |

### Visual-sanity diagnoses (per level)

**L1**: 4 yellow shapes in the corners of the interior — top-left and top-right are filled blocks (off-white centre pip), bottom-left and bottom-right are outline-only targets (transparent centre showing dark backdrop). Grey wall_solid border ring fully visible. Yellow HUD bar across frame row 0. Matches spec § 4.L1.

**L2**: Yellow block at lattice (3, 1), orange block at lattice (5, 1) at the top. Row-3 divider with yellow-rim-wall (yellow outline + grey core) at lattice (3, 3) and orange-rim-wall at (5, 3); other row-3 cells are grey full-blocking walls. Bottom row has yellow target at lattice (1, 5), grey stop-wall at (4, 5), orange target at (5, 5). HUD bar present. Matches spec § 4.L2.

**L3**: Yellow block + orange block at top row. Row-3 divider with yellow-rim at lattice (1, 3) and orange-rim at (5, 3); other row-3 cells grey full-blocking. Bottom row has the sticky-pad-on-yellow-target combo at lattice (3, 5) (rendered as yellow outline corners + magenta plus-pattern centre — exactly the layered visual the spec describes) plus orange target at (5, 5). HUD bar present. Matches spec § 4.L3.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_down_advances_l1` | current_level_index: before=0 after=1 | M1 slide-to-end ferries every yellow block to bottom-row targets in one DOWN press; `next_level()` triggers. |
| `check_no_op_action_consumes_step` | `_steps_used: before=0 after=1` | wasted presses (UP at top border) still cost a step — energy bar can in principle drain. |
| `check_rim_blocks_wrong_colour` | after DOWN: `[('block_orange', 15, 15), ('block_yellow', 9, 15)]` | M2: yellow crosses yellow-rim at (3, 3) lattice; orange crosses orange-rim at (5, 3) lattice; both end at row 5 base 15. Without M2 the rim cells would be impassable and blocks would stop at row 2 base 6. |
| `check_sticky_catches_first_crosser` | `_fixed_block_cells = [(9, 15)]` | M3: after the L3 partial-witness `[LEFT, DOWN, RIGHT]`, yellow has slid across the sticky-pad at lattice (3, 5) base (9, 15) and is recorded as fixed there. |

Visit count: 1/3.
