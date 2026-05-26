# nl6v — color-mixing-reservoir

## Summary

This is a chemistry mixing puzzle. The top-left tap adds yellow reagent,
the top-right tap adds cyan reagent, the center beaker shows the current
mixture, and the bottom spouts pour the current beaker contents into the
target vials.

- yellow + cyan = green
- pouring empties the beaker
- a vial only locks when the poured mixture matches its target color
- a wrong pour drains to waste and leaves the target unfilled

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK a reagent tap or a pour spout. | only visible controls react |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base mixing rule | Make green in the beaker, then pour it into the left vial. One valid witness is `YCL`. |
| 2 | + ordered two-vial filling | The two targets now want different mixtures, so the player must route one beaker load to the right and a later one to the left. One valid witness is `YCRYL`. |
| 3 | + third outlet under the beaker | Level 3 adds a middle vial, so the player has to produce yellow, green, and cyan in one program rather than just reusing a two-vial pattern. One valid witness is `YCDYLCR`. |

## Win condition

All target vials are filled with their matching mixture.

## Lose condition

The step budget runs out before all target vials are filled.
