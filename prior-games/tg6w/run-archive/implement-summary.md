# implement-summary

- **Source**: `prior-games/tg6w/tg6w.py`
- **Metadata**: `prior-games/tg6w/metadata.json`
- **Lines of code**: 597

## Plain-English summary of the rule

Each arrow press sets the playfield's "down" direction; every loose block sprite slides simultaneously, multi-cell, in that direction, animated one cell per frame, until obstructed by a wall, another block, or the playfield border. Coloured-rim walls are passable to blocks of the matching colour and blocking to all others. Sticky-pads catch the first block to slide across them and fix that block at the cell for the rest of the level. The level wins when every block sits on a same-coloured target; loses on step exhaustion or on a soft-lock (a block is fixed off-target, or every same-colour target is occupied by a wrong-colour fixed block).

## Witness verification (runtime smoke run)

All three levels won via their planned witness sequences:

- L1 `[ACTION2]` → next_level()
- L2 `[ACTION2, ACTION3]` → next_level()
- L3 `[ACTION3, ACTION2, ACTION4, ACTION2]` → win()

Final game state after the L3 witness: `GameState.WIN`.
