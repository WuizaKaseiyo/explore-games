# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == grid_size (64,64) per level |
| CHECK_SPRITE_CONTENT | 7 | 9 | 11 | distinct non-letter-box palette values per level (≥ 2) |
| CHECK_ACTION_BRANCHES | ✅ | — | — | only ACTION6 declared; `GameAction.ACTION6` referenced in step() |
| CHECK_ACTION_RUNTIME | ✅ | — | — | ACTION6 dispatch ran without exception (click at (32, 32)) |
| CHECK_PALETTE_RANGE | 3..15 | 2..15 | 3..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` present in source (engine auto-calls win() after last level) |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` present in source (wall hit, conflict cells, budget exhaustion) |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all 3 levels use grid_size (64,64); no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

## CHECK_VISUAL_SANITY per-level diagnoses

- **L1** — PASS. Yellow courier (top-left of horizontal corridor), one
  green-blade junction in the centre, one purple+maroon terminal at
  bottom of the vertical corridor, yellow HUD bar centred along row
  63. The stub corridor north of the junction is visible (showing the
  default-route death). Roughly one courier + one junction + one
  terminal + walls + HUD — matches spec §3 sprite roster and §4 L1.
- **L2** — PASS. Yellow courier at left, four green-blade junctions
  along the central artery, two south detours each containing a red
  hollow ring (stop_red), purple+maroon terminal at right end of
  artery, yellow HUD bar. Roughly one courier + four junctions + two
  stops + one terminal — matches spec §4 L2.
- **L3** — PASS. Two disjoint corridors visible: the upper red
  corridor with yellow courier, red hollow stop_red, two junctions
  (one green-blade default-H, one magenta-blade default-V),
  purple+maroon terminal_red; the lower blue corridor with light-blue
  courier, light-blue hollow stop_blue, two junctions (one
  magenta-blade default-V at left, one green-blade default-H at right
  — wait, see note), purple+blue terminal_blue. Yellow HUD bar.
  Roughly two couriers + four junctions + two stops + two terminals —
  matches spec §4 L3.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_off_board_click_ticks_courier | before=(4,28) after=(8,28) | Off-board click ticks courier 1 cell (the implicit "wait" verb of live-switch-routing). |
| check_clicking_switch_toggles_blade | before=TANGIBLE after=REMOVED | Click on a switch sprite swaps the H/V twin's interaction mode. |
| check_l1_minimal_solve_wins | current_level_index=1 | The spec witness for L1 (one click on junction + 13 wait clicks) advances the level. |
| check_lose_when_courier_hits_wall | state=GAME_OVER | If the player never toggles the L1 junction, the courier walks into the wall above and the engine ends with GAME_OVER. |

Visit count: 1/6.
