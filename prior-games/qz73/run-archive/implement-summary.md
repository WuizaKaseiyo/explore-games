# Implement summary — qz73

## Files written

- `prior-games/qz73/qz73.py` — 394 lines.
- `prior-games/qz73/metadata.json`.

## Plain-English mechanic summary

A hub sits in the centre of the playfield with a small number of
coloured tip-pieces orbiting at fixed angular positions, plus
matching coloured rings ("sockets") at other positions. ACTION5
advances every unlocked tip to the next position clockwise (skipping
positions held by locked tips). ACTION6 click toggles a tip's
locked state. The level wins when every socket holds a tip whose
colour matches the socket's colour.

## Verification performed

- `python -c "import ast; ast.parse(...)"` → syntax OK.
- `Qz73()` instantiates without error.
- L1: 2× ACTION5 advances `_current_level_index` 0 → 1.
- L2: ACTION6 (lock purple) + ACTION5 advances 1 → 2.
- L3: planned 7-action witness (lock M, rotate, lock Y, rotate, lock
  O, lock G, rotate) drives the game to `GameState.WIN`. The
  witness sequence completes within the 32-step budget. Pure-rotation
  play was confirmed to never reach win on L3 (verified by tracing the
  rotation orbit).
