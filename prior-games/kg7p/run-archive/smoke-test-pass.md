# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | PASS | PASS | PASS | camera (64, 64) == level.grid_size for every level |
| CHECK_SPRITE_CONTENT | 7 | 7 | 8 | distinct non-letter-box palettes per level |
| CHECK_ACTION_BRANCHES | PASS | PASS | PASS | all 5 declared actions referenced in step() |
| CHECK_ACTION_RUNTIME | PASS | PASS | PASS | each action runs without exception; _action_count advances |
| CHECK_PALETTE_RANGE | 4..15 | 4..15 | 4..15 | within [0, 15] for every level |
| CHECK_WIN_PATH_EXISTS | PASS | — | — | next_level() found in source |
| CHECK_WITNESS_WINS | PASS | PASS | PASS | L1 witness → score 1; L2 witness → score 2; L3 witness → WIN |
| CHECK_LOSE_PATH_EXISTS | PASS | — | — | lose() found in source |
| CHECK_CAMERA_DEFAULT | n/a | — | — | all levels have identical grid_size = (64, 64); no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered frames match spec — see `workspace/smoke-frames/level_*.png` |

### Visual sanity per level

- **L1** — avatar (light-blue body with green emitter) at left-middle, yellow hollow block in the middle, blue+orange target ring on the right. HUD bar at bottom. Matches spec L1 layout (avatar at logical (3,8), block at (8,8), target at (12,8)).
- **L2** — avatar at left-middle, yellow hollow block at upper-middle, orange hollow block at middle-middle, magenta-rimmed target with yellow interior at bottom-middle. Target_orange (under the avatar at logical (3,8)) is rendered beneath the avatar layer; revealed once the player moves. Matches spec L2 layout.
- **L3** — avatar at upper-left, two yellow blocks with magenta edge-stripes at middle (block_D with east-stripe at (3,5), block_C with north-stripe at (5,5)), two blue-and-red target rings at top-middle and middle-right (target_C at (5,1), target_D at (8,5)). Matches spec L3 layout. Magenta stripes are clearly visible as edge markings, not arrow glyphs.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_east_moves_avatar | x0=12 x1=16 | ACTION4 moves the avatar one cell (4 px) east |
| check_action5_toggles_beam | before=False after=True | ACTION5 toggles beam state |
| check_beam_couples_block_on_walk | coupled=True block_x=32 | after 4 east walks with beam on, block at (8,8) becomes coupled |
| check_lose_at_budget | state_after_budget+1=GAME_OVER | step budget exhaustion triggers lose() |

Visit count: 1 of ≤6.
