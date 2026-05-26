# gg10 — echo-delay-follower

## Summary

The player moves an orange lead pawn with arrow actions. A blue echo pawn
replays the lead's movement after a fixed delay. Targets are large
colour-matched pads on the board and require both pawns to arrive on the same
turn. Level 3 adds follower-only hazard crosses and a delay dial.

## Actions

- `ACTION1` / `ACTION2` / `ACTION3` / `ACTION4`: move the lead and enqueue
  the attempted direction for delayed follower replay.
- `ACTION6`: on level 3, cycle the delay dial.

## Levels

- Level 1: large-cell corridor with a centre barrier; the lead must insert a
  vertical detour so the delayed echo lands on its own colour-matched target.
- Level 2: larger maze with two gate walls. There are no hazard reset pads on
  this level; the puzzle is purely about routing the delayed echo through a
  different gate from the lead.
- Level 3: larger maze with red follower-only hazard crosses plus delay
  cycling; replaying the movement path without cycling the dial leaves the
  echo one cell off target.

## Win / Lose

Win when lead and follower simultaneously occupy their own target cells. Lose
when the step bar reaches zero.
