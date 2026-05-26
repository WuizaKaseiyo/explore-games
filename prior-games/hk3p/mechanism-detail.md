# hk3p — heat-phase-routing

## Summary

This is a phase-change routing puzzle. The player clicks the visible
red heater, blue cooler, and side blowers mounted around the chamber
to move one amber material blob into its amber socket.

- **heat** raises the material one phase: solid -> liquid -> gas
- **cool** lowers it one phase: gas -> liquid -> solid
- **liquid** falls to the bottom of its column
- **gas** rises to the top of its column
- the side blowers move each phase differently:
  - solid moves **exactly one cell**
  - liquid slides horizontally until blocked, then settles downward
  - gas slides horizontally until blocked, then settles upward

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK the heater, cooler, or side blowers. | only visible controls react |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base liquid slide rule | The solid starts grounded, so the first successful solve comes from heating into a liquid and using the horizontal slide to reach the far socket. Witness: `HR`. |
| 2 | + gas rise on the top lane | The material starts grounded again, and the wall placement makes the second heat necessary before the rightward top-lane move. Witness: `HHR`. |
| 3 | + cooling for precise placement | The grounded solid must rise, slide, then cool back to a solid so the final move becomes a one-cell nudge onto the floor socket. Witness: `HHRCL`. |

## Win condition

The material occupies the amber socket.

## Lose condition

The step budget runs out before the material reaches the socket.
