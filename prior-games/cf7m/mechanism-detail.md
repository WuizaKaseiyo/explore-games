# cf7m — crystallization-front

## Summary

This is a staged crystal-growth puzzle. The player walks a lab tech with
the arrow keys, pushes grey impurity blocks to reshape the chamber, clicks
one of the visible seed nodes to choose which crystal colony is active,
and presses ACTION5 to send one crystallization pulse through the open
solution.

Each pulse grows the selected colony by exactly one orthogonal layer. The
growth is permanent and blocks movement. The lab tech's occupied cell also
blocks crystal spread, so standing in the wrong place can choke the front
and standing in the right place can steer it.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1-4 | Walk the lab tech; moving into a grey impurity pushes it if the next cell is clear. The avatar's occupied cell also temporarily masks crystal growth. | Always offered. |
| ACTION5 | Emit one crystallization pulse from the currently selected seed colour. | Always offered; no effect until a seed has been clicked. |
| ACTION6 | CLICK a visible amber or cyan seed to choose the active crystal front. | Only seed cells react. |
| ACTION7 | Undo the previous non-undo action. | Always offered. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Avatar-as-mask | The tech begins by blocking the only amber lane, so the player must step aside before pulsing the crystal upward. Witness: `D, click amber, PULSE ×5`. |
| 2 | + two-colony sequencing | The same masking rule now applies to two colours, so the player must clear the junction, finish amber, then switch to cyan. Witness: `D, click amber, PULSE ×5, click cyan, PULSE ×5`. |
| 3 | + real push + shared choke geometry | A true block push is required before either colony can use the upper route, and the two colours now compete for the same central approach. Amber must seed its left branch first, cyan then claims the shared channel, and amber finishes last along the side route. Witness: `R, L, click amber, PULSE, click cyan, PULSE ×6, click amber, PULSE ×5`. |

## Win condition

Every target ring is occupied by crystal of its own colour.

## Lose condition

The top horizontal life bar runs out before the targets are filled. It is
implemented as the per-level action budget.
