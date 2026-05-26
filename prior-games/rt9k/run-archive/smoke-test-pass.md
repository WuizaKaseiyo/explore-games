# Smoke test PASS — `rt9k`

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 60) == level.grid_size for every level |
| CHECK_SPRITE_CONTENT | 4 | 4 | 5 | distinct non-letter-box palette values |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions have `GameAction.ACTION<n>` references in `step()` |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | actions 1..4 each ran without exception |
| CHECK_PALETTE_RANGE | 1..14 | 1..14 | 1..14 | within [0, 15] for every rendered frame |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all 3 levels share `grid_size=(64,60)` so per-level resize is not strictly required; `on_set_level` resets viewport anyway |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 witness `[3]*9` advanced score 0→1; L2 witness `[3]*4 + [2]*12` advanced 1→2; L3 witness `[3]*4 + [1]*15` reached WIN |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered initial frames at `workspace/smoke-frames/level_{1,2,3}.png` match spec § 4 — sprite count, placement, HUD presence, no rendering bugs |

### Visual sanity per level (operational test)

- **L1.** Magenta avatar at left, single tall black-grey vertical wall mid-screen, grey-ringed goal at right, green step bar across the bottom. 1 + 1 + 1 sprite-clusters as spec describes; HUD visible; no overlaps. PASS.
- **L2.** Magenta avatar at top-left, two vertical wall columns (black-grey solid + green filter), grey-ringed goal at bottom-right, green step bar. Two columns dividing playfield into three vertical strips; goal placed in the rightmost open region; HUD visible. PASS.
- **L3.** Magenta avatar at mid-left, two vertical wall columns (solid + green filter), short yellow filter strip across the right half's bottom row (5 cells, cols 9..13), yellow-ringed goal in the corridor between the solid wall and green filter at mid-height, green step bar. Sprite count and placement match spec; goal-tone cue (yellow ring) visible; no overlap between green filter column and yellow filter strip; HUD visible. PASS.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_left_moves_avatar | x: 4→0, y: 4→4 | LEFT moves avatar one cell left when destination is open. |
| check_left_wrap_changes_tone | avatar=(60,4); tone 0→2 (expected 2) | LEFT-wrap from col 0 lands at col 15 AND advances tone by −1 mod 3 (magenta=0 → green=2). |
| check_wall_blocks_movement | avatar=(28,28); pre-attempt was (28,28) | A solid wall at the destination cell blocks movement (no position change). |
| check_step_budget_decrements | before=30, after=29 | Each action consumes exactly one step from the budget. |

## Implementation refinement during smoke

While running the visual-sanity check, I noticed that the original L3
layout placed `filter_yellow` at cells (col c, row 14) for c in 9..14,
which overlapped `filter_green` at cell (col 14, row 14) — two
"filter"-tagged sprites at the same coordinate, with `_filter_at`
resolving the cell to the green filter (insertion order) but the
camera rendering it as yellow (later draw call wins). Functionally
the witness was unaffected (it traverses (col 13, row 14), not col
14), but the visual would mislead a player. Fixed in
`_level_3_sprites()` by reducing the yellow strip to cols 9..13 (5
cells) so the corner cell (col 14, row 14) is unambiguously green
filter both visually and behaviourally. Re-ran all universal +
custom checks after the fix; all PASS. The spec's counterfactual
necessity argument for `filter_yellow` (every yellow-tone arrival at
goal must traverse a yellow filter cell) still holds — the witness
uses (col 13, row 14), and alternative paths through cols 9..13 row
14 still exercise the filter.

Visit count: 1 / 6.
