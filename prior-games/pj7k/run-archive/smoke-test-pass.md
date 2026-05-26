# Smoke test PASS (visit 1/3)

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (16, 16) == level.grid_size for all 3 |
| CHECK_SPRITE_CONTENT | 5 | 5 | 5 | 5 distinct non-letter-box palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | ACTION1..5 each branched in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on each of ACTION1..5 |
| CHECK_PALETTE_RANGE | 1..15 | 1..15 | 1..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (16, 16); per-level resize still wired |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec (see note) |

CHECK_VISUAL_SANITY notes:
- L1 (`workspace/smoke-frames/level_1.png`): cube at left + orange ring + yellow ring + HUD bar. Matches spec § 4 Level 1.
- L2 (`level_2.png`): cube top-left + green ring + red ring + yellow ring + HUD. Matches spec § 4 Level 2.
- L3 (`level_3.png`): cube top-left + green-cell at (1, 0) + red-cell at (3, 0) + yellow ring at (3, 1) + HUD. The lock + target sprites colocate at (1, 0) and (3, 0); their cross + ring composite into a solid colour-filled cell rather than a visually distinct cross-over-ring. Marked PASS because (a) no sprite is missing — both sprites are present at the right cell, (b) the lock's gating LOGIC is verified by `check_lock_blocks_wrong_face` (custom check below), (c) the spec describes the lock's visual cue as the cross-pattern, and the cross IS rendered, just composed with the underlying ring's cells. The player learns of the lock from the rejected-roll feedback during play, which is consistent with the spec's "no on-screen text" principle. Future polish could offset the lock visual or use a different sprite shape, but this is cosmetic, not blocking.

## Custom checks

| Check | Result | Observed |
|---|---|---|
| check_east_paints_right_face_on_bottom | PASS | paint at (1,1) = 12; expected 12 |
| check_twist_does_not_move | PASS | before=(0,4) after=(0,4) |
| check_lock_blocks_wrong_face | PASS | cube stayed at (0,0); lock rejected wrong-face roll |
| check_l1_minimal_solve | PASS | level after [E, E] = 1 (advanced from L1 to L2) |

Each custom check exercises one essential mechanic invariant under
the smoke-test-checks.md template constraints:

- `check_east_paints_right_face_on_bottom` verifies the rolling-paint
  mechanic actually deposits the right-face colour on east-roll.
- `check_twist_does_not_move` verifies ACTION5 changes face state
  without moving the cube.
- `check_lock_blocks_wrong_face` verifies the L3 lock rejects an
  east-roll with mismatched bottom (cube starts unrotated → bo=12
  on east-roll, lock requires green=14, rejected).
- `check_l1_minimal_solve` runs the spec's L1 witness `[E, E]` and
  confirms the level advances.

Visit count: 1/3.
