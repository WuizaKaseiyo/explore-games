# Game generation final report

## Generated game
- **ID**: hl4n
- **Source**: `prior-games/hl4n/hl4n.py`
- **Metadata**: `prior-games/hl4n/metadata.json`
- **Lines of code**: 394

## Mechanic
The player is presented with an 8×8 grid of cells, framed along the left edge by 8 clickable row-tint markers and along the top edge (in L2 and L3) by 8 clickable column-tint markers. Each marker click cycles its tint through a 4-color palette (background → red → yellow → green → background), recoloring every cell in its row or column. A small number of cells carry ringed lock targets in a required color; the level wins when every lock-target cell renders its required color. The cell-color rule composes per level: L1 uses row-tint only (column markers absent); L2 has columns override rows when set; L3 introduces a brighter-wins blend rule, where the higher-palette-index of the row's and column's tints wins each cell — opening the door for a row to override a dimmer column tint at a single cell. A green step-counter HUD bar drains per click; running out loses the level.

## Action mapping
| Action | Effect |
|---|---|
| ACTION6 | Click at `(x, y)`. If the click hits a row marker, cycle that row's tint by one step in the cycle and recolor the row; if it hits a column marker, cycle that column's tint and recolor the column; otherwise no-op. |

## Levels
- **L1** introduces M1 (row-tint cycling). Three lock targets in distinct rows; solve each by clicking its row marker until it shows the required tint.
- **L2** adds M2 (column-tint with override rule). Lock pairs share rows or columns with conflicting required colors; solve the conflicts by overriding rows with column tints (or vice versa).
- **L3** adds M3 (brighter-wins blend). Adds a lock that can only be satisfied by setting the row's tint *brighter* than the column's tint at one cell — exercising the row-dominates-column case unique to L3.

## Novelty note
- **Closest taxonomy entry**: `lp85` (row-col-shift-grid). lp85 physically permutes cell positions when a row/column button is clicked. *Distinguishing rule*: hl4n's clicks recolor stationary cells; cells never move.
- **Closest prior-game entry**: `qx7p` (column-shift-row-align). qx7p slides vertical color-bands past a horizontal scan line. *Distinguishing rule*: hl4n cycles per-row and per-column tint *values* in place; no bands move.

## Index update
One row appended to `prior-games/index.md`:

```
| hl4n | row-col-tint-cross | Hue-Cross Loom — click left-edge row markers and top-edge column markers to cycle row/column tints; cells take their color from a level-specific row+column combiner; satisfy ringed lock targets. | 2026-05-09T01:28:09Z | (autonomous) |
```
