# wr2h — carrier-strip-array

## Summary
This game is a clean carrier-strip puzzle about colored movable platforms whose control pads are built into the strips themselves. The avatar walks on gray islands and on whichever strip cells are currently aligned; using `ACTION5` while standing on a strip control shifts that entire strip to its next rail position and carries the avatar along with it. Level 1 teaches a single bridge strip, level 2 composes a bridge strip with a lift strip, and level 3 chains bridge, lift, and shuttle.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | step up one cell | target cell is walkable |
| ACTION2 | step down one cell | target cell is walkable |
| ACTION3 | step left one cell | target cell is walkable |
| ACTION4 | step right one cell | target cell is walkable |
| ACTION5 | shift the strip under the current control pad | avatar stands on a strip control cell |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | One carrier bridge strip | Shift the red strip to the right and walk across it. Witness `[4, 4, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4]` |
| 2 | Bridge plus lift | Shift the red strip to the dock, step onto the blue strip control, then ride the blue strip upward to the top shelf. Witness `[4, 4, 5, 4, 4, 4, 4, 4, 4, 1, 5, 1, 1, 4, 4, 4]` |
| 3 | Bridge, lift, then shuttle | Shift red to the dock, ride blue to the side perch, step onto the green shuttle control, then ride green into the goal bay. Witness `[4, 4, 5, 4, 4, 4, 4, 4, 4, 1, 5, 3, 5, 4]` |

## Win condition
Reach the goal cell on the current level.

## Lose condition
The step counter reaches the level budget.

## Internal state

- avatar cell
- each strip's current rail index
- each strip's active base position
- whether the avatar is currently riding a strip during a shift
- current step count
- current step budget

## Notable code patterns

- Each strip keeps a marked control segment inside the strip, so control and transport are the same object.
- When a strip shifts, the avatar is translated by the same delta if they are standing on that strip.
- A full-width bottom energy bar matches the stronger 64x64 layout used by the better prior games.
