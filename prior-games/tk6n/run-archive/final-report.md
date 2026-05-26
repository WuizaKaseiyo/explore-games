# Game generation final report

## Generated game
- **ID**: tk6n
- **Source**: `prior-games/tk6n/tk6n.py`
- **Metadata**: `prior-games/tk6n/metadata.json`
- **Lines of code**: 716

## Mechanic

The player controls a single avatar that walks one cell per arrow
press and carries a thrown projectile. Pressing ACTION5 launches the
projectile in the avatar's current facing direction; it travels
outbound a fixed number of cells per level, then enters a homing
return phase where it greedy-Manhattan-steps toward the avatar's
CURRENT cell each tick. The projectile lights coloured target
sprites it overlaps on either leg, and is caught when its cell
coincides with the avatar's. Level 1 introduces the throw-and-catch
loop in an open arena. Level 2 adds a wall-height gating rule:
tall walls block both avatar and projectile, but short walls block
only the avatar (the projectile flies over) — the target hides
behind a short wall the projectile must traverse. Level 3 adds a
deterministically patrolling guard sprite that the projectile
freezes on contact, while the avatar must dodge by walking off the
guard's row before the patrol overtakes the start cell.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Walk avatar one cell up (and set facing = up). |
| ACTION2 | Walk avatar one cell down (and set facing = down). |
| ACTION3 | Walk avatar one cell left (and set facing = left). |
| ACTION4 | Walk avatar one cell right (and set facing = right). |
| ACTION5 | If boomerang is held: launch it in current facing direction. If boomerang is dropped and avatar overlaps the dropped cell: pick up. Invalid (gated) while in flight. |

## Levels

- **Level 1** — Base mechanic: throw + outbound + homing-return +
  catch + target-light-on-overlap. Open arena, single target.
- **Level 2** — Adds wall-height gating: `wall_tall` blocks both
  avatar walking and boomerang flight; `wall_short` blocks avatar
  walking only (boomerang flies over). Sealed corridor with a
  wall_short barrier between avatar and target.
- **Level 3** — Adds a deterministic patrolling guard. Avatar
  collision = lose; boomerang overlap = freeze guard for 4 ticks.
  L3 composes all three mechanics — boomerang must traverse
  wall_short AND avatar must avoid guard.

## Novelty note

- Closest taxonomy entry: **vt6q (prior-game) — grapple-anchor-
  yank**. Distinguishing rule: vt6q's grapple resolves in a single
  tick (instant yank); tk6n's boomerang is a multi-tick projectile
  with a homing return that re-aims toward the avatar's CURRENT
  cell each tick, lighting targets along its path on both legs.
- Closest prior-game entry: **bx84 — beam-mirror-reflect**.
  Distinguishing rule: bx84's beam is steady-state with player-
  cycled mirrors; tk6n has no continuous beam, no mirrors — a
  discrete projectile fires from the avatar and the player controls
  only the launch direction and subsequent walk.

`prior-games/index.md` was not empty at run start (70 entries).
Negative-similarity-check (8-dimension): 1 shared dimension
(universal step counter) with closest prior; well below the
3-dim rejection threshold.

## Index update

One row appended to `prior-games/index.md`:

```
| tk6n | boomerang-arc-catch | Boomerang Loop — throw a projectile that flies outbound then homing-returns to avatar's current cell, lighting targets along its path; catch on coincidence. | 2026-05-10T14:05:51Z | (autonomous) |
```
