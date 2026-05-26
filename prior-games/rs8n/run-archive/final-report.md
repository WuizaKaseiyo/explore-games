# Game generation final report  (revision 4 — L3 redesigned as a 3×5 grid)

## Generated game
- **ID**: rs8n
- **Source**: `prior-games/rs8n/rs8n.py`
- **Metadata**: `prior-games/rs8n/metadata.json`
- **Lines of code**: 654

## Mechanic
A maroon avatar walks a 16-cell-square arena scattered with coloured shape items (hollow pink ring, yellow 2-pixel checkerboard, orange filled blob, blue vertical bar). Pressing an arrow key rotates the avatar to face that direction and walks one cell unless blocked. Pressing ACTION5 fires a small sweeper in the avatar's facing direction; the sweeper picks up every item along that cardinal line until it hits a wall or anchor pillar, then returns and re-deposits the carried items at the cells they came from, in **reversed pickup-order** — a per-segment in-place reversal. Level 2 introduces anchor pillars flanked by access-blocking walls that geometrically force the anchor's mid-line stop to be the only way to partition the row, and the level requires both an east-from-west AND a west-from-east sweep to reverse both segments. Level 3 carries the same row mechanic and adds a perpendicular column with its own anchor + access walls, requiring two further sweeps in the vertical axis (north and south) — the player must compose four sweeps from four geometrically-distinct firing positions.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | Face up; walk one cell up if open (rotate-only if blocked). |
| ACTION2 | Face down; walk one cell down if open. |
| ACTION3 | Face left; walk one cell left if open. |
| ACTION4 | Face right; walk one cell right if open. |
| ACTION5 | Fire a sweeper in the avatar's current facing; multi-tick animation reverses the item ordering along the cardinal segment between the avatar and the first blocker. |

## Levels
- **Level 1** — base dynamic system: walk + line-reverse-sweep on a 4-item row. Witness `[4, 4, 5]` (3 actions, budget 50).
- **Level 2** — adds anchor pillar with access-blocking walls: row 8 is partitioned into two 2-item segments by an anchor at (5,8) flanked by walls at (5,7) and (5,9). Both segments must be reversed, requiring an east-from-west sweep AND a west-from-east sweep with a detour south of the anchor between them. Witness 15 actions, budget 100. Strictly unwinnable without the anchor (the unblocked-row permutation group lacks the target permutation).
- **Level 3** — a 3-row × 5-column grid of 14 items + 1 anchor at the centre cell (7,5). The grid's own geometry blocks the avatar from the anchor cell (every cardinal neighbour is an item). The target requires four full-column reverses (columns 5, 6, 8, 9 — each swapping `(col, 4)↔(col, 6)`) AND both row-5 segment-reverses across the anchor (swapping `(5,5)↔(6,5)` and `(8,5)↔(9,5)`). Column 7 and the row-4/row-6 fixed points of the column reversals are untouched. The player must compose 6 sweeps (4 vertical column sweeps + 2 horizontal row-5 partial sweeps) from 6 firing positions outside the grid's edges, routing the avatar around the grid because items block direct passage. Witness 31 actions, budget 250.

## Novelty note
- **Closest taxonomy entry**: `vc33 row-column-swap-stripe`. Distinguishing rule: vc33 cyclically slides whole rows/columns by one position per click (cyclic translation); `rs8n` reverses an arbitrary cardinal segment (involutive permutation), chosen at fire-time by the avatar's position + facing + anchor placement, on a 2D arena where items are scattered.
- **Closest prior-game entry**: `qx7p column-shift-row-align`. Distinguishing rule: qx7p slides whole vertical colour-band columns past a horizontal scan line (cyclic, single-axis); `rs8n` reverses arbitrary cardinal segments (involutive) chosen at fire-time, and at L3 requires both axes.

The negative-similarity check (per `mechanic-novelty/negative-similarity-check.md`) was performed against r11l, su15, and vt6q L1 frames. No prior overlaps `rs8n`'s candidate L1/L2/L3 visual on three or more of the eight surface dimensions; the core dynamic — segment reversal as the primary verb, in either axis — is implemented by no prior.

## Index update
The index row appended in the original finalize pass remains valid (game-id and family-tag unchanged):

```
| rs8n | line-reverse-sweep | Line-Reverse Sweeper — walking avatar fires sweeps that pick up items along a cardinal line and re-deposit them in reversed order; anchors partition lines so partial-reverses are needed; L3 is a 3×5 grid with a central anchor requiring composition of horizontal and vertical sweeps. | 2026-05-08T19:12:48Z | (autonomous) |
```
