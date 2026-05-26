# Smoke test PASS

Visit count: 2/6.

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (12,12)/(12,12)/(16,16) match level grid_size every level |
| CHECK_SPRITE_CONTENT | 3 | 4 | 7 | distinct non-letterbox palettes per level (≥ 2 required) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | both ACTION5 and ACTION6 referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | both raise no exceptions; action_count advances 0→1 |
| CHECK_PALETTE_RANGE | 0..14 | 0..14 | 0..14 | all values within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | self.next_level() and self.win() both present |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | self.lose() present |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | levels have differing grid_sizes (12,12)/(12,12)/(16,16); per-level camera resize present in `on_set_level` |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | all 3 rendered initial frames match the spec; PNGs at workspace/smoke-frames/level_*.png |

### CHECK_VISUAL_SANITY notes per level

- **L1 (PASS)** — Rendered frame shows: 1 red filled-square emitter (centre-left) + 1 red hollow-frame resonator (centre-right). Dark-grey background, black letter-box, yellow step-counter HUD bar at the bottom. Sprite count, placement, and HUD presence all match the spec's L1 description. No catastrophic rendering bug.
- **L2 (PASS)** — 2 emitters (red top-left, blue bottom-left) and 2 resonators (red top-right, blue bottom-right), with HUD bar. Quadrant-level placement matches spec. Colour-keying is readable from outline colours.
- **L3 (PASS)** — 3 distinct-colour emitters (red, blue, green) at corners; grey-outlined multi-colour resonator in centre with 2 coloured pips (red + blue) above its top edge; green-outlined single-colour resonator at the bottom-right; magenta phase-delay tile rendered as 4 corner dots (inactive state); HUD bar at bottom. All sprites visible, no overlaps, no clipping.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_action_counter_increments | before=0, after=1 | engine advances `_action_count` per ACTION6 |
| check_arm_emitter_toggle | after_click1=True, after_click2=False | M1: arm-state toggles per click on the same emitter |
| check_phase_delay_tile_toggle | counts=0/1/0 | M3: tile-state toggles per click on the tile |
| check_l1_minimal_solve | level after solve=1, state=NOT_FINISHED | M1 end-to-end: `[arm emitter_red, fire]` (2-action witness) advances L1 → L2; the state being NOT_FINISHED on the new level is the expected post-advance state |

All 13 checks (9 universal + 4 custom) pass on visit 2/6.
