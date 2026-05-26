# Game generation final report

## Generated game
- **ID**: qf8m
- **Source**: `prior-games/qf8m/qf8m.py`
- **Metadata**: `prior-games/qf8m/metadata.json`
- **Lines of code**: 545

## Mechanic

The player faces a 5×5 grid of square state-tiles next to a smaller
mirror grid showing the level's target pattern. Clicking a tile
(ACTION6 only) drives state changes through the grid; the rule
that fires depends on the clicked tile's *kind*, which is signalled
by its internal motif. A **rook** tile (`+`-cross motif) toggles
the state of every tile in its row OR column — a (2N−1)-cell
rook-cross flip. A **bishop** tile (`X`-cross motif) toggles every
tile on its main and anti-diagonals. A **tri-state** tile
(pink-ring motif with a state-coloured centre) is itself click-
inert but cycles mod 3 whenever its row/column/diagonal is touched
by another tile's click. Level 1 is rook-only and discoverable by
1-2 exploratory clicks; Level 2 introduces bishop tiles, requiring
the player to combine rook and bishop reach to reach a centred-plus
target; Level 3 introduces a tri-state cell at the grid centre,
forcing the player to plan the *exact number* of clicks whose
flip-region passes through the centre cell.

## Action mapping

| Action | Effect |
|---|---|
| ACTION6 | Click at pixel `(x, y)`. The clicked grid cell's *kind* (rook / bishop / tri-state) selects the rule. Rook click → flip every tile in row `row` OR col `col`. Bishop click → flip every tile on the main and anti-diagonals through `(col, row)`. Tri-state click → no-op (the step is consumed but no state changes). Out-of-grid clicks are no-ops with no step consumed. |

## Levels

- **Level 1** — rook-flip alone, all-rook 5×5 grid. Witness: 2
  clicks (rook(1,1), rook(3,3)). Step budget: 25.
- **Level 2** — adds bishop-flip. Layout: 23 rook + 2 bishop at
  (1,1) and (3,3). Witness: 3 clicks (rook(2,2), bishop(1,1),
  bishop(3,3)) producing the 5-cell centred-plus target. Step
  budget: 50.
- **Level 3** — adds the tri-state cell at (2,2). Layout: 22 rook
  + 2 bishop at (1,1) and (3,3) + 1 tri-state at (2,2). Witness:
  4 clicks (rook(0,4), rook(4,0), bishop(1,1), bishop(3,3)). The
  tri-state cell ends in state 2 because exactly two flips
  (the two bishop clicks' main-diagonal pass) touch (2,2). Step
  budget: 60.

## Novelty note

- **Closest taxonomy entry**: `ft09` (stamp-3x3-paint).
  Distinguishing rule: ft09's flip-region is a tunable 3×3 stamp
  with a constraint-graph win predicate; qf8m's flip-region is a
  fixed (2N−1)-cell rook-cross (and L2/L3's diagonal alternative)
  with a target-image win predicate.
- **Closest prior-game entry**: `tm5x` (thermal-aura-imprint).
  Distinguishing rule: tm5x stamps a local 5-cell plus-shape via
  an avatar's footprint; qf8m flips the full row+col rook-cross
  (or full diagonals for bishop) per click on a static grid.
  Local 5-cell plus vs global (2N−1)-cell row+col reach;
  avatar-carried stamp vs click-anywhere on a static grid.

## Index update

One row appended to `prior-games/index.md`:

```
| qf8m | rook-cross-toggle | Rook-Cross Toggle Pattern Match — click tiles to flip a (2N-1)-cell row+col cross; bishop tiles flip diagonals; tri-state cell cycles mod 3. | 2026-05-08T17:29:34Z | (autonomous) |
```
