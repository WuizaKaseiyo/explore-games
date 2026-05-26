# st5b — surface-tension-bridge

## Summary

This is a liquid-bridge navigation puzzle. The player walks a small
avatar across land tiles with the arrow keys, clicks anchor posts to mark
exactly two endpoints, and presses ACTION5 to **set** that meniscus into
a permanent bridge. Undo rewinds the previous setup step for free.

The bridge rule is simple: if the two selected anchors lie on the same row
or column and the cells between them are all pit cells, ACTION5 turns that
entire gap into a solid walkable bridge and then clears the selection.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1-4 | Walk the avatar on land, anchors, goal cells, or currently active liquid bridges. | Always offered. |
| ACTION5 | Set the currently selected anchor pair into a permanent bridge. | Always offered; only works when exactly two anchors are selected and they span pure pit cells. |
| ACTION6 | CLICK an anchor post to add or remove it from the current two-anchor selection. A third click starts a fresh selection. | Only anchor cells react. |
| ACTION7 | Undo the previous non-undo action. | Always offered. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Single bridge commit | Select the only valid anchor pair, set it, and walk across. Witness: `R, R, click left anchor, click right anchor, SET, R, R, R`. |
| 2 | + two serial bridges | The player must commit an upper bridge and then a lower bridge before the path to the goal is complete. Witness: `R, R, click upper-left, click upper-right, SET, R, R, D, D, click lower-left, click lower-right, SET, R, R, R`. |
| 3 | + three-bridge chain | The path now requires three commits in a row: top horizontal, then lower vertical, then lower horizontal. Witness: `R, R, click top-left, click top-right, SET, R, R, D, D, D, click lower-top, click lower-bottom, SET, click lower-left, click lower-right, SET, L, L, D, D, L`. |

## Win condition

The avatar reaches the goal ring.

## Lose condition

The top horizontal life bar runs out before the avatar reaches the goal.
As in the rest of the batch, that bar is implemented as the level's
action budget.
