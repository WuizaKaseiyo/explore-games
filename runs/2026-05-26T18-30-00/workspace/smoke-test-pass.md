# Smoke test PASS — hd7r (smoke_test visit 1/6)

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == level.grid_size (64,64) |
| CHECK_SPRITE_CONTENT | 6 | 7 | 8 | distinct non-letter-box palette values |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all of [1,2,3,4,6] branched in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on any declared action |
| CHECK_PALETTE_RANGE | 1..12 | 1..15 | 1..15 | within [0,15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` present |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1→L2 (score 0→1), L2→L3 (1→2), L3→WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` present |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | grids equal; resize present anyway |
| CHECK_LOSE_FIRES (dynamic) | ✅ | — | — | GAME_OVER after budget+2 wall-bumps on L1 |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; see workspace/smoke-frames/level_*.png |

### Visual sanity detail
- **L1**: amber HUD top row; grey beveled wall border; 1 orange creature
  (filled, eyes) center-right, 1 hollow orange pen ring top-right corner,
  teal shepherd lower-centre. Distinct shapes; no glyph/digit.
- **L2**: HUD; horizontal dividing wall with a single gate gap at centre
  (teal shepherd above it); 2 orange creatures (top-left, bottom-centre);
  2 hollow orange pens. Sprite count and quadrants match spec.
- **L3**: HUD; vertical dividing wall with gate at centre; magenta
  skittish creature + magenta pen on the west side, orange timid creature
  + orange pen on the east side. Two visually-distinct creature
  temperaments (orange vs magenta + shape tick) as specified.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_flee_straight_backs_away | creature (10,8)→(12,8) | straight creature steps away (never toward) |
| check_outside_radius_no_move | creature (10,8)→(10,8) | beyond scare radius ⇒ no move |
| check_perp_creature_sidesteps | skittish (5,11)→(5,10) | perp creature veers vertical, not straight back |
| check_closed_gate_blocks_then_opens | blocking=True → removed=True | click toggles gate closed→open |

All universal AND custom checks return PASS-equivalent results.

Visit count: smoke_test 1/6.
