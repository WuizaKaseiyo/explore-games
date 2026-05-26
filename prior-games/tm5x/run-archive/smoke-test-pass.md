# Smoke test PASS

All 10 universal checks and all 4 custom checks PASS. Visit count: 1/6.

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == level.grid_size (64,64) for every level |
| CHECK_SPRITE_CONTENT | 6 palettes | 7 palettes | 8 palettes | distinct non-letter-box values: L1 {0,1,5,7,8,14}, L2 {0,1,5,7,8,9,14}, L3 {0,1,3,5,7,8,9,14} |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions (1,2,3,4,5) referenced by name in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | each action raises no exception; action_count increments 0→1 for every action |
| CHECK_PALETTE_RANGE | 0..14 | 0..14 | 0..14 | all rendered pixels within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | replaying L1 witness (5 actions) → score 1; L2 witness (16 actions) → score 2; L3 witness (43 actions) → state=WIN. Total path length matches spec |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all 3 levels use grid_size (64, 64), so per-level resize is unnecessary; default camera matches |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered frames match spec; PNGs at workspace/smoke-frames/level_*.png. L1: pawn at centre + target_hot below + step-bar HUD. L2: pawn at centre + target_hot left, target_cold right + HUD. L3: pawn top-left + walls down middle column with top gap + target_hot bottom-left + target_cold bottom-right + HUD. |

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_down_moves_pawn | y0=32 y1=36 | ACTION2 moves pawn one thermal cell DOWN (4 px) |
| check_action5_toggles_polarity | before=1 after=-1 | ACTION5 flips polarity sign |
| check_action5_swaps_pawn_variant | pawn_cold.interaction=TANGIBLE | the cold variant becomes the tangible (rendered) sprite after toggle |
| check_imprint_at_pawn_cell | _temperature[8,8]=2 (expected +2) | the aura-imprint rule sets the pawn-cell to +2 when hot |

## Visual-sanity per-level diagnostics

- **L1 PASS** — sprite count 2 (pawn cluster + 1 target); pawn centre at thermal (8,8) with pink halo aura; target_hot below at (8,13); HUD black bar visible at top row. No catastrophic rendering. The pink "+ shape" around the red pawn cell is the +1 imprint at four cardinal neighbours (visible learning cue per checklist item 19/21 — the player can read the pawn's polarity AND its aura's reach off the screen).
- **L2 PASS** — sprite count 3 (pawn + 2 targets); pawn at centre; target_hot left, target_cold right (green frame with red vs blue centre — different required temperatures cued by centre colour); HUD at top.
- **L3 PASS** — sprite count ~15 (pawn + 2 targets + 12 walls); pawn at top-left; vertical wall-column down middle starts at row 4 leaving a top gap (rows 0..3); target_hot bottom-left, target_cold bottom-right. Walls render unambiguously as solid black-bordered grey blocks — visually distinct from the chamfered thermal tiles and the green-framed targets.

## Spec-driven rule fidelity

- The pawn aura visibly imprints the 4 cardinal-neighbour cells in
  pink (warm/+1) when pawn is hot. After ACTION5, the imprint cells
  flip to light-blue (cool/-1). The aura is visible WITHOUT taking
  any action — discoverable from L1's static frame. Checklist item
  21 satisfied (UI teaches role).
- Targets read as goals (green-framed rings), with the centre
  colour signalling required temperature (red = +2 hot, blue = -2
  cold). Identical-visuals-imply-correlated-roles: target_hot and
  target_cold share the green frame (= "this is a goal cell") and
  differ only by centre colour (= "this is the temperature it needs"),
  which is correctly the correlation the spec promises.
- Walls render as solid blocks distinct from any thermal pattern,
  signalling tangibility correctly.
- HUD step-counter bar fills the top row in palette 5 (black),
  draining left-to-right as actions are spent.

**Transition: finalize.**
