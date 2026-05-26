# Smoke test PASS — dj5h

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == level.grid_size for every level |
| CHECK_SPRITE_CONTENT | 10 | 11 | 12 | distinct non-letter-box palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 6 declared actions (1–6) referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | every action runs without exception |
| CHECK_PALETTE_RANGE | 1..13 | 1..13 | 1..14 | every rendered pixel within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | `WITNESS_L1` (6 actions) → L2; `WITNESS_L2` (16 actions) → L3; `WITNESS_L3` (20 actions) → WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all three levels share `grid_size=(64, 64)`; no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match the spec — beam + pulley wheel(s) at top, hanging coloured platforms with rope segments, floor islands at row 56-onwards, avatar humanoid at the spec-described start position, goal marker visible (slightly overlapping the platform's top edge at HIGH); HUD bar at row 63; no catastrophic rendering bugs. PNGs at `workspace/smoke-frames/level_*.png`. |

## Custom checks (mechanic invariants)

| Check | Observed | Notes |
|---|---|---|
| check_action4_moves_avatar_right | `x0=12 x1=16` | ACTION4 moves the avatar +4 px in x when destination is walkable |
| check_click_on_wheel_selects_pulley | `active_pulley='PA'` | ACTION6 inside the wheel footprint sets `active_pulley` |
| check_action5_flips_pulley_state | `before=LEFT_HIGH after=LEFT_LOW` | ACTION5 with an active pulley flips its binary state |
| check_toggle_carries_avatar_when_on_low_platform | `y0=53 y1=11` | When avatar is on a LOW platform, ACTION5 (toggle to HIGH) carries the avatar with the platform from row 53 to row 11 |

Visit count: 1 / 6.

All universal and custom checks pass. Proceed to `finalize`.
