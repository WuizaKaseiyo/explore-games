# Game generation final report

## Generated game

- **ID**: `mw8p`
- **Source**: `prior-games/mw8p/mw8p.py`
- **Metadata**: `prior-games/mw8p/metadata.json`
- **Lines of code**: 423

## Mechanic

The player controls a single light-blue A-creature on a small 8-cell ×
8-cell logical playfield (rendered on a 64×64 canvas at native
resolution). Cardinal arrow keys translate A by one cell. The
playfield also contains two species of autonomous NPC: B-creatures
(orange, spiky) pursue A one cell per turn along their dominant
Manhattan axis and remove A on same-cell coincidence (lose); and
C-creatures (green, leafy) pursue the nearest live B under the same
policy and remove that B on coincidence. The triangle closes via the
A-eats-C rule: when A walks onto a C, A enters the cell and the C is
consumed. Walls block all three species; the level wins when A
enters the exit cell. Level 1 is a tutorial with one B trapped in a
walled middle chamber so the player learns B's pursuit policy
safely. Level 2 introduces C as a tool: the only winning first
action causes C to land on B's pursuit-step cell and remove B,
which is essential because B otherwise catches A by turn 8. Level 3
introduces A-eats-C: A's only legal first move at the start is
onto a C-cell, forcing that mechanic, while a second C autonomously
catches the B that would otherwise block A's path to the exit.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | MOVE UP — translate A by one 8-px cell in the −y direction (blocked by walls, grid bounds; entering B's cell loses; entering C's cell consumes the C). |
| ACTION2 | MOVE DOWN — +y direction; same blocking + lose + consume rules. |
| ACTION3 | MOVE LEFT — −x direction; same rules. |
| ACTION4 | MOVE RIGHT — +x direction; same rules. |

(No ACTION5/6/7 declared. Pure cardinal walking.)

## Levels

| Level | Mechanic introduced | Step budget |
|---|---|---|
| 1 | M1 (B-chases-A and kills on same cell). B trapped in a walled middle chamber while A traverses the bottom corridor + col-7 corridor to the top-right exit. | 25 |
| 2 | M2 (C-chases-B and kills on same cell). A walks RIGHT-first to draw B's vertical-pursuit step onto C's pursuit step; B is removed at turn 1. The witness is 7×RIGHT + 7×DOWN. | 30 |
| 3 | M3 (A-eats-C on entry). A's only legal first move is onto C₁, forcing M3. C₂ catches B at turn 1 (M2). A continues right (eating C₂ at turn 4) and up col-7 to the top-right exit. | 35 |

## Novelty note

- **Closest taxonomy entry**: `tu93` (maze-pickup-train). Distinguishing rule: tu93's secondary NPC species follow independent tick functions and the win condition is collecting them onto a goal tile; mw8p's two secondary species follow ONE shared pursuit rule (Manhattan-dominant chase) parameterised by who-chases-whom, and they predate each other in a directed cycle.
- **Closest prior-game entry**: `zk9p` (pursuer-merge-walk). Distinguishing rule: zk9p has ONE species of pursuer that merges on self-collision; mw8p has THREE species in a directed predation cycle (A predates C, B predates A, C predates B), and the win condition is "reach an exit cell", not "eliminate all pursuers".

## Index update

One row appended to `prior-games/index.md`:

```
| mw8p | predator-prey-triangle | Predator-Prey Triangle — A walks; autonomous B chases A and kills on same-cell; C autonomously chases nearest B and removes B on coincidence; A eats C on entry. | 2026-05-11T02:17:20Z | (autonomous) |
```
