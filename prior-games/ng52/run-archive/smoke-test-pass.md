# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera 64×64 == grid_size 64×64 |
| CHECK_SPRITE_CONTENT | 4 | 5 | 5 | distinct non-letter-box palettes |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | ACTION5 + ACTION6 both branched |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions |
| CHECK_PALETTE_RANGE | 0..9 | 0..15 | 0..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | resize present |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per level
- **L1** — 3 hollow bins side by side; single-stick blue signatures of lengths 3/4/5 above each bin; 3 small blue objects (L-tromino, T-tetromino, plus-pentomino) below the divider. Step bar visible at top. Matches spec § Levels — Level 1.
- **L2** — same 3-bin frame; signatures show single blue (length 6), blue+purple stacked (lengths 3+3), blue+purple stacked (lengths 4+2); 6 objects in the pool (4 blue + 2 purple shapes). Matches spec § Levels — Level 2.
- **L3** — same as L2 PLUS a 5-blue plus-shape (the distractor) sitting beneath the regular pool row at the bottom-left. Matches spec § Levels — Level 3.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_click_selects_object | selection=o1 | clicking a pool object marks it selected |
| check_place_in_bin | container=bin_0 placed=[o1] | clicking a bin with a selection places the object |
| check_failed_commit_resets_pool | container=pool pos=(8,38) | a wrong-bin commit snaps every placement back to its pool origin |
| check_l1_minimal_solve | level after solve=1 | the 7-action L1 witness advances past L1 |

Visit count: 1/3.
