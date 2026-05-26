# qv7f — charge-accumulation

## Summary

This is an electric threshold puzzle on a bent rail. The spark starts empty,
the bright pad adds charge, the dark pad drains charge, and the side
blowers push the spark along the rail.

- a **low** lock needs 1 charge to pass
- a **high** lock needs 2 charge to pass
- passing a lock consumes exactly the charge that lock required

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK charge pad, drain pad, or a side blower. | only visible controls react |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base low-threshold lock | Charge once, then pass the low lock. Witness: `+R`. |
| 2 | + bent rail and recharge point | The rail now turns upward, and the spark must build to full charge for the first high lock, then recharge later for the low lock near the far socket. Witness: `++R+RRR`. |
| 3 | + second high-threshold gate | The path bends again and now includes a second high lock, so the spark has to recharge twice while traversing the longer route. Witness: `++R++R+RR`. |

## Win condition

The spark reaches the target socket.

## Lose condition

The step budget runs out before the socket is reached.
