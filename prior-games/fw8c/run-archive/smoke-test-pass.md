# Smoke test PASS — fw8c

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | grid_size (64,64), camera (64,64) |
| CHECK_SPRITE_CONTENT | 6 | 8 | 10 | distinct palette values per level (incl. background + walls + sprites) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions referenced via `GameAction.ACTIONn` |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | each of [1,2,3,4] perform_action returned without raising |
| CHECK_PALETTE_RANGE | 1..12 | 1..14 | 1..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` present in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 (9 actions) → level 1 advanced; L2 (20 actions) → level 2 advanced; L3 (26 actions) → state WIN reached |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` present in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all 3 levels use grid_size (64, 64) — no per-level camera resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered PNGs inspected; sprite counts and placements match spec |

### CHECK_VISUAL_SANITY notes

PNGs at `runs/2026-05-10T06-15-58/workspace/smoke-frames/level_1.png`,
`level_2.png`, `level_3.png`.

- **L1**: rendered frame shows carrier at top-left (black-outlined
  hollow body with off-white centre), pad_orange (orange concentric
  ring with off-white centre) at the middle of the playfield, and
  slot_orange (thick orange rim with off-black centre) at the
  bottom-right. Wall border visible. HUD bar visible across top
  row. Three distinct sprite shapes present per spec, each in the
  region the spec describes. PASS.
- **L2**: 5 sprite clusters visible — carrier (top-left), pad_orange
  + pad_pink along row 3, slot_pink at left of row 5, slot_green
  at right of row 5. All distinct shapes per spec. PASS.
- **L3**: chamber partitioned by an interior wall row at y=4 with a
  green barred-door (`door_green`) at the middle gap. Upper half
  shows carrier (top-left), pad_orange (left of row 3),
  pad_pink_upper (right of row 3). Lower half shows slot_green +
  pad_lightblue along row 5, and slot_pink + pad_pink_lower +
  slot_lightblue + slot_magenta along row 6. The door's X-bar
  pattern is visually distinct from the slots' hollow rim, per
  checklist item 21. HUD visible. PASS.

No catastrophic rendering bugs; no glyphs resembling letters/digits.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_arrow_moves_carrier | x0=9 x1=17 | ACTION4 advances carrier by STEP_SIZE pixels |
| check_pad_pickup_sets_pigment | pigment_set=0b1 | walking onto pad_orange ORs bit 0 |
| check_slot_consume_clears_pigment | post-consume pigment_set=0 | matching-state slot consume resets carrier |
| check_door_blocks_when_unmatched | before=(33,25) after=(33,25) pigment_set=0 | door_green at (4,4) blocks the carrier when state ≠ {O,P} |

Visit count: 1/6.

**Verdict**: PASS — proceed to `finalize`.
