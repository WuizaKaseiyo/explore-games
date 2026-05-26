# gg14 — kiln-mosaic-stamp

The live board is a clay mosaic. `ACTION6` clicks one of the stamp handles
below the board to select it, then clicks a board cell to place that stencil
with its origin at the clicked cell. Selection is free; each board placement
consumes one energy step.

- Empty clay takes the stamp colour.
- A differently coloured occupied cell fuses into a third colour.
- Stamps can be reused at different origins.
- Level 3 adds a scraper stamp that clears selected cells before the final
  colour is pressed.

The target mosaic is shown in a separated right panel. The player must infer
which overlapping stamps produce each fused colour, instead of collecting
items or following a path.

Win when the live mosaic exactly equals the target mosaic. The step budget is
the intended number of placements, so solving requires both selecting the
right stencil and placing it at the right origin.
