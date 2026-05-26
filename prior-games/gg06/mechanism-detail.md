# Cluster-Rotate-Pivot: Mechanism Detail

## Core Mechanics

### 1. The Pivot-Rotation Grid
The game board is a 6x6 grid of logical tiles. Between each 2x2 cluster of tiles sits a **Pivot Point**. There are 5x5 = 25 possible pivot points.
- Clicking a pivot point rotates the 4 surrounding tiles 90 degrees clockwise (CW).
- Pivots one step outside all four visible board edges are valid. They rotate
  through an off-board buffer, so tiles can leave and later re-enter from the
  top, bottom, left, or right edge.
- A single rotation is a cyclic permutation of the four tiles:
  - Top-Left (TL) moves to Top-Right (TR)
  - TR moves to Bottom-Right (BR)
  - BR moves to Bottom-Left (BL)
  - BL moves to TL

### 2. Physical Rendering
- Each logical tile is rendered as a 3x3 pixel block.
- The 6x6 logical grid is surrounded by a visible one-tile buffer. Tiles that
  rotate off the left, top, right, or bottom edge remain visible in this buffer
  and can later rotate back into the board.
- Pivot points are rendered as 1x1 pixel dots at the intersections of the tiles.

### 3. Constraints
#### Locked Tiles (M3)
Certain tiles are marked as "Locked" (rendered as black immovable tiles). 
- Any pivot point that touches a locked tile is effectively disabled.
- Clicking a pivot that touches a locked tile results in a no-op (no rotation, no step cost).

#### Disabled Pivots (M4)
Certain pivot points are explicitly disabled (rendered as dark grey dots).
- These pivots cannot be used to rotate tiles even if all surrounding tiles are free.
- Clicking a disabled pivot results in a no-op.

### 4. Objective
The player must match the live board configuration to the **Target Preview** (displayed to the right of the board).
- The level is won when all tiles match the target configuration.

## Level Design Principles

- **Level 1 (Mechanic Introduction)**: Uses a 4x4 subset of the board with a checkerboard pattern. Introduces the basic rotation mechanic.
- **Level 2 (Constraint Introduction)**: Adds a locked central tile. This forces the player to route tiles around the obstacle rather than moving them directly through the center.
- **Level 3 (Complex Orchestration)**: Uses the full 6x6 grid with multiple locked tiles and disabled pivots. This creates bottlenecks and requires careful planning of tile transport across the board.

## Victory Condition
- Target state is reached.
- Step budget (shown in HUD) must not be exceeded.
