# Smoke test PASS — mw8p

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == level.grid_size for every level |
| CHECK_SPRITE_CONTENT | 9 | 9 | 10 | distinct non-letter-box palette values per level (all ≥ 2) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions (1..4) referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on a fresh-game first action for each declared action |
| CHECK_PALETTE_RANGE | 0..15 | 0..15 | 0..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | spec witnesses replayed via `perform_action(ActionInput(...))`; L1 score 0→1, L2 score 1→2, L3 reaches `WIN` |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | uniform `grid_size = (64, 64)` across all 3 levels; no per-level resize needed |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at `workspace/smoke-frames/level_{1,2,3}.png` (L1: walled middle chamber with B + col-7 corridor + bottom-left A + top-right exit; L2: open arena with C above B in col 4 + A top-left + exit bottom-right; L3: A bottom-left + C₁/C₂/B along row 7 + wall row above row 7 + top-right exit) |

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_right_moves_player | x0=1 x1=9 | ACTION4 translates the player by +8 px in x when the destination cell is empty and in-bounds |
| check_a_eats_c_on_entry | C₁ interaction = REMOVED | M3 fires on turn 1 of L3: ACTION4 from (0, 7) consumes the C₁ at (1, 7) (interaction transitions to `InteractionMode.REMOVED`) |
| check_c_kills_b_on_coincidence | B interaction = REMOVED | M2 fires on turn 1 of L2: after ACTION4, the C at (4, 3) steps to (4, 4) where B has just landed; B's interaction transitions to `InteractionMode.REMOVED` |
| check_lose_at_budget | state after 25 blocked-LEFT = GAME_OVER | The step-counter HUD's lose path fires: 25 ACTION3 from (0, 7) are all blocked by the left bound and increment `_steps_used`; on the 25th `_steps_used >= max_steps` triggers `self.lose()` |

Visit count: 1/6.

All universal AND custom checks pass on the first smoke-test entry.
Transition: `finalize`.
