# Game generation final report

## Generated game
- **ID**: wj7d
- **Source**: `prior-games/wj7d/wj7d.py`
- **Metadata**: `prior-games/wj7d/metadata.json`
- **Lines of code**: 646

## Mechanic
The player has coloured 6×6 stamps on one half of a 64×64 playfield
that is bisected by a single white crease line. Pressing the FOLD
verb (ACTION5) reflects the currently-selected stamp's pixel pattern
across the crease and permanently deposits it onto the target half;
the stamp itself is consumed. The level wins when every pre-painted
dim-shadow target on the far half is fully covered by a same-colour
fold. Click (ACTION6) selects which stamp is active. Level 1
introduces MOVE-stamp + FOLD with a single auto-selected stamp and a
fixed crease. Level 2 adds SELECT-among-stamps and engineers a
collision so the player must fold one stamp first to clear a path
for the second. Level 3 unlocks MOVE-CREASE and RE-ORIENT-CREASE
(click on a selected crease pivots H↔V at the click cell): one stamp
needs the H-crease translated to a different row, the other needs a
specifically-positioned V-crease so the pivot column matters.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | UP (selected stamp -4 in y; selected H crease row -=4 at L3) |
| ACTION2 | DOWN (selected stamp +4 in y; selected H crease row +=4 at L3) |
| ACTION3 | LEFT (selected stamp -4 in x; selected V crease col -=4 at L3) |
| ACTION4 | RIGHT (selected stamp +4 in x; selected V crease col +=4 at L3) |
| ACTION5 | FOLD — reflect the selected stamp across the crease and consume it |
| ACTION6 | CLICK — select stamp / select crease / re-orient crease at click cell |

## Levels
- **L1**: introduces MOVE-stamp + FOLD-commit. One stamp, fixed
  H crease at row 31, auto-selected. Witness: 6 actions.
- **L2**: adds SELECT-among-stamps. Two stamps, fixed H crease,
  no auto-select; geometric collision forces fold-blue-first
  ordering for the witness. Witness: 16 actions.
- **L3**: adds MOVE-CREASE and RE-ORIENT-CREASE (+2 mechanics).
  Two stamps; one needs H crease translated to a non-default row,
  the other needs a precisely-positioned V crease (col=33).
  Witness: 9 actions.

## Novelty note
- **Closest taxonomy entry**: `ar25` (shape-mirror-cover).
  Distinguishing rule: ar25 has a stationary mirror line and a
  *continuous* mirror-ghost of a single shape that slides as
  the player slides the shape; wj7d's fold is a one-shot
  destructive commit (ACTION5) that consumes the stamp and
  permanently paints reflected colour into target cells. The
  crease is also movable and re-orientable in L3; ar25's mirror
  never moves or re-orients.
- **Closest prior-game entry**: `rj5w` (axis-fold-mirror, added
  to `prior-games/index.md` minutes before this run's finalize
  step). Both are paper-fold-across-axis mechanics. The
  distinguishing rules:
  1. **Reflected entity**: rj5w reflects PERSISTENT
     single-cell pawn anchors that survive multiple folds and
     can be LOCKED onto matching target rings. wj7d reflects
     MULTI-CELL 6×6 stamps with internal pixel patterns; each
     stamp is CONSUMED on its commit; the persistent state
     lives in a coverage map of shadow-cells that have been
     inked.
  2. **Win-condition primitive**: rj5w = anchor cells coincide
     with target anchors (single-cell coincidence per pawn).
     wj7d = every non-transparent cell of every shadow sprite
     is covered with the matching stamp colour (multi-cell
     pixel-pattern coverage per stamp).
  3. **Fold scope**: rj5w's ACTION5 reflects EVERY unlocked pawn
     globally (one-shot global update). wj7d's ACTION5 reflects
     ONLY the currently-selected stamp; multi-stamp games
     require multiple folds and a per-stamp selection step.
  4. **Selection model**: rj5w's ACTION6 toggles which of two
     pre-placed fold-line cursors (V vs H) is active. wj7d's
     ACTION6 selects which stamp is the focus of FOLD, AND
     selects/re-orients the single crease (one crease at a time
     is active; re-orient pivots at the click cell).
  5. **Visual signature**: rj5w renders small single-cell pawns
     on a paper-coloured field with thin V/H-axis cursors. wj7d
     renders 6×6 patterned stamps with internal pixel structure
     on a light-grey two-halved field with a prominent white
     bisecting crease and dim-palette-pair shadow ghosts.
  6. **Pixel grain (Principle 1 of negative-similarity-check)**:
     rj5w's primary game elements are single-cell anchors; wj7d's
     are 6×6 sprites with internal accent patterns.
  7. **Player mental model**: rj5w = "manipulate axis cursors
     until all pawns coincide with their target anchors,
     locking each one progressively". wj7d = "for each stamp,
     pre-position it and the crease, then commit one
     destructive fold per stamp; multi-stamp games require
     re-orienting the crease between commits".

  Per the negative-similarity 7-dimension test: rj5w and wj7d
  share dimensions 1, 2, 3, 4, 5 (lighter dimensions —
  axis-line + reflectible-entities, arrow input + ACTION5 +
  ACTION6, colour-pair matching, step counter, axis cursor +
  reflectible body); they DIVERGE on the heavier dimensions
  6, 7, 8 (palette/visual signature, pixel grain, core
  dynamic). The fold-paper concept is shared, but the
  instantiations differ on the heavier-weighted axes per the
  rule of thumb in `negative-similarity-check.md`.

  Note: the `pick_mechanic` step ran on a corpus that did not
  yet include `rj5w` (rj5w's `prior-games/index.md` row has
  timestamp 2026-05-08T01:06:59Z, which is later than this
  run's pick_mechanic step). The collision is a parallel-run
  artefact, not an oversight in the novelty check.

## Index update
One row appended to `prior-games/index.md`:

```
| wj7d | fold-crease-overlay | Fold-Crease Overlay — mirror-reflect coloured stamps across a single white crease that bisects the playfield to cover dim-shadow targets on the far half; crease moves and re-orients in late levels. | 2026-05-08T01:10:58Z | (autonomous) |
```
