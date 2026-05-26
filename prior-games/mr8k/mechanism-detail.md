# mr8k — magnetic-polarity-pulse

## Summary

This is a magnetic pulse puzzle. The board has one fixed central magnet. The player clicks the red or blue pole buttons to set the field polarity, then clicks the green pulse button. Every loose bead moves exactly one cell along its arm of the cross:

- same polarity as the field: repel one cell away from the magnet
- opposite polarity to the field: attract one cell toward the magnet

Matching target rings capture beads and keep them locked in place.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK the red pole button to set the field to `N`, the blue pole button to set the field to `S`, or the green button to pulse the field once. | only visible buttons react |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base repel rule | One red `N` bead and one red target. The player learns that choosing the matching pole repels the bead outward. Witness pulse sequence: `N`. |
| 2 | + opposite-polarity coordination | A red `N` bead and a blue `S` bead sit on opposite horizontal arms, and the player learns that one `N` pulse can repel one bead while attracting the other. Witness pulse sequence: `NN`. |
| 3 | + same-arm interference | Two blue `S` beads and one red `N` bead share the cross, and the left-arm pair block each other until the vertical bead is staged correctly. Witness pulse sequence: `NNSS`. |

## Win condition

All beads must end inside matching-colour target rings.

## Lose condition

The level's pulse budget runs out before all beads are captured.

## Internal state

- `pole` — current global field polarity, `N` or `S`
- `pieces` — bead cells, bead polarity, and whether each one is already locked
- `targets_by_cell` — which target polarity sits at each capture ring
- `pulses_used`, `pulse_budget` — remaining field pulses

## Notable code patterns

- The board is a fixed cross, so every move reads as “toward” or “away” from the central magnet.
- Movement resolves in distance order, which makes same-lane blocking deterministic.
- Buttons do not spend budget; only actual field pulses do.
