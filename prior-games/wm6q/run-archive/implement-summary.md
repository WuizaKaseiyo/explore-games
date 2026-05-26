# Implement summary

## Files written
- `prior-games/wm6q/wm6q.py` — 394 lines.
- `prior-games/wm6q/metadata.json` — 8 lines.

## Verification
- `python -c "import ast; ast.parse(...)"` → PARSE OK.
- Runtime smoke (`g = Wm6q()`) → instantiated OK; `_levels` count = 3;
  `_available_actions` = `[6]`.
- `__pycache__` cleaned up.

## Plain-English summary of the implemented rule
The player is presented with a fixed grid of square tiles whose four edges
each carry one of four colours; the only verb is a click on a tile, which
cycles that tile's edge-colour assignment 90° clockwise. The level is won
when every shared edge between adjacent tiles carries the same colour on
both sides. Levels 2 and 3 introduce a locked tile (visible 6×6 black
square; clicks are no-ops, edges fixed) and a linked pair of tiles
(visible 6×6 ring; clicking either rotates both in lockstep), each adding
a new constraint that the player must reason around to find the unique
winning rotation configuration.
