# Game generation final report

## Generated game
- **ID**: rj5w
- **Source**: `prior-games/rj5w/rj5w.py`
- **Metadata**: `prior-games/rj5w/metadata.json`
- **Mechanism detail**: `prior-games/rj5w/mechanism-detail.md`
- **Run archive**: `prior-games/rj5w/run-archive/`
- **Lines of code**: 443

## Mechanic
The playfield is a sheet of "paper" with one or two thin
fold-line cursors that the player slides across the sheet using
arrow keys. Pressing ACTION5 commits a fold along the **active**
fold-line; every (unlocked) pawn's position is reflected through
that line. ACTION6 clicks a fold-line cursor to make it the
active axis (V vs. H). Pawns that move onto their colour-matched
target sprite become **locked** — visibly dimmed — and are no
longer affected by subsequent folds. The level is won when every
pawn coincides with its same-colour target. Composition: L1 has
only the vertical fold; L2 adds the horizontal fold and the
axis-toggle click; L3 adds the lock mechanic, which is the load-
bearing piece — without it, no fold sequence wins L3 because the
witness exploits a double-vertical-fold-cancels-itself trick that
moves one pawn into position twice (effectively undoing it) while
two locked pawns stay put.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Move active fold-line UP one row (only when H is active; L2/L3) |
| ACTION2 | Move active fold-line DOWN one row (only when H is active; L2/L3) |
| ACTION3 | Move active fold-line LEFT one column (only when V is active) |
| ACTION4 | Move active fold-line RIGHT one column (only when V is active) |
| ACTION5 | Commit a fold along the active axis — reflect every unlocked pawn through the fold-line |
| ACTION6 | Click `(gx, gy)`: cell on the V-line cursor → V active, cell on the H-line cursor → H active, else no-op (L2/L3 only) |

## Levels

- **L1 — V-fold tutorial.** One green pawn, one green target on
  opposite halves of the sheet, single vertical fold-line. Witness
  3 actions; budget 25.
- **L2 — adds H-fold and axis-toggle.** Three pawns (green,
  purple, yellow) in a diagonally-symmetric layout; the same F_v
  and F_h satisfy all three pairs. Witness 7 actions; budget 50.
- **L3 — adds lock-on-target.** Three pawns/targets arranged so
  the trivial single-fold-each-axis heuristic fails; the witness
  fires V-fold twice (the second cancels the first for the
  unlocked pawn) before firing H-fold once. Witness 12 actions;
  budget 80.

## Novelty note
- Closest taxonomy entry: **`ar25` (shape-mirror-cover)** — the
  only reference game that uses geometric reflection. Distinguishing
  rule: ar25 has STATIC reflectors that copy-mirror sprites
  passively (a piece exists at both real and reflected positions
  simultaneously); rj5w has a PLAYER-POSITIONED fold-line cursor
  and a discrete commit verb that PERMANENTLY teleports pawns to
  their reflected positions (pawns never co-exist at both spots).
- Closest prior-game entry: **`bx84` (beam-mirror-reflect)** —
  shares the word "mirror" but the mechanic is materially
  different. bx84 places per-cell mirrors that reflect a coloured
  beam emitter; rj5w has no beam at all — the fold-line reflects
  every pawn's position across the line in one discrete commit.
  Different scale (cell vs. whole sheet) and different verb
  (place-mirror-and-fire-beam vs. fold-and-flip).

## Index update
One row appended to `prior-games/index.md`:

```
| rj5w | axis-fold-mirror | Paper Folding — slide a fold-line cursor and commit to reflect every (unlocked) pawn across the line; lock-on-target keeps progress through subsequent folds. | 2026-05-08T01:06:59Z | (autonomous) |
```
