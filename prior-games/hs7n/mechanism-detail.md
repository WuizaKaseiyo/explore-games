# hs7n — gravity-sorter-bay

## Summary

This is a gravity-programmed sorting puzzle. The player clicks the bottom arrow slots to choose a short gravity sequence, then clicks the green RUN button. The chamber resets, the programmed gravity pulses execute left-to-right, and every loose object slides until blocked. The orange ball must end in the orange ring target, and the yellow block must end in the yellow square target.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK a bottom arrow slot to cycle its gravity direction clockwise (`U -> R -> D -> L -> U`), or click the green RUN button to execute the programmed sequence from the chamber's reset state. | only visible slots and RUN react |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base gravity routing | One orange ball, no block. The player learns to drop the ball, then sweep it sideways into the target ring. Witness: `DR`. |
| 2 | + simultaneous sorting | The orange ball and yellow block move together under the same gravity program, but must finish on different matching targets. Witness: `URD`. |
| 3 | + crossed target planning | Both objects still move under the same pulses, but the wall layout now forces a longer program that places the block first and then routes the ball around it. Witness: `RDRU`. |

## Win condition

After RUN finishes, the orange ball must sit in the orange ring target. On levels with a block target, the yellow block must also sit in the yellow square target.

## Lose condition

The per-level click budget runs out before a successful run.

## Internal state

- `program` — current gravity directions for the visible slots.
- `ball_cell` — current ball position during or after the last run.
- `crates` — current block positions during or after the last run.
- `wall_cells` — static chamber geometry, including the outer ring walls.
- `ball_target`, `crate_target` — success cells.
- `steps_used`, `step_budget` — click budget.

## Notable code patterns

- RUN always resets the chamber first, so the puzzle behaves like a tiny program instead of an incremental sandbox.
- Gravity execution animates one cell of motion at a time, so long slides are legible.
- Object/target correspondence is conveyed by matching colour and shape: round orange object to round orange target, square yellow object to square yellow target.
