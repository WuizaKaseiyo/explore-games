# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == level.grid_size (64, 64) for all 3 |
| CHECK_SPRITE_CONTENT | 5 | 5 | 7 | distinct non-letter-box palettes per level (≥ 2 required) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | ACTION1/2/3/4 all referenced in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on any of the 4 actions |
| CHECK_PALETTE_RANGE | 0..13 | 0..13 | 0..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | self.next_level() found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | self.lose() found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (64, 64); no per-level resize required |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 [ACTION3, ACTION1] → L2; L2 [ACTION3, ACTION4] → L3; L3 [ACTION3, ACTION4] → WIN (rev 4: same witness as L2; second colour adds planning load, no new mechanic) |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per-level notes
- **L1**: 8×8 checkered active region centred in frame; 1 orange filled piece (upper-left, cell 1,1) + 1 orange ring anchored target (lower-right, cell 6,6); HUD bar at bottom.
- **L2**: Same active region; 2 orange filled pieces (cells 1,4 and 6,4) + 1 orange ring anchored target (5,4); HUD bar.
- **L3**: Active region; 2 orange pieces (cells 1,4 and 6,4), orange anchored target at (5,4), 1 purple piece at (2,1), purple anchored target at (5,1); HUD bar. (decoy removed in rev 4)

Animation verified by rendering all 4 frames of an L1 ACTION3 fold: piece interpolates from (1,1) toward (6,1), the folded-out (left) half visibly recolours into a maroon overlay during phases 0–2, the active region snaps to its contracted form on phase 3 with the piece at the destination cell. No catastrophic rendering bugs; no sprite missing; no glyph resembling a letter or digit.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_fold_reflects_piece | cy0=4 cy1=3 (expected 7-cy0=3) | ACTION2 reflects piece's y-coord across horizontal mid-axis (M1) |
| check_same_colour_merge | before=2 after=1 | ACTION3 on L2 collapses two oranges to one (M2) |
| check_l3_two_colour_witness | L3 state after witness = WIN | L3 witness `[ACTION3, ACTION4]` lands both colours on their anchored targets simultaneously |
| check_l1_two_fold_witness | L1 score after 2-fold witness = 1 | no single fold wins L1; 2-fold witness `[ACTION3, ACTION1]` wins; ACTION2 and ACTION4 as first actions immediately fire `lose()` (anchored target destroyed) |
| check_anchored_target_lose | L1 ACTION2 → state == GAME_OVER | the anchored-target rule fires `lose()` when a fold retires the target's cell |

Visit count: 1/6.
