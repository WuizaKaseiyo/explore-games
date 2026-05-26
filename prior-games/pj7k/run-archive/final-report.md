# Game generation final report

## Generated game
- **ID**: pj7k
- **Source**: `prior-games/pj7k/pj7k.py`
- **Metadata**: `prior-games/pj7k/metadata.json`
- **Lines of code**: 420

## Mechanic

The player controls a single coloured-faced cube — a 3×3 sprite
showing the cube's current top face plus thin strips for each of
its four side faces. Pressing an arrow key rolls the cube one cell
in that direction; the roll deterministically permutes the six
face colours so that the side facing the move direction becomes
the new top, the previously-top face moves to the trailing side,
and the trailing-side face becomes the new bottom. The colour
that ends up on the bottom after the roll is deposited as paint
on the cell the cube just landed on. Targets are tinted ring
sprites that the player must "paint" with the matching colour by
arriving with the right bottom face. ACTION5 twists the cube in
place (cycling the four side faces 90° clockwise) without moving
or painting. In Level 3, some cells are gated by colour locks
that only allow the cube through when its bottom-after-roll
matches the lock's colour. The composition arc is: L1 introduces
rolling-paint alone; L2 adds twist (target colours unreachable
without it); L3 adds locks (cells unreachable except through the
matching face). Win when every target cell shows its required
paint colour.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Roll cube one cell north; permute faces; deposit bottom on landed cell |
| ACTION2 | Roll cube one cell south; same |
| ACTION3 | Roll cube one cell west; same |
| ACTION4 | Roll cube one cell east; same |
| ACTION5 | Twist 90° clockwise about vertical axis; no movement; no paint |

## Levels

- **L1** — base rolling-paint verb; cube + 2 in-line targets;
  witness `[ACTION4, ACTION4]`.
- **L2** — adds in-place twist (ACTION5); cube + 3 targets;
  witness `[ACTION5, ACTION4, ACTION4, ACTION4, ACTION5,
  ACTION2]`.
- **L3** — adds colour-locks colocated with two targets; witness
  identical in shape to L2 but every roll is gated by the lock
  bottom-face check; the third target's planning depth requires
  one trailing twist + south-roll.

## Novelty note

- Closest taxonomy entry: **ls20 (cycler-attribute-match)**.
  Distinguishing rule: ls20's attribute cycle is triggered by
  stepping on dedicated cycler-tile sprites, decoupling movement
  from attribute change; pj7k couples movement and face-cycle
  inseparably (every roll permutes faces).
- Closest prior-game entry: **none** — the 8 priors (kf42, qz73,
  kx14, qb84, lq5x, gv47, hr8q, ng52) cover tether-pawn, rotor,
  fluid, lattice, cone, region-grow, recipe, classifier
  mechanics; none involve a rolling cube or face-orientation
  state.

## Index update

Appended one row to `prior-games/index.md`:

```
| pj7k | rolling-cube-face-paint | Rolling Cube Face-Paint — a single coloured-faced cube rolls through cells; each roll permutes its faces and deposits the bottom-face colour onto the cell. | 2026-04-30T20:31:35Z | (autonomous) |
```
