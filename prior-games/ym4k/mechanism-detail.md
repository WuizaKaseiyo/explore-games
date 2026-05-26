# ym4k — pivot-bridge-alignment

## Summary
This game is a 3-level traversal puzzle about rotating bridge arms from fixed pivot hubs. The avatar walks only on stone pads and on whichever bridge cells are currently extended into the gap. `ACTION5` rotates the arm under the current pivot one quarter turn clockwise, reconfiguring the reachable path. The first level teaches a single rotation, the second chains two pivots with a vertical climb between them, and the third builds a three-stage route that reaches a high goal shelf.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | step up one cell | target cell is on static stone or an extended bridge arm |
| ACTION2 | step down one cell | target cell is on static stone or an extended bridge arm |
| ACTION3 | step left one cell | target cell is on static stone or an extended bridge arm |
| ACTION4 | step right one cell | target cell is on static stone or an extended bridge arm |
| ACTION5 | rotate the current pivot arm clockwise | avatar stands on a pivot hub |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | One pivot turns a dead-end arm into a horizontal bridge | Rotate once, then cross the newly aligned span. Witness `[4, 4, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4]` |
| 2 | Two pivots must be used in sequence | Open the lower bridge, climb the center tower, then rotate the upper arm toward the goal shelf. Witness `[4, 4, 5, 4, 4, 4, 4, 1, 1, 1, 1, 5, 4, 4, 4, 4, 4]` |
| 3 | A third pivot extends the route to a higher shelf | Chain the red, blue, and green pivots in order to build the full ascent. Witness `[4, 4, 5, 4, 4, 4, 4, 1, 1, 1, 1, 5, 1, 1, 1, 1, 5, 4, 4, 4, 4, 4]` |

## Win condition
The avatar reaches the goal pad for the current level; the final level calls `win()`.

## Lose condition
The step counter reaches the level budget before the route is completed.

## Internal state

- avatar cell
- current step count
- current step budget
- each arm's pivot cell
- each arm's length
- each arm's orientation

## Notable code patterns

- Each arm is rendered as a set of one-cell bridge segments that are repositioned when the pivot rotates.
- The puzzle state is almost entirely topological: walkable cells are the union of static stone and currently occupied bridge cells.
- Pivot hubs use distinct colors so each stage of the route has a visible control point.
