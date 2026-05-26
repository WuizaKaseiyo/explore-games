# Game generation final report

## Generated game
- **ID**: `zd7m`
- **Source**: `prior-games/zd7m/zd7m.py`
- **Metadata**: `prior-games/zd7m/metadata.json`
- **Lines of code**: 413

## Mechanic

`zd7m` is a pure-arrow puzzle in which each press of a cardinal
arrow attempts to step **every** movable pawn on the board one
cell in that direction simultaneously. The cohort moves as a
synchronised group; pawns that would collide with a wall, an
immovable anchor block, or another pawn whose own destination
is blocked stay put for the turn while the rest of the cohort
moves. The win condition is positional + colour-matched: each
coloured pawn must end the level on a target tile of its own
colour. Level 1 introduces cohort-step + colour-matching with
three free pawns descending to three matching targets. Level 2
adds anchor sprites that selectively block pawns and let the
player change the cohort's relative offsets. Level 3 adds a
purple portal pair that teleports a pawn from `portal_a` to
`portal_b` on landing, providing the only access route into a
chamber sealed by anchor walls.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 (UP) | Every movable pawn attempts to step (x, y - 1). |
| ACTION2 (DOWN) | Every movable pawn attempts to step (x, y + 1). |
| ACTION3 (LEFT) | Every movable pawn attempts to step (x - 1, y). |
| ACTION4 (RIGHT) | Every movable pawn attempts to step (x + 1, y). |

## Levels

- **L1** — base dynamic system: cohort-step + colour-matching.
  Three pawns + three same-colour targets; descend together.
- **L2** — adds the anchor mechanic. Two pawns + two targets +
  two anchor blocks that selectively block pawns so the cohort's
  relative offset can change.
- **L3** — adds the portal pair. Two pawns + two targets + five
  anchors (carrying-forward selective-block + new chamber walls)
  + a purple portal pair that teleports a pawn into the
  otherwise-inaccessible chamber.

## Novelty note

- Closest taxonomy entry: `m0r0 mirror-orb-merge`. Distinguishing
  rule: m0r0 is exactly two anti-coupled mirror orbs (LEFT moves
  them in opposite directions); zd7m has any number of
  isotropically-coupled pawns (LEFT moves them all left).
- Closest prior-games entry: `kn58 anchor-pull-magnet`.
  Distinguishing rule: kn58 is click-only — clicking any cell
  plants an attractor and every pawn slides one cell along its
  dominant Manhattan axis toward the click. zd7m is arrow-only:
  each press translates every pawn one cell in the global
  pressed direction (no click, no per-pawn-axis projection).
  Visual signature also diverges (zd7m off-black + bright
  pastels + 3×3 ring-with-centre-dot sprites; kn58 pale-grey +
  small sparse blocks).

## Index update

One row appended to `prior-games/index.md`:

```
| zd7m | cohort-step-route | Cohort-Step Routing — arrows step every movable pawn one cell; anchors selectively block; portals teleport into a sealed chamber. | 2026-05-06T23:34:10Z | (autonomous) |
```
