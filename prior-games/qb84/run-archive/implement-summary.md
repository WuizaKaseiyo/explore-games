# Implement summary — qb84

## Files written
- `prior-games/qb84/qb84.py` — 519 lines.
- `prior-games/qb84/metadata.json` — 9 lines.

## Plain-English summary of the implemented rule

A serpentine chain of coloured beads needs to be recoloured to
match a target sequence. The player has a logical cursor that
moves forward / backward along the chain via two arrow keys, and
two additional arrow keys that displace the active bead toward an
adjacent peg sprite — when the displacement collides with a peg,
the bead and peg swap colours. Special pegs introduce wrinkles in
later levels: one variant locks the bead's colour after a single
swap, and another variant pairs with a second peg so that swapping
with one also forces the chain neighbour to take the other peg's
colour. Each level wins when every bead's colour matches its
target slot in the reference strip.

## Smoke verification done at implement time

- Python `ast.parse` succeeds.
- `Qb84()` instantiates without raising; engine initialises
  level 1 from `Level.data`.
- L1 witness sequence `[1, 4, 4, 1, 4, 4, 4, 2]` advances to L2
  (engine state still NOT_FINISHED — correct, more levels remain).
- L2 witness sequence `[1, 4, 4, 1, 4, 2, 4, 4, 2, 4, 4, 2]`
  advances to L3.
- L3 witness sequence
  `[1, 4, 4, 4, 1, 4, 4, 1, 4, 4, 4, 2, 4, 2]`
  reaches `GameState.WIN` after action 14 — every bead's colour
  matches L3's target sequence
  `[11, 6, 14, 14, 11, 11, 15, 15, 14, 11]`.
- Pair-peg propagation verified: action 8 of L3 (lift on B5
  to pair-A `pg_l3_c`) sets B5=11 directly AND B6=15 via
  propagation from pair-B `pg_l3_d`'s purple.
- Sticky-peg lock verified: bead at index 3 in L3 locks after
  action 5, never recoloured by subsequent steps.
- One implementation bug found and fixed during smoke test:
  `_peg_color` initially read `pixels[1, 1]` (centre cell) which
  for sticky pegs returns the marker pixel (palette 4) instead of
  the body colour. Fixed by reading `pixels[1, 0]` (left-centre),
  which is the body colour for all peg variants.

## Pycache cleaned
- `find ... __pycache__ -exec rm -rf` ran without error.
