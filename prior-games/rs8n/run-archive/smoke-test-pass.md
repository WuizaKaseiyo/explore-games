# Smoke test PASS  (revision 4 — L3 redesigned as a 3×5 grid)

Re-run after the redesign that dropped the L3 colour-shifter, made anchors strictly necessary via access-blocking walls, required east-and-west sweeps at L2, and added vertical-axis sweeps at L3.

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera viewport (64,64) matches level.grid_size (64,64) per level |
| CHECK_SPRITE_CONTENT | 8 | 9 | 9 | distinct non-letter-box palette values per rendered initial frame; threshold ≥ 2 |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | every action in [1,2,3,4,5] is referenced in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | each of the 5 actions runs without raising |
| CHECK_PALETTE_RANGE | 0..13 | 0..13 | 0..13 | every rendered pixel in [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (64,64); no per-level camera resize required |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 `[4,4,5]` advances 0→1; L2 (15-action witness) advances 1→2; L3 (31-action witness on the 3×5 grid) reaches state == WIN with score 3 |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered frames at workspace/smoke-frames/level_{1,2,3}.png — see notes below |

### CHECK_VISUAL_SANITY per-level notes
- **L1** — PASS. Frame shows perimeter walls, preview row at top with [blue bar, orange blob, yellow checker, pink ring] (the desired reversed order), a row of items [pink ring, yellow checker, orange blob, blue bar] in row 8, and the maroon avatar east-facing on the left. HUD bar visible at row 63 in pink.
- **L2** — PASS. Frame shows: top preview `[yellow checker, pink ring, gap, blue bar, orange blob]` (both segments reversed); row 8 with items at (3..7,8) split by the anchor pillar at (5,8); the access-blocking walls clearly visible immediately above and below the anchor (rendered as the same grey-brick texture as the perimeter). Avatar at left.
- **L3** — PASS. Frame shows the playable 3-row × 5-column grid at the centre of the arena (rows 4..6, cols 5..9) with the central anchor pillar clearly visible at (7,5) — its bright-centred pillar tile distinct from any wall. Items pack the other 14 grid cells (rings, checkers, blobs, bars in mixed colours). A matching 3×5 target-preview grid renders three rows below at rows 11..13 with a deliberate gap at (7,12) corresponding to the anchor. Avatar at left of arena. HUD bar at row 63. No access-walls visible because the grid's own packed geometry makes the anchor cell unreachable.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_action4_walks_east` | `x0=8 y0=32 -> (12,32)` | ACTION4 advances player one cell east on a clear path |
| `check_action5_advances_l1` | `level_index=1` | the L1 witness `[4, 4, 5]` advances past L1 — confirms ACTION5 runs the sweep state machine and the win predicate fires |
| `check_anchor_blocks_walk` | `x0=8 -> x1=8 (expected blocked)` | At L2 the avatar walking east into the item at (3,8) is blocked, rotating in place — confirms item collidability + rotate-on-block walking |
| `check_action_counter_decrements` | `before=50 after=49 delta=1` | one ACTION1 consumes exactly one unit of step budget |

## Verdict
**PASS.** All universal + visual-sanity + custom checks succeed on the revised design. Witnesses confirmed: L1=3 actions, L2=15 actions, L3=31 actions. Budgets 50/100/250 leave 17×/6.7×/8× cushion respectively.
