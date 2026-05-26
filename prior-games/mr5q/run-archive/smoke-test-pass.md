# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (16,16) == level.grid_size (16,16) for all three levels |
| CHECK_SPRITE_CONTENT | 3 | 5 | 9 | distinct non-letter-box palette values per level (≥ 2 each) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | both ACTION5 and ACTION6 referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | ACTION5 and ACTION6 both run without exception |
| CHECK_PALETTE_RANGE | 1..14 | 1..14 | 0..15 | all rendered pixels in [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | self.next_level() found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | self.lose() found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | source mutates self.camera.width/height in on_set_level (kept even though all levels have same grid_size, defensive) |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec — see workspace/smoke-frames/level_*.png |

### Visual sanity per level (the four-question check)

**L1 (level_1.png)** — PASS
- Sprite count: 2 green-yang pawns visible (matches spec § L1: "2 green pawns at start").
- Sprite placement: pawns at upper-left and lower-right, axis-symmetric (matches spec layout (3, 4) and (10, 9)).
- HUD presence: dark step-counter bar visible at top row (matches spec § HUD).
- Catastrophic rendering: none — playfield fills the cream background; pawns clearly readable as ringed sprites with yellow top-half (yang).

**L2 (level_2.png)** — PASS
- Sprite count: 4 pawns in 2 colour groups (2 green-yang at top row, 2 orange-yin at bottom row). Matches spec § L2 (greens both yang, oranges both yin).
- Sprite placement: greens above oranges, axis-symmetric. Matches spec layout.
- HUD: step-counter bar visible at top row.
- Catastrophic rendering: none — clearly readable colour groups; the half-fill polarity orientation is visually obvious (yang yellow on top vs yin magenta on bottom).

**L3 (level_3.png)** — PASS
- Sprite count: 2 green-yang above the y=4 wall; 1 orange-yin above the y=10 wall; 1 orange-yin below the y=10 wall; 2 horizontal walls; 1 flip-pad at the y=10 wall gap. Matches the implemented L3 layout.
- Sprite placement: greens isolated above the y=4 full-strip wall; orange pair on opposite sides of the y=10 wall; flip-pad in the wall's only gap.
- HUD: step-counter bar visible at top.
- Catastrophic rendering: none — walls and gap legible; the flip-pad's checkered light-blue+white pattern is clearly distinct from any pawn or wall.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_click_flips_polarity | before=yang after=yin | ACTION6 on a pawn toggles its polarity bit |
| check_tick_moves_attracted_pair | pair0 (3,4)→(4,4); pair1 (10,9)→(9,9) | ACTION5 moves opposite-state pawns toward each other |
| check_discharge_at_adjacency | both pairs discharged | flip + ticks → opposite-state pair within Cheb-distance ≤ PAWN_SIZE removes both |
| check_action_counter_increments | before=0 after=1 | engine action counter advances on each step() |

## Verdict

**ALL UNIVERSAL CHECKS AND ALL CUSTOM CHECKS PASS. PROCEED TO `finalize`.**

Visit count: 1/3.
