# mg5d — magnetic-split-field

## Summary

This is a global magnetic field puzzle. The player clicks the bottom arrow slots to choose a short field program, then clicks the green `RUN` button. On each pulse:

- the red `N` bead slides in the field direction until blocked
- the blue `S` bead slides in the opposite direction until blocked

Matching target rings capture beads and keep them locked in place.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK an arrow slot to cycle that field pulse (`U -> R -> D -> L`), or click the green `RUN` button to execute the whole sequence from the reset state. | only visible slots and `RUN` react |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Opposite motion | One red bead and one blue bead must go to opposite sides under the same field pulse. Witness program: `R`. |
| 2 | Order matters | The same two beads now need three pulses, and the first `U` pulse parks the blue bead before the red one finishes. Witness program: `URD`. |
| 3 | + blocker walls | Two internal walls force a four-step sequence where the red bead must be staged around the wall while the blue bead backtracks into its socket. Witness program: `ULRD`. |

## Win condition

Both beads must end inside matching-colour target rings.

## Lose condition

The run budget is exhausted before a successful program is executed.

## Internal state

- `program` — current field directions for the visible slots
- `north_cell`, `south_cell` — live bead positions
- `north_locked`, `south_locked` — whether a bead is already captured
- `wall_cells` — the board border and any internal blockers
- `runs_used`, `run_budget` — remaining executions

## Notable code patterns

- Slot edits are free; only `RUN` consumes budget.
- Both beads move on every pulse, but in opposite directions.
- Capture locks a bead in place, which creates the sequencing logic in levels 2 and 3.
