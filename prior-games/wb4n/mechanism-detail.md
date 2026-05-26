# wb4n — waterline-buoyancy

## Summary

This is a buoyancy-and-current puzzle. The player clicks the top
spout to fill the tank, the bottom outlet to drain it, and the left
or right side jets to push the floating buoy along the visible water
surface.

The yellow stopper block only drifts sideways when it is submerged,
and the green floodgate opens only when the tank is completely full.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK the top spout to fill, the bottom outlet to drain, or a side jet to push the water current left/right. | only the visible controls react |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Waterline + current | The buoy rides the water surface, so the player must raise the tank and then push sideways. Witness: `FR`. |
| 2 | + submerged stopper drift | The stopper now needs to end in its socket, so the player first raises the water until the buoy reaches its row and then uses the current to move both objects for real. Witness: `FFR`. |
| 3 | + floodgate | A gate cell stays closed until the tank is completely full. The stopper still has to drift into place, but now the final side push only works at maximum fill. Witness: `FFFL`. |

## Win condition

The buoy ends in its buoy ring, and on levels with a stopper socket,
the stopper ends in its matching square dock.

## Lose condition

The step budget runs out before the required end state is reached.

## Internal state

- `water_level` — current tank height, 1 through 5
- `buoy_x` — buoy column; row is derived from the water surface
- `block_cell` — stopper position
- `gates` — cells that become passable only at full tank height
- `steps_used`, `step_budget` — remaining actions

## Notable code patterns

- The buoy's vertical position is derived from the waterline rather
  than stored independently.
- The visible water fill is updated cell-by-cell every action.
- Current affects the buoy strongly, but only nudges the stopper one
  cell if it is submerged.
