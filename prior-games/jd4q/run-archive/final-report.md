# Game generation final report

## Generated game
- **ID**: jd4q
- **Source**: `prior-games/jd4q/jd4q.py`
- **Metadata**: `prior-games/jd4q/metadata.json`
- **Lines of code**: 530

## Mechanic

The player walks an avatar through a maze on a 64×64 grid (cell-stride
4). Every cell the avatar leaves becomes a fading echo-stone visible
on the grid; the player can click any visible echo to teleport the
avatar back to that cell, consuming the clicked echo and every echo
deposited after it (rewinding the trail). Some cells are one-way
passages that seal into walls the moment the avatar walks off them;
one cell type wipes the entire echo-trail when entered. Level 1 is a
plain corridor walk with the echo system disabled (tutorial). Level 2
introduces the echo-trail and the one-way passages together: a single
dead-end branch holds a pickup, after which the corridor is sealed
and the only escape is teleport. Level 3 layers the trail-wipe cell
on top: three branches, three pickups, and the wipe-cell on the only
path to goal — the player must save the wipe-branch for last or
trap themselves at one of the closing-door dead-ends.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Walk avatar one cell (4 px) up |
| ACTION2 | Walk avatar one cell down |
| ACTION3 | Walk avatar one cell left |
| ACTION4 | Walk avatar one cell right |
| ACTION6 | Click on a visible echo cell — teleport avatar to that cell, consuming that echo + every later echo (no-op at level 1 where echoes are disabled) |

## Levels

- **L1** (tutorial): single horizontal corridor, walk to goal. Witness 11 actions.
- **L2**: introduces echo-trail-with-rewind and closing-doors; one dead-end branch behind closing-doors holds the required pickup; teleport is required to escape. Witness 25 actions.
- **L3**: introduces echo-eraser cell; three branches with three pickups, the eraser is on the only path to goal — visit branches A and B first (closing-door dead-ends, teleport-back), then walk through the eraser-cell into branch C last. Witness 32 actions.

## Novelty note

- **Closest taxonomy entry**: `g50t` (walk-vs-scroll / ghost-replay-multitarget). g50t commits paths via ACTION5 to spawn ghosts that replay in lockstep with the avatar; ghosts ACCUMULATE and ANIMATE every step. jd4q has no commit, no ghost-replay, no scrolling timer — echoes are STATIC fading dots that are CONSUMED by clicking. g50t adds-trails-to-the-world; jd4q removes-trails-from-the-world.
- **Closest prior-games entry**: `bp35` (procedural-graph-walk + undo) shares click-teleport surface; jd4q teleports to PRIOR-SELF positions on a continuous Manhattan grid, while bp35 teleports to highlighted graph-neighbour nodes — different topology and different teleport target.
- `prior-games/index.md` was non-empty (28 prior entries scanned including the latest `vd3g` at 2026-05-07T20:47:47Z); jd4q's distinguishing rule against each was articulated in spec § 9.

## Index update

One row appended to `prior-games/index.md`:

```
| jd4q | echo-trail-teleport | Echo-Trail Maze — avatar walks; each step deposits a fading echo, click to teleport back consuming the trail; closing-doors and an eraser cell shape branch-visit ordering. | 2026-05-07T20:54:37Z | (autonomous) |
```

Verified via `tail -1` on the file.
