# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == every level grid_size (64,64) |
| CHECK_SPRITE_CONTENT | 2 | 3 | 5 | distinct non-letter-box palettes per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | both ACTION5 and ACTION6 branched |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on either action |
| CHECK_PALETTE_RANGE | 0..14 | 0..14 | 0..15 | all within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` and `self.win()` (via engine) found |
| CHECK_WITNESS_WINS | PASS | PASS | PASS | L1 (`(15,15),(50,15),(30,50),A5`) → score 0→1; L2 (`(12,15),(52,15),(32,55),A5`) → score 1→2; L3 (`(12,13),(54,13),(54,54),(12,54),A5`) → WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all 3 levels share grid_size (64,64); per-level resize present in `on_set_level` regardless |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at `workspace/smoke-frames/level_*.png` |

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_action6_places_post` | posts before=0 after=1 | clicking an empty playfield cell adds a `vertex_post` |
| `check_action5_with_zero_posts_is_noop` | greens before=3 after=3 | ACTION5 with no posts removes nothing |
| `check_action5_captures_enclosed_green` | L1_greens=3 level_after=1 | placing a triangle around all 3 greens + commit captures all and advances level |
| `check_strike_on_maroon_capture` | strikes before=0 after=1 | committing a pen that encloses a maroon adds exactly 1 strike |

Visit count: 1 / 6.

## Visual sanity notes (per-level)

- **L1.** PASS — 3 green critter blobs scattered in the playfield centre,
  3 small green tally dots at the top, green step-counter bar at the
  bottom. Matches spec layout (3 greens at `(20,20)`, `(40,22)`, `(30,40)`).
- **L2.** PASS — 3 green critters in the centre cluster + 4 maroon
  critters at the playfield corners + 3 green tally dots + green step
  bar. Matches spec layout.
- **L3.** PASS — 3 greens, 2 yellows, 3 maroons, 3 purple patrollers
  (visibly distinct shape — single-eye tapered diamond), 3 green + 2
  yellow tally dots. Matches spec layout.
