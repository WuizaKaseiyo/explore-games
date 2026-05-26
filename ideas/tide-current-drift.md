# Tide-Current-Drift

## Summary

The grid hosts several **drift pawns** of various colours, plus
fixed **walls** and **target rings** (one per pawn colour). A
global **current direction** is one of `{N, E, S, W}`. Each turn,
when the player presses ACTION5, every non-anchored drift pawn
moves exactly **one cell in the current direction** if the
destination cell is in-bounds and not a wall; otherwise the pawn
stays put.

The player can: cycle the global current direction with the four
arrow keys (each arrow sets the direction explicitly: ACTION1=N,
ACTION2=S, ACTION3=W, ACTION4=E); ACTION5 advances the drift one
tick; ACTION6 click on a pawn toggles its **anchor** state
(anchored pawns ignore drift).

The level wins when every pawn is on its same-colour target ring
AT THE END of the most recent action. The only failure mode is
exhausting the per-level step counter.

## Visual elements

- 12×12 grid; pale-blue background.
- Each pawn is a single saturated-colour cell.
- Walls are solid black 1-cell sprites.
- Target rings are 1×1 hollow rings in matching pawn colour.
- A small **current-direction indicator** sits in the top rim — a
  3-pixel arrow rotated to the current direction.
- An **anchored pawn** displays a 1-pixel dark-grey pin in one
  corner.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION1 | Set global current direction to North. Does not move pawns. | always |
| ACTION2 | Set current direction to South. | always |
| ACTION3 | Set current direction to West. | always |
| ACTION4 | Set current direction to East. | always |
| ACTION5 | Advance drift by one tick: every non-anchored pawn moves 1 cell in the current direction if in-bounds and not into a wall, else stays. | always |
| ACTION6 | Click on a pawn to toggle its anchor state. Click on empty cell or wall is no-op (no step consumed). | always |

`available_actions = [1, 2, 3, 4, 5, 6]`.

## Mechanics enumeration

- **M1 — set-current:** ACTION1-4 sets the global current
  direction without moving any pawn (each ACTION1-4 still costs
  1 step).
- **M2 — drift-tick:** ACTION5 advances simulation: every
  non-anchored pawn moves 1 cell in the current direction subject
  to wall/bounds.
- **M3 — pawn-pawn-collision:** if two pawns would land on the
  same cell during a tick, the one earlier in a fixed iteration
  order moves; the second is blocked and stays. (Iteration order:
  pawns sorted by `(pos in current direction)` so the leading
  pawn moves first, then the trailing — preventing
  push-through.)
- **M4 — anchor-toggle:** ACTION6 click toggles a pawn's anchor.
  Anchored pawns ignore drift but still BLOCK other pawns'
  drift (act as walls for collision purposes).
- **M5 — colour-target match:** the win predicate requires every
  pawn to occupy its same-colour target ring.
- **M6 — sticky-target (level 2+):** target rings are *sticky*
  for matching-colour pawns: once a pawn lands on its
  matching-colour target, it auto-anchors (the anchor toggles
  on automatically, and the player cannot un-anchor it for the
  rest of the level). This means the player must finish each
  pawn's path before moving on.
- **M7 — vortex-cell (level 3+):** specific cells are tagged
  `vortex` and carry a fixed `chirality ∈ {+1, -1}`. When a
  non-anchored pawn lands on a vortex cell at the END of a
  drift step, the pawn slides ONE EXTRA cell perpendicular to
  the current direction within the same tick — clockwise-90°
  if `chirality = +1`, counter-clockwise-90° if `-1`. The
  perpendicular slide is itself subject to wall and bounds
  checks (rejected if blocked, leaving the pawn on the vortex
  cell). The rule is fully deterministic and tied to the
  vortex cell's chirality, not to any randomness.

## Per-level progression

### Level 1 — base system (M1 + M2 + M3 + M5)
- 8×8 active region. Two pawns, two targets. One pawn is anchored to block the other.
- **Witness:** 15 actions. The player must un-anchor the blocking pawn, drift both into position, and potentially re-anchor to hold one while positioning the other.
- **Mechanics required:** M1, M2, M3, M4, M5.

### Level 2 — + M6 (sticky target)
- 10×10 region. 3 pawns, walls forming corridors.
- **Witness:** 35 actions. Sticky-targets force the player to sequence the deliveries. If a pawn is delivered too early, it auto-anchors and acts as an immovable wall that blocks the paths of the other pawns.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

### Level 3 — + M7 (vortex cells)
- 12×12 region with 4 pawns, 4 targets, and vortex cells. Direct paths to targets are completely blocked by walls.
- **Witness:** 60+ actions. The vortex perpendicular shift is REQUIRED to deliver pawns to their target rings. The player must drift pawns onto vortices from specific directions to utilize the orthogonal "kick" to bypass walls. This requires extensive setup and multi-pawn orchestration.
- **Mechanics required:** M1, M2, M3, M4, M5, M6, M7.

## Win condition
After every action, walk every pawn. For each, check its cell matches its same-colour target. If all match, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`.

## Internal state
- `self.pawns: list[Pawn]` — each has `pos`, `colour`, `anchored: bool`.
- `self.current_dir: int` — 0..3 representing N/E/S/W.
- `self.walls: set[(int, int)]`.
- `self.targets: dict[int, (int, int)]` — colour → target cell.
- `self.vortex_cells: dict[(int, int), int]` — vortex cell to perpendicular direction sign (+1 = CW, -1 = CCW).
- `self.sticky_anchored: set[Pawn]` — pawns that auto-anchored on hitting a target (irreversible) (level 2+).
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `kx14 — tide-tilt-buoyant`**: Tide-current-drift uses a 4-way global current direction with discrete 1-cell-per-tick drift, not buoyancy.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
Random arrow + ACTION5 + ACTION6 presses produce arbitrary drift patterns; for L3 with multiple pawns and required vortex routing, the chance of every pawn ending on its colour-matching target is zero.

## Planning depth
- **L1:** moderate — coordinate anchoring to prevent unwanted drift.
- **L2:** deep — sticky targets act as permanent commits. Player must deliver pawns in the correct order.
- **L3:** very deep — vortex mechanics require indirect routing. The player must calculate the exact state of the board before drifting a pawn onto a vortex.
