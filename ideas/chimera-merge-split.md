# Chimera-Merge-Split

## Summary

The player controls multiple **single-cell coloured pawns** on the
grid. Arrows move the **active pawn** one cell. Whenever two
pawns of *different colours* end up in the same cell, they
**merge** into a single 2-cell **chimera** sprite that occupies
both their colours simultaneously (visualised as a 1×2 cell with
each half showing one colour). The chimera moves as one unit:
arrows move both halves together; if either half is blocked by a
wall, neither moves. ACTION5 splits the active chimera back into
its two component pawns at their last-merged positions (the
chimera disappears, the two pawns reappear adjacent).

Each level has **target rings**, one per pawn colour. The level
wins when every pawn is on its same-colour target ring AT THE
END of the most recent action. The only failure mode is
exhausting the per-level step counter.

## Visual elements

- 12×12 grid; pale-grey floor.
- Each **pawn** is a single saturated-colour cell (orange, blue,
  purple).
- A **chimera** is a 1×2 sprite — the merge axis (horizontal vs
  vertical) records which axis the merge occurred on. Each half
  of the chimera shows its component colour. The chimera carries
  a small dark-grey "join" pixel between the two halves.
- A small **active-marker** (white 1-pixel border) hugs the
  currently active pawn or chimera.
- **Target rings** are 1×1 hollow rings in saturated colour — one
  ring per pawn colour.
- **Walls** are solid black 1×1 cells.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION1 | Move active pawn or chimera up 1 cell. Movement is rejected if any occupied cell would land on a wall. | always |
| ACTION2 | Move active down 1 cell. | always |
| ACTION3 | Move active left 1 cell. | always |
| ACTION4 | Move active right 1 cell. | always |
| ACTION5 | If the active sprite is a chimera, SPLIT it into its component pawns: pawn A appears at the chimera's "first" cell, pawn B at the chimera's "second" cell. Both pawns retain individual identities. The previously-active sprite becomes one of the pawns. | only when active is a chimera |
| ACTION6 | Click on a pawn or chimera to make it the active sprite. Click on empty cell or wall is a no-op (no step consumed). | always |

`available_actions = [1, 2, 3, 4, 5, 6]`.

## Mechanics enumeration

- **M1 — pawn-walk:** ACTION1-4 moves the active pawn 1 cell.
  Walls block; out-of-bounds is a no-op (still consumes step).
- **M2 — auto-merge:** if the active pawn's step would land on
  another (different-colour) pawn, the two pawns instead form a
  1×2 chimera spanning the mover's PRE-step cell and the
  stationary pawn's cell. The mover does NOT enter the
  stationary pawn's cell; both pawns remain on their original
  cells, but they are now bound as a single chimera sprite. The
  merge axis is the direction the mover attempted to move:
  east-step → horizontal chimera with the mover on the LEFT
  cell and the stationary pawn on the RIGHT cell; west-step →
  horizontal with mover RIGHT, other LEFT; etc. The active
  sprite becomes the chimera.
- **M3 — chimera-walk:** the chimera moves both cells together;
  if either cell would land on a wall (or off-grid), the move
  is rejected and the chimera stays put.
- **M4 — split:** ACTION5 separates a chimera back into its two
  component pawns. The split is done in-place; pawn A occupies
  the first cell, pawn B the second.
- **M5 — colour-target match:** the win predicate requires each
  pawn (after possible split) to be on a same-colour target ring.
- **M6 — chimera-only-corridor (level 2+):** specific 1-cell-tall
  passages have a height of 2 cells (i.e. 2 cells stacked
  vertically) and are gated so that ONLY a chimera (which fills
  exactly 2 cells) can pass through. A single pawn entering one
  of these cells is rejected (treated like a wall). Visualised
  as a 2-cell vertical slot with bracket markers.
- **M7 — single-pawn-only-gate (level 3+):** specific gates have
  a height of 1 cell and are gated so that ONLY a single pawn
  can pass; a chimera entering one of these cells is rejected.
  Visualised with a single bracket marker.

## Per-level progression

### Level 1 — base system (M1 + M2 + M3 + M4 + M5)
- 8×8 region. Two pawns, two targets. Narrow pathways.
- **Witness:** 15 actions. Player must merge the pawns into a chimera to move them together through a space that is more easily navigated as a single unit, then split them at the target.
- **Mechanics required:** M1 (walk), M2 (auto-merge), M3 (chimera walk), M4 (split), M5 (match).

### Level 2 — + M6 (chimera-only corridor)
- 10×10 region. Three pawns. Chimera-only corridors act as filters.
- **Witness:** 35 actions. The corridors force specific merges. The player must merge pawns A and B to cross a corridor, split them, then merge B and C to cross another corridor. This requires deep sequencing of merges and splits.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

### Level 3 — + M7 (single-pawn-only gate) + composition
- 12×12 region. Four pawns, four targets. Complex maze with chimera-only and single-pawn-only gates.
- **Witness:** 60+ actions. The player must navigate a highly constrained topology where pawns must repeatedly merge to cross wide gaps and split to squeeze through narrow gates. Commuting two adjacent merges/splits in the witness changes which pawn is at which side of a gate, making the order strictly deterministic.
- **Mechanics required:** M1, M2, M3, M4, M5, M6, M7.

## Win condition
After every action, walk every pawn (split chimera into its two component pawns for the check, but DO NOT actually split). For every pawn, check that its current cell equals the matching target's cell. If all match, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`.

## Internal state
- `self.pawns: list[Pawn]` — each pawn has `pos`, `colour`, `merged_with: Pawn | None`.
- `self.chimeras: list[Chimera]` — each chimera has `pawn_a`, `pawn_b`, `axis: 'h' | 'v'`, `pos_a`, `pos_b`.
- `self.active: Pawn | Chimera` — currently active sprite.
- `self.targets: dict[int, (int, int)]` — colour → target cell.
- `self.walls: set[(int, int)]`.
- `self.chimera_corridors: set[(int, int)]` — cells where only chimera can be.
- `self.single_pawn_gates: set[(int, int)]` — cells where only single pawn can be.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `kf42 — tether-pawn-cycle`**: chimera-merge-split has no tether — pawns are FREE until they collide and FUSE into one movable unit, then split on demand.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
Random presses of arrows + ACTION5 + ACTION6 produce arbitrary merge/split states; the chance of every pawn ending on its matching target ring is exponentially small in the number of pawns. Size-gated corridors (M6, M7) make most random trajectories rejected outright.

## Planning depth
- **L1:** moderate — recognise when to merge to save steps.
- **L2:** deep — corridor forces a specific merge order before the corridor and a specific split after.
- **L3:** very deep — player must solve a complex topological puzzle by dynamically changing the size and composition of their avatars.
