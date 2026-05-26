# Smoke test PASS — vd3g

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == grid_size (64,64) every level |
| CHECK_SPRITE_CONTENT | 6 | 6 | 8 | distinct non-letter-box palette values per level (≥ 2 required) |
| CHECK_ACTION_BRANCHES | ✅ | — | — | `GameAction.ACTION6` referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | — | — | ACTION6 runs without exception |
| CHECK_PALETTE_RANGE | 1..14 | 1..14 | 1..14 | within legal [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 (6 actions) → L2; L2 (32 actions) → L3; L3 (30 actions) → WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size=(64,64); no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders at workspace/smoke-frames/level_*.png |

### Visual sanity diagnostics (one-liners per level)

- **L1 — PASS.** Outer black wall ring; inner playfield mostly mottled grey HIGH cells; one red cross-shaped marble at upper-mid (cell ≈ (5, 5)); one red ring target at lower-mid (cell ≈ (5, 9)); green-and-black step-counter bar at top row. Matches spec § Levels — L1.
- **L2 — PASS.** Outer wall ring + vertical wall column slightly left of centre with one mid-row gap; red marble on the west side; red target on the east side; HUD bar at top. Matches spec § Levels — L2.
- **L3 — PASS.** Outer wall ring + vertical wall column with TWO gaps at the two anchor rows (each gap shows a magenta corner-cap pixel marking the anchor link); red marble + blue target on the west side, red target + blue marble on the east side; HUD bar at top. Matches spec § Levels — L3.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_click_toggles_normal_cell | h0=1 h1=0 | clicking a NORMAL HIGH cell flips it to LOW |
| check_marble_rolls_to_dug_low | y0=5 y1=6 | digging the cell south of marble makes it roll one cell south |
| check_anchor_click_flips_partner | a:1→0 b:1→0 | clicking one anchor cell flips both linked anchors at once |
| check_lose_at_budget_exhaustion | state after budget+1 clicks = GAME_OVER | exhausting step budget triggers self.lose() |

## Aggregate

ALL_PASS = True. Visit count: 1/6.

Frames: `workspace/smoke-frames/level_1.png`, `level_2.png`, `level_3.png`.
Custom-check source: `workspace/smoke-test-custom.py`.
Aggregate JSON: `workspace/smoke-test-aggregate.json`.

**Decision**: PROCEED to `finalize`.
