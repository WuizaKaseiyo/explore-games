# Game generation final report

## Generated game
- **ID**: yh3p
- **Source**: `prior-games/yh3p/yh3p.py`
- **Metadata**: `prior-games/yh3p/metadata.json`
- **Lines of code**: 411

## Mechanic

The player nurses a single rooted vine across a 16×16 logical grid
(rendered at 64×64 pixels). Arrow keys extend the vine's active
glowing tip one cell in the pressed direction; the cell the tip
leaves becomes a permanent green stalk, and growth into walls or
existing vine is blocked. Clicking any prior vine cell (root or
stalk) jumps the active tip back to that cell, letting the player
spawn a new branch from a chosen anchor — the vine grows as a tree,
not a single path. The final level adds notched flower buds whose
yellow stamen marks an intake side; the player must arrive at the
bud moving INTO that side and press ACTION5 to bloom-commit.
Successful bloom turns the tip dormant until the next click. The
level is won when every bud is bloomed before the step counter
runs out; lose comes only from budget exhaustion.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Grow active tip 1 cell UP (sets tip facing → UP). |
| ACTION2 | Grow active tip 1 cell DOWN (sets tip facing → DOWN). |
| ACTION3 | Grow active tip 1 cell LEFT (sets tip facing → LEFT). |
| ACTION4 | Grow active tip 1 cell RIGHT (sets tip facing → RIGHT). |
| ACTION5 | Bloom-commit at tip cell — succeeds only on a notched bud whose intake direction matches tip's facing. Sets tip dormant on success. |
| ACTION6 | Click at (x, y); if the click cell is a vine cell, re-anchor the active tip there and clear facing. |

(ACTION7 omitted; this game has no undo verb.)

## Levels

- **L1** — base mechanic only (extend-tip): single root, single
  closed bud at the far end of an empty horizontal corridor. The
  player learns that arrow keys extend a glowing tip and that the
  bud blooms automatically when the tip arrives.
- **L2** — adds click-to-rebranch (ACTION6): two closed buds in
  walled-off regions; covering both requires re-anchoring the tip
  back at the root after the first bud and routing a second branch
  through the wall column's bottom-row gap.
- **L3** — adds directional bloom-commit (ACTION5): three notched
  buds in three quadrants of an L-walled playfield; each bud's
  yellow stamen indicates the direction from which the tip must
  approach. After each successful bloom the tip is dormant, so the
  player must use ACTION6 between buds; routing each branch's
  terminal cell from the correct side is the L3 puzzle.

## Novelty note

- **Closest taxonomy entry**: `sk48 paired-snake-trail` (arrow-grown
  trail with per-cell colour matching). Distinguishing rule: yh3p
  is a *single rooted vine that branches* via click-rebranch (sk48
  has *two heads in lockstep mirror*); yh3p's win is per-target
  bloom-commit with directional intake matching, not trail-colour
  parity.
- **Closest prior-game entry**: `ek73 wake-trail-evade` (avatar
  walks; trail decays into hazards). Distinguishing rule: yh3p's
  trail is a *permanent helpful structure* the player intentionally
  builds and re-anchors on; ek73's trail is a *decaying hazard the
  player evades*. Opposite-direction core dynamic and opposite role
  for the trail.

## Index update

Confirmed: one row appended to
`prior-games/index.md`:

```
| yh3p | vine-branch-bloom | Vine-Branch-Bloom — arrow-grow vine from root; click any vine cell re-anchors tip; L3 buds need directional ACTION5 bloom-commit. | 2026-05-10T07:03:58Z | (autonomous) |
```

## Smoke test summary

All 10 universal checks passed across all 3 levels; 4 custom
checks (extend-moves-tip, wall-blocks-extend,
click-resets-facing, bloom-requires-facing-match) passed.
Witness routes (12, 29, 40 actions respectively) all replay
to advance/win.
