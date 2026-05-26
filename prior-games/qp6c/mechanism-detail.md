# qp6c — gravity-slot-chamber

## Summary

This is a clear click-to-program physics puzzle. The player clicks the visible arrow slots along the bottom to choose a short gravity sequence, then clicks the green RUN button; the chamber resets to its start state and the sequence is executed from left to right. Under each programmed gravity pulse, the ball and any free blocks slide until they hit a wall or another object. Later levels add a movable block, then a green docking pocket that permanently catches the block and makes it part of the final arrangement.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK a bottom arrow slot to cycle its gravity direction clockwise (`U -> R -> D -> L -> U`), or click the green RUN button to execute the full programmed sequence from the chamber's reset state. | only visible slots and RUN react |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base gravity programming | One ball, no block. The player must choose the unique 2-step gravity program that drops the ball into the goal cup. Witness: `RU`. |
| 2 | + movable block as stopper | The ball and block both drop, then slide right together. The block hits the wall first, and the ball stops against it one cell earlier in the goal cup. Witness: `DR`. |
| 3 | + docking pocket | The block still moves under gravity, but now there is a green pocket that traps it permanently when it lands there. The winning 4-step program must first dock the block, then use the new fixed obstacle to route the ball into the goal. Witness: `LURD`. |

## Win condition

After RUN finishes, the ball must be sitting in the blue goal cup. On levels with dock pockets, every dock must also be occupied by a block.

## Lose condition

The per-level click budget runs out before the player produces a successful run.

## Internal state

- `program` — current gravity directions for the visible slots.
- `ball_cell` — current simulated ball position during or after the last run.
- `crates`, `docked` — block positions and whether each block has wedged into a dock.
- `wall_cells` — static chamber geometry, including the outer ring walls.
- `goal_cell`, `dock_cells` — success constraints.
- `trace_cells` — ball path from the most recent run.
- `steps_used`, `step_budget` — click budget.

## Notable code patterns

- RUN always resets the chamber to its start state before simulating, so the puzzle behaves like a tiny program rather than an incremental sandbox.
- The gravity solver uses directional sweep ordering (`rightmost first`, `topmost first`, etc.) to emulate simultaneous falling/sliding without overlapping objects.
- Slot arrows are just mutable sprites, so the programmed sequence is directly readable on the board at all times.
- The HUD overlays the last-run trace on top of the chamber, making failed programs easy to inspect and revise.
