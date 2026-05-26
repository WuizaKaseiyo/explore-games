# rt4c — size-selective-membrane

## Summary

This is a membrane-filter puzzle on a single channel. The cyan bead is
small, the orange block is large, and the membrane in the middle can be
set to a **narrow** pore or a **wide** pore before each flush.

- click the **top** button to set the membrane to a narrow pore
- click the **bottom** button to set the membrane to a wide pore
- click the **left** or **right** blower to flush the whole channel
- the **small** bead can pass through either pore
- the **large** block can only pass through the wide pore

Pieces slide until blocked by the channel wall, the membrane, or a
locked piece already sitting in its socket.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK top = narrow pore, bottom = wide pore, left/right = flush the channel. | only visible controls react |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base permeability rule | The small bead passes straight through the narrow pore. Witness: `R`. |
| 2 | + large-size exclusion | The large block cannot cross until the pore is widened first. Witness: `DR`. |
| 3 | + ordered composition | First widen and flush both pieces right, then narrow and flush left to pin the large block at its socket while sending the small bead back across, then flush right once more to dock the bead. Witness: `DRULR`. |

## Win condition

All pieces occupy their matching sockets.

## Lose condition

The step budget runs out before all sockets are filled.
