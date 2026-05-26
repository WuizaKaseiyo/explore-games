# Game generation final report

## Generated game
- **ID**: `mz6t`
- **Source**: `prior-games/mz6t/mz6t.py`
- **Metadata**: `prior-games/mz6t/metadata.json`
- **Lines of code**: 573

## Mechanic

The player faces a 5×5 grid of small cells, each in one of three colour states (light-blue solid disc / orange hollow ring / pink plus-sign), with a quarter-scale target panel on the right edge of the frame showing the desired final configuration. The only verbs are ACTION6 (click a cell to advance its colour state by `+1 mod 3`) and ACTION5 (tick — apply majority-vote propagation simultaneously to every voting cell: each cell adopts whichever colour has at least 3 of its 4 cardinal neighbours, otherwise keeps its current colour). L1 establishes the base rule with a clean 2-action witness; L2 introduces walls (immutable cells that don't vote and aren't voted on) which protect a seed line from being out-voted to lb; L3 adds anchor cells that freeze permanently the first time their colour matches a per-cell target, which is what keeps the central pink anchor from being out-voted by its 4 orange neighbours when the final tick fires. The win check fires only on ACTION5 — making the tick verb structurally required by the engine.

## Action mapping

| Action | Effect |
|---|---|
| ACTION5 | Tick: apply synchronous majority-vote propagation to every voting cell (excluding walls and locked anchors). For each cell, count colour states among non-wall, in-grid cardinal neighbours; if any state `C` has `count(C) ≥ 3`, the cell adopts `C`. Walls don't change. The win check fires after this update. |
| ACTION6 | Click: advance the clicked cell's colour state by `+1 mod 3`. Click on a wall or a locked anchor consumes a step but produces no state change. |

## Levels

- **L1.** Base mechanics (click + tick). 5×5 grid, no walls, no anchors. A 3×3 inner block of orange around a single lb centre and one missing inner-corner cell. Player clicks the missing corner orange and ticks; tick fills the centre via majority rule. Witness 2 actions.
- **L2.** + Walls. 5×5 grid with walls at the 4 inner-corner cells. Walls protect the central row's orange line from being out-voted to lb during the final tick. Player clicks the 4 edge-midpoints orange and ticks; tick fills the centre. Witness 5 actions.
- **L3.** + Anchor freeze. Same wall layout plus an anchor at the centre whose target is pink. Player clicks the anchor twice (lb → orange → pink → LOCK), clicks the 4 ring cells around the anchor + the 2 row-1 / row-3 columns to orange, and ticks. The freeze keeps the anchor at pink despite 4 orange neighbours; without the freeze, the final tick flips the anchor to orange and the level fails. Witness 7 actions.

## Novelty note

- **Closest taxonomy entry**: `dc22 (colour-cycle-walk)`. *Distinguishing rule:* dc22 has a walking pawn whose footprint *globally* cycles every wedge of one colour-class via a trigger; mz6t has *no walking pawn*, mutates colour state per-cell on click and via a *separate global tick rule (majority of 4 cardinal neighbours)*.
- **Closest prior-game entry**: `gv47 (seed-grow-surround-dissolve)`. *Distinguishing rule:* gv47 grows paint regions outward from explicitly-placed seed sprites and merges contacting regions into derived colours on ACTION5; mz6t has no seeds or regions, every cell is a first-class voter, and the tick rule is *uniformly local 4-neighbour majority* with no colour-creation step.

## Index update

Appended to `prior-games/index.md`:

```
| mz6t | majority-vote-stabilize | Majority-Vote Stabilizer — click cells to cycle 3 colour states; ACTION5 ticks majority-vote; walls + anchors at L2/L3. | 2026-05-08T19:32:33Z | (autonomous) |
```

(Confirmed via `tail -1` after the append.)
