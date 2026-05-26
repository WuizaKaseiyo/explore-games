# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == level.grid_size (64,64) for every level |
| CHECK_SPRITE_CONTENT | 2 | 2 | 5 | distinct non-letterbox palette values per level (≥ 2 threshold met) |
| CHECK_ACTION_BRANCHES | ✅ | — | — | declared `[6]`, `GameAction.ACTION6` referenced in step() |
| CHECK_ACTION_RUNTIME | ✅ | — | — | ACTION6 raised no exception |
| CHECK_PALETTE_RANGE | 3..6 | 3..6 | 2..10 | within [0, 15] for every level |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 (2-action), L2 (3-action), L3 (4-action) witnesses all advance the engine; L3 reaches WIN state |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source (step-budget exhaustion path) |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all 3 levels share `grid_size=(64,64)` — no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity findings (per-level)

- **L1**: 5×5 grid of `+`-motif rook tiles top-left; target display
  bottom-right shows 14-lit magenta + tile pattern matching the spec's
  L1 target (cross-grid shape from XORing rook(1,1) ⊕ rook(3,3));
  magenta step-counter bar across row 63. PASS.
- **L2**: 5×5 grid with 23 `+`-motif rook tiles + 2 `X`-motif bishop
  tiles at cells (1,1) and (3,3); target display shows the 5-lit
  centred-plus pattern; HUD bar visible. The bishop motif is visibly
  distinct from the rook motif (X vs +), so a player can read the
  cell type off the rendered frame as the spec's checklist item 21
  requires. PASS.
- **L3**: 5×5 grid with rook (+) + bishop (X) + the tri-state ring
  tile at (2,2) (pink ring framing a light-grey state-0 centre);
  target display shows 9-lit magenta + cells + the tri-state
  mini-tile with a *light-blue* centre (= state 2 target); HUD bar
  visible. The three cell kinds are mutually distinguishable at a
  glance. PASS.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_rook_click_flips_row_and_col | initial_lit=0 after_lit=9 | one rook click in L1 toggles exactly 9 cells (5 row + 5 col − 1 corner) |
| check_bishop_click_flips_diagonals_only | initial_lit=0 after_lit=7 | one bishop click at (1,1) in L2 toggles exactly 7 cells (5 main-diag + 3 anti-diag − 1 centre) |
| check_tristate_advances_mod_3 | tristate(2,2) state after 2 flips = 2 | bishop(1,1) + bishop(3,3) deliver 2 flips through (2,2); tri-state cycles 0 → 1 → 2 mod 3 |
| check_l1_witness_advances_level | score before=0 after=1 | L1's 2-action witness advances the engine score by 1 (= level advance) |

Visit count: 1/6.
