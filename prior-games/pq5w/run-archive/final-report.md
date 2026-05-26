# Game generation final report

## Generated game
- **ID**: pq5w
- **Source**: `prior-games/pq5w/pq5w.py`
- **Metadata**: `prior-games/pq5w/metadata.json`
- **Lines of code**: 461

## Mechanic
**Twin-Portal Drag** (`portal-pair-relocate`). The playfield contains
exactly two paired portal sprites — an anchor portal A (fixed, dark
ring) and a float portal B (movable, light pink ring) sharing a
matching magenta core that signals their pairing. The player walks
the avatar with arrow keys; stepping onto either portal queues a
teleport that resolves on the next action, sending the avatar to
the paired portal's cell. To relocate B, the player uses a
select-then-place pattern with ACTION6: clicking B's cell selects
it (visible cue — B's four corner pixels tint from pink to
light-blue; the rest of the outer ring and the magenta core stay
unchanged), and a subsequent click on a valid empty floor cell
places B at that cell and deselects. Levels compose as: L1 introduces the walk +
portal-traverse base system (a wall column the only crossing of
which is via the portal pair); L2 adds portal-relocate by sealing
the goal in a walled room with both portals starting inside, so the
player MUST relocate B near the avatar to enter; L3 adds
forbidden-cell-avoid, splitting the room interior with a column of
red-cornered forbidden cells that fail the level on contact — forcing
a SECOND relocate + teleport to bridge sub-area-1 to sub-area-2.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Walk avatar UP one STRIDE-cell |
| ACTION2 | Walk avatar DOWN one STRIDE-cell |
| ACTION3 | Walk avatar LEFT one STRIDE-cell |
| ACTION4 | Walk avatar RIGHT one STRIDE-cell |
| ACTION6 | Click (x, y): select-then-place. Click on B's cell toggles its selected state (its 4 corner pixels tint pink ↔ light-blue); a second click on a valid empty floor cell relocates B there and deselects. Invalid targets and clicks while not selected are no-ops. |

When a teleport is pending, the next action's id is consumed to
resolve the teleport (avatar moves to paired portal's cell, no
other effect).

## Levels

- **L1** — base: walk + portal-traverse. Full-height wall column
  at x=8 splits the playfield; portal pair is the only crossing.
  Witness 5 actions; step budget 30.
- **L2** — adds portal-relocate. Closed walled room sealing both
  portals and the goal; player must select-then-place B outside
  near the avatar to enter the room. Witness 8 actions; step budget 50.
- **L3** — adds forbidden-cell-avoid. Same room + a forbidden
  column at x=8 inside, splitting the interior into sub-areas;
  player must do a second select-then-place + teleport to bridge
  them. Witness 10 actions; step budget 80.

## Novelty note

- **Closest taxonomy entry**: none — no portal-pair mechanic in the
  25 reference games. The flavour-closest is `g50t` (walk-vs-scroll,
  continuous world-shift) but distinguished by pq5w's discrete
  point-to-point pair and click-to-relocate verb.
- **Closest prior-games entry**: `jd4q` (echo-trail-teleport) —
  jd4q teleports back along a fading echo trail, consuming the
  trail. Distinguished by pq5w's persistent 2-endpoint pair the
  player drags via ACTION6 click — no trail, no consumption.

## Index update

Confirmed one row appended to
`prior-games/index.md`:

```
| pq5w | portal-pair-relocate | Twin-Portal Drag — fixed anchor + movable float portal pair; click-relocate B; walk into either portal to teleport; forbidden cells at L3. | 2026-05-10T13:33:24Z | (autonomous) |
```
