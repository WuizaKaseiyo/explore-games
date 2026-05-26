# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == level.grid_size (64, 64) for every level |
| CHECK_SPRITE_CONTENT | 5 | 5 | 6 | distinct non-letter-box palettes (palettes {1, 3, 4, 10, 14} for L1/L2; +6 magenta in L3) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | both declared actions (5, 6) referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions; ACTION5 and ACTION6 each increment _action_count by 1 |
| CHECK_PALETTE_RANGE | 1..14 | 1..14 | 1..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (64, 64); per-level resize present in `on_set_level` (defensive) |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per-level notes

- **Level 1 (PASS).** Grey hollow + cross (slot) at logical (3, 8) center; light-blue hollow ring (target) at (12, 8) center. Border of grey/dark-grey 4×4 checker walls around the playfield. Step-counter green bar at the top edge. No HUD overlap, no catastrophic rendering bug. Matches spec § 4 L1 (slot at (3, 8), target at (12, 8), no walls beyond border).
- **Level 2 (PASS).** Two grey hollow + crosses on the left side (logical (3, 4) and (3, 12)); two light-blue hollow rings on the right (logical (12, 4) and (10, 12)). Border + step-counter bar visible. Matches spec § 4 L2.
- **Level 3 (PASS).** Two grey hollow + crosses (slot_blue at (2, 2), slot_magenta at (4, 13)); one magenta hollow ring (target_magenta at (13, 2)) and one light-blue hollow ring (target_blue at (13, 13)). Vertical wall column at logical x=8 with single-row gap at y=7 — clearly visible bisecting the chamber. Border + step-counter bar visible. Matches spec § 4 L3.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_action6_activates_slot | emitters before=0 after=1 | ACTION6 click on L1 slot's center cell creates exactly one active emitter |
| check_action5_advances_global_tick | tick before=0 after=1 | ACTION5 increments the global tick counter by exactly 1 |
| check_l1_minimal_solve | level after L1 witness=1 | L1's full witness (1× ACTION6 + 9× ACTION5) advances level_idx to 1 |
| check_lose_at_budget | state after budget+1=GAME_OVER | spamming ACTION5 past L1's 30-step budget triggers GAME_OVER |

Visit count: 1/6.
