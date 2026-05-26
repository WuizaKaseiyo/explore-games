# Smoke test PASS — wt39

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera 14×14 == grid_size 14×14 |
| CHECK_SPRITE_CONTENT | 4 | 5 | 6 | distinct non-letter-box palette values |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions reference `GameAction.ACTION<n>` in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions; `_action_count` increments per call |
| CHECK_PALETTE_RANGE | 0..13 | 0..13 | 0..13 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` reachable |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` reachable |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (14, 14); per-level resize not required, but camera viewport is set in `on_set_level` anyway |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at `workspace/smoke-frames/level_*.png` |

Visual notes per level:
- **L1.** Red pawn at top-left; maroon goal-ring at lower-mid; two
  black wall blocks visible (one in upper-right of the playfield,
  one below the goal). Red HUD bar fills the top edge.
- **L2.** Red pawn at top-left; orange bumper at top-right; three
  black wall blocks (mid-left, mid-right, just below the goal);
  maroon goal-ring lower-left. Spec described: 1 pawn + 1 goal +
  3 walls + 1 bumper — all present.
- **L3.** Red pawn at top-left; orange bumper at top-right; three
  black wall blocks; maroon goal-ring; light-blue thaw-tile just
  above the goal. Spec described: 1 pawn + 1 goal + 3 walls + 1
  bumper + 1 thaw_frozen — all present.

No catastrophic rendering bugs. No sprite resembles a digit, letter,
or culturally-loaded glyph (all are colored squares).

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_right_slides_until_wall | x=8 y=2 | RIGHT from (2, 2) glides east and stops one cell west of the wall at (9, 2). M1 (slide-until-wall) verified. |
| check_bumper_deflects_right_to_down | x=10 y=6 | RIGHT from L2 start hits the bumper at (10, 2) and deflects south to (10, 6) (one cell above wall (10, 7)). M2 (bumper-deflect) verified. |
| check_thaw_cracks_after_one_pass | cracked-at-4-8 count=1 | After the L3 path RIGHT-LEFT-DOWN, the original `thaw_frozen` at (4, 8) has been removed and a `thaw_cracked` sprite occupies (4, 8). M3 (thaw-cracking) verified. |
| check_lose_at_budget | state after exhausting budget: GAME_OVER, steps=0 | Spamming UP/DOWN on L1 ping-pongs the pawn between (2, 1) and (2, 12) without ever reaching the goal; after 30 actions, `state == GAME_OVER`. Lose path verified. |

Visit count: 1/6.
