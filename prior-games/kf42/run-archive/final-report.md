# Game generation final report

## Generated game
- **ID**: kf42
- **Source**: `prior-games/kf42/kf42.py`
- **Metadata**: `prior-games/kf42/metadata.json`
- **Lines of code**: 407

## Mechanic
The player controls one of two single-cell pawns by clicking it
to make it active, then steps it one cell at a time with the four
arrow keys. The two pawns are joined by an invisible
maximum-distance tether: when an active-pawn step would otherwise
stretch the distance past the level's tether budget, the inactive
pawn is dragged exactly one cell toward the active one along the
shortest-strain line. Walking the active pawn onto a coloured
"set-pad" instantly assigns that pawn the pad's colour. Each level
holds two coloured target pads; the level is solved when both
pawns simultaneously occupy distinct target pads whose colours
match the pawns' current body colours. Level 1 introduces only the
tether (no cycler); level 2 introduces the colour-set pad and uses
it to force one pawn through a recolouring before reaching its
target; level 3 composes the two — both pawns must be cycled by
distinct pads and routed via separate maze corridors, with mid-
route click-switching to keep neither pawn dragged into the wrong
cycler.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | move active pawn UP one cell |
| ACTION2 | move active pawn DOWN one cell |
| ACTION3 | move active pawn LEFT one cell |
| ACTION4 | move active pawn RIGHT one cell |
| ACTION6 | click at `(data["x"], data["y"])`; if a pawn is at the resulting grid cell, that pawn becomes the active pawn |

`_get_valid_actions` returns ACTION6 entries (one per pawn) at all
times and ACTION1..4 only after the first selection.

## Levels
- **L1 (12×12, tether 4, 30 steps).** Open arena; two pawns and
  two colour-matched targets. Mechanic introduced: the
  max-distance tether — moving the active pawn far enough drags
  the inactive one.
- **L2 (14×14, tether 5, 50 steps).** A short interior wall and
  one blue colour-set pad. Both pawns start red; the player must
  walk one pawn over the blue pad to convert it, then route both
  to their colour-matched targets.
- **L3 (16×16, tether 6, 80 steps).** Two corridors carved by
  interior walls; one red colour-set pad and one blue colour-set
  pad placed asymmetrically. Pawns start red and blue but the
  geometry forces each pawn through the *opposite-colour* cycler
  before its own colour target. Composition of tether + cycler is
  necessary; click-switching the active pawn mid-route is
  necessary.

## Novelty note
- **Closest taxonomy entries**: `m0r0` (mirror-orb-merge — coupled
  by per-key MIRROR transform; kf42 couples by MAX-DISTANCE
  TETHER), `r11l` (centroid-puppet-leg — coupled by CENTROID
  AVERAGE; kf42 has no virtual sprite), `sk48` (paired-snake-trail
  — couples by colour-segment-tile match between two snake bodies;
  kf42 keeps each pawn as a single cell), and `ls20` (cycler-
  attribute-match — cycles avatar attributes via alphabet-walker;
  kf42's cycler is a direct destination-set, not an alphabet
  walker, and kf42 has TWO avatars under a tether).
- **Closest prior-game entry**: (none — `prior-games/index.md`
  was header-only at the start of this run.)

## Index update
One row appended to `prior-games/index.md`:

```
| kf42 | tether-pawn-cycle | Tether-Pair with Colour-Set Pads — two pawns share a max-distance tether; click selects, arrows step, walking onto a coloured pad sets pawn colour. | 2026-04-28T16:19:10Z | (autonomous) |
```
