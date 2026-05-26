# Smoke Test Pass

## Universal checks

| Check | Result |
|---|---|
| CHECK_CAMERA_VIEWPORT | PASS |
| CHECK_SPRITE_CONTENT | PASS |
| CHECK_ACTION_BRANCHES | PASS |
| CHECK_ACTION_RUNTIME | PASS |
| CHECK_PALETTE_RANGE | PASS |
| CHECK_WIN_PATH_EXISTS | PASS |
| CHECK_LOSE_PATH_EXISTS | PASS |
| CHECK_CAMERA_DEFAULT | PASS |
| CHECK_VISUAL_SANITY | PASS |

## Custom checks

| Check | Result |
|---|---|
| check_l1_first_lift | PASS |
| check_l2_latch_restores_right | PASS |
| check_l2_witness_wins | PASS |
| check_l3_bridge_deploys | PASS |
| check_l3_witness_wins | PASS |

Verified witness sequences:
- L1: `[4, 4, 1, 1, 4, 5, 4, 4, 4, 4, 4]`
- L2: `[4, 4, 1, 1, 4, 5, 4, 4, 4, 2, 2, 2, 4, 5, 4, 4, 4, 4, 4]`
- L3: `[4, 4, 1, 1, 4, 5, 4, 4, 4, 2, 2, 2, 4, 5, 4, 4, 4, 4, 4, 4]`

