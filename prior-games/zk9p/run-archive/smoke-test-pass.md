# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (14,14) / (16,16) / (18,18) match level.grid_size |
| CHECK_SPRITE_CONTENT | 6 | 8 | 9 | distinct non-letter-box palette values |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions branched in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions for ACTION1-5 on a fresh instance |
| CHECK_PALETTE_RANGE | 3-11 | 2-11 | 2-14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | `self.camera.width` / `.height` mutated in `on_set_level` |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY notes per level

- **L1** — magenta avatar visible centre-bottom, red and yellow
  pursuers in upper half (red left-of-centre, yellow right-of-centre);
  pink HUD bar at row 63; floor speckle pattern fills the playfield.
  Matches §4 L1 layout.
- **L2** — same avatar / red / yellow positions plus a cyan pursuer
  centred at the top; vertical wall column visible mid-grid (palette
  2 light-grey strip from y=4..9 with a small extension); pink HUD
  bar present. Matches §4 L2 layout.
- **L3** — five entities (avatar, red, yellow, cyan, green) and a
  more elaborate wall structure (horizontal break at y=8 with a
  2-cell gap, plus vertical wall column at x=4 in the lower half).
  Pink HUD bar present. Matches §4 L3 layout.

No glyphs that read as letters/digits in any frame; no catastrophic
rendering bugs; playfields fill the frame.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_up_moves_avatar | y0=10 y1=9 | ACTION1 decrements avatar y by 1 |
| check_pursuer_chases_after_avatar_move | red.y0=3 red.y1=4 | Manhattan pursuer steps toward avatar (Manhattan-major y) |
| check_l1_minimal_solve_advances_level | level_idx after UP×4 = 1 | merge-on-collision wires through to next_level() |
| check_lose_at_budget | state=GAME_OVER, budget=60, used=60 | step-budget exhaustion triggers lose() |

Visit count: 1/6.
