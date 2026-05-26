# Smoke test PASS — yh3p

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera 64×64 == grid_size 64×64 for all levels |
| CHECK_SPRITE_CONTENT | 6 | 7 | 8 | distinct non-letter-box palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 6 declared actions referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on any of ACTION1..6 |
| CHECK_PALETTE_RANGE | 2..13 | 2..13 | 2..13 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1: 12 actions → idx 1; L2: 29 actions → idx 2; L3: 40 actions → all buds bloomed |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (64, 64); no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

## Custom checks (4 authored, all pass)

| Check | Observed | Notes |
|---|---|---|
| check_extend_moves_tip | before=(12,28) after=(16,28) | ACTION4 from L1 root extends tip 1 cell right |
| check_wall_blocks_extend | expected tip at (28,32), got (28,32) | RIGHT-growth from L2 root halts at (28, 32) before the wall column |
| check_click_rebranch_resets_facing | facing after rebranch: None | ACTION6 click on root clears tip facing to None |
| check_bloom_requires_facing_match | buds before=3 after=3 | ACTION5 with WRONG facing on L3 bud P does NOT bloom |

## Visual sanity notes

- L1 (`smoke-frames/level_1.png`): grey background; root at left-center
  with white+grey-checkered tip_dormant overlay clearly visible; orange
  bud_closed at right-center; pink step bar across the top row.
  Matches spec § L1 "Layout: Root at cell (3, 7); bud_closed at cell
  (15, 7); empty corridor" — all four conspicuous elements present
  and correctly placed.

- L2 (`smoke-frames/level_2.png`): vertical crosshatched wall column
  at center splitting the playfield; bud_closed (orange ring + magenta
  core) in upper-left; another bud_closed mid-right; root with
  tip_dormant overlay in left-center; pink step bar top. Wall column
  has 15 wall sprites stacked vertically (cells (8, 0..14)) with the
  bottom-row gap at (8, 15) — visible as a single empty cell at the
  bottom of the column. Matches spec § L2.

- L3 (`smoke-frames/level_3.png`): L-shaped wall (vertical + horizontal
  segments) clearly visible; three notched buds in three quadrants
  with directional yellow stamens — top-right with stamen UP (rotation
  180), bottom-left with stamen RIGHT (rotation 270), bottom-right
  with stamen DOWN (rotation 0). Root in top-left quadrant with
  tip_dormant overlay clearly visible. Pink step bar top. Matches
  spec § L3 layout and bud-rotation table.

## Implementation tweak during smoke-test

Initial render of L1 showed the `tip_dormant` overlay using palette
`{2, 3}` blending into the palette-2 light-grey background, making
the tip nearly invisible. Per checklist item 19 (no hidden state),
the dormant tip's location must be visually readable. Applied a
1-line palette tweak to `tip_dormant`'s outer cells from palette 2
to palette 0 (white), creating a high-contrast white+grey checkered
appearance against the grey background. All universal and custom
checks remain PASS after the tweak.

Visit count: 1/6.
