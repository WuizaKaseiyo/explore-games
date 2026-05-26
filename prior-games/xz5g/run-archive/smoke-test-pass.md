# Smoke test PASS — xz5g

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == level.grid_size (64,64) all 3 levels |
| CHECK_SPRITE_CONTENT | 5 | 6 | 9 | distinct non-letter-box palette values per level (letter-box = 2; uniques L1 = {0,1,4,6,9}, L2 = {0,1,4,6,9,12}, L3 = {0,1,4,6,9,11,12,13,14}) |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | declared `[5, 6]`; both reference `GameAction.ACTION5` and `GameAction.ACTION6` in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | both actions execute without exception in a fresh game on L1 |
| CHECK_PALETTE_RANGE | 0..9 | 0..12 | 0..14 | all within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` and `self.win()` (engine-auto on terminal) referenced |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` referenced and wired through `_steps_left ≤ 0` check |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | uniform `grid_size=(64, 64)` across all 3 levels; no per-level resize needed; default 64×64 camera matches |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | each spec witness replayed against the loaded game and advanced past its level: L1 `[click(32,32), ACTION5]` → score 1; L2 `[click(32,32), 2×ACTION5]` → score 2; L3 `[click(4,4), click(32,32), 2×ACTION5]` → score 3, state WIN |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered initial frames at `workspace/smoke-frames/level_*.png` match spec — see per-level visual notes below |

### Visual sanity notes

- **L1**: blue avatar (filled with white pips) at lower-mid-left;
  hollow blue avatar_target ring at upper-mid-center; magenta-on-
  dark depleting bar along the bottom row; light off-white
  background. Sprite count = 2 game-elements + HUD bar. Matches
  spec § 4 L1 layout.
- **L2**: 4-fold-symmetric layout — blue avatar (left) /
  blue avatar_target (right) / orange companion (top) / orange
  companion_target (bottom). Filled-vs-hollow distinction reads
  cleanly; colour-pairing reads (this orange pawn → this orange
  ring; this blue pawn → this blue ring). HUD bar present.
  Matches spec § 4 L2 layout.
- **L3**: blue avatar (top-mid) / blue avatar_target (bottom-mid) /
  orange companion (mid-left) / orange companion_target
  (mid-right) / green anchor_pin under-overlapping the companion's
  right edge / maroon-square direction_indicator widget with
  yellow corner-pip at top-left corner. The companion-on-
  anchor_pin VISUAL OVERLAP is cosmetic (companion top-left (8,32)
  ≠ anchor_pin top-left (12,32), so the visit-checkpoint does NOT
  trigger from start; the visit fires only when avatar lands at
  exactly (12,32) on CCW1). HUD bar present. Matches spec § 4 L3
  layout.

No catastrophic rendering bugs: every level's grid fills the
64×64 frame (no kf42-style corner-patch); sprites are visibly
distinct; no sprite resembles a digit / letter / arrow glyph.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_click_sets_pivot` | pre=None post=(32, 32) | ACTION6 click on empty cell sets `_pivot` correctly; the halo gets rendered at the marked cell. |
| `check_action5_rotates_avatar` | pre=(12, 32); won_l1=True (score=1) | After click + ACTION5, the L1 win predicate fires (score advances from 0 to 1); the rotation is therefore correctly transforming avatar (12,32) → (32,12). |
| `check_l3_direction_toggle_via_widget` | pre=CW post=CCW | At L3, clicking the direction_indicator widget at (4, 4) toggles `_direction` from "CW" to "CCW". |

Visit count: 1/6.

## Implementation note caught at smoke

None — the implement-time bug (init field ordering clobbering
on_set_level's budget) was already caught and fixed during
`implement` step 5. No regression observed at smoke.
