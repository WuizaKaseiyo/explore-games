# gg03 (Chimera-Merge-Split) Mechanism Detail

## Core Interaction
The player navigates single-cell colored pawns through a 12x12 logical maze
rendered on a 64x64 canvas with larger 5x5 cells. The objective is to park
every pawn on its matching colored target block. Arrow keys (`ACTION1`-`ACTION4`)
move the currently active entity. Clicking on another pawn or chimera
(`ACTION6`) switches active control to it. The refreshed rendering uses clean
solid floor cells, thick chasm tiles, active outlines, and visible target cross
marks instead of a distracting checkerboard.

## Advanced Mechanics
- **Auto-Merge (M2)**: If the active pawn attempts to walk into another pawn, the move is intercepted. Instead of pushing or blocking, the two pawns instantly fuse into a **Chimera**. The Chimera is a 2-cell long rigid body spanning the exact positions the pawns occupied. If the collision happened horizontally, it forms a 1x2 Horizontal Chimera. If vertically, it forms a 2x1 Vertical Chimera. The active entity becomes the newly formed Chimera.
- **Chimera Movement (M3)**: A Chimera moves as a single, multi-cell rigid body. If any part of its body is blocked by a wall, the entire movement is rejected.
- **Gap Traverse (M6)**: A key physical puzzle element. The map contains "Gap" (chasm) tiles. A single pawn attempting to step onto a Gap tile will be blocked (it would fall). However, a 2-cell Chimera can bridge a 1-cell wide Gap! As long as at least one half of the Chimera remains on solid ground, it can step over the chasm. This physical rigid-body logic elegantly forces the player to merge pawns to cross treacherous terrain.
- **Split (M4)**: At any time, pressing `ACTION5` will split the active Chimera back into its two constituent single pawns, leaving them exactly where they currently stand.
- **The 90-Degree Corner (M7)**: Because NovaEngine entities do not rotate, a rigid 2-cell Horizontal Chimera cannot navigate around a 1-cell wide 90-degree corner. It will physically get stuck because its "tail" sweeps into the wall. To turn a tight corner, the player MUST split the Chimera into single pawns, walk them around the bend individually, and potentially re-merge them later. 

## Per-Level Progression
- **Level 1**: Introduction to Merge. The player starts with two scattered pawns separated by a wall. They must navigate a simple maze to meet in the center, merge into a Chimera, cross a horizontal gap, and then split to park on targets in opposite corners.
- **Level 2**: Introduction to Split and 90-Degree Corners. The pawns must merge to cross a gap, but immediately encounter a tight 1-cell wide zig-zag labyrinth. The vertical chimera safely crosses the gap but gets stuck at the first corner of the zig-zag. The player must split and carefully maneuver the single pawns through the winding tunnel to their goals.
- **Level 3**: Advanced Ferry Mechanic. The player is presented with 3 pawns, two sequential horizontal gaps, and a trap corner. Two pawns must merge to cross the first gap, but are forced to split by a 1-cell wide bottleneck. One pawn must navigate the bottleneck to reach the third stranded pawn, merge with it, and cross the second gap to win. This requires significant forethought and spatial planning.

## Win Condition
After every action, the game checks if every target ring is covered by a pawn of the matching color. Chimeras "count" as their constituent pawns for this check. If all targets are covered, the level is won.
