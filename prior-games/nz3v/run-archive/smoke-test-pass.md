# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera viewport (12, 12) == level.grid_size (12, 12) for every level |
| CHECK_SPRITE_CONTENT | 8 | 9 | 9 | distinct non-letter-box palette values: L1={0,1,4,5,6,10,11,14}; L2 adds 12; L3 adds 12 |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions (1, 2, 3, 4) referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on any action |
| CHECK_PALETTE_RANGE | 0..14 | 0..14 | 0..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | levels share grid_size; resize-per-level still implemented in `on_set_level` |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 (18 actions) + L2 (15 actions) + L3 (15 actions) advance score 0→1→2→3; final state == WIN |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | all four sanity questions pass for every level (sprite count, placement, HUD presence, no catastrophic rendering bug); see `workspace/smoke-frames/level_*.png` |

### CHECK_VISUAL_SANITY notes per level

- **L1**: NW quadrant lit (yellow 4-corner-dot pattern); avatar (light-blue chequered) at NW corner; central rotor with yellow notch (pointing at NW lit sector) + magenta direction-marker dot at NE side (indicating clockwise next-direction); target (green chequered ring) at SE corner; step-counter bar visible on bottom row.
- **L2**: NW quadrant lit; avatar at NW corner; vertical wall column at gx=4 (3 wall cells visible as black squares); stop-tile (solid orange square) at (2, 4); rotor at centre with notch/marker; target at NE corner.
- **L3**: NW quadrant lit; avatar at NW corner; wall cells at gx=3 (3 separated black squares); stop-tile (orange) at (2, 3); counter-switch (magenta square) at (4, 5); rotor at centre; target at SW corner.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_action4_moves_avatar_east | x0=1 x1=2 | ACTION4 moves avatar one cell east when destination is in lit sector |
| check_action_counter_increments | before=0 after=1 | engine `_action_count` advances per action |
| check_rotor_advances_after_K_actions | angle_before=0 angle_after=1 | after K=6 valid NW-phase actions, rotor angle advances NW (0) → NE (1) |
| check_stop_tile_freezes_rotor | frozen_before=0 frozen_after=3 | stepping on L2's stop-tile arms `_frozen_remaining` (initial K_FREEZE=4 minus the per-action decrement = 3 immediately after) |

Visit count: 1 / 6.

## Verdict

**PASS** — every universal check and every custom check passes.
Transition to `finalize`.
