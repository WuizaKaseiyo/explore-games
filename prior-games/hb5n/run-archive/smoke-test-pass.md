# Smoke test PASS (v3 — adjacency-absorb)

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | grid=(64,64) camera=(64,64) on every level |
| CHECK_SPRITE_CONTENT | 8 | 9 | 9 | distinct non-letter-box palettes |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 5 declared actions (1..5) have branches |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions for ACTION1..5 |
| CHECK_PALETTE_RANGE | 1..14 | 1..14 | 1..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size=(64, 64) |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 (23 actions) → L2 (21 actions, single absorb) → L3 (29 actions, three absorbs) → WIN, score 3 |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at `workspace/smoke-frames/level_*.png` |

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_east_moves_anchor | anchor (2,2) → (3,2) | ACTION4 translates anchor x by +1 |
| check_rotate_changes_silhouette | before=[(1,2),(1,3),(2,2)] after=[(1,1),(2,1),(2,2)] | ACTION5 changes the cell set |
| check_adjacency_absorbs_pickup | cells 3 → 4 | walking to a position where an avatar cell is adjacent to a pickup absorbs it |
| check_non_adjacent_pickup_not_absorbed | cells 3→3; pickups 1→1 | moves that leave every avatar cell ≥2 cells from the pickup do not absorb it |

Visit count: 2/6 (re-run after the L2/L3 absorption-rule redesign).

Mechanic recap (post-redesign):

- L2 introduces M3 — *adjacency absorption*. Any pickup that ends a
  move orthogonally adjacent to an avatar cell is absorbed
  immediately; the new cell sticks at the pickup's absolute position.
- L3 introduces M4 — *surplus-pickup routing*. Five pickups are
  placed, the target is a 6-cell shape requiring exactly three
  absorptions at three specific relative offsets. Routing the avatar
  to absorb only the right three (and at the right relative offsets)
  is the planning gate; absorbing a fourth pushes the avatar past
  the target's cell count and the level becomes unwinnable.
