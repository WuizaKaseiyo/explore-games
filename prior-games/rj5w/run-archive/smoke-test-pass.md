# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == level.grid_size (64, 64) for all 3 levels |
| CHECK_SPRITE_CONTENT | 5 | 8 | 8 | distinct non-letterbox palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 6 declared actions (1, 2, 3, 4, 5, 6) referenced in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on any action |
| CHECK_PALETTE_RANGE | 0..14 | 0..15 | 0..15 | all rendered pixels in [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` reachable in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | spec witnesses replay end-to-end → final state WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` reachable in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share `grid_size = (64, 64)`; no per-level camera resize needed |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY notes
- **L1**: off-white sheet, single orange dashed vertical fold-line at column 32, green pawn (4-fold-symmetric pattern) on the left, green target ring on the right, magenta HUD bar at row 63. Matches spec § Levels — Level 1.
- **L2**: 3 pawns (green top-left, yellow middle-left, purple bottom-left) and 3 targets (purple top-right, yellow middle-right, green bottom-right) arranged for diagonal-coupling. Vertical fold-line orange (active), horizontal fold-line grey (inactive). HUD present. Matches spec § Levels — Level 2.
- **L3**: green and purple pawns clustered upper-left (rows 16 and 8), yellow pawn at the centre (28, 28), three targets at the spec-described positions (green right at row 16, purple bottom-left at row 56, yellow at (36, 28) just right of the V-line). V-line orange (active), H-line grey (inactive). HUD present. Matches spec § Levels — Level 3.
- No sprite resembles a digit, letter, or arrow glyph. Pawns are abstract 4-fold-symmetric patterns; targets are hollow rings with a centre dot.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_v_fold_reflects_pawn | fv=32 x0=8 expected=56 got=56 | Verifies M1: V-fold at F_v reflects an unlocked pawn's x to 2·F_v − x. |
| check_axis_toggle_via_click | before=V after=H fh=30 | Verifies M3: clicking a cell on the H-line cursor (gy == fh) makes H the active axis. |
| check_lock_freezes_pawn | after_fold1=(56, 16) after_fold2=(56, 16) | Verifies M4: a pawn locked on its target stays put on the next V-fold (green at L3 doesn't move on the second V-fold). |
| check_lose_at_budget | budget0=25 state=GAME_OVER | Verifies the lose path: when the L1 budget exhausts, the engine state becomes GAME_OVER. |

Visit count: 1 / 6.
