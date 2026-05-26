# vz8r — viscosity-zones

## Summary

This is a viscosity puzzle on a longer winding gel channel. The player clicks
the cyan pad to make the gel thin, the grey pad to make it thick,
and the left/right paddles to push the pieces along the channel.

- in **thin** gel, loose beads slide until blocked
- in **thick** gel, loose beads move exactly one cell

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK cyan to set thin gel, grey to set thick gel, or the left/right paddles to push the lane. | only visible controls react |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base viscosity rule | Start in thin gel; the player must thicken it to make a precise one-step move onto the first bend. Witness: `GL`. |
| 2 | + longer winding path | The red bead now has to traverse a much longer channel, with the stopper changing where the thin slide can end. Witness: `TRRRR`. |
| 3 | + second bead on the winding path | A blue bead shares the expanded channel, so the player first sweeps the loose pair right, then thickens the gel to place red precisely before the final return push. Witness: `RLGR`. |

## Win condition

All beads are inside their matching sockets.

## Lose condition

The step budget runs out before all sockets are filled.
