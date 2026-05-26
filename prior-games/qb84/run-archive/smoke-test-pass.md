# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == level.grid_size (64, 64) for all levels |
| CHECK_SPRITE_CONTENT | 5 | 6 | 6 | distinct non-letter-box palette values per level (excludes letter_box=4) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions ([1,2,3,4]) referenced in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | each of [1,2,3,4] runs without exception; action counter advances 0→1 |
| CHECK_PALETTE_RANGE | 0..14 | 0..15 | 0..15 | all rendered pixels in [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all 3 levels share grid_size (64, 64) — no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec's per-level descriptions; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per-level notes
- **L1:** 6 beads in S-curve (top row green-yellow-magenta L→R, bottom row magenta-yellow-green R→L) ✓; 3 plain "+/diamond" pegs (magenta+yellow above, green below) ✓; light-grey path markers connecting beads ✓; step bar at top (white centred) ✓; cursor white-corner indicator on B0 (left-most green bead, top-row) ✓; target ref strip in bottom-right ✓.
- **L2:** 8 beads in 2-row S-curve ✓; 5 pegs visible — sticky pegs show as diamonds with central black hole (palette 4 matches background) ✓; HUD + cursor + target strip ✓.
- **L3:** 10 beads in double-S layout (top row 4, middle row 2, bottom row 3) ✓; 7 pegs visible including pair-pegs marked with white corner pixel; sticky-trap pg_l3_g visible below B6 ✓; HUD + cursor + target strip ✓.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_lift_swaps_colors | bead 14→6 peg 6→14 | ACTION1 on B0 (above-peg present) swaps the bead and peg body colours bidirectionally |
| check_sticky_locks_bead | locked before=False after=True | ACTION1 on a sticky peg flips the bead's locked flag True |
| check_pair_propagation_sets_neighbour | partner_color_at_start=15 neighbour_after=15 | Lifting B5 onto pair-A propagates pair-B's purple (15) into the chain neighbour B6 |
| check_lose_at_budget | state after 24 ACTION3s: GameState.GAME_OVER | Exhausting L1's 24-step budget triggers self.lose() correctly |

Visit count: 1/3.
