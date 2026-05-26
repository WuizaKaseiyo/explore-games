# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == level.grid_size (64, 64) for all 3 levels |
| CHECK_SPRITE_CONTENT | 5 | 7 | 8 | distinct non-letter-box palettes per level (L1: {4, 9, 11, 12, 14}; L2: + {3, 8}; L3: + {7} for pink markers) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions (1, 2, 3, 4) reference `GameAction.ACTION<n>` in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | every action runs without exception; `_action_count` increments correctly |
| CHECK_PALETTE_RANGE | 1..14 | 1..14 | 1..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` is called from `step()` |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | each spec witness replayed against the live game advances past its level. Total witness 129 actions: L1 (18) + L2 (54) + L3 (54 L2-loops + 3 down-left detour for the bottom pink = 57). All three levels' witnesses cleanly trigger `next_level` (L1 → L2 → L3) and the L3 witness triggers `win` |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` is called from `step()` (budget-exhaust + 3-strike + pursuer-adjacent) |
| CHECK_CAMERA_DEFAULT | n/a | — | — | all 3 levels share `grid_size=(64, 64)`; no per-level camera resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png. L1: blue avatar, 3 yellow targets in centre row, green step-bar at top. L2: blue avatar bottom-centre, 4 yellow corner-targets, 3 red middle-column forbiddens, green step-bar + 3 grey strike-dots at top. L3: same as L2 plus 3 small pink 2×2 waypoints (left-mid, right-mid, just below the avatar) |

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_up_moves_avatar | y0=32 y1=28 | ACTION1 moves the avatar up by exactly one logical cell (4 pixels) |
| check_step_deposits_trail_at_old_position | old_pos=(20, 32) trail_present=True | a successful move deposits a trail_cell sprite at the avatar's previous cell |
| check_closure_advances_level | level_index_after_L1_witness=1 | L1 witness's closing-loop fires next_level (the closure-captures-interior mechanic is wired through to the engine) |
| check_blocked_by_forbidden | before=(32, 40) after=(32, 40) | avatar cannot step onto a forbidden cell (movement is blocked at the wall_residue / forbidden / target / pursuer collision rules) |

## Notes (post-finalize redesign)

The spec's original L3 used a moving pursuer (M5) plus closure-leaves-walls (M6). User feedback rejected the pursuer as "not a good design and not intuitive". L3 was redesigned to drop the pursuer and walls entirely and add **pink-marker waypoints (M5)** instead: a few small pink 2×2 squares the avatar's trail-head must step on for the level to win. The pink markers are sub-cell sprites (centred 2×2 inside a 4×4 cell, transparent borders); they don't block movement and they're consumed on entry.

The new L3 layout: same 4 corner targets + 3 forbidden column as L2, plus 3 pink markers at cells `(2, 7)`, `(14, 7)`, `(8, 14)`. The L2 witness already naturally walks through `(2, 7)` (on loop 1's left edge) and `(14, 7)` (on loop 2's right edge); the third at `(8, 14)` needs a 3-step `[down, left, left]` detour after loop 2's closure. L3 witness is 57 actions, well within the 200-step budget.

The redesign keeps L1 and L2 unchanged. Composition rule still satisfied (L1=2, L2=4, L3=5; each promotion adds 1–2 new mechanics).

Visit count: 1/6.
