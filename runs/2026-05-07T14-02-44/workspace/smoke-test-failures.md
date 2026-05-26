# Smoke test FAILURES (visit 1/6)

## Universal checks

All 8 programmatic universal checks PASS:

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera 12×12 == level grid_size 12×12 every level |
| CHECK_SPRITE_CONTENT | 3 | 4 | 7 | distinct non-letterbox palettes ≥ 2 every level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | both ACTION5 and ACTION6 referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | both actions raise no exceptions; action_count advances 0→1 |
| CHECK_PALETTE_RANGE | 0..14 | 0..14 | 0..14 | within [0, 15] every level |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | self.next_level() and self.win() both present |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | self.lose() present |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | per-level camera resize present (sizes uniform here so the resize is informational) |

## CHECK_VISUAL_SANITY

Levels 1 and 2 PASS. Level 3 FAILS due to layout issues:

### L1 — PASS
The rendered initial frame shows: a red filled-square emitter (centre-left of playfield) and a red hollow-frame resonator (centre-right). Dark-grey background, black letter-box, yellow step-counter HUD bar at the bottom. Sprite count, placement, and HUD presence match the spec's L1 description. No catastrophic rendering bug.

### L2 — PASS
The rendered initial frame shows: two filled-square emitters (red top-left and blue bottom-left areas of the playfield) and two hollow-frame resonators (red top-right and blue bottom-right). HUD bar at bottom. Sprite count (4 game elements + HUD) and quadrant-level placement match spec. Colour-keying readable from outline colours. No catastrophic rendering bug.

### L3 — FAIL: sprite overlap, off-grid placement, and pip-overlap

#### Failure 1 — emitter_blue extends off-grid
- observed: `emitter_blue.set_position(2, 9)` places a 5×5 sprite anchored at (2, 9), so its bounding box is `(2..6, 9..13)`. The 12×12 grid's valid row range is `0..11`, so rows 12 and 13 are OOB. The engine clips silently, but the visible blue emitter is truncated to a 5×3 fragment at the bottom-left of the playfield.
- threshold: every primary game sprite must render fully within `level.grid_size`.
- diagnosis: 5×5 sprites placed at row 9 cannot fit in a 12×12 grid (need anchor row ≤ 7).
- fix-direction: redesign L3 layout so all 5×5 sprites have anchors in `[0, 7]² ` (or use a larger grid_size for L3).

#### Failure 2 — emitter_green extends off-grid
- observed: `emitter_green.set_position(8, 5)` → bbox `(8..12, 5..9)`. Cols 12 is OOB.
- threshold: same as Failure 1.
- diagnosis: 5×5 emitter at column 8 needs grid width ≥ 13.
- fix-direction: same as Failure 1.

#### Failure 3 — green-resonator extends off-grid
- observed: `resonator_green.set_position(5, 9)` → bbox `(5..9, 9..13)`. Rows 12-13 are OOB.
- threshold: same.
- diagnosis: 5×5 resonator at row 9 cannot fit in 12 rows.
- fix-direction: same.

#### Failure 4 — phase-delay tile overlaps emitter_red
- observed: `phase_delay_tile.set_position(1, 1)` (3×3) bbox `(1..3, 1..3)` and `emitter_red.set_position(2, 2)` (5×5) bbox `(2..6, 2..6)`. Overlap at cells `(2..3, 2..3)` (4 cells). The phase-delay tile's body and the emitter_red's body conflict at these cells.
- threshold: gameplay-relevant primary sprites should not visually overlap.
- diagnosis: tile at (1, 1) is too close to emitter_red at (2, 2) — they share a quadrant.
- fix-direction: move the phase-delay tile to a position not overlapping any emitter or resonator. Preserve the tile's mechanical role (delay red ring at small radius, not blue ring at multi-resonator decision tick).

#### Failure 5 — emitter_green overlaps multi-resonator
- observed: emitter_green bbox `(8..12, 5..9)` and multi-resonator bbox `(5..9, 5..9)`. Overlap at `(8..9, 5..9)` (10 cells).
- threshold: same as Failure 4.
- diagnosis: emitter_green's column anchor 8 and the multi-resonator's column extent 5..9 collide.
- fix-direction: same.

#### Failure 6 — emitter_blue overlaps green-resonator
- observed: emitter_blue bbox `(2..6, 9..13)` (clipped at 11) and green-resonator bbox `(5..9, 9..13)` (clipped at 11). Overlap at `(5..6, 9..11)` (6 cells in-bounds).
- threshold: same.
- diagnosis: row 9 placement causes both sprites to stack column-wise.
- fix-direction: same.

#### Failure 7 — pips overlap multi-resonator's top edge
- observed: `pip_red.set_position(6, 4)` bbox `(6..7, 4..5)`. Multi-resonator's top edge at row 5. Overlap at `(6..7, 5)` — pips paint red over the multi-resonator's grey outline at those cells.
- threshold: pips should sit ABOVE the multi-resonator, not on its outline.
- diagnosis: anchor row 4 + 2-cell sprite extends to row 5 = multi-resonator's top edge.
- fix-direction: place pips at row ≤ 3 so the 2×2 sprite ends at row 4, fully above the multi-resonator's top edge at row 5.

## Custom checks

Authored 4 custom checks per `code/smoke-test-checks.md` § Custom checks. All 4 PASS.

| Check | Observed | Notes |
|---|---|---|
| check_action_counter_increments | before=0, after=1 (both ACTION5 and ACTION6) | engine advances `_action_count` per action |
| check_arm_emitter_toggle | armed=True after first click; armed=False after second click on same emitter | M1: arm-state toggles per click |
| check_phase_delay_tile_toggle | active=True after first click; active=False after second click | M3: tile-state toggles |
| check_l1_minimal_solve | level advanced after `[arm emitter_red, fire]` 2-action witness | M1 end-to-end: L1 wins via the spec's 2-action witness |

(Pre-fire animation completion lets the engine fire `next_level()` after the multi-tick fire animation.)

## Visit count
1 / 6.

## Next state
`fix_implementation` — redesign L3 layout to (a) avoid sprite overlaps, (b) keep all sprites in-bounds, (c) ensure pips sit above multi-resonator's top edge. Mechanic-relevant Manhattan distances must preserve "red and blue arrive at multi-resonator on the same tick when phase-delay tile is active, different ticks when inactive".
