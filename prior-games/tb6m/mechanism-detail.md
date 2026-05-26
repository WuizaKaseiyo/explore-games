# tb6m — phase-channel-relay

## Summary
This game is a compact phase-routing puzzle built around colored switches and matching channel cells. The avatar walks on gray floor cells and uses `ACTION5` while standing on a colored switch to flip that color between two complementary bridge patterns. Level 1 teaches a single red bridge, level 2 requires toggling red twice to change which red lane exists, and level 3 chains red, blue, red again, then green. The board stays visually strict: floor, colored switch, colored phase lane, and goal.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | step up one cell | target cell is walkable |
| ACTION2 | step down one cell | target cell is walkable |
| ACTION3 | step left one cell | target cell is walkable |
| ACTION4 | step right one cell | target cell is walkable |
| ACTION5 | flip the phase of the switch underfoot | avatar stands on a colored switch |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Single red bridge phase | Flip red on, then cross the bridge. Witness `[4, 4, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]` |
| 2 | Branch-order routing | Red now opens both the lower entry bridge and the upper-left branch, so the player must go left to the blue switch first, then return through the hub and flip red again on the right side to expose the final descent. Witness `[4, 4, 5, 4, 4, 4, 4, 4, 1, 1, 1, 3, 3, 3, 3, 5, 4, 4, 4, 4, 4, 4, 5, 2, 2, 4, 4]` |
| 3 | Five-switch hub composition | The final board is now a real hub: red opens the lower and upper-left branches, blue opens the long mid bridge, red flips again to expose the right shaft, green opens the top bridge, and blue must finally flip off to reveal the short goal link. Witness `[4, 4, 5, 4, 4, 4, 4, 4, 1, 1, 1, 3, 3, 3, 3, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 1, 1, 1, 5, 3, 3, 3, 3, 5, 3, 3]` |

## Win condition
Reach the goal cell on the current level.

## Lose condition
The step counter reaches the level budget.

## Internal state

- avatar cell
- per-color phase state
- current step count
- current step budget

## Notable code patterns

- Each phase cell is represented by an active sprite and an inactive sprite at the same coordinate, swapped by a boolean polarity test.
- Red is reused in levels 2 and 3 with opposite polarity cells, so one toggle changes which bridge exists rather than only opening more space.
- The bottom-row HUD is a full-width energy bar like the stronger 64x64 games.
