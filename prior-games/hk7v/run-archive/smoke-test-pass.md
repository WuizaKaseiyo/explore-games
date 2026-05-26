# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == every level grid_size (64,64) |
| CHECK_SPRITE_CONTENT | 7 | 9 | 11 | distinct non-letter-box palettes per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions branched in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on any action |
| CHECK_PALETTE_RANGE | 2..15 | 2..15 | 2..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | self.next_level() found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | self.lose() found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size=(64,64); no per-level resize needed |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 advanced 0→1, L2 advanced 1→2, L3 reached WIN |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per-level (manual inspection of the saved frames)

- **L1** — Trolley + hook visible top-left; floor (light-grey) at the
  bottom; one red block (with internal dual-colour pattern) on the
  floor at the left half; one red target stripe (dashed) on the
  right half of the floor; step counter present (the central dark bar
  at the very bottom row). Sprite count ≈ 4 + HUD (matches spec L1
  roster). Sprite placement matches spec (supply on left, target on
  right). PASS.
- **L2** — Adds a dark vertical wall in the middle of the playfield;
  red block (left) and blue block (right of wall, near target_blue);
  red target stripe (between supply column and wall) and blue target
  stripe (far right of floor). Wall is tall (rows 20..55) and 3 cells
  wide as spec described. Sprite count ≈ 4 blocks/targets + wall + HUD.
  PASS.
- **L3** — Same scaffold + the supply column at x=4 shows a stacked
  triple (yellow top, blue middle, red bottom) — three distinct
  blocks visibly stacked. Wall in middle. Three target stripes on
  the floor: blue (left of wall), yellow (right of wall), red (far
  right). Sprite count and placement match spec L3. PASS.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_action4_moves_trolley_right | x0=0 x1=1 | ACTION4 advances trolley by 1 cell |
| check_action2_lower_blocks_at_block_top | hook.y=49 (expected 49) | hook lowering stops adjacent to block top |
| check_action5_grabs_block_directly_below | carrying=Sprite | ACTION5 attaches block to hook when adjacent |
| check_lose_at_budget | state=GAME_OVER | exhausting step budget triggers lose |

Visit count to smoke_test: 1/6.

**Verdict: PASS — proceed to `finalize`.**
