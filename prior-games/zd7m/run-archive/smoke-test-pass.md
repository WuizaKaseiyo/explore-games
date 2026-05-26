# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (20, 20) == level.grid_size (20, 20) for all levels |
| CHECK_SPRITE_CONTENT | 6 | 6 | 7 | distinct non-letter-box palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | ACTION1-4 all referenced in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | each ACTION1-4 runs without exception |
| CHECK_PALETTE_RANGE | 1..14 | 1..14 | 1..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | self.next_level() found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | self.lose() found |
| CHECK_CAMERA_DEFAULT | n/a | — | — | all levels share grid_size (20, 20); per-level resize unnecessary (still implemented in on_set_level for safety) |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual-sanity narrative (per level)

- **L1.** PASS — 3 pawns (top row at y=4: pink, yellow, light-blue
  with off-white centre dots) + 3 targets (bottom row at y=14:
  same colours, hollow dark centres). Step-counter green bar at
  top. Coarse layout matches spec.
- **L2.** PASS — pink pawn top-left, pink target top-right,
  yellow pawn middle-left, yellow target bottom-left, two grey
  checker anchor blocks visible (one near (7, 10), one near
  (14, 7)). Step-counter green bar at top.
- **L3.** PASS — pink pawn top-left, pink target top-right with
  anchor below it, yellow pawn middle-left, purple portal_a at
  bottom-left, yellow target visible inside the bottom-right
  chamber (bordered by two anchors), additional anchor between
  yellow pawn and the right-of-yellow zone. Step-counter green
  bar at top. Initial layer-order bug (portal_b hiding
  target_yellow) was caught here and fixed before re-render.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_cohort_step_moves_all_pawns` | all 3 pawns y+1 after one DOWN on L1 | cohort-step verified |
| `check_anchor_blocks_yellow_right` | pink.x=5, yellow.x=4 after one RIGHT on L2 | anchor (7, 10) blocks yellow ✓; pink moves freely ✓ |
| `check_portal_teleports_yellow` | yellow=(17, 17) after L3 witness (RIGHT × 10 + DOWN × 4) | portal teleport verified |
| `check_lose_at_step_budget` | state=GAME_OVER after 24 UPs (which immediately bound at the top edge so no progress is made) | step-budget exhaustion fires lose ✓ |

Visit count: 1 / 6.
