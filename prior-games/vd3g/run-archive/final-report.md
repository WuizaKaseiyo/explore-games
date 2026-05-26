# Game generation final report

## Generated game
- **ID**: vd3g
- **Source**: `prior-games/vd3g/vd3g.py`
- **Metadata**: `prior-games/vd3g/metadata.json`
- **Lines of code**: 553

## Mechanic

The player is given a 16×16 grid of terrain whose every non-wall non-
target cell is in one of two heights, raised (HIGH) or lowered (LOW),
and a small number of coloured marble pawns each with a same-coloured
target ring. The only player input is ACTION6 — click a cell to
toggle its terrain state HIGH↔LOW. After every click, every marble
on a HIGH cell with at least one cardinal LOW neighbour rolls one
cell into the lowest neighbour using the priority N→E→S→W; marbles
on LOW cells stay (settled in a valley); two marbles cannot share a
cell. Walls (introduced at L2) are immutable HIGH cells that
marbles never enter, forcing detours. Linked-anchor pairs (introduced
at L3) are two cells visually banded by a shared corner-cap colour
that toggle together regardless of distance — every anchor click
flips both linked cells in the same settling pass, so a single click
can ferry two marbles through opposite gaps simultaneously when
pre-positioned. Each level wins when every marble is on its
matching-coloured target cell; running out of step budget loses.

## Action mapping
| Action | Effect |
|---|---|
| ACTION6 | Click at display (x, y); engine converts via `camera.display_to_grid` to a logical (col, row) cell. Toggles the cell's terrain state if it is a normal HIGH/LOW or anchor cell (anchors also flip their partner). Walls and target cells are no-ops. After the toggle, the marble settling pass runs. |

## Levels
- **L1**: introduces the dig-toggle + roll-to-low mechanic. Single
  marble routed through three intermediate cells to its target. 6-action
  witness; step budget 16.
- **L2**: composes the L1 mechanic with WALL cells. A vertical wall
  column with a single mid-row gap forces an L-shaped detour. 32-action
  witness; step budget 50.
- **L3**: composes the L1+L2 mechanics with ANCHOR-LINK pairs. Two
  marbles must cross a wall column whose only gaps are two paired
  anchor cells; one anchor click flips both. 30-action witness;
  step budget 80.

## Novelty note

- Closest taxonomy entry: **m0r0** (mirror-orb-merge). Both involve
  coordinating multiple pawns to settle / merge. Distinguishing rule:
  m0r0 moves four avatars on direction press with per-quadrant
  mirrored axes (one global press affects everyone with reflected
  signs); vd3g uses ACTION6 click only and each marble independently
  reads its own 4-neighbourhood for a LOW cell — no axis mirroring,
  no global motion. The player edits TERRAIN, not pawn positions.
- Closest prior-game entries: **tg6w** (settle-pile-tilt) and
  **kn58** (anchor-pull-magnet).
  - vs tg6w: tg6w tilts the playfield's gravity direction with
    arrow keys and lets blocks slide multi-cell to the rim; vd3g
    has per-cell binary heights with marbles stepping exactly one
    cell per click toward a LOW neighbour. Different operating
    principle (global tilt vs local-gradient field) and different
    settling rule (slide-to-rim vs one-cell-step).
  - vs kn58: kn58 places a single global anchor that pulls every
    pawn one cell along its dominant Manhattan axis; vd3g has
    NO global attractor — marbles inspect their immediate
    4-neighbourhood for a LOW cell and step accordingly.

## Index update

One row appended to `prior-games/index.md`:

```
| vd3g | valley-dig-roll | Mound-and-Marble Routing — click cells to toggle binary terrain HIGH/LOW; marbles flow downhill into adjacent low cells; walls and remote-linked anchor pairs add composition. | 2026-05-07T20:47:47Z | (autonomous) |
```
