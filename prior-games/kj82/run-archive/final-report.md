# Game generation final report

## Generated game
- **ID**: kj82
- **Source**: `prior-games/kj82/kj82.py`
- **Metadata**: `prior-games/kj82/metadata.json`
- **Lines of code**: 730

## Mechanic

**Plank-Pivot Crossing** is a path-walking puzzle on a plane of long
rigid planks pinned at one end by fixed anchors. The player controls
a small pawn that walks one cell per arrow-press but only on cells
covered by a plank. Clicking a plank selects it, and ACTION5 pivots
the active plank 90° clockwise around its anchor end — the plank's
free tip sweeps through a quarter-arc of cells, and any pawn standing
on the plank's body is carried with it into the new orientation.
Level 2 introduces toggleable posts: a solid post in the rotation arc
blocks the pivot until clicked to its hollow state. Level 3 adds
spring pads on planks that, when stood on, launch the pawn along the
underlying plank's axis to reach goal cells planks cannot otherwise
cover. The win condition is to walk the pawn onto the level's goal
tile before a generous step-counter HUD drains.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Walk pawn 1 cell up (north). Rejected (action consumed, no movement) if destination isn't a plank cell or is a blocking-post cell. |
| ACTION2 | Walk pawn 1 cell down (south). Same gating. |
| ACTION3 | Walk pawn 1 cell left (west). Same gating. |
| ACTION4 | Walk pawn 1 cell right (east). Same gating. |
| ACTION5 | Pivot the active plank 90° clockwise around its anchor; the pawn rides if it was on a non-anchor cell. Rejected if the rotation would put a plank cell on a blocking post or off-grid. |
| ACTION6 | Click at display (x, y); on a post: toggle blocking↔permeable; on a plank cell: select that plank (or deselect if already active). |

## Levels

- **Level 1 (32×32, budget 30)**: introduces walking + pivot-with-carry.
  One short plank, no posts/springs, no hazards. Witness solves in 6
  actions.
- **Level 2 (32×32, budget 50)**: introduces toggleable posts. Two
  long planks with a blocking post in the south-arc of the first
  plank — the player must toggle the post to permeable before the
  pivot succeeds. Witness 23 actions.
- **Level 3 (32×32, budget 60)**: introduces the spring-launch pad
  on the second plank. The goal tile is off any plank; the spring
  is the only path. Composes all earlier mechanics. Witness 18
  actions.

## Novelty note

- **Closest taxonomy entry**: `cn04` (rotate-translate-jigsaw).
  Distinguishing rule — cn04 rotates a piece in place around the
  piece's geometric centre and the piece's cells stay the same;
  kj82 rotates a plank around a fixed anchor at one end, sweeping
  the plank's tip through a quarter-arc and changing every cell the
  plank occupies. cn04's verb set is {select, translate, rotate};
  kj82's is {select, rotate, walk-pawn} — translation is not a verb
  in kj82.

- **Closest prior-game entry**: `pz4t` (anchor-pivot-place).
  Distinguishing rule — pz4t is a tiling puzzle with user-chosen
  placement anchors and free piece translation; kj82's anchors are
  level-author-fixed and planks cannot translate. pz4t's goal is to
  cover a target region with placed pieces; kj82's is to walk a
  separate pawn avatar to a destination cell. Verb sets are disjoint
  apart from "rotate".

## Index update

One row appended to `prior-games/index.md`:

```
| kj82 | plank-pivot-walk | Plank-Pivot Crossing — pawn walks long pinned planks; click selects a plank, ACTION5 pivots it 90° around its anchor end; toggleable posts gate rotations; springs launch the pawn along their plank's axis. | 2026-05-07T22:08:44Z | (autonomous) |
```
