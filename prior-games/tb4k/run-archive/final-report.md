# Game generation final report

## Generated game
- **ID**: tb4k
- **Source**: `prior-games/tb4k/tb4k.py`
- **Metadata**: `prior-games/tb4k/metadata.json`
- **Lines of code**: 390

## Mechanic

The player controls a 1×1×2 brick on a tiled floor. Cardinal arrow
presses tumble the brick end-over-end one step at a time; the brick
has three footprint states — standing (1-cell), lying horizontal
(1×2 east-west), and lying vertical (2×1 north-south) — that
alternate deterministically with each tumble. The level wins when
the brick comes to rest in the **standing** state exactly on the
goal cell. Hole tiles destroy the brick if any part of its
footprint coincides with them (3 lives per level, with respawn at
start). The third level introduces 1-cell-wide bridges flanked by
holes that force the player to keep the brick lying *along* the
bridge axis or standing — lying perpendicular overhangs into the
holes and dies. The combination "my own footprint is the constraint
that interacts with the terrain" is what makes the game read.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Tumble UP (north). |
| ACTION2 | Tumble DOWN (south). |
| ACTION3 | Tumble LEFT (west). |
| ACTION4 | Tumble RIGHT (east). |

No ACTION5/6/7 in use.

## Levels

- **L1** — base dynamic system: just the tumble mechanic (M1). Solid
  floor, no hazards, brick rolls from (3, 3) to (11, 11).
- **L2** — +M2 (hole hazard + 3 lives): a Z-shaped pattern of holes
  blocks the direct east route at row y=3 / y=5 and at (8, 4); brick
  must detour around the hole field while preserving lives.
- **L3** — +M3 (narrow bridge): the middle column-band is entirely
  holes except a 1-cell-wide bridge at y=3; the brick must approach
  the bridge, cross with east-only tumbles, then climb to the goal.

## Novelty note

- **Closest taxonomy entry**: `ka59` (sokoban-explode-chase) — a
  block slides on arrows with possible detonation on contact.
  Distinguishing rule: ka59's block has a **fixed 1-cell footprint**
  and slides one cell per press, with detonation triggered against
  walls; tb4k's brick has **three footprint states** (1×1 / 1×2 /
  2×1) that alternate with each tumble, with hole-fall (geometric
  overhang) as the hazard.
- **Closest prior-games entry**: `hb5n` (polyomino-walker-rotate)
  — a rigid L-polyomino avatar walks via arrows, rotates 90° via
  ACTION5, absorbs adjacent pickups to grow. Distinguishing rule:
  hb5n maintains a **fixed-and-growing** polyomino whose footprint
  only grows monotonically via pickup absorption and target-shape
  matching; tb4k's brick has 3 fixed footprints that cycle
  deterministically with each tumble, with no pickups, no growth,
  no shape-matching — tb4k's target is "stand on this one cell".

## Index update

One row appended to `prior-games/index.md`:

```
| tb4k | tumble-block-stand-fall | Tumble-Block Stand-on-Goal — a 1×1×2 brick tumbles end-over-end; state-alternating footprint must end standing on the goal cell over holes and narrow bridges. | 2026-05-12T11:04:44Z | (autonomous) |
```
