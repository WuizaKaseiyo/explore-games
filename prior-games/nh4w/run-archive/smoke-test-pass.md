# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | grid_size=(64,64) and camera=(64,64) for every level |
| CHECK_SPRITE_CONTENT | 6 | 8 | 9 | distinct non-letter-box palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | ACTION3, ACTION4, ACTION6 all referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on any of [3, 4, 6] |
| CHECK_PALETTE_RANGE | 3..14 | 3..14 | 3..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 witness `[ACTION4, ACTION6@(56,51)]` advances to L2; L2 witness `[ACTION4, ACTION4, ACTION6@(62,51)]` advances to L3; L3 witness `[ACTION4, ACTION6@(40,51), ACTION4, ACTION6@(52,51)]` reaches WIN state |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (64,64); per-level resize present in `on_set_level` for safety |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual-sanity per-level notes

- **L1.** PASS. Launcher pawn (blue body + yellow muzzle) sits on the floor near the left edge; single yellow target on the floor near the right edge; HUD bar (green) at the top row; sky (light-blue palette 10) fills the air. Matches the spec's L1 layout: launcher (4, 46), target_yellow (56, 51), no walls/ceilings.
- **L2.** PASS. Same as L1 plus a brick-patterned wall (orange-red on dark-red) standing on the floor between launcher and target. Matches spec L2 layout: wall_h8 at (24, 43), target_yellow (60, 51).
- **L3.** PASS. Same as L2 plus two grey hanging stalactites with maroon drips at their tips: a longer one over the launcher's column (covering x ≈ 8-15) and a shorter one over the wall's right side (covering x ≈ 32-39). Two targets on the floor (yellow then blue). Matches spec L3 layout.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_action4_moves_launcher_right | x0=4 x1=8 | ACTION4 advances launcher 4 px right |
| check_action3_blocked_at_left_edge | x0=0 x1=0 | walking blocked at playfield left bound |
| check_action6_fires_arc_lands_on_target_l1 | score 0 -> 1 (in 0 extra ticks) | click in range from x=8 lands on L1 target and advances level |
| check_action_counter_increments_per_walk | before=0 after=1 | engine action counter advances on each walk |

## Counterfactual binding (L3 mechanic-necessity, run as part of CHECK_WITNESS_WINS investigation)

| Launcher x | Click x | Result | Spec expectation | Match |
|---|---|---|---|---|
| 4 | 40 (yellow) | blocked (collision idx 3, ceiling1) | blocked | ✓ |
| 8 | 40 (yellow) | lands on target_yellow | lands | ✓ |
| 12 | 40 (yellow) | blocked (collision idx 5, wall) | blocked | ✓ |
| 16 | 40 (yellow) | blocked (collision idx 3, wall) | blocked | ✓ |
| 4 | 52 (blue) | blocked (collision idx 3, ceiling1) | blocked | ✓ |
| 8 | 52 (blue) | blocked (collision idx 12, ceiling2) | blocked | ✓ |
| 12 | 52 (blue) | lands on target_blue | lands | ✓ |
| 16 | 52 (blue) | blocked (collision idx 3, wall) | blocked | ✓ |

All 8 cases match the spec's intent: yellow only fires from x=8, blue only fires from x=12, and the trivial heuristic "fire both shots from the same launcher position" genuinely fails.

Visit count: 1/6.
