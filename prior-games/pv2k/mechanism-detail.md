# pv2k — bellows-pressure-pulse

## Summary

This is a side-pressure puzzle. The player clicks one of four
visible bellows mounted around the chamber. A pulse from a bellows
pushes loose round beads in that direction until they hit a wall,
another object, or a matching socket. The yellow stopper block also
responds, but only moves one cell per pulse.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK a bellows on the left, right, top, or bottom side of the chamber to fire one pressure pulse from that side. | only the visible bellows react |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base pressure pulse | One red bead and one red socket. The player learns that clicking a side bellows pushes the bead across the chamber. Witness: `R`. |
| 2 | + movable stopper | The yellow stopper block now starts directly on the target, so the player has to shove it aside before the red bead can be parked. Witness: `RU`. |
| 3 | + two-bead interference | A blue bead with its own matching socket shares the chamber. The block still matters, but now both beads must be staged without knocking the other off-course. Witness: `RDLD`. |

## Win condition

Every bead is locked into its matching socket.

## Lose condition

The pulse budget runs out before all sockets are filled.

## Internal state

- `red_cell`, `blue_cell` — current bead positions
- `red_locked`, `blue_locked` — whether those beads are already captured
- `block_cell` — current stopper position
- `wall_cells` — border walls and any internal baffles
- `pulses_used`, `pulse_budget` — remaining pressure pulses

## Notable code patterns

- Beads slide for the full pulse, while the stopper moves at most one
  cell.
- Matching sockets lock beads in place, which creates the
  order-of-operations logic in later levels.
- The four clickable side bellows are the only controls; there is no
  separate run phase.
