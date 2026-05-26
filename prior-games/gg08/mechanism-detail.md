# gg08 — row-flip-mirror

## Summary

The player clicks edge buttons to reflect a full row or column of coloured
tiles. The target grid is shown in a separated side panel. Later levels add
anchor cells that stay fixed during flips and disabled buttons that force the
player to use alternate rows/columns.

## Actions

`ACTION6` clicks a row or column button. Clicks on disabled buttons or the
board are no-ops.

## Levels

- Level 1: a compact 3x3 lesson board with a hand-authored two-flip scramble.
- Level 2: anchor cells are skipped by the reflection rule, with a moderate
  scramble.
- Level 3: anchors plus disabled buttons and the deepest scramble.

## Win / Lose

Win when the live grid equals the target grid. Lose when the step bar reaches
zero.
