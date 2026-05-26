# implement summary

## Files

- `prior-games/bw7k/bw7k.py` (337 lines)
- `prior-games/bw7k/metadata.json`

## Plain-English summary of the implemented rule

A small avatar walks the grid one cell per arrow press. Scattered
on the board are coloured rune-pads paired with same-coloured
hollow rings. The first time the avatar steps on a rune-pad, a
ghostly companion of the matching colour appears — the companion
is positioned at where it would have ended if it had repeated the
avatar's recorded walk-history from the rune-pad's cell, walking
through walls only when free and skipping any step blocked by a
wall or grid edge. The level resolves when the avatar stands on
its goal frame and every spawned companion stands on its same-
coloured ring. A bottom-row step bar drains one cell per action
and ends the level if it empties before the goal is satisfied.
