# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == level.grid_size (64, 64) for every level |
| CHECK_SPRITE_CONTENT | 6 | 8 | 8 | distinct non-letter-box palettes per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions (1, 2, 3, 4, 5) referenced via `GameAction.ACTION<n>` |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | all 5 actions ran without exception; `_action_count` advanced |
| CHECK_PALETTE_RANGE | 0..14 | 0..15 | 0..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 witness (9 actions) → score 0→1; L2 witness (25 actions) → 1→2; L3 witness (22 actions) → 2→3 with state == WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all 3 levels share grid_size (64, 64); per-level resize code is present in `on_set_level` regardless |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

## CHECK_VISUAL_SANITY notes per level

- **L1** (PASS): rendered frame shows the avatar (maroon block with white corner indicator) at the left of a stone-bordered corridor at row 4, two grey-striped walls at tiles (3, 4) and (5, 4) on the corridor, and the green nested-square exit at the right. The step counter HUD is the thin black-and-white bar across row 0. Stones above row 3 and below row 5 visually frame the corridor as the spec describes.
- **L2** (PASS): the red charge-pad is at top-left (tile (1, 0)), the blue charge-pad is mid-right at (6, 2), the avatar is at left, the red and blue walls sit on the corridor at (3, 4) and (5, 4), and the exit is at the far right. Vertical stone barriers seal col 3 (except (3, 4)) and col 7 (except (7, 4)); the right-half stone diagonals at (5, 1)/(5, 3)/(5, 5)/(6, 3)/(6, 5) are visible as the dark blocky shapes that funnel access to (6, 4) only via the blue wall.
- **L3** (PASS): same layout as L2 but with two visible red walls in col 3 — the upper one at (3, 1) shows TWO stripes (hardness 2) and the lower one at (3, 4) shows THREE stripes (hardness 3). The stripe-count visual cue for the layered-hardness mechanic is unambiguously legible from the rendered frame, distinguishing the two walls' required strike counts.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_arrow_moves_avatar | x0=0 x1=8 | ACTION4 moves the avatar +8 pixels east (one logical tile) |
| check_uncharged_erode_is_noop | before=[((3,4),1),((5,4),1)] after=[((3,4),1),((5,4),1)] | At L2 the avatar is uncharged; ACTION5 leaves wall hardness unchanged |
| check_charge_pad_sets_state | charge_state=red | Walking onto the red pad at L2 sets `charge_state` to `"red"` |
| check_l3_layered_hardness | wall_hardness[(3,1)]=2 | At L3 the (3, 1) red wall starts at hardness 2 (multi-strike layered-hardness mechanic) |

Visit count: 1/6.
