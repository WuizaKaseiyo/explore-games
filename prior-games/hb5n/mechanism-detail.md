# hb5n — polyomino-walker-rotate

## Summary

The player controls an irregular-shaped walking avatar — a rigid
polyomino starting as a 3-cell L — that translates one cell per
arrow press and rotates 90° clockwise about its anchor cell with
ACTION5. The anchor cell is visually distinguished by an
orange-centred pattern (vs the maroon centres of body cells), so
the rotation pivot is legible from any static frame. Level 1's
target is a different L-silhouette (rotation 270), reached by
walking + rotating. Level 2 introduces growth pickups: **any
pickup orthogonally adjacent to an avatar cell after a move is
absorbed immediately, sticking as a new body cell at the
pickup's absolute position**. The player thus chooses *where*
the new cell merges by ending the avatar in the right position
relative to the pickup. Level 3 scales this up: five pickups are
scattered but the target is a 6-cell shape requiring exactly
three absorptions at three specific relative offsets; the player
must route the avatar to absorb the right three pickups at the
right merge positions while avoiding accidental adjacencies that
would lock in a wrong shape.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Translate the polyomino 1 cell UP. | Rejected if any post-move body cell would collide with a wall or fall off-grid. |
| ACTION2 | Translate 1 cell DOWN. | Same rejection rule. |
| ACTION3 | Translate 1 cell LEFT. | Same rejection rule. |
| ACTION4 | Translate 1 cell RIGHT. | Same rejection rule. |
| ACTION5 | Rotate 90° clockwise about the anchor cell. | Rejected if any post-rotation cell would collide with a wall or fall off-grid. |

Rejected actions still consume one step from the budget. After
every action (translate or rotate), the engine runs a pickup-
absorption pass: every pickup that is orthogonally adjacent to
some avatar cell — and whose own cell is not currently inside
the polyomino — is absorbed. The new body cell joins at the
pickup's absolute position. The pass cascades: if absorbing
pickup A places a new body cell that is now adjacent to pickup
B, B absorbs in the same step. Cascading continues until no
more absorptions fire.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 walk + M2 rotate-self (base dynamic system, N=2 mechanics) | 3-cell L avatar at (2,2) rotation 0; target L-silhouette at (12,12) rotation 270; walk to position then rotate 3× to match. **Witness [ACTION4]×10 + [ACTION2]×10 + [ACTION5]×3 (23 actions)**, step budget 50. |
| 2 | + M3 adjacency-absorb pickup (N+1 = 3 mechanics) | One pickup at (5,4); when any avatar cell becomes orthogonally adjacent to the pickup after a move, the pickup absorbs and the new cell sticks at its absolute position. Target = L-tetromino at rotation 90 cells {(12,12),(12,11),(11,11),(12,13)}, reachable only by ending the avatar at anchor (4,4) so the pickup absorbs at rel (1,0), then rotating to 90. **Witness [ACTION2]×2 + [ACTION4]×2 (absorb p at anchor (4,4)) + [ACTION4]×8 + [ACTION2]×8 + [ACTION5]×1 (21 actions)**, step budget 60. |
| 3 | + M4 surplus-pickup routing (4 mechanics) | Five pickups at (5,3), (5,5), (5,7), (8,4), (8,6); target = 6-cell irregular shape at rotation 90 with cells {(11,11),(11,12),(12,11),(12,12),(12,13),(13,12)}. The avatar must absorb EXACTLY three pickups at three specific relative offsets — rel (1,0), rel (0,-1), and rel (0,1). Routing matters: at anchor (5,6) both p2 and p3 are adjacent simultaneously and absorb in the same step at rel (0,-1) and (0,1); at anchor (4,3) p1 absorbs at rel (1,0). The two remaining decoys p4 and p5 must be left untouched. Consuming any fourth pickup pushes the avatar to 7 cells, making the 6-cell target unreachable. **Witness [ACTION2]×3 + [ACTION4]×2 (anchor (5,6) — p2 and p3 absorb simultaneously) + [ACTION3]×2 + [ACTION1]×3 + [ACTION4]×1 (anchor (4,3) — p1 absorbs) + [ACTION2]×9 + [ACTION4]×8 + [ACTION5]×1 (29 actions)**, step budget 100. |

## Win condition

`set(avatar_absolute_cells) == set(target_slot_cells)`. After
every action the engine computes the avatar's current absolute
cell footprint and compares to the per-level pre-cached set of
cells tagged `target` (the dim outline sprites in the level
layout). On set-equality, `self.next_level()` fires.

## Lose condition

Step budget exhaustion: `self.step_remaining <= 0 and not
self._check_win()`. Walking into walls and rotating into walls
are silently rejected (no effect) but still decrement the step
counter. The avatar can also become geometrically stuck —
absorbing a fourth pickup in L3 grows it past the target's cell
count, so the target becomes unreachable and the player must
wait out the step budget.

## Internal state

- `avatar_anchor: tuple[int, int]` — anchor cell's logical position.
- `avatar_rotation: int` — 0..3 (multiples of 90°).
- `avatar_relative_cells: list[tuple[int, int]]` — polyomino cells
  in canonical rotation-0 frame; index 0 is always the anchor
  (`(0, 0)`).
- `avatar_sprites: list[Sprite]` — parallel to `avatar_relative_cells`;
  the per-cell Sprite instances rendered each frame.
- `wall_cells: set[tuple[int, int]]` — per-level cache of wall
  cells, populated in `on_set_level` from `wall`-tagged sprites.
- `target_cells: set[tuple[int, int]]` — per-level cache of
  target-slot cells.
- `pickup_cells: set[tuple[int, int]]` — un-absorbed pickups.
- `step_budget, step_remaining: int` — per-level countdown.

## Notable code patterns

- **Per-cell-sprite avatar**: each cell of the polyomino is an
  independent 4×4-px sprite (anchor sprite with orange centre +
  body sprites with maroon centres). Walking / rotating moves
  the cells' absolute positions in lock-step; on absorption a
  new body sprite is spawned at the pickup's absolute position.
- **Adjacency-triggered absorption**: `_try_absorb_pickups`
  iterates over remaining pickups, checking Manhattan-1
  adjacency to any avatar cell. The new cell's rotation-0
  relative offset is computed by inverse-rotating the
  pickup-to-anchor display offset, so subsequent rotations of
  the polyomino carry the absorbed cell correctly. The loop
  restarts after each absorption so cascading adjacencies (a
  new body cell pulling in another adjacent pickup) all
  resolve in a single step.
- **Set-equality win predicate**: target cells are pre-cached in
  `on_set_level` from `target`-tagged sprite positions, then
  compared to the avatar's current cell set after every action.
  Trivial O(n) test (n = avatar cell count, up to 6 at L3).
- **Surplus-pickup planning gate**: L3 places 5 pickups when
  only 3 are needed. Absorption is geometrically irreversible —
  once a fourth body cell joins the polyomino, the 6-cell
  target set can never equal the 7-cell avatar set. This forces
  the player to plan the route so the avatar never grazes an
  unwanted pickup's neighbourhood.
- **Rotation as a pure function**: `_rotate_cw(rel, k)` applies
  the 90° CW formula `(x, y) → (-y, x)` k times.
  `_rotate_ccw(rel, k)` is its inverse, used to translate the
  pickup-to-anchor offset into the rotation-0 storage frame so
  the absorbed cell's relative position is independent of the
  avatar's current rotation when the absorption fires.
