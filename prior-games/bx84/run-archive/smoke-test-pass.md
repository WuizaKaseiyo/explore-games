# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (16, 16) == level.grid_size for all 3 levels |
| CHECK_SPRITE_CONTENT | 3 | 4 | 5 | distinct non-letter-box palette values per level (well above ≥2) |
| CHECK_ACTION_BRANCHES | ✅ | — | — | declared `[6]`; `GameAction.ACTION6` referenced in `step()` |
| CHECK_ACTION_RUNTIME | ✅ | — | — | ACTION6 dispatches without exception |
| CHECK_PALETTE_RANGE | 3..11 | 3..11 | 3..12 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | All levels share grid_size (16, 16) — vacuously satisfies the per-level resize requirement; the source still resizes in `on_set_level` |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per-level notes

- **L1 (level_1.png)**: PASS. Grey emitter at top-left (cell ~(1, 8) on the 16×16 grid scaled to 64×64), yellow beam line traversing the upper-middle row east, and a yellow 3×3 hollow ring target at lower-middle (~cell (8, 11)). HUD bar at bottom. Spec match: "1 emitter + 1 target_yellow at (8, 11) + step counter HUD". ✓
- **L2 (level_2.png)**: PASS. Grey emitter top-left, top-row beam in two segments — short yellow segment immediately east of the emitter, then a long blue segment continuing east. The yellow→blue transition cell IS the filter (palette-9 blends with post-filter blue beam, but the player perceives the recolour boundary). Blue 3×3 hollow ring target at lower-right (~cell (10, 11)). HUD bar at bottom. Spec match: "1 emitter + 1 filter + 1 target_blue + step counter HUD". ✓
- **L3 (level_3.png)**: PASS. Six game-element clusters: grey emitter (mid-left), orange prism mid-row, yellow→blue transition (filter) further east, yellow east-branch beam to the prism plus blue east-branch beam continuing east-of-filter, yellow south-branch beam descending from the prism through the lower-left yellow ring (target_yellow_south), yellow ring at top-left (target_yellow_north, currently UN-visited because prism is in initial state ES so no north branch), and a blue 3×3 hollow ring at right-middle (target_blue, currently UN-visited because no mirror placed yet). HUD bar at bottom. Spec match: "1 emitter + 1 prism + 1 filter + 3 targets + step counter HUD". ✓

## Custom checks

| Check | Result | Observed | Notes |
|---|---|---|---|
| `check_l1_minimal_solve` | PASS | level after L1 solve = 1 | The spec's L1 1-click witness (click at grid (8, 8)) advances to L2. |
| `check_click_empty_places_mirror` | PASS | mirror_bs count before=0, after=1 | Clicking an empty cell adds a `mirror_bs` sprite at that cell. |
| `check_filter_recolours_beam` | PASS | pre_filter cell (2, 2) = palette-11; post_filter cell (4, 2) = palette-9 | The filter at (3, 2) recolours the beam from yellow (11) to blue (9). |
| `check_prism_toggle_changes_branch` | PASS | prism before=`prism_es`, after=`prism_en` | Clicking the prism cell at (4, 8) toggles the sprite from `prism_es` to `prism_en`. |

Visit count: 1/6.

## Custom checks — authoring rationale

The four mechanic invariants tested:
1. **`check_l1_minimal_solve`**: end-to-end witness sanity — if this fails, the L1 win-predicate or beam tracing is broken.
2. **`check_click_empty_places_mirror`**: M1 mechanic primitive — if clicks don't add mirrors, every level is unsolvable.
3. **`check_filter_recolours_beam`**: M2 mechanic primitive — if the filter doesn't change beam colour, target_blue can't ever be lit.
4. **`check_prism_toggle_changes_branch`**: M4 mechanic primitive — if clicking the prism doesn't toggle its sprite, target_yellow_north (which requires state EN) can never be lit and L3 is unsolvable in ≤ 80 clicks.

All four invariants are essential — failure of any one makes the corresponding level unsolvable.
