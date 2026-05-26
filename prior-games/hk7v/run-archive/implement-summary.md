# Implementation summary — hk7v

## Files

- `prior-games/hk7v/hk7v.py` — 449 lines
- `prior-games/hk7v/metadata.json`

## Plain-English summary

The player operates a horizontal trolley along a top beam and a hook
hanging from a vertical rope of variable length. ACTION3/4 slide the
trolley left/right; ACTION1/2 raise/lower the hook; ACTION5 toggles
grab and release. Coloured blocks must be moved from their starting
positions to same-coloured marker stripes on the floor. Across three
levels the puzzle composes additional constraints: a wall the rope
must clear by hook-raising before horizontal traversal, and a stacked
supply column whose blocks must be removed top-down.

## Verification

- `ast.parse` accepts the source.
- `Hk7v()` instantiates without raising.
- L1, L2, L3 witnesses simulated in-process via the public movement
  helpers; each completes with `_check_win()` returning True.
