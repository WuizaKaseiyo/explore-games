# Game generation final report

## Generated game
- **ID**: hb5n
- **Source**: `prior-games/hb5n/hb5n.py`
- **Metadata**: `prior-games/hb5n/metadata.json`
- **Lines of code**: 471

## Mechanic

The player controls an irregular-shaped walking avatar (a rigid
3-cell L polyomino) on a 16×16 logical playfield. Arrow keys
translate the entire polyomino one cell in their direction;
ACTION5 rotates it 90° clockwise about the anchor cell (the cell
visually marked by an orange centre, distinct from the maroon
centres of body cells). The level wins when the avatar's cell
footprint exactly matches a target SLOT silhouette (a dim
palette-3 outline) at the goal position. Level 2 introduces a
GROWTH pickup that, on consumption, adds a fourth body cell to
the polyomino (extending the L into a J at rotation 0). Level 3
introduces a PIVOT-RESET cell that transfers the anchor
designation from cell A to cell B of the polyomino, opening up a
new rotation space (B-pivot rotations include a T-silhouette
which A-pivot rotations cannot produce). The L3 target is a
T-silhouette unreachable without pivot-reset, forcing the player
to discover and use both M3 and M4 in concert.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | Translate the polyomino 1 cell UP (rejected if any body cell would collide with a wall or fall off-grid). |
| ACTION2 | Translate 1 cell DOWN. |
| ACTION3 | Translate 1 cell LEFT. |
| ACTION4 | Translate 1 cell RIGHT. |
| ACTION5 | Rotate the polyomino 90° clockwise about the current anchor (rejected if any post-rotation cell would collide). |

## Levels
- **L1**: walk (M1) + rotate-self (M2). Avatar at (2,2) starts rotation 0; target L-silhouette at (12,12) is at rotation 270; player walks SE then rotates 3× to match. Witness 23 actions; step budget 50.
- **L2**: + growth-pickup (M3). Pickup at (4,2) extends the avatar from 3-cell L to 4-cell J; target J-silhouette at rotation 180 in the lower-right requires walking + consuming + rotating twice. Witness 22 actions; step budget 60.
- **L3**: + pivot-reset (M4). Pivot-reset at (10,10) transfers anchor to the B cell, opening a T-silhouette in the B-pivot's rotation 90; target T at (12,12) is geometrically unreachable from A-pivot. Witness 20 actions; step budget 80.

## Novelty note
- **Closest taxonomy entry**: cn04 (rotate-translate-jigsaw) — click-select multi-piece flat board with rotate-and-translate verbs. **Distinguishing rule**: hb5n has no clicks and no multi-piece selection; the avatar IS the only mobile polyomino and walks through a maze; the win is silhouette-match-at-slot, not connector-snap between pieces.
- **Closest prior-game entry**: xv4n (cavity-nest-fit) — irregular pieces lifted/dropped into matching cavities via click; ACTION5 rotates held piece. **Distinguishing rule**: hb5n has no clicks, no lift/drop verb, and no placement teleportation; the polyomino IS the walking player and traverses the maze cell-by-cell. Also closer-in-spirit prior nz3v (rotor-pivot-walk) uses a 2×2 SQUARE avatar with a separately-rotating wedge — hb5n's avatar is irregular and rotates AS itself.

## Index update

Row appended to `prior-games/index.md`:

```
| hb5n | polyomino-walker-rotate | Polyomino Threader — 3-cell L avatar walks + rotates 90° about anchor; growth pickup adds 4th cell; pivot-reset transfers anchor designation to a different body cell, opening a T-silhouette rotation space. | 2026-05-11T02:00:26Z | (autonomous) |
```
