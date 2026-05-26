# implement-summary

## Files
- `prior-games/hr8q/hr8q.py` (729 lines)
- `prior-games/hr8q/metadata.json`

## Summary
The player sees a target colour chip on the left, a row of input
slots beneath it, a result slot below those, and a column of
clickable colour blocks on the right. Clicking two (or, at the
third level, three) blocks fills the input slots; the result auto-
displays; pressing the commit verb either consumes the matching
target or distils the result back into the palette as a new one-
shot block. Difficulty grows by adding chained recipes that
require distilling intermediates, then by adding a third input slot
that enables triple recipes.

## Smoke evidence
Instantiation succeeds; the L1+L2+L3 witnesses (3+6+7=16 actions
total) drive the engine to `GameState.WIN` cleanly.
