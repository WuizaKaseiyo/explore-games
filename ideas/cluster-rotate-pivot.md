# Cluster-Rotate-Pivot

## Summary

The grid is a 6×6 mosaic of single-cell **coloured tiles**. Between
every 2×2 block of adjacent tiles is an **interior pivot point** —
the corner shared by 4 tiles. Clicking a pivot rotates the 4
surrounding tiles 90° clockwise around that pivot (a discrete
permutation of the 4 cells). The player has only this rotate-cluster
verb. Each level shows a static **target arrangement** of tile
colours; the level wins when the live tile arrangement equals the
target. The only failure mode is exhausting the per-level step
counter.

## Visual elements

- 6×6 inner grid; tiles are 1×1 cells in saturated palette
  colours (typically 4-5 distinct colours per level).
- The 5×5 grid of **interior pivots** is shown as 1-pixel
  light-grey dots at the corners between tiles. Clicks register
  on the nearest pivot.
- A small **target frame** in the top-right of the grid shows the
  required arrangement at a 1:1 scale.
- A static-coloured tile that is already in its correct target
  position renders with a 1-pixel **green outline** (visual
  confirmation, not strictly necessary for solving).

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION6 | Click pixel `(x, y)`. The engine finds the nearest interior pivot and rotates the 4 surrounding tiles 90° CW around it: `(p, q) → (q, -p)` mapped to the 4 corner cells. Clicks far from any pivot are no-ops. | always; far-from-pivot clicks consume no step. |

`available_actions = [6]`. No avatar.

## Mechanics enumeration

- **M1 — pivot-rotate:** ACTION6 click rotates a 2×2 block of
  tiles 90° CW around the pivot. Specifically, the four tiles at
  positions `(c, r)`, `(c+1, r)`, `(c+1, r+1)`, `(c, r+1)` (where
  the pivot is at corner `(c+1, r+1)` in pixel coords) are
  permuted as: top-left → top-right → bottom-right → bottom-left
  → top-left.
- **M2 — match-target:** the win predicate compares the live
  6×6 tile colour grid to the level's target colour grid.
- **M3 — locked-tile (level 2+):** specific tiles are tagged
  `locked` and refuse to participate in any rotation. A pivot
  whose 4 surrounding tiles include any locked tile is a
  forbidden pivot — clicking it is a no-op (no step consumed).
  The locked tile renders with a 1-pixel **dark-purple border**.
- **M4 — fixed-pivot (level 3+):** specific pivots are tagged
  `disabled` (visually dimmed) and refuse to rotate even when
  all 4 surrounding tiles are unlocked. The player must route
  rotations around these.

## Per-level progression

### Level 1 — base system (M1 + M2)
- 6×6 active region. 12 tiles in 3 colours (red, green, blue), remainder blank (black). Initial state is scattered. Target arrangement groups them into 3 distinct 2x2 blocks.
- **Witness:** The player must use 6-8 specific pivot-clicks to transport tiles across the board. The 2x2 rotations must be sequenced to avoid breaking previously formed blocks.
- **Mechanics required:** M1, M2.

### Level 2 — + M3 (locked tile)
- Full 6×6 grid; 4 colours; 4 locked tiles forming a central wall. The target requires moving tiles from the left side of the locked wall to the right side, forcing the player to route them *around* the locked tiles (which disable adjacent pivots).
- **Witness:** 12-15 pivot clicks. The locked tiles severely restrict the available permutation paths, turning a simple transport task into a tight maze for tiles.
- **Mechanics required:** M1, M2, M3.

### Level 3 — + M4 (disabled pivot) + complex interference
- Full 6×6 grid; 5 colours. 3 locked tiles AND 4 disabled pivots placed in a checkerboard pattern. The puzzle requires swapping the positions of two complex 3-tile structures. 
- **Witness:** 25-30 pivot clicks. Because of the disabled pivots, direct transport is impossible. The player must use "holding areas" to temporarily park tiles while rotating other tiles past them. Commuting two adjacent rotations changes the outcome entirely.
- **Mechanics required:** M1, M2, M3, M4.

## Win condition
After every ACTION6 click that resolves to a valid rotation, compare every cell's colour to the target grid. If equal, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` triggers `self.lose()`. Clicks that resolve to forbidden pivots (locked tile in cluster, disabled pivot) consume no step.

## Internal state
- `self.tiles: np.ndarray[int]` — colour grid (6×6, int per cell).
- `self.locked: set[(int, int)]` — locked tile cells.
- `self.disabled_pivots: set[(int, int)]` — disabled pivot positions (corner coordinates).
- `self.target: np.ndarray[int]` — target colour grid.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `lp85 — row-col-shift-grid`**: lp85 shifts an entire row or column. Cluster-rotate is a *local* 2×2 rotation — fundamentally a different permutation group.
- **vs `pj7k — rolling-cube-face-paint`**: rolling cube permutes the cube's faces; cluster-rotate permutes the grid tiles.

## Step budget
- L1: 20.
- L2: 40.
- L3: 80.

## Random-resistance
The permutation group has immense state space. For L3, the requirement to swap specific structures through a bottleneck of disabled pivots makes random clicking computationally zero-probability to succeed.

## Planning depth
- **L1:** moderate — player learns how 2x2 rotations can transport a tile linearly by alternating pivots.
- **L2:** deep — locked tiles act as walls for the permutation group. Player must plan multi-step transport routes.
- **L3:** very deep — interference between tile payloads. Player must deliberately disassemble and reassemble structures to squeeze them past disabled pivots.
