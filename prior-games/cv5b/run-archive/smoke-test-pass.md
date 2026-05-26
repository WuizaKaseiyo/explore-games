# Smoke test PASS — cv5b

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | grid_size (64,64) == camera (64,64) per level |
| CHECK_SPRITE_CONTENT | 5 | 5 | 7 | distinct non-letterbox palette values (≥ 2 threshold) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | All 6 declared actions (1-6) referenced via `GameAction.ACTION{n}` in `step()` |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | Each of ACTION1..6 runs from a fresh game without exception; action_count increments |
| CHECK_PALETTE_RANGE | 0..12 | 0..12 | 0..12 | within [0, 15] all levels |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 1-action witness advances to L2; L2 14-action witness advances to L3; L3 36-action witness reaches WIN state |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | All levels share grid_size (64,64); per-level resize not required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per level

- **L1 PASS:** rendered frame shows orange launcher (bottom-left
  with yellow dot), pink hollow target ring (further right at the
  ground row), white step-counter HUD bar at top of frame, sky-blue
  background. Sprite count, placement and HUD presence all match
  the spec's L1 description.
- **L2 PASS:** orange launcher at bottom-left + two pink target
  rings (middle of frame and right of frame), HUD bar at top.
  Matches spec's L2 description (1 launcher + 2 targets, no shield,
  no wind).
- **L3 PASS:** orange launcher at bottom-left + black vertical
  shield bar (middle-left) + stippled blue/white wind column
  (middle-right) + pink target ring (right side), HUD bar at top.
  Matches spec's L3 description (1 launcher + 1 shield + 1 wind +
  1 target).

No catastrophic rendering bug, no symbol/letter/digit glyph in any
sprite, no overlapping sprites that read as a single blob.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_action4_walks_right | origin (4,50) → (5,50) | ACTION4 moves active launcher 1 cell right |
| check_action5_cycles_power | before=1 after=2 | ACTION5 cycles power 1→2 |
| check_l1_minimal_solve | level after solve=1 | ACTION6@(16,50) at L1 default power lands and advances to L2 |
| check_lose_at_budget | state after budget+1=GAME_OVER | step counter exhausts → `self.lose()` fires |

Visit count: 1/6.
