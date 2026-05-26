# implement summary for vd3g

## Files written
- `prior-games/vd3g/vd3g.py` (553 lines)
- `prior-games/vd3g/metadata.json`

## Plain-English rule summary

The player clicks a playfield cell to toggle its terrain state
between two heights. After every click, every marble pawn that
sits on a raised cell with at least one cardinal lower neighbour
rolls one cell into that neighbour, picking the first lower
neighbour by a fixed cardinal priority. Marbles that come to rest
on a lower cell stay until the cell is toggled back. Two marbles
cannot share a cell. Each level wins when every marble is on its
matching-coloured target cell; running out of step budget loses.

## Verification
- Syntactic parse: PASS.
- Runtime instantiation: PASS — 3 levels detected, available_actions=[6].
- L1 witness (6 actions): PASS — level_idx advances 0 → 1.
- L2 witness (32 actions): PASS — level_idx advances 1 → 2.
- L3 witness (30 actions): PASS — final state == WIN.
