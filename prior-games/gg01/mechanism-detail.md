# gg01 (Chain Segment Drag) Mechanism Detail

## Core Interaction
The player controls a "chain head" (active: orange, palette 12; inactive: brown, palette 13) which pulls a series of "body segments" (yellow, palette 11) behind it. The game is a spatial puzzle requiring the player to drag the chain to cover multiple, disjoint target zones (pink, palette 6) on the grid.

Unlike a classic "Snake" game where segments strictly follow the exact path of the head, this chain allows "bunching up" (overlapping segments). This is achieved by moving a segment to its predecessor's old position *only* if its Manhattan distance to the predecessor's new position exceeds 1. This overlapping mechanic creates the "slack" necessary for the chain to bend and route.

## Advanced Mechanics
- **Chain Split (ACTION6 on Body)**: Clicking on a yellow body segment splits the chain into two independent chains at that exact point. The clicked segment breaks off to become the Head of the new chain.
- **Switch Control (ACTION6 on Head)**: Clicking on any inactive Head (brown) switches your active control to that chain (turning it orange). Only the active chain can be moved.
- **Chain Reverse (ACTION5)**: Reverses the logical order of the *active* chain. The tail segment becomes the new head, allowing the player to drag that specific chain from the opposite end.

## Per-Level Progression
- **Level 1 (Introduction to Split)**: The grid has two disconnected 1x1 target holes. You start with a single chain of length 3. You must walk the chain into position, split it perfectly to drop one segment in the first hole, and walk the remaining chain to the second hole.
- **Level 2 (Reverse + Efficiency)**: Introduces a U-shaped pocket and separate targets. The player must efficiently manage a length-5 chain. Splitting and Reversing both play crucial roles in routing the chain segments efficiently to avoid running out of steps.
- **Level 3 (Composition)**: A complex central room with four distinct 1-cell corners as targets. The player starts with a master chain of length 4 and must perfectly shave off exactly 1-segment chains, parking them in each corner without exceeding the extremely tight step budget.

## Energy Budgets (Step Counters)
To enforce the puzzle constraints, the step counters are meticulously calculated to be exactly `optimal_path + 5`. Every action consumes a step. Players cannot use trial-and-error; they must calculate exactly when to split and reverse to traverse the grid efficiently.

## Internal State
- `self.chains`: A list of lists of segment indices. Each list represents an independent, contiguous chain.
- `self.active_chain_idx`: Integer pointing to the currently controllable chain in `self.chains`.
- `self.segments`: A master list of dictionaries, each holding references to three synchronized sprites (`head_active`, `head_inactive`, `body`). The `_sync_visuals` method toggles their `InteractionMode` based on their role in `self.chains`.
