# Implementation summary — fw8c

## Files written
- `prior-games/fw8c/fw8c.py` — 495 lines.
- `prior-games/fw8c/metadata.json` — schema-conformant JSON.

## Smoke verification
- `python -c "import ast; ast.parse(...)"` — SYNTAX OK.
- Runtime instantiation `Fw8c()` succeeded; reports 3 levels,
  `available_actions=[1, 2, 3, 4]`, L1 grid_size (64, 64), 31 sprites
  in L1.

## Plain-English rule summary
The carrier walks a chamber via cardinal arrow keys; stepping onto a
pigment-pad sprite combines that pigment into the carrier's stored set;
stepping onto a slot whose demand matches the carrier's set consumes the
slot and clears the carrier. Levels promote difficulty by introducing
multi-pigment mixture slots (level 2) and a state-conditional gate that
constrains routing (level 3). Step-counter HUD drains per action; level
ends in a win when every slot is consumed or a loss when the budget runs
out.
