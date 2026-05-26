# Game generation final report

## Generated game
- **ID**: qx7p
- **Source**: `prior-games/qx7p/qx7p.py`
- **Metadata**: `prior-games/qx7p/metadata.json`
- **Lines of code**: 456

## Mechanic
The player operates on three to five tall vertical columns, each
painted as a stack of differently-coloured horizontal segments — a
vertical bar-code of twelve segments. A horizontal scan line cuts
across all columns at one specific row; the segment of each column
the scan line crosses is that column's "currently aligned" colour.
Above each column sits a framed colour-swatch label showing the
colour the player must surface at the scan line. Click selects a
column; up- or down-arrow keys cyclically scroll the active column's
band-stack one segment at a time. Difficulty composes: level 2
introduces a permanently-coupled bound pair (visibly tied by an
orange ribbon) that drives partner columns in opposite directions
when one is shifted; level 3 introduces a movable scan line cycled
by the modal action key, where two distinct bound pairs each demand
a different scan-line offset and the level cannot be solved without
moving the scan line.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Shift the active column's band-stack one segment up. If the active column is in a bound pair, the partner shifts one segment down in the same tick. |
| ACTION2 | Shift the active column's band-stack one segment down. Bound-pair coupling fires with opposite sign. |
| ACTION5 | (L3 only) Advance the scan-line cycle to the next of three pre-defined rows; re-evaluates which segment of each column is read. |
| ACTION6 | Click a cell. If the cell is inside a column's bounding box, set that column as the active column. Otherwise deselect. |

## Levels

- **L1.** 3 independent columns at fixed scan line. Mechanic introduced: column-shift. Witness: `[ACTION6@(16,14), ACTION1×4, ACTION6@(32,14), ACTION2×5, ACTION6@(48,14), ACTION1×3]` — 15 actions; budget 40.
- **L2.** 4 columns; the leftmost two are a bound pair. Mechanic introduced: bound-pair coupling. Carries column-shift forward. Witness: `[ACTION6@(12,14), ACTION1×4, ACTION6@(40,14), ACTION1×6, ACTION6@(54,14), ACTION1×2]` — 15 actions; budget 70.
- **L3.** 5 columns; two bound pairs (both with sum-4 invariant) and one independent column; movable scan line cycles {row 32, row 35, row 38} (offsets 6, 7, 8) with only offset 8 satisfying the bound-pair invariant. Mechanic introduced: scan-line shift (M3). Witness: `[ACTION5, ACTION5, ACTION6@(6,14), ACTION2×5, ACTION6@(30,14), ACTION2×4, ACTION6@(54,14), ACTION2×3]` — 15 actions; budget 100.

## Novelty note

- **Closest taxonomy entry: `lp85`** (button-permutation-puzzle). Distinguishing rule: lp85 applies pre-baked permutation tables to a 2D grid of pawn-pieces (clicks fire global permutations); qx7p has independent vertical band-stacks each manipulated by a +1/−1 modular shift. There are no permutation tables; shifts are local, linear, and deterministic per column. lp85's win is positional pawn-to-cell matching anywhere on the grid; qx7p's win is row-pattern match at one horizontal scan line.
- **Closest prior-games entry: `qz73`** (radial-cycle-lock). Distinguishing rule: qz73 rotates a single radial rotor with per-tip locking around a central pivot; qx7p has multiple independent vertical bars with no shared pivot, no per-segment locking, and a separate horizontal scan-line as the win-condition axis. Visually qz73 is radial pawns around a centre; qx7p is straight vertical bars.

## Index update

Appended one row to `prior-games/index.md`:

```
| qx7p | column-shift-row-align | Column-Shift Row-Align — vertical colour-band columns slid past a horizontal scan line to match a target row colour pattern; bound-pair coupling and movable scan line. | 2026-05-07T22:06:44Z | (autonomous) |
```
