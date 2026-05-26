# Game generation final report

## Generated game

- **ID**: xz5g
- **Source**: `prior-games/xz5g/xz5g.py`
- **Metadata**: `prior-games/xz5g/metadata.json`
- **Lines of code**: 479

## Mechanic

The player solves three rotation puzzles by clicking a free
pivot cell on a 64×64 grid and pressing ACTION5 to rotate every
"rotatable" sprite 90° clockwise around the pivot. A tiny pink
"+" marks the exact pivot cell so the player can read off the
rotation centre at a glance. There is no direct movement verb —
pawns reach their targets only via the world-rotation transform.
Level 1 introduces the verb pair (click-to-set-pivot +
commit-rotate) and asks the player to deliver one blue avatar
onto its colour-matched target ring with a single rotation.
Level 2 adds an orange companion pawn that co-rotates with the
avatar; the player must find a single pivot whose two-rotation
sequence delivers each pawn to its target. Level 3 keeps the
same two-pawn cast but moves the pawns to NW/NE corners and
their targets diagonally to SE/SW; this corner-rotation puzzle
admits no single-rotation solution (brute-force verified) — the
unique short witness is two CWs around the centre, cycling
each pawn through the other's start to its own target.

## Action mapping

| Action | Effect |
|---|---|
| ACTION5 | Commit-rotate. Rotates every `rotatable` sprite 90° clockwise around `_pivot`. Rejected if a destination is out of bounds or two rotatables would collide on the same cell (clean simultaneous swap excepted). |
| ACTION6 | Click at (x, y). If it hits any rotatable or target sprite → no-op. Else → set `_pivot` to that cell and place the 3×3 "+" marker so its centre is on the pivot. |

(`available_actions=[5, 6]`. ACTION1-4 omitted; ACTION7 omitted —
no undo.)

## Levels

- **L1** — base dynamic system (M1 pivot-set + M2 commit-rotate). Avatar at (12, 32); avatar_target at (32, 12); single CW rotation around pivot (32, 32) wins. Witness 2 actions.
- **L2** — adds M3 companion-deliver. Avatar (8, 32) and companion (32, 8) each go to their colour-matched targets via 2 CWs around pivot (32, 32). Witness 3 actions.
- **L3** — same mechanic family as L2, reconfigured into a corner-rotation puzzle. Avatar (12, 12) → (52, 52) and companion (52, 12) → (12, 52) sit on diagonally-opposite corners. Brute-force verified that no single rotation around any pivot wins; exactly two CWs around the centre (32, 32) cycle each pawn through the other's start to its own target. Witness 3 actions.

## Novelty note

- **Closest taxonomy entry**: `cn04 nub-pair-glyph` — cn04 rotates
  a single SELECTED sprite 90° in place; xz5g rotates every
  `rotatable` sprite simultaneously around an EXTERNAL
  player-chosen pivot. Per-piece self-rotate vs whole-world-
  pivot-rotate are different rotation contracts.
- **Closest prior-game entry**: `vy3k region-swap-arrange` — vy3k
  has 4 fixed quadrant centres and rotates one quadrant's
  contents at a time within a 32×32 sub-region; xz5g has no
  quadrants and the pivot is a player-chosen any-cell
  (4096 candidates), with rotation applied to every rotatable
  sprite globally. The cognitive task differs:
  continuous-pivot-search (xz5g) vs discrete-quadrant-choice
  (vy3k); this is the Principle 3 core-dynamic divergence in
  `mechanic-novelty/negative-similarity-check.md`. xz5g also
  introduces a visit-checkpoint mechanic (anchor_pin) and a
  direction-toggle widget at L3 — neither present in vy3k.

## Index update

One row appended to `prior-games/index.md`:

```
| xz5g | arena-pivot-rotate | Pivot-and-Spin — click any cell to set the pivot; ACTION5 rotates every rotatable sprite 90° around it; pawns delivered to colour-matched targets. | 2026-05-08T19:15:42Z | (autonomous) |
```
