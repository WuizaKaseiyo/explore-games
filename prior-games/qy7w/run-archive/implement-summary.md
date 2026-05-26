# Implement summary

## Files written
- `prior-games/qy7w/qy7w.py` (730 lines)
- `prior-games/qy7w/metadata.json`

## Plain-English summary of the implemented rule

The game presents three coloured strands hanging from coloured caps at
the top of the playfield down to coloured slots at the bottom. Between
them are clickable crossings. Clicking a crossing toggles it between a
"pass-through" visual and a "swap" visual; the swap re-routes the
strands below it. Some levels add a wider crossing that swaps the
outermost strands in one click, a passive marker that ends the run if
a particular-coloured strand is routed through it, and a dye station
that re-paints whichever strand passes through it. The level wins when
each bottom slot's colour is met by the strand that ends up in its
column.

## Verification performed
- `python -c "import ast; ast.parse(open(...))"` → parse OK.
- Instantiated `Qy7w()` from a fresh subprocess → 3 levels, action
  subset `[6]`.
- Replayed all three spec witnesses end-to-end:
  - L1 (2 clicks): advanced to level 1.
  - L2 (2 clicks): advanced to level 2.
  - L3 (2 clicks): final state `WIN`.
- All three witnesses match the spec's `Witness solution` lines.
