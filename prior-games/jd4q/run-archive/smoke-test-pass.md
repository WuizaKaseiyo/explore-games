# Smoke test PASS — jd4q

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera 64×64 == level.grid_size 64×64 every level |
| CHECK_SPRITE_CONTENT | 6 | 9 | 12 | distinct non-letter-box palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions (1,2,3,4,6) referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | each action runs without exception (action_count advanced to 1) |
| CHECK_PALETTE_RANGE | 0..15 | 0..15 | 0..15 | within legal range |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 (11 east) → score 0→1; L2 (s×6, e×6, e×6, click@34,34, s×6 = 25) → score 1→2; L3 (s×6, e×6, n×6, click, e×6, click, s×6 = 32) → state WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | per-level resize present (`self.camera.width/height` mutated in `on_set_level`); all levels share `(64, 64)` so resize is a no-op but the code is in place |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY notes (per level)

- **L1**: PASS — single horizontal corridor visible at top of frame; magenta avatar (with pink eye) at left, purple square-frame goal at right; HUD bar visible at top edge. Matches spec L1 layout (S=(2,2), goal=(13,2), single floor row).
- **L2**: PASS — vestibule visible at top-left, S→J corridor (south then east), J at center, branch east of J as 5 light-blue door cells leading to green diamond pickup (pickup_a), continuation south to purple square goal at bottom. HUD bar visible at top. Matches spec L2 layout.
- **L3**: PASS — vestibule at top-left, S→J corridor (south then east), J at center; branch north (5 light-blue door cells) to green pickup at top; branch east (5 light-blue door cells) to blue diamond pickup; eraser cell visible (maroon corners with magenta cross) directly south of J; continuation south through floor to orange diamond pickup (pickup_c) and purple square goal at bottom. All 4 mechanic-relevant elements visible. HUD bar visible.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_action4_moves_avatar_east | x0=8 x1=12 | ACTION4 moves avatar +4 px east in L1 corridor |
| check_action_counter_increments | before=0 after=1 | engine `_action_count` advances by 1 per action |
| check_l2_echo_deposits_on_walk | before=0 after=1 | one walk in L2 (echoes_active) deposits one echo |
| check_l1_no_echoes_deposited | after one walk: echoes=0 | walks in L1 (echoes_active=False) do NOT deposit |

All 4 custom checks PASS.

Visit count: 1/6.
