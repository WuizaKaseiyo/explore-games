# xs2m — neutralization-basin

## Summary

This is a movement-based neutralization puzzle. The droplet moves with the
directional controls, and `ACTION6` cycles its chemistry without spending
step budget. Matching crust barriers dissolve when the droplet moves through
them, and the reaction resets the droplet to neutral.

- an **acid** droplet dissolves the orange basic crust
- a **base** droplet dissolves the blue acidic crust
- dissolving any crust consumes the reaction and resets the droplet to **neutral**

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1-4 | Move the droplet up, down, left, or right. | only clear cells or dissolvable barriers can be entered |
| ACTION6 | Cycle chemistry `neutral -> acid -> base -> acid ...`. | always valid, and does not spend life |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base neutralization | Toggle once to acid, pass one basic crust, and walk to the socket. Witness: `6, 4, 4, 4`. |
| 2 | + opposite-crust sequence on a bent corridor | The first reaction still returns the droplet to neutral, but now the route bends upward before the second crust, so the player has to carry the reset through a turn and toggle twice to reach base again. Witness: `6, 4, 1, 1, 4, 6, 6, 4, 4`. |
| 3 | + winding corridor | The path bends more deeply, so the player must dissolve the first crust, follow the corridor, then toggle twice into base for the second reaction before climbing to the socket. Witness: `6, 4, 2, 2, 6, 6, 4, 4, 1, 1`. |

## Win condition

The droplet reaches the target socket.

## Lose condition

The step budget runs out before the socket is reached.
